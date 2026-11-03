# Mrbaeksang/korea-stock-analyzer-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://korea-stock-analyzer-mcp-production.up.railway.app/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"삼성전자"}` | 삼성전자 발견 (ticker: 005930), rc=0 |
| 2 | get_financials | `{"ticker":"005930"}` | 2025년 기준 최신 재무정보 조회, rc=0 |

### 답변

삼성전자의 2025년 최신 실적(연결재무제표 기준)은 다음과 같습니다:

- **매출**: 333조 6,059억 원
- **영업이익**: 43조 6,010억 원
- **영업이익률**: 13.07%

2024년(매출 300조 8,709억 원, 영업이익 32조 7,260억 원)과 비교하면 매출은 11.1% 증가, 영업이익은 33.1% 증가했습니다.

### 근거로 쓴 응답 발췌

```
"year":2025,"fs_div":"CFS","report":"사업보고서","revenue":333605938000000,"operating_income":43601051000000,"ratios":{"operating_margin_pct":13.07}
```

```
"year":2024,"fs_div":"CFS","report":"사업보고서","revenue":300870903000000,"operating_income":32725961000000,"ratios":{"operating_margin_pct":10.88}
```

```
"statement_basis":"CFS","statement_basis_note":"CFS=연결재무제표"
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"*"}` | 와일드카드 검색 결과 0건, rc=0 |

### 답변

죄송하지만, 이 MCP 서버의 도구로는 코스피 시가총액 상위 종목 목록을 직접 조회할 수 없습니다.

이 서버의 search_company 도구는 "회사명이나 6자리 ticker 코드로 특정 회사를 검색"하는 기능만 제공하며, 시가총액 기준 상위 종목 순위나 목록을 반환하는 도구가 없습니다. get_quote 도구로 개별 종목의 시가총액을 조회할 수는 있지만, 먼저 어떤 종목들을 조회할지 알아야 합니다.

### 근거로 �은 응답 발췌

```
search_company	필수=query	Searches Korean listed companies (KOSPI/KOSDAQ) by company name or 6-digit ticker code via Korea Stock MCP(한국주식 분석). Returns up to 20 matches
```

```
get_quote	필수=ticker	Retrieves the latest quote snapshot for a Korean stock — price, market cap, 52-week high/low, volume
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"삼성전자"}` | 삼성전자(005930) 검색됨, rc=0 |
| 2 | get_financials | `{"ticker":"005930"}` | 2021~2025년 재무제표 수신, rc=0 |

### 답변

삼성전자의 2025년 실적(가장 최신)은 다음과 같습니다.

**매출**: 333.6조 원 (2024년 300.9조 원 대비 10.9% 증가)
**영업이익**: 43.6조 원 (2024년 32.7조 원 대비 33.5% 증가)

영업이익률은 13.07%로 전년 10.88%보다 개선되었습니다. 당기순이익도 45.2조 원으로 2024년의 34.5조 원에서 31.4% 증가했습니다.

### 근거로 쓴 응답 발췌

