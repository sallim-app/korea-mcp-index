#!/usr/bin/env python3
"""축③ — 도구 표면에 조인·계산·판정이 있는가 (2026-08-19 착수, D-2026W34-21).

D-2026W34-21이 정한 선정 기준은 "데이터를 주는가"가 아니라 **"원천도 웹검색도 못 주는
정형 조인·계산·판정을 주는가"**다(단순 API 래퍼는 스킬처럼 프론티어에 흡수된다).
그런데 filter_candidates.py는 이름·설명 문자열만 봤고 **도구 목록을 한 번도 안 봤다** —
그 파일의 boundaries에 "다음 단계=실호출"로 적혀 있던 그 빈칸이 이 모듈이다.

## 우리가 재는 것과 못 재는 것을 먼저 가른다 (기치 ②)

선언된 축은 "**원천이** 직접 안 주는가"다. 그것을 판정하려면 그 서버가 무엇을 감싸는지,
그 원천 API가 어떤 엔드포인트를 주는지 알아야 한다. **우리는 전 분야에서 그것을 모른다** —
부동산·공공계약의 원천은 알지만 의료·교통·학사는 모른다. 모르면서 "이건 래퍼다"라고
쓰면 남의 서버를 근거 없이 깎는 것이고(2026-08-20에 정확히 그 사고를 냈다 — 못 읽은
패키지명을 '설치 불가'로 게시), 우리가 경계하는 그럴듯한 요약을 우리가 생산하는 것이다.

그래서 이 모듈이 내놓는 판정값의 주어는 **원천이 아니라 도구 이름**이다:

    재는 것    도구 이름의 동사류와 인자 형태 — "이 서버의 도구 표면에 조인·계산·판정
               동사가 있는가". 검증 가능한 진술이다(도구 목록이 공개돼 있다).
    못 재는 것 그 계산을 원천이 이미 주는지 — 분야별 원천 대조가 필요하다. 안 했다고 공시한다.

따라서 **이 축은 후보를 떨어뜨리지 않는다.** 라벨과 근거만 붙이고, 나머지 판단은
블라인드 심사 레인(D-2026W34-25)으로 넘긴다. 이유 둘:
  ① 도구 목록이 있는 서버는 233건 중 25건뿐이다. 이 축으로 걸러내면 **우리가 도구를 못 본
     208건을 '가치 없음'으로 게시**하게 된다 — 못 봄 ≠ 없음.
  ② 이름은 관례일 뿐이다. `check_price_adjustment`(룰 계산)와 `check_email_valid`(단일 필드
     조회)는 같은 동사를 쓴다. 이름만으로 갈리지 않는 것은 `ambiguous`로 남긴다.

## 동사류

파생(derive) 후보로 세는 토큰은 **그 토큰 자체가 2건 이상의 레코드나 룰 적용을 뜻하는 것**만
넣는다. 원천이 그 이름으로 엔드포인트를 주는 일이 드문 것들이다. 반례를 알면서 빼둔 것:
`forecast`는 기상 원천이 직접 준다, `history`·`stats`도 대개 원천 엔드포인트다 — 넣으면
"파생을 준다"가 부풀려진다.
"""
import json
import pathlib
import re

# 조인·계산·판정 — 토큰 자체가 연산이다
DERIVE = ["compare", "vs", "diff", "match", "estimate", "calc", "simulate", "score",
          "evaluate", "valuation", "eligibility", "feasibility", "impact", "burden",
          "decide", "analyze", "analysis", "plan", "linked", "delegated", "tier",
          "reference", "references", "connection", "connections", "scan", "radar",
          "alert", "alerts", "basket", "explain", "tree", "flags"]
# 어미가 갈리는 것은 어간으로 본다(analyz-e/-is, estimat-e/-ion, calc-ulate…)
DERIVE_STEM = ["analyz", "estimat", "evaluat", "simulat", "valuat", "eligib", "feasib",
               "referenc", "delegat", "connect", "calc", "compar"]
# 동사는 파생인데 **원천이 그 이름으로 직접 주는 일이 흔한 것**과, 단일 필드 검증일 수도
# 있는 것. 이름만으로 안 갈린다 — `check_price_adjustment`(룰 계산)와 `check_email_valid`
# (단일 필드 조회)는 같은 동사다. `recommend`·`rank`도 여기다: 언론사의 '추천 기사'와
# 거래소의 '거래량 순위'는 원천이 그대로 주는 피드다(hankookilbo·aikstockdata 실측에서
# 이 둘이 파생으로 잡혀 오탐이 났다 — forecast·history·stats를 뺀 것과 같은 이유다).
AMBIGUOUS = ["check", "validate", "verify", "trend", "summary", "coverage", "status",
             "recommend", "suggest", "rank", "rankings"]
