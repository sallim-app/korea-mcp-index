#!/usr/bin/env python3
"""수집 후보 → 한국 데이터 MCP 판정 (2026-08-18, D-2026W34-21).

왜 자동 판정인가: 검색어에 걸린 369건 중 대부분은 우연이다(ClickUp 서버가 'skr'로,
캘린더 도구가 'korea'로 걸린다). 사람이 369건을 매번 다시 읽으면 재실행이 불가능해지고,
재실행이 안 되면 우리 목록도 6개월 뒤 정체된 29개 중 하나가 된다.

**조용히 버리지 않는다**(기치 ②). 세 통으로 나누고 각 건에 사유를 붙인다:
  keep   — 한국 관련 + 데이터 제공형이 둘 다 잡힌 것
  drop   — 제외 신호가 명확한 것(프레임워크·클라이언트·조직 프로필 등). 사유를 남긴다
  review — 애매한 것. **사람이 봐야 한다.** 이 통을 0으로 만들려고 기준을 억지로 넓히지 마라.

판정 축 3개(기치 3절: "많은 데이터가 아니라 좋은 데이터"):
  ① 한국 관련성 — 한국의 데이터·제도·서비스를 다루는가
  ② 데이터 제공형 — AI에게 **사실을 주는가**. 프레임워크·클라이언트·자동화 도구는 우리 주제가 아니다
  ③ 조인·계산·판정 — 원천도 웹검색도 못 주는 것을 주는가(D-2026W34-21의 선정 기준)

**축③은 keep/drop을 바꾸지 않는다.** 라벨만 붙인다(`value_add.py`가 그 이유를 길게 적어
뒀다 — 요지는 도구 목록을 본 서버가 233건 중 25건뿐이고, 못 본 208건을 이 축으로 떨어뜨리면
"못 봄"을 "없음"으로 게시하게 된다는 것이다). 남은 판단은 블라인드 심사 레인(D-2026W34-25).

실행: python3 filter_candidates.py   →  candidates_filtered.json + 커버리지 표
"""
import argparse
import json
import re

import value_add

KR = ["korea", "korean", "한국", "대한민국", "molit", "국토부", "kosis", "법제처",
      "krx", "dart", "공공데이터", "naver", "네이버", "kakao", "카카오", "seoul", "서울",
      "kma", "기상청", "popbill", "실거래", "청약", "행정안전부", "관세청", "k-beauty",
      "south korea", "hangul", "한글", "원화", "kospi", "kosdaq"]
# 사실을 주는 쪽
DATA = ["search", "query", "lookup", "fetch", "retrieve", "data", "dataset", "records",
        "statistics", "stats", "disclosure", "transaction", "price", "forecast", "weather",
        "database", "registry", "catalog", "directory", "filing", "auction", "geocod",
        "조회", "검색", "데이터", "통계", "공시", "실거래", "시세", "법령", "판례"]
# 우리 주제가 아닌 쪽 — 있으면 drop
NOT_DATA = ["framework", "boilerplate", "template", "starter", "scaffold", "all-in-one",
            "orchestrat", "workspace", "calendar", "erp", "workshop", "tutorial", "example",
            "playground", "client for", "gateway", "proxy", "wrapper generator", "sdk",
            "awesome", "curated list", "공개 프로필", "profile"]


# 부분문자열로 찾으면 반드시 오탐이 나는 짧은 약어들. 여기 있는 것만 단어 경계를 건다.
# **전부에 경계를 걸면 반대편 오탐이 난다** — `data`에 경계를 걸었더니 govdata·opendata가
# 데이터형 신호를 잃고 review로 떨어졌다(2026-08-18 실측). 경계는 필요한 곳에만.
AMBIGUOUS = {"dart", "krx", "kma", "kr-", "kospi", "kosdaq"}


def _hit(text: str, words: list) -> list:
    """모호한 약어만 **단어 경계**로 찾는다.

    실측 2026-08-18: 네덜란드 서버 `agentdata-nl`이 한국 후보로 잡혔다 — `dart`가
    **agent`data`-nl** 안에 들어 있었기 때문이다. 부분문자열 매칭은 dart·krx·kma 같은
    짧은 약어에서 반드시 오탐을 낸다. 한글은 교착어라 경계 판정이 다르므로 종전대로 둔다.
    """
    t = text.lower()
    out = []
    for w in words:
        if w in AMBIGUOUS:
            if re.search(rf"\b{re.escape(w)}\b", t):
                out.append(w)
        elif w in t:
            out.append(w)
    return out


