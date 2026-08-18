# 한국 데이터 MCP — 실측 목록

한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 "있다"를 말한다. 이 목록은 **"지금 되냐"**를 잰다.
2026-08-18 UTC 측정 기준, 원격 주소를 확인한 한국 MCP **56건 중 24건(43%)이
응답하지 않았다.** 등록은 가동의 증거가 아니다.

**주소의 출처를 갈라 읽어라.** 관리자가 공식 레지스트리에 **직접 등록한** 주소 27건 중
11건이 무응답이고, 나머지 29건은 우리가 README에서 뽑은 **추정** 주소다(무응답 13건).
추정 주소의 무응답은 "그 서버가 죽었다"보다 약한 주장이다 — 우리가 주소를 잘못 짚었을 수 있다.

## 이 목록을 믿어도 되는 이유 (그리고 믿으면 안 되는 부분)

- **측정 스크립트와 원자료가 이 저장소에 있다.** `measure.py`를 돌리면 아래 표를 다시 만들 수 있다.
  우리가 1위여도 당신이 직접 재서 반박할 수 있다.
- **우리도 이 목록에 있다.** `sallim-app`이 이 목록의 운영자이며, 우리 서버 `korea-realty`가
  표에 들어 있다. 빼지 않는 대신 **밝히고**, 우리가 지는 항목(셀프호스팅 가능 여부)을 같이 싣는다.
- **측정 항목은 결과를 보기 전에 고정했다.** 사후에 우리에게 유리하게 바꾸지 않는다.
- **남는 편향**: 어떤 항목을 재기로 골랐는지 자체는 우리가 정했다. 원자료를 공개하는 것으로
  줄일 수는 있어도 없앨 수는 없다. 없는 척하지 않는다.
- **측정 지점**: 한국(Oracle Cloud) 두 지점에서 쟀다. 국외에서 재면 값이 다를 수 있고
  그건 아직 확인하지 않았다.

## 무엇을 재는가

| 항목 | 뜻 |
|---|---|
| 도구 수 | `tools/list` 응답에 실제로 들어 있는 도구 개수. 0개면 껍데기다 |
| 웜 | 연달아 부를 때의 왕복(ms). 이미 쓰고 있는 사용자의 체감 |
| 콜드 | 첫 호출(ms). 서버리스는 기동 시간이 붙는다. **처음 붙는 사용자의 체감이라 버리지 않는다** |
| 키 | 키·가입 없이 도구 목록을 볼 수 있는가 |
| 셀프호스팅 | 패키지가 배포돼 직접 띄울 수 있는가. **원격 전용인 우리 서버는 여기서 진다** |


## 응답하는 서버

