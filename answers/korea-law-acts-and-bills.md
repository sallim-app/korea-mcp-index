# com.koreanics/korea-law-acts-and-bills

> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 **3회** 물었다(1·2·3회차). 호출 주소 `https://koreanics.com/wp-json/koreanics/v1/mcp`.


---

# 1회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"discretionary contract State Contract Act"}` | Financial Investment Services 등 관련 법령 검색, rc=0 |
| 2 | search_law_articles | `{"query":"contract award method cases"}` | Act on Contracts to Which the State Is a Party 관련 조문 발견, rc=0 |
| 3 | search_law_articles | `{"query":"Act on Contracts to Which the State Is a Party negotiated contract cases"}` | 수의계약 조문 13개 발견, rc=0 |
| 4 | get_law_article | `{"law":"enforcement-decree-of-the-act-on-contracts-to-which-the-state-is-a-party","article":"26"}` | 수의계약 허용 요건 전문, rc=0 |

### 답변

국가계약법(정식명: 「국가계약법」의 시행령인 「국가계약법 시행령」)에서 수의계약(협상계약)을 할 수 있는 경우는 「국가계약법 시행령」 제26조에 상세히 규정되어 있습니다. 주요 경우들은 다음과 같습니다:

**1. 경합이 성립하지 않거나 경쟁을 할 여유가 없는 경우**
- 천재지변, 전염병 방역, 전쟁 작전, 긴급 재해 복구 등 긴급사태
- 국방·외교·국가보안 등 보안이 필요한 경우
- 방위사업청장이 지정한 군사용 물자

**2. 특정인의 기술이 필요하거나 유일한 생산자인 경우**
- 이전 또는 현 시공자와의 건설계약(하자책임 배분이 어려운 경우)
- 부적합한 대체품이 없는 특허상품
- 유일한 생산자 또는 공급자
- 특정인의 경험·기술·자격이 필요한 설계, 감리, 연구 용역 등

**3. 소상공인·창업자·장애인 기업 등 특정 대상 우대 계약**
- 중소기업의 인증 제품 구매
- 소상공인, 여성기업, 장애인기업과의 계약
- 사회적기업, 자활기업 등

**4. 일정 금액 이하의 소규모 계약**
- 건설공사 4억원 이하, 전문건설 2억원 이하
- 물품·용역 2천만원 이하
- 중소기업과의 계약으로 2천만원 초과 1억원 이하

**5. 그 밖의 비효율적 경우**
- 해외외교관 용품 현지 구매
- 물품 처리, 수송, 보관이 비효율적인 경우
- 방위산업 물자
- 혁신제품

근거 조문: **「국가계약법 시행령」 제26조** (시행일: 2026년 6월 3일)

### 근거로 쓴 응답 발췌

```
1 The cases in which a negotiated contract may be concluded pursuant to the proviso to Article 7(1) of the Act are as follows:
  1. Cases where there is no time to put the contract out to competition, or where it is determined that putting the contract out to competition would make it difficult to achieve the purpose of the contract, falling under any of the following items:
    가. Natural disasters, prevention and containment of the spread of infectious diseases, operational troop movements, urgent events, emergency disasters such as flood damage requiring urgent restoration, sudden surges in raw material prices, urgent safety inspections and facility improvements for accident prevention, and other cases equivalent thereto;
    나. Cases involving national security, national defense plans and intelligence activities, management of military facilities, diplomatic relations, or other equivalent matters, where there is a need for security or where the acts of State agencies need to be carried out in secret;

  2. Cases where competition cannot be established, such as where a specific person's technology is required or where there is only one producer of the relevant goods, falling under any of the following items:
    가. Cases where, in connection with construction work, it is difficult to allocate responsibility for future defects in the facilities, and a contract is made with the immediately preceding or current contractor;
    자. Cases where there is only one producer or holder of the relevant goods, and the purpose of the project cannot be achieved by having other goods manufactured, purchased, or leased;
    차. Contracts for surveys, design, supervision, special surveying, or training that require the technology, quality, experience, or qualifications of a specific person;
    
  3. Cases where the following products, directly produced by a small and medium enterprise under Article 2, subparagraph 1 of the Small and Medium Enterprises Promotion Act, are manufactured by, or purchased or leased from, that small and medium enterprise:
    가. Products that have received performance certification...
    
  5. Cases, other than those under subparagraphs 1 through 4, where it is determined, in light of the purpose, nature, etc. of the contract, that concluding the contract through competition would be inefficient, falling under any of the following items:
    가. A contract falling under any of the following: 1) A contract for construction work... with an estimated price of KRW 400 million or less
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"drunk driving punishment blood alcohol"}` | Road Traffic Act 관련 조문 10개 발견, rc=0 |
| 2 | get_law_article | `{"law":"road-traffic-act","article":"148-2"}` | 음주운전 처벌 규정 전문, rc=0 |
| 3 | get_law_article | `{"law":"road-traffic-act","article":"44"}` | 음주운전 금지 기준 정의, rc=0 |

