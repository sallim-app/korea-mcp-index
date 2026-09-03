#!/usr/bin/env python3
"""측정값 → README (2026-08-19 재작성, D-2026W34-21/22).

**사람이 순위를 손으로 쓰지 않는다.** 손으로 쓰면 재현이 끊기고, 재현이 끊기면 이해충돌을
방어할 수단이 사라진다. 이 파일이 만드는 표는 measured.json + classification.json의 함수다.

2026-08-19 재작성 계기(사장님 검수 7건): 첫 서버가 나오기까지 30줄이 해명이었고, 순위도
분야도 없었고, 무응답이 섞여 있었고, 링크 없는 줄이 있었고, 볼드가 깨졌다.
벤치마크(punkpeye/awesome-mcp-servers)의 순서를 따른다 — 한 줄 정체 → 목차 → 표기 → 분야별.
**방법론과 한계는 맨 아래로 내린다.** 중요하지 않아서가 아니라, 목록이 먼저 답을 줘야 해서다.

실행: python3 render_readme.py [--lang en]
"""
import argparse
import collections
import json
import re
import sys

from observed import MISFILED, RENAMED, SCOPE

OURS = ("app.sallim/", "sallim-app/")
# 웹판(2026-08-29). 저장소 README는 검색엔진이 사실상 안 읽는다 — 그래서 같은 원자료에서
# 정적 HTML을 따로 뽑아 발행한다(`render_site.py`). 두 문서는 **같은 함수의 두 출력**이다.
SITE = "https://mcp-index.sallim.app"
CATS = ["공공데이터·행정", "법령·판례", "금융·증시", "부동산", "세금·재정", "지도·주소",
        "날씨·환경", "교통·이동", "의료·복지", "교육·문화", "한국어·언어", "커머스·생활",
        "미디어·뉴스", "핀테크·인증", "디렉토리·개발자도구", "기타"]
CAT_EN = {"공공데이터·행정": "Public Data", "법령·판례": "Law", "금융·증시": "Finance",
          "부동산": "Real Estate", "세금·재정": "Tax", "지도·주소": "Maps", "날씨·환경": "Weather",
          "교통·이동": "Transit", "의료·복지": "Health", "교육·문화": "Education",
          "한국어·언어": "Korean NLP", "커머스·생활": "Commerce", "미디어·뉴스": "Media",
          "핀테크·인증": "Fintech", "디렉토리·개발자도구": "Directory", "기타": "Other"}

# 닫는 `**` 앞이 문장부호이고 뒤가 글자면 CommonMark가 강조를 닫지 않는다.
# `**"지금 되냐"**를` 이 형태로 실제로 깨져서 게시됐다(2026-08-19).
BROKEN_EMPH = re.compile(r'[)\]}"\'.,!?:;][*]{2}[0-9A-Za-z가-힣]')
# `****`는 리터럴 별표로 렌더된다 — `emph()` 결과를 `**`로 또 감싸면 나온다(실제 사고).
DOUBLE_EMPH = re.compile(r'\*{4,}')


# ── 판정 어휘 세 갈래 (2026-09-03, T-2026W35-119) ───────────────────────────
# **두드려서 못 받은 것을 '죽음'이라 쓰지 않는다.** 종전 산출물은 `reachable=False`를
# 통째로 "응답 없음"으로 게시했고, 그 명단에는 우리 두드리개가 MCP 규격(initialize
# 핸드셰이크·307 추적·SSE 전송)을 안 지켜서 거절당한 서버가 섞여 있었다 — 남의 제품에
# 우리 결함으로 사망 선고를 한 셈이다. 어휘를 셋으로 가른다.
#   live       살아있음 확인 — MCP 응답을 실제로 받았다
#   unverified 확인 못 함   — 우리 호출로 확인이 안 됐다. **죽었다는 뜻이 아니다**
#   down       죽음 확인    — 호스트가 없다는 직접 증거(DNS 미해결·연결 거부)가 있다
# 라벨 정본은 measure.STATUS_LABEL이고 tests/test_mcp_probe.py가 둘이 어긋나면 실패한다.
STATUS_LABEL = {"live": "살아있음 확인", "unverified": "확인 못 함", "down": "죽음 확인"}
_DOWN_SIGNS = ("Name or service not known", "nodename nor servname",
               "Temporary failure in name resolution", "No address associated",
               "Connection refused", "ConnectionRefusedError")


def status_of(rec: dict) -> str:
    """레코드의 세 갈래 판정. 옛 회차 원자료(`status` 없음)도 안전하게 읽는다."""
    rm = rec.get("remote") or {}
    st = rm.get("status")
    if st in STATUS_LABEL:
        return st
    if rm.get("reachable"):
        return "live"
    why = f'{rm.get("why") or ""} {rm.get("error") or ""}'
    return "down" if any(x in why for x in _DOWN_SIGNS) else "unverified"


def emph(text: str) -> str:
    """강조를 만드는 유일한 경로. 끝 문장부호는 강조 **밖으로** 밀어낸다."""
    t = text.rstrip()
    tail = ""
    while t and t[-1] in ')]}"\'.,!?:;':
        tail = t[-1] + tail
        t = t[:-1]
    return f"**{t}**{tail}" if t else text


def clip(text: str, n: int) -> str:
    """**문장 한가운데서 자르지 않는다**(2026-08-19 눈으로 읽고 고침).

    종전엔 `why[:200]`·`why[:60]`로 잘랐고 그 결과가 게시본에 그대로 나갔다 —
    "이 데이터셋은  · " · "포털 실물은 행정안전부( · " · "마진 13.07%가 " ·
    "판정조차 못 하고 끝났다(". 괄호를 열고 끝나거나 조사에서 끊긴 문장은
    정보가 아니라 사고로 읽힌다.

    문장이 끝나는 자리(`다.`·`.`)를 먼저 찾고, 너무 짧게 잘릴 때만 어절 경계에서
    자르고 말줄임을 붙인다. 말줄임이 붙었다는 것 자체가 "뒤가 더 있다"는 신호다.
    """
    t = " ".join((text or "").split())
    if len(t) <= n:
        return t
    head = t[:n]
    for end in ("다. ", ". ", "다.", "."):
        i = head.rfind(end)
        if i >= n * 0.55:
            return t[:i + len(end)].strip()
    i = head.rfind(" ")
    out = head[:i] if i >= n * 0.5 else head
    # **여는 괄호만 남기고 끝내지 않는다.** 위 어절 절단이 괄호 안에서 멈추면
    # "…전달 형식에 있다(발췌가 조 전문의 앞머리에서 잘리고…"가 되어 괄호가 안 닫힌다
    # (회귀 test_no_unbalanced_bracket_in_table_cells가 실제로 이걸 잡았다 —
    #  내 눈은 못 봤다). 짝이 안 맞으면 마지막 여는 괄호 앞으로 물러선다.
    for op, cl in (("(", ")"), ("「", "」"), ("『", "』"), ("[", "]"), ("“", "”")):
        while out.count(op) > out.count(cl):
            out = out[:out.rfind(op)]
    return out.rstrip(" ,·—(「『[") + "…"


