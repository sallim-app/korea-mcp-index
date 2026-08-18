[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) [![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)

# Korean Data MCP — Measured Index

> We actually connect to every Korean data MCP server, measure it, and publish the numbers.

Other lists tell you a server exists. This one tells you whether it **works right now**. As of 2026-08-18, 25 of 55 (45%) did not respond.

| | |
|---|---|
| 응답하는 서버 | **28**건 |
| 응답 없음 | 25건 → [DOWN.md](DOWN.md) |
| 주제 밖(데이터 제공형 아님) | 2건 |

* [왜 만드나](#왜-만드나)
* [한눈에](#한눈에)
* [표기](#표기)
* [공공데이터·행정](#공공데이터행정)
* [법령·판례](#법령판례)
* [금융·증시](#금융증시)
* [부동산](#부동산)
* [커머스·생활](#커머스생활)
* [기타](#기타)
* [우리 목록에 넣으려면](#우리-목록에-넣으려면)
* [어떻게 재나](#어떻게-재나)
* [믿으면 안 되는 부분](#믿으면-안-되는-부분)

## 왜 만드나

**AI가 좋은 MCP를 못 찾는다.** 한국 MCP 스토어들은 대부분 AI가 읽을 수 없다 — 화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. 정작 MCP는 AI가 쓰라고 만든 것인데.

그래서 이 목록은 **AI가 읽을 수 있게** 만든다. JS도 로그인도 차단도 없는 마크다운과 JSON이다. 그리고 **있다고 말하지 않고 두드려 본다** — 등록은 가동의 증거가 아니다.

**우리 것만 싣지 않는다.** 남의 MCP가 더 나으면 더 낫다고 쓴다. 이 목록의 운영자(🏠 표시)도 같은 표에서 같은 잣대로 잰다.

## 한눈에

종합 점수는 매기지 않는다 — 가중치를 우리가 정하면, 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없다. 대신 **축마다 1위**를 적는다.

| 축 | 1위 | 값 |
|---|---|---|
| 도구가 가장 많다 | [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125종 |
| 가장 빠르다(웜) | [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 23ms |
| 설명이 가장 충실하다 | [com.arcasos/arcasos-rentals](https://mcp.arcasos.com) | 중앙 652자 |
| 키 없이 바로 된다 | 22/28건 | 가입·키 불필요 |

## 표기

* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다
* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다
* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. **둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다
* **키** — 🔑 이면 도구 목록을 보는 데도 키가 필요하다
* **무료/전체** — 서버가 스스로 공시할 때만 채운다. `—`는 “무료”가 아니라 **확인 못 했다**는 뜻이다
* 🏠 — 이 목록의 운영자가 만든 서버

## 공공데이터·행정

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [app.apick/all](https://apick.app) | 82 | 64 | 128 | 100% | 100% | — | — |
| [app.apick/business](https://apick.app) | 16 | 35 | 47 | 100% | 100% | — | — |
| [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 9 | 23 | 28 | 100% | 100% | — | — |

<details><summary>나머지 3건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [yousunjung84-edu/academyinfo-mcp](https://github.com/yousunjung84-edu/academyinfo-mcp) | 8 | 137 | 236 | 100% | 100% | — | — |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp) | 7 | 218 | 550 | 100% | 100% | — | — |
| [seolcoding/korean-stat-mcp](https://github.com/seolcoding/korean-stat-mcp) | — | — | 964 | —% | —% | 🔑 | — |

</details>

## 법령·판례

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 213 | 292 | 76% | 0% | — | — |
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 13 | 128 | **4140** | 100% | 0% | — | — |
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 36 | **140** | 100% | 100% | — | — |

<details><summary>나머지 1건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 209 | 279 | 100% | 100% | — | — |

</details>

## 금융·증시

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 25 | 68 | 100% | 100% | — | — |
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 12 | 29 | **243** | 100% | 0% | — | — |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 220 | 547 | 100% | 100% | — | — |

<details><summary>나머지 2건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [app.apick/finance](https://apick.app) | 3 | 32 | 33 | 100% | 100% | — | — |
| [MarcoYou/open-proxy-mcp](https://github.com/MarcoYou/open-proxy-mcp) | — | — | 911 | —% | —% | 🔑 | — |

</details>

## 부동산

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 47 | 45 | **138** | 100% | 100% | — | 37/47 |
| [com.airblockfz/seoul-apt-signal](https://seoul-apt-signal.airblock2026.workers.dev) | 6 | 26 | 54 | 100% | 0% | — | — |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp) | 3 | 125 | **5226** | 100% | 0% | — | — |

## 커머스·생활

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [com.theprotoclinical/commerce](https://www.theprotoclinical.com) | 13 | 147 | 197 | 100% | 0% | — | — |
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 10 | 202 | 386 | 100% | 100% | — | — |
| [ai.timeplex/booking](https://chat.timeplex.ai) | 6 | 455 | 1182 | 100% | 100% | — | — |

<details><summary>나머지 6건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [com.saaskr/korean-saas-directory](https://saaskr.com) | 5 | 254 | 664 | 100% | 0% | — | — |
| [com.arcasos/arcasos-rentals](https://mcp.arcasos.com) | 3 | 660 | 1704 | 100% | 0% | — | — |
| [io.github.accentist/buyking-mcp](https://github.com/accentist/buyking-mcp) | — | 26 | 77 | —% | —% | — | — |
| [com.beauticslab/mcp](https://github.com/websfactory/beauticslab-mcp) | — | — | 167 | —% | —% | 🔑 | — |
| [com.empresskorea/kbeauty-agent-commons](https://empresskorea.com) | — | — | 299 | —% | —% | 🔑 | — |
| [jeonghwanko/coffee-price-mcp](https://github.com/jeonghwanko/coffee-price-mcp) | — | — | 327 | —% | —% | 🔑 | — |

</details>

## 기타

| Server | Tools | Warm | Cold | Desc | Annot | Key | Free/All |
|---|---|---|---|---|---|---|---|
| [com.boltena/erp](https://app.boltena.com) | — | — | 148 | —% | —% | 🔑 | — |

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
* **못 잰 것이 더 많다.** 후보 중 178건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다

---

생성 `render_readme.py` · 마지막 측정 2026-08-18 · 운영 [sallim-app](https://github.com/sallim-app)