### 답변

도로교통법의 현재 음주운전 처벌 기준은 2026년 10월 13일부터 시행되는 기준입니다. 혈중알코올농도에 따라 다음과 같이 구분됩니다:

**1. 초범 처벌**
- **혈중알코올농도 0.2% 이상**: 징역 2년 이상 5년 이하 또는 벌금 1천만원 이상 2천만원 이하
- **혈중알코올농도 0.08% 이상 0.2% 미만**: 징역 1년 이상 2년 이하 또는 벌금 5백만원 이상 1천만원 이하
- **혈중알코올농도 0.03% 이상 0.08% 미만**: 징역 1년 이하 또는 벌금 5백만원 이하

**2. 재범 처벌 (10년 이내 재위반)**
- **혈중알코올농도 0.2% 이상**: 징역 1년 이상 6년 이하 또는 벌금 5백만원 이상 3천만원 이하
- **혈중알코올농도 0.03% 이상 0.2% 미만**: 징역 1년 이상 5년 이하 또는 벌금 5백만원 이상 2천만원 이하

**3. 측정 거부·방해**
- 음주운전이 의심되면서 경찰의 호흡측정 거부: 징역 1년 이상 5년 이하 또는 벌금 5백만원 이상 2천만원 이하
- 음주운전 후 음주측정 방해: 징역 1년 이상 5년 이하 또는 벌금 5백만원 이상 2천만원 이하

**음주 기준** (제44조): 혈중알코올농도 0.03% 이상이 음주운전 금지 기준입니다.

근거 조문: **「도로교통법」 제44조 (음주운전 금지 정의), 제148-2조 (처벌규정)** (시행일: 2026년 10월 13일)

### 근거로 쓴 응답 발췌

```
Article 44, paragraph 4: The standard for the state of intoxication in which driving is prohibited under paragraph (1) is a driver's blood alcohol concentration of 0.03 percent or more.

Article 148-2, paragraph 3:
  1. A person whose blood alcohol concentration is 0.2 percent or higher: Imprisonment with labor for not less than 2 years but not more than 5 years, or a fine of not less than KRW 10 million but not more than KRW 20 million;
  2. A person whose blood alcohol concentration is 0.08 percent or higher but less than 0.2 percent: Imprisonment with labor for not less than 1 year but not more than 2 years, or a fine of not less than KRW 5 million but not more than KRW 10 million;
  3. A person whose blood alcohol concentration is 0.03 percent or higher but less than 0.08 percent: Imprisonment with labor for not more than 1 year, or a fine not exceeding KRW 5 million.

Article 148-2, paragraph 1:
  1. A person who violates Article 44(2) or (5) shall be punished by imprisonment with labor for not less than 1 year but not more than 6 years, or by a fine of not less than KRW 5 million but not more than KRW 30 million;
  2. A person who violates Article 44(1) and whose blood alcohol concentration is 0.2 percent or higher shall be punished by imprisonment with labor for not less than 2 years but not more than 6 years, or by a fine of not less than KRW 10 million but not more than KRW 30 million;

Article 148-2, paragraph 2:
  1. A person for whom there are reasonable grounds to believe that he or she is under the influence of alcohol and who refuses to comply with a test by a police officer under Article 44(2)... shall be punished by imprisonment with labor for not less than 1 year but not more than 5 years, or by a fine of not less than KRW 5 million but not more than KRW 20 million
```

