# io.github.pipeworx-io/dart-kr

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/dart-kr/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"삼성전자 최근 실적 매출 영업이익"}` | 최근 반기보고서 조회, rc=0 |
| 2 | dart_financials | `{"corp_code":"00126380","bsns_year":"2026","reprt_code":"11"}` | 2026 반기 재무정보 반환, rc=0 |

### 답변

삼성전자의 2026년 상반기(1-6월) 반기보고서 기준 실적입니다.

**연결기준:**
- 매출액: 171조 4,994억 7,000만 원
- 영업이익: 89조 4,924억 1,200만 원

지난해 같은 기간(2025년 상반기) 대비 매출은 2.3배 증가했고, 영업이익은 약 19배 증가한 수치입니다.

### 근거로 쓴 응답 발췌

```
{
  "corp_code": "00126380",
  "bsns_year": "2026",
  "reprt_code": "11",
  "fs_div": "CFS",
  "count": 30,
  "statements": [
    {
      "statement_division": "IS",
      "statement_name": "손익계산서",
      "account_name": "매출액",
      "current_period_label": "제 58 기반기",
      "current_period_amount": "171,499,470,000,000",
      "prior_period_label": "제 57 기반기",
      "prior_period_amount": "74,566,317,000,000",
      "currency": "KRW"
    },
    {
      "statement_division": "IS",
      "statement_name": "손익계산서",
      "account_name": "영업이익",
      "current_period_label": "제 58 기반기",
      "current_period_amount": "89,492,412,000,000",
      "prior_period_label": "제 57 기반기",
      "prior_period_amount": "4,676,057,000,000",
      "currency": "KRW"
    }
  ]
}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"코스피 시가총액 상위 종목"}` | kr_top_by_market_cap 라우팅, rc=0 |

### 답변

2026년 11월 3일 현재 코스피 시가총액 상위 종목입니다:

1. **삼성전자** (005930) - 1,297조 8,739억 원
2. **SK하이닉스** (000660) - 1,032조 9,162억 원
3. **삼성전자우** (005935) - 139조 509억 원
4. **SK스퀘어** (402340) - 120조 1,828억 원
5. **삼성전기** (009150) - 84조 1,051억 원
6. **LG에너지솔루션** (373220) - 80조 2,620억 원
7. **삼성바이오로직스** (207940) - 66조 4,275억 원
8. **현대차** (005380) - 56조 7,672억 원
9. **KB금융** (105560) - 53조 9,125억 원
10. **삼성생명** (032830) - 52조 7,000억 원

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
      "market_cap_text": "139조 509억원"
    },
    {
      "rank": 4,
      "code": "402340",
      "name_ko": "SK스퀘어",
      "market_cap_text": "120조 1,828억원"
    },
    {
      "rank": 5,
      "code": "009150",
      "name_ko": "삼성전기",
      "market_cap_text": "84조 1,051억원"
    },
    {
      "rank": 6,
      "code": "373220",
      "name_ko": "LG에너지솔루션",
      "market_cap_text": "80조 2,620억원"
    },
    {
      "rank": 7,
      "code": "207940",
      "name_ko": "삼성바이오로직스",
      "market_cap_text": "66조 4,275억원"
    },
    {
      "rank": 8,
      "code": "005380",
      "name_ko": "현대차",
      "market_cap_text": "56조 7,672억원"
    },
    {
      "rank": 9,
      "code": "105560",
      "name_ko": "KB금융",
      "market_cap_text": "53조 9,125억원"
    },
    {
      "rank": 10,
      "code": "032830",
      "name_ko": "삼성생명",
      "market_cap_text": "52조 7,000억원"
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
| 1 | ask_pipeworx | `{"question":"삼성전자 최근 실적 매출 영업이익"}` | DART 반기보고서(2026.06) 공시 확인, rc=0 |
| 2 | dart_financials | `{"corp_code":"00126380","bsns_year":"2026","reprt_code":"06"}` | 연결 재무제표 손익계산서 확인, rc=0 |

### 답변

삼성전자의 2026년 반기(2026년 상반기) 실적은 다음과 같습니다.

- **매출액**: 171조 4,994억 7,000만원
- **영업이익**: 89조 4,924억 1,200만원

연결 재무제표 기준이며, 작년 같은 기간(2025년 상반기)과 비교하면 매출액은 74조 5,663억원에서 2배 이상 증가했고, 영업이익은 4조 6,760억원에서 약 19배 증가했습니다.

### 근거로 쓴 응답 발췌

```
"statements":[
  {
    "statement_division":"IS",
    "statement_name":"손익계산서",
    "account_name":"매출액",
    "current_period_label":"제 58 기반기",
    "current_period_amount":"171,499,470,000,000",
    "prior_period_label":"제 57 기반기",
    "prior_period_amount":"74,566,317,000,000",
    "currency":"KRW"
  },
  {
    "statement_division":"IS",
    "statement_name":"손익계산서",
    "account_name":"영업이익",
    "current_period_label":"제 58 기반기",
    "current_period_amount":"89,492,412,000,000",
    "prior_period_label":"제 57 기반기",
    "prior_period_amount":"4,676,057,000,000",
    "currency":"KRW"
  }
]
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"코스피 시가총액 상위 종목 순위"}` | kr_top_by_market_cap으로 라우팅, KOSPI 상위 50개 종목 확인, rc=0 |

### 답변

2026년 11월 3일 종가 기준 코스피 시가총액 상위 종목은 다음과 같습니다.

1. **삼성전자** (005930) - 1,297조 8,739억원
2. **SK하이닉스** (000660) - 1,032조 9,162억원
3. **삼성전자우** (005935) - 139조 509억원
4. **SK스퀘어** (402340) - 120조 1,828억원
5. **삼성전기** (009150) - 84조 1,051억원
6. **LG에너지솔루션** (373220) - 80조 2,620억원
7. **삼성바이오로직스** (207940) - 66조 4,275억원
8. **현대차** (005380) - 56조 7,672억원
9. **KB금융** (105560) - 53조 9,125억원
10. **삼성생명** (032830) - 52조 7,000억원

상위 10개 중 삼성 계열사가 4개(삼성전자, 삼성전자우, 삼성전기, 삼성생명)를 차지하고 있으며, 삼성전자와 SK하이닉스의 시가총액이 압도적으로 높습니다.

### 근거로 쓴 응답 발췌

```
{"market":"KOSPI","page":1,"count":50,"results":[
  {"rank":1,"code":"005930","name_ko":"삼성전자","price":222000,"change_pct":-3.06,"market_cap_text":"1,297조 8,739억원"},
  {"rank":2,"code":"000660","name_ko":"SK하이닉스","price":1414000,"change_pct":-3.94,"market_cap_text":"1,032조 9,162억원"},
  {"rank":3,"code":"005935","name_ko":"삼성전자우","price":173300,"change_pct":-2.09,"market_cap_text":"139조 509억원"},
  {"rank":4,"code":"402340","name_ko":"SK스퀘어","price":911000,"change_pct":-4.11,"market_cap_text":"120조 1,828억원"},
  {"rank":5,"code":"009150","name_ko":"삼성전기","price":1126000,"change_pct":-5.62,"market_cap_text":"84조 1,051억원"},
  {"rank":6,"code":"373220","name_ko":"LG에너지솔루션","price":343000,"change_pct":-3.65,"market_cap_text":"80조 2,620억원"},
  {"rank":7,"code":"207940","name_ko":"삼성바이오로직스","price":1435000,"change_pct":0.91,"market_cap_text":"66조 4,275억원"},
  {"rank":8,"code":"005380","name_ko":"현대차","price":279000,"change_pct":-2.79,"market_cap_text":"56조 7,672억원"},
  {"rank":9,"code":"105560","name_ko":"KB금융","price":152000,"change_pct":-0.91,"market_cap_text":"53조 9,125억원"},
  {"rank":10,"code":"032830","name_ko":"삼성생명","price":263500,"change_pct":-3.12,"market_cap_text":"52조 7,000억원"}
]}
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | dart_financials | `{"corp_code":"00126380","bsns_year":"2026","reprt_code":"13"}` | 2026년 3분기 연결 재무제표, rc=0 |

