# com.theprotoclinical/commerce

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://www.theprotoclinical.com/api/ucp/mcp`.


---

# 1회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_business | `{"meta": {}, "ask": "요즘 많이 팔리는 상품이 뭐야?"}` | UCP discovery 오류, rc=3 |
| 2 | search_catalog | `{"meta": {}, "catalog": "best seller"}` | UCP discovery 오류, rc=3 |

### 답변

이 MCP 서버에서 제품 정보를 불러올 수 없습니다. 

서버가 응답할 때마다 "UCP discovery failed" 오류가 발생합니다. 이는 프로필 설정이 누락되었음을 의미하며, 서버 자체의 문제로 보입니다. 따라서 인기 상품 정보를 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
HTTP 422 오류 응답:
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32001,
    "message": "UCP discovery failed",
    "data": {
      "code": "invalid_profile_url",
      "content": "Unable to fetch agent profile: Missing profile uri"
    }
  }
}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_business | `{"meta": {}, "ask": "이 서비스로 예약할 수 있는 게 뭐가 있어?"}` | UCP discovery 오류, rc=3 |

### 답변

이 MCP 서버가 제공 가능한 예약 서비스를 파악할 수 없습니다.

서버가 작동하지 않아 도구를 통해 정보를 얻을 수 없습니다. 도구 목록에는 장바구니, 결제, 주문 관련 기능이 있으나, 구체적인 예약 가능 항목은 서버 오류로 인해 확인할 수 없습니다.

### 근거로 쓴 응답 발췌

```
사용 가능한 도구(서버 오류로 호출 불가):
- create_checkout
- update_checkout  
- complete_checkout
- create_cart
- update_cart
- search_catalog
- get_product
- ask_business

그러나 모든 호출에서 HTTP 422 / UCP discovery failed 오류 발생
```

---

# 2회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_catalog | `{"meta":{},"catalog":"best sellers"}` | UCP discovery failed · Missing profile uri, rc=3 |

### 답변

죄송합니다. 이 MCP 서버에 접근할 수 없습니다. 서버가 특별한 프로필 인증을 요구하는데, 필요한 인증 정보가 없어서 도구 호출에 실패했습니다. 

오류: `UCP discovery failed - Missing profile uri`
계속 URL: https://yxcs11-ry.myshopify.com/

### 근거로 쓴 응답 발췌

```
{"error": "tools/call 실패: HTTP 422", "body": "{\"jsonrpc\":\"2.0\",\"id\":2,\"error\":{\"code\":-32001,\"message\":\"UCP discovery failed\",\"data\":{\"code\":\"invalid_profile_url\",\"content\":\"Unable to fetch agent profile: Missing profile uri\",\"continue_url\":\"https://yxcs11-ry.myshopify.com/\"}}"}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_business | `{"meta":{"profile_uri":"https://yxcs11-ry.myshopify.com/"},"ask":"이 서비스로 예약할 수 있는 게 뭐가 있어?"}` | UCP discovery failed · Missing profile uri, rc=3 |

### 답변

죄송합니다. 이 MCP 서버에 접근할 수 없습니다. 도구 호출에 필요한 프로필 인증이 없어서 서비스 정보를 조회할 수 없습니다.

오류: `UCP discovery failed - Missing profile uri`

### 근거로 쓴 응답 발췌

```
{"error": "tools/call 실패: HTTP 422", "body": "{\"jsonrpc\":\"2.0\",\"id\":2,\"error\":{\"code\":-32001,\"message\":\"UCP discovery failed\",\"data\":{\"code\":\"invalid_profile_url\",\"content\":\"Unable to fetch agent profile: Missing profile uri\",\"continue_url\":\"https://yxcs11-ry.myshopify.com/\"}}"}
```

---

# 3회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_business | `{"meta":{},"ask":"요즘 많이 팔리는 상품이 뭐야?"}` | UCP discovery failed - Missing profile uri, rc=3 |
| 2 | search_catalog | `{"meta":{},"catalog":"많이 팔리는"}` | UCP discovery failed - Missing profile uri, rc=3 |

### 답변

이 서버는 현재 사용할 수 없습니다. 모든 도구 호출에서 "UCP discovery failed - Missing profile uri" 오류가 발생합니다.

이 MCP 서버(Shopify Universal Commerce Platform)는 사용자 프로필 인증이 필수적입니다. 비상호형 세션에서는 OAuth 인증 흐름을 실행할 수 없어 도구에 접근할 수 없습니다.

도구가 범위 밖입니다: 서버 인증 미완료 — 대화형 세션에서 `claude mcp` 또는 `/mcp` 명령으로 인증이 필요합니다.

### 근거로 쓴 응답 발췌

```
HTTP 422
{
  "error": {
    "code": -32001,
    "message": "UCP discovery failed",
    "data": {
      "code": "invalid_profile_url",
      "content": "Unable to fetch agent profile: Missing profile uri",
      "continue_url": "https://yxcs11-ry.myshopify.com/"
    }
  }
}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_business | `{"meta":{},"ask":"이 서비스로 예약할 수 있는 게 뭐가 있어?"}` | UCP discovery failed - Missing profile uri, rc=3 |

### 답변

이 서버는 현재 사용할 수 없습니다. ask_business 도구 호출에서 "UCP discovery failed - Missing profile uri" 오류가 발생합니다.

이 MCP 서버는 사용자 프로필 인증이 필수입니다. 비상호형 세션에서는 인증할 수 없어 서버의 도구를 사용할 수 없습니다.

도구가 범위 밖입니다: 서버 인증 미완료.

### 근거로 쓴 응답 발췌

```
HTTP 422
{
  "error": {
    "code": -32001,
    "message": "UCP discovery failed",
    "data": {
      "code": "invalid_profile_url",
      "content": "Unable to fetch agent profile: Missing profile uri",
      "continue_url": "https://yxcs11-ry.myshopify.com/"
    }
  }
}
```