---

# 2회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"State Contract Act"}` | 국가계약법 관련 조문 검색, rc=0 |
| 2 | search_law_articles | `{"query":"negotiated contract Act on Contracts to Which the State Is a Party"}` | 수의계약 관련 조문 검색, rc=0 |
| 3 | get_law_article | `{"law":"enforcement-decree-of-the-act-on-contracts-to-which-the-state-is-a-party","article":"27"}` | 수의계약 요건 조문 조회, rc=0 |

### 답변

국가계약법상 수의계약(negotiated contract)을 할 수 있는 경우는 다음과 같습니다:

**1. 입찰에 참여자가 1명뿐인 경우**
   - 공개 입찰 절차 결과 입찰자가 1명뿐이고, 2차 공고를 해도 입찰 자격 요건을 충족하는 사람이 1명뿐일 것이 명백한 경우

**2. 2차 공고 후에도 입찰자나 낙찰자가 없는 경우**
   - 2차 공고를 했으나 입찰자가 없거나 낙찰자가 없는 경우

**특수 상황:**
   - 재정경제부 장관이 재난 극복이나 경제 위기(경제 침체, 대량 실업 등)로 인한 국가경제 위기 극복 기간을 공시한 경우, 2차 공고 없이도 입찰자 1명만으로 수의계약 체결 가능

**조건:**
   - 수의계약 시 최초 입찰 시점의 가격 및 기타 조건은 원칙적으로 변경 불가 (단, 담보금과 기간은 제외)
   - 턴키 공사나 기본설계 기술제안 공사인 경우, 국가재정법에 따른 총사업비 조정으로 인한 가격 변경은 가능

### 근거로 쓴 응답 발췌

```
"Article 27: Second Public Notice of Tender and Negotiated Contract"

"1 A negotiated contract may be made if a competitive tendering procedure results in any one of the following cases:
  1. Where only one tenderer participates in a competitive tendering procedure conducted pursuant to Article 10, and it is deemed obvious that only one person meets the requirements for qualification for participation in tendering under Article 12 even if tenders are invited by the second public notice under Article 20(2)
  2. Where tenders have been invited by the second public notice under Article 20(2) but there is no tenderer or successful tenderer"

"2 In the case of a negotiated contract under paragraph (1), the price and other terms and conditions determined at the time of the initial tender may not be changed, except for the bond and the time limit"

"3 Notwithstanding subparagraph 1 of paragraph (1), where the Minister of Finance and Economy has publicly notified a period in order to overcome a disaster under subparagraph 1 of Article 3 of the Framework Act on the Management of Disasters and Safety or a national economic crisis caused by an economic recession, mass unemployment, etc., a negotiated contract may be made if only one tenderer participates in a competitive tendering procedure conducted pursuant to Article 10, even if tenders are not invited by the second public notice under Article 20(2)."
```

