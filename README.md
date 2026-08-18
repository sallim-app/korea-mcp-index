# 한국 데이터 MCP — 실측 목록

한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 "있다"를 말한다. 이 목록은 **"지금 되냐"**를 잰다.
2026-08-18 측정 기준, 공식 MCP 레지스트리에 원격 주소를 등록한 한국 MCP **16건 중
8건(50%)이 응답하지 않았다.** 등록은 가동의 증거가 아니다.

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
| [app.sallim/korea-realty](https://github.com/sallim-app/korea-realty) **(이 목록 운영자)** | 47 | 49 | 94 | 불필요 | 불가 |
| [io.github.pipeworx-io/dart-kr](https://github.com/pipeworx-io/mcp-dart-kr) | 36 | 36 | **292** | 불필요 | 불가 |
| kr.eocpa/mydart | 16 | 196 | 206 | 불필요 | 불가 |
| com.airblockfz/seoul-apt-signal | 6 | 35 | 39 | 불필요 | 불가 |
| [io.github.lazymac2x/govdata-korea](https://github.com/lazymac2x/govdata-korea-api) | 6 | 122 | 115 | 불필요 | 불가 |
| com.saaskr/korean-saas-directory | 5 | 260 | 274 | 불필요 | 불가 |
| io.github.namuaix/seoul-tourism | 3 | 19 | 38 | 불필요 | 불가 |
| com.empresskorea/kbeauty-agent-commons | — | — | 427 | 필요 | 불가 |

## 응답하지 않는 서버

공식 레지스트리에 원격 주소가 등록돼 있으나 측정 시점에 응답하지 않았다. 일시적 장애일 수 있으니 **폐기 판정이 아니라 관측 기록**으로 읽어라.

| 서버 | 증상 |
|---|---|
| ai.smithery/jjlabsio-korea-stock-mcp | HTTP 404 |
| app.wishpool/korea-invoice-mcp | URLError: <urlopen error [Errno -2] Name or service not known> |
| io.github.SongT-50/korean-agriculture-mcp | HTTP 503 |
| io.github.SongT-50/korean-public-data-mcp | HTTP 503 |
| io.github.SongT-50/korean-stock-mcp | HTTP 503 |
| io.github.bakyang2/kr-crypto-intelligence | HTTP 400 |
| io.github.koreal6803/finlab-ai | HTTP 404 |
| io.github.whdrnr2583-cmd/koreanpulse | HTTP 400 |

## 못 잰 것 — 117건

후보 133건 중 **117건은 원격 주소도 배포 패키지도 없어 가동 여부를 재지 못했다.** 이것은 '작동하지 않는다'가 아니라 '우리가 확인하지 못했다'는 뜻이다. 저장소만 있고 레지스트리에 등록하지 않은 경우가 대부분이다 — 등록하면 다음 회차에 자동으로 잡힌다.

- AgentBridge-Lab/korea-space-support-mcp: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- Beau314/korea-tax-skills: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- ChangooLee/mcp-kr-legislation: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- Dayoooun/korea-stats-mcp: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)
- Engccer/gildongmu: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)

## 우리 목록에 넣어 달라면

공식 MCP 레지스트리에 등록하면 다음 회차 수집에 자동으로 들어온다. PR로 직접 제안해도 된다 — **우리 경쟁 서비스여도 받는다.** 좋은 MCP는 남의 것이어도 알리는 것이 이 목록의 목적이다.

---

생성: `render_readme.py` · 측정: `measure.py` · 원자료: `measured.json` · 마지막 측정 2026-08-18 12:44 UTC
