# com.selectbnbs/verify

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://selectbnbs.com/mcp`.


---

# 1회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | verify_listing_registration | `{"listing_details":"popular_products","country":"KR"}` | 매칭되는 기록 없음(NOT_FOUND), rc=1 |

### 답변

SelectBnBs 서버는 판매 상품 통계나 인기 상품 정보를 제공하지 않습니다. 이 서비스는 Airbnb, 게스트하우스, 한옥 스테이, 홈스테이, 펜션 같은 단기 숙박 리스팅이 **정부에 등록·허가되었는지 검증**하는 도구만 제공합니다. 판매량 데이터나 상품 인기도를 조회할 수 있는 도구가 없습니다.

### 근거로 쓴 응답 발췌

```
SelectBNBs Verify - South Korea government accommodation registry
Result: No matching record found (NOT_FOUND).
No matching government permit record was found for these details.
Source: official government registry, cache refreshed 2026-11-02.
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | verify_listing_registration | `{"listing_details":"reservation_service","country":"KR"}` | 매칭되는 기록 없음(NOT_FOUND), rc=1 |

### 답변

SelectBnBs로는 예약을 할 수 없습니다. 이 서비스는 예약 플랫폼이 아니라 **정부 허가 검증 서비스**입니다. 도구 설명에 따르면 Airbnb, 게스트하우스, 한옥 스테이, 홈스테이, 펜션의 정부 등록 여부를 확인할 수 있을 뿐, 예약 기능은 제공되지 않습니다.

### 근거로 쓴 응답 발췌

```
SelectBNBs Verify - South Korea government accommodation registry
Result: No matching record found (NOT_FOUND).
No matching government permit record was found for these details.
What to do next: A name or address search found no permit record.
Source: official government registry, cache refreshed 2026-11-02.
SelectBNBs Verify covers South Korea today; more countries are coming.
```

---

# 2회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_permit_record | `{"country":"KR"}` | 인자 부족(management_number 또는 name+region 필요), rc=1 |

### 답변

이 MCP 서버는 한국 정부의 숙박업 등록 데이터를 검증하는 도구만 제공합니다. "많이 팔리는 상품"이나 판매 통계, 인기도 정보는 제공하지 않습니다. 

**서버가 제공하는 기능**: 특정 숙박 허가 기록을 정부 데이터베이스에서 조회하거나, Airbnb의 등록 정보가 정부 등록과 일치하는지 검증하는 것뿐입니다.

### 근거로 쓴 응답 발췌

```
Send either management_number, or name together with region.
What to do next: Send either management_number alone, or name together with the Korean region (e.g. 제주특별자치도 제주시).
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | verify_listing_registration | `{"country":"KR","listing_details":"test"}` | 형식 오류(Airbnb의 Registration details 박스 필요), rc=1 |

### 답변

SelectBNBs(selectbnbs.com/mcp)는 예약 서비스가 아니라, **한국 정부의 숙박업 등록 여부를 검증하는 도구**입니다. 이 서버로는 예약을 할 수 없으며, 제공하는 기능은:

- Airbnb 목록의 등록 정보가 정부 데이터와 일치하는지 확인
- 정부 허가 기록 조회 (management number나 이름+지역으로)

예약은 Airbnb나 다른 숙박 예약 플랫폼을 통해야 합니다.

### 근거로 쓴 응답 발췌

```
SelectBNBs Verify - South Korea government accommodation registry
Copy and paste the whole "Registration details" box from Airbnb, including Region of issuance, Licence type, and Licence number.
Source: official government registry, cache refreshed 2026-11-02. SelectBNBs Verify covers South Korea today; more countries are coming. Human check page: https://selectbnbs.com/verify/
```

---

# 3회차

## 질문 1: 요즘 많이 팔리는 상품이 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | verify_listing_registration | `{"listing_details":"best sellers","country":"KR"}` | 매칭 기록 없음, rc=1 |

### 답변

이 서비스(SelectBnBs)는 단기 숙박시설의 정부 허가 여부를 검증하는 도구만 제공하고 있어서, 요즘 많이 팔리는 상품에 대한 정보는 제공하지 않습니다. SelectBnBs는 Airbnb, 게스트하우스, 한옥체험, 홈스테이, 펜션 등 숙박시설이 한국 정부에 등록되어 있는지 확인해주는 서비스일 뿐, 판매 통계나 인기 상품 목록 기능이 없습니다.

### 근거로 쓴 응답 발췌

```
SelectBNBs Verify - South Korea government accommodation registry
Result: No matching record found (NOT_FOUND).
```

---

## 질문 2: 이 서비스로 예약할 수 있는 게 뭐가 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_permit_record | `{"country":"KR"}` | 필수 인자 부족 오류, rc=1 |

### 답변

이 서비스(SelectBnBs)는 예약 기능을 제공하지 않습니다. SelectBnBs는 숙박시설의 정부 허가 등록 여부를 검증하는 것만 목적이며, 실제 예약이나 숙박업소 검색·예약 기능은 없습니다. 도구가 제공되지 않는 범위입니다.

### 근거로 쓴 응답 발췌

```
SelectBNBs Verify - South Korea government accommodation registry
```
