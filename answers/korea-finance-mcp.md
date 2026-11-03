# emceeKim/korea-finance-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 호출 주소 `https://korea-finance-mcp-divine-hillside-8872.fly.dev/mcp`.
> **측정하지 못했다** — tools/call 응답이 HTTP 청크 중간에서 끊겨(IncompleteRead) 우리 호출기가 읽지 못했다(rc=3) — 1회차에서 멈췄다. 채점·순위에 넣지 않았다.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_company | `{"query":"삼성전자"}` | HTTP 연결 실패 (IncompleteRead), rc=3 |

### 답변

MCP 서버(`https://korea-finance-mcp-divine-hillside-8872.fly.dev/mcp`)에 연결할 수 없습니다. HTTP 통신 중 응답이 불완전하게 끊겼습니다(IncompleteRead). 삼성전자 실적 정보를 조회할 수 없습니다.

### 근거로 쓴 응답 발췌

```
http.client.IncompleteRead: IncompleteRead(0 bytes read)
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | get_market_index | `{"index_code":"KOSPI"}` | HTTP 연결 실패 (IncompleteRead), rc=3 |

### 답변

MCP 서버에 연결할 수 없어 코스피 지수 정보를 조회할 수 없습니다. 현재 상위 시가총액 종목 정보도 제공할 수 없습니다.

### 근거로 쓴 응답 발췌

```
http.client.IncompleteRead: IncompleteRead(0 bytes read)
```
