# io.github.pipeworx-io/kr-equities

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/kr-equities/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"삼성전자의 최근 분기 실적 매출과 영업이익은?"}` | DART 공시 링크 반환, rc=0 |
| 2 | ask_pipeworx | `{"question":"Samsung Electronics 005930 quarterly earnings revenue operating profit 2026"}` | 도구 없음 오류, rc=1 |

### 답변

죄송합니다. 이 MCP 서버는 한국 주식의 분기별 매출과 영업이익 수치를 제공하지 않습니다.

서버가 제공하는 한국 주식 도구(`kr_quote`, `kr_search_stocks`, `kr_investor_flows`)는 현재 시세·종목 정보·투자자 유형별 거래량만 담당하며, 재무 실적 데이터는 커버하지 않습니다. 

삼성전자의 공식 분기 실적은 금융감독원 DART 전자공시(https://dart.fss.or.kr)에서 반기보고서 또는 분기보고서를 통해 조회하실 수 있습니다. 해당 공시서에 매출(연결/별도)과 영업이익 수치가 기재되어 있습니다.

### 근거로 쓴 응답 발췌

```
{
  "error": "no_match",
  "filter_gap": "metric: quarterly revenue and operating profit for 005930 — no listed tool provides Korean corporate financial statements; only quote/identity/investor-flow data is available",
  "message": "Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists. Detail: The only Korean-equity tools available (kr_quote, kr_search_stocks, kr_investor_flows) return price/quote, identity, and investor-flow data — none exposes quarterly earnings, revenue, or operating profit for Samsung Electronics, and no other listed tool covers Korean financial statements."
}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_top_by_market_cap | `{"market":"KOSPI"}` | 상위 10개 종목 반환, rc=0 |

### 답변

코스피 시가총액 상위 10개 종목은 다음과 같습니다(2026-11-03 종가 기준):

1. **삼성전자** (005930) - 1,297조 8,739억원 | 222,000원 (-3.06%)
2. **SK하이닉스** (000660) - 1,032조 9,162억원 | 1,414,000원 (-3.94%)
3. **삼성전자우** (005935) - 139조 509억원 | 173,300원 (-2.09%)
4. **SK스퀘어** (402340) - 120조 1,828억원 | 911,000원 (-4.11%)
5. **삼성전기** (009150) - 84조 1,051억원 | 1,126,000원 (-5.62%)
6. **LG에너지솔루션** (373220) - 80조 2,620억원 | 343,000원 (-3.65%)
7. **삼성바이오로직스** (207940) - 66조 4,275억원 | 1,435,000원 (+0.91%)
8. **현대차** (005380) - 56조 7,672억원 | 279,000원 (-2.79%)
9. **KB금융** (105560) - 53조 9,125억원 | 152,000원 (-0.91%)
10. **삼성생명** (032830) - 52조 7,000억원 | 263,500원 (-3.12%)

삼성전자가 시가총액 1,297조원 규모로 압도적 1위이며, SK하이닉스가 1,032조원으로 뒤따릅니다.

### 근거로 쓴 응답 발췌

