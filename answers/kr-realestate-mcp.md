# io.github.hoftlab/kr-realestate-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://kr-realestate-mcp.gamto.workers.dev/mcp`.


---

# 1회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_region_lookup | `{"query":"서울 강남구"}` | 강남구 지역코드(11680) 확인, rc=0 |
| 2 | kr_region_market | `{"region":"11680"}` | 강남구 실거래 시장 데이터 조회, rc=0 |

### 답변

서울 강남구 아파트 실거래가는 **평균 2억 6,500만 원**(3개월 기준, 2026년 9월~11월)으로, 지난 시즌 대비 **평당가 8.6% 상승**했습니다.

**최근 거래 추이:**
- 9월: 거래 124건, 중위가 2억 8,575만 원 (평당 11,754만원/평)
- 10월: 거래 79건, 중위가 2억 5,000만 원 (평당 12,768만원/평)
- 11월: 아직 거래 없음 (신고 대기 중)

**지역별 편차가 큽니다:**
- 압구정동: 최고가 7억 2,000만 원 (평당 16,541만원/평)
- 대치동: 3억 1,500만 원 (평당 13,432만원/평)
- 역삼동: 9,325만 원 (평당 5,106만원/평, 가장 저가)

**면적대별 시세:**
- 135㎡ 초과: 4억 8,500만 원
- 85~135㎡: 3억 5,600만 원
- 60~85㎡: 3억 675만 원
- 60㎡ 미만: 1억 5,500만 원

**거래량 많은 단지:** 은마(대치동, 21건, 중위 3억 1,550만 원)가 가장 활발합니다.

### 근거로 쓴 응답 발췌

