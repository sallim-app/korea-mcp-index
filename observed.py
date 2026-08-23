#!/usr/bin/env python3
"""불러 보고 알게 된 것 — 수집 분야의 교정 (2026-08-19).

**분류가 검색어를 낳는다**(`categories.py`)는 수집엔 옳지만, 그 검색어가 그 서버의
정체를 정하지는 않는다. `mcp 네이버`로 잡힌 서버가 뉴스 배포 API일 수 있다.
실제로 도구를 부르기 전까지 우리는 그것을 알 방법이 없었다 — 그리고 모르는 채로
**그 서버를 남의 분야 질문으로 채점하고 순위를 매겼다.**

그건 측정이 아니라 오심이다. 한국일보 뉴스 서버에게 "요즘 많이 팔리는 상품이 뭐야"를
묻고 못 답했다고 순위를 내리는 것은 그 서버에 대해 아무것도 재지 않은 것과 같다.

그래서 규칙: **채점 과정에서 실제 주제가 다르다고 확인된 서버는 그 분야의 순위에서
뺀다.** 지우지는 않는다 — 「분야 교정」 구역에 실제로 무엇을 하는지와 함께 남긴다.
이것이 기치 ②(못 봄 ≠ 없음)를 우리 자신에게 적용하는 자리다: 우리가 잘못 넣은 것을
조용히 빼면 독자는 그 서버를 영영 못 본다.

각 항목의 `근거`는 `grades/<분야>.json`에 실제로 들어 있는 문장이다 —
`tests/test_observed.py`가 축자 대조로 검증한다. 우리가 지어낸 판정이 아니다.
"""

# 서버 → (수집된 분야, 실제 분야, 채점자 원문 발췌)
MISFILED: dict[str, tuple[str, str, str]] = {
    "com.hankookilbo.mcp/hankookilbo-mcp": (
        "커머스·생활", "미디어·뉴스",
        "상품·예약과는 무관한 미디어 서버다.",
    ),
    "com.saaskr/korean-saas-directory": (
        "커머스·생활", "디렉토리·개발자도구",
        "상품 판매나 예약을 하는 곳이 아니다.",
    ),
    "app.apick/finance": (
        "금융·증시", "핀테크·인증",
        "이름만 finance일 뿐 실제로는 은행 계좌 검증(1원 인증·실명조회) 서비스로 "
        "한국 증시와 주제가 다르며",
    ),
    "MosslandOpenDevs/alpha": (
        "금융·증시", "미디어·뉴스",
        "한국 크립토·매크로 뉴스 알파 서버로 증시와 주제가 다르며",
    ),
    "app.apick/business": (
        "공공데이터·행정", "커머스·생활",
        "상거래·물류 데이터형 서버로 이 분야 두 질문은 설계 범위 밖이며",
    ),
    "yousunjung84-edu/academyinfo-mcp": (
        "공공데이터·행정", "교육·문화",
        "이름과 달리 학원이 아니라 대학알리미 기반 고등교육 통계 서버로, "
        "공공데이터·행정 분야와는 주제가 다르며",
    ),
}

# 분야는 맞으나 **무엇을 주는지**가 독자의 기대와 다른 것. 순위에서 빼지 않는다 —
# 이건 오심이 아니라 그 서버의 성질이고, 성질을 모르고 쓰면 값을 헛짚는다.
SCOPE: dict[str, str] = {
    "haklaekim/public-data-lens":
        "카탈로그형 — 값이 아니라 데이터셋 위치를 준다",
    "obundh/korea-public-data-catalog-mcp":
        "카탈로그형 — 값이 아니라 데이터셋 위치를 준다",
    "com.airblockfz/seoul-apt-signal":
        "실거래가가 아니라 산식 미공개 매매신호. 분석 도구는 HTTP 402(사실상 유료)",
    "hlucent/realestate-stats-mcp":
        "개별 실거래가 아니라 한국부동산원 집계 통계표. 분당 3회 제한",
    "com.theprotoclinical/commerce":
        "특정 Shopify 스토어 한 곳의 결제 엔드포인트(UCP)",
    "ai.timeplex/booking":
        "뷰티·웰니스 예약. 등록 매장 1곳",
    "com.arcasos/arcasos-rentals":
        "주 단위 단기임차. 총계 미공시로 항상 10건에서 조용히 잘린다",
    # 분야가 틀렸을 개연성이 크지만(같은 운영사 app.apick/business가 상거래다)
    # 전 도구가 키 게이트라 **확인하지 못했다** — 확인 못 한 것을 교정으로 적지 않는다.
    "app.apick/all":
        "전 도구가 API 키 게이트라 종류(데이터형/카탈로그형)조차 확인할 수 없었다",
}


# 저장소가 옮겨간 것 — **같은 서버다**. 새 이름 → 옛 이름 (2026-08-24).
#
# 순위(ranking.json)·범위 공시(SCOPE)·분야 교정(MISFILED)은 전부 **이름**을 키로 붙는다.
# 이름이 바뀐 것을 모르면 그 서버는 "지난주에 죽고 이번 주에 새로 태어난" 것으로 게시된다 —
# 실제로 받아 둔 등수가 통째로 사라지고, 독자는 1위가 없어진 분야를 본다. 우리 잣대가
# 흔들린 것을 남의 서버가 바뀐 것처럼 싣는 자리라 조용히 넘기면 안 된다.
#
# **같은 서버라는 근거는 이름이 아니라 주소다.** 이름만 닮은 다른 서버를 여기 적으면
# 남이 받은 등수를 엉뚱한 서버에 옮겨 붙이게 된다 — 주소가 같을 때만 적는다.
RENAMED: dict[str, str] = {
    # haklaekim/public-data-lens → hike-lab/public-data-lens.
    # 근거 ①: 두 저장소의 README가 같은 커넥터를 선언한다
    #        (https://service.datahub.kr/projects/public-data-lens/mcp).
    # 근거 ②: 2026-08-19 측정본에서 두 이름의 remote.url이 같았다(그때는 둘 다 후보라
    #        주소 중복 제거가 합쳤고, 살아남은 이름이 haklaekim 쪽이라 등수도 거기 붙었다).
    # 근거 ③: 옛 경로는 GitHub 404이고 **리디렉트가 없다** — 그래서 자동으로는 못 잇는다.
    "hike-lab/public-data-lens": "haklaekim/public-data-lens",
}

# 이름만 바뀐 서버가 옛 이름으로 받아 둔 공시를 그대로 잇는다. 손으로 두 번 적지 않는다 —
# 한쪽만 고치면 표와 근거가 어긋나고, 그 어긋남은 조용하다.
for _new, _old in RENAMED.items():
    if _old in SCOPE and _new not in SCOPE:
        SCOPE[_new] = SCOPE[_old]
    if _old in MISFILED and _new not in MISFILED:
        MISFILED[_new] = MISFILED[_old]


def misfiled_in(category: str) -> dict[str, tuple[str, str, str]]:
    return {k: v for k, v in MISFILED.items() if v[0] == category}


if __name__ == "__main__":
    print(f"분야 교정 {len(MISFILED)}건 · 범위 공시 {len(SCOPE)}건 · 개명 {len(RENAMED)}건")
    for n, (was, now, why) in MISFILED.items():
        print(f"  {n:<42} {was} → {now}")
    for n, o in RENAMED.items():
        print(f"  개명 {o} → {n}")
