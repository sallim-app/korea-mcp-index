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

def test_judged_servers_all_have_tools():
    """심사 대상에 도구 0건이 섞이면 안 된다 — 지표가 비어 비교가 성립하지 않는다."""
    m = {i["name"]: i for i in MEASURED["items"]}
    for v in RANKING["items"].values():
        for t in v["top"]:
            rm = (m.get(t["name"]) or {}).get("remote") or {}
            assert rm.get("tool_count"), f"{t['name']}은 도구 0건인데 심사됐다"


def test_table_order_matches_the_judgement():
    """표의 순서가 심사 순위와 같아야 한다 — 다르면 순위를 표기만 하고 안 지킨 것이다."""
    for v in RANKING["items"].values():
        names = [t["name"].split("/")[-1] for t in sorted(v["top"], key=lambda x: x["rank"])]
        block = re.split(r"^## ", README, flags=re.M)
        block = [b for b in block if b.startswith(v["category"])]
        if not block:
            continue
        pos = [block[0].find(n) for n in names]
        assert all(p >= 0 for p in pos), f"{v['category']}: 표에 없는 심사 항목"
        assert pos == sorted(pos), f"{v['category']}: 표 순서가 심사 순위와 다름"


def test_every_ranked_server_shows_its_reason():
    """순위에는 근거가 붙어야 한다 — 이유 없는 순위가 신뢰를 깨뜨린 원인이다."""
    for v in RANKING["items"].values():
        for t in v["top"]:
            assert t["why"].strip(), f"{t['name']}에 심사 이유가 없다"
            assert t["why"][:20] in README, f"{t['name']}의 이유가 README에 안 실렸다"


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
