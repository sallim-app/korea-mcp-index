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
import json
import re
import sys
from datetime import UTC, datetime

OURS = ("app.sallim/", "sallim-app/")
CATS = ["공공데이터·행정", "법령·판례", "금융·증시", "부동산", "세금·재정", "지도·주소",
        "날씨·환경", "교통·이동", "의료·복지", "교육·문화", "한국어·언어", "커머스·생활", "기타"]
CAT_EN = {"공공데이터·행정": "Public Data", "법령·판례": "Law", "금융·증시": "Finance",
          "부동산": "Real Estate", "세금·재정": "Tax", "지도·주소": "Maps", "날씨·환경": "Weather",
          "교통·이동": "Transit", "의료·복지": "Health", "교육·문화": "Education",
          "한국어·언어": "Korean NLP", "커머스·생활": "Commerce", "기타": "Other"}

# 닫는 `**` 앞이 문장부호이고 뒤가 글자면 CommonMark가 강조를 닫지 않는다.
# `**"지금 되냐"**를` 이 형태로 실제로 깨져서 게시됐다(2026-08-19).
BROKEN_EMPH = re.compile(r'[)\]}"\'.,!?:;][*]{2}[0-9A-Za-z가-힣]')


def emph(text: str) -> str:
    """강조를 만드는 유일한 경로. 끝 문장부호는 강조 **밖으로** 밀어낸다."""
    t = text.rstrip()
    tail = ""
    while t and t[-1] in ')]}"\'.,!?:;':
        tail = t[-1] + tail
        t = t[:-1]
    return f"**{t}**{tail}" if t else text


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


def row(rec: dict, en=False) -> str:
    rm = rec["remote"]
    mark = " 🏠" if rec["name"].startswith(OURS) else ""
    warm, cold = rm.get("warm_ms"), rm.get("cold_ms")
    slow = cold and warm and cold > warm * 3
    pd = rec.get("paid_disclosure") or {}
    paid = f" <sub>무료 {pd.get('free')}/{pd.get('total')}</sub>" if pd.get("disclosed") else ""
    return (f"| {link(rec)}{mark}{paid} | {rm.get('tool_count') or '—'} | {warm or '—'} | "
            f"{emph(str(cold)) if slow else (cold or '—')} | "
            f"{q(rec, 'described_pct')}% | {q(rec, 'annotated_pct')}% |")


