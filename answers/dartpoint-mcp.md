# dartpointai/dartpoint-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://dartpoint.ai/mcp-sse/mcp/`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_corp_name | `{"corp_name": "삼성전자"}` | 빈 응답, rc=0 |
| 2 | get_corp_code | `{"corp_name": "삼성전자"}` | 빈 응답, rc=0 |
| 3 | get_corp_code | `{"corp_name": "Samsung"}` | 빈 응답, rc=0 |

### 답변

죄송하지만, dartpoint-mcp 서버에서 삼성전자의 실적 정보를 가져올 수 없습니다. 

기업명으로 기업 코드를 조회하는 도구(get_corp_name, get_corp_code)들이 응답을 반환하지 않았으므로, 재무 정보 조회까지 진행할 수 없었습니다. 이 서버는 DART 기반 기업 정보를 제공하려고 하지만, 현재 기업 검색 기능이 작동하지 않거나 데이터를 반환하지 않고 있습니다.

### 근거로 쓴 응답 발췌

```
{"content": [], "isError": false}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

이 질문에 대한 답을 얻기 위한 도구 호출이 없습니다.

### 답변

dartpoint-mcp 서버는 코스피 시가총액 상위 종목을 조회할 수 있는 도구를 제공하지 않습니다. 

이 서버의 도구 목록을 검토한 결과, 모두 특정 기업의 코드를 알아야 정보를 조회할 수 있는 구조입니다. 코스피 지수, 시장 지표, 또는 전체 상장사 순위 같은 시장 전체 정보를 반환하는 도구가 없으므로, 코스피 상위 종목 정보를 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
도구 목록에 포함된 기능:
- 기업별 재무 정보: get_financial_summary_by_date, get_financial_info_by_date_compact
- 기업별 주가 이력: get_stock_history, get_stock_history_compact
- 기업별 뉴스/감성 분석: get_news_sentiments, get_monthly_news_forum_sentiments

시장 전체 정보 조회 도구: 없음
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_corp_name | `{"corp_name":"삼성전자"}` | 빈 응답 (기업 검색 결과 없음), rc=0 |
| 2 | get_corp_code | `{"corp_name":"삼성전자"}` | 빈 응답 (기업 검색 결과 없음), rc=0 |
| 3 | get_corp_code | `{"corp_name":"Samsung Electronics"}` | 빈 응답 (기업 검색 결과 없음), rc=0 |

### 답변

이 MCP 서버는 삼성전자의 재무정보를 조회하지 못했습니다.

dartpoint-mcp 서버의 get_corp_code, get_corp_name 도구를 사용하여 "삼성전자", "Samsung Electronics" 등으로 기업을 검색했지만, 도구가 기업 코드를 반환하지 않았습니다. 기업 코드 없이는 재무 상세정보(매출, 영업이익 등)를 조회할 수 없습니다.

**제한 사항**: 이 서버의 도구로 요청하신 기업 정보를 조회할 수 없습니다(도구: 기업명 검색 실패, 범위: DART 등재 기업).

### 근거로 쓴 응답 발췌

```
호출 1 응답: {"content": [], "isError": false}
호출 2 응답: {"content": [], "isError": false}
호출 3 응답: {"content": [], "isError": false}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | (도구 목록 조회) | KOSPI, 시가총액, 순위 검색 | 관련 도구 없음 |

### 답변

이 MCP 서버는 코스피 시가총액 상위 종목 정보를 제공하는 도구가 없습니다.

dartpoint-mcp의 도구 목록을 확인한 결과, 이 서버는 특정 기업의 코드를 알고 있을 때 그 기업의 상세 정보(사업 개요, 재무제표, 임원, 배당, 주가 이력 등)를 조회하는 데 특화되어 있습니다. 시장 전체 순위, 코스피 구성 종목 목록, 시가총액 순위 조회 등의 도구는 제공되지 않습니다.

**제한 사항**: 요청하신 정보를 제공할 도구가 없습니다(범위: 개별 기업 정보 조회만 지원).

### 근거로 쓴 응답 발췌

```
dartpoint-mcp 도구 43개: get_corp_code, get_corp_name, get_corp_info, get_corp_products_info, 
get_corp_bsns_summary, get_dividends, get_executive_status, get_shareholders, 
get_employees, get_competitors, get_industry_growth, get_stock_history, 
get_news_sentiments, get_stock_bbs_sentiments, get_monthly_news_forum_sentiments, 
get_financial_summary_by_date, get_main_reports, get_etc_reports, get_financial_info_by_date, 
get_financial_health, get_affiliate, get_subsidiaries, get_finance_forecasts, 
get_related_corporations, get_financial_info_by_date_compact, get_stock_history_compact, 
get_etc_reports_compact, get_main_reports_compact, get_related_corporations_compact, 
get_dividends_compact, get_affiliate_compact, get_monthly_news_forum_sentiments_compact, 
get_executive_status_compact, get_finance_forecasts_compact, get_shareholders_compact, 
get_industry_growth_compact, get_financial_health_compact
(중: 시가총액 순위/코스피 상위 종목 조회 도구 없음)
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_corp_name | `{"corp_name": "삼성전자"}` | 빈 배열, rc=0 |
| 2 | get_corp_name | `{"corp_name": "삼성"}` | 빈 배열, rc=0 |
| 3 | get_financial_summary_by_date | `{"corp_code": "005930", "start_ref_dt": "2026-01-01", "end_ref_dt": "2026-12-31"}` | 빈 배열, rc=0 |

### 답변

죄송하지만 dartpoint-mcp 서버에서 삼성전자의 실적 정보를 조회할 수 없었습니다. 

**이유:**
- 기업명 조회 도구(`get_corp_name`)가 "삼성전자", "삼성" 등의 검색어로 기업 코드를 반환하지 못했습니다.
- 코드를 직접 입력하여 재무정보 조회를 시도했으나 데이터가 반환되지 않았습니다.
- 서버가 현재 요청된 정보를 제공하지 못하는 상태입니다.

### 근거로 쓴 응답 발췌

```
질문 1 도구 호출 결과:
{"content": [], "isError": false}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | (적절한 도구 없음) | - | 코스피 시가총액 상위 종목을 조회하는 도구가 서버에 없음 |

### 답변

dartpoint-mcp 서버에서 코스피 시가총액 상위 종목을 조회할 수 없습니다.

**이유:**
- 서버의 도구 목록을 확인한 결과, 코스피 인덱스 구성 종목이나 시가총액 상위 종목을 직접 조회하는 도구가 없습니다.
- 이 서버는 특정 기업의 기업 코드를 알고 있을 때, 그 기업의 재무정보·주가·뉴스 감성 등을 조회하는 데 특화되어 있습니다.
- 코스피 전체 리스트나 시가총액 순위 조회 기능은 제공하지 않습니다.

### 근거로 쓴 응답 발췌

```
dartpoint-mcp 서버 도구 목록에 포함된 주요 도구:
- 기업 정보: get_corp_info, get_corp_products_info
- 재무 정보: get_financial_summary_by_date, get_financial_info_by_date
- 주가/뉴스: get_stock_history, get_news_sentiments, get_stock_bbs_sentiments
- 임원/주주: get_executive_status, get_shareholders

코스피 전체 조회 또는 시가총액 상위 조회 도구는 목록에 없음.
```

---

완료 dartpoint-mcp r3
