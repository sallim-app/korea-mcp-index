[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) [![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)

# 한국 데이터 MCP — 실측 목록

> 한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 “있다”를 말한다. 이 목록은 **지금 되냐**를 잰다. 2026-08-18 기준 주소를 확인한 55건 중 **25건(45%)이 응답하지 않았다**.

| | |
|---|---|
| 비교 가능한 서버 | **21**건 |
| 응답했으나 못 잼(키 필요·규격 이탈) | 7건 |
| 응답 없음 | 25건 → [DOWN.md](DOWN.md) |
| 주제 밖(데이터 제공형 아님) | 2건 |

* [왜 만드나](#왜-만드나)
* [한눈에](#한눈에)
* [공공데이터·행정](#공공데이터행정)
* [법령·판례](#법령판례)
* [금융·증시](#금융증시)
* [부동산](#부동산)
* [커머스·생활](#커머스생활)
* [표기](#표기)
* [측정 못 함](#측정-못-함)
* [우리 목록에 넣으려면](#우리-목록에-넣으려면)
* [어떻게 재나](#어떻게-재나)
* [믿으면 안 되는 부분](#믿으면-안-되는-부분)

## 왜 만드나

**AI가 좋은 MCP를 못 찾는다.** 한국 MCP 스토어들은 대부분 AI가 읽을 수 없다 — 화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. 정작 MCP는 AI가 쓰라고 만든 것인데.

그래서 이 목록은 **AI가 읽을 수 있게** 만든다. JS도 로그인도 차단도 없는 마크다운과 JSON이다. 그리고 **있다고 말하지 않고 두드려 본다** — 등록은 가동의 증거가 아니다.

**우리 것만 싣지 않는다.** 남의 MCP가 더 나으면 더 낫다고 쓴다. 이 목록의 운영자(🏠 표시)도 같은 표에서 같은 잣대로 잰다.

## 한눈에

분야마다 1위 하나씩. 순서는 아래 각 분야의 심사 결과와 **같은 값에서 나온다** — 여기와 본문이 어긋날 수 없다.

| 분야 | 1위 | 왜 |
|---|---|---|
| [공공데이터·행정](#공공데이터행정) | [app.apick/business](https://apick.app) | 사업자등록·기업정보·택배·검증의 핵심 질문을 직결, 응답 최고속(1.34배), 스키마 94%, 설명 명확 |
| [법령·판례](#법령판례) | [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 법령·판례·조례를 폭넓게 다루며 100% 설명·스키마·주석으로 AI가 도구 용도를 명확히 구분 가능, 성능  |
| [금융·증시](#금융증시) | [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | KOSPI/KOSDAQ 시세 + DART 공시는 한국 증시의 정수; 25ms 콜드·370자 상세설명·주석 1 |
| [부동산](#부동산) | [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 47개 도구로 법원경매·실거래 기록·시세 예측 등 부동산 핵심 질문 모두 커버, 설명·스키마·주석 100%  |
| [커머스·생활](#커머스생활) | [ai.timeplex/booking](https://chat.timeplex.ai) | 뷰티·웰니스 예약은 실제로 자주 쓰는 생활 서비스. 완벽한 주석(100%)과 충분한 설명(268자), 빠른  |

종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.

## 공공데이터·행정 (Public Data)

> 도구 수 경쟁이 아니라 AI 발견성·실제 질문 커버·응답속이 핵심 — S2(집중)·S1(폭)·S3(게이트웨이) 삼각형 구성이 도메인 최적

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [app.apick/business](https://apick.app) | 16 | 35 | 47 | 100% | 100% |
| [app.apick/all](https://apick.app) | 82 | 64 | 128 | 100% | 100% |
| [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 9 | 23 | 28 | 100% | 100% |

1. business — 사업자등록·기업정보·택배·검증의 핵심 질문을 직결, 응답 최고속(1.34배), 스키마 94%, 설명 명확
2. all — 공공데이터 전역 커버(82개 도구: 사업자등록·택배·OCR·검색), 설명 품질 우수(중앙 176자), 스키마 98%
3. public-data-lens — AI가 공공데이터를 판단·라우팅하도록 설계된 전문 레이어(AIRD 표준), 설명 최상(225자로 '언제' 명확), 1.22배 응답속

<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 [JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>

<details><summary>심사에 들지 못한 2건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [yousunjung84-edu/academyinfo-mcp](https://github.com/yousunjung84-edu/academyinfo-mcp) | 8 | 137 | 236 | 100% | 100% |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp) | 7 | 218 | 550 | 100% | 100% |

</details>

## 법령·판례 (Law)

> S1은 창업법 특화로 도메인 통합 불가, 콜드 4140ms 성능 문제로 제외

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 209 | 279 | 100% | 100% |
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 36 | **140** | 100% | 100% |
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 213 | 292 | 76% | 0% |

1. korean-law-mcp — 법령·판례·조례를 폭넓게 다루며 100% 설명·스키마·주석으로 AI가 도구 용도를 명확히 구분 가능, 성능 안정적(콜드 1.3배)
2. contract-compass — 최상의 문서화(584자 중앙)와 최고 성능(콜드 140ms)이나 공공조달 전문이라 일반 법령 도메인 한정
3. korean-law-alio-mcp — 1,600법률·판례 수만건 광범위하지만 125개 도구를 42자 설명으로는 AI가 어느 도구를 쓸지 구분 불가능

<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 [JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>

<details><summary>심사에 들지 못한 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 13 | 128 | **4140** | 100% | 0% |

</details>

## 금융·증시 (Finance)

> 증시 데이터는 S4-S2 이원화(시세·공시); S1은 크립토 미디어로 범주 밖, 주석 0%라 LLM이 도구에 접근 불가

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 25 | 68 | 100% | 100% |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 220 | 547 | 100% | 100% |
| [app.apick/finance](https://apick.app) | 3 | 32 | 33 | 100% | 100% |

1. mcp — KOSPI/KOSDAQ 시세 + DART 공시는 한국 증시의 정수; 25ms 콜드·370자 상세설명·주석 100% = 모델이 실제 사용 가능
2. korea-stock-analyzer-mcp — KRX + DART 공시로 S4와 동일한 핵심 커버, 287자 설명·주석 100% 보장; 느림(547ms 콜드)이 유일한 약점
3. finance — 은행계정검증은 증시 외면이나 금융권이고, 33ms 속도·주석 100%로 모델이 사용 가능; S1의 주석 무(0%)는 12도구를 죽인다

<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 [JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>

<details><summary>심사에 들지 못한 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 12 | 29 | **243** | 100% | 0% |

</details>

## 부동산 (Real Estate)

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> S1의 포괄성·완성도·속도 삼박자가 우월하고, S3의 극도의 콜드 펼티(5+초)는 모바일 환경에서 치명적이라 실무 사용성 최악

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 <sub>무료 37/47</sub> | 47 | 45 | **138** | 100% | 100% |
| [com.airblockfz/seoul-apt-signal](https://seoul-apt-signal.airblock2026.workers.dev) | 6 | 26 | 54 | 100% | 0% |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp) | 3 | 125 | **5226** | 100% | 0% |

1. korea-realty — 47개 도구로 법원경매·실거래 기록·시세 예측 등 부동산 핵심 질문 모두 커버, 설명·스키마·주석 100% 완성으로 모델이 용도를 명확히 판단 가능, 45ms 웜 지연으로 실시간 답변에 적합
2. seoul-apt-signal — 6개 도구로 서울 25개 구 공식 거래·신호 제공하는 전문 도구, 26ms 최고속 응답, 설명·스키마 완성도 높음 (주석 0%는 단점이나 도구 수가 적어 보충)
3. realestate-stats-mcp — 한국부동산원 공식 시세·거래현황의 권위 있는 데이터지만, 콜드 5226ms 초과로 실시간 사용 실패, 설명 222자 최소로 도구 이해도 최악, 3개 도구 한정으로 보조용만 가능

<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 [JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>

## 커머스·생활 (Commerce)

> 생활 예약·숙소·쇼핑이 이 카테고리의 중심인데 상위 3곳이 담아냈다. S3는 뉴스로 상거래 아님. S4는 설명 49자는 너무 짧고 주석도 없어 모델이 쓸 때를 판단 불가.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [ai.timeplex/booking](https://chat.timeplex.ai) | 6 | 455 | 1182 | 100% | 100% |
| [com.theprotoclinical/commerce](https://www.theprotoclinical.com) | 13 | 147 | 197 | 100% | 0% |
| [com.arcasos/arcasos-rentals](https://mcp.arcasos.com) | 3 | 660 | 1704 | 100% | 0% |

1. booking — 뷰티·웰니스 예약은 실제로 자주 쓰는 생활 서비스. 완벽한 주석(100%)과 충분한 설명(268자), 빠른 응답(455ms warm)으로 모델 이해도 높음.
2. commerce — 가장 빠른 성능(147ms warm/197ms cold)과 가장 많은 도구(13개), 충분한 설명(489자)으로 실행 가능. K-뷰티 쇼핑은 실제 상거래 수요.
3. arcasos-rentals — 단기숙소는 실제로 많이 찾는 서비스. 가장 상세한 설명(652자)이 모델의 도구 활용도를 높이나, 1704ms 콜드 지연과 0% 주석이 실사용 포기를 초래할 수 있음.

<sub>순위는 이름을 가린 채 심사한 결과다. 기준·입력·이유 전문은 [JUDGING.md](JUDGING.md)·[ranking.json](ranking.json).</sub>

<details><summary>심사에 들지 못한 2건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 |
|---|---|---|---|---|---|
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 10 | 202 | 386 | 100% | 100% |
| [com.saaskr/korean-saas-directory](https://saaskr.com) | 5 | 254 | 664 | 100% | 0% |

</details>

## 표기

* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다
* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다
* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. **둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다
* 이름 옆 <sub>무료 N/M</sub> — 서버가 유료 게이트를 **스스로 공시**할 때만 붙는다. 없다고 무료라는 뜻이 아니다 — 밖에서는 판정할 수 없다
* 🏠 — 이 목록의 운영자가 만든 서버

## 측정 못 함

응답은 했지만 **비교할 값을 얻지 못한 7건.** 지우지 않고 여기 둔다 — “없다”가 아니라 **“우리가 못 봤다”**이기 때문이다. 대부분 도구 목록을 보는 데도 키를 요구한다. 키가 있으면 잘 도는 서버일 수 있다.

| 서버 | 증상 |
|---|---|
| [MarcoYou/open-proxy-mcp](https://github.com/MarcoYou/open-proxy-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.beauticslab/mcp](https://github.com/websfactory/beauticslab-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.boltena/erp](https://app.boltena.com) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.empresskorea/kbeauty-agent-commons](https://empresskorea.com) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.accentist/buyking-mcp](https://github.com/accentist/buyking-mcp) | 200이지만 tools/list 응답을 못 읽었다 — 규격 이탈 의심 |
| [jeonghwanko/coffee-price-mcp](https://github.com/jeonghwanko/coffee-price-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [seolcoding/korean-stat-mcp](https://github.com/seolcoding/korean-stat-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |

## 우리 목록에 넣으려면

**우리에게 올릴 필요가 없다.** [공식 MCP 레지스트리](https://registry.modelcontextprotocol.io)에 등록하면 다음 회차에 자동으로 들어온다. 그쪽이 나은 이유는 우리만 읽는 게 아니라서다.

이미 등록했는데 여기 없다면 **우리 수집기의 버그일 수 있다** — 이슈로 알려 달라. 경쟁 서비스여도 받는다.

제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 그래서 심사할 것이 없다.

## 어떻게 재나

```
collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API
filter   한국 관련성(한글·.go.kr·기관명) → 후보 좁히기
enrich   README에서 엔드포인트·패키지·기관 도메인 추출
classify 분야·데이터제공형 판정 (LLM, 결과는 classification.json에 고정)
measure  tools/list 실호출 — 가동·도구수·지연·설명·주석
render   이 문서
```

서버당 `tools/list` 3회(콜드 1 + 웜 2), 사이에 간격을 두고, User-Agent로 우리를 밝힌다. 원자료는 [measured.json](measured.json)·[candidates.json](candidates.json)에 있다. **돌리면 같은 표가 나온다** — 우리가 1위여도 직접 재서 반박할 수 있다.

## 믿으면 안 되는 부분

* **데이터가 정확한지는 재지 않는다.** 우리는 부동산·공공계약은 정답을 알지만 의료·교통은 모른다. 모르면서 점수를 매기면 우리가 경계하는 그것을 우리가 하게 된다
* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다
* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다
* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다
* **못 잰 것이 더 많다.** 후보 중 175건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다

---

생성 `render_readme.py` · 마지막 측정 2026-08-18 · 운영 [sallim-app](https://github.com/sallim-app)
