# com.airblockfz/stock-signal-kr

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://stock-signal-kr.airblock2026.workers.dev/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | evaluate_symbol | `{"symbol":"005930.KS"}` | HTTP 402 Payment Required — 결제 필요, rc=1 |

### 답변

이 서버는 삼성전자의 재무 실적(매출, 영업이익)을 제공하지 않습니다. stock-signal-kr은 기술적 신호와 차트 지표에 기반한 매수/매도 신호만 제공하는 서버로, 상세한 도구 호출에는 결제($0.01 per call 또는 $50/월 구독)가 필요합니다. 

무료로 제공되는 정보는 코스피 지수(^KS11)의 헤드라인 신호뿐이며, 삼성전자를 포함한 개별 종목의 평가나 실적 정보는 도구의 범위에 없습니다.

### 근거로 쓴 응답 발췌

```
"catalog":{"total":14,"free":0,"sub":14,"groups":2,
"youGet":{"free":"headline verdict for this market's showcase symbol only (1 symbol, zone + score + coarse per-timeframe lean)","paid":"any symbol in the universe: the fused bottom/top verdict + -100..+100 score, the daily/weekly/monthly breakdown with vote counts behind it, and the engine rule that produced it"
"provenance":{"source":"Yahoo Finance OHLC via the flagship KospiAI desktop scan export","universe":"KOSPI + KOSDAQ names + ^KS11 index (~103 symbols)"
"offer":{"try":"$0.01 per call — run evaluate_symbol on ANY symbol, no account, pay via x402","unlimited":"$50 / month — every indicator's per-timeframe breakdown + scan_bottoms/scan_tops across the whole market"}
"disclaimer":"Informational indicator output. Not financial advice."
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 시장 정보 조회 성공, rc=0 |
| 2 | scan_bottoms | `{}` | HTTP 402 Payment Required — 결제 필요, rc=1 |

### 답변

이 서버는 시가총액 순위를 직접 제공하지 않습니다. 대신 기술적 신호 기반으로 현재 시장 상황을 다음과 같이 제시합니다:

**현재 코스피 지수(^KS11)**: NEUTRAL(중립) · 스코어 50/100 · 가격 5,706.6

**시장 신호**:
- 강매수(strong-buy) 신호인 종목: 33개
- 강매도(strong-sell) 신호인 종목: 9개
- 매수 신호: 5개
- 매도 신호: 2개

어떤 종목이 강매수/강매도 신호에 포함되어 있는지 확인하려면 scan_bottoms·scan_tops 도구를 호출해야 하지만, 이들 도구는 $0.01 per call 또는 $50/월 구독으로 결제가 필요합니다.

### 근거로 쓴 응답 발췌

```
"live":{"symbol":"^KS11","zone":"neutral","verdictKo":"중립","score":50,"price":5706.6,"timeframes":{"daily":{"verdict":"strong_buy","low":1,"high":0,"n":2},"weekly":{"verdict":"strong_buy","low":2,"high":0,"n":2},"monthly":{"verdict":"neutral","low":1,"high":1,"n":2}}}
"opportunities":{"atBottom":{"strong_buy":33,"buy":5},"atTop":{"strong_sell":9,"sell":2},"universe":103,"asOf":"2026-11-03T01:45:33.868Z","note":"Counts are free; which names they are is what scan_bottoms / scan_tops return."}
"edge":"One fused verdict per Korean stock, not dozens of charts."
"market":{"id":"kr","label":"Korea stocks (KOSPI / KOSDAQ + ^KS11)","engine":"KospiAI composite verdict — VERDICT-2IND-LOCK, SCAN_VER 15"
"provenance":{"source":"Yahoo Finance OHLC via the flagship KospiAI desktop scan export","universe":"KOSPI + KOSDAQ names + ^KS11 index (~103 symbols)","refresh":"snapshot pushed per scan run; every response carries asOf"
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | evaluate_symbol | `{"symbol":"005930.KS"}` | HTTP 402 결제 필요, rc=1 |

### 답변

이 서버의 evaluate_symbol 도구는 결제가 필요해 호출할 수 없습니다. 삼성전자의 최근 실적 데이터(매출과 영업이익)를 이 서버로부터 받을 수 없습니다.

이 MCP 서버는 대금 결제를 요구합니다(X Layer의 USDT 토큰 10,000 필요). 무료로 제공되는 도구는 pitch(소개)와 rate(평점만 있습니다.

### 근거로 쓴 응답 발췌

```
{"error": "tools/call 실패: HTTP 402", "body": "{\"x402Version\":2,\"error\":\"Payment required\",\"resource\":{\"url\":\"https://stock-signal-kr.airblock2026.workers.dev/mcp\",\"description\":\"KospiAI Korea stock bottom/top signal (A2MCP)\",\"mimeType\":\"\"},\"accepts\":[{\"scheme\":\"exact\",\"network\":\"eip155:196\",\"amount\":\"10000\",\"asset\":\"0x779ded0c9e1022225f8e0630b35a9b54be713736\",\"payTo\":\"0xb4cb25019c18c7f1663150e249aeeabcab67fbc6\",\"maxTimeoutSeconds\":300,\"extra\":{\"name\":\"USDT₀\",\"version\":\"1\"}}]}"
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | scan_bottoms | `{}` | HTTP 402 결제 필요, rc=1 |

### 답변

코스피 시가총액 상위 종목을 조회할 수 없습니다. 이 서버에서 시장 전체 데이터를 받을 수 있는 도구(scan_bottoms, scan_tops)도 모두 결제를 요구하기 때문입니다.

이 서버의 도구 목록을 보면:
- evaluate_symbol: 개별 종목 조회 (결제 필수)
- scan_bottoms: 시장 바닥 신호 스캔 (결제 필수, $0.01 per call)
- scan_tops: 시장 상단 신호 스캔 (결제 필수, $0.01 per call)

코스피 시가총액 상위 종목이라는 특정 데이터를 직접 제공하는 도구는 없으며, 시장 데이터에 접근하려면 결제가 필수입니다.

### 근거로 쓴 응답 발췌

```
{"error": "tools/call 실패: HTTP 402", "body": "{\"x402Version\":2,\"error\":\"Payment required\",\"resource\":{\"url\":\"https://stock-signal-kr.airblock2026.workers.dev/mcp\",\"description\":\"KospiAI Korea stock bottom/top signal (A2MCP)\",\"mimeType\":\"\"},\"accepts\":[{\"scheme\":\"exact\",\"network\":\"eip155:196\",\"amount\":\"10000\",\"asset\":\"0x779ded0c9e1022225f8e0630b35a9b54be713736\",\"payTo\":\"0xb4cb25019c18c7f1663150e249aeeabcab67fbc6\",\"maxTimeoutSeconds\":300,\"extra\":{\"name\":\"USDT₀\",\"version\":\"1\"}}]}"
```

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 서버 소개 및 시장 정보, rc=0 |

### 답변

이 서버는 재무 실적 데이터(매출, 영업이익)를 제공하지 않습니다. stock-signal-kr은 기술 차트 기반 매매 신호만 제공하는 서버로, KospiAI 14개 기술 지표를 사용하여 '매수/매도 신호'만 생성합니다. 데이터 소스가 야후 파이낸스 OHLC(가격 데이터)이기 때문에 재무제표 정보는 범위 밖입니다. 삼성전자의 실적을 조회하려면 재무 데이터 전문 서버가 필요합니다.

### 근거로 쓴 응답 발췌

```
"source":"Yahoo Finance OHLC via the flagship KospiAI desktop scan export"
"universe":"KOSPI + KOSDAQ names + ^KS11 index (~103 symbols)"
"catalog":{"total":14,"free":0,"sub":14,"groups":2,"byGroup":[{"id":"oscillator","label":"Momentum & sentiment oscillators (보조지표)","why":"Seven sub-chart oscillators time every entry/exit..."
"engine":"KospiAI composite verdict — VERDICT-2IND-LOCK, SCAN_VER 15"
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 시장 스냅샷 및 기회 정보, rc=0 |

### 답변

이 서버는 시가총액 상위 종목을 제공하지 않습니다. 대신 기술 신호 기반 '매매 시점' 순위만 제공합니다.

현재 시장 스냅샷(2026-11-03 01:45:33 UTC): 코스피 지수(^KS11)는 5706.6에서 NEUTRAL 신호(스코어 50/100)를 보이고 있습니다. 지수의 일일/주간 신호는 strong-buy(강력 매수)이나 월간은 중립입니다.

전체 103개 종목 기준, 현재 매매 시점 분류:
- Strong-buy 바닥권: 33개
- Buy 바닥권: 5개  
- Strong-sell 고점권: 9개
- Sell 고점권: 2개

구체적인 종목명과 개별 시가총액 순위는 이 서버에서 제공하지 않습니다. 개별 종목 신호 분석($0.01/호출)은 결제가 필요합니다.

### 근거로 쓴 응답 발췌

```
"live":{"symbol":"^KS11","zone":"neutral","verdictKo":"중립","score":50,"price":5706.6,"timeframes":{"daily":{"verdict":"strong_buy","low":1,"high":0,"n":2},"weekly":{"verdict":"strong_buy","low":2,"high":0,"n":2},"monthly":{"verdict":"neutral","low":1,"high":1,"n":2}}}
"opportunities":{"atBottom":{"strong_buy":33,"buy":5},"atTop":{"strong_sell":9,"sell":2},"universe":103,"asOf":"2026-11-03T01:45:33.868Z"}
"youGet":{"free":"headline verdict for this market's showcase symbol only (1 symbol, zone + score + coarse per-timeframe lean)","paid":"any symbol in the universe: the fused bottom/top verdict + -100..+100 score..."}
```
