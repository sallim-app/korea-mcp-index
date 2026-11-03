# io.github.pipeworx-io/seoul-data

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://gateway.pipeworx.io/seoul-data/mcp`.


---

# 1회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "서울시 인구가 최근 몇 년간 어떻게 변했나"}` | 도구 부재로 응답 불가, rc=1 |
| 2 | seoul_dataset | `{"service": "SPOP_LOCAL_RESD_DONG", "start": 1, "end": 50}` | 동(동) 단위 인구 데이터 반환, rc=0 |

### 답변

이 서버의 pipeworx에서는 **한국 인구의 시계열 데이터를 제공하지 않습니다.** 

서버가 제공하는 seoul_dataset 도구로 조회한 데이터는 **2026년 7월 31일 기준** 서울의 동(동) 단위 거주 인구 수치인데, 시간 추이 데이터가 아니라 가장 최신 스냅샷입니다. 서울시 인구 변화 추이를 보려면 한국 통계청(KOSIS, Korea Statistics Information Service)의 시계열 데이터가 필요합니다만, 이 서버는 그 자료를 연결하지 않습니다.

예시: 조회된 종로구 내 일부 동들의 최신 인구: 종로1·2·3가동 14,305명, 종로4·5·6가동 10,824명 (2026년 7월 31일 기준).

### 근거로 쓴 응답 발췌

```
{"error":"no_match","filter_gap":"place/subject: Seoul population time series — no tool in this pack exposes Korean population data; a Korean statistics source (e.g. KOSIS) would be needed","filter_gap_note":"No tool was run. The router named a qualifier it could not satisfy: place/subject: Seoul population time series — no tool in this pack exposes Korean population data; a Korean statistics source (e.g. KOSIS) would be needed.
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "공공데이터포털 공기질 대기질 데이터 API 서비스"}` | 국제 공기질 API 목록 반환(한국 정보 포함 안 함), rc=0 |
| 2 | seoul_air_quality | `{}` | 서울 자치구 실시간 대기질 데이터, rc=0 |

### 답변

이 서버는 **공공데이터포털 대기질 데이터의 정확한 API 위치나 서비스명을 직접 제시하지 않습니다.**

다만, 서버의 seoul_air_quality 도구가 서울 대기질 데이터를 제공하고 있어서, 공공데이터포털(data.go.kr) 또는 서울 열린데이터 광장(data.seoul.go.kr)의 대기질 서비스를 통해 데이터에 접근할 수 있을 것으로 추정됩니다. 현재 측정 데이터로는 **PM-10, PM2.5, 오존, NO₂, CO, SO₂ 등의 오염물질과 종합 공기질 지수(CAI), 등급(좋음~나쁨)** 이 포함됩니다.

### 근거로 쓴 응답 발췌

```
{"count":5,"note":"Sample tier returns 5 of 25 districts (the full-key tier needs a Korean-ID Seoul membership).","districts":[{"district":"종로구","measured_at":"202611032200","air_index":"83","grade":"보통","dominant_pollutant":"PM-10","pm10":"71","pm25":"29","ozone":"0.004","no2":"0.048","co":"0.8","so2":"0.003"},{"district":"중구","measured_at":"202611032200","air_index":"85","grade":"보통","dominant_pollutant":"PM-10","pm10":"66","pm25":"31","ozone":"0.003","no2":"0.044","co":"0.7","so2":"0.003"}]}
```

---

# 2회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "서울시 인구가 최근 몇 년간 어떻게 변했는지 통계를 보여줘"}` | 한국 전국 인구 데이터 반환 (도시 수준 데이터 없음), rc=0 |
| 2 | seoul_dataset | `{"service": "인구"}` | 서버 오류 (500), rc=3 |

### 답변

죄송하지만 이 MCP 서버에서는 서울시 인구 통계를 제공할 수 없습니다. 

첫 번째 도구(`ask_pipeworx`)는 World Bank 데이터를 기반으로 **한국 전국 인구 통계만** 반환했습니다. 필터 갭에 따르면 "서울시 도시 수준의 인구 통계를 다루는 도구가 이 팩에 없다"고 명시되어 있습니다.

두 번째 도구(`seoul_dataset`)는 서울 공공데이터포털에 직접 접근하려 했으나 **서버 오류(500)**가 발생했습니다.

### 근거로 쓴 응답 발췌

```
"filter_gap":"geo: Seoul city asked, South Korea (country) served — no tool in this pack publishes municipal population for Korea; World Bank SP.POP.TOTL is country-level only"

"error":"tool_error","message":"Seoul Open Data (ERROR-500): 서버 오류입니다.\n지속적으로 발생시 열린 데이터 광장으로 문의(Q&A) 바랍니다."
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question": "공공데이터포털에서 대기질 데이터는 어디서 받을 수 있나? 관련 서비스나 데이터셋 정보를 알려줘"}` | 매칭 실패 (범위 밖), rc=1 |

