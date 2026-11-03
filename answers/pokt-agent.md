# io.github.jsymen1290/pokt-agent

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://mcp.pokt-agent.com/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | dart_events | `{"question":"삼성전자 최근 실적 매출 영업이익"}` | 삼성전자 최근 공시 85건 조회, 반기보고서·연결재무제표기준영업 잠정실적 공시 목록 반환, rc=0 |

### 답변

죄송하지만 이 서버의 도구로는 삼성전자의 구체적인 매출과 영업이익 수치를 드릴 수 없습니다. 

DART 공시 시스템을 조회한 결과, 삼성전자의 최근 주요 공시는 다음과 같습니다:
- **2026년 2분기 반기보고서** (2026-08-14 공시)
- **2026년 3분기 잠정 실적** (2026-10-29 공시, 최신)

이 도구는 공시 문서의 존재와 링크만 제공하며, 실제 매출·영업이익 수치는 DART 웹사이트에서 해당 공시 문서를 직접 열어야 확인할 수 있습니다.

### 근거로 쓴 응답 발췌

```
"filings": [
  {"rcept_no": "20260814003699", "rcept_dt": "20260814", "report_nm": "반기보고서 (2026.06)", ...},
  {"rcept_no": "20261008800004", "rcept_dt": "20261008", "report_nm": "연결재무제표기준영업(잠정)실적(공정공시)", ...},
  {"rcept_no": "20261029800087", "rcept_dt": "20261029", "report_nm": "연결재무제표기준영업(잠정)실적(공정공시)", ...}
]
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| (도구 없음) | - | - | 코스피 상위 종목을 조회하는 도구가 이 MCP 서버에 없음, rc=3 |

### 답변

죄송하지만 이 서버는 코스피 시가총액 상위 종목을 조회할 수 있는 도구를 제공하지 않습니다.

이 MCP 서버(`https://mcp.pokt-agent.com/mcp`)의 도구들은 주로 한국의 세부 금융 데이터(DART 공시, 환율, 금리, 아파트 실거래, 수출통계 등)에 특화되어 있으며, 코스피 지수나 시가총액 순위 정보는 범위 밖입니다. 이 정보는 다른 금융 데이터 서버에서 조회해야 합니다.

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | dart_events | `{"question":"삼성전자 최근 실적 매출 영업이익"}` | 공시 목록 85건 반환, 반기보고서(2026.06) 및 임시공시 포함, rc=0 |
| 2 | pocket_catalog | `{"query":"한국 상장사 재무실적 매출 영업이익"}` | 해당 서비스 0건, rc=0 |

### 답변

죄송하지만, 이 서버에는 삼성전자의 구체적인 매출과 영업이익 수치를 직접 조회할 수 있는 도구가 없습니다.

dart_events 도구로 삼성전자의 DART 공시 목록은 확인할 수 있었습니다(8월 반기보고서, 10월 임시공시 등). 다만 이 도구는 공시 제목과 링크만 제공할 뿐, 보고서 안의 구체적인 재무 수치(매출액, 영업이익)를 추출할 수 없습니다.

포켓 네트워크의 카탈로그에도 한국 상장사 재무정보를 조회할 수 있는 서비스가 없었습니다.

### 근거로 쓴 응답 발췌

