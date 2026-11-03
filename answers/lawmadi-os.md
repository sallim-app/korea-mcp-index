# io.github.peter120525-cmd/lawmadi-os

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://lawmadi.com/mcp`.


---

# 1회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query":"국가계약법상 수의계약을 할 수 있는 경우와 근거 조문"}` | 인증 필요(HTTP 401), rc=1 |
| 2 | search | `{"q":"국가계약법"}` | 인증 필요(HTTP 401), rc=1 |
| 3 | lookup_statute | `{"reference":"국가계약법 제50조"}` | 봇 거부(anon_preview_automated), rc=1 |

### 답변

lawmadi.com/mcp 서버의 도구들은 대부분 API 키 인증이 필요합니다. 인증 없이 호출 가능한 유일한 도구는 `get_pricing`(가격 정보)이며, 조문 조회 도구인 `lookup_statute`는 자동화된 봇의 호출을 거부합니다.

**서버가 못 준 이유:**
- `ask` 도구: 인증 필수 (2 credits 소비)
- `search` 도구: 인증 필수 (키 필요)
- `lookup_statute` 도구: 자동화된 봇으로 인식되어 거부 (preview depth 미리보기도 불가)

따라서 도구 출력에서 국가계약법상 수의계약 경우와 근거 조문을 얻을 수 없습니다.

### 근거로 쓴 응답 발췌

```
Authentication required for `ask`. Usable right now without any key: 
get_pricing (full) and lookup_precedent, lookup_statute (preview depth, 1/day). 
Call `get_pricing` (no auth needed) for the sign-up and pricing steps, 
then retry with `Authorization: Bearer <API key>`.

No-key previews are not served to self-declared automated checkers 
(bot/monitor/audit user agents). `initialize`, `tools/list` and `get_pricing` 
stay open. Issue a free API key for results.
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query":"도로교통법 음주운전 처벌 기준"}` | 인증 필요(HTTP 401), rc=1 |

### 답변

lawmadi.com/mcp 서버의 도구들을 통해 도로교통법의 음주운전 처벌 기준을 조회할 수 없습니다.

**서버가 못 준 이유:**
- 질문에 적합한 도구인 `ask`·`search`·`lookup_statute` 모두 인증이 필요하며, 자동화된 봇의 호출이 거부됩니다.

따라서 도구 출력에서 음주운전 처벌 기준을 얻을 수 없습니다.

### 근거로 쓴 응답 발췌

```
Authentication required for `ask`. 
Call `get_pricing` (no auth needed) for the sign-up and pricing steps, 
then retry with `Authorization: Bearer <API key>`.

Sign in: https://lawmadi.com · 
API key: https://lawmadi.com/mcp-key-guide-en · 
Pricing: https://lawmadi.com/pricing-en
```

---

# 2회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query": "국가계약법상 수의계약을 할 수 있는 경우"}` | API 키 필수, rc=3 |
| 2 | search | `{"q": "국가계약법"}` | API 키 필수, rc=3 |
| 3 | get_pricing | `{}` | 도구 정보 획득, rc=0 |

### 답변

죄송하지만 이 MCP 서버로는 두 질문 모두 답할 수 없습니다.

**이유:**
1. 법률 질문에 답하는 주요 도구(`ask`, `search`)는 **API 키가 필수**입니다
2. 키 없이 사용 가능한 도구(`lookup_statute`, `lookup_precedent`)는 조문 번호나 사건번호를 미리 알아야 사용 가능합니다
3. 조문 번호를 먼저 찾아주는 검색 도구도 모두 API 키를 요구합니다

지시서 규칙에 따라 웹검색이나 다른 정보원을 사용할 수 없으므로, 이 서버는 인증 없이 두 질문에 대해 답변을 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
"ask": {
  "auth": "key",
  "credits": 2,
  "resets": "00:00 KST"
},
"search": {
  "auth": "key",
  "credits": 0,
  "daily_cap": 60,
  "cap_raised_by_buying_credits": false,
  "resets": "00:00 KST"
},
"lookup_statute": {
  "auth": "preview",
  "credits": 0,
  "free_per_day": 30,
  "then_credits_per_calls": [1, 10],
  "daily_ceiling": 300,
  "allowance_bucket": "lookup",
  "no_key_per_day": 1,
  "no_key_scope": "per caller (IP+User-Agent)",
  "resets": "00:00 KST"
},
"preview_withholds": "full holding / summary / referenced articles / statute body — those need a key (free to issue)",
"Notes": "Anonymous queries are not allowed; discovery (initialize/tools/list) is public."
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query": "도로교통법 음주운전 처벌 기준"}` | API 키 필수, rc=3 |

### 답변

마찬가지로 이 서버로는 답할 수 없습니다.

도로교통법상 음주운전 처벌 기준은 자주 개정되는 내용이므로, 이를 정확하게 답하려면:
- 최신 법령을 조회할 수 있는 `search` 도구: **API 키 필수**
- 또는 법률 분석 도구 `ask`/`ask_expert`: **API 키 필수**

키가 없으면 이 서버는 어떤 답변도 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
"ask": {
  "auth": "key",
  "credits": 2
},
"ask_expert": {
  "auth": "key",
  "credits": 3,
  "requires_plan": "pro"
},
"error": "Authentication required for `ask`. Usable right now without any key: get_pricing (full) and lookup_precedent, lookup_statute (preview depth, 1/day). Call `get_pricing` (no auth needed) for the sign-up and pricing steps, then retry with `Authorization: Bearer <API key>`."
```

---

# 3회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query":"국가계약법상 수의계약을 할 수 있는 경우"}` | 인증 필요, rc=1 |
| 2 | lookup_statute | `{"reference":"국가계약법 제50조"}` | 자동 체커로 거부, rc=3 |

### 답변

죄송하지만 이 서버의 도구로 답변을 드릴 수 없습니다.

이 MCP 서버는 유료 인증(API 키 + 크레딧)이 필요합니다. 주요 도구인 `ask`는 인증 없이 호출 불가능(Authentication required)하고, 무료 미리보기를 제공하는 `lookup_statute`는 자동화된 호출자(bot)로 인식되어 접근이 거부됩니다.

현재 사용 가능한 제한 없는 도구는 `get_pricing`뿐이며, 이는 가격 정보만 제공합니다. 

**서버가 제공하지 않으므로**, 이 질문에 대한 도구 기반 답변을 드릴 수 없습니다.

### 근거로 쓴 응답 발췌

```
HTTP 401: "Authentication required for `ask`. Usable right now without any key: get_pricing (full) and lookup_precedent, lookup_statute (preview depth, 1/day)."

"No-key previews are not served to self-declared automated checkers (bot/monitor/audit user agents). `initialize`, `tools/list` and `get_pricing` stay open."
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask | `{"query":"도로교통법 음주운전 처벌 기준"}` | 인증 필요, rc=1 |
| 2 | lookup_statute | `{"reference":"도로교통법 제44조"}` | 자동 체커로 거부, rc=3 |

### 답변

이 질문도 동일한 이유로 서버의 도구로 답변할 수 없습니다.

**도구 호출 불가 사유:**
- 주 도구 `ask` (2 credits 필요): 유료 인증 필수
- 보조 도구 `lookup_statute` (무료 preview): 자동 호출자 차단

서버의 제약으로 인해 도로교통법의 음주운전 처벌 기준에 관한 현황 정보를 제공하지 못합니다.

### 근거로 쓴 응답 발췌

```
HTTP 401: "Authentication required for `ask`. Usable right now without any key..."

HTTP 403 (preview denied): "No-key previews are not served to self-declared automated checkers"
```
