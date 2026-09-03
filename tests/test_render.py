#!/usr/bin/env python3
"""산출물 회귀 고정 (2026-08-19).

**이 목록의 상품은 표다.** 표가 깨지면 값이 맞아도 상품이 아니다. 2026-08-19 사장님 검수에서
7건이 지적됐고, 그중 넷은 사람이 눈으로 봐야만 잡히는 종류였다(볼드 깨짐·링크 없음·
무응답 혼입·분야 없음). 그래서 산출물 자체를 검사한다 — 다음에 조용히 재발하지 않도록.

실행: python3 -m pytest tests/test_render.py -q
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
DOWN = (ROOT / "DOWN.md").read_text(encoding="utf-8")
MEASURED = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
RANKING = json.loads((ROOT / "ranking.json").read_text(encoding="utf-8"))

# 닫는 `**` 앞이 문장부호이고 뒤가 글자면 CommonMark가 강조를 닫지 않는다.
BROKEN_EMPH = re.compile(r'[)\]}"\'.,!?:;][*]{2}[0-9A-Za-z가-힣]')
def _server_rows(md: str) -> list[str]:
    """서버 표(헤더가 `| 서버 |`)의 데이터 줄만. 요약·축별 표는 대상이 아니다."""
    rows, inside = [], False
    for ln in md.splitlines():
        if ln.startswith("| 서버 |"):
            inside = True
            continue
        if inside:
            if not ln.startswith("|"):
                inside = False
            elif not ln.startswith("|---"):
                rows.append(ln.split("|")[1].strip())
    return rows


def test_no_broken_emphasis():
    """볼드가 실제로 닫히는가 — 게시본에서 깨졌던 자리."""
    for name, md in (("README", README), ("DOWN", DOWN)):
        assert not BROKEN_EMPH.findall(md), f"{name}에 깨지는 강조: {BROKEN_EMPH.findall(md)[:3]}"


def test_every_server_row_has_a_link():
    """링크 없는 줄은 독자가 그 서버로 갈 방법이 없다 — 목록의 기능이 죽는다."""
    rows = _server_rows(README) + _server_rows(DOWN)
    assert rows, "서버 표를 못 찾았다 — 파서가 산출물과 어긋났다"
    bad = [r for r in rows if "](" not in r]
    assert not bad, f"링크 없는 항목: {bad[:3]}"


def test_down_servers_are_not_in_the_main_list():
    """무응답은 본문에서 빠져야 한다(별도 DOWN.md)."""
    dead = {i["name"] for i in MEASURED["items"]
            if i.get("remote") and not i["remote"].get("reachable")}
    leaked = [n for n in dead if f"[{n}]" in README]
    assert not leaked, f"무응답이 본문에 남음: {leaked[:3]}"


def test_categories_exist_and_top3_is_capped():
    """분야별로 나뉘고 상위 3개만 먼저 보여야 한다."""
    cats = re.findall(r"^## ([^\n(]+?) \(", README, re.M)
    assert len(cats) >= 4, f"분야 섹션이 너무 적다: {cats}"
    # 순위 분야 섹션만 본다. `측정 못 함`·`DOWN` 같은 구역은 순위표가 아니라 전량 목록이다
    # — 그것까지 3줄로 자르면 "못 본 것을 숨기지 않는다"는 규약과 정면으로 충돌한다.
    ranked_cats = {v["category"] for v in RANKING["items"].values()}
    for block in re.split(r"^## ", README, flags=re.M)[1:]:
        if "|---|" not in block:
            continue
        if not any(block.startswith(c) for c in ranked_cats):
            continue
        # `분야 교정` 표도 순위표가 아니다 — 순위에서 **뺀** 것을 싣는 구역이라
        # 여기까지 3줄로 자르면 뺀 사실 자체가 사라진다.
        head = block.split("<details>")[0].split("**분야 교정")[0]
        rows = [ln for ln in head.splitlines() if ln.startswith("| [") or ln.startswith("| ")]
        rows = [r for r in rows if "](" in r]
        assert len(rows) <= 3, f"Top 3를 넘김({len(rows)}): {block[:40]}"


def test_operator_is_disclosed():
    """우리 서버는 표에 있고 운영자 표시가 붙어야 한다 — 빼는 것도 숨기는 것도 안 된다."""
    assert "korea-realty" in README, "운영자 서버가 표에서 빠졌다"
    assert "🏠" in README, "운영자 표시가 없다"


def test_no_private_or_personal_paths():
    """비공개 저장소·개인 계정 경로가 공개본에 새면 안 된다(2026-08-19 실사고)."""
    for name, md in (("README", README), ("DOWN", DOWN)):
        for leak in ("kwenhwang", "sallim-app/realty-mcp"):
            assert leak not in md, f"{name}에 {leak} 유출"


# ── 순위 신뢰 회귀 (2026-08-19, "순위가 신뢰가 안 가는데?") ──────────────────

# **채점 명단과 이번 주 명단은 어긋나게 되어 있다.** 가동은 매주, 순위는 매월 1일이다
# (README「어떻게 재나」). 그 사이에 채점받은 서버가 죽거나 이름이 바뀌면 이번 주 표에는
# 없다 — 그건 결함이 아니라 이 제품의 설계다. 2026-08-24 첫 주간 회차에서 실제로 둘 다
# 일어났다(obundh 404 · haklaekim→hike-lab 개명).
#
# 그래서 아래 세 검사는 "채점된 전원이 표에 있다"를 요구하지 않는다. 대신 **사라진 것은
# 반드시 설명돼 있어야 한다**를 요구한다 — 조용히 빠지는 것이 진짜 결함이기 때문이다.
def _shown_as(name: str) -> str:
    """채점 당시 이름 → 이번 주 표에 실린 이름(개명 반영)."""
    from observed import RENAMED
    back = {old: new for new, old in RENAMED.items()}
    return back.get(name, name)


def _accounted_for(name: str) -> bool:
    """표에 없다면, 없는 이유가 게시본에 적혀 있는가."""
    shown = _shown_as(name)
    if shown in README:
        return True
    # 무응답으로 빠졌으면 DOWN.md에, 그 외 사유면 「빠진 등수」 줄에 적혀 있어야 한다.
    return name in DOWN or f"위 {name}(" in README or f"위 {shown}(" in README


def test_judged_servers_all_have_tools():
    """심사 대상에 도구 0건이 섞이면 안 된다 — 지표가 비어 비교가 성립하지 않는다.

    이번 주 표에 남아 있는 서버에 한한다. 채점 뒤 죽은 서버까지 요구하면 이 검사는
    "지난달 명단이 이번 주에도 전원 살아 있어야 한다"가 되는데, 그건 참일 수 없다.
    """
    m = {i["name"]: i for i in MEASURED["items"]}
    for v in RANKING["items"].values():
        for t in v["top"]:
            cur = m.get(_shown_as(t["name"]))
            if cur is None:
                assert _accounted_for(t["name"]), \
                    f"{t['name']}이 설명 없이 표에서 사라졌다"
                continue
            rm = cur.get("remote") or {}
            if not (rm.get("reachable")):
                assert _accounted_for(t["name"]), \
                    f"{t['name']}이 무응답인데 그 사실이 게시본에 없다"
                continue
            assert rm.get("tool_count"), f"{t['name']}은 도구 0건인데 심사됐다"


def test_table_order_matches_the_judgement():
    """표의 순서가 심사 순위와 같아야 한다 — 다르면 순위를 표기만 하고 안 지킨 것이다."""
    for v in RANKING["items"].values():
        block = re.split(r"^## ", README, flags=re.M)
        block = [b for b in block if b.startswith(v["category"])]
        if not block:
            continue
        # **표 줄만 본다.** 블록 전체를 문자열로 훑으면 「빠진 등수」 공시에 적힌
        # 이름까지 "표에 있다"로 세어, 사라진 서버가 순서 위반으로 둔갑한다.
        rows = "\n".join(ln for ln in block[0].splitlines() if ln.startswith("| ["))
        pos, kept = [], 0
        for t in sorted(v["top"], key=lambda x: x["rank"]):
            n = _shown_as(t["name"]).split("/")[-1]
            p = rows.find(n)
            if p < 0:
                assert _accounted_for(t["name"]), \
                    f"{v['category']}: {t['name']}이 설명 없이 표에서 사라졌다"
                continue
            kept += 1
            pos.append(p)
        assert kept, f"{v['category']}: 채점된 서버가 표에 하나도 안 남았다"
        assert pos == sorted(pos), f"{v['category']}: 표 순서가 심사 순위와 다름"


def test_every_ranked_server_shows_its_reason():
    """순위에는 근거가 붙어야 한다 — 이유 없는 순위가 신뢰를 깨뜨린 원인이다."""
    for v in RANKING["items"].values():
        for t in v["top"]:
            assert t["why"].strip(), f"{t['name']}에 심사 이유가 없다"
            if t["why"][:20] in README:
                continue
            assert _accounted_for(t["name"]), \
                f"{t['name']}의 이유가 README에 없고 사라진 사유도 없다"


def test_unmeasurable_servers_are_not_ranked():
    """키가 있어야 도구 목록도 못 보는 서버는 순위표에 없어야 한다."""
    ranked = {t["name"] for v in RANKING["items"].values() for t in v["top"]}
    blocked = {i["name"] for i in MEASURED["items"]
               if (i.get("remote") or {}).get("needs_key")}
    assert not (ranked & blocked), f"측정 못 한 서버가 순위에: {ranked & blocked}"


def test_glance_agrees_with_the_category_rankings():
    """첫 화면과 본문이 어긋나면 안 된다.

    2026-08-19 실사고: 순위를 블라인드 심사로 바꾸면서 `한눈에`를 안 고쳐, 지표 정렬 시절의
    축별 1위가 그대로 남았다. 그 결과 첫 화면 1위 셋이 본문에서 각각 3위·3위·2위였다.
    **순위 근거가 둘이면 반드시 어긋난다** — 같은 값에서 나오는지 검사한다.
    """
    block = README.split("## 한눈에")[1].split("\n## ")[0]
    for v in RANKING["items"].values():
        first = next(t["name"] for t in v["top"] if t["rank"] == 1)
        assert first.split("/")[-1] in block, f"{v['category']} 1위({first})가 한눈에 없다"


def test_no_all_empty_columns():
    """모든 줄이 `—`인 열은 정보가 아니라 소음이다(키·무료/전체를 뺀 계기)."""
    rows = _server_rows(README)
    header = next(ln for ln in README.splitlines() if ln.startswith("| 서버 |"))
    cols = [c.strip() for c in header.split("|")[1:-1]]
    body = [ln for ln in README.splitlines() if ln.startswith("| [") and ln.count("|") == len(cols) + 1]
    assert rows and body, "서버 표를 못 찾았다"
    for idx, name in enumerate(cols):
        vals = {r.split("|")[idx + 1].strip() for r in body}
        assert vals != {"—"}, f"'{name}' 열이 전부 비었다 — 열을 빼거나 각주로 내려라"


# ── 분야 교정 (2026-08-19) ────────────────────────────────────────────────
# 수집 검색어가 정한 분야가 실호출로 틀렸음이 드러난 서버들. 남의 분야 질문으로 매긴
# 등수는 그 서버를 잰 값이 아니라 우리 수집기의 오분류다 — 순위에서 빼고 따로 싣는다.

def test_misfiled_quotes_are_verbatim_from_grades():
    """교정 근거가 **채점 파일에 실제로 있는 문장**인가 — 우리가 지어낸 판정이면 안 된다."""
    from observed import MISFILED
    for name, (was, _now, why) in MISFILED.items():
        f = ROOT / "grades" / f"{was}.json"
        assert f.exists(), f"{name}: 채점 파일 없음 {f}"
        blob = f.read_text(encoding="utf-8")
        assert json.dumps(why, ensure_ascii=False)[1:-1] in blob, \
            f"{name}: 근거가 grades/{was}.json에 없다 — {why[:40]}"


def test_misfiled_target_category_is_known():
    """교정된 분야가 우리가 렌더할 수 있는 분야인가 — 아니면 다음 회차에 사라진다."""
    import render_readme
    from observed import MISFILED
    for name, (_was, now, _why) in MISFILED.items():
        assert now in render_readme.CATS, f"{name}: 모르는 분야 {now}"


def test_misfiled_never_ranked():
    """오분류 서버가 순위에 남아 있지 않은가 — 남으면 오심을 그대로 게시한다."""
    from observed import MISFILED
    for v in RANKING["items"].values():
        ranked = {t["name"] for t in v["top"]} | set(v.get("전체순위") or [])
        assert not (ranked & set(MISFILED)), \
            f"{v['category']}: 오분류가 순위에 있다 {ranked & set(MISFILED)}"


def test_misfiled_disclosed_not_deleted():
    """뺀 서버가 README에 그대로 살아 있는가 — 조용히 빼면 독자가 영영 못 본다."""
    from observed import MISFILED
    live = {r["name"] for r in MEASURED["items"]
            if (r.get("remote") or {}).get("reachable") and (r["remote"].get("tool_count") or 0)}
    for name in MISFILED:
        if name in live:
            assert name in README, f"{name}: 순위에서 빼놓고 README에서도 사라졌다"


def test_scope_notes_have_no_broken_table_cells():
    """범위 공시가 표 칸을 깨뜨리지 않는가 — `|`가 들어가면 열이 밀린다."""
    from observed import SCOPE
    for name, note in SCOPE.items():
        assert "|" not in note, f"{name}: 범위 공시에 파이프 문자"


def test_remeasure_channel_is_open():
    """고친 서버가 옛 감점에 묶이지 않게 **신호 받는 창구**가 README에 있는가."""
    assert "## 고쳤다면 다시 잰다" in README
    assert "issues" in README.split("## 고쳤다면 다시 잰다")[1].split("## ")[0], \
        "재측정 요청 경로(이슈 링크)가 없다"


def test_ranking_ratchet_rule_is_published():
    """**우리만 다시 재지 않는다**는 규약이 공개돼 있는가.

    우리는 고칠 때마다 다시 잴 수 있고 남은 못 그런다. 그 비대칭을 적어 두지 않으면
    개별 재측정이 순위에 스며들어 표가 조용히 우리 쪽으로 기운다.
    """
    sec = README.split("## 고쳤다면 다시 잰다")[1].split("## ")[0]
    assert "전원 동시에" in sec and "예외" in sec, "재측정 대칭 규약이 안 적혀 있다"


def test_round_count_is_disclosed():
    """**몇 번 물어본 순위인지**가 표 옆에 적혀 있는가.

    1회짜리 순위는 서버의 성질과 모델의 주사위를 구별하지 못한다(variance/ 실측:
    4개 질문 자리 중 2곳 등급 갈림). 회차수를 안 적으면 독자는 그 등수가 한 번의
    주사위인지 세 번의 합의인지 알 방법이 없다.
    """
    assert "순위는 **실제로 물어본 결과**다" in README
    n = {int(v.get("회차수") or 1) for v in RANKING["items"].values()}
    if n == {1}:
        assert "재현성은 재지 않았다" in README, "1회 회차인데 그 사실을 숨겼다"
    else:
        assert "재현성까지 채점했다" in README


def test_judging_doc_matches_current_method():
    """공개 기준 문서가 **실제로 쓰는 방식**을 적고 있는가.

    2026-08-19에 JUDGING.md가 폐기된 블라인드 심사를 그대로 싣고 있었다 — 독자가
    우리 순위를 재현하려면 이 문서를 따르는데, 그러면 우리가 안 쓰는 방식을 따르게 된다.
    """
    j = (ROOT / "JUDGING.md").read_text(encoding="utf-8")
    assert "실제로 물어보고" in j, "JUDGING.md가 실측 채점 방식을 안 적는다"
    for must in ("3회", "매월 1일", "재현성"):
        assert must in j, f"JUDGING.md에 {must}가 없다"


def test_no_double_emphasis():
    """`****`는 굵게가 아니라 **리터럴 별표**로 렌더된다.

    `emph()` 결과를 다시 `**`로 감싸면 나온다 — 2026-08-19 게시본에
    `****가동 지표는 돌리면 같은 값이 나온다****`로 실제로 나갔다.
    기존 깨진-강조 검사는 '문장부호 뒤 닫는 **' 형태만 봐서 이건 못 잡았다.
    """
    for name, md in (("README", README), ("DOWN", DOWN)):
        assert "****" not in md, f"{name}에 이중 강조(****)가 있다"


def test_judging_doc_does_not_overstate_current_round():
    """공개 기준이 **아직 안 하는 것을 하는 것처럼** 적고 있지 않은가.

    JUDGING.md는 '서버당 3회'라고 쓰는데 지금 게시된 회차는 1회다. 독자가 answers/와
    대조하면 우리가 거짓말한 것이 되므로, 1회인 동안에는 그 사실이 문서에 있어야 한다.
    (2026-08-19: JUDGING.md가 이미 폐기한 방식을 계속 싣고 있던 전례가 있다)
    """
    j = (ROOT / "JUDGING.md").read_text(encoding="utf-8")
    n = {int(v.get("회차수") or 1) for v in RANKING["items"].values()}
    if n == {1}:
        assert "아직 1회짜리" in j, "3회라고만 적고 현행이 1회인 사실을 안 밝혔다"


def test_no_bold_markup_inside_code_fences():
    """코드블록 안의 `**굵게**`는 굵게가 아니라 **리터럴 별표**로 렌더된다."""
    for name in ("README.md", "JUDGING.md"):
        md = (ROOT / name).read_text(encoding="utf-8")
        inside, bad = False, []
        for ln in md.splitlines():
            if ln.startswith("```"):
                inside = not inside
                continue
            if inside and "**" in ln:
                bad.append(ln.strip()[:50])
        assert not bad, f"{name} 코드블록에 마크업: {bad[:2]}"


# ── 문장이 끝나는가 (2026-08-19) ──────────────────────────────────────────
# 오늘 게시본에 이런 것들이 그대로 나갔다: "포털 실물은 행정안전부( · " ·
# "마진 13.07%가 " · "판정조차 못 하고 끝났다(" · "함께 주지 않".
# `why[:200]`이 문장 한가운데를 잘랐고, **사람이 읽기 전까지 아무도 몰랐다.**
# 눈으로 찾은 것을 다시 눈에 맡기지 않는다 — 자르는 자리는 이제 clip()이고,
# clip()이 지키기로 한 성질을 여기서 검사한다.

_ENDS_OK = ("다.", "…", ".", ")", "”", "%", "건", "다", "라")


def _sentence_ends(line: str) -> bool:
    return line.rstrip().endswith(_ENDS_OK)


def test_ranking_lines_end_in_a_finished_sentence():
    """순위 이유 줄이 조사·여는괄호에서 끊기지 않는가."""
    bad = [ln for ln in README.splitlines()
           if re.match(r"^\d+\. \*\*", ln) and not _sentence_ends(ln)]
    assert not bad, f"순위 줄이 문장 중간에서 끝난다: {[b[-45:] for b in bad][:3]}"


def test_glance_reasons_end_in_a_finished_sentence():
    """「한눈에」의 '왜' 칸도 마찬가지 — 여기가 첫 화면이라 더 눈에 띈다."""
    rows, inside = [], False
    for ln in README.splitlines():
        if ln.startswith("| 분야 | 1위 |"):
            inside = True
            continue
        if inside:
            if not ln.startswith("|"):
                break
            if not ln.startswith("|---"):
                rows.append(ln.rstrip().rstrip("|").split("|")[-1].strip())
    assert rows, "「한눈에」 표를 못 찾았다"
    bad = [c for c in rows if not _sentence_ends(c)]
    assert not bad, f"'왜' 칸이 문장 중간에서 끝난다: {[b[-45:] for b in bad][:3]}"


def test_no_unbalanced_bracket_in_table_cells():
    """여는 괄호만 남고 끝나는 칸이 없는가 — 절단의 가장 눈에 띄는 흔적이다."""
    bad = []
    for ln in README.splitlines():
        if not ln.startswith("|") or ln.startswith("|---"):
            continue
        for cell in ln.split("|"):
            if cell.count("(") != cell.count(")") and "http" not in cell:
                bad.append(cell.strip()[:45])
    assert not bad, f"괄호가 안 닫힌 표 칸: {bad[:3]}"


def test_server_names_are_identifiable():
    """순위 줄의 이름이 그 서버를 **특정**하는가.

    `com.aikstockdata/mcp`를 `mcp`로, `app.apick/all`을 `all`로 줄여 싣던 자리.
    꼬리만 남기면 어느 서버인지 알 수 없다.
    """
    names = re.findall(r"^\d+\. \*\*(.+?)\*\*", README, re.M)
    assert names, "순위 줄을 못 찾았다"
    vague = [n for n in names if "/" not in n or len(n) < 6]
    assert not vague, f"어느 서버인지 알 수 없는 이름: {vague}"


# ── 측정일 (2026-08-21, T-2026W34-109) ─────────────────────────────────────
# 게시본이 "마지막 측정 {오늘}"을 `datetime.now()`로 찍고 있었다. 재측정 없이 문서만 다시
# 뽑아도 측정일이 소리 없이 밀리는 구조라, 남의 목록에서 우리가 잡아내는 종류의 부정직
# 공시를 우리가 하고 있었다. 이제 잰 쪽이 박은 날짜만 게시한다 — 그것을 여기에 박는다.

def test_measured_at_존재하고_ISO_날짜다():
    ts = MEASURED.get("measured_at")
    assert ts, "measured.json에 measured_at이 없다 — 렌더가 오늘 날짜로 때우게 된다"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", ts), ts


def test_게시된_측정일이_원자료와_같다():
    """README·DOWN에 적힌 측정일은 전부 measured_at이어야 한다(렌더 날짜 금지)."""
    ts = MEASURED["measured_at"]
    for label, md in (("README.md", README), ("DOWN.md", DOWN)):
        found = set(re.findall(r"\d{4}-\d{2}-\d{2}(?= 기준| 측정 시점| 측정에서| 그 순간)", md))
        assert found, f"{label}에 측정일 문구가 없다"
        assert found == {ts}, f"{label} 측정일 {found} != measured_at {ts}"


def test_패키지축_재측정일은_응답_측정일과_섞지_않는다():
    """--repair-packages는 원격을 안 두드린다 — 같은 날짜로 합치면 하나가 거짓말이 된다."""
    pkg = MEASURED.get("repackaged_at")
    if not pkg or pkg == MEASURED["measured_at"]:
        return
    assert f"마지막 측정 {MEASURED['measured_at']}" in README
    assert f"패키지 축 재측정 {pkg}" in README


def test_렌더는_measured_at_없으면_멈춘다():
    """오늘 날짜로 때우는 폴백이 되살아나지 않게."""
    src = (ROOT / "render_readme.py").read_text(encoding="utf-8")
    body = "\n".join(ln for ln in src.splitlines() if not ln.lstrip().startswith("#"))
    assert "datetime.now" not in body, "렌더가 다시 현재 시각을 측정일로 쓰고 있다"
    assert 'd.get("measured_at")' in body


# ── 2026-08-24 주간 회차에서 실제로 잡힌 것들 ──────────────────────────────

def test_losing_axes_are_actually_measured():
    """**우리가 지는 축이 비어 있으면 게시하면 안 된다**(PROTOCOL.md ②).

    실사고 2026-08-24: 주간 회차 명령표에 `measure.py --measure-axes`가 빠져 있었다.
    `measure.py`는 measured.json을 처음부터 다시 쓰므로 축이 통째로 사라졌는데, 렌더는
    그 빈 값을 0으로 세어 **「배포판 확인 0건 · 라이선스 확인 못 함 241건」**을 뽑았다.
    남의 저장소 241개를 '라이선스 없음'으로 낙인찍는 문장이고, 0건은 측정 결과처럼
    보이기 때문에 아무도 안 멈춘다. 값이 아니라 **존재**를 검사한다.
    """
    assert MEASURED.get("axes_at"), "measured.json에 axes_at이 없다 — --measure-axes를 안 돌렸다"
    n = sum(1 for i in MEASURED["items"] if i.get("open_source"))
    assert n, "open_source 축이 한 건도 없다 — 빈 축을 0건으로 게시하려던 참이다"
    assert "라이선스 확인 못 함 0건" not in README


def test_down_addresses_are_not_truncated():
    """**무응답 표의 주소를 자르지 않는다.**

    이 표의 주장은 "이 주소가 응답하지 않았다"인데, 잘린 주소는 우리가 부른 주소가
    아니다. 실측 2026-08-24: `…up.railway.` `…hf.sp`처럼 도메인 한가운데서 끊긴 채
    게시돼 있었다 — 운영자는 무엇을 고칠지 못 보고, 독자는 우리가 애초에 엉뚱한 데를
    두드린 것인지 확인할 수 없다.
    """
    urls = re.findall(r"\| `(https?://[^`]*)` \|", DOWN)
    assert urls, "DOWN.md에서 주소 칸을 못 찾았다 — 표 구조가 바뀌었다"
    for u in urls:
        real = {(i.get("remote") or {}).get("url") for i in MEASURED["items"]}
        assert u in real, f"게시된 주소가 측정한 주소와 다르다(절단 의심): {u}"


def test_renamed_servers_keep_their_rank_and_say_so():
    """**개명은 죽음이 아니다** — 그리고 조용히 이어 붙이지도 않는다.

    실사고 2026-08-24: haklaekim/public-data-lens가 GitHub 404가 되고
    hike-lab/public-data-lens가 나타났다(리디렉트 없음). 같은 주소를 부르는 같은
    서버인데 이름으로 키를 잡는 순위·범위 공시가 전부 끊겨, 그 분야 1위가 표에서
    사라질 뻔했다. 서버가 나빠져서가 아니라 우리 잣대가 이름에 묶여 있어서다.
    """
    from observed import RENAMED
    for new, old in RENAMED.items():
        if new not in README:
            continue
        assert f"`{old}` → `{new}`" in README, f"{new}의 개명 사실이 공시되지 않았다"
        # 옛 이름이 순위에 있었으면 새 이름이 그 자리를 이어받아야 한다.
        ranked_old = any(t["name"] == old
                         for v in RANKING["items"].values() for t in v["top"])
        if ranked_old:
            assert re.search(rf"^\d+\. \*\*{re.escape(new)}\*\*", README, re.M), \
                f"{new}가 등수를 잇지 못했다"


def test_this_index_does_not_list_itself():
    """이 목록 자신은 후보가 아니다.

    실측 2026-08-24: 저장소를 공개한 다음 주, GitHub 검색('mcp 한국')이 우리 색인
    저장소를 잡아 keep으로 올렸다. 원격도 패키지도 없으니 "가동 여부를 못 쟀다"로
    실려, 목록이 자기 자신을 미측정 서버로 게시하게 된다.
    """
    names = {i["name"] for i in MEASURED["items"]}
    assert "sallim-app/korea-mcp-index" not in names
