# kr.ibtcc/competition-ratio

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://ibtcc.kr/api/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

도구 없음 — 이 서버의 범위 밖

### 답변

죄송하지만, 이 MCP 서버는 **공공기관 채용 정보**만 제공합니다(채용 경쟁률·일정·공고). 서울시 인구 추이 데이터는 제공하지 않습니다. 

인구 데이터는 **통계청 통계 자료실**이나 **서울시 지역경제실의 통계**에서 확인할 수 있습니다.

### 근거로 쓴 응답 발췌

```
제공 도구 목록:
- lookup_competition_ratio: 공공기관 채용 경쟁률
- lookup_job_schedule: 공공기관 채용 일정
- lookup_job_posting: 공공기관 채용 공고
- convert_exam_score: 영어 점수 환산
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

도구 없음 — 이 서버의 범위 밖

### 답변

죄송하지만, 이 MCP 서버는 **공공기관 채용 정보**만 제공합니다. 공공데이터포털의 대기질 데이터 위치나 접근 방법은 제공하지 않습니다.

대기질 데이터는 **공공데이터포털(data.go.kr)**에서 "대기질"을 검색하거나, **환경부 에어코리아(airkorea.or.kr)** 사이트에서 확인할 수 있습니다.

### 근거로 쓴 응답 발췌

```
제공 도구 목록:
- lookup_competition_ratio: 공공기관 채용 경쟁률
- lookup_job_schedule: 공공기관 채용 일정
- lookup_job_posting: 공공기관 채용 공고
- convert_exam_score: 영어 점수 환산
```

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | - | - | 호출 안 함 |

### 답변

이 MCP 서버(`https://ibtcc.kr/api/mcp`)는 한국 공공기관과 공기업의 채용 정보만 제공합니다. 인구 통계 도구가 없어서 서울시 인구 변화를 조회할 수 없습니다.

서울시 인구 데이터는 통계청(KOSTAT)의 인구통계나 공공데이터포털(data.go.kr)의 인구 관련 API를 이용해야 합니다.

### 근거로 쓴 응답 발췌

이 서버가 제공하는 도구:
- lookup_competition_ratio: 공기업 채용 경쟁률
- lookup_job_schedule: 공기업 채용 일정
- lookup_job_posting: 공기업 채용 공고
- convert_exam_score: 시험 점수 환산
- get_my_roadmap_summary: 개인 로드맵 요약

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | - | - | 호출 안 함 |

### 답변

이 MCP 서버(`https://ibtcc.kr/api/mcp`)는 한국 공공기관과 공기업의 채용 정보만 제공합니다. 대기질 데이터 조회 도구가 없어서 공공데이터포털의 대기질 데이터 위치를 알려드릴 수 없습니다.

대기질 데이터는 공공데이터포털(data.go.kr)에서 직접 검색하거나, 환경부·기상청 등 환경 관련 기관의 공개 API를 이용해야 합니다.

### 근거로 쓴 응답 발췌

이 서버가 제공하는 도구:
- lookup_competition_ratio: 공기업 채용 경쟁률
- lookup_job_schedule: 공기업 채용 일정
- lookup_job_posting: 공기업 채용 공고
- convert_exam_score: 시험 점수 환산
- get_my_roadmap_summary: 개인 로드맵 요약

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

(도구 호출 없음)

### 답변

이 서버(ibtcc.kr/api/mcp)는 한국 공공기관의 채용 정보만 제공합니다. 서울시 인구 통계는 이 서버의 범위에 없어서 조회할 수 없습니다.

이 서버가 제공하는 도구는:
- lookup_competition_ratio: 공공기관 채용 경쟁률
- lookup_job_schedule: 공공기관 채용 일정
- lookup_job_posting: 공공기관 채용 공고
- convert_exam_score: 시험 점수 환산
- get_my_roadmap_summary: 로드맵 요약

인구 통계는 **통계청(kosis.kr)** 또는 **서울시청 공식 통계** 페이지에서 확인하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
lookup_competition_ratio - 필수=institution 한국 공공기관(공기업) 채용 경쟁률
lookup_job_schedule - 필수=company 한국 공공기관(공기업)의 채용 일정
lookup_job_posting - 필수=org_name 한국 공공기관(공기업)의 채용 공고
(인구 통계 도구 없음)
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

(도구 호출 없음)

### 답변

이 서버(ibtcc.kr/api/mcp)는 한국 공공기관의 채용 정보만 제공합니다. 공공데이터포털의 대기질 데이터 접근 경로는 이 서버의 범위에 없어서 조회할 수 없습니다.

대기질 데이터는 **공공데이터포털(data.go.kr)**에서 직접 검색하시거나, **한국환경공단의 에어코리아(airkorea.or.kr)** 에서 확인하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
lookup_competition_ratio - 필수=institution 한국 공공기관(공기업) 채용 경쟁률
lookup_job_schedule - 필수=company 한국 공공기관(공기업)의 채용 일정
lookup_job_posting - 필수=org_name 한국 공공기관(공기업)의 채용 공고
(대기질 데이터 도구 없음)
```
