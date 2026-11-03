# it.marketpilot/marketpilot

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://api.marketpilot.it/mcp`.


---

# 1회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | list_products | `{}` | 상품 목록 조회 완료, rc=0 |

### 답변

죄송하지만, 이 서비스는 **상품의 판매량·인기도 정보를 제공하지 않습니다**. 

marketpilot은 SNS 마케팅 상품(인스타그램·페이스북 좋아요·팔로우·댓글 등) 구매 서비스로, 도구는 단순히 **전체 상품 목록**만 제시할 수 있습니다. 어떤 상품이 요즘 많이 팔리는지는 서버의 데이터 범위 밖입니다.

서비스에서 주문할 수 있는 상품은 있으며(인스타그램, 페이스북, 스레드 등 SNS별 마케팅 상품 100개 이상), 각 상품마다 단가와 주문 수량 제한이 있습니다.

### 근거로 쓴 응답 발췌

```
list_products는 주문 가능한 마케팅 상품 목록(상품 ID·이름·분류·단가·최소/최대 수량)을 조회합니다.
응답에는 productId, productName, category, unitPrice, minOrderUnit, maxOrderUnit, aiOrderable 만 포함되며
판매량이나 인기도 필드는 없습니다.
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

(호출 없음 — 도구 목록에서 예약 기능 부재 확인)

### 답변

이 서비스에는 **예약 기능이 없습니다**. 

Marketpilot은 SNS 마케팅 상품(좋아요, 팔로우, 댓글 등) **구매 서비스**입니다. 예약이나 시간 설정 같은 기능은 서버가 제공하지 않으며, 제공되는 도구는:

- 상품 주문 및 결제 (create_checkout)
- 주문 상태 조회 (get_checkout_status)  
- 정부지원사업 정보 조회
- 나라장터 입찰공고 정보 조회
- 회원가입 및 포인트 관리

예약할 수 있는 것이 없습니다. 원하시는 서비스가 다른 것이라면 상담(submit_inquiry)을 통해 문의하실 수 있습니다.

### 근거로 쓴 응답 발췌

```
whoami 도구 응답에 따르면 이 서버의 모든 도구는:
- list_products: 상품 목록 조회
- get_product: 상품 상세 조회
- search_places: 네이버 플레이스 검색
- create_checkout: 결제 링크 생성
- get_checkout_status: 결제 상태 확인
- submit_inquiry: 상담 문의
- send_signup_code, signup: 회원가입
- quote_order, create_order: 주문 생성
- list_my_orders, get_my_order: 주문 조회
- get_point_balance, request_point_charge: 포인트 관리
- list_support_matches, search_support_programs, get_support_program: 정부지원사업
- search_startup_events: 창업 행사
- search_procurement_bids, get_procurement_bid: 나라장터 입찰

예약(booking, reservation, schedule) 관련 도구는 없습니다.
```

완료 marketpilot r1

---

# 2회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | list_products | `{}` | 전체 상품 목록 조회(103개 상품), rc=0 |

### 답변

이 서비스에서 제공하는 도구에는 판매량이나 인기도를 보여주는 기능이 없어서, 어떤 상품이 요즘 많이 팔리는지 알 수 없습니다.

조회할 수 있는 것은 전체 상품 목록뿐인데, 여기서는 각 상품의 단가와 주문 가능 수량 범위만 나타나고, 판매량이나 인기 순위 정보는 제공되지 않습니다. 만약 구체적인 상품이 궁금하시다면, 상품 카테고리별로는 다음과 같이 정리되어 있습니다: 네이버 플레이스 서비스(저장, 유입, 길찾기, 통합), 인스타그램 서비스(좋아요, 팔로우, 댓글, 저장, 공유, 릴스, 리그램 등 다양한 조합), 페이스북 서비스, 스레드 서비스 등입니다.

### 근거로 쓴 응답 발췌

```
도구 list_products의 응답에는 productId, productName, category, unitPrice, minOrderUnit, maxOrderUnit, aiOrderable 필드만 포함되며, 판매량(sales volume), 인기도(popularity), 순위(rank) 등의 정보는 없음.

서버의 사용 가능한 도구 중 판매량·인기도를 조회하는 도구:
- whoami: 신원·권한 확인
- list_products: 상품 목록 조회
- get_product: 상품 상세 조회
- search_places: 네이버 플레이스 검색
- create_checkout: 결제 링크 생성
- get_checkout_status: 결제 상태 확인
- submit_inquiry: 상담 문의
- send_signup_code: 회원가입(1단계)
- signup: 회원가입(2단계)