```
{
  "market": "KOSPI",
  "page": 1,
  "count": 10,
  "results": [
    {
      "rank": 1,
      "code": "005930",
      "name_ko": "삼성전자",
      "price": 222000,
      "change_pct": -3.06,
      "volume": 13389433,
      "market_cap_text": "1,297조 8,739억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:21+09:00"
    },
    {
      "rank": 2,
      "code": "000660",
      "name_ko": "SK하이닉스",
      "price": 1414000,
      "change_pct": -3.94,
      "volume": 2302839,
      "market_cap_text": "1,032조 9,162억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:24+09:00"
    },
    {
      "rank": 3,
      "code": "005935",
      "name_ko": "삼성전자우",
      "price": 173300,
      "change_pct": -2.09,
      "volume": 2359540,
      "market_cap_text": "139조 509억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:22+09:00"
    },
    {
      "rank": 4,
      "code": "402340",
      "name_ko": "SK스퀘어",
      "price": 911000,
      "change_pct": -4.11,
      "volume": 473468,
      "market_cap_text": "120조 1,828억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:21+09:00"
    },
    {
      "rank": 5,
      "code": "009150",
      "name_ko": "삼성전기",
      "price": 1126000,
      "change_pct": -5.62,
      "volume": 622995,
      "market_cap_text": "84조 1,051억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:25+09:00"
    },
    {
      "rank": 6,
      "code": "373220",
      "name_ko": "LG에너지솔루션",
      "price": 343000,
      "change_pct": -3.65,
      "volume": 502945,
      "market_cap_text": "80조 2,620억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:18+09:00"
    },
    {
      "rank": 7,
      "code": "207940",
      "name_ko": "삼성바이오로직스",
      "price": 1435000,
      "change_pct": 0.91,
      "volume": 51571,
      "market_cap_text": "66조 4,275억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:23+09:00"
    },
    {
      "rank": 8,
      "code": "005380",
      "name_ko": "현대차",
      "price": 279000,
      "change_pct": -2.79,
      "volume": 461930,
      "market_cap_text": "56조 7,672억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:24+09:00"
    },
    {
      "rank": 9,
      "code": "105560",
      "name_ko": "KB금융",
      "price": 152000,
      "change_pct": -0.91,
      "volume": 735755,
      "market_cap_text": "53조 9,125억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:20+09:00"
    },
    {
      "rank": 10,
      "code": "032830",
      "name_ko": "삼성생명",
      "price": 263500,
      "change_pct": -3.12,
      "volume": 200021,
      "market_cap_text": "52조 7,000억원",
      "market_status": "CLOSE",
      "as_of": "2026-11-03T20:20:22+09:00"
    }
  ],
  "source": "Korea Exchange (KOSPI/KOSDAQ) market data",
  "data_as_of": "2026-11-03T20:20:21+09:00"
}
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_search_stocks | `{"query":"삼성전자"}` | 삼성전자 코드 005930 확인, rc=0 |
| 2 | kr_quote | `{"code":"005930"}` | 현재 주가 정보 응답, rc=0 |
| 3 | company_facts | `{"company":"005930","attribute":"revenue","period":{"type":"annual","fiscal_year":2025}}` | SEC 등록 회사만 지원으로 데이터 없음, rc=0 |
| 4 | entity_profile | `{"type":"company","value":"005930"}` | SEC 소스 없음, rc=0 |

### 답변

죄송하지만, 이 서버는 한국 회사의 매출과 영업이익 같은 구체적인 재무 실적 데이터를 제공하지 않습니다.

제공할 수 있는 것은 현재 주가 정보입니다. 삼성전자(005930)의 2026년 11월 3일 현재가는 **22만 2,000원**이며, 전날 종가 대비 **7,000원(-3.06%)** 하락했습니다. 시가총액은 **1,297조 8,739억 원**입니다.

**한국 회사의 최근 실적 정보가 필요하면** 한국거래소(KRX)의 전자공시시스템(DART)이나 각 회사의 공시 자료를 직접 확인하시는 것이 좋습니다. 이 서버는 주가·시가총액·투자자 수급 같은 시장 데이터에 특화되어 있습니다.

### 근거로 쓴 응답 발췌

```json
{
  "code": "005930",
  "name_ko": "삼성전자",
  "market": "KOSPI",
  "price": 222000,
  "change": -7000,
  "change_pct": -3.06,
  "market_cap_krw_text": "1,297조 8,739억",
  "eps_krw": 22292,
  "per": 9.96
}
```

```
"status": "unavailable",
"reason_code": "filer_submissions_unavailable",
"reason": "SEC returned 404 for this filer's submissions document"
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_top_by_market_cap | `{"market":"KOSPI"}` | KOSPI 상위 10개 종목 리스트, rc=0 |

### 답변

코스피 시가총액 상위 10개 종목은 다음과 같습니다 (2026년 11월 3일 장마감 기준):

| 순위 | 종목명 | 코드 | 현재가 | 전일대비 | 시가총액 |
|---|---|---|---|---|---|
| 1 | 삼성전자 | 005930 | 22만 2,000원 | -3.06% | 1,297조 8,739억원 |
| 2 | SK하이닉스 | 000660 | 141만 4,000원 | -3.94% | 1,032조 9,162억원 |
| 3 | 삼성전자우 | 005935 | 17만 3,300원 | -2.09% | 139조 509억원 |
| 4 | SK스퀘어 | 402340 | 91만 1,000원 | -4.11% | 120조 1,828억원 |
| 5 | 삼성전기 | 009150 | 112만 6,000원 | -5.62% | 84조 1,051억원 |
| 6 | LG에너지솔루션 | 373220 | 34만 3,000원 | -3.65% | 80조 2,620억원 |
| 7 | 삼성바이오로직스 | 207940 | 143만 5,000원 | +0.91% | 66조 4,275억원 |
| 8 | 현대차 | 005380 | 27만 9,000원 | -2.79% | 56조 7,672억원 |
| 9 | KB금융 | 105560 | 15만 2,000원 | -0.91% | 53조 9,125억원 |
| 10 | 삼성생명 | 032830 | 26만 3,500원 | -3.12% | 52조 7,000억원 |

삼성전자가 1조 297조 원 규모로 1위를 차지했으며, SK하이닉스(2위, 1조 32조 원), 삼성전자우(3위, 139조 원)가 뒤를 따릅니다. 전반적으로 반도체·전자 관련 종목이 상위를 차지했고, 대부분 전날 대비 하락한 상태입니다.

### 근거로 쓴 응답 발췌

```json
{
  "rank": 1,
  "code": "005930",
  "name_ko": "삼성전자",
  "price": 222000,
  "change_pct": -3.06,
  "market_cap_text": "1,297조 8,739억원"
}
```

```json
{
  "rank": 2,
  "code": "000660",
  "name_ko": "SK하이닉스",
  "price": 1414000,
  "change_pct": -3.94,
  "market_cap_text": "1,032조 9,162억원"
}
```

