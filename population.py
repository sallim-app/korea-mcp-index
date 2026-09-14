#!/usr/bin/env python3
"""측정 모집단 — **후보 전체와 실제로 잰 것의 차이를 값으로 말한다** (2026-09-14, T-2026W38-18).

계기. 판정기가 둘인데 모집단은 하나만 읽고 있었다.

  ① `filter_candidates.py` — 이름·설명의 **문자열**만 보는 키워드 판정기. keep/review/drop.
  ② 분류 단계의 **LLM 판정기**(`classification.json`) — 같은 항목에 `is_data_provider`를 붙인다.

`measure.py`는 ①의 `keep`만 재고, ②는 렌더 단계에서 「주제 밖」을 가려내는 데만 쓰였다.
그래서 ①이 `review`로 미룬 218건은 ②가 **데이터 제공형이라고 판정한 105건까지 통째로**
측정 밖에 있었는데, 게시본은 그 모집단을 「후보 전체 282건」이라고 적었다. 빠진 명단에
`042Jason/kosis-mcp`(KOSIS)·`MikeVenge/krx-dart-mcp`(DART)·`Tech-curator/korean-patent-mcp`
(특허청)·`SeoNaRu/korean-law-mcp`(법령)이 있었고 **우리 서버 `app.sallim/korea-stay`도 거기
있었다** — 우리가 남의 목록에서 잡아내는 종류의 은닉이다(기치 ②, 못 봄 ≠ 없음).

이 모듈이 그 둘을 한자리에서 맞춘다. 두 소비처가 있다.
  * `measure.py` — 다음 회차부터 **재는 모집단**을 정한다: keep + (review인데 ②가 데이터
    제공형이라 한 것). ②가 `false`라 한 review는 여전히 안 잰다(주제가 아니다).
  * `render_readme.py` / `render_site.py` — 잰 것 옆에 **안 잰 것을 같은 표에** 싣는다.
    수를 고치는 것보다 명단을 내놓는 것이 값이다.

원자료는 공개본만 읽는다(`candidates.json` + `classification.json`) — 둘 다 커밋돼 있어
남이 같은 수를 다시 뽑을 수 있다. `candidates_filtered.json`은 5~7MB라 안 실린다.
"""
import json

CANDIDATES = "candidates.json"
CLASSIFICATION = "classification.json"


def load_classification(path: str = CLASSIFICATION) -> dict:
    """name → 분류 레코드."""
    with open(path, encoding="utf-8") as f:
        return {v["name"]: v for v in json.load(f)["items"].values()}


def is_data_provider(cls: dict, name: str) -> bool:
    """LLM 분류기가 **데이터 제공형이라고 말한** 것만 True.

    분류가 없으면 False다 — 모르는 것을 '맞다'로 읽으면 모집단이 조용히 넓어진다.
    (모르는 것은 `unclassified`로 따로 세어 공시한다.)
    """
    rec = cls.get(name)
    return bool(rec and rec.get("is_data_provider"))


def measurable(items: list, cls: dict, bucket: str = "keep") -> list:
    """**재는 모집단.** keep + (review인데 LLM이 데이터 제공형이라 한 것).

    `bucket`이 keep이 아니면(진단용 실행) 종전대로 그 통만 준다 — 승격은 keep 회차의 규칙이다.
    """
    if bucket != "keep":
        return [i for i in items if i["verdict"] == bucket]
    return [i for i in items
            if i["verdict"] == "keep"
            or (i["verdict"] == "review" and is_data_provider(cls, i["name"]))]


def promoted(items: list, cls: dict) -> list:
    """승격분만 — review인데 LLM이 데이터 제공형이라 한 것."""
    return [i for i in items
            if i["verdict"] == "review" and is_data_provider(cls, i["name"])]


def measured_names(measured: str = "measured.json") -> set:
    """이미 잰 서버 이름. 합쳐진 이름(`also_known_as`)도 잰 것이다 — 빼면 유령이 생긴다."""
    try:
        with open(measured, encoding="utf-8") as f:
            d = json.load(f)
    except OSError:
        return set()
    out = set()
    for i in d.get("items") or []:
        out.add(i["name"])
        out.update(i.get("also_known_as") or [])
    return out