| 서버 | 도구 | 웜(ms) | 콜드(ms) | 키 | 셀프호스팅 |
|---|---|---|---|---|---|
| [scvcoder/korean-law-alio-mcp](https://github.com/scvcoder/korean-law-alio-mcp) | 125 | 221 | 345 | 불필요 | 가능 |
| app.apick/all | 82 | 63 | 138 | 불필요 | 불가 |
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) **(이 목록 운영자)** | 47 | 47 | 81 | 불필요 | 불가 |
| app.apick/business | 16 | 35 | 35 | 불필요 | 불가 |
| [Choihello/startup-law-mcp](https://github.com/Choihello/startup-law-mcp) | 13 | 134 | **4021** | 불필요 | 가능 |
| com.theprotoclinical/commerce | 13 | 146 | 372 | 불필요 | 불가 |
| [MosslandOpenDevs/alpha](https://github.com/MosslandOpenDevs/alpha) | 12 | 29 | **387** | 불필요 | 가능 |
| [com.aikstockdata/mcp](https://github.com/na77tech-creator/aikstockdata) | 12 | 28 | 81 | 불필요 | 불가 |
| [app.sallim/contract-compass](https://github.com/kwenhwang/contract-compass) **(이 목록 운영자)** | 11 | 33 | 67 | 불필요 | 불가 |
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 10 | 203 | 282 | 불필요 | 가능 |
| [com.hankookilbo.mcp/hankookilbo-mcp](https://github.com/hkilbo/hankookilbo-mcp) | 10 | 217 | 635 | 불필요 | 불가 |
| [kang-aco/korean-law](https://github.com/kang-aco/korean-law) | 10 | 218 | 213 | 불필요 | 불가 |
| [haklaekim/public-data-lens](https://github.com/haklaekim/public-data-lens) | 9 | 22 | 38 | 불필요 | 가능 |
| [hike-lab/public-data-lens](https://github.com/hike-lab/public-data-lens) | 9 | 23 | 33 | 불필요 | 불가 |
| [yousunjung84-edu/academyinfo-mcp](https://github.com/yousunjung84-edu/academyinfo-mcp) | 8 | 55 | **172** | 불필요 | 가능 |
| io.aidc-ai/design-engine | 7 | 285 | 590 | 불필요 | 불가 |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp) | 7 | 232 | 542 | 불필요 | 가능 |
| [Mrbaeksang/korea-stock-analyzer-mcp](https://github.com/Mrbaeksang/korea-stock-analyzer-mcp) | 6 | 215 | 512 | 불필요 | 가능 |
| ai.timeplex/booking | 6 | 493 | **1628** | 불필요 | 불가 |
| com.airblockfz/seoul-apt-signal | 6 | 28 | **105** | 불필요 | 불가 |
| com.saaskr/korean-saas-directory | 5 | 254 | 305 | 불필요 | 불가 |
| app.apick/finance | 3 | 30 | 38 | 불필요 | 불가 |
| com.arcasos/arcasos-rentals | 3 | 720 | 1034 | 불필요 | 불가 |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp) | 3 | 121 | **5038** | 불필요 | 가능 |
| [io.github.accentist/buyking-mcp](https://github.com/accentist/buyking-mcp) | — | 28 | **109** | 불필요 | 가능 |
| [MarcoYou/open-proxy-mcp](https://github.com/MarcoYou/open-proxy-mcp) | — | — | 1726 | 필요 | 가능 |
| [com.beauticslab/mcp](https://github.com/websfactory/beauticslab-mcp) | — | — | 299 | 필요 | 불가 |
| com.boltena/erp | — | — | 143 | 필요 | 불가 |
| com.empresskorea/kbeauty-agent-commons | — | — | 429 | 필요 | 불가 |
| [jeonghwanko/coffee-price-mcp](https://github.com/jeonghwanko/coffee-price-mcp) | — | — | 351 | 필요 | 가능 |
| [jeongmk522-netizen/smishing-stop-mcp](https://github.com/jeongmk522-netizen/smishing-stop-mcp) | — | — | 79 | 필요 | 가능 |
| [seolcoding/korean-stat-mcp](https://github.com/seolcoding/korean-stat-mcp) | — | — | 1246 | 필요 | 가능 |

## 응답하지 않는 서버

측정 시점에 그 주소가 응답하지 않았다. 일시적 장애일 수 있으니 **폐기 판정이 아니라 관측 기록**으로 읽어라.

주소 출처를 같이 싣는다. `레지스트리`는 관리자가 직접 등록한 주소라 무응답이 그 서버에 대한 관측이지만, `README 추정`은 우리가 문서에서 뽑은 주소여서 **우리가 잘못 짚었을 가능성이 남아 있다**. 둘을 같은 무게로 읽지 마라.

| 서버 | 증상 | 주소 출처 |
|---|---|---|
| Dayoooun/korea-stats-mcp | HTTP 404 | README 추정 |
| ai.atdev/supershopping | HTTP 400 | 레지스트리 |
| ai.smithery/alphago2580-naramarketmcp | HTTP 404 | 레지스트리 |
| ai.smithery/hjsh200219-pharminfo-mcp | HTTP 404 | 레지스트리 |
| ai.smithery/isnow890-data4library-mcp | HTTP 404 | 레지스트리 |
| ai.smithery/jjlabsio-korea-stock-mcp | HTTP 404 | 레지스트리 |
| app.wishpool/korea-invoice-mcp | URLError: <urlopen error [Errno -2] Name or service not known> | 레지스트리 |
| bootpay/bootpay-mcp | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certific | README 추정 |
| chrisryugj/archhub-mcp | URLError: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1000)> | README 추정 |
| dartpointai/dartpoint-mcp | HTTP 307 | README 추정 |
| eddmpython/dartlab | HTTP 405 | README 추정 |
| hjsh200219/korea-public-data-mcp | HTTP 400 | README 추정 |
| io.github.SongT-50/korean-agriculture-mcp | HTTP 503 | 레지스트리 |
| io.github.SongT-50/korean-public-data-mcp | HTTP 503 | 레지스트리 |
| io.github.SongT-50/korean-stock-mcp | HTTP 503 | 레지스트리 |
| io.github.a-mashiro-art/jp-data | HTTP 404 | 레지스트리 |
| io.github.bakyang2/kr-crypto-intelligence | HTTP 400 | 레지스트리 |
| kmgvv23/stock-data-mcp | HTTP 400 | README 추정 |
| kokogo100/ragalgo-mcp-server | HTTP 404 | README 추정 |
| lucidwatper/Kosis-mcp | TimeoutError: The read operation timed out | README 추정 |
| nokelan/health-fee-mcp | HTTP 405 | README 추정 |
| sjh9714/electronics-price-mcp | HTTP 404 | README 추정 |
| smilemin07/korean-rnd-regs-mcp | HTTP 400 | README 추정 |
| whdrnr2583-cmd/koreanpulse | HTTP 400 | README 추정 |

## 못 잰 것 — 177건

후보 233건 중 **177건은 원격 주소도 배포 패키지도 없어 가동 여부를 재지 못했다.** 이것은 '작동하지 않는다'가 아니라 '우리가 확인하지 못했다'는 뜻이다. 저장소만 있고 레지스트리에 등록하지 않은 경우가 대부분이다 — 등록하면 다음 회차에 자동으로 잡힌다.

여기엔 **주소 미상**도 들어 있다. README에서 뽑은 주소가 그 서버의 것이 아니라 디렉터리·문서 사이트(Glama·LobeHub 등)이거나 문서의 placeholder였던 건들이다. 그런 주소로 얻은 응답은 살았다는 증거도 죽었다는 증거도 아니라서 판정에서 뺐다.

- 2geonhyup/dart-mcp: README에서 뽑은 주소가 제3자 디렉터리·문서 사이트 주소(https://glama.ai/mcp)라 **측정 대상에서 뺐다** — 이 서버가 안 된다는 뜻이 아니라 우리가 이 서버의 주소를 모른다는 뜻이다
- CNI-KaeSoon/public-rules-mcp: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- JTech-CO/kr-apartment-market-skill: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- JungHoonGhae/gongctl: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- JungHoonGhae/k-vote-cli: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)

## 우리 목록에 넣어 달라면

공식 MCP 레지스트리에 등록하면 다음 회차 수집에 자동으로 들어온다. PR로 직접 제안해도 된다 — **우리 경쟁 서비스여도 받는다.** 좋은 MCP는 남의 것이어도 알리는 것이 이 목록의 목적이다.

---

생성: `render_readme.py` · 측정: `measure.py` · 원자료: `measured.json` · 마지막 측정 2026-08-18 17:44 UTC
