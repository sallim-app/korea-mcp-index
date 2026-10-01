# com.theprotoclinical/commerce

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_catalog | {"meta": {}, "catalog": {"query": "popular"}} | HTTP 422 - UCP discovery failed |
| 2 | get_product | {"meta": {}, "catalog": "sample"} | HTTP 422 - UCP discovery failed |

### 답변
**이 서버로는 답할 수 없습니다.**

서버가 Shopify UCP(Universal Commerce Platform)와 통합되어 있으나, 현재 profile_uri 설정이 누락되어 카탈로그 쿼리 불가 상태입니다(HTTP 422 오류). 추가로, search_catalog·get_product 도구는 **단순 검색·조회만 가능하며 판매 통계나 트렌드 데이터는 제공하지 않습니다.** "요즘 많이 팔리는" 정보는 이 MCP의 범위를 벗어납니다.

### 근거로 쓴 응답 발췌
```
{"error": "HTTP 422", "message": "UCP discovery failed", "data": {"code": "invalid_profile_url", "content": "Unable to fetch agent profile: Missing profile uri"}}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | (도구 목록 검토) | - | 예약 관련 도구 없음 확인 |

### 답변
**이 서버로는 답할 수 없습니다.**

이 MCP의 도구 목록(15개)에 예약(reservation/booking) 기능이 없습니다. 제공되는 것은 get_checkout, create_checkout, update_checkout, complete_checkout, cancel_checkout, get_cart, create_cart, update_cart, cancel_cart, get_order, search_catalog, lookup_catalog, get_product로, 모두 **전자상거래/쇼핑 결제 기능**입니다. 의료 서비스 예약이나 일정 예약 기능은 이 서버에 없습니다.

### 근거로 쓴 응답 발췌
서버 제공 도구 목록(15개 전수):
- 결제/장바구니: get_checkout, create_checkout, update_checkout, complete_checkout, cancel_checkout, get_cart, create_cart, update_cart, cancel_cart, get_order
- 제품 검색: search_catalog, lookup_catalog, get_product

---

## 실제로 이 서버가 다루는 것
Shopify 온라인 스토어의 전자상거래 기능 — 상품 검색·조회, 장바구니 관리, 결제 처리, 주문 관리. (예약·예약 시간 관리는 미포함)

## 이 서버를 쓰면서 느낀 점
theprotoclinical 도메인명은 의료 임상 관련으로 보이지만, MCP 서버는 Shopify 기반 순수 전자상거래 기능만 노출됩니다. 사용자의 "예약" 기대(의료 서비스 예약 추정)와 실제 기능(상품 판매)이 맞지 않으므로 질문이 성립하지 않습니다. 서버 설정 미완 + 범위 불일치로 인해 두 질문 모두 답 불가입니다.