HANGUL = re.compile(r"[가-힣]")


def classify(item: dict) -> dict:
    name, desc = item["name"], item.get("description") or ""
    blob = f"{name} {desc}"
    kr, data, nod = _hit(blob, KR), _hit(blob, DATA), _hit(blob, NOT_DATA)
    # **한글로 쓰였다는 것 자체가 한국 신호다.** 2026-08-18 실측: 우리 계약나침반이
    # "계약나침반 — 공공계약 방법 결정 도우미(국가계약법·지방계약법 룰엔진)"라는 순한글
    # 설명 때문에 kr신호 0으로 drop됐다 — 목록에 `공공계약`이 없었기 때문이다. 단어를
    # 계속 늘리는 것은 지는 싸움이고(한국어 어휘는 무한하다), 문자 자체가 더 강한 신호다.
    if HANGUL.search(desc):
        kr = kr + ["한글 설명"]
    # **한국 도메인은 사실상 오탐이 없다.** `.go.kr`은 정부, `.or.kr`은 공공기관·협회다.
    # 영어로만 쓰인 설명이라도 `apis.data.go.kr`을 부르면 그것은 한국 공공데이터 MCP다.
    # (검색어로 쓸 때는 GitHub이 `go`·`kr`로 쪼개 노이즈가 섞이지만, **문자열 신호로는**
    #  깨끗하다 — 그래서 여기서 쓴다. 2026-08-18 사장님 지적.)
    kr = kr + [d for d in (".go.kr", ".or.kr", ".re.kr") if d in blob.lower()]
    # 보강 단계가 README에서 찾아낸 한국 도메인 — 설명이 영어뿐이어도 여기서 잡힌다.
    kr = kr + [f"README:{d}" for d in (item.get("kr_domains") or [])]

    # 저장소 자체가 MCP 서버가 아닌 것 — 이름으로 확실히 걸리는 것만
    if name.endswith("/.github") or re.search(r"awesome[-_]", name, re.I):
        return {"verdict": "drop", "why": "MCP 서버가 아니다(조직 프로필·목록 저장소)", "kr": kr, "data": data}
    # **이 목록 자신은 후보가 아니다.** 2026-08-24 실측: 저장소를 공개한 다음 주 회차에
    # GitHub 검색('mcp 한국')이 우리 색인 저장소를 잡아 keep으로 올렸다. 원격도 패키지도
    # 없으니 "가동 여부를 못 쟀다"로 실려, 목록이 자기 자신을 미측정 서버로 게시하게 된다.
    # 이름 하나만 막는다 — 우리 **서버**(korea-realty·contract-compass)는 후보가 맞고,
    # 여기서 넓게 막으면 우리를 순위에서 빼는 것이 되어 PROTOCOL.md와 어긋난다.
    if name == "sallim-app/korea-mcp-index":
        return {"verdict": "drop", "why": "MCP 서버가 아니다(이 목록 자신)", "kr": kr, "data": data}
    if not kr:
        return {"verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림", "kr": kr, "data": data}
    if nod and not data:
        return {"verdict": "drop", "why": f"데이터 제공형이 아니다({', '.join(nod[:3])})", "kr": kr, "data": data}
    if data:
        return {"verdict": "keep", "why": f"한국({kr[0]}) + 데이터({data[0]})", "kr": kr, "data": data}
    if not desc.strip():
        return {"verdict": "review", "why": "설명이 비어 자동 판정 불가 — 사람이 열어봐야 한다", "kr": kr, "data": data}
    return {"verdict": "review", "why": "한국 관련은 맞으나 데이터 제공형 신호가 없다", "kr": kr, "data": data}


def slug(name: str) -> str:
    """registry(app.sallim/korea-realty)와 github(sallim-app/korea-realty) 병합용 휴리스틱.
    마지막 경로 조각만 본다 — 완전하지 않다(같은 이름의 다른 서버를 합칠 수 있다). 공시 대상."""
    s = name.rsplit("/", 1)[-1].lower()
    return re.sub(r"[-_](mcp|server|mcp[-_]server)$", "", s)


