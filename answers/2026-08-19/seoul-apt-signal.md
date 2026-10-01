# com.airblockfz/seoul-apt-signal

## 질문 1: 서울 강남구 아파트 실거래가가 요즘 어때?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | {} | 정상 응답 — 강남구 실시간 판정 포함 |
| 2 | evaluate_symbol | {"symbol":"강남구"} | HTTP 402 결제 필요 |

### 답변
강남구는 **강한 매도(STRONG SELL)** 신호를 보이고 있습니다. 점수는 -86.7/100입니다.

시간대별 세부:
- **일중(일일)**: 중립
- **주간**: 매도
- **월간**: 강한 매도

이는 MOLIT(국토부) 공식 실거래 데이터 기반 기술적 매매신호입니다.

### 근거로 쓴 응답 발췌
```
"live":{"symbol":"강남구","zone":"strong_sell","verdictKo":"강한매도","score":-86.7,"timeframes":{"daily":{"verdict":"neutral","verdictKo":"중립"},"weekly":{"verdict":"sell","verdictKo":"매도"},"monthly":{"verdict":"strong_sell","verdictKo":"강한매도"}}}
```

## 질문 2: 지금 경매 나온 서울 아파트 중에 유찰 많이 된 거 있어?

### 호출한 도구
| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | pitch | {} | 서버 범위 확인 |
| 3 | scan_bottoms | {} | HTTP 402 결제 필요 |
| 4 | scan_tops | {} | HTTP 402 결제 필요 |

### 답변
**이 서버로는 답할 수 없습니다.**

서버가 다루는 데이터는 MOLIT(국토부) 공식 완료된 실거래 기록입니다. 경매 유찰(낙찰 실패)은 성사되지 않은 거래이므로 MOLIT 등록 데이터에 포함되지 않습니다. 이 서버는 공식 등록 실거래가만 분석하며, 경매 과정의 유찰 통계는 별개 정보원(법원경매시스템, 온비드 등)에서 조회해야 합니다.

### 근거로 쓴 응답 발췌
```
"provenance":{"source":"MOLIT (Korean Ministry of Land) official closed-transaction records — real registered closings, not asking prices","universe":"all 25 Seoul districts; 700k+ trades since 2016"}
```

## 이 서버를 쓰면서 느낀 점
이 서버는 **MOLIT 공식 완료 실거래 데이터에만 제한됨**. 실제 거래된 가격 기반 매매신호는 충실하나, 미성사 거래(경매 유찰, 미체결 매물)는 범위 밖이다. 서버가 제공하는 기술적 신호(13개 지표 기반 강매도/강매수 판정)는 유용하지만, 실제 투자 결정을 위해서는 경매·정책·금융 규제 등 다층 데이터가 필요하다.
