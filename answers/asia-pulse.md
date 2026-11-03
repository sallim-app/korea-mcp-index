# com.asia-pulse/asia-pulse

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://asia-pulse.com/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | chain_semis | `{}` | 유료 도구(0.1 USD) — 접근 불가, rc=3 |

### 답변

죄송합니다. 이 MCP 서버의 반도체 데이터 도구(chain_semis)는 유료 서비스라 사용할 수 없습니다. 

삼성전자의 최근 실적(매출·영업이익)을 조회하려면 이 서버의 한국 반도체 축 데이터가 필요한데, 해당 도구가 0.1 USD의 결제를 요구하고 있습니다. 무료 도구만으로는 이 정보를 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
{"x402Version": 2, "error": "Payment required to access this tool", "resource": {"url": "mcp://tool/chain_semis", "description": "Korea semiconductor supply chain with listed companies.", "mimeType": "application/json"}, "accepts": [{"scheme": "exact", "network": "eip155:8453", "amount": "100000", "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "payTo": "0x30c13c7fc1d975e6fc3af5d5154081cb5e52ff54", "maxTimeoutSeconds": 60, "extra": {"name": "USD Coin", "version": "2"}}]}
Pay per call over x402 at https://asia-pulse.com/chain/semis ($0.1).
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | report | `{}` | 유료 도구(0.03 USD) — 접근 불가, rc=3 |
| 2 | brief_preview | `{}` | 제목만 제공, 실적 데이터 없음, rc=0 |

### 답변

죄송합니다. 이 MCP 서버의 무료 도구로는 코스피 시가총액 상위 종목 정보를 제공할 수 없습니다.

- **유료 도구**: 시장 데이터(report)는 0.03 USD의 결제가 필요합니다.
- **무료 도구**: 브리프 미리보기(brief_preview)는 제목과 연결된 섹션만 제공하며 실제 시가총액 데이터는 포함되지 않습니다.

이 서버는 주로 블록체인 기반 x402 결제 네트워크를 통한 유료 금융 데이터 서비스입니다.

### 근거로 쓴 응답 발췌

```
{"date": "2026-11-03", "stories": [{"title": "Asia Brief, Nov 3 — story 1 of 2: Entertainment", "linked": []}, {"title": "Asia Brief, Nov 3 — story 2 of 2: Market", "linked": ["KR defense"]}]}

{"x402Version": 2, "error": "Payment required to access this tool", "resource": {"url": "mcp://tool/report", "description": "Seoul and Tokyo session state, kimchi premium, BTC and ETH funding, BTC regime; premium layers refresh every 30 minutes.", "mimeType": "application/json"}
Pay per call over x402 at https://asia-pulse.com/report ($0.03).
```

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | brief_preview | `{}` | 무료 도구이나 최신 뉴스 제목만 반환, 실적 수치 미포함, rc=0 |

### 답변

죄송하지만 이 서버는 삼성전자 최근 실적(매출, 영업이익)을 제공하지 않습니다. 

asia-pulse MCP 서버가 제공하는 도구는 한국 반도체·방위산업·전력망 공급망의 거시 지표, 암호화폐 시장 현황, 일본 경제 데이터 등을 담고 있으나, 개별 상장기업의 재무 실적은 범위 밖입니다. 유료 도구들도 마찬가지입니다.

### 근거로 쓴 응답 발췌

```
"brief_preview": "Story titles and linked companies from the latest Korea attention brief. Free."
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | brief_preview | `{}` | 무료 도구이나 최신 뉴스 제목만 반환, 시장 구성 정보 미포함, rc=0 |

### 답변

이 서버는 코스피 시가총액 상위 종목 목록을 제공하지 않습니다.

asia-pulse의 도구들은 거시 지표·섹터 베타·공급망 분석·거래소 세션 상태 같은 집계 수준의 데이터를 다루며, 개별 종목의 시가총액 순위나 종목 리스트 정보는 포함하지 않습니다. 무료 도구인 brief_preview도 뉴스 제목 링크만 제공합니다.

### 근거로 쓴 응답 발췌

```
도구 목록:
- catalog: 상품 가격 및 엔드포인트 목록 (실적·시가총액 미포함)
- chain: 한국 반도체·방위산업·전력망 공급망 (섹터 베타, 뉴스이벤트)
- chain_semis: 반도체축만 (수출·베타 데이터)
- brief_preview: 뉴스 제목만 제공
```

완료 asia-pulse r2

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | brief_preview | `{}` | 스토리 제목만 반환(구체 데이터 없음), rc=0 |
| 2 | chain_semis | `{}` | 결제 필요(x402 $0.1), rc=1 |
| 3 | report | `{}` | 결제 필요(x402 $0.03), rc=1 |

### 답변

죄송하지만 이 서버는 삼성전자의 최근 실적(매출, 영업이익) 정보를 제공하는 무료 도구가 없습니다. 

반도체 공급망 정보를 다루는 `chain_semis` 도구나 한국 시장 데이터를 제공하는 `report` 도구가 있지만, 모두 x402 결제가 필요합니다. 무료로 제공되는 `brief_preview` 도구는 뉴스 스토리 제목만 반환하고 실적 수치는 담지 않습니다.

### 근거로 쓴 응답 발췌

```
brief_preview 응답:
{"date": "2026-11-03", "stories": [{"title": "Asia Brief, Nov 3 — story 1 of 2: Entertainment", "linked": []}, {"title": "Asia Brief, Nov 3 — story 2 of 2: Market", "linked": ["KR defense"]}]}

chain_semis 응답 (Payment required):
"Pay per call over x402 at https://asia-pulse.com/chain/semis ($0.1). Call that HTTPS endpoint with an x402 payment header; it returns the data."

report 응답 (Payment required):
"Pay per call over x402 at https://asia-pulse.com/report ($0.03). Call that HTTPS endpoint with an x402 payment header; it returns the data."
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | brief_preview | `{}` | 스토리 제목만 반환(구체 데이터 없음), rc=0 |
| 2 | report | `{}` | 결제 필요(x402 $0.03), rc=1 |

### 답변

이 서버에서 코스피 시가총액 상위 종목 정보를 얻을 수 없습니다.

한국 시장 데이터를 제공하는 `report` 도구가 있지만 유료(x402 $0.03)입니다. 무료 도구인 `brief_preview`는 뉴스 스토리 제목만 반환할 뿐, 종목별 시가총액 정보는 담지 않습니다.

### 근거로 쓴 응답 발췌

```
brief_preview 응답 (무료, 하지만 제목만 제공):
{"date": "2026-11-03", "stories": [{"title": "Asia Brief, Nov 3 — story 1 of 2: Entertainment", "linked": []}, {"title": "Asia Brief, Nov 3 — story 2 of 2: Market", "linked": ["KR defense"]}]}

catalog의 도구 가격표:
- report (Seoul session state, Korea market data): 필수 결제 필요
- chain_semis, chain_defense, chain_power 등 세부 공급망: 모두 유료
```
