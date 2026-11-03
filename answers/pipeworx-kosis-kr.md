# io.github.pipeworx-io/kosis-kr

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/kosis-kr/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kosis_search | `{"searchNm":"서울시 인구"}` | KOSIS API 키 필요, rc=1 |
| 2 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했는지 알려줘"}` | 한국 전체 인구 반환(시티 레벨 아님), rc=0 |
| 3 | discover_tools | `{"query":"Seoul population time series city level Korea statistics"}` | KOSIS 도구 발견했으나 API 키 필요, rc=0 |
| 4 | ask_pipeworx | `{"question":"Seoul city population trend recent years"}` | 타임아웃 오류, rc=1 |

### 답변

죄송하지만, 이 서버에서 서울시 인구의 최근 추세를 제공할 수 없습니다. 

**이유:**
- **KOSIS(통계청) 데이터 도구**: 한국 통계청의 공식 데이터를 제공할 수 있는 `kosis_search`와 `kosis_stat_data` 도구가 있지만, 무료 API 키가 필요합니다(https://kosis.kr/openapi/에서 무료 등록 가능).
- **World Bank 데이터**: 서버가 제공하는 다른 도구는 국가 수준의 데이터만 반환하며, 서울시 같은 도시 수준의 데이터는 제공하지 않습니다.
- **도시 레벨 한국 인구 데이터**: 현재 이 서버에 서울시 같은 광역시 수준의 인구 시계열 데이터를 제공하는 도구가 없습니다.

### 근거로 쓴 응답 발췌

```
{"error":"tool_error","message":"KOSIS (Statistics Korea) requires an API key. Contact the operator about platform credentials, or BYO via ?_apiKey=<key> — free registration at https://kosis.kr/openapi/."}
```

```
"filter_gap":"geo: Seoul city asked, South Korea (country) served — no listed tool provides city-level Korean population"
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터는 어디서 받을 수 있는가"}` | 도구 매칭 실패(no_match), rc=1 |

### 답변

이 서버는 한국 공공데이터포털(data.go.kr)의 카탈로그를 색인하지 않아, 공공데이터포털 내에서 대기질 데이터의 위치를 안내할 수 없습니다.

**서버의 범위:**
- 이 Pipeworx-KOSIS 서버는 한국 통계청(KOSIS) 공식 통계와 한국은행(BOK) 경제 지표에 중점을 두고 있습니다.
- 공공데이터포털(data.go.kr) 자체의 오픈 API 카탈로그는 이 서버의 범위에 포함되지 않습니다.
- 대기질 데이터는 지역별로 환경부, 각 지역 환경청 등에서 제공하지만, 이 서버는 그 위치 정보를 가지고 있지 않습니다.

### 근거로 쓴 응답 발췌

```
"error":"no_match","filter_gap":"source: Korea 공공데이터포털 (data.go.kr) air-quality datasets — no listed tool indexes Korean government open-data catalogs"
```

```
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists."
```

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | kosis_search | `{"searchNm":"서울시 인구"}` | API 키 필요, rc=1 |
| 2 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했어?"}` | 해당 도구 없음, rc=1 |

### 답변

죄송하지만 이 서버는 서울시 인구 변화 데이터를 제공하지 못합니다. 

첫 번째 시도인 KOSIS(한국 통계청) 검색 도구는 API 키가 필요한데 제공되지 않아 호출할 수 없었습니다. 두 번째 시도인 범용 검색 도구(ask_pipeworx)는 "no listed tool covers non-US population statistics"라고 응답했으며, 한국 통계 데이터는 KOSIS 같은 한국 소스가 필요하지만 이 서버에서는 인증 없이 접근 불가하다고 명시했습니다.

### 근거로 쓴 응답 발췌

```
kosis_search 오류:
"message":"KOSIS (Statistics Korea) requires an API key. Contact the operator about platform credentials, or BYO via ?_apiKey=<key> — free registration at https://kosis.kr/openapi/."

ask_pipeworx 응답:
"filter_gap":"place: Seoul, South Korea — no listed tool covers non-US population statistics; a Korean source (e.g. KOSIS/Statistics Korea) would be needed"

"message":"That is a gap on our side rather than a statement about whether the information exists."

"Detail: The question asks how Seoul's population has changed over recent years, but every demographic tool listed covers only US geographies (census_population and housing_metro_demand are US Census ACS-based) and none accepts a South Korean city or any non-US place — no listed tool can retrieve Seoul population data."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?"}` | 해당 도구 없음, rc=1 |

### 답변

죄송하지만 이 서버는 공공데이터포털 관련 정보를 제공하지 못합니다.

ask_pipeworx 도구가 명시한 바로는, 한국의 공공데이터포털(공공데이터포털)에 대한 정보를 다루는 도구가 없으며, 외부 데이터 소스에 대한 위치 안내 질문도 지원하지 않는다고 했습니다. 서버의 도구 7,179개 중에서도 "한국 정부 데이터 포털 또는 '어디서 X를 받을 수 있는가'에 대한 안내를 하는 도구가 없다"고 명시했습니다.

### 근거로 쓴 응답 발췌

```
ask_pipeworx 응답:
"error":"no_match"

"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists."

"Detail: The question asks where to obtain air-quality data from Korea's Public Data Portal (공공데이터포털) — a request for guidance about an external data source, not a lookup of any published dataset the listed tools can retrieve. No available tool covers Korean government data portals or answers 'where do I get X' sourcing questions."
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "서울시 인구가 최근 몇 년간 어떻게 변했어?"}` | 한국 인구 통계 도구 미보유, rc=1 |
| 2 | kosis_search | `{"searchNm": "서울시 인구"}` | KOSIS API 키 필요, rc=1 |

### 답변

죄송하지만 이 서버로는 질문에 답할 수 없습니다.

**이유:**
- KOSIS 검색 도구들(`kosis_search` 등)은 한국통계청 API 키가 필수인데, 이 세션에서는 인증 정보가 없습니다.
- 범용 라우팅 도구(`ask_pipeworx`)는 한국 인구 통계 데이터를 담당하는 도구가 카탈로그에 없다고 응답했습니다. 이 서버의 도구 구성에 한국 인구 시계열 데이터가 포함되지 않은 상태입니다.

### 근거로 쓴 응답 발췌

```
ask_pipeworx 응답:
"filter_gap":"place: Seoul, South Korea — no tool in this pack provides Korean population statistics or a multi-year population time series for Seoul"
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it..."

kosis_search 응답:
"error":"tool_error","message":"KOSIS (Statistics Korea) requires an API key. Contact the operator about platform credentials, or BYO via ?_apiKey=<key> — free registration at https://kosis.kr/openapi/."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?"}` | 매칭 도구 없음, rc=1 |

### 답변

죄송하지만 이 서버로는 질문에 답할 수 없습니다.

**이유:**
이 서버(pipeworx-kosis-kr)는 KOSIS(한국통계청 국가통계포털)와 국제 통계·재무 데이터에 특화되어 있습니다. 공공데이터포털(data.go.kr) API의 대기질 데이터셋 위치나 사용법을 알려주는 도구가 이 서버에 없습니다.

공공데이터포털의 대기질 데이터는 일반적으로 환경부나 한국환경공단 관련 API로 제공되는데, 이 서버의 도구 범위 밖입니다.

### 근거로 쓴 응답 발췌

```
ask_pipeworx 응답:
"error":"no_match"
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates... were judged not to answer it."
```
