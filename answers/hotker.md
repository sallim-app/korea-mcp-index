# ai.hotker/hotker

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://hotker.ai/mcp`.


---

# 1회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_products | `{}` | 공개 상품 0건, rc=0 |

### 답변

죄송하지만 현재 hotker 서비스의 공개 카탈로그에는 등록된 상품이 없습니다. 검색 결과가 비어 있어 요즘 많이 팔리는 상품을 안내해 드릴 수 없습니다.

### 근거로 쓴 응답 발췌

```
{"ok":true,"schemaVersion":"1.0.0","mcpServerVersion":"1.0.2","tool":"search_verified_products","status":"verified","generatedAt":"2026-11-03T13:41:29.160Z","data":{"dataAsOf":"2026-11-03T13:41:29.160Z","query":null,"category":null,"resultCount":0,"items":[]}}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_mobile_deals | `{}` | 휴대폰 판매 조건 0건(verified 0, partner_presented 0), rc=0 |

### 답변

현재 hotker에서는 확인된 예약 관련 도구가 없으며, 휴대폰 판매 조건 검색 결과도 비어 있습니다. 이 서버는 휴대폰 통신 요금 비교와 총비용(TCO) 계산 기능만 제공하고 있으며, 예약 기능은 제공되지 않습니다.

### 근거로 쓴 응답 발췌

```
{"ok":true,"schemaVersion":"1.0.0","mcpServerVersion":"1.0.2","tool":"search_verified_mobile_deals","status":"verified","generatedAt":"2026-11-03T13:41:33.303Z","data":{"dataAsOf":"2026-11-03T13:41:32.646Z","query":null,"carrier":null,"includePartnerPresented":true,"resultCount":0,"verifiedCount":0,"partnerPresentedCount":0,"items":[]}}
```

---

# 2회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_products | `{}` | 검증된 상품 목록 조회, 반환 건수 0건, rc=0 |

### 답변

죄송하지만 현재 HOTKER의 공개 카탈로그에는 검증된 상품이 등록되어 있지 않습니다. 서버가 반환한 결과가 비어 있어서 "요즘 많이 팔리는 상품"을 알려드릴 수 없습니다.

### 근거로 쓴 응답 발췌

```
{
  "ok": true,
  "schemaVersion": "1.0.0",
  "mcpServerVersion": "1.0.2",
  "tool": "search_verified_products",
  "status": "verified",
  "generatedAt": "2026-11-03T13:46:35.812Z",
  "data": {
    "dataAsOf": "2026-11-03T13:46:35.812Z",
    "query": null,
    "category": null,
    "resultCount": 0,
    "items": []
  }
}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_mobile_deals | `{}` | 휴대폰 판매조건 검색, 반환 건수 0건, rc=0 |

### 답변

HOTKER 서비스는 휴대폰 요금제와 통신사 계약 조건을 비교·계산하는 서비스입니다. 도구 검색 결과, 현재 예약 가능한 휴대폰 판매조건이 등록되어 있지 않습니다. 

HOTKER의 도구 목록을 보면 휴대폰 총비용 계산(calculate_mobile_tco), 약정 반환금 계산(calculate_contract_penalty), 결합할인 계산(calculate_combo_discount) 등이 있어서, 이미 구성된 요금제의 비용을 계산하고 비교하는 것은 가능합니다. 하지만 예약이나 신청을 직접 받는 기능은 이 서비스 범위에 없는 것으로 보입니다.

### 근거로 쓴 응답 발췌

```
{
  "ok": true,
  "schemaVersion": "1.0.0",
  "mcpServerVersion": "1.0.2",
  "tool": "search_verified_mobile_deals",
  "status": "verified",
  "generatedAt": "2026-11-03T13:46:28.013Z",
  "data": {
    "dataAsOf": "2026-11-03T13:46:27.142Z",
    "query": null,
    "carrier": null,
    "includePartnerPresented": true,
    "resultCount": 0,
    "verifiedCount": 0,
    "partnerPresentedCount": 0,
    "items": []
  }
}
```

---

# 3회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_products | `{}` | 공개 카탈로그 상품 0건, rc=0 |

### 답변

죄송하지만 HOTKER 서비스는 현재 공개된 상품 카탈로그를 제공하지 않고 있습니다. INDEX 검증을 통과한 상품이 없어서 "요즘 많이 팔리는 상품"에 대한 정보를 드릴 수 없습니다.

HOTKER는 통신사별 휴대폰 구매 조건과 요금제를 계산·비교하는 도구들을 제공하는 서비스입니다. 하지만 상품 카탈로그나 판매 현황 조회 기능은 이 MCP 도구 집합에 포함되어 있지 않습니다.

### 근거로 쓴 응답 발췌

```
{"ok":true,"schemaVersion":"1.0.0","mcpServerVersion":"1.0.2","tool":"search_verified_products","status":"verified","generatedAt":"2026-11-03T13:52:32.433Z","data":{"dataAsOf":"2026-11-03T13:52:32.433Z","query":null,"category":null,"resultCount":0,"items":[]}}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_verified_mobile_deals | `{}` | 검증된 휴대폰 거래 조건 0건, rc=0 |
| 2 | get_calculation_evidence | `{}` | 계산 엔진 정보 조회, rc=0 |

### 답변

HOTKER 서비스는 **예약 기능을 제공하지 않습니다**. 이 서비스는 통신사(SKT, KT, LG U+)의 휴대폰 구매 조건과 요금을 **계산·비교하는 도구**입니다.

제공되는 기능은:
- 휴대폰 총비용(12~36개월 TCO) 계산
- 약정 반환금 계산
- 통신사별 결합할인 계산
- 계산 근거 및 출처 제시

예약이나 구매 주문 기능은 없으며, 계산 결과를 바탕으로 통신사 공식 사이트에서 직접 신청해야 합니다. 따라서 이 서비스로 "예약할 수 있는 것"은 없습니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
- calculate_mobile_tco: 단말 전체 판매가, 기간별 요금, 의무 부가서비스·비용, 할부이자에서 확정 할인을 차감
- calculate_contract_penalty: SKT·KT·LG U+ 약정 반환금 계산
- calculate_combo_discount: 통신사별 월 결합할인 계산
- search_verified_products: HOTKER 공개 카탈로그 상품 검색 (현재 결과 0건)
- search_verified_mobile_deals: 휴대폰 판매조건 검색 (현재 결과 0건)
- get_calculation_evidence: 계산 엔진 버전, 산식 설명, 출처 URL 제시

결론: 예약 기능 없음 - 계산 도구만 제공
```
