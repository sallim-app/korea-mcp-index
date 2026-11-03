# com.airblockfz/seoul-apt-signal

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://seoul-apt-signal.airblock2026.workers.dev/mcp`.


---

# 1회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | evaluate_symbol | `{"symbol":"Gangnam"}` | HTTP 402 Payment Required — 서버가 USDT 결제를 요청함, rc=3 |

### 답변

죄송합니다. 이 서버의 주요 분석 도구들은 유료 결제(블록체인 기반 USDT)가 필요해서 조회할 수 없습니다. 강남구 아파트 실거래가 분석을 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
{"error": "tools/call 실패: HTTP 402", "body": "{\"x402Version\":2,\"error\":\"Payment required\",\"resource\":{\"url\":\"https://seoul-apt-signal.airblock2026.workers.dev/mcp\",\"description\":\"Bit Monk Seoul Apartments bottom/top signal (A2MCP)\",\"mimeType\":\"\"},\"accepts\":[{\"scheme\":\"exact\",\"network\":\"eip155:196\",\"amount\":\"10000\",\"asset\":\"0x779ded0c9e1022225f8e0630b35a9b54be713736\",\"payTo\":\"0xb4cb25019c18c7f1663150e249aeeabcab67fbc6\",\"maxTimeoutSeconds\":300,\"extra\":{\"name\":\"USDT₀\",\"version\":\"1\"}}]}
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

(호출하지 않음)

### 답변

이 서버는 경매 데이터를 제공하지 않습니다. 이 서버의 도구는 서울 25개 구의 아파트 실거래 신호(저점/고점)만 제공하며, 경매·유찰 관련 기능은 범위 밖입니다. 경매 유찰 관련 질문에는 다른 부동산 MCP 서버를 사용해야 합니다.

---

# 2회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | evaluate_symbol | `{"symbol":"강남"}` | 결제 필요(HTTP 402), rc=3 |

### 답변

죄송합니다. 이 서버의 실거래가 신호 도구는 유료 서비스로, 호출하려면 X Layer 2 네트워크의 USDT 결제가 필요합니다. 서버가 응답을 제공하지 않아 강남구 아파트 실거래 현황을 조회할 수 없습니다.

### 근거로 쓴 응답 발췌

```
HTTP 402 Payment Required
x402Version: 2
error: "Payment required"
accepts: [{"scheme":"exact","network":"eip155:196","amount":"10000","asset":"0x779ded0c9e1022225f8e0630b35a9b54be713736"}]
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 없음 | - | - | 해당 도구 없음 |

### 답변

이 서버는 서울 아파트의 **실거래가 신호(바닥/상단 판정)**에만 특화되어 있으며, 법원경매나 유찰 통계는 제공하지 않습니다. 경매 물건의 유찰 현황을 조회하려면 법원경매 데이터를 다루는 별개 MCP 서버가 필요합니다.

### 근거로 쓴 응답 발췌

```
서버 도구 목록 (총 5종):
- pitch (소개)
- evaluate_symbol (강남구 등 지구별 바닥/상단 판정)
- scan_bottoms (서울 25개 지구 바닥 찾기)
- scan_tops (서울 25개 지구 상단 찾기)
- subscribe (구독 상태)
- rate (피드백)

경매·유찰 관련 도구: 없음
```

완료 seoul-apt-signal r2

---

# 3회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 서울 25개 구 시장 소개 및 강남구 신호 반환, rc=0 |
| 2 | evaluate_symbol | `{"symbol":"강남구"}` | 결제 필요(402), rc=3 |

### 답변

이 서버는 MOLIT 공시 실거래 데이터로 기술적 신호(13개 기술지표)를 생성하는 유료 서비스입니다.

**강남구 현재 신호(무료 제공 범위):**
- 종합 판정: **중립(NEUTRAL)** · 점수 -50.9/100
- 일일(daily): 강한매도
- 주간(weekly): 중립
- 월간(monthly): 중립

기술지표 세부 분석(마모멘텀·가격오버레이 등)은 유료 구독이 필요합니다. 개별 구역별 상세 평가도 호출당 $0.01(x402 블록체인 결제) 또는 월 $50 구독으로 이용 가능합니다. 서버가 실거래 **수치**(가격, 거래량, 평당가 등)는 유료 범위에만 제공하므로 이 조회로는 받을 수 없습니다.

### 근거로 쓴 응답 발췌

```
"market":{"id":"sa","label":"Seoul apartments (25 districts · official MOLIT actual-transaction prices, 2016~now)","engine":"SeoulAptAI composite verdict — VERDICT-2IND-LOCK standard model, SCAN_VER 11","timeframes":["daily","weekly","monthly"],"sampleSymbol":"강남구","provenance":{"source":"MOLIT (Korean Ministry of Land) official closed-transaction records — real registered closings, not asking prices"}}
"live":{"symbol":"강남구","zone":"neutral","verdictKo":"중립","score":-50.9,"timeframes":{"daily":{"verdict":"strong_sell","verdictKo":"강한매도"},"weekly":{"verdict":"neutral","verdictKo":"중립"},"monthly":{"verdict":"neutral","verdictKo":"중립"}}}
"youGet":{"free":"headline verdict for this market's showcase symbol only (1 symbol, zone + score + coarse per-timeframe lean)","paid":"any symbol in the universe: the fused bottom/top verdict + -100..+100 score, the daily/weekly/monthly breakdown with vote counts behind it, and the engine rule that produced it"}
"error": "Payment required"
```

---

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 서버 범위 확인, rc=0 |

### 답변

이 서버는 경매와 유찰 데이터를 제공하지 않습니다. MOLIT 공시 **실거래(closed-transaction)** 데이터만 다루므로, 법원경매나 공매의 경매 건수·유찰률 정보는 범위 밖입니다.

경매 유찰 데이터는 다른 출처(법원·캠코)를 통해 별도로 조회해야 합니다.

### 근거로 쓴 응답 발췌

```
"market":{"id":"sa","label":"Seoul apartments (25 districts · official MOLIT actual-transaction prices, 2016~now)","provenance":{"source":"MOLIT (Korean Ministry of Land) official closed-transaction records — real registered closings, not asking prices","universe":"all 25 Seoul districts; 700k+ trades since 2016, volume-weighted median price per pyeong"}}
```