```
{"rcept_no": "20260814003699", "rcept_dt": "20260814", "report_nm": "반기보고서 (2026.06)", "base_name": "반기보고서 (2026.06)", "kind": "ORIGINAL"},
{"rcept_no": "20261008800004", "rcept_dt": "20261008", "report_nm": "연결재무제표기준영업(잠정)실적(공정공시)", "base_name": "연결재무제표기준영업(잠정)실적(공정공시)"}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

이 질문에 답하기 위해 도구 목록을 검토했지만, 코스피 시가총액 상위 종목을 조회할 수 있는 도구를 찾을 수 없었습니다.

### 답변

죄송하지만, 이 서버에는 코스피 시가총액 상위 종목 정보를 조회할 수 있는 도구가 없습니다.

포kt-agent 서버의 도구들은 주로 다음을 제공합니다:
- TradingView Pine Script 검증 (pine_integrity, pine_lint)
- 백테스트 정리 (backtest_reconcile)
- 한국 금리·환율 (kr_rates, kr_fx)
- DART 공시 목록 (dart_events)
- 아파트 실거래 (kr_apartment_trades)
- 수출 통계 (kr_export_pulse)

코스피 상장 종목의 시가총액 순위나 현재 주가 정보를 직접 조회할 수 있는 도구는 없습니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
- pine_integrity, pine_lint, backtest_reconcile
- kr_figure_check, dart_correction_impact, kr_rates, kr_fx, kr_law_article
- kr_apartment_trades, dart_events, kr_export_pulse, pocket_catalog
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | dart_events | `{"question":"삼성전자 최근 분기 실적 매출 영업이익"}` | 2026년 8월~11월 공시 목록 85건 조회, rc=0 |
| 2 | dart_events | `{"question":"삼성전자 2026년 3분기 분기별 실적 매출액 영업이익"}` | 같은 기간 공시 목록 재조회, rc=0 |

### 답변

죄송합니다. 이 MCP 서버는 삼성전자의 **최근 실적 숫자(매출과 영업이익)를 직접 제공하지 않습니다.**

dart_events 도구는 한국 상장사의 공시 메타데이터(공시 제목, 공시일자, 공시 링크 등)만 반환합니다. 실제 매출액과 영업이익 같은 재무 수치는 포함되지 않습니다.

다만 삼성전자가 최근 공시한 **3분기(잠정)실적 공시는 있습니다**:
- 2026년 10월 8일 "연결재무제표기준영업(잠정)실적(공정공시)"
- 2026년 10월 29일 "연결재무제표기준영업(잠정)실적(공정공시)" (정정보고 포함)

이 공시에 매출과 영업이익이 담겨 있을 것으로 예상되지만, 도구가 그 문서 내용까지는 추출하지 않습니다.

### 근거로 쓴 응답 발췌

```
"rcept_no": "20261008800004",
"rcept_dt": "20261008",
"report_nm": "연결재무제표기준영업(잠정)실적(공정공시)",
"base_name": "연결재무제표기준영업(잠정)실적(공정공시)",
"kind": "ORIGINAL",

"rcept_no": "20261029800087",
"rcept_dt": "20261029",
"report_nm": "연결재무제표기준영업(잠정)실적(공정공시)",
"base_name": "연결재무제표기준영업(잠정)실적(공정공시)",
"kind": "ORIGINAL",

"rcept_no": "20261029800099",
"rcept_dt": "20261029",
"report_nm": "[기재정정]연결재무제표기준영업(잠정)실적(공정공시)",
"kind": "CORRECTION",
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pocket_catalog | `{"query":"주식 시가총액 코스피"}` | 재무 카테고리 서비스 3건 반환(DART 관련), rc=0 |
| 2 | pocket_catalog | `{"query":"finance stock market"}` | 23개 서비스 중 처음 10개 반환, 주식시장 정보 없음, rc=0 |

### 답변

죄송합니다. 이 MCP 서버에는 **코스피 시가총액 상위 종목에 대한 도구가 없습니다.**

포켓 네트워크의 Pocket Agent MCP 서버가 제공하는 금융 도구들은 주로 다음을 다룹니다:
- 한국 DART 공시 (dart_events, dart_correction_impact)
- 한국 아파트 실거래 (kr_apartment_trades)
- 한국 수출 통계 (kr_export_pulse)
- 한국 금리·환율 (kr_rates, kr_fx)
- 재무 텍스트 숫자 검증 (kr_figure_check)

코스피 지수, 상장사의 현재 시가총액, 종목별 시장 점유율 등의 실시간 주식 시장 데이터는 이 서버의 제공 범위에 포함되지 않습니다.

### 근거로 쓴 응답 발췌

```
{"count": 3, "returned": 3, "services": [
{"serviceId": "dart-correction-impact-v1", "displayName": "DART Correction Impact", "category": "finance"},
{"serviceId": "dart-kr-events-v1", "displayName": "DART KR Events", "category": "finance"},
{"serviceId": "kr-figure-check-v1", "displayName": "KR Figure Check", "category": "finance"}
]}

{"count": 23, "returned": 10, "services": [
{"serviceId": "backtest-reconcile-v1", "displayName": "Backtest Reconcile", "category": "finance"},
{"serviceId": "dart-correction-impact-v1", "displayName": "DART Correction Impact", "category": "finance"},
{"serviceId": "kr-apt-trades-v1", "displayName": "KR Apartment Trades", "category": "finance"},
{"serviceId": "kr-export-pulse-v1", "displayName": "KR Export Pulse", "category": "finance"},
{"serviceId": "kr-rates-fx-v1", "displayName": "Korean Rates and FX", "category": "finance"}
]}
```