**법률 출처:**
- 국가계약법 시행령 제27조 (Enforcement Decree of the Act on Contracts to Which the State Is a Party, Art. 27)
- https://koreanics.com/laws/enforcement-decree-of-the-act-on-contracts-to-which-the-state-is-a-party/article-27/

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"Road Traffic Act drunk driving punishment"}` | 음주운전 처벌 조문 검색, rc=0 |
| 2 | search_law_articles | `{"query":"Road Traffic Act alcohol concentration"}` | 혈중 알코올 농도 기준 검색, rc=0 |
| 3 | get_law_article | `{"law":"road-traffic-act","article":"148-2"}` | 음주운전 처벌 규정 조회, rc=0 |

### 답변

도로교통법에서 음주운전 처벌 기준은 **혈중 알코올 농도에 따라 구분**됩니다:

**음주 운전 금지 기준:**
- 혈중 알코올 농도 **0.03% 이상**일 때 운전 금지 (도로교통법 제44조)

**처벌 기준 (1차 위반):**

1. **혈중 알코올 농도 0.2% 이상:**
   - 징역 2년 이상 6년 이하 또는 벌금 1,000만원 이상 3,000만원 이하

2. **혈중 알코올 농도 0.08% 이상 ~ 0.2% 미만:**
   - 징역 1년 이상 2년 이하 또는 벌금 500만원 이상 1,000만원 이하

3. **혈중 알코올 농도 0.03% 이상 ~ 0.08% 미만:**
   - 징역 1년 이하 또는 벌금 500만원 이하

**재범 처벌 (10년 내 재위반):**
- 더 엄격한 처벌이 적용됨
- 혈중 알코올 농도 0.2% 이상: 징역 2년 이상 6년 이하 또는 벌금 1,000만원 이상 3,000만원 이하
- 혈중 알코올 농도 0.03% 이상 ~ 0.2% 미만: 징역 1년 이상 5년 이하 또는 벌금 500만원 이상 2,000만원 이하

**추가 처벌:**
- 음주 측정 거부: 징역 1년 이상 5년 이하 또는 벌금 500만원 이상 2,000만원 이하
- 음주 측정 방해(측정 후 음주 또는 약물 복용): 징역 1년 이상 5년 이하 또는 벌금 500만원 이상 2,000만원 이하

### 근거로 쓴 응답 발췌

```
"Article 44: Prohibition on Driving While Intoxicated"

"4 The standard for the state of intoxication in which driving is prohibited under paragraph (1) is a driver's blood alcohol concentration of 0.03 percent or more."

"Article 148-2: Penalties"

"3 A person who drives a motor vehicle, etc. or a tram while under the influence of alcohol in violation of Article 44(1) shall be punished according to the following classification:
  1. A person whose blood alcohol concentration is 0.2 percent or higher: Imprisonment with labor for not less than 2 years but not more than 5 years, or a fine of not less than KRW 10 million but not more than KRW 20 million;
  2. A person whose blood alcohol concentration is 0.08 percent or higher but less than 0.2 percent: Imprisonment with labor for not less than 1 year but not more than 2 years, or a fine of not less than KRW 5 million but not more than KRW 10 million;
  3. A person whose blood alcohol concentration is 0.03 percent or higher but less than 0.08 percent: Imprisonment with labor for not more than 1 year, or a fine not exceeding KRW 5 million."

"1 A person who violates Article 44(1), (2), or (5) (limited to cases of driving a motor vehicle, etc. or a tram, but excluding cases of driving a personal mobility device; hereinafter the same shall apply in this Article), is sentenced to a fine or heavier punishment, and again violates Article 44(1), (2), or (5) within 10 years from the date on which the sentence became final (including a person whose sentence has lapsed) shall be punished according to the following classification:
  2. A person who violates Article 44(1) and whose blood alcohol concentration is 0.2 percent or higher shall be punished by imprisonment with labor for not less than 2 years but not more than 6 years, or by a fine of not less than KRW 10 million but not more than KRW 30 million;
  3. A person who violates Article 44(1) and whose blood alcohol concentration is 0.03 percent or higher but less than 0.2 percent shall be punished by imprisonment with labor for not less than 1 year but not more than 5 years, or by a fine of not less than KRW 5 million but not more than KRW 20 million."