def main() -> int:
    # 보강(enrich)이 README에서 `.go.kr`·패키지·엔드포인트를 찾아낸 뒤 **다시 판정**할 수
    # 있어야 한다. 보강이 필터 뒤에 오는데 보강 산출물이 판정을 바꾸므로, 같은 판정기를
    # 두 번 돌린다: 수집→판정→보강→**재판정**→측정.
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="candidates_raw.json")
    ap.add_argument("--output", default="candidates_filtered.json")
    a = ap.parse_args()
    raw = json.load(open(a.input, encoding="utf-8"))
    specs = value_add.load_specs()
    out, buckets = [], {"keep": 0, "drop": 0, "review": 0}
    a3: dict[str, int] = {}
    for it in raw["items"]:
        c = classify(it)
        buckets[c["verdict"]] += 1
        # 축③ — 도구 목록이 있는 서버만 실측 라벨, 나머지는 unknown(0이 아니다)
        ax = value_add.axis3(specs.get(it["name"]))
        a3[ax["signal"]] = a3.get(ax["signal"], 0) + 1
        out.append({**it, **c, "slug": slug(it["name"]), "axis3": ax})

    merged: dict[str, list] = {}
    for o in out:
        merged.setdefault(o["slug"], []).append(o["name"])
    dupes = {k: v for k, v in merged.items() if len(v) > 1}

    json.dump({"buckets": buckets, "dupe_slugs": dupes,
               "boundaries": raw.get("boundaries", []) + [
                   "슬러그 병합은 마지막 경로 조각 휴리스틱이다 — 동명이인을 합칠 수 있다",
                   "keep/drop 판정(축①②)은 이름·설명 문자열만 본다 — 도구 목록을 안 본다",
                   f"축③(조인·계산)은 도구 목록을 본 {sum(1 for o in out if o['axis3']['signal'] != 'unknown')}건만 "
                   f"라벨했다. 나머지 {a3.get('unknown', 0)}건은 unknown이며 **파생이 없다는 뜻이 아니다**",
                   "축③은 도구 **이름**의 동사류를 본다. 그 계산을 원천이 이미 주는지는 대조하지 않았다 "
                   "— 분야별 원천을 우리가 전부 모르기 때문이다(공시 대상)",
                   "축③은 후보를 떨어뜨리지 않는다 — keep/drop은 축①②만으로 결정된다"],
               "items": out},
              open(a.output, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"입력 {len(out)}건 → keep {buckets['keep']} · review {buckets['review']} · drop {buckets['drop']}")
    print(f"슬러그 중복 {len(dupes)}건(레지스트리↔GitHub 같은 서버로 추정)")
    order = ["derived", "ambiguous", "action_heavy", "retrieval_only", "unknown"]
    print("축③ 라벨: " + " · ".join(f"{k} {a3[k]}" for k in order if k in a3)
          + f"  (도구 목록을 본 것 {sum(v for k, v in a3.items() if k != 'unknown')}건 — "
            f"이 축은 keep/drop을 바꾸지 않는다)")
    keep3 = [o for o in out if o["verdict"] == "keep" and o["axis3"]["signal"] == "derived"]
    print(f"keep 중 축③ derived {len(keep3)}건 — 목록의 첫 화면 후보")
    print("\n■ keep 상위 (한국 데이터 MCP 후보)")
    for o in sorted([x for x in out if x["verdict"] == "keep"],
                    key=lambda x: -(x.get("stars") or 0))[:18]:
        star = f"★{o['stars']}" if "stars" in o else "reg"
        print(f"  {star:<7} {o['name'][:44]:<44} {o['why'][:34]}")
    print("\n■ review — 사람이 봐야 하는 것")
    for o in [x for x in out if x["verdict"] == "review"][:12]:
        print(f"  {o['name'][:46]:<46} {o['why'][:44]}")
    print("\n■ drop 사유 분포")
    why: dict[str, int] = {}
    for o in out:
        if o["verdict"] == "drop":
            why[o["why"][:40]] = why.get(o["why"][:40], 0) + 1
    for w, n in sorted(why.items(), key=lambda x: -x[1]):
        print(f"  {n:3d}  {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
