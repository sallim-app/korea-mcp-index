# io.github.pipeworx-io/ecos-kr

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/ecos-kr/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | discover_tools | `{"query":"서울시 인구 통계 최근 몇 년"}` | 8개 도구 발견(중국 주식·부동산·스웨덴 통계), 한국 인구 데이터 없음, rc=0 |
| 2 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했어?"}` | no_match 오류, 한국 인구 통계 도구 부재, rc=1 |

### 답변

이 서버는 한국 인구 통계 데이터를 제공하지 않습니다. 서버에 있는 도구들은 주로 한국은행 ECOS 경제 지표(환율, 금리, CPI, GDP 등), 미국 센서스 데이터, 중국 A주 주식, 스웨덴 통계청 데이터 등을 다루고 있으며, 한국의 인구 또는 인구 통계는 커버 범위에 없습니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"place: Seoul, South Korea — no tool in this pack provides Korean population statistics or a multi-year population time series for a non-US city"

"Detail: No listed tool covers Seoul or South Korean population data — census_population and housing_metro_demand are US-only (Census ACS), and the other tools cover China A-shares, Sweden, Norway, or US local datasets, so the question cannot be answered with the available tools."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?"}` | no_match 오류, 공공데이터포털 정보 도구 부재, rc=1 |

### 답변

이 서버는 공공데이터포털에 대한 정보 또는 데이터를 제공하지 않습니다. 서버에 있는 대기질 관련 도구들은 싱가포르 국립환경청(NEA), 네덜란드 RIVM, 미국 EPA, OpenAQ 같은 특정 지역의 측정소 데이터만 다루고 있으며, 한국의 공공데이터포털이나 한국 대기질 데이터 소스에 대한 정보는 제공하지 않습니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"source: Korea Public Data Portal (data.go.kr) air-quality datasets — no tool in this list queries that portal or provides source-discovery guidance"

"Detail: The question asks where to obtain air-quality data from Korea's Public Data Portal (공공데이터포털) — a request for guidance about a data source, not a lookup of published measurements. No listed tool covers the Korean portal or answers 'where to get data'; the air-quality tools here are region-specific retrieval endpoints (Singapore NEA, Netherlands RIVM, EPA AQS, OpenAQ nearest-station), none of which can express or answer this question."
```

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했나?"}` | no_match 에러, rc=0 |

### 답변

이 MCP 서버는 서울시 인구 데이터를 제공하지 않습니다. 서버가 응답한 바에 따르면, 이 서버의 도구들은 US 인구 통계(US Census ACS 기반)만 커버하며, 한국의 인구 데이터는 KOSIS 같은 한국 통계 출처에서 필요합니다.

서울시 인구 추이는 한국통계청의 KOSIS나 공공데이터포털에서 별도로 조회해야 합니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"place: Seoul, South Korea — no listed tool covers non-US population statistics; a Korean statistics source (e.g. KOSIS) would be needed"

"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists. It has been added to our demand log, which is what decides what we build or buy next. Detail: The question asks how Seoul's population has changed over recent years, but every demographic tool listed covers only US geographies (census_population and housing_metro_demand are US Census ACS-based), and no listed tool covers South Korean population data."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있나?"}` | no_match 에러 (웹 검색 질문), rc=0 |

### 답변

이 MCP 서버는 공공데이터포털(data.go.kr)의 데이터셋을 다루지 않습니다. 서버는 이 질문을 웹 검색 질문으로 분류했으며, 자신의 도구 범위가 SEC 공시, 경제 지표, FDA, 특허, 날씨, 시장 데이터 등 구조화된 라이브 데이터에 제한되어 있다고 설명했습니다. 

공공데이터포털의 대기질 데이터 위치는 이 서버가 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"source: 공공데이터포털 (data.go.kr) air-quality datasets — no tool in this pack covers the Korean public data portal; a web search or the portal's own catalog would be needed"

"message":"This is a web-search question, not a live-data question. Pipeworx is built to feed workflows and production systems with structured live data — SEC filings, economic series, FDA, patents, weather, markets, and thousands of other sources. Web search is a premium offering: paid accounts route questions like this through metered web search automatically — https://pipeworx.io/pricing. For a one-off, a general search engine or assistant is the right tool for this class of question."

