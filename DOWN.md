# 확인하지 못한 서버

2026-09-14 측정에서 **우리가 살아있음을 확인하지 못한** 목록. **사망 명단이 아니다** — 확인 못 함(unverified)과 죽음 확인(down)은 다른 값이고, 이 문서는 그 둘을 갈라 싣는다.

`죽음 확인`은 호스트가 없다는 직접 증거(DNS에 이름 없음·연결 거부)가 있을 때만 붙인다. 그 밖의 전부 — 4xx·5xx·타임아웃·TLS 오류 — 는 `확인 못 함`이다. 우리 두드리개가 못 본 것을 남의 사망으로 적지 않기 위해서다.

고쳤거나 우리가 주소를 잘못 짚었다면 이슈로 알려 달라. 다음 회차에 다시 잰다.

## 죽음 확인 — 호스트가 없다 — 5건

이 줄만 **우리가 사망을 주장하는 것**이다. 근거는 DNS 미해결·연결 거부처럼 우리 클라이언트 규격과 무관한 신호뿐이다.

| 서버 | 판정 | 증상 | 주소 |
|---|---|---|---|
| [app.wishpool/korea-invoice-mcp](https://github.com/junter1989k-ai/korea-invoice-mcp) | 죽음 확인 | URLError: <urlopen error [Errno -2] Name or service not known> | `https://inv-kr.wishpool.app/mcp` |
| [hlucent/airkorea-realtime-mcp](https://github.com/hlucent/airkorea-realtime-mcp) | 죽음 확인 | URLError: <urlopen error [Errno -2] Name or service not known> | `https://airkorea-realtime-mcp.fly.dev/mcp` |
| [hlucent/realestate-stats-mcp](https://github.com/hlucent/realestate-stats-mcp) | 죽음 확인 | URLError: <urlopen error [Errno -2] Name or service not known> | `https://realestate-stats-mcp.fly.dev/mcp` |
| [hlucent/safemap-uv-index-mcp](https://github.com/hlucent/safemap-uv-index-mcp) | 죽음 확인 | URLError: <urlopen error [Errno -2] Name or service not known> | `https://safemap-uv-index-mcp.fly.dev/mcp` |
| [io.github.CSOAI-ORG/korea-ai-basic-act-mcp](https://github.com/CSOAI-ORG/korea-ai-basic-act-mcp) | 죽음 확인 | URLError: <urlopen error [Errno -2] Name or service not known> | `https://api.meok.ai/v1/governance/korea-ai-basic-act` |

## 확인 못 함 — 등록된 주소 — 13건

관리자가 공식 레지스트리에 **직접 등록한** 주소다. 주장이 강하지만 **그래도 사망 판정이 아니다** — 우리가 확인하지 못했다는 뜻이다.

| 서버 | 판정 | 증상 | 주소 |
|---|---|---|---|
| [ai.smithery/alphago2580-naramarketmcp](https://github.com/alphago2580/naramarketmcp) | 확인 못 함 | HTTP 404 | `https://server.smithery.ai/@alphago2580/naramarketmcp/mcp` |
| [ai.smithery/hjsh200219-pharminfo-mcp](https://github.com/hjsh200219/pharminfo-mcp) | 확인 못 함 | HTTP 404 | `https://server.smithery.ai/@hjsh200219/pharminfo-mcp/mcp` |
| [ai.smithery/isnow890-data4library-mcp](https://github.com/isnow890/data4library-mcp) | 확인 못 함 | HTTP 404 | `https://server.smithery.ai/@isnow890/data4library-mcp/mcp` |
| [ai.smithery/jjlabsio-korea-stock-mcp](https://github.com/jjlabsio/korea-stock-mcp) | 확인 못 함 | HTTP 404 | `https://server.smithery.ai/@jjlabsio/korea-stock-mcp/mcp` |
| [com.whooing/whooing](https://whooing.com) | 확인 못 함 | HTTP 404 | `https://whooing.com/mcp` |
| [io.github.HyosikPark/kr-apt-trades](https://hawker-gateway.fly.dev) | 확인 못 함 | URLError: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in… | `https://hawker-gateway.fly.dev/mcp/kr-apt-trades` |
| [io.github.HyosikPark/kr-district-codes](https://hawker-gateway.fly.dev) | 확인 못 함 | URLError: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in… | `https://hawker-gateway.fly.dev/mcp/kr-district-codes` |
| [io.github.HyosikPark/kr-holidays](https://hawker-gateway.fly.dev) | 확인 못 함 | URLError: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in… | `https://hawker-gateway.fly.dev/mcp/kr-holidays` |
| [io.github.SongT-50/korean-agriculture-mcp](https://github.com/SongT-50/korean-agriculture-mcp) | 확인 못 함 | HTTP 503 | `https://korean-agriculture-mcp.onrender.com/mcp` |
| [io.github.SongT-50/korean-news-mcp](https://github.com/SongT-50/korean-news-mcp) | 확인 못 함 | HTTP 503 | `https://korean-news-mcp.onrender.com/mcp` |
| [io.github.SongT-50/korean-public-data-mcp](https://github.com/SongT-50/korean-public-data-mcp) | 확인 못 함 | HTTP 503 | `https://korean-public-data-mcp.onrender.com/mcp` |
| [io.github.SongT-50/korean-stock-mcp](https://github.com/SongT-50/korean-stock-mcp) | 확인 못 함 | HTTP 503 | `https://korean-stock-mcp.onrender.com/mcp` |
| [io.github.a-mashiro-art/jp-data](https://jp-data-api-production.up.railway.app) | 확인 못 함 | HTTP 404 | `https://jp-data-api-production.up.railway.app/mcp` |

## 확인 못 함 — 추정 주소 — 10건

우리가 README에서 뽑은 **추정** 주소다. **우리가 주소를 잘못 짚었을 수 있다** — 그 서버가 죽었다는 뜻으로 읽지 마라.

| 서버 | 판정 | 증상 | 주소 |
|---|---|---|---|
| [chrisryugj/archhub-mcp](https://github.com/chrisryugj/archhub-mcp) | 확인 못 함 | URLError: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in… | `https://archhub-mcp.fly.dev/mcp` |
| [harimkang/mcp-korea-tourism-api](https://github.com/harimkang/mcp-korea-tourism-api) | 확인 못 함 | HTTP 200 | `https://pypi.org/project/mcp` |
| [hwain-ai/Real-Estate-Location-Analyzer_MCP](https://github.com/hwain-ai/Real-Estate-Location-Analyzer_MCP) | 확인 못 함 | HTTP 404 | `https://immortal0900-real-estate-location-analyzer-mcp.hf.space/gradio_api/mcp/sse` |
| [iiacjay/incheon-airport-mcp](https://github.com/iiacjay/incheon-airport-mcp) | 확인 못 함 | HTTP 404 | `https://incheon-airport-mcp-production.up.railway.app/mcp` |
| [kendrick-na/segeum-matjip](https://github.com/kendrick-na/segeum-matjip) | 확인 못 함 | UnicodeError: label empty or too long | `https://.../mcp` |
| [lucidwatper/Kosis-mcp](https://github.com/lucidwatper/Kosis-mcp) | 확인 못 함 | HTTP 400 | `https://kosis-mcp-70b9.onrender.com/mcp` |
| [obundh/korea-public-data-catalog-mcp](https://github.com/obundh/korea-public-data-catalog-mcp) | 확인 못 함 | HTTP 404 | `https://korea-public-data-catalog-mcp-production.up.railway.app/mcp` |
| [sjh9714/electronics-price-mcp](https://github.com/sjh9714/electronics-price-mcp) | 확인 못 함 | HTTP 404 | `https://electronics-price-mcp.jinhyuk9714.workers.dev/mcp` |
| [taxwoong/nts-tax-mcp](https://github.com/taxwoong/nts-tax-mcp) | 확인 못 함 | HTTP 404 | `https://web-production-10fe2.up.railway.app/mcp` |
| [yonghwan1106/korea-culture-mcp](https://github.com/yonghwan1106/korea-culture-mcp) | 확인 못 함 | HTTP 404 | `https://korea-culture-mcp.vercel.app/mcp` |

---

[← 목록으로](README.md)
