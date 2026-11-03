# hjsh200219/korea-public-data-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://public-data.up.railway.app/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action":"서울시 인구"}` | 도구 범위 밖 - 약료·병원·경매 데이터만 제공, rc=1 |

### 답변

이 MCP 서버는 서울시 인구 통계를 제공하지 않습니다.

서버의 `public_data` 도구는 약국, 병원, 동물병원, 희귀의약품, 건강기능식품, 의약품 특허, 온비드 경매 정보 등 제한된 범위의 공공 데이터만 다루고 있습니다. 인구 통계는 이 도구의 범위에 포함되지 않습니다.

서울시 인구 변화 추이를 알아보려면 **서울시청 통계** 또는 **통계청 인구통계** 같은 다른 공공데이터포털의 인구 통계 API를 이용해야 합니다.

### 근거로 쓴 응답 발췌

```
MCP error -32602: Input validation error: Invalid arguments for tool public_data: [
  {
    "code": "invalid_value",
    "values": [
      "search_pharmacy",
      "search_hospital",
      "get_hospital_detail",
      "search_animal_hospital",
      "search_rare_medicine",
      "search_health_food",
      "search_bio_equivalence",
      "search_medicine_patent",
      "verify_business",
      "check_business_status",
      "search_onbid_pbanc_cltr_detail",
      "search_onbid_pbanc_list"
    ]
  }
]
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | (해당 도구 없음) | - | 대기질 조회 도구 부재, rc=3 |

### 답변

이 MCP 서버는 대기질 데이터를 조회하는 도구를 제공하지 않습니다.

서버의 전체 도구 목록(legal_research, case_research, law_amendment, import_clearance, export_clearance, shipping_logistics, tariff_lookup, trade_entity, corporate_disclosure, public_data, insurance, tourism, financial_product, procurement, youtube, product_review, foreign_case_research, assembly, gov24_ai)을 검토한 결과, 환경이나 공기질 관련 데이터를 제공하는 도구가 없습니다.

**공공데이터포털(data.go.kr)에서 대기질 데이터를 받으려면:**
- 공공데이터포털 웹사이트에서 "대기질", "공기질", "미세먼지" 등의 키워드로 검색
- 환경부, 각 지역 보건환경연구원 등 기관에서 제공하는 데이터셋 확인
- 해당 데이터의 Open API 또는 CSV 다운로드 옵션 활용

### 근거로 쓴 응답 발췌

```
Available tools in korea-public-data-mcp server:
- legal_research
- case_research
- law_amendment
- import_clearance
- export_clearance
- shipping_logistics
- tariff_lookup
- trade_entity
- corporate_disclosure
- public_data (약료·병원·경매만 제공)
- insurance
- tourism
- financial_product
- procurement
- youtube
- product_review
- foreign_case_research
- assembly
- gov24_ai

(환경·대기질 관련 도구 없음)
```

완료 korea-public-data-mcp r1

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action": "search", "query": "서울시 인구"}` | 도구가 해당 데이터를 지원하지 않음, rc=1 |

### 답변

이 MCP 서버는 서울시 인구에 관한 데이터를 제공하지 않습니다. 서버에 포함된 public_data 도구는 약국, 병원, 희귀약, 약특허, 온비드 공매 물건 등의 정보만 지원하며, 통계 데이터는 범위 밖입니다.

### 근거로 쓴 응답 발췌

```
Invalid option: expected one of "search_pharmacy"|"search_hospital"|"get_hospital_detail"|"search_animal_hospital"|"search_rare_medicine"|"search_health_food"|"search_bio_equivalence"|"search_medicine_patent"|"verify_business"|"check_business_status"|"search_onbid_pbanc_cltr_detail"|"search_onbid_pbanc_list"
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | gov24_ai | `{"action": "ask", "question": "대기질 데이터"}` | 명확한 답변을 제공하지 못함, rc=0 |

### 답변

이 MCP 서버는 공공데이터포털의 대기질 데이터에 관한 구체적인 정보를 제공하지 않습니다. 서버의 도구들은 법령, 관세, 금융상품, 관광, 기업공시, 민원절차 등 다른 분야에 특화되어 있으며, 환경·대기질 데이터는 범위 밖입니다.

### 근거로 쓴 응답 발췌

```
죄송하지만 문의하신 대기질 데이터에 대한 자료가 현재 확인되지 않아 자세한 안내를 도와드리기 어려워요.

⚠️ 답변 유형: NEED_CLARIFICATION (정상 답변이 아닐 수 있습니다)
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

(도구 호출 불가)

### 답변

이 서버에서는 서울시 인구 통계 데이터를 제공하지 않습니다.

이 MCP 서버의 public_data 도구는 약국·병원·희귀의약품·건강식품·의약품 특허·온비드 경매 물건 등만 검색할 수 있습니다. 인구 통계는 도구 범위에 포함되지 않습니다.

**대신 이용 가능한 출처:**
- 통계청(kostat.go.kr): 인구총조사, 장래인구추계
- 서울시청 통계(stat.seoul.go.kr): 서울 인구 추이
- 공공데이터포털(data.go.kr): 행정안전부 지역별 인구 데이터

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

(도구 호출 불가)

### 답변

이 서버에서는 공공데이터포털의 데이터 카탈로그 정보를 제공하지 않습니다.

이 MCP 서버의 도구는 특정 공공 데이터(약국·병원·의약품·경매·관광·법률·통관 등)에 대한 직접 조회만 제공합니다. 공공데이터포털의 대기질 데이터셋이 어디 있는지, 또는 어떤 API로 접근하는지에 대한 정보는 이 서버의 범위를 벗어납니다.

**직접 확인하는 방법:**
- 공공데이터포털(data.go.kr)에 접속해 "대기질" 또는 "에어코리아"로 검색
- 환경부 에어코리아(airkorea.or.kr)의 개방 API 활용
- 각 지자체의 환경 데이터 API

---

**이 회차 평가:** 이 MCP 서버의 도구는 두 질문 모두에 대한 데이터를 제공하지 않습니다. 특정 공공 정보 도메인에 특화된 서버이며, 범용 통계(인구) 또는 범용 카탈로그 정보(데이터포털 메타데이터)는 제공 범위가 아닙니다.