def head(en=False) -> list[str]:
    # `키`와 `무료/전체`를 열에서 뺐다(2026-08-19). 측정 가능한 것만 표에 남기니 `키`는
    # 21줄 전부 `—`였고, `무료/전체`는 스스로 공시하는 서버가 우리뿐이라 20/21이 `—`였다.
    # **빈 열은 정보가 아니라 소음이고, 그것을 설명하는 범례는 독자의 첫 화면을 잡아먹는다.**
    # 유료 공시는 각주로 내린다.
    return ["| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |" if not en else
            "| Server | Tools | Warm | Cold | Desc | Annot |",
            "|---|---|---|---|---|---|"]


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
    o.append("# 응답하지 않는 서버")
    o.append("")
    o.append(f"{ts} 측정 시점에 `tools/list`에 응답하지 않은 목록. "
             "**폐기 판정이 아니라 관측 기록이다** — 일시적 장애일 수 있다.")
    o.append("")
    o.append("고쳤거나 우리가 주소를 잘못 짚었다면 이슈로 알려 달라. 다음 회차에 다시 잰다.")
    o.append("")
    strong = [r for r in dead if r.get("addr_registered")]
    weak = [r for r in dead if r not in strong]
    for title, group, note in (
            ("등록된 주소가 응답하지 않음", strong,
             "관리자가 공식 레지스트리에 **직접 등록한** 주소다. 주장이 강하다."),
            ("추정 주소가 응답하지 않음", weak,
             "우리가 README에서 뽑은 **추정** 주소다. **우리가 주소를 잘못 짚었을 수 있다** — "
             "그 서버가 죽었다는 뜻으로 읽지 마라."),
    ):
        if not group:
            continue
        o.append(f"## {title} — {len(group)}건")
        o.append("")
        o.append(note)
        o.append("")
        o.append("| 서버 | 증상 | 주소 |")
        o.append("|---|---|---|")
        for r in group:
            rm = r["remote"]
            why = rm.get("why") or f"HTTP {rm.get('http')}"
            o.append(f"| {link(r)} | {why[:60]} | `{(rm.get('url') or '')[:60]}` |")
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
    cat_note = {}         # 분야 → 총평
    for v in rk.values():
        cat_note[v["category"]] = v.get("note", "")
        for t in v["top"]:
            rank_of[t["name"]] = (t["rank"], t.get("why", ""))

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

    ts = datetime.now(UTC).strftime("%Y-%m-%d")
    pct = round(100 * len(dead) / max(len(rem), 1))
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
    A(f"다른 목록은 “있다”를 말한다. 이 목록은 {emph('지금 되냐')}를 잰다. "
      f"{ts} 기준 주소를 확인한 {len(rem)}건 중 {emph(f'{len(dead)}건({pct}%)이 응답하지 않았다')}."
      if not en else
      f"Other lists tell you a server exists. This one tells you whether it {emph('works right now')}. "
      f"As of {ts}, {len(dead)} of {len(rem)} ({pct}%) did not respond.")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| 비교 가능한 서버 | {emph(str(len(live)))}건 |")
    A(f"| 응답했으나 못 잼(키 필요·규격 이탈) | {len(unmeasured)}건 |")
    A(f"| 응답 없음 | {len(dead)}건 → [DOWN.md](DOWN.md) |")
    A(f"| 주제 밖(데이터 제공형 아님) | {len(off)}건 |")
    A("")

    # ── 목차 ──
    cats_live = [c for c in CATS if any(cls.get(r["name"], {}).get("category") == c for r in live)]
    A("* [왜 만드나](#왜-만드나)")
    A("* [한눈에](#한눈에)")
    for c in cats_live:
        A(f"* [{c}](#{c.replace('·', '')})")
    A("* [표기](#표기)")
    A("* [측정 못 함](#측정-못-함)")
    A("* [우리 목록에 넣으려면](#우리-목록에-넣으려면)")
    A("* [어떻게 재나](#어떻게-재나)")
    A("* [믿으면 안 되는 부분](#믿으면-안-되는-부분)")
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

    # ── 한눈에 ──
    A("## 한눈에")
    A("")
    A("분야마다 1위 하나씩. 순서는 아래 각 분야의 심사 결과와 **같은 값에서 나온다** — "
      "여기와 본문이 어긋날 수 없다.")
    A("")
    A("| 분야 | 1위 | 왜 |")
    A("|---|---|---|")
    for c in cats_live:
        winner = next((r for r in live
                       if cls.get(r["name"], {}).get("category") == c
                       and rank_of.get(r["name"], (9, ""))[0] == 1), None)
        if not winner:
            continue
        why = rank_of[winner["name"]][1]
        A(f"| [{c}](#{c.replace('·', '')}) | {link(winner)}"
          f"{' 🏠' if winner['name'].startswith(OURS) else ''} | {why[:60]} |")
    A("")
    A("종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 "
      "반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.")
    A("")

    # ── 분야별 ──
    for c in cats_live:
        group = [r for r in live if cls.get(r["name"], {}).get("category") == c]
        judged = [r for r in group if r["name"] in rank_of]
        judged.sort(key=lambda r: rank_of[r["name"]][0])
        rest = sorted([r for r in group if r["name"] not in rank_of],
                      key=lambda r: -(r["remote"].get("tool_count") or 0))
        A(f"## {c}" + (f" ({CAT_EN[c]})" if not en else ""))
        A("")
        if not judged:
            # 후보가 적어 심사하지 않은 분야 — "Top 3"라고 쓰면 실제보다 두껍게 읽힌다.
            A(f"후보가 {len(group)}건뿐이라 순위를 매기지 않았다. "
              f"3개 중 3개를 고르는 것은 순위가 아니라 목록이다.")
            A("")
        else:
            if len(group) <= 3:
                # 셋 중 셋이면 고른 것이 아니라 줄 세운 것이다 — 그 차이를 적는다.
                A(f"<sub>이 분야는 후보가 {len(group)}건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>")
                A("")
            if cat_note.get(c):
                A(f"> {cat_note[c]}")
                A("")
        top = judged
        out.extend(head(en))
        for r in (top or rest[:3] if not judged else top):
            A(row(r, en))
        A("")
        if judged:
            for r in judged:
                rank, why = rank_of[r["name"]]
                A(f"{rank}. {r['name'].split('/')[-1]} — {why}")
            A("")
            A("<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 "
              "[JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>")
            A("")
        if judged and rest:
            A("<details><summary>" + f"심사에 들지 못한 {len(rest)}건" + "</summary>")
            A("")
            out.extend(head(en))
            for r in rest:
                A(row(r, en))
            A("")
            A("</details>")
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
    A("* 🏠 — 이 목록의 운영자가 만든 서버")
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
    A("제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 그래서 심사할 것이 없다.")
    A("")

    # ── 방법론 ──
    A("## 어떻게 재나")
    A("")
    A("```")
    A("collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API")
    A("filter   한국 관련성(한글·.go.kr·기관명) → 후보 좁히기")
    A("enrich   README에서 엔드포인트·패키지·기관 도메인 추출")
    A("classify 분야·데이터제공형 판정 (LLM, 결과는 classification.json에 고정)")
    A("measure  tools/list 실호출 — 가동·도구수·지연·설명·주석")
    A("render   이 문서")
    A("```")
    A("")
    A("서버당 `tools/list` 3회(콜드 1 + 웜 2), 사이에 간격을 두고, User-Agent로 우리를 밝힌다. "
      "원자료는 [measured.json](measured.json)·[candidates.json](candidates.json)에 있다. "
      "**돌리면 같은 표가 나온다** — 우리가 1위여도 직접 재서 반박할 수 있다.")
    A("")

    # ── 한계 ──
    A("## 믿으면 안 되는 부분")
    A("")
    A("* **데이터가 정확한지는 재지 않는다.** 우리는 부동산·공공계약은 정답을 알지만 "
      "의료·교통은 모른다. 모르면서 점수를 매기면 우리가 경계하는 그것을 우리가 하게 된다")
    A("* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다")
    A("* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다")
    A("* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다")
    A(f"* **못 잰 것이 더 많다.** 후보 중 {len(d['items']) - len(rem)}건은 주소도 패키지도 찾지 못했다. "
      "“작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다")
    A("")
    A("---")
    A("")
    A(f"생성 `render_readme.py` · 마지막 측정 {ts} · "
      f"운영 [sallim-app](https://github.com/sallim-app)")

    if not en:
        write_down(dead, ts)

    text = "\n".join(out) + "\n"
    bad = BROKEN_EMPH.findall(text)
    if bad:
        print(f"생성 중단 — 깨지는 강조 {len(bad)}건: {bad[:3]}", file=sys.stderr)
        return 1
    open("README-en.md" if en else "README.md", "w", encoding="utf-8").write(text)
    print(f"{'README-en' if en else 'README'}.md — 응답 {len(live)} · 무응답 {len(dead)} · "
          f"주제밖 {len(off)} · 분야 {len(cats_live)}개 · 병합 {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