```

**법률 출처:**
- 도로교통법 제44조 (Road Traffic Act, Art. 44) - 음주 운전 금지 기준
- 도로교통법 제148-2조 (Road Traffic Act, Art. 148-2) - 처벌 규정
- https://koreanics.com/laws/road-traffic-act/article-148-2/

---

# 3회차

## 질문 1: 국가계약법상 수의계약을 할 수 있는 경우가 뭐야? 근거 조문도 알려줘.

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"discretionary contract or negotiated contract Government Procurement Act"}` | 국가계약법 관련 규정 검색, rc=0 |
| 2 | get_law_article | `{"law":"enforcement-decree-of-the-act-on-contracts-to-which-the-state-is-a-party","article":"26"}` | 시행령 제26조 전문 조회, rc=0 |

### 답변

국가계약법(국가를 당사자로 하는 계약에 관한 법)의 시행령 제26조에서 수의계약을 할 수 있는 경우를 규정하고 있습니다. 크게 5가지 경우가 있습니다:

**1. 경쟁이 불가능하거나 어려운 경우**
- 자연재해, 전염병 확산 방지, 긴급 재해, 원자재 가격 급등 등 긴급한 상황
- 국가 안보, 국방, 외교 관련 사항으로 보안이 필요한 경우
- 국방 특수물자 제조 또는 구매
- 긴급재난 발생 시 국가 보유 복구 자재 판매

**2. 경쟁이 성립되지 않는 경우**
- 특정 기술이나 유일한 생산자의 물품이 필요한 경우
- 이전 계약자와의 계속 계약 (시공 책임, 혼선 방지, 완공 등)
- 특허 기술, 신기술 적용 공사
- 부품 교체나 기존 장비 확장으로 호환성 문제가 있는 경우
- 부동산 매입, 임차 등 특정인과의 거래

**3. 중소기업 제품의 경우**
- 성능 인증, 품질 인증, 우수 조달 물품으로 지정된 중소기업 제품

**4. 취약계층 지원 목적**
- 국가 유공자, 장애인 등을 위한 복지시설·기관과의 계약

**5. 효율성이 인정되는 기타 경우**
- 4억원 이하 일반 건설공사, 2억원 이하 전문 건설, 1.6억원 이하 기타 공사
- 2천만원 이하의 물품 제조·구매·임차 및 용역 계약
- 중소기업·여성기업·장애인기업과의 특정 금액 이상 계약
- 해외 외교 관련 물품의 현지 구매
- 소액 계약 등

### 근거로 쓴 응답 발췌

```
Enforcement Decree of the Act on Contracts to Which the State Is a Party, Article 26
"Cases Where Negotiated Contracts May Be Used"

1 The cases in which a negotiated contract may be concluded pursuant to the proviso to Article 7(1) of the Act are as follows:
  1. Cases where there is no time to put the contract out to competition, or where it is determined that putting the contract out to competition would make it difficult to achieve the purpose of the contract, falling under any of the following items:
    가. Natural disasters, prevention and containment of the spread of infectious diseases, operational troop movements, urgent events, emergency disasters such as flood damage requiring urgent restoration, sudden surges in raw material prices, urgent safety inspections and facility improvements for accident prevention, and other cases equivalent thereto;
    나. Cases involving national security, national defense plans and intelligence activities, management of military facilities, diplomatic relations, or other equivalent matters, where there is a need for security or where the acts of State agencies need to be carried out in secret;
  2. Cases where competition cannot be established, such as where a specific person's technology is required or where there is only one producer of the relevant goods, falling under any of the following items:
    가. Cases where, in connection with construction work, it is difficult to allocate responsibility for future defects in the facilities, and a contract is made with the immediately preceding or current contractor;
    라. Cases of construction work carried out in special areas such as areas adjacent to the front line, where competition is practically impossible;
  5. Cases, other than those under subparagraphs 1 through 4, where it is determined, in light of the purpose, nature, etc. of the contract, that concluding the contract through competition would be inefficient, falling under any of the following items:
```

