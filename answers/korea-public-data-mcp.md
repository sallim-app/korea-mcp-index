# hjsh200219/korea-public-data-mcp

> 2026-10-01 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://public-data.up.railway.app/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action":"search_population_trends","region":"Seoul","years":["2019","2020","2021","2022","2023","2024"]}` | rc=1, 유효한 action 없음 |

### 답변

이 서버에서는 서울시 인구 변화 데이터를 제공하지 않습니다. public_data 도구는 약국, 병원, 동물병원, 드래그, 건강식품, 의약품 특허, 온비드 경매 정보만을 다룹니다.

### 근거로 쓴 응답 발췌
```
Invalid option: expected one of "search_pharmacy"|"search_hospital"|"get_hospital_detail"|"search_animal_hospital"|"search_rare_medicine"|"search_health_food"|"search_bio_equivalence"|"search_medicine_patent"|"verify_business"|"check_business_status"|"search_onbid_pbanc_cltr_detail"|"search_onbid_pbanc_list"
```

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action":"search_air_quality"}` | rc=1, 유효한 action 없음 |

### 답변

이 서버에서는 공공데이터포털의 대기질 데이터 정보를 제공하지 않습니다. public_data 도구가 다루는 범위에 대기질 데이터가 포함되지 않습니다.

### 근거로 쓴 응답 발췌
```
Invalid option: expected one of "search_pharmacy"|"search_hospital"|"get_hospital_detail"|"search_animal_hospital"|"search_rare_medicine"|"search_health_food"|"search_bio_equivalence"|"search_medicine_patent"|"verify_business"|"check_business_status"|"search_onbid_pbanc_cltr_detail"|"search_onbid_pbanc_list"
```


---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action": "서울시 인구", "query": "인구 변화"}` | rc=1, 도구가 지원하지 않음 (인구 통계 미지원) |
| 2 | gov24_ai | `{"action": "ask", "question": "서울시 인구가 최근 몇 년간 어떻게 변했습니까?"}` | rc=0, NEED_CLARIFICATION (명확한 답변 불가) |

### 답변

이 MCP 서버에서 서울시 인구의 최근 변화 추이에 대한 데이터를 제공받지 못했습니다. 

공공데이터포털의 public_data 도구는 약국, 병원, 의약품 등 보건의료 관련 데이터만 다루고 있으며, 인구 통계 데이터는 지원하지 않습니다. 정부24 AI에 문의한 결과도 명확한 답변(NEED_CLARIFICATION)을 받았으므로, 서울시 인구 변화 통계는 통계청(KOSIS) 등 다른 공식 통계 제공 기관을 직접 방문하여 확인하셔야 합니다.

### 근거로 쓴 응답 발췌
```
[public_data 도구 오류]
Invalid option: expected one of "search_pharmacy"|"search_hospital"|"get_hospital_detail"|"search_animal_hospital"|"search_rare_medicine"|"search_health_food"|"search_bio_equivalence"|"search_medicine_patent"|"verify_business"|"check_business_status"|"search_onbid_pbanc_cltr_detail"|"search_onbid_pbanc_list"

[gov24_ai 응답]
혹시 서울특별시의 인구 변화 추이를 확인하시려는 건가요? 최근 몇 년간의 인구 통계나 관련 자료를 찾고 계신지 궁금합니다.
⚠️ 답변 유형: NEED_CLARIFICATION (정상 답변이 아닐 수 있습니다)
```

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | gov24_ai | `{"action": "ask", "question": "공공데이터포털에서 대기질 데이터를 어디서 받을 수 있습니까?"}` | rc=0, 답변 획득 (신뢰도 95%) |

### 답변

공공데이터포털에서 대기질 데이터를 받으려면 다음 절차를 따르시면 됩니다:

**신청 방법:**
- 공공데이터 포털(www.data.go.kr)에 접속합니다
- 데이터를 검색하여 제공 여부를 확인합니다
- 제공되지 않는 경우 공공데이터 제공 신청서를 작성하여 제출합니다

**기본 정보:**
- 신청 자격: 일반 개인 또는 단체 모두 가능
- 비용: 무료
- 처리 기간: 제공 여부 결정까지 10일 이내
- 불복 구제: 제공 거부 결정에 불복이 있는 경우, 공공데이터제공 분쟁조정위원회에 신청 가능

**문의:**
- 소관 기관: 한국지능정보사회진흥원
- 공식 안내 링크: https://www.gov.kr/portal/service/serviceInfo/PTR000050579