```
{"region":{"lawdCd":"11680","lawdCds":["11680"],"fullName":"서울특별시 강남구","umd":null},
"period":{"from":"2026-09","to":"2026-11","yms":["202609","202610","202611"]},
"unit":{"amount":"만원","pricePerPyeong":"만원/평"},
"market":{"total":{"count":203,"cancelled":4,"complexes":99,"median":265000,"medianPerPyeong":12247,
"perPyeongHalfChangePct":8.6},
"monthly":[{"ym":"2026-09","incomplete":false,"count":124,"cancelled":1,"directSharePct":5.6,
"median":285750,"medianPerPyeong":11754},
{"ym":"2026-10","incomplete":true,"count":79,"cancelled":3,"directSharePct":3.8,"median":250000,
"medianPerPyeong":12768},
{"ym":"2026-11","incomplete":true,"count":0,"cancelled":0,"directSharePct":null,"median":null,
"medianPerPyeong":null}],
"byUmd":[{"umd":"압구정동","count":18,"median":720000,"medianPerPyeong":16541},
{"umd":"대치동","count":39,"median":315000,"medianPerPyeong":13432},
{"umd":"개포동","count":38,"median":301000,"medianPerPyeong":13812},
{"umd":"역삼동","count":24,"median":93250,"medianPerPyeong":5106}],
"areaMix":[{"band":"135㎡ 초과","count":27,"median":485000},
{"band":"85~135㎡","count":26,"median":356000},
{"band":"60~85㎡","count":82,"median":306750},
{"band":"60㎡ 미만","count":68,"median":155000}],
"topByCount":[{"aptName":"은마","umd":"대치동","buildYear":1979,"count":21,"median":315500,
"medianPerPyeong":13561}]
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

(이 서버에는 경매 도구가 없으므로 도구 호출 없음)

### 답변

죄송하지만, 이 MCP 서버는 **경매 정보를 제공하지 않습니다**. 

이 서버가 다루는 범위는 아파트 **실거래 시세**·**단지 정보**·**청약 분양** 공고뿐이며, 법원경매나 온비드 공매 데이터는 보유하지 않습니다.

경매 정보(특히 유찰 통계)를 조회하려면 법원경매 시스템이나 온비드 등 별도 경매 전문 서버에 문의하세요.

### 근거로 쓴 응답 발췌

```
kr_pricing 도구 목록:
kr_apt_search, kr_apt_trades, kr_apt_price_summary, kr_apt_rents, kr_apt_rent_summary,
kr_apt_profile, kr_apt_report, kr_region_market, kr_presale_trades, kr_apt_compare,
kr_subscription_search, kr_subscription_competition
(경매·공매 도구 없음)
```

---

# 2회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_region_market | `{"region":"서울 강남구"}` | 강남구 최근 3개월(9월~11월) 매매 시장 현황 조회 완료, rc=0 |

### 답변

서울 강남구의 아파트 실거래가는 최근 몇 개월 상승 추세를 보이고 있습니다.

**최근 3개월(9월~11월) 시장 현황:**
- 총 거래건수: 203건
- 중위가: 265,000만원
- 평당가: 12,247만원/평 (9월 대비 8.6% 상승)

**월별 추이:**
- 9월: 중위가 285,750만원 (평당가 11,754만원/평, 124건)
- 10월: 중위가 250,000만원 (평당가 12,768만원/평, 79건) - 10월은 실거래 신고 기한 때문에 아직 집계 중
- 11월: 아직 거래가 없음 (현재 월이라 집계 미완)

**지역별 시세 차이:**
- 가장 비싼 지역: 압구정동 (중위가 720,000만원, 평당가 16,541만원/평)
- 대치동: 중위가 315,000만원
- 개포동: 중위가 301,000만원

**면적대별 분포:**
- 135㎡ 초과: 중위가 485,000만원
- 85~135㎡: 중위가 356,000만원
- 60~85㎡: 중위가 306,750만원
- 60㎡ 미만: 중위가 155,000만원

### 근거로 쓴 응답 발췌

```
{"region":{"lawdCd":"11680","lawdCds":["11680"],"fullName":"서울특별시 강남구","umd":null},"period":{"from":"2026-09","to":"2026-11","yms":["202609","202610","202611"]},"unit":{"amount":"만원","pricePerPyeong":"만원/평"},"market":{"total":{"count":203,"cancelled":4,"complexes":99,"median":265000,"medianPerPyeong":12247,"perPyeongHalfChangePct":8.6},"monthly":[{"ym":"2026-09","incomplete":false,"count":124,"cancelled":1,"directSharePct":5.6,"median":285750,"medianPerPyeong":11754},{"ym":"2026-10","incomplete":true,"count":79,"cancelled":3,"directSharePct":3.8,"median":250000,"medianPerPyeong":12768},{"ym":"2026-11","incomplete":true,"count":0,"cancelled":0,"directSharePct":null,"median":null,"medianPerPyeong":null}]
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | 도구 목록 조회 | N/A | 경매 관련 도구 없음, rc=3 |

### 답변

죄송하지만, 이 서버에서는 **경매 관련 도구를 제공하지 않습니다**. 

이 서버가 제공하는 도구들은 아파트 실거래가, 분양 정보, 청약 현황 등 일반 매매 시장 정보에 한정되어 있습니다. 법원경매의 유찰률 통계나 경매 물건 정보는 이 서버의 범위를 벗어납니다.

경매 정보를 조회하려면 법원 경매 정보시스템이나 캠코(온비드) 등 경매 전문 데이터베이스를 이용하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
kr_pricing
kr_region_lookup
kr_apt_search
kr_apt_trades
kr_apt_price_summary
kr_apt_rents
kr_apt_rent_summary
kr_apt_profile
kr_apt_report
kr_region_market
kr_presale_trades
kr_apt_compare
kr_subscription_search
kr_subscription_competition
```
제공 도구는 위 13종이며, 경매(auction), 유찰(unsold) 관련 도구는 없음.

---

# 3회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_region_market | `{"region":"서울 강남구"}` | 강남구 시장 스냅샷 조회 성공, rc=0 |

### 답변

서울 강남구 아파트 실거래가는 **최근 3개월(9월~11월) 중위가 265,000만원, 평당 12,247만원**입니다.

월별로 보면:
- **9월**: 중위가 285,750만원(평당 11,754만원), 거래 124건
- **10월**: 중위가 250,000만원(평당 12,768만원), 거래 79건
- **11월**: 아직 신고 기한 전이라 거래 0건(집계 진행 중)

9월 대비 10월에 **중위가가 약 125,750만원 하락**(약 -44%)했고, **평당가는 상승**(약 +8.6%)한 상태입니다. 거래량은 감소 추세입니다.

동별로는 **압구정동이 평당 16,541만원으로 가장 비싸고**, 개포동(평당 13,812만원), 대치동(평당 13,432만원)이 뒤를 잇습니다. 면적대로는 135㎡ 초과 대형이 485,000만원(27건) 중위가로 가장 높습니다.

거래가 가장 활발한 단지는 **은마(대치동, 21건, 중위가 315,500만원)**이고, 그 다음이 개포주공6단지(개포동, 9건)입니다.

### 근거로 쓴 응답 발췌

```
"total":{"count":203,"cancelled":4,"complexes":99,"median":265000,"medianPerPyeong":12247,"perPyeongHalfChangePct":8.6},
"monthly":[
{"ym":"2026-09","incomplete":false,"count":124,"cancelled":1,"directSharePct":5.6,"median":285750,"medianPerPyeong":11754},
{"ym":"2026-10","incomplete":true,"count":79,"cancelled":3,"directSharePct":3.8,"median":250000,"medianPerPyeong":12768},
{"ym":"2026-11","incomplete":true,"count":0,"cancelled":0,"directSharePct":null,"median":null,"medianPerPyeong":null}
],
"byUmd":[
{"umd":"압구정동","count":18,"median":720000,"medianPerPyeong":16541},
{"umd":"개포동","count":38,"median":301000,"medianPerPyeong":13812},
{"umd":"대치동","count":39,"median":315000,"medianPerPyeong":13432}
],
"areaMix":[
{"band":"135㎡ 초과","count":27,"median":485000}
],
"topByCount":[
{"aptName":"은마","umd":"대치동","count":21,"median":315500,"medianPerPyeong":13561},
{"aptName":"개포주공6단지","umd":"개포동","count":9,"median":320000,"medianPerPyeong":16603}
],
"note":"실거래 신고 기한(계약 후 30일) 때문에 이번 달·지난달(incomplete=true)은 건수가 아직 늘어나는 중이다."
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| (도구 없음) | (경매 관련 도구 조회) | - | rc=3 |

### 답변

죄송합니다만, **이 서버는 경매 관련 도구를 제공하지 않습니다**. 

도구 목록을 조회한 결과 총 14개의 도구가 있으나, 모두 다음 범주에 한정됩니다:
- 아파트 실거래(매매, 전월세)
- 단지 검색·분석·비교
- 청약(분양) 공고·경쟁률
- 분양권 거래

법원경매나 공매의 유찰·낙찰률 통계는 이 서버의 지원 범위 밖입니다. 경매 정보가 필요하시면 다른 부동산 정보 서버를 이용하시기 바랍니다.