---

## 질문 2: 도로교통법에서 음주운전 처벌 기준이 지금 어떻게 돼 있어?

### 호출한 도구

| 순서 | 도구 | 인자 | 결과 |
|---|---|---|---|
| 1 | search_law_articles | `{"query":"drunk driving impaired driving Road Traffic Act punishment penalty"}` | 도로교통법 음주운전 관련 규정 검색, rc=0 |
| 2 | get_law_article | `{"law":"road-traffic-act","article":"44"}` | 도로교통법 제44조 (음주운전 금지 및 기준), rc=0 |
| 3 | get_law_article | `{"law":"act-on-special-cases-concerning-the-settlement-of-traffic-accidents","article":"3"}` | 교통사고처리특례법 제3조 (음주운전 처벌), rc=0 |

### 답변

도로교통법에서 규정하는 음주운전 처벌 기준은 다음과 같습니다:

**1. 음주운전의 정의 및 기준 (도로교통법 제44조)**
- 혈중알콜농도 0.03% 이상인 상태에서 운전하는 것이 음주운전으로 정의됩니다
- 경찰은 필요하다고 판단되거나 음주운전 혐의가 있을 때 호흡 검사로 측정할 수 있고, 운전자는 이에 응해야 합니다
- 운전자가 결과에 이의를 제기하면 혈액 검사로 재검사할 수 있습니다

**2. 교통사고 발생 시 처벌 기준 (교통사고처리특례법 제3조)**
음주운전으로 인해 교통사고가 발생한 경우:
- **징역**: 최대 5년(노동 없는 징역 금지)
- **벌금**: 2천만원 이하

다만, 음주운전 상태에서 신호 무시, 중앙선 침범, 제한 속도 20km/h 초과, 횡단보도 보행자 보호 의무 위반 등의 추가 위반이 있는 경우나 음주 측정 거부/방해 행위가 있는 경우에는 피해자 합의 여부와 관계없이 처벌받습니다.

**3. 측정 거부 및 방해 행위 (도로교통법 제44조)**
- 운전자는 경찰의 음주 측정 요구에 응해야 하고, 응하지 않으면 법적 제재를 받습니다
- 운전 후 추가 음주를 하거나 혈중알콜농도에 영향을 미치는 의약품 복용하는 행위는 위법입니다

### 근거로 쓴 응답 발췌

```
Road Traffic Act, Article 44 "Prohibition on Driving While Intoxicated"

4 The standard for the state of intoxication in which driving is prohibited under paragraph (1) is a driver's blood alcohol concentration of 0.03 percent or more.
5 A person for whom there are reasonable grounds to believe that he or she is intoxicated shall not, after driving a motor vehicle, etc. or a tram, or riding a bicycle, consume additional alcohol, or use an item prescribed by Ordinance of the Ministry of the Interior and Safety, such as a medicine that may affect blood alcohol concentration, for the purpose of making a measurement under paragraph (2) or (3) difficult.

---

Act on Special Cases concerning the Settlement of Traffic Accidents, Article 3 "Special Cases for Punishment"

1 A driver of a vehicle who commits the crime under Article 268 of the Criminal Act by reason of a traffic accident shall be punished by imprisonment without prison labor for not more than 5 years or by a fine not exceeding KRW 20 million.

2 A public prosecution may not be instituted, against the express will of the victim, against a driver who, through the traffic of a vehicle, commits the crime of bodily injury by occupational negligence or the crime of bodily injury by gross negligence among the crimes under paragraph (1)... provided, that this shall not apply where... the driver fails to comply with a demand for an alcohol test in violation of Article 44(2) of the Road Traffic Act... or commits an act interfering with an alcohol test in violation of Article 44(5) of the Road Traffic Act; and where the same crime is committed through an act falling under any of the following subparagraphs:
  8. Where the driver drove while intoxicated in violation of Article 44(1) of the Road Traffic Act
```
