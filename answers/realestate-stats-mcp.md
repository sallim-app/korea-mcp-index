# hlucent/realestate-stats-mcp

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_statistics | keyword="강남구 실거래" | 0건 |
| 2 | search_statistics | keyword="아파트 실거래" | 0건 |
| 3 | search_statistics | keyword="실거래" | HTTP 429 rate_limited |

### 답변
이 서버로는 답할 수 없다.

검색 쿼리 "강남구 실거래", "아파트 실거래" 모두 통계표 0건이 반환되었다. 이는 서버의 통계표 목록에 해당 키워드를 포함한 표가 없다는 뜻이다. "실거래" 단어만으로 검색 시도 시 분당 3회 요청 제한(rate limit)에 도달했다.

### 근거로 쓴 응답 발췌
```
search_statistics("강남구 실거래"): {"count":0,"results":[]}
search_statistics("아파트 실거래"): {"count":0,"results":[]}
search_statistics("실거래"): {"error":"rate_limited","message":"분당 요청 제한(3회)을 초과했습니다"}
```

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 4 | search_statistics | keyword="경매" | HTTP 429 rate_limited |

### 답변
이 서버로는 답할 수 없다.

rate limit 도달로 경매 통계표 검색을 완료하지 못했다.

### 근거로 쓴 응답 발췌
```
search_statistics("경매"): {"error":"rate_limited","message":"분당 요청 제한(3회)을 초과했습니다"}
```

## 이 서버를 쓰면서 느낀 점
- search_statistics 도구는 키워드 "강남구 실거래", "아파트 실거래" 모두 0건으로 반환했으며, 이는 서버의 통계표 목록이 한국부동산원의 738개 표 중 이 질문들을 커버하는 표를 포함하지 않는다는 뜻으로 보인다.
- 분당 3회 요청 제한이 있어 탐색을 미리 완료해야 한다. 실제 환경에서는 가능한 통계표 목록을 미리 확인한 후 키워드를 설계해야 효율적이다.
