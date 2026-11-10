[![한국어](https://img.shields.io/badge/한국어-README-blue)](README.md) [![English](https://img.shields.io/badge/English-README--en-lightgrey)](README-en.md)

# 한국 데이터 MCP — 실측 목록

> 한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 “있다”를 말한다. 이 목록은 **지금 되냐**를 잰다. 2026-11-08 기준 주소를 확인한 216건 중 **182건이 살아있음 확인**, 29건은 **확인 못 함**, 5건만 **죽음 확인**이다. 확인 못 함은 사망이 아니다 — 우리가 못 본 것과 그쪽이 없는 것은 다르다.

> **웹판** <https://mcp-index.sallim.app> — 같은 값을 분야별·서버별 주소로 갈라 놓았다. 기계가 읽을 것은 [index.json](https://mcp-index.sallim.app/index.json)·[llms.txt](https://mcp-index.sallim.app/llms.txt).

| | |
|---|---|
| 비교 가능한 서버 | **140**건 |
| 응답했으나 못 잼(키 필요·규격 이탈) | 29건 |
| 확인 못 함(우리 호출로 확인 실패 — **사망 아님**) | 29건 → [DOWN.md](DOWN.md) |
| 죽음 확인(DNS 미해결·연결 거부) | 5건 → [DOWN.md](DOWN.md) |
| 주제 밖(데이터 제공형 아님) | 13건 |
| 설치형(원격 주소 없음) | 배포 확인 **102**건 · 배포판 없음 137건 · 이름을 못 읽어 미측정 20건 |
| **이번 회차 측정 모집단**(위 줄 전부 — 93건은 주소가 없어 두드리지 못했다) | 569건 — 같은 주소 1건을 합쳐 568줄로 실린다 |
| **재지 않은 후보**(한 번도 두드리지 않음) | 166건 |
| **후보 전체** | 735건 |

**순위 밖 사유** — 두드려 본 서버 중 순위표에 없는 158건에는 전부 왜 없는지를 적는다(웹판 분야 페이지 「순위 밖」 절·서버 상세 페이지, index.json `unranked_reason`). 순위 밖은 나쁘다는 판정이 아니다 — 사유는 가동 측정과 채점 기록에서 기계적으로 옮기고, 이 목록 운영자의 서버도 같은 규칙을 따른다.

| 사유 | 건수 |
|---|---|
| 결제 요구(HTTP 402·x402) — 결제 없이 데이터가 오지 않아 측정 불가 | 5 |
| 키·인증 요구 — 키 없이 부르면 데이터가 오지 않아 측정 불가 | 37 |
| 우리 호출기 한계 — 응답을 우리 쪽이 읽지 못했다(서버 결함 판정 아님) | 3 |
| 도구 목록 없음 — 응답은 했지만 비교할 값을 얻지 못했다 | 1 |
| 분야 교정 — 다른 분야 질문으로 매긴 점수는 쓰지 않는다 | 23 |
| 채점하지 않는 분야 — 이 분야는 아직 순위를 매기지 않는다 | 35 |
| 다음 채점 회차 대기 — 마지막 채점 회차 뒤에 새로 응답·편입됐다 | 8 |
| 주제 밖 — 데이터를 주는 서버가 아니라고 분류됐다 | 13 |
| 전송 방식 불일치 가능 — 우리 호출에 4xx(규격 서버도 주는 코드)가 왔다 | 18 |
| 응답 확인 못 함 — 우리 호출로 확인이 안 됐다(사망 아님) | 10 |
| 죽음 확인 — DNS 미해결·연결 거부처럼 호스트가 없다는 직접 증거가 있다 | 5 |

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
* [디렉토리·개발자도구](#디렉토리개발자도구)
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
| [공공데이터·행정](#공공데이터행정) | [dev.datagokr/datagokr](https://github.com/datagokr-dev/datagokr) | 1건 | 공공데이터포털에서 '무엇을 어디서 어떻게 받나'를 묻는 용도로는 이번 묶음에서 가장 정확하고 절차까지 안내한다. |
| [법령·판례](#법령판례) | [kr.lifelaw/kr-law](https://mcp.lifelaw.kr/) | 0건 | kr.lifelaw/kr-law는 자연어 질문으로 조문을 찾고 현행본을 기본으로 돌려주는 범용 법령 서버로, 두 질문 모두 세 번 다 맞고 근거가 분명한 답을 냈다. |
| [금융·증시](#금융증시) | [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 1건 | 삼성전자 실적처럼 개별 종목의 공시 재무를 묻는 용도로는 이번 묶음에서 가장 믿을 만하다 — 누계·잠정·연결을 도구가 먼저 갈라 주고 DART 접수번호까지 붙인다. |
| [부동산](#부동산) | [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 | 3건 | 강남구 실거래 시세(월별 추이·평형대별 중앙값)와 서울 경매 유찰 물건을 둘 다 한 서버에서 출처·단위·총계 공시와 함께 받을 수 있고, 재호출 값과 다른 서버 값이 맞아떨어졌다. |
| [커머스·생활](#커머스생활) | [io.github.aminpiano/nara-tour](https://github.com/aminpiano/naratour-mvp) | 0건 | 수원·경기 남부 단체여행 여행사 한 곳의 회사 정보와 카카오 상담 링크만 주는 좁은 범위의 서버다. 상품·판매·예약 데이터는 없지만 없다는 것이 출력에서 분명해 답변이 정직했고, 이 여행사에… |

종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.

## 우리가 지는 항목

**유리한 축만 재면 그 순위는 판정이 아니라 광고지다.** 원격 MCP인 우리가 불리한 축을 같이 잰다 — 무엇을 잴지는 결과를 보기 전에 [신뢰 규약](PROTOCOL.md)에 고정했고, 여기서 뺄 수 없게 회귀 테스트로 묶어 두었다.

| 축 | 이 목록 전체 | 운영자(🏠) |
|---|---|---|
| 셀프호스팅 | 배포판 확인 131건 · 소스만 323건 · 미확인 114건 | **소스만** 2건 — 그리고 클론해도 답이 안 나온다 · **소스 비공개 1건**(korea-stay) — 이 축에서 우리가 제일 나쁘다 |
| 오픈소스 | MIT 232건, Apache-2.0 22건, AGPL-3.0 3건, ISC 1건 · 라이선스 확인 못 함 310건 | MIT — **이 축에서는 우리가 지지 않는다**. 단 korea-stay는 저장소가 없어 라이선스도 없다 |
| 무료 한도 | 스스로 공시한 서버 1건 | 그 1건이 우리다 — 도구 57종 중 **10종 유료** |

* **셀프호스팅은 우리가 제일 나쁘다.** 우리 저장소는 MIT로 열려 있지만 도구들이 우리 비공개 데이터 API를 부르므로 [클론해서 띄우면 거의 다 실패한다](https://github.com/sallim-app/korea-realty) — 우리 README가 먼저 적어 둔 것이고, 여기서도 적는다. 축의 값(`source_only`)보다 실질이 나쁘다
* **`소스만`은 “띄우면 같은 답이 나온다”가 아니다.** 코드가 공개돼 있다는 뜻일 뿐이고, 남의 서버도 우리처럼 자기 데이터에 묶여 있을 수 있다 — 그건 우리가 재지 않았다
* **`라이선스 확인 못 함`을 “오픈소스 아님”으로 읽지 말라.** 저장소가 비공개거나 지워졌거나 이름이 바뀐 것도 여기 들어온다. 다만 **공개 저장소인데 라이선스 파일이 없는 것**은 기본값이 저작권 전부 유보라 실제로 가져다 쓸 수 없다
* **유료 공시가 1건뿐인 것은 나머지가 무료라는 뜻이 아니다.** 밖에서는 판정할 수 없다. 밝힌 쪽만 표에 유료 게이트가 보이고, 지금 그 쪽은 우리다

축이 모자란다고 보면 다른 가중치로 직접 재계산할 수 있다 — [axes.csv](axes.csv)가 서버 1행 × 축 1열이고, `python3 recompute.py --weights tool_count=1,warm_ms=-0.01`이 그 계산기다. **그 결과는 우리 순위가 아니다** — 지표로 줄 세우는 방식은 우리가 실측으로 폐기했다([JUDGING.md](JUDGING.md)).

## 공공데이터·행정 (Public Data)

> 질문2(공공데이터포털 대기질 데이터 위치)는 datagokr-dev/datagokr와 kloud80/datagokr-mcp가 세 회차 모두 에어코리아 API와 신청 절차까지 정확히 답했고, 나머지 카탈로그형 서버는 일반 낱말 '대기질' 검색에서 대표 데이터셋을 놓쳤다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 8건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [dev.datagokr/datagokr](https://github.com/datagokr-dev/datagokr)<br><sub>지난 회차 표기 `datagokr-dev/datagokr` → `dev.datagokr/datagokr` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 6 | 137 | 145 | 100% | 100% | 1 |
| [kloud80/datagokr-mcp](https://github.com/kloud80/datagokr-mcp) | 6 | 36 | 36 | 100% | 100% | 1 |
| [Dayoooun/korea-stats-mcp](https://github.com/Dayoooun/korea-stats-mcp) | 14 | 269 | 488 | 100% | 0% | 3 |

1. **datagokr/datagokr** — 공공데이터포털에서 '무엇을 어디서 어떻게 받나'를 묻는 용도로는 이번 묶음에서 가장 정확하고 절차까지 안내한다. 외부 링크형 자료는 실제 값을 읽지 못하므로 '수치가 어떻게 변했나'에는 직접 답하지 못한다는 점을 알고 쓰면 된다.
2. **kloud80/datagokr-mcp** — 공공데이터포털 데이터셋을 찾고 실측 필드·표본값까지 보여주는 용도로 강하며 대기질처럼 '어디서 받나' 질문에는 정확하다. 표본값을 수치 답으로 쓸 때는 데이터셋이 관측인지 추계인지 직접 확인해야 한다.
3. **Dayoooun/korea-stats-mcp** — KOSIS 기반 통계 수치·시계열이 필요하면 이 묶음에서 유일하게 실제 연도별 값을 주는 서버이며, 지역 인자를 정확히 넣으면 값도 맞다. 공공데이터포털 카탈로그 안내 용도는 아니다.
4. **hike-lab/public-data-lens** — 공공데이터 카탈로그의 메타데이터를 정확히 돌려주지만, 일반 낱말 검색에서 대표 데이터셋이 상위에 안 올라오는 경우가 있어 '어디서 받나'의 1순위 답으로는 불안하다. 데이터셋 비교·구조 확인 같은 카탈로그 분석 용도에 더 맞다.
5. **star365/data** — 자체 적재한 지역 데이터와 data.go.kr 카탈로그 검색을 함께 주지만, 이 두 질문에서 적재 데이터는 쓸모가 없었고 카탈로그 검색도 대표 데이터셋을 놓치는 일이 잦았다. 공공데이터 위치 안내용으로는 datagokr 계열 서버보다 덜 믿을 만하다.
6. **SongT-50/korean-public-data-mcp** — 사업자등록·아파트 실거래·날씨·대기질·한국은행 지표 몇 가지를 한데 묶은 소형 공공데이터 서버로, 대기질 현황은 정확하게 주지만 인구 통계는 없고 응답에 원천 데이터셋 출처를 적지 않아 '어디서 받나'류 질문에는 답하지 못한다. 서울·주요 지역 대기질 현황을 빠르게 볼 용도로는 쓸 만하다.
7. **lazymac2x/govdata-korea** — 지역별 인구·환율·공휴일 같은 정적 참조값을 빠르게 주는 소형 서버이며 추이나 데이터 위치 안내는 못 한다. 인구값의 기준 시점이 KOSIS 연간값과 맞지 않아 보이므로 정밀한 수치 근거로 쓰기 전에 원천 대조가 필요하다.
8. **pipeworx-io/seoul-data** — 서울 자치구 실시간 대기질·부동산 실거래·문화행사와 서울 열린데이터광장 통과 조회를 갖췄지만, 서비스명을 모르면 통과 조회를 못 쓰고 라우터가 자기 팩의 서울 데이터를 모른다고 답해 인구 추이 질문은 세 번 모두 실패했다. 서울 대기질 현황처럼 전용 도구가 있는 질문에만 권할 만하며, 익명 일일 호출 한도(채점 중 '72/50' 안내)가 낮다.
9. **pipeworx-io/korea-tenders** — 이 서버의 고유 도구는 나라장터 입찰·낙찰·조달업체 조회이고 나머지는 Pipeworx 공용 카탈로그라, 인구·대기질 같은 일반 공공데이터 질문에는 국가 단위 대체값 이상을 주지 못한다. 공공조달 입찰 검색 용도로만 고려할 서버이며 낙찰 결과 도구는 자기 키(BYOK)가 필요하다.
10. **pipeworx-io/kosis-kr** — KOSIS 통계표 검색·시계열 조회 도구는 제대로 갖췄지만 키 없이는 하나도 돌지 않아, 이번 회차에서 서울 인구 질문에 실제 값을 낸 적이 없다. 자기 KOSIS 키를 _apiKey로 넣을 수 있는 사용자에게만 쓸모가 있다.
11. **kgu25kkwak/JOBWAY-API-MCP** — 공공채용 스냅샷(2025-12-31·2023-09-01 시점)·충남/전국 고용 통계·공주시 버스를 묶은 지역 특화 서버로, 시점·범위 공시가 정직하다. 서울 인구나 대기질 같은 전국 공공데이터 질문에는 답이 없고 공주·충남 고용·교통을 볼 때 쓸 서버다.
12. **hjsh200219/korea-public-data-mcp** — 법령·관세·DART·조달·관광·의약 등 여러 공공 API를 묶은 서버지만 인구 통계와 공공데이터포털 카탈로그는 다루지 않는다. 이 두 질문 같은 범용 공공데이터 탐색 용도로는 쓸 수 없다.
13. **boim/vendors** — 조달청 나라장터 납품 실적·국세청 사업자 상태로 만든 업체 카드와 공공 입찰공고·상가 데이터를 찾는 서버로, 출처·기준일 표기가 충실하다. 인구·대기질 같은 일반 공공 통계 질문에는 답이 없고 공공조달 업체·입찰을 찾을 때 쓸 서버다.
14. **donghyeon01/kr-public-mcp** — 나라장터 입찰공고·사전규격·낙찰 이력 전용 서버로(사전규격·낙찰 집계·알림은 Pro 전용), 인구·대기질 같은 일반 공공 통계에는 답이 없다. 공공조달 입찰을 찾는 용도로만 고를 서버다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 11건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [hike-lab/public-data-lens](https://github.com/haklaekim/public-data-lens)<br><sub>카탈로그형 — 값이 아니라 데이터셋 위치를 준다</sub><br><sub>지난 회차 표기 `haklaekim/public-data-lens` → `hike-lab/public-data-lens` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 9 | 25 | 25 | 100% | 100% | 1 |
| [site.star365/data](https://data.star365.site/) | 10 | 116 | 111 | 100% | 100% | 1 |
| [io.github.SongT-50/korean-public-data-mcp](https://github.com/SongT-50/korean-public-data-mcp) | 6 | 158 | 179 | 100% | 0% | 0 |
| [io.github.lazymac2x/govdata-korea](https://github.com/lazymac2x/govdata-korea-api) | 6 | 124 | 113 | 100% | 0% | 1 |
| [io.github.pipeworx-io/seoul-data](https://github.com/pipeworx-io/mcp-seoul-data) | 48 | 64 | 54 | 100% | 100% | 2 |
| [io.github.pipeworx-io/korea-tenders](https://github.com/pipeworx-io/mcp-korea-tenders) | 49 | 57 | 66 | 100% | 100% | 1 |
| [io.github.pipeworx-io/kosis-kr](https://github.com/pipeworx-io/mcp-kosis-kr) | 47 | 54 | 68 | 100% | 100% | 0 |
| [kgu25kkwak/JOBWAY-API-MCP](https://github.com/kgu25kkwak/JOBWAY-API-MCP) | 7 | 45 | **769** | 100% | 100% | 1 |
| [hjsh200219/korea-public-data-mcp](https://github.com/hjsh200219/korea-public-data-mcp) | 19 | 518 | 744 | 100% | 100% | 0 |
| [io.boim/vendors](https://github.com/kikiyop1101/boim-mcp) | 6 | 49 | 53 | 100% | 100% | 0 |
| [io.github.donghyeon01/kr-public-mcp](https://github.com/donghyeon01/kr-public-mcp) | 5 | 49 | 56 | 100% | 0% | 0 |

</details>

<details><summary>채점하지 않은 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.ChloePark85/kr-groundtruth](https://kr-groundtruth-mcp.vercel.app) | 8 | 413 | 434 | 100% | 100% | — |

</details>

**분야 교정 8건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [app.apick/all](https://github.com/lead788/apick-mcp) | 기타 | “도구 115종이 계좌·신분증 진위확인, OCR, 웹검색, 영상·문서 변환 같은 유료 범용 API이고 인구 통계나 공공데이터포털 목록을 다루는 도구는 없다…” |
| [app.apick/business](https://github.com/lead788/apick-mcp) | 커머스·생활 | “상거래·물류 데이터형 서버로 이 분야 두 질문은 설계 범위 밖이며…” |
| [bhyunco/korea-holiday-mcp](https://github.com/bhyunco/korea-holiday-mcp) | 커머스·생활 | “도구 6종이 모두 공휴일 확인·연휴·영업일 계산이라 일상 일정 계산용이며 공공데이터 조회 도구가 없다.” |
| [com.easykmarket.vote/votebox-law](https://vote.easykmarket.com/developers) | 법령·판례 | “도구가 법령 조문 원문·의결정족수·전자투표 근거 조문·가결 판정으로 이뤄진 단체 의결 법령 서버다.” |
| [io.github.SongT-50/korean-agriculture-mcp](https://github.com/SongT-50/korean-agriculture-mcp) | 커머스·생활 | “도구 6종이 모두 도매시장 농산물 경매가격·시장별 비교·가격 추이 조회라 생활 물가 영역이다.” |
| [io.github.pipeworx-io/ecos-kr](https://github.com/pipeworx-io/mcp-ecos-kr) | 금융·증시 | “이 팩의 고유 도구 네 개가 모두 한국은행 ECOS 경제통계(통화·환율·금리·물가·GDP) 조회라 공공데이터·행정보다 금융·증시 분야의 서버다.” |
| [kr.eocpa/mydart](https://github.com/taesueocpa/mydart-mcp) | 금융·증시 | “도구 전부가 DART 전자공시의 기업 공시·재무제표·감사보고서 조회라 공공데이터·행정이 아니라 금융·증시 분야의 서버다.” |
| [kr.ibtcc/competition-ratio](https://github.com/jojunho74/hometest) | 기타 | “도구가 공기업 채용 경쟁률·채용 일정·공고와 어학 점수 환산이라 행정 데이터 조회가 아니라 취업 준비 도구다.” |

## 법령·판례 (Law)

> 두 질문 모두에서 실제로 잘 답한 곳은 kr.lifelaw/kr-law였고, 같은 법제처 원문을 주는 io.github.chrisryugj/korean-law-mcp와 kang-aco/korean-law(묶음 이름 chrisryugj/korean-law-mcp, korean-law-mcp.fly.dev — gomdori 주소의 io.github.chrisryugj/korean-law-mcp와는 다른 서버다)가 뒤를 이었다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 1건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.lifelaw/kr-law](https://mcp.lifelaw.kr/) | 21 | 81 | 241 | 100% | 100% | 0 |
| [io.github.chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 238 | 229 | 100% | 100% | 1 |
| [kang-aco/korean-law](https://github.com/kang-aco/korean-law)<br><sub>지난 회차 표기 `chrisryugj/korean-law-mcp` → `kang-aco/korean-law` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 10 | 296 | 228 | 100% | 100% | 3 |

1. **lifelaw/kr-law** — kr.lifelaw/kr-law는 자연어 질문으로 조문을 찾고 현행본을 기본으로 돌려주는 범용 법령 서버로, 두 질문 모두 세 번 다 맞고 근거가 분명한 답을 냈다. 현행 조문을 빠르게 확인하는 용도라면 이 분야에서 바로 쓸 만하다.
2. **chrisryugj/korean-law-mcp** — io.github.chrisryugj/korean-law-mcp는 법제처 원문 조문을 정확히 꺼내 주는 범용 법령 서버로 두 질문 모두 실질적으로 맞는 답의 재료를 줬다. 조문 조회 기본값이 시행예정본이라 '현행' 질문에서는 경고 줄을 보고 시점을 지정해 다시 불러야 하며, 이 점만 감안하면 일반 법령 조회에 쓸 만하다.
3. **kang-aco/korean-law** — kang-aco/korean-law는 법제처 원문을 조문 단위로 정확히 꺼내 주고 efYd로 시점 지정 조회도 되는 범용 법령 서버로, 두 질문 모두 실질적으로 맞는 답을 냈다. 다만 조문 조회 기본값이 시행예정본이라 '현행'을 물을 때는 efYd를 지정하거나 경고 줄을 확인해야 하고, 법률에서 시행령으로 내려가는 단계를 모델이 빠뜨리면 답이 얕아진다.
4. **sallim/contract-compass** — app.sallim/contract-compass는 공공계약(국가계약법·지방계약법)과 세법 114개 법령만 담은 좁은 범위의 서버로, 그 안의 질문에는 법률 위임 근거와 시행령 원문을 정확히 묶어 답한다. 도로교통법 같은 범위 밖 법령은 못 본다고 분명히 거절하므로, 공공계약 실무용으로는 쓸 만하고 범용 법령 검색용으로는 맞지 않는다.
5. **leejaejeon/beobi-daneun-got** — 한국어 조문 원문을 개정 이력 표시와 함께 돌려줘 형량처럼 한 조문에 다 있는 질문에는 정확하게 답한다. 다만 검색이 법률과 시행령·특례규정을 섞어 핵심 시행령 조문을 놓치고, 시행 예정판을 현행 표시 없이 내줘 시행일을 잘못 알릴 수 있어 '지금 무엇이 시행 중인가'를 판단하는 데는 시행일 재확인이 필요하다.
6. **koreanics/korea-law-acts-and-bills** — 현행 조문을 공포일·시행일과 출처 URL이 붙은 영문 번역으로 정확히 돌려주는 서버이며, 재호출한 조문 본문은 법제처 현행본과 일치했다. 다만 비공식 영문 번역이라 한국어 법률용어로 되옮길 때 오역(수의계약→협상계약)과 수치 혼동이 생기기 쉽고 검색도 영어 질의가 필요해, 한국어 사용자가 형량·금액을 그대로 옮겨 쓰기에는 원문 대조가 필요하다.
7. **aefact/aefact** — 법령의 현행 시행일·공포번호·소관부처와 곧 시행될 개정 내용을 법제처 원자료 인용과 함께 돌려주는 '언제 무엇이 바뀌나' 추적 서버로, 이번 재호출 값은 법제처 현행본과 맞았다. 조문 본문과 형량은 담지 않으므로 '지금 처벌 기준이 무엇인가'에는 답하지 못하고, 개정 시행일 확인 용도로 쓰는 것이 맞다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 4건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [app.sallim/contract-compass](https://github.com/sallim-app/contract-compass) 🏠 | 11 | 43 | 62 | 100% | 100% | 0 |
| [io.github.leejaejeon/beobi-daneun-got](https://jake-asus.tail2c6a90.ts.net) | 9 | 885 | 1383 | 100% | 100% | 2 |
| [com.koreanics/korea-law-acts-and-bills](https://koreanics.com/mcp-server/) | 7 | 244 | 250 | 100% | 100% | 4 |
| [site.aefact/aefact](https://github.com/cizion/aefact-mcp) | 14 | 274 | 279 | 100% | 100% | 2 |

</details>

<details><summary>채점하지 않은 3건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 235 | 245 | 76% | 0% | — |
| [io.github.pipeworx-io/kr-law](https://github.com/pipeworx-io/mcp-kr-law) | 47 | 63 | 68 | 100% | 100% | — |
| [io.github.peter120525-cmd/lawmadi-os](https://lawmadi.com) | 19 | 254 | 233 | 100% | 0% | — |

</details>

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 기타 | “이 서버는 창업 관련 법령과 K-Startup 지원사업을 다루는 도구라 국가계약법·도로교통법 질문에는 맞지 않으며…” |

## 금융·증시 (Finance)

> 두 질문을 모두 제대로 덮은 서버는 없었고, 실적은 aikstockdata·datasinking, 시총 순위는 pipeworx kr-equities·dart-kr·maedong이 각각 맞혀 질문별로 강자가 갈렸다. 실적 질문에서 갈린 것은 '최근'의 기간 정의였다 — 2026 반기 누계와 3분기 잠정까지 연결 기준으로 가른 곳과, 1년 전 연간치나 분기 단독치를 반기로 오표기한 곳의 차이다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 4건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 27 | 31 | 100% | 100% | 1 |
| [io.github.pipeworx-io/kr-equities](https://github.com/pipeworx-io/mcp-kr-equities) | 50 | 56 | 51 | 100% | 100% | 2 |
| [io.github.heubme2020/datasinking](https://github.com/heubme2020/datasinking) | 8 | 416 | 71 | 100% | 100% | 1 |

1. **aikstockdata/mcp** — 삼성전자 실적처럼 개별 종목의 공시 재무를 묻는 용도로는 이번 묶음에서 가장 믿을 만하다 — 누계·잠정·연결을 도구가 먼저 갈라 주고 DART 접수번호까지 붙인다. 시총 순위 같은 시장 전체 목록은 데이터는 있으나 list_stocks의 기본값 때문에 모델이 잘 못 찾으므로, 그 용도로 쓰려면 filter=all·sort=cap을 명시해야 한다.
2. **pipeworx-io/kr-equities** — 코스피·코스닥 시총 순위와 종목 시세를 당일 종가 기준으로 정확하게 주며 세 번 물어 세 번 같았다. 기업 재무는 범위 밖이고, 게이트웨이 라우터가 자매 팩(dart-kr)의 재무 도구를 안내하지 못하므로 실적 질문에는 다른 서버를 써야 한다.
3. **heubme2020/datasinking** — DART 정기보고서 원문을 섹션 단위로 주는 서버라 삼성전자 같은 상장사 실적을 공시 원문 그대로, 연결·기간 구분까지 확인할 수 있다. 시세·시가총액은 다루지 않으므로 증시 순위 질문에는 쓸 수 없다.
4. **maedong/maedong** — 국내 증시 스크리너 목록(시가총액 상위·거래대금·저PER 등)과 그 성과를 주는 서버라 시가총액 상위 같은 시장 질문에는 바로 쓸 만하다. 개별 기업 재무 실적은 다루지 않고, 필요한 목록이 slug 뒤에 있어 모델이 한 번 더 찾아야 한다.
5. **pipeworx-io/dart-kr** — 시총 순위처럼 표로 떨어지는 시장 데이터는 정확하고 일관되지만, DART 재무는 분기 단독치를 반기로 보이게 돌려줘 실적 질문에 기간이 틀린 답을 만든다. 이 끝점은 dart-kr 팩이지만 수천 개 범용 도구가 함께 노출되는 게이트웨이라, 한국 공시 재무를 물을 때는 누계 여부를 다른 원천으로 확인해야 한다.
6. **Mrbaeksang/korea-stock-analyzer-mcp** — 상장사의 연간 감사 재무와 비율·리스크 신호를 보는 용도에는 값이 정확하고 일관되지만, 분기·반기 실적과 시장 전체 순위는 범위 밖이다. get_quote의 시가총액이 null로 나오는 결함이 있어 시세 쪽은 아직 쓰기 어렵다.
7. **kmgvv23/stock-data-mcp** — DART·KRX 원천을 그대로 내주는 얇은 래퍼라 인자를 정확히 넣으면 값은 맞고, 반기 누계(thstrm_add_amount)까지 원문 그대로 준다. 다만 최신 기간 기본값이 없고 시총 도구가 정렬·건수 제한 없이 수백 KB를 쏟아내 모델이 잘린 출력으로 오답을 내기 쉬우므로, 인자를 직접 지정할 수 있는 숙련 사용자 용도에 가깝다.
8. **moss/alpha-mcp** — 유튜브·뉴스 발화를 엮은 AI 합성 이벤트 서버라 삼성전자 분기 실적 같은 헤드라인 수치는 맞게 잡혀 있지만, 확정치·전망·오기가 한 별칭 목록에 섞여 있어 재무 수치의 원천으로 쓰기엔 근거가 약하다. 시장 분위기·이슈 흐름을 훑는 용도에 맞고, 종목 재무나 시총 순위는 범위 밖이다.
9. **jsymen1290/pokt-agent** — DART 공시 목록·정정 추적과 금리·환율·수출·아파트 실거래를 무료로 주는 금융 데이터 서버로, 공시 메타데이터는 정확했다. 다만 실적 수치는 kr_figure_check의 검증 결과(연간 주요계정)로만 우회해 얻을 수 있고 분기 실적·시가총액 순위 도구는 없어, 이 두 질문에는 직접 답하지 못한다.
10. **SongT-50/korean-stock-mcp** — 국내 종목 시세·지수·종목 비교는 KRX 값과 맞게 주지만 데이터가 하루 이상 늦을 수 있고, 재무 실적과 시가총액 순위 도구는 없다. 특정 종목 시세 확인 용도로는 쓸 만하나 '상위 종목' 같은 시장 전체 질문에는 모델이 엉뚱한 순위를 지어내게 만든다.
11. **trading/community** — 국내 종목 시세·업종 지도·거래대금 상위·해외 선행지표를 키 없이 주는 커뮤니티 서버지만 재무 실적과 시가총액 순위는 없다. 시장 분위기 확인용으로는 쓸 수 있으나 시총 순위 질문에는 잘못된 목록을 낳기 쉽다.
12. **agentmaru/agentmaru** — 거시지표(CPI·환율·GDP)·해운 운임·금융 리서치 출처 안내와 KED 수출 추정치를 다루는 서버라 개별 상장사 실적이나 시세 순위 용도에는 쓸 수 없다. 금융 리서치의 출처·접근 조건을 찾는 용도로 범위가 좁은 서버다.
13. **dartpointai/dartpoint-mcp** — 도구 목록은 DART 기업정보·재무·주가·감성까지 넓게 갖췄지만 이번 회차에는 기업 코드 조회부터 모든 호출이 오류 표시 없는 빈 응답이라 실사용이 불가능했다. 빈 결과를 isError 없이 돌려주므로 모델이 '자료 없음'으로 오독할 위험도 있다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 10건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.maedong/maedong](https://maedong.kr) | 6 | 313 | 551 | 100% | 100% | 1 |
| [io.github.pipeworx-io/dart-kr](https://github.com/pipeworx-io/mcp-dart-kr) | 49 | 60 | 84 | 100% | 100% | 3 |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 212 | 545 | 100% | 100% | 1 |
| [kmgvv23/stock-data-mcp](https://github.com/kmgvv23/stock-data-mcp) | 42 | 463 | 508 | 100% | 0% | 3 |
| [land.moss/alpha-mcp](https://github.com/MosslandOpenDevs/alpha-mcp)<br><sub>지난 회차 표기 `MosslandOpenDevs/alpha` → `land.moss/alpha-mcp` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 12 | 30 | 39 | 100% | 0% | 0 |
| [io.github.jsymen1290/pokt-agent](https://github.com/jsymen1290/pocket-agents) | 12 | 58 | 50 | 100% | 100% | 0 |
| [io.github.SongT-50/korean-stock-mcp](https://github.com/SongT-50/korean-stock-mcp) | 7 | 178 | 175 | 100% | 0% | 2 |
| [kr.pe.trading/community](https://trading.pe.kr/join) | 32 | 54 | 56 | 100% | 100% | 3 |
| [com.agentmaru/agentmaru](https://agentmaru.com/connect) | 15 | 45 | 49 | 100% | 100% | 2 |
| [dartpointai/dartpoint-mcp](https://github.com/dartpointai/dartpoint-mcp) | 37 | 26 | 25 | 100% | 0% | 0 |

</details>

<details><summary>채점하지 않은 17건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [MarcoYou/open-proxy-mcp](https://github.com/MarcoYou/open-proxy-mcp) | 37 | 227 | 224 | 100% | 0% | — |
| [io.stockdrifts/mcp](https://github.com/Stockdrifts/stockdrifts-mcp) | 32 | 909 | 919 | 100% | 0% | — |
| [space.finquest/finquest](https://mcp.finquest.space/) | 31 | 107 | 134 | 100% | 100% | — |
| [io.github.jsymen1290/pokt-agent-x402](https://x402.pokt-agent.com/) | 29 | 35 | **136** | 100% | 100% | — |
| [kr.gronox/finbridge](https://github.com/Jakechj/finbridge-mcp) | 27 | 77 | 106 | 100% | 100% | — |
| [eddmpython/dartlab](https://github.com/eddmpython/dartlab) | 26 | — | 655 | 100% | 0% | — |
| [emceeKim/korea-finance-mcp](https://github.com/emceeKim/korea-finance-mcp) | 25 | 156 | 170 | 100% | 100% | — |
| [io.github.bakyang2/kr-crypto-intelligence](https://github.com/bakyang2/kr-crypto-intelligence) | 18 | 105 | 142 | 100% | 100% | — |
| [io.github.bubilife1202/crossfin](https://github.com/bubilife1202/crossfin) | 16 | 154 | 394 | 100% | 0% | — |
| [com.asia-pulse/asia-pulse](https://asia-pulse.com) | 10 | 103 | 102 | 100% | 100% | — |
| [chromato99/krx-rule-mcp](https://github.com/chromato99/krx-rule-mcp) | 7 | 46 | 57 | 100% | 0% | — |
| [com.airblockfz/stock-signal-kr](https://airblockfz.com) | 5 | 42 | 49 | 100% | 0% | — |
| [io.github.eddyParkGG/bamsai](https://github.com/eddyParkGG/bamsaikr) | 5 | 132 | 86 | 100% | 0% | — |
| [kr.co.knockwatch/coin-check](https://knockwatch.co.kr/ai) | 5 | 460 | 693 | 100% | 100% | — |
| [kr.eocpa/myfss](https://eocpa.kr/myfss) | 4 | 118 | 121 | 100% | 100% | — |
| [xyz.comepass/korean-companies](https://agents.comepass.xyz) | 4 | 47 | **153** | 100% | 100% | — |
| [io.github.jaypark8780/baedang](https://baedang.info) | 3 | 22 | 24 | 100% | 100% | — |

</details>

**분야 교정 4건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [app.apick/finance](https://github.com/lead788/apick-mcp) | 핀테크·인증 | “이름만 finance일 뿐 실제로는 은행 계좌 검증(1원 인증·실명조회) 서비스로 한국 증시와 주제가 다르며…” |
| [bootpay/bootpay-mcp](https://github.com/bootpay/bootpay-mcp) | 핀테크·인증 | “도구 9종이 전부 Bootpay 결제 연동용 SDK 버전·문서 검색·설정 체크리스트·CSP 허용목록이고 시세·공시 데이터 도구가 없다.” |
| [com.oilpicker/oilpicker](https://oilpicker.com/ai) | 커머스·생활 | “도구 5종이 지역화폐 주유 할인율·실질 연료가 계산·가맹점 검색·지역 목록·링크 생성뿐이고 증권 데이터 도구가 없다.” |
| [kr.vlsi/vlsi-korea](https://mcp.vlsi.kr/) | 미디어·뉴스 | “도구 대부분(기사 검색·최신 기사·일일 브리핑·뉴스 피드·용어집·Q&A·채용지수)이 반도체 산업 뉴스·지식 서비스이고 증시 도구는 반도체 관련 약 113종목의 지연 종가와 변동률 목록뿐이라 금융·증시 서버로 보기 어렵다.” |

## 부동산 (Real Estate)

> 실거래와 경매 두 질문에 모두 데이터로 답한 곳은 korea-realty와 richgo 둘뿐이었다. 그중 실거래 원값과 경매 유찰 물건을 재호출 값 그대로 낸 곳은 korea-realty였다. 실거래 쪽은 대부분 서버가 같은 값을 냈다(강남구 10월 중앙값 25억원·79건이 서버 간에 맞아떨어졌다). 갈린 것은 답변 모델이 만원 맨숫자를 열 배 틀리게 옮겼는지, 그리고 월별 흐름을 주는 도구가 있었는지였다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 1건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) 🏠 <sub>무료 47/57</sub> | 57 | 57 | 56 | 100% | 100% | 3 |
| [ai.richgo.m/richgo](https://m.richgo.ai/developers/mcp.html) | 15 | 27 | 22 | 100% | 100% | 4 |
| [io.github.hoftlab/kr-realestate-mcp](https://kr-realestate-mcp.gamto.workers.dev/) | 14 | 90 | 96 | 100% | 100% | 6 |

1. **sallim/korea-realty** — 강남구 실거래 시세(월별 추이·평형대별 중앙값)와 서울 경매 유찰 물건을 둘 다 한 서버에서 출처·단위·총계 공시와 함께 받을 수 있고, 재호출 값과 다른 서버 값이 맞아떨어졌다. 다만 추이 도구와 수준 도구가 나뉘어 있고 경매 목록의 종류 필터가 기본으로 꺼져 있어서, 답변 모델이 도구를 하나만 부르거나 필터를 빠뜨리면 질문과 어긋난 답이 나온다. 부동산 실거래·경매를 함께 보는 용도에 쓸 만하지만, 아파트 경매를 찾을 때는 종류를 꼭 지정해야 한다.
2. **m/richgo** — 구·동 단위 아파트 시세 흐름(리치고 추정 평당 시세, 주·월·연 변동, 동별 순위)은 재호출해도 같은 값으로 안정적으로 나오지만, 실거래가가 아니라 추정 시세라는 점을 답변이 놓치기 쉽다. 경매는 서울 물건 목록을 주지만 유찰 횟수 필터·정렬이 없고, 틀린 인자를 조용히 무시해서 '유찰 많은 물건' 질문에는 믿고 쓰기 어렵다. 시세 흐름을 보는 용도에는 쓸 만하고, 경매 선별에는 부족하다.
3. **hoftlab/kr-realestate-mcp** — 강남구 3개월 실거래를 월별·동별·면적대별·단지별로 한 번에 주고, 신고 지연 미완 달을 표시하며, 다른 서버와 값도 맞는다. 다만 금액이 만원 맨숫자라 답변 모델이 열 배 틀리게 옮기기 쉽고, 변화율 설명과 실제 계산이 어긋난다. 경매는 다루지 않으므로 실거래 시세 조회용으로만 쓰고, 금액 단위는 답변에서 꼭 다시 확인하는 것이 좋다.
4. **goyo-studio/korean-real-estate-mcp** — 국토부 아파트 매매 실거래를 자연어 주소 하나로 바로 집계해 주고 기간·건수·잘림 여부(truncated)를 함께 밝히므로, 특정 지역의 최근 거래 사례와 12개월 평균을 확인하는 용도로는 쓸 만하다. 월별 추이를 주지 않아 '요즘 오르나 내리나'에는 답이 얕고, 경매·공매는 범위 밖이다.
5. **reevl/reevl-mcp** — 전국 아파트 단지를 대표가·거래량·전세가율·학군·AI 예측 같은 축으로 거르고 단위를 출력에 붙여 주므로, 조건에 맞는 단지를 고르는 용도로는 쓸 만하다. 대표가의 기준 시점이 출력에 없고 구 단위 추이를 주지 않아 '요즘 시세가 어떤가'에는 간접적으로만 답하며, 경매는 범위 밖이다.
6. **pagong/auctions** — 법원경매 물건을 사건번호·감정가·최저가·현재 사이클 유찰 횟수와 정본 URL로 주고 계산값이 상위 3건만 채워진다는 사실도 공시해, 바른 인자로 부르면 서울·강남구 아파트 경매를 찾는 용도로 쓸 수 있다. 다만 모르는 인자를 오류 없이 버려 필터가 빠진 결과를 정상 응답처럼 돌려주고, 유찰 횟수 정렬이 없으며 한 번에 10건까지만 주므로 '유찰 많은 것'을 전체에서 고르려면 여러 번 나눠 불러야 한다. 실거래 시세는 범위 밖이다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 3건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.goyo-studio/korean-real-estate-mcp](https://github.com/goyo-studio/korean-real-estate-mcp) | 1 | 112 | 277 | 100% | 0% | 2 |
| [kr.co.reevl/reevl-mcp](https://reevl.co.kr/mcp)<br><sub>지난 회차 표기 `exclusiveyon-a11y/reevl-plugins` → `kr.co.reevl/reevl-mcp` — 같은 서버로 이었고, 등수는 옛 이름으로 받은 것이다</sub> | 7 | 33 | 30 | 100% | 100% | 2 |
| [net.pagong/auctions](https://www.pagong.net) | 7 | 163 | 178 | 100% | 100% | 3 |

</details>

<details><summary>채점하지 않은 2건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.seoulstart/seoulstart](https://seoulstart.com/connect) | 7 | 245 | 242 | 100% | 100% | — |
| [com.airblockfz/seoul-apt-signal](https://airblockfz.com)<br><sub>실거래가가 아니라 산식 미공개 매매신호. 분석 도구는 HTTP 402(사실상 유료)</sub> | 6 | 30 | **91** | 100% | 0% | — |

</details>

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [io.github.richard-kim-79/jejusns](https://jejusns.com) | 커머스·생활 | “도구 17개 중 부동산은 제주 매물 검색·저장과 제주 아파트 시세 통계 3개뿐이고 나머지는 게시글·피드·채용·병의원·관광 통계라, 이 서버는 부동산 서버가 아니라 제주 지역 생활 커뮤니티 서버다.” |

## 세금·재정 (Tax)

후보가 4건뿐이라 순위를 매기지 않았다. 4개 중 4개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.xdata/xdata-mcp](https://xdata.kr) | 283 | 277 | 246 | 100% | 100% | — |
| [io.github.minsooparkk/korea-tax-law-mcp](https://github.com/minsooparkk/korea-tax-law-mcp) | 20 | 153 | 113 | 100% | 100% | — |
| [kr.co.accountingwiki/accountingwiki](https://accountingwiki.co.kr/about#mcp) | 11 | 261 | 436 | 100% | 100% | — |

## 지도·주소 (Maps)

후보가 4건뿐이라 순위를 매기지 않았다. 4개 중 4개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [org.thealibrary/thea](https://thealibrary.org) | 5 | 76 | 73 | 100% | 100% | — |
| [io.github.geon0814/piwoom](https://seoulsmokingmap.vercel.app/en/ai-connect) | 4 | 226 | 424 | 100% | 100% | — |
| [io.github.namuaix/seoul-tourism](https://mcp.namu.ai.kr) | 3 | 110 | 20 | 100% | 100% | — |

## 날씨·환경 (Weather)

후보가 0건뿐이라 순위를 매기지 않았다. 0개 중 0개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [io.github.sean-park-funda/korea-data-mcp](https://github.com/sean-park-funda/korea-data-mcp) | 기타 | “도구 6종이 한국관광공사 관광정보, 시내버스 정류소, 기상 평년값뿐이라 공공데이터 목록 검색이나 인구 통계는 다루지 않는다…” |

## 교통·이동 (Transit)

후보가 3건뿐이라 순위를 매기지 않았다. 3개 중 3개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.pyungyo/mvno-plans](https://pyungyo.com/developers/) | 10 | 23 | 21 | 100% | 100% | — |
| [io.github.kimnchai/korea-flight-mcp](https://korea-flight.kimnchai.com) | 8 | 52 | 59 | 100% | 100% | — |
| [app.stamptour/stamptour](https://stamptour.app) | 4 | 36 | 36 | 100% | 100% | — |

## 의료·복지 (Health)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [kr.caregrade/catalog](https://caregrade.kr) | 6 | 33 | 44 | 100% | 100% | — |
| [org.medicalaialliance/intelligence](https://github.com/austinpw-cloud/maa-website) | 5 | 361 | 253 | 100% | 0% | — |

## 교육·문화 (Education)

후보가 11건뿐이라 순위를 매기지 않았다. 11개 중 11개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.k-agentpay/kaia-x402](https://github.com/k-agentpay/kaia-x402) | 9 | 119 | 116 | 100% | 0% | — |
| [com.torrent100/korea-travel-demand](https://torrent100.com/developers.html) | 9 | 22 | 22 | 100% | 100% | — |
| [app.wonbuddhism/scripture](https://scripture.wonbuddhism.app) | 7 | 57 | **298** | 100% | 100% | — |

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [io.github.yousunjung84-edu/academyinfo](https://github.com/yousunjung84-edu/academyinfo-mcp)<br><sub>지난 회차 표기 `yousunjung84-edu/academyinfo-mcp` → `io.github.yousunjung84-edu/academyinfo` — 같은 서버로 이었다</sub> | 교육·문화 | “이름과 달리 학원이 아니라 대학알리미 기반 고등교육 통계 서버로, 공공데이터·행정 분야와는 주제가 다르며…” |

## 커머스·생활 (Commerce)

> 질문1(요즘 많이 팔리는 상품)에 판매량·인기 근거로 답한 서버는 이 분야에 0곳이고, 실제로 잘한 것은 그 부재를 출력 근거로 밝힌 곳(jitdot·encha·korea-stay·nara-tour·led-sign-quote·marketpilot)이었다 — korea-stay는 무시된 sort 인자를 공시해 세 회차 모두 순위를 지어내지 않았고, 갈림은 서버가 '판매순 축이 없다'를 응답에 적느냐에서 났다.

<sub>위 총평의 서버 수는 **분야 교정 전** 기준이다 — 이 분야에서 5건이 아래 「분야 교정」으로 빠졌다.</sub>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.aminpiano/nara-tour](https://github.com/aminpiano/naratour-mvp) | 3 | 36 | 50 | 100% | 0% | 0 |
| [com.jitdot/catalog](https://jitdot.com/developers/) | 5 | 131 | 119 | 100% | 100% | 0 |
| [app.ncha/encha](https://github.com/vincenzo0219/encha) | 4 | 69 | 65 | 100% | 100% | 0 |

1. **aminpiano/nara-tour** — 수원·경기 남부 단체여행 여행사 한 곳의 회사 정보와 카카오 상담 링크만 주는 좁은 범위의 서버다. 상품·판매·예약 데이터는 없지만 없다는 것이 출력에서 분명해 답변이 정직했고, 이 여행사에 연락하는 용도로만 쓸 수 있다.
2. **jitdot/catalog** — 인테리어 자재를 규격·재질·마감으로 찾고 재고·설계 파일을 확인하는 좁은 용도에 맞는 서버이고, 판매 통계가 없다는 한계를 답변이 일관되게 정확히 전했다.
3. **ncha/encha** — 경기·서울의 오래된 음식점을 인허가 기록으로 찾는 좁은 용도의 서버이고, 범위 밖 질문에는 일관되게 정직하게 선을 긋는다. 판매·예약 같은 커머스 질문에는 쓸 수 없다.
4. **sallim/korea-stay** — 전국 인허가 숙박업 원장과 관광공사 숙박 정보를 합친 숙소 검색 서버로, 판매량·인기·요금·재고가 없다는 사실을 출력에서 공시해 답변자가 세 번 다 인기 순위를 지어내지 않았다. 숙소 존재·업종 확인 용도로는 믿을 만하지만 예약·가격 비교는 원본 링크로 넘겨야 한다.
5. **oneulsanji/catalog** — 정직하고 정확하지만 지금 판매 상품이 1종뿐이라 '무엇이 많이 팔리나' 같은 커머스 질문에 쓸 만한 폭이 없다. 판매량 필드도 없으므로 인기 질문에는 쓰지 않는 것이 맞고, 이 스토어의 상품·배송 정책 확인 용도로만 쓸 만하다.
6. **wooktech/led-sign-quote** — 대전·충청권 LED 전광판 업체의 견적·회사정보·FAQ 서버로, 범위 밖 질문을 정직하게 거절하고 견적 절차는 정확하다. 이 업체에 견적을 받으려는 용도로는 쓸 만하지만 일반 커머스 질문에는 범위가 좁고, FAQ 빈 결과에 붙는 엉뚱한 업종 안내 문구는 고쳐야 할 결함이다.
7. **timeplex/booking** — 서울 중심 비의료 뷰티(마사지·헤드스파·세신·메이크업 등) 18곳의 메뉴·가격·예약 링크를 주는 서버로, 판매량이 없다는 사실을 답변자가 정직하게 전할 수 있게 출력이 짜여 있다. 무엇을 예약할 수 있는지 알아보고 실제 예약 링크까지 가는 용도로는 쓸 만하고, 인기·판매 순위 용도로는 맞지 않는다.
8. **marketpilot/marketpilot** — SNS·플레이스 마케팅 상품을 결제 링크로 주문하는 서버로, 판매 인기 정보가 없다는 것을 세 회차 모두 정직하게 밝혔다. 상품을 골라 주문하는 용도로는 쓸 만하지만 상품 수 같은 총계는 응답에 없으므로 모델이 센 숫자를 믿지 말아야 한다.
9. **celadon-wholesale-mcp/celadon-wholesale** — 미국·캐나다 사업자용 한국 스킨케어 도매 카탈로그로, 약관·가격·브랜드 규모 질문에는 정확하다. 판매량·인기 데이터는 없으므로 '잘 팔리는 것' 질문에는 쓰지 말고, 한국 소비자용 커머스가 아니라는 범위도 감안해야 한다.
10. **bidon/bidon** — 한국 B2B 전자·산업 부품 품번·사양·판매처 검색 서버로, 견적 요청 절차와 매물·견적 건수를 정직하게 보여준다. 인기 상품 집계는 없으니 판매 동향 질문에는 쓰지 말고, 특정 품번 조달 용도로 쓰는 것이 맞다.
11. **www/dongdaemun** — 동대문 도매 신상품과 스톨 위치를 실시간으로 훑는 용도에는 적합하다. 다만 가격·판매량은 주지 않으므로 '잘 팔리는 것'을 묻는 데는 맞지 않고, 신상 목록을 판매 순위로 읽지 않도록 주의해야 한다.
12. **hotker/hotker** — 국내 통신 3사 휴대폰 구매 조건의 총비용·위약금·결합할인을 계산하는 서버로, 판매 순위나 예약 질문에는 답할 수 없다. 견적을 이미 가진 사용자가 비용을 계산하는 용도로는 의미가 있지만, 상품·판매조건 검색은 이번 회차에 0건이거나 백엔드 장애 상태였다.
13. **nmjib/nmjib** — 반셀프 인테리어 공정·비용·체크리스트 문서와 상담·자재 견적 접수에 쓸 만한 서버다. 판매 순위는 주지 않고 자재 목록은 가격·총계가 없으므로 인기 상품 질문에는 맞지 않으며, '예약'이라 할 만한 것은 상담·자재 문의 접수뿐이다.
14. **nodajimarket/catalog** — 한국 수공예·작가 작품을 해외로 파는 카탈로그라고 설명하지만, 이번 측정에서는 어떤 검색어로도 상품이 나오지 않아 실제로 쓸 수 있는 상태인지 확인되지 않았다. 빈 결과의 이유를 공시하지 않으므로 지금은 상품 탐색 용도로 권하기 어렵다.
15. **shift7667/cheapest-esim** — 한국 여행자용 eSIM 가격 비교로는 매일 수집 날짜와 출처를 밝히고 공식몰 교차확인까지 해 정확도가 높다. 다만 판매량 데이터는 없으므로 '많이 팔리는' 질문에 쓰면 답변 모델이 가격 순위나 누적 리뷰 수를 인기로 오독하기 쉽다는 점을 알고 써야 한다.
16. **atdev/supershopping** — 신품·중고를 한 번에 찾고 비교하는 용도에는 쓸 만하지만, 추천 도구의 reason 문구가 상품명 태그만으로 '판매량이 많다'고 단정하고 데이터가 2026-07 수집분이라 '요즘 잘 팔리는 것'을 묻는 데는 쓰면 안 된다.
17. **moaibuy/moa** — 도매 상품을 배송비 포함 총액·도착 예상으로 비교하는 데는 유용하지만, 판매량·인기 근거가 없어 '많이 팔리는 상품'을 물으면 상품명 키워드 일치가 순위로 둔갑한다. 인기 상품 질문에는 쓰지 말아야 한다.
18. **arcasos/arcasos-rentals** — 서울·부산 단기 임대 매물을 자연어로 찾고 예약 요청 초안을 만드는 서버다. 매물 검색 용도로는 쓸 수 있지만, 검색 질의에 담긴 '인기'·'많이 팔리는' 같은 조건을 처리하지 못한다는 사실을 공시하지 않아 답변 모델이 관련도 순 결과를 인기 순위로 전하는 일이 세 번 다 일어났다.

<sub>순위는 **실제로 물어본 결과**다 — 같은 질문을 각 서버에 던지고 답변을 채점했다. 서버당 **3회** 물어 재현성까지 채점했다. 질문·호출기록·답변은 [answers/](answers)에, 채점은 [grades/](grades)에, 기준은 [JUDGING.md](JUDGING.md)에 있다.</sub>

<details><summary>채점됨 — 4위 이하 15건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [app.sallim/korea-stay](https://stay.sallim.app) 🏠 | 4 | 47 | 41 | 100% | 100% | 0 |
| [com.oneulsanji/catalog](https://oneulsanji.com) | 5 | 31 | 34 | 100% | 100% | 0 |
| [kr.co.wooktech/led-sign-quote](https://wooktech.co.kr) | 4 | 103 | 263 | 100% | 100% | 1 |
| [ai.timeplex/booking](https://timeplex.ai)<br><sub>뷰티·웰니스 예약. 등록 매장 18곳(2026-11-03 회차 확인)</sub> | 5 | 457 | 757 | 100% | 100% | 4 |
| [it.marketpilot/marketpilot](https://www.marketpilot.it) | 25 | 28 | 29 | 100% | 100% | 2 |
| [dev.workers.dermatologicalbeautyllc.celadon-wholesale-mcp/celadon-wholesale](https://celadonbeauty.com/pages/celadon-wholesale-connector-for-ai-assistants) | 5 | 39 | 41 | 100% | 100% | 2 |
| [kr.bidon/bidon](https://bidon.kr/ai-agent) | 4 | 112 | 113 | 100% | 100% | 1 |
| [com.apmzoom.www/dongdaemun](https://github.com/apmleokeo-gif/apmzoom-mcp) | 5 | 42 | 44 | 100% | 100% | 2 |
| [ai.hotker/hotker](https://github.com/c2bcom10-ship-it/hotker) | 6 | 40 | 74 | 100% | 100% | 0 |
| [com.nmjib/nmjib](https://github.com/Deall-International/nmjib-mcp) | 12 | 237 | 360 | 100% | 100% | 3 |
| [com.nodajimarket/catalog](https://github.com/NodajiFi-Tokenomy/NodajiFi-Ecosystem) | 5 | 394 | 481 | 100% | 100% | 1 |
| [io.github.shift7667/cheapest-esim](https://github.com/shift7667/cheapest-esim-mcp) | 5 | 23 | 22 | 100% | 100% | 4 |
| [ai.atdev/supershopping](https://github.com/alex-hoyeol-choi/headless-commerce) | 8 | 55 | 49 | 100% | 100% | 3 |
| [com.moaibuy/moa](https://moaibuy.com) | 10 | 62 | 114 | 100% | 100% | 3 |
| [com.arcasos/arcasos-rentals](https://arcasos.com)<br><sub>주 단위 단기임차. 총계 미공시로 항상 10건에서 조용히 잘린다</sub> | 5 | 602 | 620 | 100% | 100% | 5 |

</details>

<details><summary>채점하지 않은 1건</summary>

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [me.wehome/stays](https://www.wehome.me) | 2 | 17 | 18 | 100% | 100% | — |

</details>

**분야 교정 5건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.kbeautyverified/ingredients](https://kbeautyverified.com/developers) | 공공데이터·행정 | “판매·구매·순위 기능 없이 식약처(MFDS)·EU CosIng·미국 FDA의 공식 규제 기록과 리콜 기록에 화장품 성분표를 대조하는 규제 조회 서버다.” |
| [com.kimchi-sushi/agent-mcp](https://kimchi-sushi.com) | 교육·문화 | “도구가 한일 유학·워킹홀리데이 안내와 커뮤니티 게시글 검색·조회뿐이고 상품 판매나 예약 도구가 없다.” |
| [com.selectbnbs/verify](https://selectbnbs.com/verify/agents/) | 공공데이터·행정 | “도구가 숙박 리스팅을 정부 숙박업 인허가 원장과 대조하는 검증·조회 두 개뿐이고 상품 판매나 예약 도구가 없다.” |
| [io.github.SongT-50/korean-news-mcp](https://github.com/SongT-50/korean-news-mcp) | 미디어·뉴스 | “도구가 카테고리별 뉴스·키워드 검색·트렌딩 헤드라인·기사 본문 읽기·일일 브리핑뿐이고 상품 판매나 예약 기능은 없다.” |
| [io.github.Youjg25/maison-de-talents](https://maisondetalents.com) | 기타 | “도구가 백화점·면세점·명품 매장 판매직 채용공고 검색·상세·연봉 벤치마크뿐이라 상품 판매나 예약을 다루지 않는다.” |

## 미디어·뉴스 (Media)

후보가 7건뿐이라 순위를 매기지 않았다. 7개 중 7개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.lifenplanner/babynews](https://github.com/lifenplanner/babynews-gemini-extension) | 13 | 31 | 35 | 100% | 100% | — |
| [kr.co.internettrend/internettrend-try](https://internettrend.co.kr/mcp) | 12 | 55 | 60 | 92% | 100% | — |
| [ai.smilestory/koreantoday](https://thekoreantoday.com) | 5 | 131 | 140 | 100% | 100% | — |

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 미디어·뉴스 | “상품·예약과는 무관한 미디어 서버다.” |

## 디렉토리·개발자도구 (Directory)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [io.github.Wonderfulian/kbv-server](https://github.com/Wonderfulian/kbv-server) | 6 | 167 | 148 | 100% | 100% | — |
| [io.github.a01038137493-coder/easybuilder-directory](https://builder.easyagency.co.kr/llms.txt) | 2 | 82 | **1056** | 100% | 100% | — |

**분야 교정 1건** — 이 분야 검색어에 걸려 수집됐지만 **불러 보니 다른 것을 하는** 서버다. 남의 분야 질문으로 매긴 등수는 그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.

| 서버 | 실제 분야 | 채점자가 확인한 것 |
|---|---|---|
| [com.saaskr/korean-saas-directory](https://saaskr.com/mcp) | 디렉토리·개발자도구 | “상품 판매나 예약을 하는 곳이 아니다.” |

## 기타 (Other)

후보가 2건뿐이라 순위를 매기지 않았다. 2개 중 2개를 고르는 것은 순위가 아니라 목록이다.

| 서버 | 도구 | 웜ms | 콜드ms | 설명 | 주석 | 사실오류 |
|---|---|---|---|---|---|---|
| [com.kwhmate/calculators](https://kwhmate.com/developers/) | 19 | 65 | 144 | 100% | 100% | — |
| [com.seoapi/naverbot](https://seoapi.com/naverbot/) | 1 | 39 | 46 | 100% | 0% | — |

## 표기

* **도구** — `tools/list`에 실제로 들어 있는 개수. 0이면 껍데기다
* **웜 / 콜드** — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다
* **설명 / 주석** — 도구에 설명이 붙은 비율 / `readOnlyHint` 같은 주석이 붙은 비율. **둘 다 없으면 모델이 그 도구를 언제 어떻게 쓸지 모른다** — 데이터가 정확해도 답에 도달하지 못한다
* 이름 옆 <sub>무료 N/M</sub> — 서버가 유료 게이트를 **스스로 공시**할 때만 붙는다. 없다고 무료라는 뜻이 아니다 — 밖에서는 판정할 수 없다
* 이름 밑 작은 글씨 — 불러 보고 알게 된 **그 서버의 성질**. 카탈로그형은 값이 아니라 데이터셋 위치를 주고, 집계 통계표는 개별 거래를 주지 않는다. 몰라서 헛짚는 자리라 표에 낸다
* **사실오류** — 그 서버로 답한 내용 중 채점자가 **실제와 다르다고 확인한** 건수. 서버가 틀린 값을 준 경우와 모델이 옮겨 적다 틀린 경우가 섞여 있고, 어느 쪽인지는 [grades/](grades)에 문장째 적혀 있다. `—`는 채점하지 않았다는 뜻이다
* 🏠 — 이 목록의 운영자가 만든 서버. **이 목록의 축을 고른 것도 같은 운영자다** — 축과 그 개정 이력은 [PROTOCOL.md](PROTOCOL.md)에 있다

## 측정 못 함

응답은 했지만 **비교할 값을 얻지 못한 29건.** 지우지 않고 여기 둔다 — “없다”가 아니라 **“우리가 못 봤다”**이기 때문이다. 대부분 도구 목록을 보는 데도 키를 요구한다. 키가 있으면 잘 도는 서버일 수 있다.

| 서버 | 증상 |
|---|---|
| [00data-kr/narajangteo-mcp](https://github.com/00data-kr/narajangteo-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [KIMDONGWOOK12/job-radar](https://github.com/KIMDONGWOOK12/job-radar) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [LimEulYoung/lawful-mcp](https://github.com/LimEulYoung/lawful-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [ai.0si/disclosures](https://0si.ai/developers.html#mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [ai.heyyumi/heyyumi](https://github.com/hmp-dev/heyyumi-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [ai.seldons/korea-business-trade](https://seldons.ai/mcp) | initialize는 됐는데 tools/list를 못 읽었다(HTTP 400) |
| [biz.nunchi/nunchi](https://nunchi.biz/mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.baroezip/mcp](https://baroezip.com/ai) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.beauticslab/mcp](https://github.com/websfactory/beauticslab-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.empresskorea/kbeauty-agent-commons](https://empresskorea.com/kb-agent-network/) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.find-ref/find-ref](https://find-ref.com/connect/) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.founderssaid/founderssaid](https://founderssaid.com) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.goodsaegim/goodsaegim](https://www.goodsaegim.com) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [com.koreastockcheck/mcp](https://github.com/koreastockcheck/mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [epoko77-ai/korean-bill-debate-mcp](https://github.com/epoko77-ai/korean-bill-debate-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.ThatMojo/encarapi-mcp](https://github.com/ThatMojo/encarapi-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.laplacetec/ecommerce-analytics](https://www.analytics-docs.laplacetec.com/guide/mcp/start) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [io.github.namen-ceo/factbat-public-record-locator](https://factbat.com/finder?src=mcp-pulsemcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [jeonghwanko/coffee-price-mcp](https://github.com/jeonghwanko/coffee-price-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [kr.co.internettrend/internettrend](https://internettrend.co.kr/mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [kr.co.prebid/prebid](https://prebid.co.kr/ai) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [kr.qnector/qnector](https://github.com/SJ-PARK-Yesnet/Qnector) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [kr.wandsol/patent-search](https://mcp.wandsol.kr) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [one.aisa/seo-serp-other-engines](https://aisa.one) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [risingdream/legal-kb-plugin](https://github.com/risingdream/legal-kb-plugin) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [risingdream/taxlens-plugin](https://github.com/risingdream/taxlens-plugin) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [scvcoder/korean-privacy-law-mcp](https://github.com/scvcoder/korean-privacy-law-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [seolcoding/korean-stat-mcp](https://github.com/seolcoding/korean-stat-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |
| [taip-tech/tax2ai-mcp](https://github.com/taip-tech/tax2ai-mcp) | 인증 필요 — 키 없이는 도구 목록도 못 본다 |

## 우리 목록에 넣으려면

**우리에게 올릴 필요가 없다.** [공식 MCP 레지스트리](https://registry.modelcontextprotocol.io)에 등록하면 다음 회차에 자동으로 들어온다. 그쪽이 나은 이유는 우리만 읽는 게 아니라서다.

이미 등록했는데 여기 없다면 **우리 수집기의 버그일 수 있다** — 이슈로 알려 달라. 경쟁 서비스여도 받는다.

제출은 등재가 아니다. 실제로 `tools/list`에 응답해야 표에 오른다 — 우리가 통과시키고 말고 할 것이 없다.

## 고쳤다면 다시 잰다

이 표의 값은 **2026-11-08 그 순간의 기록**이다. 고쳤다면 [이슈](https://github.com/sallim-app/korea-mcp-index/issues)로 알려 달라 — 다음 회차에 다시 잰다. 경쟁 서비스여도 받는다.

**우리가 먼저 다시 두드리지는 않는다.** 바뀐 게 없는 서버를 주기적으로 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다. 그래서 두드리는 대신 신호를 받는다.

이런 것도 같은 창구다 — **우리 쪽 잘못일 수 있다.**

* 분야가 틀렸다 (검색어가 분야를 정하므로 실제로 하는 일과 어긋날 수 있다)
* 주소를 잘못 짚었다 (README에서 추정한 주소라 서버가 아니라 우리가 틀린 것)
* 채점이 틀렸다 — 답변·근거·채점이 [answers/](answers)·[grades/](grades)에 그대로 있으니 어느 문장이 왜 틀렸는지 짚어 달라

**순위는 전원 동시에만 다시 잰다 — 운영자인 우리도 예외가 아니다.** 우리는 고칠 때마다 다시 잴 수 있고 남은 그럴 수 없다. 개별 재측정을 순위에 반영하면 우리 서버만 계단식으로 올라가고 남은 자기 최악의 순간에 박제된다. 실제로 우리는 이 표의 지적을 받아 우리 서버를 고치고 다시 쟀지만 **그 결과를 순위에 넣지 않았다** — 기록은 [answers/](answers)에 ‘정규 회차 아님’으로 남겨 두었다.

## 어떻게 재나

```
collect  공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API + 제보(tips.json)
         + 게시 이력 이어받기 — 한 번 실은 서버가 안 잡히면 되살려 다시 판정한다
filter   한국 관련성(한글·.go.kr·기관명) → 후보 좁히기
enrich   README에서 엔드포인트·패키지·기관 도메인 추출
classify 분야·데이터제공형 판정 (LLM, 결과는 classification.json에 고정)
measure  tools/list 실호출 — 가동·도구수·지연·설명·주석          [매주]
answer   분야별 실제 질문을 서버에 던져 답하게 한다 (Haiku)       [매월]
grade    그 답을 원문과 대조해 채점한다 (Opus) → 순위             [매월]
render   이 문서
```

**가동은 매주, 순위는 매월 첫 화요일**(14:00 KST)에 다시 잰다. 서버가 안 바뀌면 채점 결과도 안 바뀌는데 매주 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다.

두드릴 때는 `tools/list` 3회(콜드 1 + 웜 2), 사이에 간격을 두고, User-Agent로 우리를 밝힌다.

**가동 지표는 돌리면 같은 값이 나온다** — 원자료가 [measured.json](measured.json)·[candidates.json](candidates.json)에 있다. **순위는 그렇지 않다** — 채점이 모델 판단이라 같은 입력에도 흔들린다. 얼마나 흔들리는지를 우리가 직접 재서 [variance/](variance)에 공개해 두었다. 우리가 1위인 자리일수록 이 두 문장을 함께 읽어 달라.

**다른 가중치로 다시 계산해 보라고 표를 펴 두었다** — [axes.csv](axes.csv)는 게시된 모든 축을 서버 1행 × 축 1열로 편 것이고, `python3 recompute.py --verify`는 **이 문서의 머릿수가 원자료에서 그대로 나오는지** 검사한다. 원자료를 올려 두는 것과 그 원자료로 게시본이 재현되는 것은 다른 주장이라 후자를 기계로 건다.

## 믿으면 안 되는 부분

* **정확성은 분야마다 질문 두 개로만 봤다.** 그 두 문항이 그 분야를 대표한다는 보장은 없다. 질문은 공개돼 있으니(`questions.py`) 더 나은 질문을 알려 달라
* **채점자도 모델이다.** 근거를 전부 공개하는 것으로 줄일 수는 있어도 없앨 수는 없다. 답변은 약한 모델(Haiku)이 만들고 채점은 강한 모델(Opus)이 하는데, 그 이유와 실측 근거는 [JUDGING.md](JUDGING.md)에 있다
* **세 번 물었어도 '갈릴 수 있다'까지만 말한다.** 서버마다 세 회차가 무엇이 갈렸고 서버 탓인지 모델 탓인지는 [grades/](grades)의 `재현성`에 적었지만, 몇 %로 갈리는지는 이 표본(질문 두 개 × 3회)으로 못 댄다
* **한 분야를 여러 채점자가 나눠 채점했다.** 순위는 원 기록으로 정했지만, 표의 점수 칸은 묶음이 다르면 그대로 견줄 수 없다 — 어느 서버가 어느 묶음이었는지와 엄격함이 갈린 자리는 [grades/](grades)의 `순위_근거`에 있다
* **측정 항목을 우리가 골랐다.** 원자료 공개로 줄일 수는 있어도 없앨 수는 없다 — 무엇을 고정했고 무엇을 언제 왜 바꿨는지는 [PROTOCOL.md](PROTOCOL.md)에 있다. **결과를 본 뒤에 바꾼 적이 한 번 있고**, 그 건도 거기 적어 두었다
* **측정 지점은 한국 두 곳이다.** 국외에서 재면 값이 다를 수 있고 아직 확인하지 않았다
* **콜드는 한 번뿐이다.** 그 순간 그 서버가 자고 있었을 수 있다
* **못 잰 것이 더 많다.** 후보 중 93건은 주소도 패키지도 찾지 못했다. “작동하지 않는다”가 아니라 **확인하지 못했다**는 뜻이다 — 그 밖에 102건은 배포 패키지는 확인했으나 원격 주소가 없어 응답을 못 쟀다

---

## 라이선스

코드·문서·우리가 만든 측정값은 [MIT](LICENSE). **응답 발췌는 각 서버 운영자의 것**이고 우리는 측정 근거로 인용했을 뿐이다 — 400~500자로 제한하고 개인정보 패턴을 가린다. 내려 달라고 하면 내린다.

---

생성 `render_readme.py` · 웹판 <https://mcp-index.sallim.app> · 마지막 측정 2026-11-08 · 운영 [sallim-app](https://github.com/sallim-app)