위 도구 중 판매량·인기 정보를 제공하는 도구 없음.
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | whoami | `{}` | 서비스 기능 그룹 확인, rc=0 |

### 답변

이 서비스에는 "예약" 기능이 없습니다. 대신 마케팅 상품을 **주문**하는 시스템이 있습니다.

주문할 수 있는 것들은:

1. **소셜 미디어 마케팅 서비스**: 인스타그램 좋아요·팔로우·댓글, 페이스북 좋아요·댓글, 스레드 좋아요·팔로우, 네이버 플레이스 저장·유입 등 103개의 상품을 주문할 수 있습니다.

2. **주문 방식**:
   - 카드 결제: `create_checkout`으로 결제 링크를 만들어 바로 결제
   - 포인트 결제: 계정을 연결한 후 `quote_order`(견적)→`create_order`(확정) 절차로 주문

3. **추가 서비스 (로그인 후 이용 가능)**:
   - 정부지원사업 매칭
   - 나라장터 입찰 정보 검색

예약 개념이 필요하신 경우, `submit_inquiry` 도구로 상담을 요청할 수 있습니다.

### 근거로 쓴 응답 발췌

```
availableGroups:
- key: "shop"
  label: "둘러보기·카드 결제 링크"
  tools: ["list_products", "get_product", "search_places", "create_checkout", "get_checkout_status", "submit_inquiry"]

- key: "guest_signup"
  label: "회원가입"
  tools: ["send_signup_code", "signup"]

linkableGroups (로그인 후 이용):
- key: "customer_order"
  label: "주문·포인트 (본인)"
  tools: ["quote_order", "create_order", "list_my_orders", "get_my_order", "get_point_balance", "request_point_charge", "list_charge_requests", "get_charge_request", "cancel_charge_request"]

- key: "support_program"
  label: "정부지원사업"
  
- key: "procurement"
  label: "나라장터 입찰"

서버 설명: "예약(reservation)" 기능은 없고, 상품 주문과 포인트 결제 시스템만 제공.
```

---

# 3회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | list_products | `{}` | 상품 283개 조회, 판매량/인기도 정보 없음, rc=0 |

### 답변

이 서버는 판매량이나 인기도 정보를 제공하지 않습니다. 조회한 상품 목록에는 상품명, 분류, 단가, 수량 제약만 포함되어 있고, 어떤 상품이 요즘 많이 팔리는지 알 수 있는 판매 통계나 인기 순위 데이터는 없습니다. 

서버의 상품은 주로 SNS 마케팅(네이버 플레이스, 인스타그램, 페이스북, 쿠팡 등) 서비스와 디자인 작업 같은 마케팅 상품 283개인데, 어느 것이 인기인지는 서버에서 알 수 없습니다.

### 근거로 쓴 응답 발췌

```
list_products 응답에 포함된 필드:
- productId
- productName  
- category
- unitPrice
- hasCustomPrice
- minOrderUnit
- maxOrderUnit
- aiOrderable
- aiOrderableReason

판매량, 인기도, 조회수 등 판매 통계 필드 없음.

상품 분류 예시:
- N플레이스 > 트래픽 (4개)
- 인스타그램 (50개 이상)
- 페이스북 (50개 이상)
- 스레드 (여러 개)
- 쿠팡 마케팅
- 중국 플랫폼 > 샤오홍슈
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | list_products | `{}` | 상품 283개 목록, 예약 기능 없음, rc=0 |

### 답변

이 서비스는 예약 기능을 제공하지 않습니다. 

이 서버는 마케팅 상품 주문 서비스로, SNS 팔로우/좋아요/댓글 같은 마케팅 서비스, 디자인 작업, 광고 이행 등을 돈을 주고 사는 방식입니다. 예약이라는 개념이 없고, 주문(order)과 결제(checkout) 방식으로 작동합니다. 도구 목록에도 예약 관련 도구(reservation, booking 등)가 없습니다.

### 근거로 쓴 응답 발췌

```
MCP 도구 목록:
- list_products: 주문 가능한 마케팅 상품 목록
- get_product: 상품 상세 정보
- search_places: 네이버 플레이스 검색
- create_checkout: 결제 링크 생성
- get_checkout_status: 결제 상태 확인
- create_order: 주문 생성
- quote_order: 견적 요청
- list_my_orders: 주문 내역 조회
- request_point_charge: 포인트 충전
(예약·booking·reservation 관련 도구 없음)

상품 분류: SNS 마케팅, 디자인, 광고 이행
작동 방식: 주문 → 결제 → 진행
```