### 답변

죄송하지만 이 MCP 서버는 **공공데이터포털(data.go.kr)의 대기질 데이터셋 카탈로그 정보를 제공하지 않습니다**.

도구가 반환한 오류에 따르면:
- 공공데이터포털을 인덱싱하는 도구가 없습니다
- 서버에 있는 대기질 도구들(`air_quality_pm25`, `open_meteo_air_quality`, `airquality_get_forecast`)은 실시간 측정값·예보만 제공하며, 포탈의 데이터셋 카탈로그는 다루지 않습니다
- 가장 비슷한 카탈로그 도구(`dados_pt_search_datasets`)는 포르투갈 포탈 전용입니다

### 근거로 쓴 응답 발췌

```
"filter_gap":"portal: 공공데이터포털 (data.go.kr) — no listed tool indexes the Korean open-data portal; the closest catalog tool (dados_pt_search_datasets) is Portugal-only and would return unrelated datasets"

"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it."

"The question asks where to obtain air-quality datasets/services on 공공데이터포털 (Korea's data.go.kr national open-data portal) — a catalog lookup on a specific national portal. No listed tool covers Korea..."
```

---

# 3회차

## 질문 1: 서울시 인구가 최근 몇 년간 어떻게 변했어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"서울시 인구가 최근 몇 년간 어떻게 변했는가? 연도별 인구 통계를 보여줘"}` | 서울시 데이터 없음, 대한민국 전체 인구 통계 반환, rc=0 |

### 답변

죄송하지만, 이 서버는 **서울시 수준의 지역별 인구 통계를 제공하지 않습니다**. 

도구가 반환한 데이터는 대한민국 **전국 인구**로, 서울시만의 수치가 아닙니다. 도구의 분석에 따르면 "city-level population series tool이 없어 country-level 데이터만 제공 가능"하다고 합니다.

대한민국 전체 인구는 2015년 5,101만 명에서 2024년 5,175만 명으로 소폭 증가했으나, 서울시 인구의 개별 추이는 이 서버에서 조회 불가합니다.

### 근거로 쓴 응답 발췌

```
{"filter_gap":"geo: Seoul city asked, South Korea (country) served — no city-level population series tool exists in this pack; the returned series is national, not Seoul-specific","filter_gap_note":"The result below is NOT filtered by: geo: Seoul city asked, South Korea (country) served — no city-level population series tool exists in this pack; the returned series is national, not Seoul-specific."}

{"country":"Korea, Rep.","country_id":"KR","indicator_id":"SP.POP.TOTL","indicator_name":"Population, total","date_range":"2015:2024","total_records":10,"last_updated":"2026-10-08","data":[{"year":"2024","value":51751065},{"year":"2023","value":51712619},{"year":"2022","value":51672569},{"year":"2021","value":51769539},{"year":"2020","value":51836239},{"year":"2019","value":51764822},{"year":"2018","value":51585058},{"year":"2017","value":51361911},{"year":"2016","value":51217803},{"year":"2015","value":51014947}]}
```

---

## 질문 2: 공공데이터포털에서 대기질 데이터를 어디서 받을 수 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | ask_pipeworx | `{"question":"공공데이터포털(Seoul Open Data Plaza)에서 대기질 데이터를 어디서 받을 수 있나? 데이터셋 이름이나 서비스명을 알려줘"}` | 질문 매칭 실패, rc=0 |

### 답변

죄송합니다. **이 서버는 한국 공공데이터포털(공공데이터포털/Seoul Open Data Plaza)의 데이터셋을 검색할 수 있는 도구가 없습니다.**

서버의 응답에 따르면, 지원하는 공개데이터 포털은 NYC, Seattle, Bloomington, Santa Clara, Orlando, 포르투갈(dados.pt) 등이며, 한국의 공공데이터포털은 지원 범위 밖입니다. 

공공데이터포털의 대기질 데이터 위치나 서비스명은 이 MCP 서버에서 조회 불가능합니다.

### 근거로 쓴 응답 발췌

```
{"error":"no_match","filter_gap":"source: Seoul Open Data Plaza / data.go.kr air-quality datasets — no Korean open-data catalogue or query tool is available in this toolset"}

{"message":"Sorry — we could not match that question to a source. Either no tool in our live-data catalog covers it, or the closest candidates (under did_you_mean — call one directly if it fits) were judged not to answer it. That is a gap on our side rather than a statement about whether the information exists. ... The question asks about Seoul/Korean open-data portals (공공데이터포털 / Seoul Open Data Plaza) for air-quality datasets, but every listed tool covers other jurisdictions (NYC, Seattle, Bloomington, Santa Clara, Orlando, Portugal, Ofgem) or company profiles — none can search or query Korean open data, so no tool fits."}
```