```json
{
  "rank": 3,
  "code": "005935",
  "name_ko": "삼성전자우",
  "price": 173300,
  "change_pct": -2.09,
  "market_cap_text": "139조 509억원"
}
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"삼성전자(005930)의 최근 실적 매출과 영업이익"}` | DART 공시 메타데이터만 반환, 실제 수치 없음, rc=0 |
| 2 | entity_profile | `{"type":"company","value":"Samsung Electronics"}` | SEC 등록 기업이 아님, 국제 자회사 정보만 반환, rc=0 |

### 답변

죄송하지만, 이 MCP 서버는 삼성전자의 최근 매출과 영업이익 수치를 직접 제공하지 않습니다. 

ask_pipeworx 도구로 조회했을 때는 한국거래소 공정거래위원회 공시(DART)에서 2026년 6월 반기보고서 메타데이터(보고서 이름, 접수 번호, 접수 일자)만 반환되었으며, 실제 매출과 영업이익 수치는 포함되지 않았습니다. DART는 공시 메타데이터만 제공하는 것으로 알려져 있습니다.

entity_profile 도구는 미국 SEC 등록 기업이나 국제 기업 등록 정보를 조회하는 도구로, 삼성전자(한국 코스피 상장사)는 지원하지 않습니다.

### 근거로 쓴 응답 발췌

```
ask_pipeworx 응답에서:
"pack":"dart-kr","reasoning":"Samsung Electronics is a Korean filer, so the only listed tool that can express the entity (corp_code 00126380) and pull its recent earnings disclosures is DART..."
"filter_gap":"values: DART returns filing metadata (report name/date/receipt no), not the actual revenue and operating profit numbers — no listed tool exposes Korean financial statement values directly..."

entity_profile 응답에서:
"notes":"Could not resolve \"Samsung Electronics\" to a US-listed public company (no CIK/ticker/name match in SEC's company_tickers.json)..."
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_top_by_market_cap | `{"market":"KOSPI"}` | 코스피 시가총액 상위 10개 종목 조회 성공, rc=0 |

### 답변

2026-11-03 기준 코스피 시가총액 상위 10개 종목은 다음과 같습니다:

1. **삼성전자** (005930) - 1,297조 8,739억원 / 현재가 22만 2,000원 / 변화 -3.06%
2. **SK하이닉스** (000660) - 1,032조 9,162억원 / 현재가 141만 4,000원 / 변화 -3.94%
3. **삼성전자우** (005935) - 139조 509억원 / 현재가 17만 3,300원 / 변화 -2.09%
4. **SK스퀘어** (402340) - 120조 1,828억원 / 현재가 91만 1,000원 / 변화 -4.11%
5. **삼성전기** (009150) - 84조 1,051억원 / 현재가 112만 6,000원 / 변화 -5.62%
6. **LG에너지솔루션** (373220) - 80조 2,620억원 / 현재가 34만 3,000원 / 변화 -3.65%
7. **삼성바이오로직스** (207940) - 66조 4,275억원 / 현재가 143만 5,000원 / 변화 +0.91%
8. **현대차** (005380) - 56조 7,672억원 / 현재가 27만 9,000원 / 변화 -2.79%
9. **KB금융** (105560) - 53조 9,125억원 / 현재가 15만 2,000원 / 변화 -0.91%
10. **삼성생명** (032830) - 52조 7,000억원 / 현재가 26만 3,500원 / 변화 -3.12%

### 근거로 쓴 응답 발췌

```
{"rank":1,"code":"005930","name_ko":"삼성전자","price":222000,"change_pct":-3.06,"market_cap_text":"1,297조 8,739억원","as_of":"2026-11-03T20:20:21+09:00"}
{"rank":2,"code":"000660","name_ko":"SK하이닉스","price":1414000,"change_pct":-3.94,"market_cap_text":"1,032조 9,162억원"}
{"rank":3,"code":"005935","name_ko":"삼성전자우","price":173300,"change_pct":-2.09,"market_cap_text":"139조 509억원"}
{"rank":4,"code":"402340","name_ko":"SK스퀘어","price":911000,"change_pct":-4.11,"market_cap_text":"120조 1,828억원"}
{"rank":5,"code":"009150","name_ko":"삼성전기","price":1126000,"change_pct":-5.62,"market_cap_text":"84조 1,051억원"}
{"rank":6,"code":"373220","name_ko":"LG에너지솔루션","price":343000,"change_pct":-3.65,"market_cap_text":"80조 2,620억원"}
{"rank":7,"code":"207940","name_ko":"삼성바이오로직스","price":1435000,"change_pct":0.91,"market_cap_text":"66조 4,275억원"}
{"rank":8,"code":"005380","name_ko":"현대차","price":279000,"change_pct":-2.79,"market_cap_text":"56조 7,672억원"}
{"rank":9,"code":"105560","name_ko":"KB금융","price":152000,"change_pct":-0.91,"market_cap_text":"53조 9,125억원"}
{"rank":10,"code":"032830","name_ko":"삼성생명","price":263500,"change_pct":-3.12,"market_cap_text":"52조 7,000억원"}
"source":"Korea Exchange (KOSPI/KOSDAQ) market data"
"data_as_of":"2026-11-03T20:20:21+09:00"
```
