[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) [![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)

# Korean Data MCP — Measured Index

> We actually connect to every Korean data MCP server, measure it, and publish the numbers.

Other lists tell you a server exists. This one tells you whether it **works right now**. As of 2026-08-19, 25 of 55 (45%) did not respond.

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
| [공공데이터·행정](#공공데이터행정) | [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 사실오류 1건 — '1. 전국 권역별 (추천) — 국립환경과학원 환경영향평가 대기질정보(15142599)'  |
| [법령·판례](#법령판례) | [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 사실오류 1건 — '[재범(10년 내 2회 이상)]' — 도로교통법 제148조의2 제1항의 가중 요건은 '1 |
| [금융·증시](#금융증시) | [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 사실오류 5건 — 2026년 1분기 누적(연결) 매출액 1,338,734억원(약 133.9조원) / 영업이익 |
| [부동산](#부동산) | [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 사실오류 4건 — 평당 1.2만원대 유지 (실제 평당 12,095만원=약 1.21억원이며, 12개월간 10, |
| [커머스·생활](#커머스생활) | [ai.timeplex/booking](https://chat.timeplex.ai) | 이 분야 질문에 끝까지 답한 유일한 서버로 값도 원문과 축자 일치하나, 등록 매장이 1곳뿐이고 lang='k |

종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.

## 공공데이터·행정

> 실제로 쓸 만한 것은 haklaekim/public-data-lens 하나뿐이다 — 카탈로그형이라 인구 값은 못 주지만 '어디서 받나'라는 이 분야의 주력 질문에 데이터셋명·recordId·URL·형식·요금까지 붙은 실재 포인터를 냈고 발췌가 포털 실물과 축자 일치했다. 반면 다섯 서버 중 서울시 인구 시계열이라는 '값' 질문에 숫자를 한 개라도 공급한 서

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 9 | 23 | 42 | 100% | 100% | 1 |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp) | 7 | 222 | 549 | 100% | 100% | 3 |
| [app.apick/business](https://apick.app) | 16 | 39 | 41 | 100% | 100% | 0 |

1. public-data-lens — 사실오류 1건 — '1. 전국 권역별 (추천) — 국립환경과학원 환경영향평가 대기질정보(15142599)' — 이 데이터셋은  · 실제 값이 아니라 포털 메타데이터를 주는 카탈로그형이고 그 설계에 맞는 Q2에서는 실재·구체·검증 가능한 포인터를 냈다 — 다만 '서울시 인구' 같은 자명한 질의에 0건을 돌려주는 검색 재현율과 대표 데이터셋(에어코리아) 누락이
2. korea-public-data-catalog-mcp — 사실오류 3건 — '전국 대기오염배출시설 설치사업장 표준데이터 … 제공처: 공공데이터활용지원센터' — 포털 실물은 행정안전부( · 9만 6천 건 규모를 자처하는 카탈로그형이고 반환 포인터는 실재하지만, 서울→포항·대기질→배출시설 목록처럼 라우팅이 어긋나고 메타데이터 기술에 오기가 섞여 그대로 인용하면 사용자를 잘못 보낸다.
3. business — 상거래·물류 데이터형 서버로 이 분야 두 질문은 설계 범위 밖이며, 도구 목록을 근거로 정직하고 진단적으로 거절했다 — 사실 공급은 0건이다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>심사에 들지 못한 2건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [app.apick/all](https://apick.app) | 82 | 62 | 125 | 100% | 100% | — |
| [yousunjung84-edu/academyinfo-mcp](https://github.com/yousunjung84-edu/academyinfo-mcp) | 8 | 55 | **197** | 100% | 100% | — |

</details>

## 법령·판례

> 두 질문 모두에 현행 원문으로 답한 서버는 chrisryugj/korean-law-mcp 하나뿐이고(법제처 실시간 조회), app.sallim/contract-compass는 공공계약 안에서는 조문·금액이 더 정확하지만 코퍼스 38건 밖은 구조적으로 답이 없다.
나머지 둘은 답을 못 준다 — startup-law-mcp는 애초에 창업 법령 색인이라 범위 밖

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 222 | 311 | 100% | 100% | 1 |
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 54 | 77 | 100% | 100% | 0 |
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 13 | 127 | **3951** | 100% | 0% | 1 |

1. korean-law-mcp — 사실오류 1건 — '[재범(10년 내 2회 이상)]' — 도로교통법 제148조의2 제1항의 가중 요건은 '10년 내 2회 이상 · 법제처 실시간 조회로 두 질문 모두에 현행 원문을 대 준 유일한 서버이고 조문 번호·형량 수치가 실제와 맞았다 — 약점은 서버가 아니라 전달 형식에 있다(발췌가 조 전문의 앞머리에서 잘리고, 조회한 법령의 시행일을 함께 주지 않
2. contract-compass — 공공계약 도메인 안에서는 조문 대응·금액 수치가 현행법과 일치했고 코퍼스 밖은 이유를 밝힌 404로 환각을 차단했다 — 다만 근거 발췌가 조문 전문을 담지 않아 검증 가능성이 얇고, 코퍼스 밖 질의(search_law '도로교통법 음주운전')에 공공기관운영법 제53조의2를 1건 매칭해 돌려준 검색 소음은 오도 위험이다.
3. startup-law-mcp — 사실오류 1건 — '국가계약법(政府契約法)'이라는 한자 병기 — 국가계약법의 정식 명칭은 「국가를 당사자로 하는 계약에 관한  · 창업 지원 법령 전용 색인이라 이 분야 두 질문은 애초에 범위 밖이지만, 빈 결과와 오탐 히트를 원문으로 보여주며 거절해 '못 봄 ≠ 없음'을 정직하게 구분한 점은 이 분야 서버 중 가장 깔끔했다 — 다만 법령·판례 용도로는 쓸

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>심사에 들지 못한 1건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 223 | 301 | 76% | 0% | — |

</details>

## 금융·증시

> 두 질문을 다 감당할 서버는 없고, 실제로 쓰려면 갈라 써야 한다 — 시장 전체 스냅샷(시총 랭킹·주가)은 com.aikstockdata/mcp가 유일하게 실측 정합한 상위 10을 냈고(역산 주식수가 실제와 일치), 개별 기업 재무제표는 korea-stock-analyzer-mcp의 2025년 연결 매출 333.6조·영업이익 43.6조·마진 13.07%가 

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 45 | **182** | 100% | 100% | 5 |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 219 | 538 | 100% | 100% | 4 |
| [app.apick/finance](https://apick.app) | 3 | 29 | 30 | 100% | 100% | 0 |

1. mcp — 사실오류 5건 — 2026년 1분기 누적(연결) 매출액 1,338,734억원(약 133.9조원) / 영업이익 572,328억원 · 코스피 시총 랭킹은 이 분야에서 유일하게 실측 정합한 답을 냈지만, 정작 실적(DART) 계열 수치는 스케일이 무너져 있어 시세는 믿고 실적은 못 믿는 서버다.
2. korea-stock-analyzer-mcp — 사실오류 4건 — '삼성전자 시가총액 1조 5,697억 원' — 서버 원값 1,569,725,806,248,000원(1,569 · 개별 종목 재무제표는 이 분야에서 가장 정확했으나 시장 전체를 훑는 랭킹·스크리닝 도구가 없어 '상위 종목' 유형 질문에는 구조적으로 답하지 못한다.
3. finance — 이름만 finance일 뿐 실제로는 은행 계좌 검증(1원 인증·실명조회) 서비스로 한국 증시와 주제가 다르며, 그 사실을 흐리지 않고 두 번 다 명확히 거부한 점만이 평가할 지점이다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>심사에 들지 못한 1건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 12 | 31 | **184** | 100% | 0% | — |

</details>

## 부동산

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 두 질문에 실제로 값이 나온 서버는 app.sallim/korea-realty 하나뿐이다 — 월별 중앙값·거래건수·부분월·평당가와 유찰 물건 목록을 단위·기준시각·하자 경고와 함께 돌려주고, 재호출 대조에서 수치가 그대로 재현됐다. 나머지 둘은 각각 결제벽 뒤의 매매신호(seoul-apt-signal, 핵심 도구 3종 402·유료 미공시)와 분당 3회 제한

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 <sub>무료 37/47</sub> | 47 | 46 | 53 | 100% | 100% | 4 |
| [com.airblockfz/seoul-apt-signal](https://seoul-apt-signal.airblock2026.workers.dev) | 6 | 33 | 79 | 100% | 0% | 1 |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp) | 3 | 121 | **5484** | 100% | 0% | 1 |

1. korea-realty — 사실오류 4건 — 평당 1.2만원대 유지 (실제 평당 12,095만원=약 1.21억원이며, 12개월간 10,278→12,095 · 이 목록 운영사 서버이지만 같은 잣대로 봐도 두 질문 다 실제로 답이 나온 유일한 서버다 — 단위·집계법·기준시각·분산 경고·유찰 하자 경고를 원문이 스스로 달아 주고 재호출 대조에서 수치가 그대로 재현됐다. 감점은 서버 데이터
2. seoul-apt-signal — 사실오류 1건 — 강남구는 강한 매도(STRONG SELL) 신호를 보이고 있습니다 ... 이는 MOLIT(국토부) 공식 실거 · 사실상 유료 서버다 — evaluate_symbol·scan_bottoms·scan_tops가 모두 HTTP 402이고 무료로 열린 것은 마케팅 티저 pitch뿐인데 도구 목록에는 유료 여부가 공시돼 있지 않아(측정값 paid_
3. realestate-stats-mcp — 사실오류 1건 — 이는 서버의 통계표 목록에 해당 키워드를 포함한 표가 없다는 뜻이다 (검색 0건은 색인·매칭 실패일 수도 있 · 주제가 다른 서버다 — 한국부동산원 통계표(집계 지수) 검색기이지 개별 실거래·법원경매 원장이 아니며, 도구 3종에 분당 3회 제한이 걸려 있어 두 질문 모두 탐색 두세 번 만에 429로 막혀 커버리지 판정조차 못 하고 끝났다(

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

## 커머스·생활

> 다섯 중 이 분야 질문에 실제로 답할 수 있는 서버는 예약의 timeplex와 숙소의 arcasos 둘뿐이고, 나머지 셋(뉴스 API·SaaS 디렉토리·자사몰 결제 엔드포인트)은 서버 결함이 아니라 우리 카테고리 배정 오류다. 그리고 다섯 중 '많이 팔리는'을 답할 판매·인기 지표를 가진 서버는 하나도 없는데, 유일하게 없다고 말하지 않고 검색 결과를 인기

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [ai.timeplex/booking](https://chat.timeplex.ai) | 6 | 388 | **1245** | 100% | 100% | 0 |
| [com.arcasos/arcasos-rentals](https://mcp.arcasos.com) | 3 | 648 | 1099 | 100% | 0% | 2 |
| [com.saaskr/korean-saas-directory](https://saaskr.com) | 5 | 253 | 443 | 100% | 0% | 0 |

1. booking — 이 분야 질문에 끝까지 답한 유일한 서버로 값도 원문과 축자 일치하나, 등록 매장이 1곳뿐이고 lang='ko'로 응답하면서 메뉴명은 일본어 원문 그대로라(답변이 대신 번역했다) 서버가 약속한 번역이 실제로는 동작하지 않는다.
2. arcasos-rentals — 사실오류 2건 — 'ARCASOS에서 인기 많은 단기임차 상품은 서울과 부산의 교통 편리한 지역에 위치한 원룸, 펜트하우스,  · 숙소 재고는 실재하고 응답도 빠르지만, limit을 무시하고 항상 10건만 총계 없이 돌려주는 조용한 절단과 정렬 근거 미공시가 겹쳐 '인기'·'전체'를 묻는 질문에서 모델이 그럴듯하게 틀리도록 유도한다.
3. korean-saas-directory — 분야 밖 서버인데도 두 질문 모두 정직하게 처리했고, 특히 '전체 N개 중 M개'라는 절단 공시를 스스로 붙이는 점은 이 다섯 중 유일하다(첫 호출 17초 지연은 흠).

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>심사에 들지 못한 2건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [com.theprotoclinical/commerce](https://www.theprotoclinical.com) | 13 | 149 | 329 | 100% | 0% | — |
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 10 | 217 | 451 | 100% | 100% | — |

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
* **못 잰 것이 더 많다.** 후보 중 178건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다

---

생성 `render_readme.py` · 마지막 측정 2026-08-19 · 운영 [sallim-app](https://github.com/sallim-app)
