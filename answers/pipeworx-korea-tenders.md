# io.github.pipeworx-io/korea-tenders

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/korea-tenders/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_population | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했는지"}` | 한국 전체 인구 2015-2024년 시계열 데이터, rc=0 |

### 답변

죄송합니다만, Pipeworx 서버는 **서울시 수준의 인구 데이터는 제공하지 않습니다**. 대신 한국 전체 국가 수준의 인구 추세만 조회할 수 있습니다.

반환된 데이터는 한국 전체 인구입니다:
- 2024년: 51,751,065명
- 2023년: 51,712,619명
- 2022년: 51,672,569명
- 2021년: 51,769,539명
- 2020년: 51,836,239명

최근 몇 년간 한국 전체 인구는 **감소세**를 보이고 있으며, 특히 2020년(51.8백만) 이후 지속적으로 감소하는 추세입니다.

**서울시의 인구 변화를 조회하려면**: 이 서버는 서울시 같은 도시별 인구 데이터를 가지고 있지 않으며, 이를 위해서는 통계청이나 서울시청의 인구 통계가 필요합니다.

### 근거로 쓴 응답 발췌

```
"reasoning":"No listed tool returns Seoul city-level population; the only population time series that can run is the World Bank country series, which gives South Korea's year-by-year population trend (default 2015–2024) — the closest available proxy for a multi-year trend question."
"filter_gap":"geo: Seoul city asked, South Korea country-level served — no city/metro population series tool exists in this pack (census_population is US-only, ecos_key_indicators has no population series)"
{"country":"Korea, Rep.","country_id":"KR","indicator_name":"Population, total","date_range":"2015:2024","total_records":10,"data":[{"year":"2024","value":51751065},{"year":"2023","value":51712619},{"year":"2022","value":51672569},{"year":"2021","value":51769539},{"year":"2020","value":51836239},{"year":"2019","value":51764822},{"year":"2018","value":51585058},{"year":"2017","value":51361911},{"year":"2016","value":51217803},{"year":"2015","value":51014947}]}
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있나"}` | 웹 검색 질문으로 분류, 이 서버는 카탈로그 조회 미지원, rc=0 |

### 답변

죄송합니다만, **Pipeworx 서버는 공공데이터포털 카탈로그를 인덱싱하지 않으며, 이 질문에 답할 수 없습니다**.

Pipeworx는 SEC 공시, 경제 통계, FDA 데이터, 특허, 기상, 시장 정보 같은 **구조화된 라이브 데이터**를 제공하는 도구입니다. 특정 포털의 데이터셋 위치를 찾는 것은 **웹 검색**이 필요한 작업이며, Pipeworx에서는 웹 검색이 유료 계정에서만 지원됩니다.

**대기질 데이터를 찾으려면:**
- 공공데이터포털(data.go.kr)에 직접 방문해 검색하거나
- 환경부의 에어코리아(www.airkorea.or.kr) 같은 공식 채널을 이용해야 합니다.

### 근거로 쓴 응답 발췌

```
"error":"no_match"
"triage":"web_search_question"
"filter_gap":"source: Korea Public Data Portal (data.go.kr) air-quality dataset location — no listed tool indexes that portal; a web search or the portal's own catalog would be needed"
"message":"This is a web-search question, not a live-data question. Pipeworx is built to feed workflows and production systems with structured live data — SEC filings, economic series, FDA, patents, weather, markets, and thousands of other sources. Web search is a premium offering: paid accounts route questions like this through metered web search automatically"
```

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"서울시 인구 추이 최근 5년"}` | World Bank 국가 전체 인구 데이터만 반환, 서울시 데이터 없음, rc=0 |

### 답변

이 서버는 서울시 단위의 인구 통계를 제공하지 않습니다.

World Bank의 데이터로는 **한국 전체 인구** 추이만 조회할 수 있었습니다. 최근 5년(2020-2024) 한국 인구:
- 2024년: 51,751,065명
- 2023년: 51,712,619명
- 2022년: 51,672,569명
- 2021년: 51,769,539명
- 2020년: 51,836,239명

서울시 인구의 연도별 변화를 알려면 한국 통계청(KOSTAT)의 인구통계나 서울시 관련 공식 통계를 찾아야 합니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"geo: Seoul (city) asked, South Korea (country) served — no city-level population time-series tool exists in this pack"
"reasoning":"No listed tool returns a city-level population time series for Seoul; the only population trend series available is World Bank annual total population, so the country-level series for South Korea (KR) is the closest runnable source for a multi-year trend."
"data":[{"year":"2024","value":51751065},{"year":"2023","value":51712619},{"year":"2022","value":51672569},{"year":"2021","value":51769539},{"year":"2020","value":51836239},{"year":"2019","value":51764822},{"year":"2018","value":51585058},{"year":"2017","value":51361911},{"year":"2016","value":51217803},{"year":"2015","value":51014947}]
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털 data.go.kr에서 대기질 공기질 데이터를 어디서 받을 수 있는가?"}` | 도구 매칭 실패, data.go.kr 색인 없음, rc=1 |

