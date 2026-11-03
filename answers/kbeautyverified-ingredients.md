# com.kbeautyverified/ingredients

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://kbeautyverified.com/mcp`.


---

# 1회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | recent_updates | `{}` | 최신 업데이트 조회(성분 규제 변경사항), rc=0 |
| 2 | ask_kbeauty_verified | `{"question":"요즘 많이 팔리는 한국 뷰티 상품들이 뭐가 있나? 많이 판매되는 K-beauty 제품 종류를 추천해줄 수 있나?"}` | 제품 카테고리 링크 제시, rc=0 |

### 답변

죄송합니다만, KBeauty Verified™ 서비스는 **판매량이 많은 상품을 추천하거나 인기 상품 순위를 제공하지 않습니다.** 

이 서비스가 제공하는 정보는 한국(MFDS), 유럽연합(CosIng), 미국(FDA) 등의 공식 규제 기록 기반으로 상품 성분이 각 시장에서 어떤 제약을 받는지 확인하는 것입니다. 판매량이나 인기도 같은 시장 데이터는 이 서버에 없습니다.

다만 [KBeauty Verified™의 상품 페이지](https://kbeautyverified.com/products/)에서 등록된 상품들을 일반 검색으로 살펴볼 수는 있습니다.

### 근거로 쓴 응답 발췌

```
"what": "K-beauty products and ingredients compared with official records from Korea (MFDS), the EU (CosIng) and the U.S. (FDA), plus rules for 7 more export markets, each rule with its official source and the date we checked.",
"does_not": "No safety ratings, no lab tests, no medical advice, no product rankings.",
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | about | `{}` | 서비스 정보 조회, rc=0 |

### 답변

이 서비스는 **예약 기능을 제공하지 않습니다.** 

KBeauty Verified™는 K-뷰티 상품과 성분 정보를 한국, 유럽, 미국 등의 공식 규제 기록과 비교해주는 정보 제공 서비스입니다. 제공되는 기능은:

- K-뷰티 상품과 성분 검색
- 각 시장의 규제 정보 확인 (성분 제한, 금지 성분, 기능성 화장품 공고)
- 공식 리콜 및 경고 기록 조회

상품 구매나 예약과 같은 거래 기능은 없으며, 오직 규제 정보와 성분 정보 조회만 가능합니다.

### 근거로 쓴 응답 발췌

```
"what": "K-beauty products and ingredients compared with official records from Korea (MFDS), the EU (CosIng) and the U.S. (FDA), plus rules for 7 more export markets, each rule with its official source and the date we checked.",
"does_not": "No safety ratings, no lab tests, no medical advice, no product rankings.",
"data": [
  "MFDS cosmetic ingredient restrictions and functional-cosmetic notice",
  "EU CosIng annexes II–VI",
  "FDA sunscreen monograph (M020) and cosmetic rules",
  "brands' own published ingredient lists",
  "official recall and alert records"
]
```

---

# 2회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_kbeauty_verified | `{"question":"요즘 많이 팔리는 한국 화장품 상품은 어떤 게 있나요?"}` | 질문 이해 불가, kind=empty, answered=false, rc=0 |

### 답변

이 서비스는 화장품의 **판매량이나 인기도 정보를 제공하지 않습니다**. KBeauty Verified™는 화장품의 성분과 규제 정보만 담고 있으며, 서비스 소개에서 "제품 랭킹(product rankings)"을 명시적으로 제공하지 않는다고 밝혔습니다.

이 서비스가 할 수 있는 일은:
- 화장품 성분을 한국(MFDS), EU, 미국(FDA) 규제와 비교
- 특정 성분의 규제 상태 조회
- 제품의 전체 성분표와 규제 준수 여부 확인
- 화장품 리콜 및 경고 기록 검색

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_kbeauty_verified | `{"question":"이 서비스에서 예약할 수 있는 게 뭐가 있나요?"}` | 질문 이해 불가, kind=empty, answered=false, 명확화 요청, rc=0 |

### 답변

이 서비스는 **예약 기능을 제공하지 않습니다**. KBeauty Verified™는 화장품 정보 검증 서비스이며, 제품 구매나 미용 서비스 예약 같은 기능은 범위 밖입니다.

서버가 서비스 범위를 명시적으로 설명한 것처럼, 이 서비스는 다음만 지원합니다:
- **제품 조회** (브랜드 + 제품명)
- **성분 정보** (성분 규제 상태)  
- **규정 검색** (한국·EU·미국 등의 화장품 규제)

예약이나 구매 같은 거래 기능은 제공하지 않습니다.

### 근거로 쓴 응답 발췌

```
"what": "K-beauty products and ingredients compared with official records from Korea (MFDS), the EU (CosIng) and the U.S. (FDA), plus rules for 7 more export markets, each rule with its official source and the date we checked.",

"does_not": "No safety ratings, no lab tests, no medical advice, no product rankings.",

"text": "무엇을 물으시는지 잘 모르겠습니다 — 조금 더 알려 주실래요? 제품(브랜드 + 제품명), 성분(예: 「나이아신아마이드 EU에서 허용돼?」), 규정 중 어느 쪽인가요?"
```

---

# 3회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_kbeauty_verified | `{"question":"요즘 많이 팔리는 상품이 뭐야?"}` | 질문을 이해할 수 없음, rc=0 |

### 답변

죄송하지만 KBeauty Verified™는 이 정보를 제공하지 않습니다. 이 서비스는 K-beauty 제품과 성분의 **규제 정보**를 제공하는 것이지, 판매량이나 인기 제품 데이터는 갖고 있지 않습니다. 

요즘 많이 팔리는 상품을 알려드리려면 판매 데이터나 시장 조사 자료가 필요한데, KBeauty Verified™는 한국(MFDS), 유럽(CosIng), 미국(FDA) 등 공식 규제 기관의 기록만 다룹니다.

### 근거로 쓴 응답 발췌

```json
{
 "kind": "empty",
 "answered": false,
 "text": "음, 무엇을 물으시는지 확실하지 않습니다. 혹시 이 중 하나인가요?",
 "sources": [],
 "links": []
}
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_kbeauty_verified | `{"question":"이 서비스로 예약할 수 있는 게 뭐가 있어?"}` | 질문을 이해할 수 없음, rc=0 |

### 답변

KBeauty Verified™는 예약 서비스가 아닙니다. 이 서비스의 범위는 **정보 제공**에만 한정되어 있습니다. 

KBeauty Verified™가 제공하는 것:
- K-beauty 제품과 성분의 규제 정보
- 성분 검색 및 규제 기준 조회
- 공식 회수·경고 기록 검색
- 각국(한국·EU·미국 등) 규제 비교

예약이 필요하신 서비스라면 다른 플랫폼이나 예약 전문 서비스를 이용하셔야 합니다.

### 근거로 쓴 응답 발췌

```json
{
 "kind": "empty",
 "answered": false,
 "text": "무엇을 물으시는지 잘 모르겠습니다 — 조금 더 알려 주실래요? 혹시 이 중 하나인가요?",
 "sources": [],
 "links": []
}
```

---

**출처:** [KBeauty Verified™](https://kbeautyverified.com)