### 근거로 쓴 응답 발췌
```
신청방법: 공공데이터 포털(www.data.go.kr)에서 대기질 데이터 제공 여부 확인 후 신청
신청경로: 공공데이터 포털 접속 → 데이터 검색 → 제공 여부 확인 → 제공되지 않는 경우 신청서 작성

지원대상: 일반 개인 또는 단체
비용: 무료
소요시간: 제공 여부 결정까지 10일 이내

주의사항: 제공되지 않는 데이터의 경우, 공공데이터 제공 신청서를 작성하여 제출해야 합니다.
불복 구제 절차: 제공 거부 결정에 불복이 있는 경우, 공공데이터제공 분쟁조정위원회에 신청할 수 있습니다.

소관기관: 한국지능정보사회진흥원
법적근거: [법령]공공데이터의 제공 및 이용 활성화에 관한 법률
신뢰도: 95 (높음)
```


---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | public_data | `{"action":"search","query":"서울시 인구"}` | rc=1 (isError: 인구 데이터는 public_data 도구에서 지원하지 않음) |
| 2 | gov24_ai | `{"action":"ask","question":"서울시 인구가 최근 몇 년간 어떻게 변했습니까?"}` | rc=0 (답변 타입: NEED_CLARIFICATION) |
| 3 | gov24_ai | `{"action":"ask","question":"서울시 인구 통계 데이터는 공공데이터포털에서 어디서 받을 수 있습니까?"}` | rc=0 (답변 받음, 신뢰도 74) |

### 답변

서버가 서울시 인구의 최근 몇 년간 변화 추이에 대한 구체적인 통계 데이터를 직접 제공하지 못했습니다. 

gov24_ai에 따르면, 서울시 인구 통계 데이터는 공공데이터 포털(www.data.go.kr)에서 검색하여 제공 여부를 확인할 수 있습니다. 필요한 경우 공공데이터 제공 신청서를 작성하여 제출하면 10일 이내에 제공 여부 결정을 받을 수 있습니다(무료).

구체적인 인구 수치나 연도별 변화는 이 서버에서 제공받지 못했으므로, 공공데이터포털에 직접 접속하여 검색하시기 바랍니다.

### 근거로 쓴 응답 발췌
```
#### 🔍 신청/발급 방법
- **신청방법**: 공공데이터 포털(www.data.go.kr)에서 검색 및 신청
- **신청경로**: 공공데이터 포털 접속 후 원하는 데이터 검색

#### 💰 수수료 및 처리 기간
- **비용**: 무료
- **소요시간**: 제공 여부 결정까지 10일 이내

#### ℹ️ 유의사항
- **주의사항**: 제공 여부 확인 후 신청서 작성 필요
```

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | gov24_ai | `{"action":"ask","question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있습니까?"}` | rc=0 (답변 받음, 신뢰도 95) |

### 답변

공공데이터포털(www.data.go.kr)에서 대기질 데이터를 받는 방법은 다음과 같습니다:

**신청 방법:**
1. 공공데이터 포털(www.data.go.kr)에 접속
2. 대기질 데이터 검색
3. 제공 여부 확인
4. 제공하지 않는 경우 공공데이터 제공 신청서 작성 및 제출

**특징:**
- 신청 대상: 일반 국민, 개인 또는 법인/시설/단체
- 비용: 무료
- 처리 기간: 제공 여부 결정까지 10일 이내
- 제공 거부 시, 거부 결정의 내용과 사유를 통보받으며, 불복 시 공공데이터제공 분쟁조정위원회에 신청할 수 있습니다.

### 근거로 쓴 응답 발췌
```
#### 🔍 신청/발급 방법 및 경로
- **신청방법**: 공공데이터 포털(www.data.go.kr)에서 대기질 데이터 제공 여부를 검색하고, 제공하지 않는 경우 공공데이터 제공 신청서를 작성하여 제출합니다.
- **신청경로**: 공공데이터 포털 접속 → 원하는 데이터 검색 → 제공 여부 확인 → 제공하지 않는 경우 신청서 작성 및 제출

#### 👤 대상 및 자격 요건
- **지원대상**: 일반 국민, 개인 또는 법인/시설/단체

#### 💰 수수료 및 처리 기간
- **비용**: 무료
- **소요시간**: 제공 여부 결정까지 10일 이내

#### ℹ️ 유의사항
- **주의사항**: 제공 거부 시, 거부 결정의 내용과 사유를 통보받으며, 불복 시 공공데이터제공 분쟁조정위원회에 신청할 수 있습니다.
```