### 답변

이 서버는 한국 공공데이터포털(data.go.kr)을 제공하지 않습니다.

서버는 명시적으로 "No available tool queries data.go.kr or the Korean public data portal"이라고 답했습니다. 서버에 있는 대기질 도구는 싱가포르(NEA), 네덜란드(RIVM), 미국(EPA), OpenWeather 등 다른 국가의 데이터만 다룹니다.

현재 이 MCP 서버에는 한국 공공데이터포털(data.go.kr)의 대기질 데이터에 접근할 도구가 없으므로, 대기질 데이터의 정확한 위치를 알려 드릴 수 없습니다. 공공데이터포털의 카탈로그를 직접 검색하거나 환경부 에어코리아(airkorea.or.kr) 등을 통해 확인하시기를 권장합니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"source: data.go.kr (Korea public data portal) — no listed tool indexes or searches this portal; a data.go.kr catalog/search tool would be needed to answer"
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists."
"logged_to_demand":true
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했어?"}` | 도구 매칭 실패 — 한국 인구 데이터 없음, rc=1 |

### 답변

죄송하지만 이 서버는 서울시 인구 변화 데이터를 제공하지 않습니다. 

이 서버(pipeworx-korea-tenders)가 다루는 도구는 주로 미국의 SEC 재무 정보, 경제통계, FDA 데이터 등 영어권 공개 데이터에 특화되어 있습니다. 한국의 인구통계는 통계청(KOSIS)이 정본인데, 이 서버의 팩에는 한국 통계 데이터를 인덱싱하는 도구가 없습니다.

서울시 인구 추이를 알려면 통계청 KOSIS(https://kosis.kr) 또는 서울시청 통계 사이트를 직접 확인하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"place: Seoul, South Korea — no tool in this pack serves non-US population data; a Korean statistics source (e.g. KOSIS) would be needed"
"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists. Has been added to our demand log, which is what decides what we build or buy next. Detail: No listed tool covers Seoul or South Korean population data — census_population and housing_metro_demand are US-only (Census ACS), and no Korean statistics source is available."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?"}` | 도구 매칭 실패 — 한국 공공데이터포털 인덱싱 없음, rc=1 |

### 답변

죄송하지만 이 서버는 한국 공공데이터포털의 대기질 데이터 위치를 직접 제공하지 못합니다.

이 서버에 있는 대기질 관련 도구들은 싱가포르, 네덜란드, 미국 EPA, OpenAQ 같이 특정 지역만 다루며, 한국 정부의 공개데이터포털(data.go.kr)을 인덱싱하는 도구는 없습니다. 

한국의 대기질 데이터는 공공데이터포털(data.go.kr)에서 환경부·대기환경정보 관련 데이터셋을 직접 검색하거나, 환경부 에어코리아(www.airkorea.or.kr)를 방문하시는 것이 정확합니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"source: Korea Public Data Portal (data.go.kr) — no listed tool indexes Korean government open data; the available air-quality tools are region-specific (Singapore, Netherlands, US EPA, OpenAQ) and can"
"message":"This is a web-search question, not a live-data question. Pipeworx is built to feed workflows and production systems with structured live data — SEC filings, economic series, FDA, patents, weather, markets, and thousands of other sources. Web search is a premium offering: paid accounts route questions like this through metered web search automatically — https://pipeworx.io/pricing. For a one-off, a general search engine or assistant is the right tool for this class of question."
```