AMBIGUOUS_STEM = ["recommend", "rank"]
# 데이터를 주는 게 아니라 상태를 바꾸는 것 — 축②(데이터 제공형)의 반대 신호.
# **거래 표면의 명사도 여기 넣는다**(checkout·cart·booking): `get_checkout`은 상태를 바꾸지
# 않지만 그것이 주는 것은 사실이 아니라 내 장바구니다. 이 목록이 묻는 것은 "AI에게 사실을
# 주는가"이므로, 거래 표면은 읽어도 데이터가 아니다.
ACTION = ["create", "update", "cancel", "complete", "delete", "submit", "request",
          "subscribe", "unsubscribe", "rate", "post", "reply", "ack", "transfer",
          "start", "booking", "checkout", "cart", "execute"]
# 조회형 — 원천이 그대로 준다고 보는 쪽
RETRIEVE = ["get", "list", "search", "fetch", "read", "lookup", "find", "explore",
            "discover", "ping", "info"]

MEASURED = "도구 이름의 동사류·인자 형태만 봤다. 그 계산을 원천이 이미 주는지는 대조하지 않았다"


def _seg(name: str) -> list:
    """도구 이름을 **의미 조각**으로 쪼갠다. snake_case와 camelCase 둘 다 쓰인다.

    부분문자열로 찾으면 반드시 오탐이 난다 — 이 저장소는 이미 한 번 당했다(`dart`가
    **agent`data`-nl** 안에 있어 네덜란드 서버가 한국 후보로 잡혔다, filter_candidates.py).
    같은 사고가 도구 이름에서도 났다: `get_checkout`·`create_cart`가 `check`에 걸려
    결제 액션 서버가 '판정형'으로 분류됐다(2026-08-21 실측). 그래서 조각 단위로 맞춘다.
    """
    n = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return [x for x in re.split(r"[^A-Za-z0-9]+", n.lower()) if x]


def _has(segs: list, exact: list, stems: list = ()) -> bool:
    """조각과 **정확히 같거나**, 선언한 어간으로 시작하는 조각이 있는가."""
    if any(s in exact for s in segs):
        return True
    return any(s.startswith(st) for s in segs for st in stems)


# 설명(한국어·영어)에서 조인·계산을 말하는 표현. **이름으로 안 갈린 것만** 여기로 온다 —
# 산문에 토큰 매칭을 넓게 걸면 오탐이 늘기 때문에 적용 범위를 좁게 묶어 둔다.
DESC_DERIVE_KO = ["비교", "대조", "계산", "산출", "추정", "판정", "결합", "조인", "연계",
                  "교차", "합산", "집계한", "환산", "시뮬", "점수", "등급을", "적용해"]


def _cls_with_desc(t: dict) -> tuple:
    """이름으로 분류하고, **애매한 것만** 설명으로 한 번 더 본다.

    왜 애매한 것만인가: 이름은 관례라 `check_price_adjustment`(룰 계산)와
    `check_email_valid`(단일 필드 조회)를 못 가른다 — 그 둘을 가르는 문장은 설명에 있다.
    반대로 설명 산문 전체에 토큰을 넓게 걸면 조회형 도구도 "…를 비교할 때 쓰세요" 같은
    문구로 파생이 된다. 그래서 **이름이 못 가른 자리에만** 설명을 쓴다.

    반환: (분류, 근거). 근거가 설명이면 그 문구를 남긴다 — 판정은 근거를 대야 한다.
    """
    c = _cls(t.get("name") or "")
    if c != "ambiguous":
        return c, None
    d = (t.get("desc") or "")
    if not d:
        return c, None
    seg = _seg(d)
    hit = ([w for w in DESC_DERIVE_KO if w in d]
           + [w for w in DERIVE if w in seg]
           + [w for w in seg if any(w.startswith(st) for st in DERIVE_STEM)])
    if hit:
        return "derive", f"설명: {hit[0]}"
    return c, None


def _cls(name: str) -> str:
    """한 도구를 분류한다. **파생 → 애매 → 상태변경 → 조회** 순으로 본다.

    순서가 판정을 바꾼다: `check_combination_feasibility`는 `check`(애매)와
    `feasibility`(파생)를 동시에 가지는데 파생을 먼저 보므로 파생으로 간다. 애매를 먼저
    보면 근거가 있는 판정이 근거 없는 판정에 덮인다.
    """
    segs = _seg(name)
    if _has(segs, DERIVE, DERIVE_STEM):
        return "derive"
    if _has(segs, AMBIGUOUS, AMBIGUOUS_STEM):
        return "ambiguous"
    if _has(segs, ACTION):
        return "action"
    if _has(segs, RETRIEVE):
        return "retrieve"
    return "unclassified"


