# io.github.ChloePark85/kr-groundtruth

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://kr-groundtruth-mcp.vercel.app/api/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law | `{"query": "인구통계"}` | API 인증 필수, UNAUTHORIZED 오류, rc=1 |

### 답변

죄송하지만 이 질문에 답변할 수 없습니다.

**이유**: kr-groundtruth MCP 서버는 모든 도구 호출에 API 키 인증을 요구합니다. 규칙상 curl·웹검색·웹 요청이 금지되어 있어 API 키를 획득할 수 없습니다.

**서버 상태**: 
- 호출 오류: `{"code":"UNAUTHORIZED","message":"This tool needs an API key. Get one free (200 credits) then reconnect with Authorization: Bearer kgt_live_..."}`
- 종료코드: rc=1 (서버 응답은 받았으나 도구 실행 불가)

### 근거로 쓴 응답 발췌

```
{"ok":false,"error":{"code":"UNAUTHORIZED","message":"This tool needs an API key. Get one free (200 credits) then reconnect with Authorization: Bearer kgt_live_... (or x-api-key).","get_key":"curl -X POST https://kr-groundtruth-mcp.vercel.app/v1/accounts -H 'content-type: application/json' -d '{\"email\":\"you@example.com\"}'","docs":"https://kr-groundtruth-mcp.vercel.app/llms.txt"}}
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law | `{"query": "대기환경 공공데이터"}` | API 인증 필수, UNAUTHORIZED 오류, rc=1 |

### 답변

죄송하지만 이 질문에도 답변할 수 없습니다.

**이유**: 위 질문과 동일합니다. kr-groundtruth MCP 서버의 모든 도구가 API 인증을 요구하므로, 규칙상 진행 불가능합니다.

**서버 특성**: 
- 이 MCP 서버는 API 키 기반 인증 시스템을 사용하며, 규칙 3에서 금지된 curl/웹 요청을 통해서만 인증을 진행할 수 있습니다.
- 따라서 이 평가 회차에서는 인증 장벽으로 인해 도구를 활용할 수 없습니다.

### 근거로 쓴 응답 발췌

```
{"ok":false,"error":{"code":"UNAUTHORIZED","message":"This tool needs an API key. Get one free (200 credits) then reconnect with Authorization: Bearer kgt_live_... (or x-api-key)."}}
```

---

## 평가 회차 요약

- **회차**: 1
- **MCP 서버**: kr-groundtruth (https://kr-groundtruth-mcp.vercel.app/api/mcp)
- **질문 처리**: 2건 모두 미완료
- **실패 원인**: 서버 측 API 인증 요구, 규칙상 인증 불가
- **도구 호출 횟수**: 2회 (모두 rc=1 UNAUTHORIZED)

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | (도구 없음) | - | 이 MCP 서버에 인구 통계 도구 없음 |

### 답변

이 MCP 서버는 인구 통계 데이터를 제공하는 도구를 가지고 있지 않습니다. 

서버의 도구 목록을 확인한 결과, 제공하는 도구는 다음과 같습니다:
- verify_business_registration (사업자등록 상태 조회)
- search_address (주소 검색)
- search_corporation (법인 검색)
- lookup_corporation (법인 상세 정보)
- apartment_trade_prices (아파트 실거래가)
- search_law (법령 검색)

서울시의 인구 변화 추이는 통계청(KOSTAT) 공식 인구동향조사나 서울시청 통계데이터센터 등에서 제공하는 정보로 조회해야 합니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
verify_business_registration	필수=business_numbers	국세청 사업자등록번호 상태
search_address	필수=keyword	도로명주소·지번주소·건물명 키워드
search_corporation	필수=name	금융감독원 DART 등록 법인 검색
lookup_corporation	필수=corp_code	DART corp_code로 기업개황 조회
apartment_trade_prices	필수=lawd_code,deal_month	국토교통부 아파트 매매 실거래가
search_law	필수=query	법제처 국가법령정보센터 법령 검색
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law | `{"query":"환경 대기질 공공데이터"}` | 인증 필요 (API 키 필요), rc=1 |

### 답변

이 MCP 서버는 공공데이터포털 정보를 직접 조회하는 도구를 제공하지 않습니다.

서버의 도구로는 법령 검색(search_law)이 가능하지만, 도구를 사용하려면 API 키를 통한 인증이 필요하며, 도구는 법제처 국가법령정보센터의 법령 검색만 가능합니다.

공공데이터포털(data.go.kr)의 대기질 데이터는 다음 방법으로 조회할 수 있습니다:
1. 공공데이터포털 웹사이트에서 "대기질"로 검색
2. 환경부가 제공하는 대기환경 데이터 API 직접 이용
3. 에어코리아(www.airkorea.or.kr) 정부 공식 대기질 서비스 이용

### 근거로 쓴 응답 발췌

```
도구 호출 오류 응답:
{"ok":false,"error":{"code":"UNAUTHORIZED","message":"This tool needs an API key. Get one free (200 credits) then reconnect with Authorization: Bearer kgt_live_..."}}

search_law 도구 설명:
법제처 국가법령정보센터에서 현행 법령(법률·시행령·시행규칙)을 검색합니다.
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

없음

### 답변

이 서버의 도구로는 답할 수 없습니다.

**이유**: kr-groundtruth MCP 서버는 다음 7개 도구만 제공합니다:
- verify_business_registration (사업자등록번호 상태)
- search_address (주소 검색)
- search_corporation (법인명 검색)
- lookup_corporation (기업개황)
- apartment_trade_prices (아파트 실거래가)
- search_law (법령 검색)
- get_balance·get_pricing (API 관리)

이 중 인구통계나 지역별 인구 추이를 제공하는 도구가 없습니다.

### 근거로 쓴 응답 발췌

```
(도구 호출 없음)
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

없음

### 답변

이 서버의 도구로는 답할 수 없습니다.

**이유**: kr-groundtruth MCP 서버의 도구 중 공공데이터포털(data.go.kr) 메타정보 조회·데이터셋 검색·API 위치 안내 기능이 없습니다. 제공되는 도구는 사업자번호, 주소, 법인, 아파트 가격, 법령 조회만 가능합니다.

### 근거로 쓴 응답 발췌

```
(도구 호출 없음)
```