"_hints":["If you meant a live-data question, rephrase towards a dataset or entity Pipeworx serves.","Paid accounts can answer web questions via serper_search — https://pipeworx.io/pricing."]
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했는지 시계열 데이터"}` | 일치 없음(no_match), rc=1 |
| 2 | discover_tools | `{"query":"한국 인구 통계 지역별"}` | 발견 결과 있음(8개 도구), rc=0 |

### 답변

이 MCP 서버는 서울시 인구 시계열 데이터를 제공하지 않습니다.

도구 검색 결과에 따르면, 이 서버의 패키지들은 주로 Bank of Korea의 경제지표(환율, 금리, CPI, GDP 등)를 다루고 있으며, 서울시 부동산 거래 데이터(seoul_real_estate)는 있지만 인구 통계는 없습니다. 한국의 인구 통계 데이터는 통계청의 KOSIS(한국통계정보시스템) 또는 서울시 공개데이터에서만 제공되는데, 이 MCP 서버에는 그 데이터원이 연결되어 있지 않습니다.

### 근거로 쓴 응답 발췌

```
"error":"no_match",
"filter_gap":"geo: Seoul population time series — no tool in this pack serves Korean demographic data; a KOSIS/Seoul open-data source would be required",
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists. It has been added to our demand log, which is what decides what we build or buy next. Detail: No listed tool covers Seoul (South Korea) population data — the only demographic tool, housing_metro_demand, is restricted to US metros via Census ACS, and no Korean statistics source (KOSIS/Seoul open data) is available.",

"tools":[...
{"name":"ecos_key_indicators","description":"Bank of Korea headline economic indicators: M1/M2 money supply, KRW/USD + KRW/JPY exchange rates, base interest rate, CPI, PPI, GDP growth, current account balance, household debt, unemployment, housing index — 101 series total"},
{"name":"ecos_search_tables","description":"Search Bank of Korea ECOS statistic tables — 800+ official Korean economic series across monetary policy, exchange rates, prices, balance of payments, GDP, real estate, household credit, etc."},
{"name":"ecos_series_items","description":"List the items (sub-series) within a Bank of Korea ECOS statistic table"},
{"name":"ecos_get_series","description":"Fetch a time series from Bank of Korea ECOS. Pass stat_code + cycle (A/Q/M/D) + start/end period"}
]
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털 대기질 에어코리아 데이터 API"}` | 선택됨(search_apis), 결과 20건 반환, rc=0 |

### 답변

이 MCP 서버는 한국 공공데이터포털의 대기질 데이터(에어코리아 API)에 대한 정보를 제공하지 않습니다.

도구가 실행한 결과는 APIs.guru 디렉토리에서 "air quality"로 검색한 일반적인 API 목록만 반환했으며, 여기에는 미국 EPA의 대기질 API는 포함되어 있지만 한국의 에어코리아나 공공데이터포털 대기질 데이터는 없습니다. 도구 응답의 설명에 명시된 대로, "APIs.guru는 주로 서구 상용 API를 색인화하며 한국 정부 API를 포함하지 않을 수 있으므로, 에어코리아 API는 data.go.kr(공공데이터포털)에서 직접 조회해야 합니다."

### 근거로 쓴 응답 발췌

```
"reasoning":"The question names a public API (Korea's AirKorea air-quality data API from the 공공데이터포털) rather than asking for a data value, so the API-directory search is the right discovery tool; no listed data tool connects to AirKorea specifically.",

"filter_gap":"provider: AirKorea / data.go.kr — APIs.guru indexes mostly Western commercial APIs and may not carry this Korean government API; if absent, the exact endpoint must be looked up on data.go.kr directly",

"filter_gap_note":"The result below is NOT filtered by: provider: AirKorea / data.go.kr — APIs.guru indexes mostly Western commercial APIs and may not carry this Korean government API; if absent, the exact endpoint must be looked up on data.go.kr directly. No listed tool could express every qualifier in the question at once, so this data is only filtered on the OTHER axis (see arguments_filled) — do not present it as if it also satisfies the qualifier named here. Check the actual returned records for that qualifier before answering, and state explicitly if none match.",

"arguments_filled":{"query":"air quality","limit":20}
```