### 답변

삼성전자의 2026년 3분기(제58기반기) 실적은 매출액 171조 4,994억 원, 영업이익 89조 4,924억 원입니다.

3분기 전년 동기 대비 매출은 약 130% 증가했고, 영업이익은 약 1,813% 증가한 것으로 나타났습니다.

### 근거로 쓴 응답 발췌

```
"statement_division":"IS","statement_name":"손익계산서","account_name":"매출액","current_period_label":"제 58 기반기","current_period_amount":"171,499,470,000,000","prior_period_label":"제 57 기반기","prior_period_amount":"74,566,317,000,000","currency":"KRW"

"statement_division":"IS","statement_name":"손익계산서","account_name":"영업이익","current_period_label":"제 58 기반기","current_period_amount":"89,492,412,000,000","prior_period_label":"제 57 기반기","prior_period_amount":"4,676,057,000,000","currency":"KRW"
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_top_by_market_cap | `{"market":"KOSPI","limit":10}` | 2026-11-03 기준 코스피 시가총액 상위 10개 종목, rc=0 |

### 답변

2026년 11월 3일 현재 코스피 시가총액 상위 10개 종목은 다음과 같습니다:

1. **삼성전자**(005930) - 1,297조 8,739억원
2. **SK하이닉스**(000660) - 1,032조 9,162억원
3. **삼성전자우**(005935) - 139조 509억원
4. **SK스퀘어**(402340) - 120조 1,828억원
5. **삼성전기**(009150) - 84조 1,051억원
6. **LG에너지솔루션**(373220) - 80조 2,620억원
7. **삼성바이오로직스**(207940) - 66조 4,275억원
8. **현대차**(005380) - 56조 7,672억원
9. **KB금융**(105560) - 53조 9,125억원
10. **삼성생명**(032830) - 52조 7,000억원

### 근거로 쓴 응답 발췌

```
{"rank":1,"code":"005930","name_ko":"삼성전자","price":222000,"change_pct":-3.06,"volume":13389433,"market_cap_text":"1,297조 8,739억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:21+09:00"}

