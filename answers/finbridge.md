# kr.gronox/finbridge

> 2026-10-01 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://mcp.gronox.kr/mcp`.


---

# 1회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_dart_company | `{"query": "삼성전자"}` | 호출 실패 (HTTP 401 Unauthorized) |
| 2 | query_db | `{"sql": "SELECT * FROM companies LIMIT 1"}` | 호출 실패 (HTTP 401 Unauthorized) |

### 답변

finbridge 서버의 도구 호출이 실패했습니다. 서버가 인증을 요구하고 있으나 제공된 명령어로는 인증 토큰을 전달할 수 없어 응답을 받을 수 없습니다.

### 근거로 쓴 응답 발췌
```
HTTP 401 Unauthorized: "Provide 'Authorization: Bearer <token>'."
```

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | query_db | `{"sql": "SELECT * FROM stocks ORDER BY market_cap DESC LIMIT 10"}` | 호출 실패 (HTTP 401 Unauthorized) |

### 답변

finbridge 서버의 도구 호출이 실패했습니다. 서버가 인증을 요구하고 있으나 제공된 명령어로는 인증 토큰을 전달할 수 없어 응답을 받을 수 없습니다.

### 근거로 쓴 응답 발췌
```
HTTP 401 Unauthorized: "Provide 'Authorization: Bearer <token>'."
```


---

# 2회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_dart_company | `{"query": "삼성전자"}` | 호출 실패 (rc=3) |

### 답변

죄송합니다. 금융 데이터 서버(finbridge)에 연결할 수 없어서 삼성전자 실적 정보를 조회할 수 없습니다. 인증 토큰이 필요합니다.

### 근거로 쓴 응답 발췌
```
HTTP 401 오류: Unauthorized. 인증 토큰 필요 (Authorization: Bearer <token>)
```

---

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | query_db | `{"sql": "SELECT * FROM ... ORDER BY market_cap DESC LIMIT 10"}` | 호출 실패 (rc=3) |

### 답변

금융 데이터 서버(finbridge)의 인증 문제로 코스피 시가총액 상위 종목을 조회할 수 없습니다.

### 근거로 쓴 응답 발췌
```
HTTP 401 오류: Unauthorized. 인증 토큰 필요
```


---

# 3회차

## 질문 1: 삼성전자 최근 실적이 어때? 매출이랑 영업이익 알려줘.

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_dart_company | `{"query":"삼성전자"}` | 호출 실패 (rc=3, HTTP 401 Unauthorized) |

### 답변

서버에 요청을 전송할 수 없었습니다. 호출 실패(인증 오류)로 인해 삼성전자의 최근 실적 정보를 조회하지 못했습니다.

### 근거로 쓴 응답 발췌
```
호출 실패 상세:
Error: "Unauthorized. Provide 'Authorization: Bearer <token>'."
HTTP Status: 401
```

## 질문 2: 코스피 시가총액 상위 종목이 지금 뭐야?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | query_db | `{"sql":"SELECT * FROM stocks ORDER BY market_cap DESC LIMIT 10"}` | 호출 실패 (rc=3, HTTP 401 Unauthorized) |

### 답변

서버에 요청을 전송할 수 없었습니다. 호출 실패(인증 오류)로 인해 코스피 시가총액 상위 종목 정보를 조회하지 못했습니다.

### 근거로 쓴 응답 발췌
```
호출 실패 상세:
Error: "Unauthorized. Provide 'Authorization: Bearer <token>'."
HTTP Status: 401
```
