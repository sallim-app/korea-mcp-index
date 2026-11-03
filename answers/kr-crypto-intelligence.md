# io.github.bakyang2/kr-crypto-intelligence

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://mcp.printmoneylab.com/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_kr_news_semiconductor_summary | `{}` | 결제 필요 (x402 프로토콜, $0.1 USDC), rc=1 |
| 2 | check_health | `{}` | 서비스 상태 확인, rc=0 |

### 답변

죄송하지만, 이 MCP 서버는 삼성전자의 재무 실적 정보를 제공하지 않습니다. 

이 서버는 **한국 암호화폐 거래소(Upbit, Bithumb, Binance) 정보 서버**이며, 주식 시장의 재무 데이터(매출, 영업이익 등)는 다루지 않습니다. 

반도체 뉴스 도구(`get_kr_news_semiconductor_summary`)가 있지만, 이는 뉴스 정보일 뿐 정확한 재무 실적 수치는 포함하지 않으며, 추가로 $0.1 USDC 결제가 필요합니다.

**필요한 정보를 얻으려면**: 금융 데이터 MCP(예: 한국 증권 거래소 정보 서버) 또는 금융 포털(네이버 금융, 국민은행 금융결산, 공시 시스템 등)을 이용하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
도구 목록: get_kimchi_premium, get_kr_prices, get_fx_rate, get_available_symbols, 
get_stablecoin_premium, check_health, get_arbitrage_scanner, get_exchange_alerts, 
get_market_movers, get_market_read, get_kr_sentiment, get_krw_macro_stress, 
get_global_vs_korea_divergence, get_kr_news_kpop, get_kr_news_kpop_summary, 
get_kr_news_semiconductor, get_kr_news_semiconductor_summary

서비스 헬스: {"status":"ok","exchanges":{"upbit":"ok","bithumb":"ok","binance":"ok"}}
→ 암호화폐 거래소만 모니터링 중
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | check_health | `{}` | 서비스 제공 범위 확인, rc=0 |

### 답변

죄송하지만, 이 MCP 서버는 코스피(한국 주식 시장) 시가총액 정보를 제공하지 않습니다.

이 서버는 **한국 암호화폐 거래소만** 다루며(Upbit, Bithumb, Binance), 주식 시장 정보는 제공하지 않습니다. 따라서 코스피의 시가총액 상위 종목 데이터를 조회할 수 있는 도구가 없습니다.

**필요한 정보를 얻으려면**: 한국 주식 시장 정보 MCP 또는 금융 포털(네이버 금융, 야후 파이낸스, 한국거래소 공식 사이트 등)을 이용하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
check_health 결과: {"status":"ok","exchanges":{"upbit":"ok","bithumb":"ok","binance":"ok"}}
→ 암호화폐 거래소만 포함. 코스피(KRX) 정보 없음

도구 범위: 암호화폐 가격·뉴스(K-pop, 반도체)
→ 주식 시장 도구 부재
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | (도구 호출 없음) | - | 서버 범위 밖 |

### 답변

죄송하지만 이 서버는 **한국 암호화폐 인텔리전스 서버**로, 주식 시장과 개별 기업의 재무 실적 데이터를 제공하지 않습니다. 

삼성전자의 매출과 영업이익 같은 재무 데이터는 이 서버의 도구 범위 밖입니다. 해당 정보는 한국거래소(KRX), 대신증권, 유진투자증권 등의 주식 정보 서비스나 재무 데이터 플랫폼에서 조회하실 수 있습니다.

### 근거로 쓴 응답 발췌

```
이 MCP 서버의 가용 도구:
- get_kr_prices (한국 암호화폐 가격)
- get_kimchi_premium (암호화폐 김치프리미엄)
- get_kr_news_semiconductor (한국 반도체 뉴스)
- get_market_movers (암호화폐 시장 변동)
- get_market_read (암호화폐 시장 분석)
- 기타 암호화폐 및 외환 관련 도구

모두 암호화폐 또는 암호화폐 시장 인텔리전스에 특화.
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| - | (도구 호출 없음) | - | 서버 범위 밖 |

### 답변

이 서버는 **한국 암호화폐 인텔리전스 서버**로, 코스피 지수와 주식 시장의 시가총액 순위 데이터를 제공하지 않습니다.

코스피(KOSPI) 상위 종목 정보는 한국거래소, 네이버 금융, 야후 파이낸스, 블룸버그 등의 주식 정보 서비스에서 실시간으로 확인하실 수 있습니다. 이 서버는 암호화폐 시장 분석에만 특화되어 있습니다.

### 근거로 쓴 응답 발췌

```
MCP 서버 tool list 조회 결과:
도구명 목록에 포함된 도구:
- 암호화폐 가격 및 거래소 데이터 (Upbit, Bithumb)
- 해외 암호화폐 시장 데이터 (Binance)
- 한국 암호화폐 관련 뉴스 및 시장 분석

주식 시장 데이터 도구: 없음
코스피 지수 도구: 없음
주식 시가총액 도구: 없음
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_kr_news_semiconductor_summary | `{}` | 결제 필요(유료), 실제 데이터 미수신, rc=1 |

### 답변

죄송하지만, 이 MCP 서버(`https://mcp.printmoneylab.com/mcp`)에서는 **삼성전자 실적(매출·영업이익) 데이터를 제공하지 않습니다.**

이유: 이 서버는 암호화폐 시장(Upbit, Bithumb 등)과 한국 뉴스(K-pop, 반도체) 관련 도구들을 제공합니다. 반도체 뉴스 도구는 있지만 이는 **뉴스 기사**이며, **재무 실적(매출액·영업이익 같은 정형 지표)**은 범위 밖입니다. 또한 해당 유료 도구는 현재 x402 결제 프로토콜이 필요해 데이터를 받을 수 없습니다.

### 근거로 쓴 응답 발췌

```json
{
  "status": "payment_required",
  "endpoint": "/api/v1/kr-news/semiconductor-summary",
  "price": "$0.1000 USDC",
  "message": "This endpoint requires $0.1000 USDC payment via x402 protocol. MCP tools currently return free metadata only. For actual data, call the HTTP API directly with an x402-capable client."
}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_market_movers | `{}` | 결제 필요(유료), 실제 데이터 미수신, rc=1 |

### 답변

죄송하지만, 이 MCP 서버에서는 **코스피 시가총액 상위 종목 정보를 제공하지 않습니다.**

이유: 이 서버의 모든 도구는 **암호화폐 시장**(Upbit의 알트코인, Bithumb, Binance 등)과 **한국 뉴스**(K-pop, 반도체)에만 특화되어 있습니다. 코스피·주식시장 데이터는 범위 밖입니다. 제공하는 도구 중 `get_market_movers`도 한국 암호화폐 거래소의 변동 종목을 추적할 뿐, 주식시장 시가총액 정보는 없습니다.

### 근거로 쓴 응답 발췌

```json
{
  "status": "payment_required",
  "endpoint": "/api/v1/market-movers",
  "price": "$0.0100 USDC",
  "message": "This endpoint requires $0.0100 USDC payment via x402 protocol. MCP tools currently return free metadata only."
}
```

도구 목록 분석 결과:
- `get_kr_prices` — 한국 거래소(Upbit, Bithumb) **암호화폐** 가격
- `get_available_symbols` — **암호화폐** 심볼만 반환
- `get_market_movers` — Upbit의 **암호화폐** 변동 추적
- 주식시장 또는 코스피 관련 도구 없음
