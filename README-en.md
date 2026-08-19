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
| 설치형(원격 주소 없음) | 배포 확인 **54**건 · 배포판 없음 68건 · 이름을 못 읽어 미측정 28건 |

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
* [고쳤다면 다시 잰다](#고쳤다면-다시-잰다)
* [어떻게 재나](#어떻게-재나)
* [믿으면 안 되는 부분](#믿으면-안-되는-부분)

## 왜 만드나

**AI가 좋은 MCP를 못 찾는다.** 한국 MCP 스토어들은 대부분 AI가 읽을 수 없다 — 화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. 정작 MCP는 AI가 쓰라고 만든 것인데.

그래서 이 목록은 **AI가 읽을 수 있게** 만든다. JS도 로그인도 차단도 없는 마크다운과 JSON이다. 그리고 **있다고 말하지 않고 두드려 본다** — 등록은 가동의 증거가 아니다.

**우리 것만 싣지 않는다.** 남의 MCP가 더 나으면 더 낫다고 쓴다. 이 목록의 운영자(🏠 표시)도 같은 표에서 같은 잣대로 잰다.

## 한눈에

분야마다 1위 하나씩. 아래 각 분야의 채점 결과와 **같은 값에서 나온다** — 여기와 본문이 어긋날 수 없다.

| 분야 | 1위 | 사실오류 | 왜 이것이 1위인가 |
|---|---|---|---|
| [공공데이터·행정](#공공데이터행정) | [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 1건 | 실제 값이 아니라 포털 메타데이터를 주는 카탈로그형이고 그 설계에 맞는 Q2에서는 실재·구체·검증 가능한 포인터를 냈다 — 다만 '서울시 인구' 같은 자명한 질의에 0건을 돌려주는 검색 재현율과… |
| [법령·판례](#법령판례) | [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 1건 | 법제처 실시간 조회로 두 질문 모두에 현행 원문을 대 준 유일한 서버이고 조문 번호·형량 수치가 실제와 맞았다 — 약점은 서버가 아니라 전달 형식에 있다… |
| [금융·증시](#금융증시) | [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 5건 | 코스피 시총 랭킹은 이 분야에서 유일하게 실측 정합한 답을 냈지만, 정작 실적(DART) 계열 수치는 스케일이 무너져 있어 시세는 믿고 실적은 못 믿는 서버다. |
| [부동산](#부동산) | [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 4건 | 이 목록 운영사 서버이지만 같은 잣대로 봐도 두 질문 다 실제로 답이 나온 유일한 서버다 — 단위·집계법·기준시각·분산 경고·유찰 하자 경고를 원문이 스스로 달아 주고 재호출 대조에서 수치가… |
| [커머스·생활](#커머스생활) | [ai.timeplex/booking](https://chat.timeplex.ai) | 0건 | 이 분야 질문에 끝까지 답한 유일한 서버로 값도 원문과 축자 일치하나, 등록 매장이 1곳뿐이고 lang='ko'로 응답하면서 메뉴명은 일본어 원문 그대로라(답변이 대신 번역했다) 서버가 약속한… |

종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.

## 공공데이터·행정

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 실제로 쓸 만한 것은 haklaekim/public-data-lens 하나뿐이다 — 카탈로그형이라 인구 값은 못 주지만 '어디서 받나'라는 이 분야의 주력 질문에 데이터셋명·recordId·URL·형식·요금까지 붙은 실재 포인터를 냈고 발췌가 포털 실물과 축자 일치했다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 2건이 아래 「분야 교정」으로 빠졌다.</sub>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens)<br><sub>카탈로그형 — 값이 아니라 데이터셋 위치를 준다</sub> | 9 | 23 | 42 | 100% | 100% | 1 |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp)<br><sub>카탈로그형 — 값이 아니라 데이터셋 위치를 준다</sub> | 7 | 222 | 549 | 100% | 100% | 3 |
| [app.apick/all](https://apick.app)<br><sub>전 도구가 API 키 게이트라 종류(데이터형/카탈로그형)조차 확인할 수 없었다</sub> | 82 | 62 | 125 | 100% | 100% | 0 |

1. **haklaekim/public-data-lens** — 실제 값이 아니라 포털 메타데이터를 주는 카탈로그형이고 그 설계에 맞는 Q2에서는 실재·구체·검증 가능한 포인터를 냈다 — 다만 '서울시 인구' 같은 자명한 질의에 0건을 돌려주는 검색 재현율과 대표 데이터셋(에어코리아) 누락이 약점이다.
2. **obundh/korea-public-data-catalog-mcp** — 9만 6천 건 규모를 자처하는 카탈로그형이고 반환 포인터는 실재하지만, 서울→포항·대기질→배출시설 목록처럼 라우팅이 어긋나고 메타데이터 기술에 오기가 섞여 그대로 인용하면 사용자를 잘못 보낸다.
3. **apick/all** — 전 도구가 API 키 게이트라 무가입 상태에서는 종류(데이터형/카탈로그형)조차 확인할 수 없었고, 이 분야 질문에 공급한 사실은 0건이다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 이 회차는 서버당 **1회**만 물었다 — **재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

**분야 교정 2건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [app.apick/business](https://apick.app) | 커머스·생활 | “상거래·물류 데이터형 서버로 이 분야 두 질문은 설계 범위 밖이며…” |
| [yousunjung84-edu/academyinfo-mcp](https://github.com/yousunjung84-edu/academyinfo-mcp) | 교육·문화 | “이름과 달리 학원이 아니라 대학알리미 기반 고등교육 통계 서버로, 공공데이터·행정 분야와는 주제가 다르며…” |

## 법령·판례

> 두 질문 모두에 현행 원문으로 답한 서버는 chrisryugj/korean-law-mcp 하나뿐이고(법제처 실시간 조회), app.sallim/contract-compass는 공공계약 안에서는 조문·금액이 더 정확하지만 코퍼스 38건 밖은 구조적으로 답이 없다.

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 222 | 311 | 100% | 100% | 1 |
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 54 | 77 | 100% | 100% | 0 |
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 13 | 127 | **3951** | 100% | 0% | 1 |

1. **chrisryugj/korean-law-mcp** — 법제처 실시간 조회로 두 질문 모두에 현행 원문을 대 준 유일한 서버이고 조문 번호·형량 수치가 실제와 맞았다 — 약점은 서버가 아니라 전달 형식에 있다(발췌가 조 전문의 앞머리에서 잘리고, 조회한 법령의 시행일을 함께 주지 않아 '지금'이라는 물음에 최신성을 증명하지 못한다).
2. **sallim/contract-compass** — 공공계약 도메인 안에서는 조문 대응·금액 수치가 현행법과 일치했고 코퍼스 밖은 이유를 밝힌 404로 환각을 차단했다 — 다만 근거 발췌가 조문 전문을 담지 않아 검증 가능성이 얇고, 코퍼스 밖 질의(search_law '도로교통법 음주운전')에 공공기관운영법 제53조의2를 1건 매칭해 돌려준 검색 소음은 오도 위험이다.
3. **Choihello/startup-law-mcp** — 창업 지원 법령 전용 색인이라 이 분야 두 질문은 애초에 범위 밖이지만, 빈 결과와 오탐 히트를 원문으로 보여주며 거절해 '못 봄 ≠ 없음'을 정직하게 구분한 점은 이 분야 서버 중 가장 깔끔했다 — 다만 법령·판례 용도로는 쓸 것이 없다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 이 회차는 서버당 **1회**만 물었다 — **재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점하지 않은 1건</summary>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 223 | 301 | 76% | 0% | — |

</details>

## 금융·증시

<sub>이 분야는 후보가 2건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 두 질문을 다 감당할 서버는 없고, 실제로 쓰려면 갈라 써야 한다 — 시장 전체 스냅샷(시총 랭킹·주가)은 com.aikstockdata/mcp가 유일하게 실측 정합한 상위 10을 냈고(역산 주식수가 실제와 일치), 개별 기업 재무제표는 korea-stock-analyzer-mcp의 2025년 연결 매출 333.6조·영업이익 43.6조·마진 13.07%가 유일하게 삼성전자 실제 규모대 안에 들어왔다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 2건이 아래 「분야 교정」으로 빠졌다.</sub>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 45 | **182** | 100% | 100% | 5 |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 219 | 538 | 100% | 100% | 4 |

1. **aikstockdata/mcp** — 코스피 시총 랭킹은 이 분야에서 유일하게 실측 정합한 답을 냈지만, 정작 실적(DART) 계열 수치는 스케일이 무너져 있어 시세는 믿고 실적은 못 믿는 서버다.
2. **Mrbaeksang/korea-stock-analyzer-mcp** — 개별 종목 재무제표는 이 분야에서 가장 정확했으나 시장 전체를 훑는 랭킹·스크리닝 도구가 없어 '상위 종목' 유형 질문에는 구조적으로 답하지 못한다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 이 회차는 서버당 **1회**만 물었다 — **재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

**분야 교정 2건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 미디어·뉴스 | “한국 크립토·매크로 뉴스 알파 서버로 증시와 주제가 다르며…” |
| [app.apick/finance](https://apick.app) | 핀테크·인증 | “이름만 finance일 뿐 실제로는 은행 계좌 검증(1원 인증·실명조회) 서비스로 한국 증시와 주제가 다르며…” |

## 부동산

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 두 질문에 실제로 값이 나온 서버는 app.sallim/korea-realty 하나뿐이다 — 월별 중앙값·거래건수·부분월·평당가와 유찰 물건 목록을 단위·기준시각·하자 경고와 함께 돌려주고, 재호출 대조에서 수치가 그대로 재현됐다. 나머지 둘은 각각 결제벽 뒤의 매매신호(seoul-apt-signal, 핵심 도구 3종 402·유료 미공시)와 분당 3회 제한에 막힌 통계표 검색기(realestate-stats-mcp)라 실거래가·경매 어느 쪽도 채우지 못했다.

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 <sub>무료 37/47</sub> | 47 | 46 | 53 | 100% | 100% | 4 |
| [com.airblockfz/seoul-apt-signal](https://seoul-apt-signal.airblock2026.workers.dev)<br><sub>실거래가가 아니라 산식 미공개 매매신호. 분석 도구는 HTTP 402(사실상 유료)</sub> | 6 | 33 | 79 | 100% | 0% | 1 |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp)<br><sub>개별 실거래가 아니라 한국부동산원 집계 통계표. 분당 3회 제한</sub> | 3 | 121 | **5484** | 100% | 0% | 1 |

1. **sallim/korea-realty** — 이 목록 운영사 서버이지만 같은 잣대로 봐도 두 질문 다 실제로 답이 나온 유일한 서버다 — 단위·집계법·기준시각·분산 경고·유찰 하자 경고를 원문이 스스로 달아 주고 재호출 대조에서 수치가 그대로 재현됐다. 감점은 서버 데이터가 아니라 옮겨 적는 과정의 자릿수·단위 실수 네 건이고(서버는 min_bid_display·억원 표기를 이미 제공했다), 서버 쪽 흠은 '(유)갈현상가'가 usage_name='아파트'로 분류돼 있는 원천 라벨 문제와 무료 30콜/일 한도다.
2. **airblockfz/seoul-apt-signal** — 사실상 유료 서버다 — evaluate_symbol·scan_bottoms·scan_tops가 모두 HTTP 402이고 무료로 열린 것은 마케팅 티저 pitch뿐인데 도구 목록에는 유료 여부가 공시돼 있지 않아(측정값 paid_disclosure=false) 모델이 결제벽을 미리 알 방법이 없으며, 그나마 나오는 것도 실거래가가 아니라 산식 미공개 매매신호라 이 분야 두 질문 중 어느 쪽도 채우지 못한다.
3. **hlucent/realestate-stats-mcp** — 주제가 다른 서버다 — 한국부동산원 통계표(집계 지수) 검색기이지 개별 실거래·법원경매 원장이 아니며, 도구 3종에 분당 3회 제한이 걸려 있어 두 질문 모두 탐색 두세 번 만에 429로 막혀 커버리지 판정조차 못 하고 끝났다(유료는 아니고 콜드 5.5초).

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 이 회차는 서버당 **1회**만 물었다 — **재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

## 커머스·생활

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 다섯 중 이 분야 질문에 실제로 답할 수 있는 서버는 예약의 timeplex와 숙소의 arcasos 둘뿐이고, 나머지 셋(뉴스 API·SaaS 디렉토리·자사몰 결제 엔드포인트)은 서버 결함이 아니라 우리 카테고리 배정 오류다. 그리고 다섯 중 '많이 팔리는'을 답할 판매·인기 지표를 가진 서버는 하나도 없는데, 유일하게 없다고 말하지 않고 검색 결과를 인기 순위인 양 답하게 만든 arcasos가 이 분야에서 가장 위험하다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 2건이 아래 「분야 교정」으로 빠졌다.</sub>

| Server | Tools | Warm | Cold | Desc | Annot | Errors |
|---|---|---|---|---|---|---|
| [ai.timeplex/booking](https://chat.timeplex.ai)<br><sub>뷰티·웰니스 예약. 등록 매장 1곳</sub> | 6 | 388 | **1245** | 100% | 100% | 0 |
| [com.arcasos/arcasos-rentals](https://mcp.arcasos.com)<br><sub>주 단위 단기임차. 총계 미공시로 항상 10건에서 조용히 잘린다</sub> | 3 | 648 | 1099 | 100% | 0% | 2 |
| [com.theprotoclinical/commerce](https://www.theprotoclinical.com)<br><sub>특정 Shopify 스토어 한 곳의 결제 엔드포인트(UCP)</sub> | 13 | 149 | 329 | 100% | 0% | 2 |

1. **timeplex/booking** — 이 분야 질문에 끝까지 답한 유일한 서버로 값도 원문과 축자 일치하나, 등록 매장이 1곳뿐이고 lang='ko'로 응답하면서 메뉴명은 일본어 원문 그대로라(답변이 대신 번역했다) 서버가 약속한 번역이 실제로는 동작하지 않는다.
2. **arcasos/arcasos-rentals** — 숙소 재고는 실재하고 응답도 빠르지만, limit을 무시하고 항상 10건만 총계 없이 돌려주는 조용한 절단과 정렬 근거 미공시가 겹쳐 '인기'·'전체'를 묻는 질문에서 모델이 그럴듯하게 틀리도록 유도한다.
3. **theprotoclinical/commerce** — 자사몰 결제 에이전트라 두 질문 다 범위 밖인 데다, 프로필 URI 없이는 카탈로그 조회가 전부 422로 막혀(continue_url이 yxcs11-ry.myshopify.com 개발 스토어를 가리킨다) 익명 AI 클라이언트로는 상품 하나 확인할 수 없다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 이 회차는 서버당 **1회**만 물었다 — **재현성은 재지 않았다**(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

**분야 교정 2건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 미디어·뉴스 | “상품·예약과는 무관한 미디어 서버다.” |
| [com.saaskr/korean-saas-directory](https://saaskr.com) | 디렉토리·개발자도구 | “상품 판매나 예약을 하는 곳이 아니다.” |

## 표기

* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다
* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다
* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. **둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다
* 이름 옆 <sub>무료 N/M</sub> — 서버가 유료 게이트를 **스스로 공시**할 때만 붙는다. 없다고 무료라는 뜻이 아니다 — 밖에서는 판정할 수 없다
* 이름 밑 작은 글씨 — 불러 보고 알게 된 **그 서버의 성질**. 카탈로그형은 값이 아니라 데이터셋 위치를 주고, 집계 통계표는 개별 거래를 주지 않는다. 몰라서 헛짚는 자리라 표에 낸다
* **사실오류** — 그 서버로 답한 내용 중 채점자가 **실제와 다르다고 확인한** 건수. 서버가 틀린 값을 준 경우와 모델이 옮겨 적다 틀린 경우가 섞여 있고, 어느 쪽인지는 [grades/](grades)에 문장째 적혀 있다. `—`는 채점하지 않았다는 뜻이다
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

제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 우리가 통과시키고 말고 할 것이 없다.

## 고쳤다면 다시 잰다

이 표의 값은 **2026-08-19 그 순간의 기록**이다. 고쳤다면 [이슈](https://github.com/sallim-app/korea-mcp-index/issues)로 알려 달라 — 다음 회차에 다시 잰다. 경쟁 서비스여도 받는다.

**우리가 먼저 다시 두드리지는 않는다.** 바뀐 게 없는 서버를 주기적으로 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다. 그래서 두드리는 대신 신호를 받는다.

이런 것도 같은 창구다 — **우리 쪽 잘못일 수 있다.**

* 분야가 틀렸다 (검색어가 분야를 정하므로 실제로 하는 일과 어긋날 수 있다)
* 주소를 잘못 짚었다 (README에서 추정한 주소라 서버가 아니라 우리가 틀린 것)
* 채점이 틀렸다 — 답변·근거·채점이 [answers/](answers)·[grades/](grades)에 그대로 있으니 어느 문장이 왜 틀렸는지 짚어 달라

**순위는 전원 동시에만 다시 잰다 — 운영자인 우리도 예외가 아니다.** 우리는 고칠 때마다 다시 잴 수 있고 남은 그럴 수 없다. 개별 재측정을 순위에 반영하면 우리 서버만 계단식으로 올라가고 남은 자기 최악의 순간에 박제된다. 실제로 우리는 이 표의 지적을 받아 우리 서버를 고치고 다시 쟀지만 **그 결과를 순위에 넣지 않았다** — 기록은 [answers/](answers)에 ‘정규 회차 아님’으로 남겨 두었다.

## 어떻게 재나

```
collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API
filter   한국 관련성(한글·.go.kr·기관명) → 후보 좁히기
enrich   README에서 엔드포인트·패키지·기관 도메인 추출
classify 분야·데이터제공형 판정 (LLM, 결과는 classification.json에 고정)
measure  tools/list 실호출 — 가동·도구수·지연·설명·주석          [매주]
answer   분야별 실제 질문을 서버에 던져 답하게 한다 (Haiku)       [매월]
grade    그 답을 원문과 대조해 채점한다 (Opus) → 순위             [매월]
render   이 문서
```

**가동은 매주, 순위는 매월 1일**에 다시 잰다. 서버가 안 바뀌면 채점 결과도 안 바뀌는데 매주 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다.

두드릴 때는 `tools/list` 3회(콜드 1 + 웜 2), 사이에 간격을 두고, User-Agent로 우리를 밝힌다.

**가동 지표는 돌리면 같은 값이 나온다** — 원자료가 [measured.json](measured.json)·[candidates.json](candidates.json)에 있다. **순위는 그렇지 않다** — 채점이 모델 판단이라 같은 입력에도 흔들린다. 얼마나 흔들리는지를 우리가 직접 재서 [variance/](variance)에 공개해 두었다. 우리가 1위인 자리일수록 이 두 문장을 함께 읽어 달라.

## 믿으면 안 되는 부분

* **정확성은 분야마다 질문 두 개로만 봤다.** 그 두 문항이 그 분야를 대표한다는 보장은 없다. 질문은 공개돼 있으니(`questions.py`) 더 나은 질문을 알려 달라
* **채점자도 모델이다.** 근거를 전부 공개하는 것으로 줄일 수는 있어도 없앨 수는 없다. 답변은 약한 모델(Haiku)이 만들고 채점은 강한 모델(Opus)이 하는데, 그 이유와 실측 근거는 [JUDGING.md](JUDGING.md)에 있다
* **한 번 물어본 순위다.** 다시 물으면 등수가 갈릴 수 있다 — 우리 서버로 재 보니 질문 네 자리 중 두 곳이 갈렸다([variance/](variance)). 다음 채점 회차부터 3회로 잰다
* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다
* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다
* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다
* **못 잰 것이 더 많다.** 후보 중 25건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다 — 그 밖에 54건은 배포 패키지는 확인했으나 원격 주소가 없어 응답을 못 쟀다

---

## 라이선스

코드·문서·우리가 만든 측정값은 [MIT](LICENSE). **응답 발췌는 각 서버 운영자의 것**이고 우리는 측정 근거로 인용했을 뿐이다 — 400~500자로 제한하고 개인정보 패턴을 가린다. 내려 달라고 하면 내린다.

---

생성 `render_readme.py` · 마지막 측정 2026-08-19 · 운영 [sallim-app](https://github.com/sallim-app)
