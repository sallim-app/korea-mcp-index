# kr.vlsi/vlsi-korea

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://mcp.vlsi.kr/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_stock_quote | `{"query":"005930"}` | 삼성전자 주식 가격 조회, rc=0 |

### 답변

죄송하지만 이 서버는 삼성전자의 매출과 영업이익 같은 **실적 정보를 제공하지 않습니다.** VLSI Korea 서버에서 제공하는 것은 주식 가격(end-of-day 시세) 데이터뿐입니다.

대신 조회된 정보는:
- **삼성전자(Samsung Electronics, KRX: 005930)**
- 주가: 218,500원
- 변동률: -4.59% (기준일: 2026-11-03)

실적 정보(매출, 영업이익 등)를 얻으려면 **회사 공시 자료, 재무 데이터베이스, 또는 다른 금융 정보 서버**를 참고하셔야 합니다.

### 근거로 쓴 응답 발췌

```json
{"query": "005930", "matched": 1, "quote": {"slug": "samsung", "ticker": "005930.KS", "name": "Samsung Electronics (KRX: 005930)", "price": 218500.0, "currency": "KRW", "change_pct": -4.59, "data_date": "2026-11-03"}}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_market_movers | `{}` | 변동폭 큰 반도체 관련 종목 조회, rc=0 |

### 답변

죄송하지만 이 서버는 **코스피 시가총액 상위 종목 정보를 제공하지 않습니다.** 

VLSI Korea 서버는 **반도체 산업 관련 주식만 약 113개** 다루며, 다음을 제공합니다:
- 반도체 관련 종목의 주가(end-of-day 시세)
- 변동폭이 큰 종목 목록(threshold 3% 이상)

코스피 전체 시가총액 상위 종목은 이 서버의 **범위를 벗어나는 데이터**입니다. 조회된 것은 현재 변동폭이 큰 반도체 관련 종목 102개이며, 이는 시가총액 기준이 아니라 **변동률 기준** 목록입니다.

코스피 시가총액 상위 종목을 확인하려면 **한국거래소 공식 정보, 금융 포털(네이버 금융, 다음 증권 등), 또는 다른 금융 정보 서버**를 이용하시기 바랍니다.

### 근거로 쓴 응답 발췌

```json
{"threshold_pct": 3.0, "direction": "all", "count": 102, "movers": [{"slug": "screen-holdings", "ticker": "7735.T", "name": "SCREEN Holdings (TSE: 7735)", "price": 9218.0, "change_pct": -18.96, "data_date": "2026-11-02"}, ...]}
```

(참고: get_market_movers는 변동폭 3% 이상인 반도체 관련 종목 102개를 반환하며, 시가총액 상위 정보가 아닙니다.)

---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_stock_quote | `{"query":"005930"}` | 삼성전자 주가 정보, rc=0 |

### 답변

죄송합니다. VLSI Korea MCP 서버는 삼성전자의 매출, 영업이익 같은 **재무 실적 정보는 제공하지 않습니다**. 이 서버의 `get_stock_quote` 도구는 주가와 변동률 같은 시장 정보만 제공합니다.

다만 최신 주가는 다음과 같습니다:
- **종목**: Samsung Electronics (KRX: 005930)
- **가격**: 218,500 KRW
- **변동률**: -4.59% (기준: 2026-11-03)

삼성전자 재무실적(매출, 영업이익)은 이 서버 범위 밖이며, 공시 자료나 재무정보 데이터베이스에서 조회하셔야 합니다.

### 근거로 쓴 응답 발췌

```
{"query": "005930", "matched": 1, "quote": {"slug": "samsung", "ticker": "005930.KS", "name": "Samsung Electronics (KRX: 005930)", "price": 218500.0, "currency": "KRW", "change_pct": -4.59, "data_date": "2026-11-03", "snapshot_generated_at": "2026-11-03T09:18:01.516339+00:00", "disclaimer": "Delayed end-of-day data from VLSI Korea market data. Not investment advice.", "source": "VLSI Korea market data"}}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_market_movers | `{}` | 102개 종목 변동 정보, rc=0 |

