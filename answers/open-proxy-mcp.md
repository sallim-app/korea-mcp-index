# MarcoYou/open-proxy-mcp

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 호출 주소 `https://open-proxy-mcp.fly.dev/mcp`.
> **측정하지 못했다** — 도구가 사용자 본인의 DART API 키를 요구해 키 없이는 답하지 않았다 — 1회차에서 멈췄다. 채점·순위에 넣지 않았다.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | company | `{"query":"삼성전자"}` | DART API 키 부재로 실행 불가, rc=3 |

### 답변

죄송하지만, 이 서버는 금융감독원의 DART 오픈API 키가 필요한데 현재 설정되어 있지 않아 서버에 연결할 수 없습니다. 삼성전자의 매출과 영업이익 실적을 조회할 수 없습니다.

서버가 작동하려면 관리자가 다음과 같이 설정해야 합니다:
- https://opendart.fss.or.kr 에서 인증키를 신청 (무료·즉시 발급)
- 커넥터 서버 주소를 `https://open-proxy-mcp.fly.dev/mcp?opendart=<발급받은 키>` 형태로 구성

### 근거로 쓴 응답 발췌

```
{"error": "opendart API key required", "message": "DART 오픈API 키가 필요해요. 금융감독원이 무료로 발급해 주고, 신청하면 바로 받을 수 있어요.", "how_to": "① https://opendart.fss.or.kr 에서 인증키를 신청하세요(무료·즉시 발급) ② 커넥터 설정의 서버 주소 끝에 키를 붙여 다시 추가하세요 — https://open-proxy-mcp.fly.dev/mcp?opendart=<발급받은 키>"}
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | trading_data | `{}` | DART API 키 부재로 실행 불가, rc=3 |

### 답변

죄송하지만, 이 서버는 금융감독원의 DART 오픈API 키가 필요한데 현재 설정되어 있지 않아 서버에 연결할 수 없습니다. 코스피 시가총액 상위 종목 데이터를 조회할 수 없습니다.

서버가 작동하려면 관리자가 다음과 같이 설정해야 합니다:
- https://opendart.fss.or.kr 에서 인증키를 신청 (무료·즉시 발급)
- 커넥터 서버 주소를 `https://open-proxy-mcp.fly.dev/mcp?opendart=<발급받은 키>` 형태로 구성

### 근거로 쓴 응답 발췌

```
{"error": "opendart API key required", "message": "DART 오픈API 키가 필요해요. 금융감독원이 무료로 발급해 주고, 신청하면 바로 받을 수 있어요.", "how_to": "① https://opendart.fss.or.kr 에서 인증키를 신청하세요(무료·즉시 발급) ② 커넥터 설정의 서버 주소 끝에 키를 붙여 다시 추가하세요 — https://open-proxy-mcp.fly.dev/mcp?opendart=<발급받은 키>"}
```