def disp(name: str) -> str:
    """표에 쓸 서버 이름. **꼬리만 남기지 않는다.**

    종전엔 `name.split("/")[-1]`이라 `com.aikstockdata/mcp`가 그냥 `mcp`,
    `app.apick/all`이 `all`로 나갔다 — 어느 서버인지 알 수 없는 이름이다.
    역DNS 형식은 마지막 라벨과 꼬리를 붙여 살린다(`aikstockdata/mcp`).
    """
    if "/" not in name:
        return name
    owner, tail = name.rsplit("/", 1)
    if "." in owner:
        owner = owner.split(".")[-1]
    return f"{owner}/{tail}"


def link(rec: dict) -> str:
    """이름에 걸 주소. 저장소 → 공식 웹 → 엔드포인트 도메인 순으로 물러선다.

    응답 33건 중 11건이 저장소 주소가 없었다(레지스트리 등록에 repository 필드가 없음).
    링크 없는 줄은 독자가 그 서버로 갈 방법이 없다는 뜻이라 목록의 기능이 죽는다.
    """
    name = rec["name"]
    for u in (rec.get("repo_url"), rec.get("website_url")):
        if u:
            return f"[{name}]({u})"
    ep = (rec.get("remote") or {}).get("url") or ""
    if ep:
        root = "/".join(ep.split("/")[:3])
        return f"[{name}]({root})"
    return name


def q(rec: dict, key: str, default="—"):
    return ((rec.get("remote") or {}).get("quality") or {}).get(key, default)


def renamed_note(name: str, en: bool, ranked: bool) -> str:
    """**개명을 숨기지 않는다.** 조용히 이어 붙이면 그 판정이 새 이름으로 측정된 것처럼 읽힌다.

    독자가 채점 근거(grades/·총평)와 「분야 교정」에서 만나는 이름은 **옛 이름**이다.
    그래서 이었다는 사실을 그 서버가 나오는 자리마다 적는다 — 등수를 받은 서버뿐 아니라
    분야 교정만 붙은 서버도 마찬가지다(2026-08-31: academyinfo가 그 자리에서 빠졌다).

    표현이 중립인 이유: 개명에는 **저장소 이전**(public-data-lens)과 **표기 출처 변경**
    (레지스트리 이름이 GitHub 경로를 대체 — academyinfo)이 섞여 있다. "저장소가 옮겨졌다"로
    통일하면 후자에 대해 사실이 아닌 것을 적게 된다.
    """
    rn = RENAMED.get(name)
    if not rn:
        return ""
    if en:
        tail = "; the rank was earned under the old name" if ranked else ""
        return f"<br><sub>Previously listed as `{rn}` → `{name}` — same server{tail}</sub>"
    tail = "고, 등수는 옛 이름으로 받은 것이다" if ranked else "다"
    return f"<br><sub>지난 회차 표기 `{rn}` → `{name}` — 같은 서버로 이었{tail}</sub>"


def row(rec: dict, en=False, err_of: dict | None = None) -> str:
    rm = rec["remote"]
    mark = " 🏠" if rec["name"].startswith(OURS) else ""
    warm, cold = rm.get("warm_ms"), rm.get("cold_ms")
    slow = cold and warm and cold > warm * 3
    pd = rec.get("paid_disclosure") or {}
    paid = f" <sub>무료 {pd.get('free')}/{pd.get('total')}</sub>" if pd.get("disclosed") else ""
    # **무엇을 주는 서버인지**를 이름 밑에 붙인다. 카탈로그형에게 값을 묻거나 집계
    # 통계표에서 개별 실거래를 찾는 것은 서버 탓이 아닌데, 표만 보면 그걸 알 수 없다.
    sc = SCOPE.get(rec["name"])
    scope = f"<br><sub>{sc}</sub>" if sc else ""
    scope += renamed_note(rec["name"], en, ranked=True)
    return (f"| {link(rec)}{mark}{paid}{scope} | {rm.get('tool_count') or '—'} | {warm or '—'} | "
            f"{emph(str(cold)) if slow else (cold or '—')} | "
            f"{q(rec, 'described_pct')}% | {q(rec, 'annotated_pct')}% | "
            f"{(err_of or {}).get(rec['name'], '—')} |")


def head(en=False) -> list[str]:
    # `키`와 `무료/전체`를 열에서 뺐다(2026-08-19). 측정 가능한 것만 표에 남기니 `키`는
    # 21줄 전부 `—`였고, `무료/전체`는 스스로 공시하는 서버가 우리뿐이라 20/21이 `—`였다.
    # **빈 열은 정보가 아니라 소음이고, 그것을 설명하는 범례는 독자의 첫 화면을 잡아먹는다.**
    # 유료 공시는 각주로 내린다.
    # `사실오류`를 표에 낸다. 순위 위쪽에 있다고 흠이 가려지면 안 된다 — 1위 서버에도
    # 오류가 있으면 그것이 먼저 보여야 한다(2026-08-19: 실제 답변 채점 도입).
    return ["| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |" if not en else
            "| Server | Tools | Warm | Cold | Desc | Annot | Errors |",
            "|---|---|---|---|---|---|---|"]


def dedupe_by_endpoint(items: list) -> tuple[list, int]:
    """**같은 주소를 부르면 같은 서버다** — 표에 두 줄로 실으면 안 된다.

    수집 시점 중복 제거로는 못 잡는다: 레지스트리 항목은 처음부터 주소를 갖지만 GitHub
    항목은 보강 단계에서야 README로 주소가 붙는다. 실제로 우리 contract-compass가 두 줄로
    실렸고, 그중 하나는 레지스트리 옛 판이 들고 있던 **이전 전 저장소 경로**였다.
    합칠 때 저장소 주소는 조직 경로를 우선한다(이전 리디렉트도 200을 주므로 200은 최신의 증거가 아니다).
    """
    by_ep: dict[str, dict] = {}
    out, merged = [], 0
    for it in items:
        ep = ((it.get("remote") or {}).get("url") or "").split("?")[0].rstrip("/").lower()
        if not ep:
            out.append(it)
            continue
        prev = by_ep.get(ep)
        if prev is None:
            by_ep[ep] = it
            out.append(it)
            continue
        merged += 1
        if it.get("self_hostable") and not prev.get("self_hostable"):
            prev["self_hostable"] = True
        if not prev.get("website_url") and it.get("website_url"):
            prev["website_url"] = it["website_url"]
        cand, cur = it.get("repo_url") or "", prev.get("repo_url") or ""
        if cand and (not cur or ("sallim-app/" in cand and "sallim-app/" not in cur)):
            prev["repo_url"] = cand
    return out, merged


