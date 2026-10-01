# com.airblockfz/seoul-apt-signal

> 2026-10-01 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://seoul-apt-signal.airblock2026.workers.dev/mcp`.


---

# 1회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | evaluate_symbol | `{"symbol":"강남구"}` | 호출 실패, HTTP 402 Payment Required (rc=3) |

### 답변

이 서버의 핵심 데이터 도구들은 모두 결제 기반이며, 현재 계정에 구독이 활성화되어 있지 않아 강남구의 실거래가 정보를 조회할 수 없습니다. 서버가 응답을 제공하지 못했습니다.

### 근거로 쓴 응답 발췌
```
{
  "error": "tools/call 실패: HTTP 402",
  "body": "{\"x402Version\":2,\"error\":\"Payment required\",
  \"resource\":{\"url\":\"https://seoul-apt-signal.airblock2026.workers.dev/mcp\",
  \"description\":\"Bit Monk Seoul Apartments bottom/top signal (A2MCP)\"},
  \"accepts\":[{\"scheme\":\"exact\",\"network\":\"eip155:196\",
  \"amount\":\"10000\",\"asset\":\"0x779ded0c9e1022225f8e0630b35a9b54be713736\"}]}"
}
```

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | - | - | 도구 없음 |

### 답변

이 서버(Seoul Apartment Signal)는 서울 아파트의 실거래가 신호와 시장 수급 판정만 제공하며, 법원경매 관련 정보는 다루지 않습니다. 경매 유찰 데이터를 조회할 수 있는 도구가 이 서버에는 없습니다.

### 근거로 쓴 응답 발췌

```
서버 도구 목록:
- pitch: 소개 도구
- evaluate_symbol: 특정 구의 실거래가 신호 (결제 필요)
- scan_bottoms: 저점 구들 스캔 (결제 필요)
- scan_tops: 고점 구들 스캔 (결제 필요)
- subscribe: 구독 상태 확인 (무료)
- rate: 사용자 피드백 (무료)

경매/유찰 관련 도구 없음
```


---

# 2회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 성공 (rc 0) — 강남구 신호 정보 및 시장 현황 제공 |

### 답변

강남구 아파트 시장은 현재 **중립(NEUTRAL)** 신호를 보이고 있으며, 점수는 -67/100입니다(약한 부정). 시간대별 판정은 다음과 같습니다:
- 일일(daily): 중립
- 주간(weekly): 매도
- 월간(monthly): 중립

이는 2026년 9월 30일 02:50:23 UTC 기준 데이터입니다. 서울 25개 지구 전체적으로는 현재 강한 매수 바닥이 2개 지구, 강한 매도 톱(과열)이 6개 지구인 상태입니다.

### 근거로 쓴 응답 발췌
```
"live":{"symbol":"강남구","zone":"neutral","verdictKo":"중립","score":-66.7,"timeframes":{"daily":{"verdict":"neutral","verdictKo":"중립","low":1,"high":0,"n":2},"weekly":{"verdict":"sell","verdictKo":"매도","low":0,"high":1,"n":2},"monthly":{"verdict":"neutral","verdictKo":"중립","low":0,"high":1,"n":2}}},"opportunities":{"atBottom":{"strong_buy":2,"buy":1},"atTop":{"strong_sell":6,"sell":2},"universe":25,"asOf":"2026-09-30T02:50:23.888Z"
```

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 성공 (rc 0) — 서버 기능 확인 |
| 2 | scan_tops | `{}` | 호출 실패 (rc 3) — 결제 필요 |

### 답변

이 서버는 경매 유찰 정보를 제공하지 않습니다. 서버는 서울 25개 지구의 공식 실거래 데이터(MOLIT 기관통계)를 기반으로 하는 시장 신호(바닥/톱)만 다루며, 경매 물건이나 유찰률에 대한 데이터는 담지 않습니다. 경매 정보는 다른 서비스에서 조회하셔야 합니다.

### 근거로 쓴 응답 발췌
```
"market":{"id":"sa","label":"Seoul apartments (25 districts · official MOLIT actual-transaction prices, 2016~now)","engine":"SeoulAptAI composite verdict — VERDICT-2IND-LOCK standard model, SCAN_VER 11","timeframes":["daily","weekly","monthly"],"sampleSymbol":"강남구","provenance":{"source":"MOLIT (Korean Ministry of Land) official closed-transaction records — real registered closings, not asking prices"
```


---

# 3회차

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | `{}` | 성공 · 강남구 중립(score -67) · 주간 매도 신호 |
| 2 | evaluate_symbol | `{"symbol":"강남구"}` | rc=3 · HTTP 402 결제 필요 |

### 답변

강남구 아파트 시장은 현재 **중립(NEUTRAL)** 상태입니다.

서버가 제공한 무료 정보에 따르면:
- **종합 신호**: 중립 (zone: neutral)
- **점수**: -67/100
- **시간대별 신호**:
  - 일일(Daily): 중립
  - 주간(Weekly): 매도(sell)
  - 월간(Monthly): 중립

더 상세한 분석(일일/주간/월간 지표 항목별 점수, 매매 거래량별 중앙값 등)을 받으려면 `evaluate_symbol` 도구를 이용해야 하는데, 이는 유료($0.01/회)입니다. 현재 이 서버는 결제 인증(x402 Lightning wallet)이 필요합니다.

### 근거로 쓴 응답 발췌
```
"live":{"symbol":"강남구","zone":"neutral","verdictKo":"중립","score":-66.7,"timeframes":{"daily":{"verdict":"neutral","verdictKo":"중립"},"weekly":{"verdict":"sell","verdictKo":"매도"},"monthly":{"verdict":"neutral","verdictKo":"중립"}}}
```

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | scan_bottoms | `{}` | rc=3 · HTTP 402 결제 필요 |

### 답변

이 서버는 경매(법원경매, 유찰 통계) 데이터를 제공하지 않습니다.

서버가 제공하는 도구들은 부동산 시세 신호(매매 거래가 기반 매수/매도 판정)에 특화되어 있습니다. 법원경매의 유찰률 같은 경매 시장 통계는 이 서버의 범위 밖입니다.

경매 정보가 필요한 경우, 캠코(Korea Asset Management Service) 공매 시스템이나 법원 경매 정보 시스템(e-나라 법원경매) 같은 전문 채널을 확인하시기 바랍니다.

### 근거로 쓴 응답 발처
```
서버 도구 목록: pitch, evaluate_symbol, scan_bottoms, scan_tops, subscribe, rate
— 경매 유찰 데이터를 반환하는 도구 없음
```