### 답변

죄송합니다. VLSI Korea MCP 서버는 **코스피 시가총액 상위 종목**을 직접 제공하는 도구가 없습니다.

`get_market_movers` 도구는 변동률이 높은 종목들(절댓값 기준 3% 이상)을 반환하는데, 이는 시가총액 순위가 아니라 **변동률 순위**입니다. 또한 이 서버는 반도체 산업 특화 서버이므로, 반도체 관련 종목들의 변동 정보만 제공합니다.

코스피 전체의 시가총액 상위 종목(삼성전자, SK하이닉스, LG전자 등)은 한국거래소 공식 데이터나 금융정보 포털에서 조회하셔야 합니다.

### 근거로 쓴 응답 발췌

```
{"threshold_pct": 3.0, "direction": "all", "count": 102, "movers": [{"slug": "screen-holdings", "ticker": "7735.T", "name": "SCREEN Holdings (TSE: 7735)", "price": 9218.0, "currency": "JPY", "change_pct": -18.96, ...}, ...]}
```

(102개 반도체 관련 종목의 변동률 상위 리스트 — 시가총액 순위가 아님)

---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_stock_quote | `{"query":"005930"}` | 삼성전자 주가 조회 성공, 다만 재무 실적 정보 없음, rc=0 |

### 답변

죄송하지만 이 MCP 서버(vlsi.kr)는 **실적 정보를 제공하지 않습니다.** 

제가 조회한 것은 삼성전자(KRX: 005930)의 현재 주가인데, 매출과 영업이익 같은 재무 실적 데이터는 도구에 포함되어 있지 않습니다. 이 서버는 주로 반도체 산업의 주가 정보, 시장 동향, 뉴스를 제공하며, 개별 종목의 재무제표나 실적 관련 도구는 없습니다.

삼성전자 최근 실적을 알고 싶으시면 공식 IR 사이트나 금융 정보 사이트(DART, 네이버파이낸스 등)를 확인해야 합니다.

### 근거로 쓴 응답 발췌

```
{"query": "005930", "matched": 1, "quote": {"slug": "samsung", "ticker": "005930.KS", "name": "Samsung Electronics (KRX: 005930)", "price": 218500.0, "currency": "KRW", "change_pct": -4.59, "data_date": "2026-11-03", "snapshot_generated_at": "2026-11-03T09:18:01.516339+00:00", "disclaimer": "Delayed end-of-day data from VLSI Korea market data. Not investment advice.", "source": "VLSI Korea market data"}}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_market_movers | `{}` | 시장 변동폭이 큰 종목 102개 반환, 하지만 시가총액 기준이 아님, rc=0 |

### 답변

이 MCP 서버는 **시가총액 기준으로 정렬된 코스피 종목 정보를 제공하지 않습니다.**

제가 호출한 도구(get_market_movers)는 변동폭이 3% 이상인 변동성 상위 종목을 보여줄 뿐, 시가총액 기준이 아닙니다. 따라서 현재 코스피 시가총액 상위 종목 순위를 알 수 없습니다.

코스피 시가총액 상위 종목을 알고 싶으시면 한국거래소(KRX) 홈페이지나 금융 정보 포털을 이용하시기 바랍니다.

### 근거로 쓴 응답 발췌

```
{"threshold_pct": 3.0, "direction": "all", "count": 102, "movers": [{"slug": "screen-holdings", "ticker": "7735.T", "name": "SCREEN Holdings (TSE: 7735)", "price": 9218.0, "currency": "JPY", "change_pct": -18.96, "data_date": "2026-11-02"...}, {"slug": "lumentum", "ticker": "LITE", "name": "Lumentum Holdings Inc. (NASDAQ: LITE)", "price": 684.4000244140625, "currency": "USD", "change_pct": -18.59, "data_date": "2026-11-02"...}, ...
```

---

완료 vlsi-korea r3