def write_down(dead: list, ts: str) -> None:
    """무응답을 본문에서 분리한다(사장님 지적 2026-08-19).

    본문에 섞어 두면 독자가 쓸 수 있는 서버와 못 쓰는 서버를 눈으로 갈라야 한다.
    그렇다고 버리지도 않는다 — "등록은 가동의 증거가 아니다"가 이 목록의 존재 이유다.

    **주장의 세기를 갈라 싣는다.** 관리자가 레지스트리에 직접 등록한 주소가 응답하지 않는 것과,
    우리가 README에서 뽑은 추정 주소가 응답하지 않는 것은 무게가 다르다. 후자는 우리가 주소를
    잘못 짚었을 수 있다 — 남의 제품에 사망 선고를 하는 자리라 그 구분을 지운 채 실으면 안 된다.
    """
    o: list[str] = []
    o.append("# 확인하지 못한 서버")
    o.append("")
    o.append(f"{ts} 측정에서 **우리가 살아있음을 확인하지 못한** 목록. "
             "**사망 명단이 아니다** — 확인 못 함(unverified)과 죽음 확인(down)은 다른 값이고, "
             "이 문서는 그 둘을 갈라 싣는다.")
    o.append("")
    o.append("`죽음 확인`은 호스트가 없다는 직접 증거(DNS에 이름 없음·연결 거부)가 있을 때만 "
             "붙인다. 그 밖의 전부 — 4xx·5xx·타임아웃·TLS 오류 — 는 `확인 못 함`이다. "
             "우리 두드리개가 못 본 것을 남의 사망으로 적지 않기 위해서다.")
    o.append("")
    o.append("고쳤거나 우리가 주소를 잘못 짚었다면 이슈로 알려 달라. 다음 회차에 다시 잰다.")
    o.append("")
    downs = [r for r in dead if status_of(r) == "down"]
    unver = [r for r in dead if r not in downs]
    strong = [r for r in unver if r.get("addr_registered")]
    weak = [r for r in unver if r not in strong]
    for title, group, note in (
            ("죽음 확인 — 호스트가 없다", downs,
             "이 줄만 **우리가 사망을 주장하는 것**이다. 근거는 DNS 미해결·연결 거부처럼 "
             "우리 클라이언트 규격과 무관한 신호뿐이다."),
            ("확인 못 함 — 등록된 주소", strong,
             "관리자가 공식 레지스트리에 **직접 등록한** 주소다. 주장이 강하지만 "
             "**그래도 사망 판정이 아니다** — 우리가 확인하지 못했다는 뜻이다."),
            ("확인 못 함 — 추정 주소", weak,
             "우리가 README에서 뽑은 **추정** 주소다. **우리가 주소를 잘못 짚었을 수 있다** — "
             "그 서버가 죽었다는 뜻으로 읽지 마라."),
    ):
        if not group:
            continue
        o.append(f"## {title} — {len(group)}건")
        o.append("")
        o.append(note)
        o.append("")
        o.append("| 서버 | 판정 | 증상 | 주소 |")
        o.append("|---|---|---|---|")
        for r in group:
            rm = r["remote"]
            why = rm.get("why") or f"HTTP {rm.get('http')}"
            # **주소는 자르지 않는다**(2026-08-24). 이 표의 주장은 "이 주소가 응답하지
            # 않았다"인데, 60자에서 잘린 주소는 우리가 부른 주소가 아니다 — 운영자는
            # 무엇을 고쳐야 할지 못 보고, 독자는 우리가 애초에 엉뚱한 데를 두드린 것인지
            # 확인할 수 없다. 남의 제품에 사망 선고를 하는 표에서 근거를 잘라 싣는 셈이다.
            # 실측: `…up.railway.` `…hf.sp`처럼 도메인 한가운데서 끊긴 채 게시돼 있었다.
            # 증상 쪽은 2026-08-19에 도입한 clip()으로 통일한다(여기만 `[:60]`이 남아
            # `Name or service not know`로 단어 중간에서 끊겼다).
            o.append(f"| {link(r)} | {STATUS_LABEL[status_of(r)]} | {clip(why, 80)} | "
                     f"`{rm.get('url') or ''}` |")
        o.append("")
    o.append("---")
    o.append("")
    o.append("[← 목록으로](README.md)")
    open("DOWN.md", "w", encoding="utf-8").write("\n".join(o) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="ko", choices=["ko", "en"])
    a = ap.parse_args()
    en = a.lang == "en"

    d = json.load(open("measured.json", encoding="utf-8"))
    cls = {v["name"]: v for v in json.load(open("classification.json", encoding="utf-8"))["items"].values()}
    try:
        src = {i["name"]: i for i in json.load(open("candidates_filtered.json", encoding="utf-8"))["items"]}
    except OSError:
        src = {}

    try:
        rk = json.load(open("ranking.json", encoding="utf-8"))["items"]
    except OSError:
        rk = {}
    rank_of = {}          # name → (순위, 이유)
    err_of = {}           # name → 채점에서 나온 사실오류 건수
    cat_note = {}         # 분야 → 총평
    cat_runs = {}         # 분야 → 그 분야를 몇 번 물어봤나(회차수)
    for v in rk.values():
        cat_note[v["category"]] = v.get("note", "")
        cat_runs[v["category"]] = int(v.get("회차수") or 1)
        for t in v["top"]:
            rank_of[t["name"]] = (t["rank"], t.get("why", ""))
            if t.get("사실오류") is not None:
                err_of[t["name"]] = t["사실오류"]
    # **개명한 서버의 등수를 잇는다**(observed.RENAMED). 채점은 옛 이름으로 받았고
    # 측정은 새 이름으로 하므로, 잇지 않으면 그 분야 1위가 표에서 통째로 사라진다 —
    # 서버가 나빠져서가 아니라 저장소 주인이 바뀌어서. 그건 측정이 아니라 우리 착오다.
    for _new, _old in RENAMED.items():
        if _old in rank_of and _new not in rank_of:
            rank_of[_new] = rank_of[_old]
        if _old in err_of and _new not in err_of:
            err_of[_new] = err_of[_old]
    # 분야별 **채점된 명단**을 따로 들고 있는다. 가동은 매주·순위는 매월이라 두 명단은
    # 어긋나게 되어 있다 — 채점 뒤에 죽거나 이름이 바뀐 서버가 표에서 그냥 사라지면
    # 순위가 "1. … 3. …"처럼 이가 빠진 채 게시된다. 빠진 자리를 설명하려고 남긴다.
    graded_of: dict[str, list[tuple[int, str]]] = {}
    for v in rk.values():
        graded_of.setdefault(v["category"], []).extend(
            (t["rank"], t["name"]) for t in v["top"])

    items, merged = dedupe_by_endpoint(d["items"])
    for it in items:
        s0 = src.get(it["name"]) or {}
        it.setdefault("website_url", s0.get("website_url"))
        # **주소의 출처를 측정본까지 끌고 온다.** 관리자가 레지스트리에 등록한 주소가
        # 응답하지 않는 것과, 우리가 README에서 추정한 주소가 응답하지 않는 것은
        # 주장의 무게가 다르다. 이 구분이 없으면 남의 제품에 과한 낙인을 찍는다.
        r0 = (s0.get("remotes") or [{}])[0]
        it["addr_registered"] = bool(r0.get("url")) and r0.get("confidence") != "readme"
    rem = [r for r in items if r.get("remote")]
    live = [r for r in rem if r["remote"].get("reachable")]
    dead = [r for r in rem if not r["remote"].get("reachable")]
    # 데이터 제공형이 아닌 것은 이 목록의 주제가 아니다 — 조용히 버리지 않고 아래에 센다.
    off = [r for r in live if cls.get(r["name"]) and not cls[r["name"]]["is_data_provider"]]
    live = [r for r in live if r not in off]
    # **비교 가능한 것만 순위에 올린다.** 키가 있어야 도구 목록도 못 보는 서버(401/403)와
    # 규격 이탈 서버는 지표가 전부 비어 있어 비교가 성립하지 않는다 — 표에 섞으면
    # 순위가 희석되고 독자는 왜 `—`뿐인지 모른다. 버리지 않고 별도 구역으로 보낸다.
    unmeasured = [r for r in live if not (r["remote"].get("tool_count") or 0)]
    live = [r for r in live if r not in unmeasured]

    # 2026-08-21(T-2026W34-109): 여기가 `datetime.now(UTC)`였다 — **재측정 없이 문서만 다시
    # 뽑아도 게시된 "마지막 측정"이 오늘로 밀렸다.** 게시본이 08-19라 적힌 채 원자료는 08-20인
    # 어긋남도 그래서 났다. 이제 잰 쪽(measure.py)이 산출물에 박은 날짜만 읽는다. 없으면 오늘로
    # 때우지 않고 **멈춘다** — 모르는 날짜를 지어내느니 렌더가 실패하는 편이 정직하다(fail-closed).
    ts = d.get("measured_at")
    if not ts:
        print("생성 중단 — measured.json에 `measured_at`이 없다. "
              "`python3 measure.py`로 다시 재거나 실제 측정일을 채워 넣어라 "
              "(렌더 날짜를 측정일로 게시하지 않는다).", file=sys.stderr)
        return 1
    # 패키지 축만 다시 잰 회차는 응답 측정일과 다르다 — 합치면 둘 중 하나가 거짓말이 된다.
    pkg_ts = d.get("repackaged_at")
    # 2026-08-24: 같은 fail-closed를 **우리가 지는 축**에도 건다. `measure.py`(축 없이)는
    # measured.json을 처음부터 다시 쓰므로 `--measure-axes`를 빠뜨린 회차는 open_source·
    # self_hosting이 통째로 빈다. 그런데 렌더는 그걸 0으로 세어 **"배포판 확인 0건 ·
    # 라이선스 확인 못 함 241건"**을 게시했다 — 남의 저장소 241개에 대한 거짓 주장이고,
    # PROTOCOL.md가 "회차마다" 재기로 고정한 축이 조용히 사라진 것이다. 0건은 측정 결과처럼
    # 보이기 때문에 아무도 안 멈춘다. 그래서 멈춘다.
    if not d.get("axes_at") or not any(i.get("open_source") for i in d["items"]):
        print("생성 중단 — 우리가 지는 축(오픈소스·셀프호스팅)이 measured.json에 없다. "
              "`python3 measure.py --measure-axes`를 돌려라. 빈 축을 0건으로 게시하면 "
              "남의 저장소를 '라이선스 없음'으로 낙인찍는다(PROTOCOL.md ②).", file=sys.stderr)
        return 1
    out: list[str] = []
    A = out.append

    A("[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) "
      "[![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)")
    A("")
    A("# 한국 데이터 MCP — 실측 목록" if not en else "# Korean Data MCP — Measured Index")
    A("")
    A("> 한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다."
      if not en else
      "> We actually connect to every Korean data MCP server, measure it, and publish the numbers.")
    A("")
    # **셋을 갈라 적는다**(2026-09-03, T-2026W35-119). "응답하지 않았다"는 두 갈래
    # 어휘였고, 그 한 단어가 우리 두드리개의 한계를 남의 사망으로 옮겨 적었다.
    n_down = len([r for r in dead if status_of(r) == "down"])
    n_unver = len(dead) - n_down
    # **살아있음 = 주소를 확인한 것 중 죽지 않은 전부**다. 아래 표의 「비교 가능」은
    # 주제 밖·키 필요를 뺀 부분집합이라 이 자리에 쓰면 재현 검사와 어긋난다.
    n_live = len(rem) - len(dead)
    A(f"다른 목록은 “있다”를 말한다. 이 목록은 {emph('지금 되냐')}를 잰다. "
      f"{ts} 기준 주소를 확인한 {len(rem)}건 중 {emph(f'{n_live}건이 살아있음 확인')}, "
      f"{n_unver}건은 {emph('확인 못 함')}, {n_down}건만 {emph('죽음 확인')}이다. "
      f"확인 못 함은 사망이 아니다 — 우리가 못 본 것과 그쪽이 없는 것은 다르다."
      if not en else
      f"Other lists tell you a server exists. This one tells you whether it {emph('works right now')}. "
      f"As of {ts}, of {len(rem)} addresses probed, {n_live} were "
      f"{emph('confirmed live')}, {n_unver} {emph('unverified')}, and only {n_down} "
      f"{emph('confirmed down')}. Unverified is not dead — it means we could not confirm it.")
    A("")
    A(f"> **웹판** <{SITE}> — 같은 값을 분야별·서버별 주소로 갈라 놓았다. "
      f"기계가 읽을 것은 [index.json]({SITE}/index.json)·[llms.txt]({SITE}/llms.txt)."
      if not en else
      f"> **Web edition** <{SITE}> — same numbers, one URL per category and per server. "
      f"Machine-readable: [index.json]({SITE}/index.json) · [llms.txt]({SITE}/llms.txt).")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| 비교 가능한 서버 | {emph(str(len(live)))}건 |")
    A(f"| 응답했으나 못 잼(키 필요·규격 이탈) | {len(unmeasured)}건 |")
    A(f"| 확인 못 함(우리 호출로 확인 실패 — {emph('사망 아님')}) | "
      f"{n_unver}건 → [DOWN.md](DOWN.md) |")
    A(f"| 죽음 확인(DNS 미해결·연결 거부) | {n_down}건 → [DOWN.md](DOWN.md) |")
    A(f"| 주제 밖(데이터 제공형 아님) | {len(off)}건 |")
    # 2026-08-20(T-2026W34-107): **설치형은 이 표에 자리가 없었다.** 원격 주소가 없는 서버는
    # `tools/list`로 잴 수 없어 측정 항목 `installable`을 재 두고도 게시하지 않았고(소비처 0),
    # 그래서 "저장소는 있는데 설치가 안 되는 것"이 목록에 드러나지 않았다 — 이 목록을 만든
    # 이유 그대로다. 세 갈래로 갈라 적는다: 확인 / 배포 없음 / **못 쟀다**. 셋째를 둘째에
    # 합치면 우리 파서의 실패가 남의 서버의 결함으로 게시된다(기치② 못 봄 ≠ 없음).
    inst = [r for r in items if not r.get("remote") and r.get("package")]
    ipub = [r for r in inst if r["package"].get("installable") is True]
    inone = [r for r in inst if r["package"].get("installable") is False]
    iunk = [r for r in inst if r["package"].get("installable") is None]
    if inst:
        A(f"| 설치형(원격 주소 없음) | 배포 확인 {emph(str(len(ipub)))}건 · "
          f"배포판 없음 {len(inone)}건 · 이름을 못 읽어 미측정 {len(iunk)}건 |")
    A("")

    # ── 목차 ──
    cats_live = [c for c in CATS if any(cls.get(r["name"], {}).get("category") == c for r in live)]
    A("* [왜 만드나](#왜-만드나)")
    A("* [한눈에](#한눈에)")
    A("* [우리가 지는 항목](#우리가-지는-항목)")
    for c in cats_live:
        A(f"* [{c}](#{c.replace('·', '')})")
    A("* [표기](#표기)")
    A("* [측정 못 함](#측정-못-함)")
    A("* [우리 목록에 넣으려면](#우리-목록에-넣으려면)")
    A("* [고쳤다면 다시 잰다](#고쳤다면-다시-잰다)")
    A("* [어떻게 재나](#어떻게-재나)")
    A("* [믿으면 안 되는 부분](#믿으면-안-되는-부분)")
    A("* [신뢰 규약 — 무엇을 재는지 먼저 말한다](PROTOCOL.md)")
    A("")

    # ── 왜 만드나 ──
    A("## 왜 만드나")
    A("")
    A("**AI가 좋은 MCP를 못 찾는다.** 한국 MCP 스토어들은 대부분 AI가 읽을 수 없다 — "
      "화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. "
      "정작 MCP는 AI가 쓰라고 만든 것인데.")
    A("")
    A("그래서 이 목록은 **AI가 읽을 수 있게** 만든다. JS도 로그인도 차단도 없는 "
      "마크다운과 JSON이다. 그리고 **있다고 말하지 않고 두드려 본다** — 등록은 가동의 증거가 아니다.")
    A("")
    A("**우리 것만 싣지 않는다.** 남의 MCP가 더 나으면 더 낫다고 쓴다. "
      "이 목록의 운영자(🏠 표시)도 같은 표에서 같은 잣대로 잰다.")
    A("")
    A(f"{emph('그리고 그 표를 설계한 것도 우리다.')} 원자료를 다 공개해도 이 편향은 "
      "안 없어진다 — 축을 하나 넣고 빼는 것만으로 등수는 바뀌고, 그 선택권을 쥔 쪽이 "
      "순위에 자기 제품을 올린 쪽이다. 그래서 이 문장을 각주가 아니라 소유 공시 바로 "
      "옆에 둔다. 무엇을 재기로 했는지는 결과를 보기 전에 "
      "[신뢰 규약](PROTOCOL.md)에 고정해 두었고, 바꾼 적이 있으면 그 이력도 거기 있다 "
      "— **한 번 있다.**")
    A("")

    # ── 한눈에 ──
    A("## 한눈에")
    A("")
    A("분야마다 1위 하나씩. 아래 각 분야의 채점 결과와 **같은 값에서 나온다** — "
      "여기와 본문이 어긋날 수 없다.")
    A("")
    # 1위인 **이유**를 적는 자리다. 종전엔 `why[:60]`이었는데 `why`가 사실오류 인용으로
    # 시작하던 탓에, 이 열이 60자에서 잘린 오류 문장만 보여 주고 정작 왜 1위인지는
    # 한 글자도 안 적혔다. 오류는 건수로 옆 칸에 세우고, 이 칸은 총평을 쓴다.
    A("| 분야 | 1위 | 사실오류 | 왜 이것이 1위인가 |")
    A("|---|---|---|---|")
    for c in cats_live:
        winner = next((r for r in live
                       if cls.get(r["name"], {}).get("category") == c
                       and rank_of.get(r["name"], (9, ""))[0] == 1), None)
        if not winner:
            continue
        why = rank_of[winner["name"]][1]
        n_err = err_of.get(winner["name"])
        A(f"| [{c}](#{c.replace('·', '')}) | {link(winner)}"
          f"{' 🏠' if winner['name'].startswith(OURS) else ''} | "
          f"{(str(n_err) + '건') if n_err else '0건'} | {clip(why, 110)} |")
    A("")
    A("종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 "
      "반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.")
    A("")

    # ── 우리가 지는 항목 ──
    # 왜 여기(순위 바로 밑)인가: 규약 ②는 "불리한 축을 포함한다"가 아니라 **"우리가 먼저
    # 싣는다"**이다. 문서 끝의 한계 절로 미루면 순위를 다 읽은 뒤에야 눈에 들어오고,
    # 그건 싣지 않은 것과 신뢰 효과가 같다.
    A("## 우리가 지는 항목")
    A("")
    A("**유리한 축만 재면 그 순위는 판정이 아니라 광고지다.** 원격 MCP인 우리가 불리한 "
      "축을 같이 잰다 — 무엇을 잴지는 결과를 보기 전에 [신뢰 규약](PROTOCOL.md)에 "
      "고정했고, 여기서 뺄 수 없게 회귀 테스트로 묶어 두었다.")
    A("")
    sh = collections.Counter((r.get("self_hosting") or {}).get("state") for r in items)
    lic = collections.Counter((r.get("open_source") or {}).get("license") for r in items)
    paid = [r for r in items if (r.get("paid_disclosure") or {}).get("disclosed")]
    ours_paid = [r for r in paid if r["name"].startswith(OURS)]
    lic_named = ", ".join(f"{k} {v}건" for k, v in lic.most_common() if k)
    A("| 축 | 이 목록 전체 | 운영자(🏠) |")
    A("|---|---|---|")
    A(f"| 셀프호스팅 | 배포판 확인 {sh['packaged']}건 · 소스만 {sh['source_only']}건 · "
      f"미확인 {sh['unknown']}건 | **소스만** — 그리고 클론해도 답이 안 나온다 |")
    A(f"| 오픈소스 | {lic_named} · 라이선스 확인 못 함 {lic[None]}건 | "
      "MIT — **이 축에서는 우리가 지지 않는다** |")
    A(f"| 무료 한도 | 스스로 공시한 서버 {len(paid)}건 | "
      + (f"그 {len(paid)}건이 우리다 — 도구 "
         f"{ours_paid[0]['paid_disclosure']['total']}종 중 "
         f"**{ours_paid[0]['paid_disclosure']['paid']}종 유료** |" if ours_paid else "— |"))
    A("")
    A("* **셀프호스팅은 우리가 제일 나쁘다.** 우리 저장소는 MIT로 열려 있지만 도구들이 "
      "우리 비공개 데이터 API를 부르므로 "
      "[클론해서 띄우면 거의 다 실패한다](https://github.com/sallim-app/korea-realty) "
      "— 우리 README가 먼저 적어 둔 것이고, 여기서도 적는다. 축의 값(`source_only`)보다 "
      "실질이 나쁘다")
    A("* **`소스만`은 “띄우면 같은 답이 나온다”가 아니다.** 코드가 공개돼 있다는 뜻일 "
      "뿐이고, 남의 서버도 우리처럼 자기 데이터에 묶여 있을 수 있다 — 그건 우리가 "
      "재지 않았다")
    A("* **`라이선스 확인 못 함`을 “오픈소스 아님”으로 읽지 말라.** 저장소가 비공개거나 "
      "지워졌거나 이름이 바뀐 것도 여기 들어온다. 다만 **공개 저장소인데 라이선스 파일이 "
      "없는 것**은 기본값이 저작권 전부 유보라 실제로 가져다 쓸 수 없다")
    A(f"* **유료 공시가 {len(paid)}건뿐인 것은 나머지가 무료라는 뜻이 아니다.** "
      "밖에서는 판정할 수 없다. 밝힌 쪽만 표에 유료 게이트가 보이고, 지금 그 쪽은 "
      "우리다")
    A("")
    A("축이 모자란다고 보면 다른 가중치로 직접 재계산할 수 있다 — "
      "[axes.csv](axes.csv)가 서버 1행 × 축 1열이고, "
      "`python3 recompute.py --weights tool_count=1,warm_ms=-0.01`이 그 계산기다. "
      f"{emph('그 결과는 우리 순위가 아니다')} — 지표로 줄 세우는 방식은 우리가 실측으로 "
      "폐기했다([JUDGING.md](JUDGING.md)).")
    A("")

    # ── 분야별 ──
    for c in cats_live:
        group = [r for r in live if cls.get(r["name"], {}).get("category") == c]
        # **잘못 넣은 것을 순위에서 뺀다**(observed.py). 뉴스 서버에게 상품을 묻고
        # 못 답했다고 등수를 내리면, 잰 것은 그 서버가 아니라 우리 수집기의 오분류다.
        mis = [r for r in group if r["name"] in MISFILED]
        group = [r for r in group if r not in mis]
        judged = [r for r in group if r["name"] in rank_of]
        judged.sort(key=lambda r: rank_of[r["name"]][0])
        rest = sorted([r for r in group if r["name"] not in rank_of],
                      key=lambda r: -(r["remote"].get("tool_count") or 0))
        A(f"## {c}" + (f" ({CAT_EN[c]})" if not en else ""))
        A("")
        if not judged:
            # 후보가 적어 심사하지 않은 분야 — "Top 3"라고 쓰면 실제보다 두껍게 읽힌다.
            # **문구가 건수를 따라가야 한다**(2026-08-31): "3개 중 3개"가 고정 문구라
            # 1건짜리 분야에서 "후보가 1건뿐인데 3개 중 3개"라는 자기모순이 나갔다.
            # 이번 회차에 레지스트리를 다 보면서 1~2건짜리 분야가 4개 생겨 그만큼 드러났다.
            n = len(group)
            A(f"후보가 {n}건뿐이라 순위를 매기지 않았다. "
              + ("이 분야에서 응답한 서버가 하나라 비교할 상대가 없다."
                 if n == 1 else
                 f"{n}개 중 {n}개를 고르는 것은 순위가 아니라 목록이다."))
            A("")
        else:
            if len(group) <= 3:
                # 셋 중 셋이면 고른 것이 아니라 줄 세운 것이다 — 그 차이를 적는다.
                A(f"<sub>이 분야는 후보가 {len(group)}건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>")
                A("")
            if cat_note.get(c):
                # 개행이 들어 있으면 두 번째 줄이 인용 밖으로 나가 blockquote가 끊긴다
                # (법령 분야에서 실제로 그렇게 게시됐다). clip이 공백을 접어 막는다.
                A(f"> {clip(cat_note[c], 260)}")
                A("")
            if mis:
                # 채점자 총평은 **분야 교정 전** 서버 수로 말한다("다섯 서버 중" 위에
                # 세 줄짜리 표). 총평은 남의 말이라 고치지 않고, 어긋나는 이유를 적는다.
                A(f"<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 "
                  f"{len(mis)}건이 아래 「분야 교정」으로 빠졌다.</sub>")
                A("")
        top = judged
        out.extend(head(en))
        for r in (top or rest[:3] if not judged else top):
            A(row(r, en, err_of))
        A("")
        if judged:
            for r in judged:
                rank, why = rank_of[r["name"]]
                A(f"{rank}. **{disp(r['name'])}** — {clip(why, 300)}")
            A("")
            # **빠진 등수를 설명한다.** 채점(매월) 뒤에 죽거나 후보에서 빠진 서버는
            # 이번 주 표에 없다. 아무 말 없이 빼면 독자는 이 빠진 번호를 렌더 버그로
            # 읽거나, 더 나쁘게는 우리가 불리한 항목을 지운 것으로 읽는다.
            here = {r["name"] for r in judged} | {r["name"] for r in mis}
            here |= {RENAMED[n] for n in here if n in RENAMED}
            gone = [(rk_, n) for rk_, n in sorted(set(graded_of.get(c, [])))
                    if n not in here]
            if gone:
                bits = []
                for rk_, n in gone:
                    why_gone = ("이번 주 가동 확인 못 함([DOWN.md](DOWN.md))"
                                if n in {x["name"] for x in dead}
                                else "이번 주 후보에서 빠졌다")
                    bits.append(f"{rk_}위 {disp(n)}({why_gone})")
                A(f"<sub>{emph('빠진 등수')} — 지난 채점 회차의 "
                  + " · ".join(bits)
                  + ". 순위는 매월 1일에만 다시 매기므로 그때까지 번호는 그대로 둔다 —"
                    " 빈자리를 위로 당기면 재채점 없이 등수가 오른 것처럼 보인다.</sub>")
                A("")
            # **몇 번 물었는지를 순위 옆에 적는다.** 1회짜리 순위는 서버의 성질과
            # 모델의 주사위를 구별하지 못한다(variance/ 실측: 4개 자리 중 2곳 등급 갈림).
            # 적지 않으면 독자는 그 등수가 한 번의 주사위인지 모른다.
            n = cat_runs.get(c, 1)
            runs = (f"서버당 {emph(f'{n}회')} 물어 재현성까지 채점했다."
                    if n >= 2 else
                    f"이 회차는 서버당 {emph('1회')}만 물었다 — "
                    "**재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). "
                    "다음 채점 회차부터 3회로 잰다.")
            A(f"<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 "
              f"답변을 채점했다. {runs} 질문·호출기록·답변은 [answers/](answers)에, 채점은 "
              "[grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>")
            A("")
        if judged and rest:
            A("<details><summary>" + f"채점하지 않은 {len(rest)}건" + "</summary>")
            A("")
            out.extend(head(en))
            for r in rest:
                A(row(r, en, err_of))
            A("")
            A("</details>")
            A("")
        if mis:
            A(f"{emph(f'분야 교정 {len(mis)}건')} — 이 분야 검색어에 걸려 수집됐지만 "
              "**불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 "
              "잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.")
            A("")
            A("| 서버 | 실제 분야 | 채점자가 확인한 것 |")
            A("|---|---|---|")
            for r in sorted(mis, key=lambda x: x["name"]):
                _, now, why = MISFILED[r["name"]]
                # 채점자 문장에서 그대로 떼어 온 조각이라 어미가 끊긴다("…범위 밖이며").
                # 고쳐 쓰면 축자성이 깨지므로(회귀가 grades/와 대조한다) 고치지 않고
                # **발췌임을 보이게** 따옴표와 말줄임으로 감싼다.
                tail = "…" if not why.rstrip().endswith("다.") else ""
                A(f"| {link(r)}{renamed_note(r['name'], en, ranked=False)} | {now} | "
                  f"“{why.rstrip()}{tail}” |")
            A("")

    # ── 표기 ──
    A("## 표기")
    A("")
    A("* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다")
    A("* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. "
      "콜드가 웜의 3배를 넘으면 굵게 표시한다")
    A("* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. "
      "**둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다")
    A("* 이름 옆 <sub>무료 N/M</sub> — 서버가 유료 게이트를 **스스로 공시**할 때만 붙는다. "
      "없다고 무료라는 뜻이 아니다 — 밖에서는 판정할 수 없다")
    A("* 이름 밑 작은 글씨 — 불러 보고 알게 된 **그 서버의 성질**. "
      "카탈로그형은 값이 아니라 데이터셋 위치를 주고, 집계 통계표는 개별 거래를 주지 않는다. "
      "몰라서 헛짚는 자리라 표에 낸다")
    A("* **사실오류** — 그 서버로 답한 내용 중 채점자가 **실제와 다르다고 확인한** 건수. "
      "서버가 틀린 값을 준 경우와 모델이 옮겨 적다 틀린 경우가 섞여 있고, "
      "어느 쪽인지는 [grades/](grades)에 문장째 적혀 있다. `—`는 채점하지 않았다는 뜻이다")
    A("* 🏠 — 이 목록의 운영자가 만든 서버. **이 목록의 축을 고른 것도 같은 운영자다** "
      "— 축과 그 개정 이력은 [PROTOCOL.md](PROTOCOL.md)에 있다")
    A("")

    # ── 측정 못 함 ──
    if unmeasured:
        A("## 측정 못 함")
        A("")
        A(f"응답은 했지만 **비교할 값을 얻지 못한 {len(unmeasured)}건.** 지우지 않고 여기 둔다 — "
          "“없다”가 아니라 **“우리가 못 봤다”**이기 때문이다. 대부분 도구 목록을 보는 데도 "
          "키를 요구한다. 키가 있으면 잘 도는 서버일 수 있다.")
        A("")
        out.extend(["| 서버 | 증상 |", "|---|---|"])
        for r in sorted(unmeasured, key=lambda x: x["name"]):
            why = (r["remote"].get("why") or "").strip() or f"HTTP {r['remote'].get('http')}"
            A(f"| {link(r)} | {why[:60]} |")
        A("")

    # ── 넣으려면 ──
    A("## 우리 목록에 넣으려면")
    A("")
    A("**우리에게 올릴 필요가 없다.** [공식 MCP 레지스트리](https://registry.modelcontextprotocol.io)에 "
      "등록하면 다음 회차에 자동으로 들어온다. 그쪽이 나은 이유는 우리만 읽는 게 아니라서다.")
    A("")
    A("이미 등록했는데 여기 없다면 **우리 수집기의 버그일 수 있다** — 이슈로 알려 달라. "
      "경쟁 서비스여도 받는다.")
    A("")
    A("제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 우리가 통과시키고 말고 할 것이 없다.")
    A("")

    # ── 고쳤다면 다시 잰다 ──
    # 왜 이 절이 필요한가: 이 표의 감점은 **측정한 그 순간**의 기록인데, 목록은 남고
    # 서버는 고쳐진다. 우리가 먼저 다시 두드리지 않기로 했으므로(아래 이유) 신호를
    # 받는 쪽을 열어 두지 않으면, 고친 서버가 옛 감점에 영영 묶인다.
    A("## 고쳤다면 다시 잰다")
    A("")
    A(f"이 표의 값은 {emph(f'{ts} 그 순간의 기록')}이다. 고쳤다면 "
      "[이슈](https://github.com/sallim-app/korea-mcp-index/issues)로 알려 달라 — "
      "다음 회차에 다시 잰다. 경쟁 서비스여도 받는다.")
    A("")
    A("**우리가 먼저 다시 두드리지는 않는다.** 바뀐 게 없는 서버를 주기적으로 재호출하는 것은 "
      "새 정보가 아니라 남의 서버에 지우는 부하다. 그래서 두드리는 대신 신호를 받는다.")
    A("")
    A("이런 것도 같은 창구다 — **우리 쪽 잘못일 수 있다.**")
    A("")
    A("* 분야가 틀렸다 (검색어가 분야를 정하므로 실제로 하는 일과 어긋날 수 있다)")
    A("* 주소를 잘못 짚었다 (README에서 추정한 주소라 서버가 아니라 우리가 틀린 것)")
    A("* 채점이 틀렸다 — 답변·근거·채점이 [answers/](answers)·[grades/](grades)에 "
      "그대로 있으니 어느 문장이 왜 틀렸는지 짚어 달라")
    A("")
    A("**순위는 전원 동시에만 다시 잰다 — 운영자인 우리도 예외가 아니다.** "
      "우리는 고칠 때마다 다시 잴 수 있고 남은 그럴 수 없다. 개별 재측정을 순위에 반영하면 "
      "우리 서버만 계단식으로 올라가고 남은 자기 최악의 순간에 박제된다. "
      "실제로 우리는 이 표의 지적을 받아 우리 서버를 고치고 다시 쟀지만 "
      f"{emph('그 결과를 순위에 넣지 않았다')} — 기록은 [answers/](answers)에 "
      "‘정규 회차 아님’으로 남겨 두었다.")
    A("")

    # ── 방법론 ──
    A("## 어떻게 재나")
    A("")
    A("```")
    A("collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API")
    A("filter   한국 관련성(한글·.go.kr·기관명) → 후보 좁히기")
    A("enrich   README에서 엔드포인트·패키지·기관 도메인 추출")
    A("classify 분야·데이터제공형 판정 (LLM, 결과는 classification.json에 고정)")
    A("measure  tools/list 실호출 — 가동·도구수·지연·설명·주석          [매주]")
    A("answer   분야별 실제 질문을 서버에 던져 답하게 한다 (Haiku)       [매월]")
    A("grade    그 답을 원문과 대조해 채점한다 (Opus) → 순위             [매월]")
    A("render   이 문서")
    A("```")
    A("")
    A("**가동은 매주, 순위는 매월 1일**에 다시 잰다. 서버가 안 바뀌면 채점 결과도 안 바뀌는데 "
      "매주 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다.")
    A("")
    A("두드릴 때는 `tools/list` 3회(콜드 1 + 웜 2), 사이에 간격을 두고, "
      "User-Agent로 우리를 밝힌다.")
    A("")
    # 종전 문구 "**돌리면 같은 표가 나온다**"는 과장이었다. 가동 지표는 재현되지만
    # 순위는 LLM 채점이라 그대로 재현되지 않는다 — 실제로 같은 질문을 다시 던졌더니
    # 4개 자리 중 2곳에서 등급이 갈렸다(variance/). 재현되는 것과 안 되는 것을 가른다.
    A(f"{emph('가동 지표는 돌리면 같은 값이 나온다')} — 원자료가 "
      "[measured.json](measured.json)·[candidates.json](candidates.json)에 있다. "
      f"{emph('순위는 그렇지 않다')} — 채점이 모델 판단이라 같은 입력에도 흔들린다. "
      "얼마나 흔들리는지를 우리가 직접 재서 [variance/](variance)에 공개해 두었다. "
      "우리가 1위인 자리일수록 이 두 문장을 함께 읽어 달라.")
    A("")
    A(f"{emph('다른 가중치로 다시 계산해 보라고 표를 펴 두었다')} — "
      "[axes.csv](axes.csv)는 게시된 모든 축을 서버 1행 × 축 1열로 편 것이고, "
      "`python3 recompute.py --verify`는 **이 문서의 머릿수가 원자료에서 그대로 나오는지** "
      "검사한다. 원자료를 올려 두는 것과 그 원자료로 게시본이 재현되는 것은 다른 주장이라 "
      "후자를 기계로 건다.")
    A("")

    # ── 한계 ──
    A("## 믿으면 안 되는 부분")
    A("")
    A("* **정확성은 분야마다 질문 두 개로만 봤다.** 그 두 문항이 그 분야를 대표한다는 "
      "보장은 없다. 질문은 공개돼 있으니(`questions.py`) 더 나은 질문을 알려 달라")
    A("* **채점자도 모델이다.** 근거를 전부 공개하는 것으로 줄일 수는 있어도 없앨 수는 없다. "
      "답변은 약한 모델(Haiku)이 만들고 채점은 강한 모델(Opus)이 하는데, 그 이유와 "
      "실측 근거는 [JUDGING.md](JUDGING.md)에 있다")
    A("* **한 번 물어본 순위다.** 다시 물으면 등수가 갈릴 수 있다 — 우리 서버로 재 보니 "
      "질문 네 자리 중 두 곳이 갈렸다([variance/](variance)). 다음 채점 회차부터 3회로 잰다")
    A("* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다 — "
      "무엇을 고정했고 무엇을 언제 왜 바꿨는지는 [PROTOCOL.md](PROTOCOL.md)에 있다. "
      "**결과를 본 뒤에 바꾼 적이 한 번 있고**, 그 건도 거기 적어 두었다")
    A("* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다")
    A("* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다")
    # 2026-08-20(T-2026W34-107): 종전 문장은 "주소도 **패키지도** 찾지 못했다"라 쓰면서
    # 계산은 `전체 - 주소있음`뿐이었다 — 패키지를 한 번도 세지 않았다. 실측 결과 그 178건 중
    # 74건은 배포 패키지와 배포일이 확인된 것이었다. 우리가 남의 목록에서 잡아내는 종류의
    # 부정직 공시를 하필 「믿으면 안 되는 부분」 절이 저지르고 있었다. 이제 실제로 센다.
    no_addr_no_pkg = [r for r in items if not r.get("remote") and not r.get("package")]
    pkg_only = [r for r in items
                if not r.get("remote") and (r.get("package") or {}).get("installable") is True]
    A(f"* **못 잰 것이 더 많다.** 후보 중 {len(no_addr_no_pkg)}건은 주소도 패키지도 찾지 "
      "못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다"
      f"{f' — 그 밖에 {len(pkg_only)}건은 배포 패키지는 확인했으나 원격 주소가 없어 응답을 못 쟀다' if pkg_only else ''}")
    A("")
    A("---")
    A("")
    A("## 라이선스")
    A("")
    A("코드·문서·우리가 만든 측정값은 [MIT](LICENSE). **응답 발췌는 각 서버 운영자의 것**이고 "
      "우리는 측정 근거로 인용했을 뿐이다 — 400~500자로 제한하고 개인정보 패턴을 가린다. "
      "내려 달라고 하면 내린다.")
    A("")
    A("---")
    A("")
    A(f"생성 `render_readme.py` · 웹판 <{SITE}> · 마지막 측정 {ts}"
      + (f" · 패키지 축 재측정 {pkg_ts}" if pkg_ts and pkg_ts != ts else "")
      + " · 운영 [sallim-app](https://github.com/sallim-app)")

    if not en:
        write_down(dead, ts)

    text = "\n".join(out) + "\n"
    bad = BROKEN_EMPH.findall(text) + DOUBLE_EMPH.findall(text)
    if bad:
        print(f"생성 중단 — 깨지는 강조 {len(bad)}건: {bad[:3]}", file=sys.stderr)
        return 1
    open("README-en.md" if en else "README.md", "w", encoding="utf-8").write(text)
    print(f"{'README-en' if en else 'README'}.md — 살아있음 {len(live)} · 확인못함/죽음 {len(dead)} · "
          f"주제밖 {len(off)} · 분야 {len(cats_live)}개 · 병합 {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