def summary(candidates: str = CANDIDATES, classification: str = CLASSIFICATION,
            measured: str = "measured.json") -> dict:
    """게시용 집계. 파일이 없으면 `None`을 돌려준다 — 렌더는 그 자리를 통째로 빼면 된다.

    **"안 잰 것"은 통 이름이 아니라 실측으로 가른다** — `measured.json`에 그 이름이 있는가.
    통(`review`)으로 가르면 승격이 적용된 회차에 이 표가 거꾸로 거짓말한다: 105건을 다 재
    놓고도 "재지 않은 218건"이라고 적게 된다. 다 잰 회차에는 이 집계가 스스로 0이 되어
    렌더에서 문단이 사라지는 것이 맞다.

    쓰는 쪽이 수를 다시 세지 않게 **명단째** 돌려준다. 수만 주면 다음 사람이 그 수를
    어디서 얻었는지 몰라 또 다른 계수기를 만든다(그게 이 결함의 발생 경로였다).
    """
    try:
        with open(candidates, encoding="utf-8") as f:
            src = json.load(f)
        cls = load_classification(classification)
    except OSError:
        return None
    # **`candidates.json`의 items가 곧 모집단은 아니다**(codex 교차검증 2026-09-15).
    # 게시 이력을 이어받은 줄은 `drop`이어도 이름째로 실린다(`export_candidates.py` —
    # 한 번 게시한 서버가 drop 통의 건수로만 남으면 또 조용히 사라지기 때문이다).
    # 그 줄까지 여기서 세면 **"한국 관련성은 통과했는데 안 잰 것"에 주제 밖이라 판정된
    # 줄이 섞여** 거짓 라벨이 되고 후보 총계도 부푼다. 통은 판정으로 가른다.
    items = [i for i in (src.get("items") or []) if i.get("verdict") in ("keep", "review")]
    done = measured_names(measured)
    not_measured = sorted((i for i in items if i["name"] not in done),
                          key=lambda i: i["name"])
    return {
        "total": len(items),
        "keep": [i for i in items if i["verdict"] == "keep"],
        "review": [i for i in items if i["verdict"] == "review"],
        "measured": [i for i in items if i["name"] in done],
        "not_measured": not_measured,
        # 안 잰 것 중 LLM이 "데이터 제공형"이라 한 것 = 쟀어야 하는 것.
        # **여기 `keep`이 섞일 수 있다**(codex 교차검증 2026-09-14): `--limit` 부분 측정이나
        # 후보·측정본의 회차 불일치면 keep인데 안 잰 것이 생긴다. 그때 "키워드 판정기가
        # 미뤘다"고 쓰면 거짓이므로, 통은 섞어 두고 **사유는 줄마다 verdict로** 적는다.
        "promoted": [i for i in not_measured if is_data_provider(cls, i["name"])],
        "promoted_review": [i for i in not_measured
                            if i["verdict"] == "review" and is_data_provider(cls, i["name"])],
        "promoted_keep": [i for i in not_measured
                          if i["verdict"] == "keep" and is_data_provider(cls, i["name"])],
        # 안 잰 것 중 **LLM이** "데이터 제공형이 아니다"라 한 것. 키워드 판정기 쪽은
        # `review`이고 그것은 "주제 밖"이 아니라 **신호 부족·판정 보류**다 — 둘을 "모두
        # 주제 밖이라 했다"로 합쳐 쓰면 113건에 거짓 라벨이 붙는다(codex 2026-09-14).
        "review_off": [i for i in not_measured
                       if i["name"] in cls and not cls[i["name"]].get("is_data_provider")],
        "unclassified": [i for i in not_measured if i["name"] not in cls],
        "cls": cls,
    }


if __name__ == "__main__":
    s = summary()
    if not s:
        raise SystemExit("candidates.json / classification.json이 없다")
    print(f"후보 전체 {s['total']}건 = keep {len(s['keep'])} + review {len(s['review'])}")
    print(f"  잰 것 {len(s['measured'])}건 · 안 잰 것 {len(s['not_measured'])}건")
    print(f"  안 잰 것 중 LLM이 데이터 제공형이라 한 것 {len(s['promoted'])}건 "
          f"— 쟀어야 하는 것이다(다음 회차부터 잰다)")
    print(f"  안 잰 것 중 LLM도 주제 밖이라 한 것 {len(s['review_off'])}건 · "
          f"분류 없음 {len(s['unclassified'])}건")
    for i in s["promoted"][:10]:
        c = s["cls"][i["name"]]
        print(f"    {i['name'][:44]:<44} {c['category'][:10]:<10} {c.get('why', '')[:30]}")
