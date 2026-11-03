# io.github.pipeworx-io/kr-law

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/kr-law/mcp`.


---

# 1회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"국가계약법 수의계약","_apiKey":"test"}` | 검색 결과 0건, rc=0 |
| 2 | kr_law_search | `{"query":"국가계약법","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

미안합니다. 이 MCP 서버의 한국법령 도구(kr_law_search)는 데모 키(test)로는 국가계약법에 대한 정보를 제공하지 못했습니다. 

도구가 반환한 empty_reason은 "no_match"였고, 검색 결과는 0건이었습니다. 

정확한 답변을 제공하려면 한국법령정보센터(law.go.kr)의 정식 Open API 키가 필요합니다. 이는 https://open.law.go.kr/LSO/main.do 에서 한국 본인확인(모바일·i-PIN)을 거쳐 신청할 수 있습니다.

### 근거로 쓴 응답 발췌

```json
{
  "query":"국가계약법",
  "total_count":0,
  "page":1,
  "display":20,
  "has_more":false,
  "results":[],
  "note":"mst identifies one specific version — pass it to kr_law_article / kr_law_history. \"status\":\"현행\" = currently in force, \"연혁\" = a past, superseded version.",
  "source":"Ministry of Government Legislation (법제처), National Law Information Center Open API",
  "data_as_of":"2026-11-03",
  "empty_reason":"no_match"
}
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"도로교통법 음주운전","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

미안합니다. 이 MCP 서버의 한국법령 도구(kr_law_search)는 데모 키(test)로는 도로교통법의 음주운전 처벌 기준에 대한 정보를 제공하지 못했습니다.

도구가 반환한 empty_reason은 "no_match"였고, 검색 결과는 0건이었습니다.

정확한 처벌 기준을 알아보려면 한국법령정보센터(law.go.kr)의 정식 Open API 키가 필요합니다. 이는 https://open.law.go.kr/LSO/main.do 에서 한국 본인확인(모바일·i-PIN)을 거쳐 신청할 수 있습니다.

### 근거로 쓴 응답 발췌

```json
{
  "query":"도로교통법 음주운전",
  "total_count":0,
  "page":1,
  "display":20,
  "has_more":false,
  "results":[],
  "note":"mst identifies one specific version — pass it to kr_law_article / kr_law_history. \"status\":\"현행\" = currently in force, \"연혁\" = a past, superseded version.",
  "source":"Ministry of Government Legislation (법제처), National Law Information Center Open API",
  "data_as_of":"2026-11-03",
  "empty_reason":"no_match"
}
```

---

# 2회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"국가계약법 수의계약","_apiKey":"test"}` | 검색 결과 0건, rc=0 |
| 2 | kr_law_search | `{"query":"국가계약법","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

죄송하지만 이 서버의 kr_law_search 도구가 한글 검색 쿼리에 반응하지 않아 국가계약법 정보를 가져올 수 없었습니다. 도구를 2회 호출했으나 모두 0건의 결과를 반환했습니다. 또한 무료 API 할당량(50회/일)이 이미 소진되어 추가 시도가 불가능합니다.

### 근거로 쓴 응답 발췌

```
{"query":"국가계약법 수의계약","total_count":0,"page":1,"display":20,"has_more":false,"results":[],"empty_reason":"no_match"}
{"query":"국가계약법","total_count":0,"page":1,"display":20,"has_more":false,"results":[],"empty_reason":"no_match"}
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"도로교통법","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

이 서버의 kr_law_search 도구가 한글 검색에 반응하지 않아 도로교통법 정보를 가져올 수 없었습니다. 무료 API 할당량이 완전히 소진되어(50/50) 추가 시도가 불가능합니다.

### 근거로 쓴 응답 발췌

```
{"query":"도로교통법","total_count":0,"page":1,"display":20,"has_more":false,"results":[],"empty_reason":"no_match","signup_hint":"You've used 50/50 of the free anonymous quota today"}
```

---

# 3회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"국가계약법 수의계약","_apiKey":"test"}` | 검색 결과 0건, rc=0 |
| 2 | kr_law_search | `{"query":"국가계약법","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

죄송합니다. 이 MCP 서버의 한국 법령 검색 도구(`kr_law_search`)가 데이터를 제공하지 못했습니다. 

**원인**: 서버가 요구하는 한국 법제처 OPEN API 키(유료 또는 실명인증 필요)가 없어서, 무료 데모 키("test")로만 호출했는데, 이 데모 키는 검색 쿼리에 응답하지 않습니다. 서버의 응답 메시지에서 보면 유효한 API 키를 발급받아야만 조회가 가능합니다.

국가계약법상 수의계약 대상과 근거 조문은 **이 서버의 도구로는 제공할 수 없습니다**.

### 근거로 쓴 응답 발췌

```
{"query":"국가계약법","total_count":0,"page":1,"display":20,"has_more":false,"results":[],"empty_reason":"no_match"}

{"error":"tool_error","message":"Korea Law kr_law_search requires an API key. Pass it via _apiKey — your own OC (Open API user id) from https://open.law.go.kr/LSO/main.do"}
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kr_law_search | `{"query":"도로교통법 음주운전","_apiKey":"test"}` | 검색 결과 0건, rc=0 |

### 답변

역시 같은 이유로 도구가 데이터를 제공하지 못했습니다. 도로교통법의 음주운전 처벌 기준(현행 기준)은 **이 서버의 도구로는 조회할 수 없습니다**.

### 근거로 쓴 응답 발췌

```
{"query":"도로교통법 음주운전","total_count":0,"page":1,"display":20,"has_more":false,"results":[],"empty_reason":"no_match"}
```