{"rank":2,"code":"000660","name_ko":"SK하이닉스","price":1414000,"change_pct":-3.94,"volume":2302839,"market_cap_text":"1,032조 9,162억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:24+09:00"}

{"rank":3,"code":"005935","name_ko":"삼성전자우","price":173300,"change_pct":-2.09,"volume":2359540,"market_cap_text":"139조 509억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:22+09:00"}

{"rank":4,"code":"402340","name_ko":"SK스퀘어","price":911000,"change_pct":-4.11,"volume":473468,"market_cap_text":"120조 1,828억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:21+09:00"}

{"rank":5,"code":"009150","name_ko":"삼성전기","price":1126000,"change_pct":-5.62,"volume":622995,"market_cap_text":"84조 1,051억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:25+09:00"}

{"rank":6,"code":"373220","name_ko":"LG에너지솔루션","price":343000,"change_pct":-3.65,"volume":502945,"market_cap_text":"80조 2,620억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:18+09:00"}

{"rank":7,"code":"207940","name_ko":"삼성바이오로직스","price":1435000,"change_pct":0.91,"volume":51571,"market_cap_text":"66조 4,275억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:23+09:00"}

{"rank":8,"code":"005380","name_ko":"현대차","price":279000,"change_pct":-2.79,"volume":461930,"market_cap_text":"56조 7,672억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:24+09:00"}

{"rank":9,"code":"105560","name_ko":"KB금융","price":152000,"change_pct":-0.91,"volume":735755,"market_cap_text":"53조 9,125억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:20+09:00"}

{"rank":10,"code":"032830","name_ko":"삼성생명","price":263500,"change_pct":-3.12,"volume":200021,"market_cap_text":"52조 7,000억원","market_status":"CLOSE","as_of":"2026-11-03T20:20:22+09:00"}
```