```
{"year":2025,"fs_div":"CFS","report":"사업보고서","revenue":333605938000000,"operating_income":43601051000000,"net_income":45206805000000,"assets":566942110000000,"liabilities":130621773000000,"equity":436320337000000,"issued_capital":897514000000,"cfo":85315148000000,"cfi":-68512206000000,"interest_expense":11733764000000,"capex":47522179000000,"fcf":37792969000000,"ratios":{"operating_margin_pct":13.07,"net_margin_pct":13.55,"roe_pct":10.36,"debt_ratio_pct":29.94,"cfo_to_net_income":1.89,"capital_impairment":false}}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| — | — | — | 조회 불가 |

### 답변

죄송하지만 이 서버는 코스피 시가총액 상위 종목을 조회하는 도구를 제공하지 않습니다.

사용 가능한 도구들:
- **search_company**: 회사명이나 티커로 특정 회사를 검색
- **get_quote**: 특정 종목의 최신 시세 조회
- **get_financials**: 특정 회사의 재무제표 조회

시가총액 상위 종목을 알고 싶으시다면, 특정 회사명이나 티커를 알려주시면 그 회사의 시가총액과 시세 정보를 조회해드릴 수 있습니다.

### 근거로 쓴 응답 발췌

```
ping	필수=-	Health check for Korea Stock MCP(한국주식 분석 서버). Returns 'pong'.
search_company	필수=query	Searches Korean listed companies (KOSPI/KOSDAQ) by company name or 6-digit ticker code via Korea Stock MCP(한국주식 분석). Returns up to 20 matches with tic
get_quote	필수=ticker	Retrieves the latest quote snapshot for a Korean stock — price, market cap, 52-week high/low, volume — with a market-cap consistency check, via Korea 
get_financials	필수=ticker	Retrieves audited annual financial statements (revenue, operating income, net income, balance sheet, cash flows) and profitability/stability/growth ra
get_risk_flags	필수=ticker	Detects financial red flags for a Korean listed company — high debt ratio, low interest coverage, negative operating cash flow streaks, revenue declin
get_valuation	필수=ticker	Computes a conservative valuation for a Korean stock — PER/PBR multiples from filed EPS/BPS and a three-scenario (pessimistic/neutral/optimistic) valu
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"삼성전자"}` | 삼성전자 티커 005930 조회, rc=0 |
| 2 | get_financials | `{"ticker":"005930"}` | 2021~2025년 재무제표 조회, rc=0 |

### 답변

삼성전자의 2025년 최근 실적은 다음과 같습니다:
- **매출**: 333조 6,059억 원 (333,605,938,000,000 KRW)
- **영업이익**: 43조 6,010억 원 (43,601,051,000,000 KRW)
- **영업이익률**: 13.07%

최근 4년간 추이를 보면, 2023년 영업이익이 극저점(6.6조 원, 영업이익률 2.54%)에서 회복세를 보이고 있습니다. 2024년에는 32조 7,259억 원, 2025년에는 43조 6,010억 원으로 개선되어 정상화 과정에 있습니다. 2025년 순이익은 45조 2,068억 원이며, 영업현금흐름은 85조 3,151억 원으로 건실합니다.

### 근거로 쓴 응답 발췌

```
{"ticker":"005930","statement_basis":"CFS","statement_basis_note":"CFS=연결재무제표, OFS=별도재무제표","unit":"KRW","years":[...{"year":2025,"fs_div":"CFS","report":"사업보고서","revenue":333605938000000,"operating_income":43601051000000,"net_income":45206805000000,"assets":566942110000000,"liabilities":130621773000000,"equity":436320337000000,"issued_capital":897514000000,"cfo":85315148000000,"cfi":-68512206000000,"interest_expense":11733764000000,"capex":47522179000000,"fcf":37792969000000,"ratios":{"operating_margin_pct":13.07,"net_margin_pct":13.55,"roe_pct":10.36,"debt_ratio_pct":29.94,"cfo_to_net_income":1.89,"capital_impairment":false}}],"growth":{"span_years":4,"revenue_cagr_pct":4.51,"net_income_cagr_pct":3.17,"note":"CAGR은 실제 연도 간격 기준. 계산 불가(적자 전환 등)는 null."},"fcf_note":"FCF = 영업활동현금흐름 − 유형자산 취득(근사치). 무형자산·리스 투자 미포함.","data_source":"DART 전자공시 사업보고서 (fnlttSinglAcntAll)"}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"삼성"}` | 삼성 그룹 계열사 20개 기업 검색, rc=0 |
| 2 | search_company | `{"query":"SK하이닉스"}` | SK하이닉스 티커 000660 조회, rc=0 |
| 3 | search_company | `{"query":"NAVER"}` | NAVER 티커 035420 조회, rc=0 |
| 4 | get_quote | `{"ticker":"005930"}` | 삼성전자 현재 주가 조회, rc=0 |

### 답변

죄송하지만, 이 MCP 서버는 **코스피 전체 시가총액 상위 종목 순위를 직접 제공하는 도구가 없습니다.** 

서버는 개별 기업의 상세 정보를 제공하는 방식으로 설계되어 있습니다. 조회 결과:
- 삼성전자(005930): 주가 222,000원, 발행주식수 58억 4,627만 주 (시가총액 정보는 미제공)
- SK하이닉스(000660): 티커 확인됨
- NAVER(035420): 티커 확인됨

코스피 시가총액 상위 종목을 확인하려면 한국거래소(KRX) 공식 데이터나 다른 시장 데이터 서버를 참고하시기를 권장합니다. 이 서버의 도구 제약으로 인해 정확한 상위 순위를 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
{"query":"삼성","count":20,"matches":[{"ticker":"028050","name":"삼성E&A","market":"KOSPI","sector":NaN},{"ticker":"448730","name":"삼성FN리츠","market":"KOSPI","sector":NaN},{"ticker":"006400","name":"삼성SDI","market":"KOSPI","sector":NaN},...]}

{"query":"SK하이닉스","count":1,"matches":[{"ticker":"000660","name":"SK하이닉스","market":"KOSPI","sector":NaN}]}

{"query":"NAVER","count":1,"matches":[{"ticker":"035420","name":"NAVER","market":"KOSPI","sector":NaN}]}

{"ticker":"005930","name":"삼성전자","market":"KOSPI","price":222000.0,"as_of":"2026-11-03","market_cap":null,"shares_outstanding":5846278608.0,"high_52w":374500.0,"low_52w":94500.0,"volume":13389433.0,"data_source":"KRX via FinanceDataReader","market_cap_check":{"status":"unavailable","reason":"가격·주식수·보고 시가총액 중 결측값 존재"}}
```
