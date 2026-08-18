#!/usr/bin/env python3
"""수집 후보 → 한국 데이터 MCP 판정 (2026-08-18, D-2026W34-21).

왜 자동 판정인가: 검색어에 걸린 369건 중 대부분은 우연이다(ClickUp 서버가 'skr'로,
캘린더 도구가 'korea'로 걸린다). 사람이 369건을 매번 다시 읽으면 재실행이 불가능해지고,
재실행이 안 되면 우리 목록도 6개월 뒤 정체된 29개 중 하나가 된다.

**조용히 버리지 않는다**(기치 ②). 세 통으로 나누고 각 건에 사유를 붙인다:
  keep   — 한국 관련 + 데이터 제공형이 둘 다 잡힌 것
  drop   — 제외 신호가 명확한 것(프레임워크·클라이언트·조직 프로필 등). 사유를 남긴다
  review — 애매한 것. **사람이 봐야 한다.** 이 통을 0으로 만들려고 기준을 억지로 넓히지 마라.

판정 축 2개(기치 3절: "많은 데이터가 아니라 좋은 데이터"):
  ① 한국 관련성 — 한국의 데이터·제도·서비스를 다루는가
  ② 데이터 제공형 — AI에게 **사실을 주는가**. 프레임워크·클라이언트·자동화 도구는 우리 주제가 아니다

실행: python3 filter_candidates.py   →  candidates_filtered.json + 커버리지 표
"""
import json
import re

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


def _hit(text: str, words: list) -> list:
    t = text.lower()
    return [w for w in words if w in t]


def classify(item: dict) -> dict:
    name, desc = item["name"], item.get("description") or ""
    blob = f"{name} {desc}"
    kr, data, nod = _hit(blob, KR), _hit(blob, DATA), _hit(blob, NOT_DATA)

    # 저장소 자체가 MCP 서버가 아닌 것 — 이름으로 확실히 걸리는 것만
    if name.endswith("/.github") or re.search(r"awesome[-_]", name, re.I):
        return {"verdict": "drop", "why": "MCP 서버가 아니다(조직 프로필·목록 저장소)", "kr": kr, "data": data}
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
    raw = json.load(open("candidates_raw.json", encoding="utf-8"))
    out, buckets = [], {"keep": 0, "drop": 0, "review": 0}
    for it in raw["items"]:
        c = classify(it)
        buckets[c["verdict"]] += 1
        out.append({**it, **c, "slug": slug(it["name"])})

    merged: dict[str, list] = {}
    for o in out:
        merged.setdefault(o["slug"], []).append(o["name"])
    dupes = {k: v for k, v in merged.items() if len(v) > 1}

    json.dump({"buckets": buckets, "dupe_slugs": dupes,
               "boundaries": raw.get("boundaries", []) + [
                   "슬러그 병합은 마지막 경로 조각 휴리스틱이다 — 동명이인을 합칠 수 있다",
                   "keep/drop 판정은 이름·설명 문자열만 본다. 실제 도구 목록은 안 봤다(다음 단계=실호출)"],
               "items": out},
              open("candidates_filtered.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"입력 {len(out)}건 → keep {buckets['keep']} · review {buckets['review']} · drop {buckets['drop']}")
    print(f"슬러그 중복 {len(dupes)}건(레지스트리↔GitHub 같은 서버로 추정)")
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
