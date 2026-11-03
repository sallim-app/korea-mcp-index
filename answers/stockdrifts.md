# io.stockdrifts/mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 호출 주소 `https://mcp.stockdrifts.io/mcp/`.
> **측정하지 못했다** — 도구가 API 키(STOCKDRIFTS_API_KEY)를 요구해 키 없이는 답하지 않았다 — 2회차에서 멈췄다. 채점·순위에 넣지 않았다.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_kpi | `{"ticker":"005930"}` | API 키 인증 필요, rc=401 |

### 답변

stockdrifts 서버는 **인증(STOCKDRIFTS_API_KEY)이 필요**해 도구를 호출할 수 없습니다.

또한 이 서버는 **재무실적(매출·영업이익) 데이터를 제공하지 않습니다**. 제공하는 것은:
- 내부자거래 정보(삼성전자 임원·주요주주가 매매한 기록)
- K-PI 스냅샷(내용 불명확)
- 내부자 거래 수익률 순위

삼성전자 실적을 알려면 **한국거래소, 전자공시시스템(DART), 또는 금융데이터 API**(예: FnGuide, FinData)를 사용해야 합니다.

### 근거로 쓴 응답 발췌

```json
{"error": {"code": "unauthorized", "status": 401, "message": "No API key available", "hint": "Set STOCKDRIFTS_API_KEY or pass an Authorization header."}}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

이 서버는 **시가총액 순위 도구를 제공하지 않습니다**.

### 답변

stockdrifts 서버는 **시가총액 상위 종목 정보가 없습니다**. 

이 서버가 제공하는 것:
- **한국(KR)**: 내부자거래 정보, 내부자 거래 수익률 리더보드, 공시 예정 거래(D005 플랜)
- **일본(JP)**: 투자자별 주식보유 리포트, 섹터별 수익률 랭킹
- **미국(US)**: 13F 투자자 포지션 추적, 펀드별 성적표

시가총액 상위 종목을 알려면 **한국거래소 공식 데이터**, **금융감시원**, 또는 **증권사 시장정보**를 사용해야 합니다.

### 근거로 쓴 응답 발췌

```
도구 목록 조회 결과:
- list_insider_trades_kr, get_insider_summary_kr
- list_top_buys_kr, list_top_sells_kr
- list_leaderboard_kr (내부자 거래 수익률 상위자)
- search_companies_kr (회사 검색)
- get_kpi (개별 종목 KPI)

→ 시가총액 순위 도구 없음
```
