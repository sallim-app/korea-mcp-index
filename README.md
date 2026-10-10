[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) [![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)

# 한국 데이터 MCP — 실측 목록

> 한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 “있다”를 말한다. 이 목록은 **지금 되냐**를 잰다. 2026-09-14 기준 주소를 확인한 119건 중 **91건이 살아있음 확인**, 23건은 **확인 못 함**, 5건만 **죽음 확인**이다. 확인 못 함은 사망이 아니다 — 우리가 못 본 것과 그쪽이 없는 것은 다르다.

> **웹판** <https://mcp-index.sallim.app> — 같은 값을 분야별·서버별 주소로 갈라 놓았다. 기계가 읽을 것은 [index.json](https://mcp-index.sallim.app/index.json)·[llms.txt](https://mcp-index.sallim.app/llms.txt).

| | |
|---|---|
| 비교 가능한 서버 | **68**건 |
| 응답했으나 못 잼(키 필요·규격 이탈) | 17건 |
| 확인 못 함(우리 호출로 확인 실패 — **사망 아님**) | 23건 → [DOWN.md](DOWN.md) |
| 죽음 확인(DNS 미해결·연결 거부) | 5건 → [DOWN.md](DOWN.md) |
| 주제 밖(데이터 제공형 아님) | 6건 |
| 설치형(원격 주소 없음) | 배포 확인 **79**건 · 배포판 없음 109건 · 이름을 못 읽어 미측정 19건 |
| **이번 회차 측정 모집단**(위 줄 전부 — 76건은 주소가 없어 두드리지 못했다) | 404건 — 같은 주소 2건을 합쳐 402줄로 실린다 |
| **재지 않은 후보**(한 번도 두드리지 않음) | 114건 |
| **후보 전체** | 518건 |

* [왜 만드나](#왜-만드나)
* [한눈에](#한눈에)
* [우리가 지는 항목](#우리가-지는-항목)
* [공공데이터·행정](#공공데이터행정)
* [법령·판례](#법령판례)
* [금융·증시](#금융증시)
* [부동산](#부동산)
* [세금·재정](#세금재정)
* [지도·주소](#지도주소)
* [날씨·환경](#날씨환경)
* [교통·이동](#교통이동)
* [의료·복지](#의료복지)
* [교육·문화](#교육문화)
* [커머스·생활](#커머스생활)
* [미디어·뉴스](#미디어뉴스)
* [핀테크·인증](#핀테크인증)
* [기타](#기타)
* [표기](#표기)
* [측정 못 함](#측정-못-함)
* [우리 목록에 넣으려면](#우리-목록에-넣으려면)
* [고쳤다면 다시 잰다](#고쳤다면-다시-잰다)
* [어떻게 재나](#어떻게-재나)
* [믿으면 안 되는 부분](#믿으면-안-되는-부분)
* [신뢰 규약 — 무엇을 재는지 먼저 말한다](PROTOCOL.md)

## 왜 만드나

**AI가 좋은 MCP를 못 찾는다.** 한국 MCP 스토어들은 대부분 AI가 읽을 수 없다 — 화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. 정작 MCP는 AI가 쓰라고 만든 것인데.

그래서 이 목록은 **AI가 읽을 수 있게** 만든다. JS도 로그인도 차단도 없는 마크다운과 JSON이다. 그리고 **있다고 말하지 않고 두드려 본다** — 등록은 가동의 증거가 아니다.

**우리 것만 싣지 않는다.** 남의 MCP가 더 나으면 더 낫다고 쓴다. 이 목록의 운영자(🏠 표시)도 같은 표에서 같은 잣대로 잰다.

**그리고 그 표를 설계한 것도 우리다**. 원자료를 다 공개해도 이 편향은 안 없어진다 — 축을 하나 넣고 빼는 것만으로 등수는 바뀌고, 그 선택권을 쥔 쪽이 순위에 자기 제품을 올린 쪽이다. 그래서 이 문장을 각주가 아니라 소유 공시 바로 옆에 둔다. 무엇을 재기로 했는지는 결과를 보기 전에 [신뢰 규약](PROTOCOL.md)에 고정해 두었고, 바꾼 적이 있으면 그 이력도 거기 있다 — **한 번 있다.**

## 한눈에

분야마다 1위 하나씩. 아래 각 분야의 채점 결과와 **같은 값에서 나온다** — 여기와 본문이 어긋날 수 없다.

| 분야 | 1위 | 사실오류 | 왜 이것이 1위인가 |
|---|---|---|---|
| [공공데이터·행정](#공공데이터행정) | [datagokr-dev/datagokr](https://github.com/datagokr-dev/datagokr) | 0건 | 공공데이터포털에서 무엇을 어떻게 받는지 찾는 용도로는 이 분야에서 가장 안정적이다. 다만 미리보기가 시간초과로 실패해 실제 수치까지는 못 가므로 통계 값이 필요하면 통계 서버를 함께 써야 한다. |
| [법령·판례](#법령판례) | [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 0건 | 일반 법령 전반을 법제처 현행 원문으로 조회할 수 있고 두 질문 모두 맞는 조문과 형량을 돌려준 유일한 서버라 이 분야에서 먼저 쓸 만하다. |
| [금융·증시](#금융증시) | [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 2건 | 삼성전자 실적은 DART 기간·연결 여부를 밝힌 최신 반기 누적값을 세 번 모두 정확히 내준다. 시총 상위 목록도 list_stocks(filter=all)로 나오지만 기본값이 흑자전환이라 약한… |
| [부동산](#부동산) | [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 5건 | 강남구 시세 추이·평형대 가격과 서울 경매 유찰 통계를 출처·단위·표본 경고와 함께 정확히 내주므로 부동산 질문에 쓸 만하다. |
| [커머스·생활](#커머스생활) | [ai.timeplex/booking](https://timeplex.ai) | 1건 | 서울 뷰티·마사지·헤드스파 예약용으로는 응답이 결정적이고 필드가 정직해 믿고 쓸 만하며, 판매 인기 순위는 주지 않으니 '잘 팔리는 것'을 묻는 용도에는 맞지 않습니다. |

종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.

## 우리가 지는 항목

**유리한 축만 재면 그 순위는 판정이 아니라 광고지다.** 원격 MCP인 우리가 불리한 축을 같이 잰다 — 무엇을 잴지는 결과를 보기 전에 [신뢰 규약](PROTOCOL.md)에 고정했고, 여기서 뺄 수 없게 회귀 테스트로 묶어 두었다.

| 축 | 이 목록 전체 | 운영자(🏠) |
|---|---|---|
| 셀프호스팅 | 배포판 확인 98건 · 소스만 259건 · 미확인 45건 | **소스만** 2건 — 그리고 클론해도 답이 안 나온다 · **소스 비공개 1건**(korea-stay) — 이 축에서 우리가 제일 나쁘다 |
| 오픈소스 | MIT 173건, Apache-2.0 18건, AGPL-3.0 2건, ISC 1건 · 라이선스 확인 못 함 208건 | MIT — **이 축에서는 우리가 지지 않는다**. 단 korea-stay는 저장소가 없어 라이선스도 없다 |
| 무료 한도 | 스스로 공시한 서버 1건 | 그 1건이 우리다 — 도구 52종 중 **10종 유료** |

* **셀프호스팅은 우리가 제일 나쁘다.** 우리 저장소는 MIT로 열려 있지만 도구들이 우리 비공개 데이터 API를 부르므로 [클론해서 띄우면 거의 다 실패한다](https://github.com/sallim-app/korea-realty) — 우리 README가 먼저 적어 둔 것이고, 여기서도 적는다. 축의 값(`source_only`)보다 실질이 나쁘다
* **`소스만`은 “띄우면 같은 답이 나온다”가 아니다.** 코드가 공개돼 있다는 뜻일 뿐이고, 남의 서버도 우리처럼 자기 데이터에 묶여 있을 수 있다 — 그건 우리가 재지 않았다
* **`라이선스 확인 못 함`을 “오픈소스 아님”으로 읽지 말라.** 저장소가 비공개거나 지워졌거나 이름이 바뀐 것도 여기 들어온다. 다만 **공개 저장소인데 라이선스 파일이 없는 것**은 기본값이 저작권 전부 유보라 실제로 가져다 쓸 수 없다
* **유료 공시가 1건뿐인 것은 나머지가 무료라는 뜻이 아니다.** 밖에서는 판정할 수 없다. 밝힌 쪽만 표에 유료 게이트가 보이고, 지금 그 쪽은 우리다

축이 모자란다고 보면 다른 가중치로 직접 재계산할 수 있다 — [axes.csv](axes.csv)가 서버 1행 × 축 1열이고, `python3 recompute.py --weights tool_count=1,warm_ms=-0.01`이 그 계산기다. **그 결과는 우리 순위가 아니다** — 지표로 줄 세우는 방식은 우리가 실측으로 폐기했다([JUDGING.md](JUDGING.md)).

## 공공데이터·행정 (Public Data)

> 공공데이터포털 자료 안내는 datagokr가 세 번 모두 에어코리아를 맨 앞에 올리며 가장 안정적이었고, public-data-lens는 기본 검색에서 전국 표준 자료가 뒤로 밀렸다. 서울 인구 변화를 실제 수치로 답한 서버는 한 곳도 없었는데, korea-stats-mcp는 region 인자로 2016~2025년 서울 시계열을 줄 수 있었는데도 답변자가 그 인자를 쓰지 못해 전국 값을 대신 냈다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 2건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [datagokr-dev/datagokr](https://github.com/datagokr-dev/datagokr) | 6 | 137 | 138 | 100% | 100% | 0 |
| [hike-lab/public-data-lens](https://github.com/hike-lab/public-data-lens)<br><sub>카탈로그형 — 값이 아니라 데이터셋 위치를 준다</sub><br><sub>지난 회차 표기 `haklaekim/public-data-lens` → `hike-lab/public-data-lens` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 9 | 26 | 26 | 100% | 100% | 1 |
| [Dayoooun/korea-stats-mcp](https://github.com/Dayoooun/korea-stats-mcp) | 14 | 193 | 427 | 100% | 0% | 2 |

1. **datagokr-dev/datagokr** — 공공데이터포털에서 무엇을 어떻게 받는지 찾는 용도로는 이 분야에서 가장 안정적이다. 다만 미리보기가 시간초과로 실패해 실제 수치까지는 못 가므로 통계 값이 필요하면 통계 서버를 함께 써야 한다.
2. **hike-lab/public-data-lens** — 공공데이터포털 목록을 정밀하게 걸러 보는 데는 쓸 만하지만, '대기질' 같은 일반 검색에서 전국 표준 자료가 뒤로 밀려 처음 찾는 사람에게는 덜 친절하다. 실제 수치는 주지 않는다.
3. **Dayoooun/korea-stats-mcp** — KOSIS 수치를 실제로 돌려주는 유일한 서버이고 값도 다른 원장과 맞지만, 지역 추세는 region 인자를 써야만 나와서 약한 모델은 전국 값을 대신 답했다. 통계 값이 필요하면 쓸 만하나 공공데이터포털 안내용은 아니다.
4. **hjsh200219/korea-public-data-mcp** — 법령·통관·공시·보건의료 등 공공 API를 넓게 묶은 서버라 이 분야 두 질문에는 맞는 도구가 없었다. 공공데이터포털 자료 찾기나 인구 통계 용도로는 권하지 않는다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [hjsh200219/korea-public-data-mcp](https://github.com/hjsh200219/korea-public-data-mcp) | 19 | 524 | 604 | 100% | 100% | 0 |

</details>

<details><summary>채점하지 않은 12건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.pipeworx-io/dart-kr](https://github.com/pipeworx-io/mcp-dart-kr) | 40 | 143 | 378 | 100% | 100% | — |
| [io.github.pipeworx-io/ecos-kr](https://github.com/pipeworx-io/mcp-ecos-kr) | 39 | 464 | 180 | 100% | 100% | — |
| [io.github.loved0543-dotcom/kdata-gate](https://github.com/loved0543-dotcom/kdata-gate-mcp) | 26 | 366 | 451 | 100% | 0% | — |
| [site.star365/hq](https://star365.site/) | 26 | 158 | 173 | 100% | 100% | — |
| [io.github.richard-kim-79/jejusns](https://jejusns.com) | 16 | 733 | 1003 | 100% | 0% | — |
| [kr.eocpa/mydart](https://eocpa.kr/mydart) | 16 | 199 | 193 | 100% | 100% | — |
| [site.star365/data](https://data.star365.site/) | 10 | 111 | 113 | 100% | 100% | — |
| [io.github.ChloePark85/kr-groundtruth](https://kr-groundtruth-mcp.vercel.app) | 8 | 599 | 240 | 100% | 100% | — |
| [042Jason/kosis-mcp](https://github.com/042Jason/kosis-mcp) | 6 | 470 | 452 | 100% | 0% | — |
| [bhyunco/korea-holiday-mcp](https://github.com/bhyunco/korea-holiday-mcp) | 6 | 227 | 240 | 100% | 0% | — |
| [io.github.lazymac2x/govdata-korea](https://github.com/lazymac2x/govdata-korea-api) | 6 | 110 | 112 | 100% | 0% | — |
| [kr.ibtcc/competition-ratio](https://github.com/jojunho74/hometest) | 1 | 244 | 237 | 100% | 0% | — |

</details>

**분야 교정 2건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [app.apick/all](https://github.com/lead788/apick-mcp) | 기타 | “도구 115종이 계좌·신분증 진위확인, OCR, 웹검색, 영상·문서 변환 같은 유료 범용 API이고 인구 통계나 공공데이터포털 목록을 다루는 도구는 없다…” |
| [app.apick/business](https://github.com/lead788/apick-mcp) | 커머스·생활 | “상거래·물류 데이터형 서버로 이 분야 두 질문은 설계 범위 밖이며…” |

## 법령·판례 (Law)

> 두 질문 모두 맞는 조문과 형량을 돌려준 서버는 chrisryugj/korean-law-mcp 하나였고, app.sallim/contract-compass는 공공계약 질문에서 가장 완결된 답을 줬지만 도로교통법은 범위 밖이었다. scvcoder/korean-law-alio-mcp는 법령 도구가 API 키 오류로 죽어 있었고, Choihello/startup-law-mcp는 창업 법령 서버라 이 분야 질문에 맞지 않았다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 204 | 202 | 100% | 100% | 0 |
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 33 | 33 | 100% | 100% | 1 |
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 222 | 240 | 76% | 0% | 1 |

1. **chrisryugj/korean-law-mcp** — 일반 법령 전반을 법제처 현행 원문으로 조회할 수 있고 두 질문 모두 맞는 조문과 형량을 돌려준 유일한 서버라 이 분야에서 먼저 쓸 만하다. 다만 search_law만으로는 조문에 닿지 못하는 경우가 있어 legal_research나 조문 지정 조회를 함께 써야 답이 안정된다.
2. **sallim/contract-compass** — 국가계약법·지방계약법 같은 공공계약 조문은 세목과 금액까지 정확히 돌려주지만 도로교통법 같은 일반 법령은 담지 않으므로, 공공계약·세법 질문용으로 고르고 일반 법령은 다른 서버와 함께 써야 한다. 응답이 스스로 '현행 여부 미검증'을 공시하고 있어 인용 전에 그 공시를 확인할 필요가 있다.
3. **scvcoder/korean-law-alio-mcp** — 도구 목록은 125종으로 크지만 이번에 다시 불러도 법령 조회 도구가 법제처 API 키 오류로 isError를 내 법령 질문에는 지금 쓸 수 없다. ALIO 공공기관 규정 조회는 동작하므로 공공기관 내부 규정을 찾을 때만 쓸 만하다.
4. **Choihello/startup-law-mcp** — 이 서버는 창업 관련 법령과 K-Startup 지원사업을 다루는 도구라 국가계약법·도로교통법 질문에는 맞지 않으며, 창업 세액감면이나 지원사업 자격 같은 질문에 쓸 서버다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp)<br><sub>창업 법령 조문과 K-Startup 창업지원사업 전용 — 일반 법령 질문은 범위 밖</sub> | 13 | 122 | 134 | 100% | 0% | 0 |

</details>

<details><summary>채점하지 않은 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.peter120525-cmd/lawmadi-os](https://lawmadi.com) | 19 | 166 | 179 | 100% | 0% | — |

</details>

## 금융·증시 (Finance)

> 삼성전자 실적은 DART 공시 대조로 aikstockdata(2026 상반기 누적 연결), MosslandOpenDevs/alpha(1·2분기 단독) 값이 모두 맞았고, 두 서버의 차이는 기간 정의(누적 대 분기 단독) 차이일 뿐이었다. 시총 상위는 stock-data-mcp만 실제 목록을 냈고, aikstockdata는 같은 목록을 낼 수 있는데도 기본값 때문에 세 회차 모두 놓쳤다. finbridge는 인증 요구로 이번 회차에 측정하지 못했다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 1건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 23 | 33 | 100% | 100% | 2 |
| [kmgvv23/stock-data-mcp](https://github.com/kmgvv23/stock-data-mcp) | 42 | 706 | 504 | 100% | 0% | 3 |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 216 | 541 | 100% | 100% | 2 |

1. **aikstockdata/mcp** — 삼성전자 실적은 DART 기간·연결 여부를 밝힌 최신 반기 누적값을 세 번 모두 정확히 내준다. 시총 상위 목록도 list_stocks(filter=all)로 나오지만 기본값이 흑자전환이라 약한 모델은 세 번 다 못 찾았다.
2. **kmgvv23/stock-data-mcp** — KRX·DART 원천 API를 거의 그대로 중계해 값 자체는 정확하고 시총 상위 목록도 나오지만, 연도·정렬·단위를 모델이 직접 챙겨야 해서 '최근 실적'을 2024년으로 답하는 일이 세 번 다 났다.
3. **Mrbaeksang/korea-stock-analyzer-mcp** — 연간 사업보고서 기준 재무는 정확하고 연결·단위 표기가 분명하지만, 분기·반기 실적이 없어 '최근 실적'이 한 해 넘게 늦고 시총 순위는 아예 못 한다.
4. **MosslandOpenDevs/alpha** — 유튜브 여론·뉴스 제목을 합성한 시장 해설 서버라 실적 수치는 운이 좋으면 이벤트 별칭에서 나오지만 전망치와 섞여 있고, 시총 같은 시세 데이터는 없다. 종목 데이터가 필요하면 쓰지 않는 편이 낫다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 12 | 29 | 34 | 100% | 0% | 1 |

</details>

<details><summary>채점하지 않은 12건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.gronox/finbridge](https://github.com/Jakechj/finbridge-mcp) | 44 | 63 | 81 | 100% | 100% | — |
| [dartpointai/dartpoint-mcp](https://github.com/dartpointai/dartpoint-mcp) | 37 | 25 | 25 | 100% | 0% | — |
| [com.thenextgennexus/global-equities-screener-mcp](https://apify.com/nexgendata/global-equities-screener-mcp) | 26 | 31 | 36 | 100% | 100% | — |
| [eddmpython/dartlab](https://github.com/eddmpython/dartlab) | 26 | — | 634 | 100% | 0% | — |
| [emceeKim/korea-finance-mcp](https://github.com/emceeKim/korea-finance-mcp) | 25 | 152 | 160 | 100% | 100% | — |
| [io.github.bakyang2/kr-crypto-intelligence](https://github.com/bakyang2/kr-crypto-intelligence) | 18 | 91 | 93 | 100% | 100% | — |
| [io.github.bubilife1202/crossfin](https://github.com/bubilife1202/crossfin) | 16 | 80 | 81 | 100% | 0% | — |
| [bootpay/bootpay-mcp](https://github.com/bootpay/bootpay-mcp) | 9 | 32 | 29 | 100% | 0% | — |
| [io.github.whdrnr2583-cmd/koreanpulse](https://github.com/whdrnr2583-cmd/koreanpulse) | 7 | 39 | 39 | 100% | 100% | — |
| [com.airblockfz/stock-signal-kr](https://airblockfz.com) | 5 | 28 | 28 | 100% | 0% | — |
| [kr.eocpa/myfss](https://eocpa.kr/myfss) | 5 | 118 | 120 | 100% | 100% | — |
| [kr.maedong/maedong](https://maedong.kr) | 5 | 300 | 302 | 100% | 100% | — |

</details>

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [app.apick/finance](https://github.com/lead788/apick-mcp) | 핀테크·인증 | “이름만 finance일 뿐 실제로는 은행 계좌 검증(1원 인증·실명조회) 서비스로 한국 증시와 주제가 다르며…” |

## 부동산 (Real Estate)

<sub>이 분야는 후보가 3건뿐이라 **고른 것이 아니라 줄 세운 것**이다.</sub>

> 부동산 분야에서 두 질문 모두에 서버 데이터로 답한 것은 korea-realty 하나였고, 그쪽의 흠은 서버 값이 아니라 답변 모델의 단위 옮김과 용도 미지정에서 나왔다. seoul-apt-signal은 서울 구별 신호 전용인 데다 유료 장벽 때문에 무료 답변은 강남구 표본 신호 한 줄에 그쳤고, 경매 질문은 범위 밖이라 정직하게 거절했다. hlucent/realestate-stats-mcp는 이번 회차 가동 확인을 못 해 채점하지 못했다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 <sub>무료 42/52</sub> | 52 | 47 | 59 | 100% | 100% | 5 |
| [com.airblockfz/seoul-apt-signal](https://airblockfz.com)<br><sub>실거래가가 아니라 산식 미공개 매매신호. 분석 도구는 HTTP 402(사실상 유료)</sub> | 6 | 36 | 27 | 100% | 0% | 0 |

1. **sallim/korea-realty** — 강남구 시세 추이·평형대 가격과 서울 경매 유찰 통계를 출처·단위·표본 경고와 함께 정확히 내주므로 부동산 질문에 쓸 만하다. 다만 경매 경보 도구는 용도 기본값이 '전체'라 아파트를 물어도 다세대가 섞여 나오니 usage_name을 꼭 지정해야 한다.
2. **airblockfz/seoul-apt-signal** — 서울 25개 구의 매수/매도 신호만 주고 핵심 도구가 전부 x402 유료라 무료로는 pitch의 강남구 표본 하나만 볼 수 있다. 실거래 가격 수치나 경매 정보가 필요하면 쓰기 어렵다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점하지 않은 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.co.reevl/reevl-mcp](https://reevl.co.kr/mcp)<br><sub>지난 회차 표기 `exclusiveyon-a11y/reevl-plugins` → `kr.co.reevl/reevl-mcp` — 같은 서버로 이었다</sub> | 7 | 37 | 33 | 100% | 100% | — |

</details>

## 세금·재정 (Tax)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.minsooparkk/korea-tax-law-mcp](https://github.com/minsooparkk/korea-tax-law-mcp) | 14 | 48 | 42 | 100% | 14% | — |
| [kr.eocpa/mykifrs](https://eocpa.kr/mykifrs) | 6 | 123 | 126 | 100% | 100% | — |

## 지도·주소 (Maps)

후보가 1건뿐이라 순위를 매기지 않았다. 이 분야에서 응답한 서버가 하나라 비교할 상대가 없다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.namuaix/seoul-tourism](https://mcp.namu.ai.kr) | 3 | 20 | 20 | 100% | 100% | — |

## 날씨·환경 (Weather)

후보가 1건뿐이라 순위를 매기지 않았다. 이 분야에서 응답한 서버가 하나라 비교할 상대가 없다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.sean-park-funda/korea-ocean-mcp](https://github.com/sean-park-funda/korea-ocean-mcp) | 8 | 27 | 34 | 100% | 0% | — |

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [io.github.sean-park-funda/korea-data-mcp](https://github.com/sean-park-funda/korea-data-mcp) | 기타 | “도구 6종이 한국관광공사 관광정보, 시내버스 정류소, 기상 평년값뿐이라 공공데이터 목록 검색이나 인구 통계는 다루지 않는다…” |

## 교통·이동 (Transit)

후보가 1건뿐이라 순위를 매기지 않았다. 이 분야에서 응답한 서버가 하나라 비교할 상대가 없다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.kimnchai/korea-flight-mcp](https://korea-flight.kimnchai.com) | 8 | 36 | 43 | 100% | 100% | — |

## 의료·복지 (Health)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [nokelan/health-fee-mcp](https://github.com/nokelan/health-fee-mcp) | 12 | — | 22 | 100% | 0% | — |
| [org.medicalaialliance/intelligence](https://github.com/austinpw-cloud/maa-website) | 5 | 357 | 224 | 100% | 0% | — |

## 교육·문화 (Education)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [app.wonbuddhism/scripture](https://scripture.wonbuddhism.app) | 7 | 53 | **296** | 100% | 100% | — |
| [clayop/korean-university-regulation-mcp](https://github.com/clayop/korean-university-regulation-mcp) | 4 | 10066 | 10068 | 50% | 0% | — |

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [io.github.yousunjung84-edu/academyinfo](https://github.com/yousunjung84-edu/academyinfo-mcp)<br><sub>지난 회차 표기 `yousunjung84-edu/academyinfo-mcp` → `io.github.yousunjung84-edu/academyinfo` — 같은 서버로 이었다</sub> | 교육·문화 | “이름과 달리 학원이 아니라 대학알리미 기반 고등교육 통계 서버로, 공공데이터·행정 분야와는 주제가 다르며…” |

## 커머스·생활 (Commerce)

> 세 서버 모두 판매량·인기 순위 데이터를 주지 않아 Q1에 직접 답한 곳은 없었고, 차이는 그 사실을 정직하게 드러내며 대리 신호를 얼마나 주느냐에서 났습니다. 예약 질문(Q2)에는 timeplex와 arcasos가 실제 예약 가능 대상을 안정적으로 돌려줬고, protoclinical은 UCP 에이전트 프로필 요건 때문에 일반 클라이언트로는 한 번도 답을 받지 못했습니다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 1건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [ai.timeplex/booking](https://timeplex.ai)<br><sub>뷰티·웰니스 예약. 등록 매장 10곳(2026-10-01 회차 확인)</sub> | 5 | 416 | 399 | 100% | 100% | 1 |
| [com.arcasos/arcasos-rentals](https://arcasos.com)<br><sub>주 단위 단기임차. 총계 미공시로 항상 10건에서 조용히 잘린다</sub> | 3 | 548 | 652 | 100% | 0% | 3 |
| [com.theprotoclinical/commerce](https://www.theprotoclinical.com/)<br><sub>특정 Shopify 스토어 한 곳의 결제 엔드포인트(UCP)</sub> | 13 | 142 | 217 | 100% | 0% | 1 |

1. **timeplex/booking** — 서울 뷰티·마사지·헤드스파 예약용으로는 응답이 결정적이고 필드가 정직해 믿고 쓸 만하며, 판매 인기 순위는 주지 않으니 '잘 팔리는 것'을 묻는 용도에는 맞지 않습니다.
2. **arcasos/arcasos-rentals** — 서울·부산 주 단위 단기임대 숙소를 찾는 데는 응답이 안정적이고 링크까지 줘서 쓸 만하지만, 결과 순서는 관련도일 뿐 인기도가 아니므로 '잘 나가는 매물'로 읽지 않도록 주의해야 합니다.
3. **theprotoclinical/commerce** — Shopify UCP 규격의 상점 서버라 서버가 받아 올 수 있는 에이전트 프로필 URI를 갖춘 클라이언트가 아니면 상품 검색조차 할 수 없으며, 이번 회차에는 어떤 상품 정보도 확인하지 못했습니다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점하지 않은 6건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.nmjib/nmjib](https://github.com/Deall-International/nmjib-mcp) | 10 | 250 | 243 | 100% | 100% | — |
| [ai.atdev/supershopping](https://github.com/alex-hoyeol-choi/headless-commerce) | 8 | 41 | 46 | 100% | 100% | — |
| [ai.hotker/hotker](https://github.com/c2bcom10-ship-it/hotker) | 6 | 38 | 41 | 100% | 0% | — |
| [com.kimchi-sushi/agent-mcp](https://kimchi-sushi.com) | 6 | 214 | 234 | 100% | 100% | — |
| [app.sallim/korea-stay](https://stay.sallim.app) 🏠 | 4 | 29 | 43 | 100% | 100% | — |
| [io.github.aminpiano/nara-tour](https://github.com/aminpiano/naratour-mvp) | 3 | 29 | 51 | 100% | 0% | — |

</details>

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.saaskr/korean-saas-directory](https://saaskr.com/mcp) | 디렉토리·개발자도구 | “상품 판매나 예약을 하는 곳이 아니다.” |

## 미디어·뉴스 (Media)

후보가 0건뿐이라 순위를 매기지 않았다. 0개 중 0개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 미디어·뉴스 | “상품·예약과는 무관한 미디어 서버다.” |

## 핀테크·인증 (Fintech)

후보가 1건뿐이라 순위를 매기지 않았다. 이 분야에서 응답한 서버가 하나라 비교할 상대가 없다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.Wonderfulian/kbv-server](https://github.com/Wonderfulian/kbv-server) | 3 | 55 | 156 | 100% | 100% | — |

## 기타 (Other)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.sadri-dridi/tz-asia-seoul](https://github.com/sadri-dridi/named-mcp-utilities)<br><sub>한 저장소(named-mcp-utilities)·한 워커로 레지스트리에 수백 건을 등록한 범용 유틸리티 묶음(abs-ok·acre-to-m2·adler32-ok…) 중 한 조각. 한국 신호는 타임존 표기 Asia/Seoul뿐이고, 도구 30개도 한국용이 아니다</sub> | 30 | 26 | 28 | 100% | 0% | — |
| [com.seoapi/naverbot](https://seoapi.com/naverbot/) | 1 | 27 | 27 | 100% | 0% | — |

## 표기

* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다
* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다
* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. **둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다
* 이름 옆 <sub>무료 N/M</sub> — 서버가 유료 게이트를 **스스로 공시**할 때만 붙는다. 없다고 무료라는 뜻이 아니다 — 밖에서는 판정할 수 없다
* 이름 밑 작은 글씨 — 불러 보고 알게 된 **그 서버의 성질**. 카탈로그형은 값이 아니라 데이터셋 위치를 주고, 집계 통계표는 개별 거래를 주지 않는다. 몰라서 헛짚는 자리라 표에 낸다
* **사실오류** — 그 서버로 답한 내용 중 채점자가 **실제와 다르다고 확인한** 건수. 서버가 틀린 값을 준 경우와 모델이 옮겨 적다 틀린 경우가 섞여 있고, 어느 쪽인지는 [grades/](grades)에 문장째 적혀 있다. `—`는 채점하지 않았다는 뜻이다
* 🏠 — 이 목록의 운영자가 만든 서버. **이 목록의 축을 고른 것도 같은 운영자다** — 축과 그 개정 이력은 [PROTOCOL.md](PROTOCOL.md)에 있다

## 측정 못 함

응답은 했지만 **비교할 값을 얻지 못한 17건.** 지우지 않고 여기 둔다 — “없다”가 아니라 **“우리가 못 봤다”**이기 때문이다. 대부분 도구 목록을 보는 데도 키를 요구한다. 키가 있으면 잘 도는 서버일 수 있다.

| 서버 | 증상 |
|---|---|
| [MarcoYou/open-proxy-mcp](https://github.com/MarcoYou/open-proxy-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [ai.heyyumi/heyyumi](https://github.com/hmp-dev/heyyumi-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [ai.seldons/korea-business-trade](https://seldons.ai/mcp) | initialize는 됐는데 tools/list를 못 읽었다(HTTP 400) |
| [com.beauticslab/mcp](https://github.com/websfactory/beauticslab-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.boltena/erp](https://boltena.com/ai) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.empresskorea/kbeauty-agent-commons](https://empresskorea.com/kb-agent-network/) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.goodsaegim/goodsaegim](https://www.goodsaegim.com) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.koreastockcheck/mcp](https://github.com/koreastockcheck/mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [epoko77-ai/korean-bill-debate-mcp](https://github.com/epoko77-ai/korean-bill-debate-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.Mobiss11/daepak-mcp](https://github.com/Mobiss11/daepak-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.lichtsalz/korea-data](https://github.com/lichtsalz/korea-data) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.namen-ceo/factbat-public-record-locator](https://factbat.com/finder?src=mcp-pulsemcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [jeonghwanko/coffee-price-mcp](https://github.com/jeonghwanko/coffee-price-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [kr.wandsol/patent-search](https://mcp.wandsol.kr) | 핸드셰이크는 됐지만 도구 목록에 키가 필요하다 |
| [one.aisa/seo-serp-other-engines](https://aisa.one) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [scvcoder/korean-privacy-law-mcp](https://github.com/scvcoder/korean-privacy-law-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [seolcoding/korean-stat-mcp](https://github.com/seolcoding/korean-stat-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |

## 우리 목록에 넣으려면

**우리에게 올릴 필요가 없다.** [공식 MCP 레지스트리](https://registry.modelcontextprotocol.io)에 등록하면 다음 회차에 자동으로 들어온다. 그쪽이 나은 이유는 우리만 읽는 게 아니라서다.

이미 등록했는데 여기 없다면 **우리 수집기의 버그일 수 있다** — 이슈로 알려 달라. 경쟁 서비스여도 받는다.

제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 우리가 통과시키고 말고 할 것이 없다.

## 고쳤다면 다시 잰다

이 표의 값은 **2026-09-14 그 순간의 기록**이다. 고쳤다면 [이슈](https://github.com/sallim-app/korea-mcp-index/issues)로 알려 달라 — 다음 회차에 다시 잰다. 경쟁 서비스여도 받는다.

**우리가 먼저 다시 두드리지는 않는다.** 바뀐 게 없는 서버를 주기적으로 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다. 그래서 두드리는 대신 신호를 받는다.

이런 것도 같은 창구다 — **우리 쪽 잘못일 수 있다.**

* 분야가 틀렸다 (검색어가 분야를 정하므로 실제로 하는 일과 어긋날 수 있다)
* 주소를 잘못 짚었다 (README에서 추정한 주소라 서버가 아니라 우리가 틀린 것)
* 채점이 틀렸다 — 답변·근거·채점이 [answers/](answers)·[grades/](grades)에 그대로 있으니 어느 문장이 왜 틀렸는지 짚어 달라

**순위는 전원 동시에만 다시 잰다 — 운영자인 우리도 예외가 아니다.** 우리는 고칠 때마다 다시 잴 수 있고 남은 그럴 수 없다. 개별 재측정을 순위에 반영하면 우리 서버만 계단식으로 올라가고 남은 자기 최악의 순간에 박제된다. 실제로 우리는 이 표의 지적을 받아 우리 서버를 고치고 다시 쟀지만 **그 결과를 순위에 넣지 않았다** — 기록은 [answers/](answers)에 ‘정규 회차 아님’으로 남겨 두었다.

## 어떻게 재나

```
collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API
         + 게시 이력 이어받기 — 한 번 실은 서버가 안 잡히면 되살려 다시 판정한다
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

**다른 가중치로 다시 계산해 보라고 표를 펴 두었다** — [axes.csv](axes.csv)는 게시된 모든 축을 서버 1행 × 축 1열로 편 것이고, `python3 recompute.py --verify`는 **이 문서의 머릿수가 원자료에서 그대로 나오는지** 검사한다. 원자료를 올려 두는 것과 그 원자료로 게시본이 재현되는 것은 다른 주장이라 후자를 기계로 건다.

## 믿으면 안 되는 부분

* **정확성은 분야마다 질문 두 개로만 봤다.** 그 두 문항이 그 분야를 대표한다는 보장은 없다. 질문은 공개돼 있으니(`questions.py`) 더 나은 질문을 알려 달라
* **채점자도 모델이다.** 근거를 전부 공개하는 것으로 줄일 수는 있어도 없앨 수는 없다. 답변은 약한 모델(Haiku)이 만들고 채점은 강한 모델(Opus)이 하는데, 그 이유와 실측 근거는 [JUDGING.md](JUDGING.md)에 있다
* **세 번 물었어도 '갈릴 수 있다'까지만 말한다.** 서버마다 세 회차가 무엇이 갈렸고 서버 탓인지 모델 탓인지는 [grades/](grades)의 `재현성`에 적었지만, 몇 %로 갈리는지는 이 표본(질문 두 개 × 3회)으로 못 댄다
* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다 — 무엇을 고정했고 무엇을 언제 왜 바꿨는지는 [PROTOCOL.md](PROTOCOL.md)에 있다. **결과를 본 뒤에 바꾼 적이 한 번 있고**, 그 건도 거기 적어 두었다
* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다
* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다
* **못 잰 것이 더 많다.** 후보 중 76건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다 — 그 밖에 79건은 배포 패키지는 확인했으나 원격 주소가 없어 응답을 못 쟀다

---

## 라이선스

코드·문서·우리가 만든 측정값은 [MIT](LICENSE). **응답 발췌는 각 서버 운영자의 것**이고 우리는 측정 근거로 인용했을 뿐이다 — 400~500자로 제한하고 개인정보 패턴을 가린다. 내려 달라고 하면 내린다.

---

생성 `render_readme.py` · 웹판 <https://mcp-index.sallim.app> · 마지막 측정 2026-09-14 · 운영 [sallim-app](https://github.com/sallim-app)