def axis3(tools: list | None) -> dict:
    """서버 한 대의 축③ 라벨. `tools`가 None이면 **모른다**고 답한다(0이 아니다)."""
    if tools is None:
        return {"signal": "unknown", "why": "도구 목록을 못 봤다 — 조인·계산이 없다는 뜻이 아니다",
                "measured": MEASURED}
    names = [t.get("name") or "" for t in tools if isinstance(t, dict)]
    if not names:
        return {"signal": "unknown", "why": "도구 목록이 비었거나 규격 이탈이다", "measured": MEASURED}
    b: dict[str, list] = {"derive": [], "ambiguous": [], "action": [], "retrieve": [],
                          "unclassified": []}
    by_desc = []
    for t in tools:
        if not isinstance(t, dict):
            continue
        c, why = _cls_with_desc(t)
        b[c].append(t.get("name") or "")
        if why:
            by_desc.append(f"{t.get('name')}({why})")
    # **설명이 있었는지를 값으로 공시한다.** 2026-08-19~08-21 수집분에는 설명이 없어
    # 이름만으로 판정했다 — 그 사실이 판정값에 안 붙으면 다음 회차와 비교가 안 된다.
    have_desc = sum(1 for t in tools if isinstance(t, dict) and (t.get("desc") or "").strip())
    basis = "이름+설명" if have_desc else "이름만(설명 미수집 회차)"
    if b["derive"]:
        sig, why = "derived", f"조인·계산·판정 동사 {len(b['derive'])}종: {', '.join(b['derive'][:4])}"
    elif b["ambiguous"]:
        sig, why = "ambiguous", (f"판정형 동사는 있으나 단일 필드 검증일 수 있다: "
                                 f"{', '.join(b['ambiguous'][:4])} — 사람·심사가 봐야 한다")
    elif len(b["action"]) * 2 >= len(names):
        # **과반을 요구한다.** 3종 중 1종이 상태 변경형인 서버를 '상태 변경 위주'라 부르면
        # 그것도 근거 없이 깎는 것이다(app.apick/finance 1/3이 그렇게 잡혔다).
        sig, why = "action_heavy", f"도구 과반이 상태 변경형({len(b['action'])}/{len(names)}종)"
    else:
        # **"전부 조회형"이라고 쓰지 않는다.** app.apick/finance는 3종 중 1종이 상태 변경형이고
        # 2종은 우리 동사류에 안 걸린다(account_realname·bank_code) — 그걸 '전부 조회형'이라
        # 부르면 우리 판정값이 우리 원자료와 어긋난다. 세어서 그대로 쓴다.
        sig = "retrieval_only"
        why = (f"파생 신호 0 — 조회형 {len(b['retrieve'])}·상태변경 {len(b['action'])}·"
               f"미분류 {len(b['unclassified'])}/{len(names)}종")
    return {"signal": sig, "why": why, "tool_count": len(names),
            "counts": {k: len(v) for k, v in b.items() if v},
            "derive_tools": b["derive"][:12], "ambiguous_tools": b["ambiguous"][:8],
            "basis": basis, "desc_coverage": f"{have_desc}/{len(names)}",
            **({"resolved_by_desc": by_desc[:8]} if by_desc else {}),
            "measured": MEASURED}


def load_specs(path: str = "schemas/tools.json") -> dict:
    """서버명 → tool specs. 파일이 없으면 **빈 dict**가 아니라 그 사실을 부른 쪽이 알아야 한다."""
    p = pathlib.Path(path)
    if not p.exists():
        return {}
    return json.load(open(p, encoding="utf-8")).get("items") or {}


def main() -> int:
    specs = load_specs()
    if not specs:
        print("schemas/tools.json이 없다 — measure.py를 먼저 돌려라(축③은 도구 목록이 원자료다)")
        return 2
    rows = [(n, axis3(t)) for n, t in specs.items()]
    order = {"derived": 0, "ambiguous": 1, "action_heavy": 2, "retrieval_only": 3, "unknown": 4}
    print(f"도구 목록을 본 서버 {len(rows)}대 — 축③ 라벨")
    print(f"재는 것: {MEASURED}\n")
    for n, a in sorted(rows, key=lambda r: (order[r[1]["signal"]], -r[1].get("tool_count", 0))):
        print(f"  {a['signal']:<14} {n[:42]:<42} {a['why'][:64]}")
    dist: dict[str, int] = {}
    for _, a in rows:
        dist[a["signal"]] = dist.get(a["signal"], 0) + 1
    print("\n분포: " + " · ".join(f"{k} {v}" for k, v in sorted(dist.items(), key=lambda x: order[x[0]])))
    print("**이 축은 후보를 떨어뜨리지 않는다** — 라벨이고, 남은 판단은 블라인드 심사 몫이다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
