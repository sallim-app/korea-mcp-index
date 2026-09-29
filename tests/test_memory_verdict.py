#!/usr/bin/env python3
"""기억 판정 회귀 — 채점 모델의 기억을 잣대로 남의 서버 수치를 틀렸다고 게시하지 않는다 (2026-09-28).

2026-09-28에 드러난 사고: `grades/금융·증시.json`이 삼성전자 2026년 1분기 영업이익 57.2조를
「역사적 밴드 5~25% 초과」「역대 최고 분기 영업이익(약 17.6조)의 3배」라며 **스케일 결함**으로
판정해 `com.aikstockdata/mcp`·`MosslandOpenDevs/alpha` 두 곳에 정확성 0점을 줬다. 잣대는 도구
출력도 공시도 아니라 **채점 모델이 학습 때 본 과거**였다. DART 연결 영업(잠정)실적 정정공시
(rcpNo 20260730800103)와 도구 재호출로 대조하니 두 서버 값은 모두 맞았고, '양립 불가'라던
두 값은 분기 단독과 1~6월 누계의 차이였다.

**기억은 학습 시점에서 멈춘다.** '역대 최고'는 그 뒤에 깨질 수 있고, 깨졌을 때 기억으로 채점하면
**현실을 먼저 따라잡은 서버가 틀린 서버로 게시된다.** 문장은 그럴듯해 읽어서는 안 걸린다.

그래서 배관으로 건다: 채점 문장이 '역사적·역대 최고·사상 최대' 같은 **과거 기준값**을 꺼내면,
**같은 문장에** 그 기준을 이번에 확인한 출처(공시 번호·URL)가 있거나, 기준값 앞에 정정 표식
`[YYYY-MM-DD 정정] 종전`이 붙고 기준값이 **같은 절의 따옴표 안에서** 옛 판정을 인용하는 자리여야
한다(표식이 뒤 절의 새 판정까지 면제하지 않게, 2026-09-29). 둘 다 없으면 기억 판정으로 보고 실패한다.

실행: python3 -m pytest tests/test_memory_verdict.py -q
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRADES = ROOT / "grades"

# 과거 기준값을 잣대로 꺼내는 말투 — 이 말이 나오면 그 문장은 '세상이 어땠는가'를 주장한다.
MEMORY_BENCHMARK = re.compile(r"역사적|역대\s*(최고|최대|최저)|사상\s*(최고|최대|최저)")

# 이번에 확인한 출처 — 같은 문장 안에 있어야 한다. '재호출'·'다시 불러' 같은 낱말은 넣지 않는다:
# "다시 불러 대조하지 않은"처럼 부정문에도 나온다. 대조했다면 가리킬 번호나 주소가 있다.
SOURCED = re.compile(r"rcpNo\s*\d{14}|https?://\S+\.\S+")

# 옛 판정을 인용해 거둬들이는 자리 — **형식 표식**으로만 인정한다: 같은 문장에서 기준값 앞에
# `[YYYY-MM-DD 정정] 종전`. 낱말로 뜻을 읽으려던 시도('정정'·'오판'·부정어 꼬리 가르기)는 codex
# 교차검증(2026-09-28)에서 다섯 차례 연달아 뚫렸다 — "정정할 필요가 없다", "오판은 결코 아니었다",
# "오판, 즉 잘못이 아니었다"… 한국어 부정은 정규식으로 닫히지 않는다. 표식은 정정을 쓰는 사람만
# 일부러 붙이는 형식이라 채점 문장이 우연히 품지 않고, 붙였으면 그 문장이 정정이라고 스스로
# 서명한 것이다(뜻이 맞는지는 사람·codex 검수 몫).
RETRACTION_MARK = re.compile(r"\[\d{4}-\d{2}-\d{2}\s*정정\]\s*종전")


# 문장 경계. 소수점(17.6조)·URL의 점은 뒤에 공백이 없어 쪼개지지 않는다.
SENTENCE = re.compile(r"(?<=[.!?])\s+")

# 절 경계 — 정정 표식은 **자기 절 안에서만** 효력이 있다. `;`·역접 접속어 뒤는 새 판정이다:
# "[정정] 종전 …; 그러나 역대 최고치는 17.6조" 에서 뒤 절은 옛 판정의 인용이 아니라 새로 기억을
# 잣대로 쓴 것이다(codex 교차검증 2026-09-29). 쉼표·줄표는 경계로 삼지 않는다 — 실제 정정문이
# 인용을 줄표로 풀어 쓴다(grades/금융·증시.json 사실오류[0]). 그 자리는 아래 인용 조건이 막는다.
CLAUSE = re.compile(r"\s*[;；]\s*|,?\s*(?=(?:그러나|하지만|그런데|반면|다만|그렇지만)(?:\s|,|$))")

# 따옴표 인용 — 정정 표식이 풀어 주는 것은 **따옴표로 옛 문장을 인용한 기준값**뿐이다. 표식 뒤라도
# 따옴표 밖의 기준값은 지금 쓰는 판정이다: "[정정] 종전 '…'는 오판이었다 — 역대 최고치는 17.6조다".
QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"|‘[^’]*’|“[^”]*”|「[^」]*」|『[^』]*』")


def _texts():
    """grades/ 안의 채점 문장 전부 — (파일:위치, 문장)."""
    for path in sorted(GRADES.glob("*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        for key in ("분야_총평", "순위_근거"):
            if isinstance(d.get(key), str):
                yield f"{path.name}:{key}", d[key]
        for s in d.get("servers", []):
            name = s.get("server")
            if isinstance(s.get("총평"), str):
                yield f"{path.name}:{name}:총평", s["총평"]
            for q in s.get("questions", []):
                for k, v in q.items():
                    if k.endswith("_why") and isinstance(v, str):
                        yield f"{path.name}:{name}:q{q.get('q')}:{k}", v
                for i, e in enumerate(q.get("사실오류") or []):
                    yield f"{path.name}:{name}:q{q.get('q')}:사실오류[{i}]", e


def _ranking_texts():
    """사이트가 실제로 렌더하는 ranking.json의 문장들 — grades/를 고치고 재산출을 빠뜨리거나
    ranking.json을 직접 고친 경우에도 게시 경로 쪽에서 걸리게 한다(codex 교차검증 2026-09-28)."""
    d = json.loads((ROOT / "ranking.json").read_text(encoding="utf-8"))
    for key, item in (d.get("items") or {}).items():
        for f in ("note", "순위_근거"):
            if isinstance(item.get(f), str):
                yield f"ranking.json:{key}:{f}", item[f]
        for t in item.get("top") or []:
            if isinstance(t.get("why"), str):
                yield f"ranking.json:{key}:{t.get('name')}:why", t["why"]


def _unsourced(text: str) -> list[str]:
    """과거 기준값을 출처 없이 잣대로 쓴 문장들.

    한계: 같은 문장에 무관한 URL이 있으면 통과한다 — 이 회귀는 의미를 읽지 않고, 출처를
    적을 자리를 강제할 뿐이다. 의미 검수는 채점 프롬프트 ④(강한 모델의 주장 판정) 몫이다.

    출처는 문장 단위로 인정한다. 정정 표식은 **같은 절에서 표식 뒤, 따옴표 안의 기준값만**
    풀어 준다 — 표식 하나로 같은 문장 뒤의 새 기억 판정까지 면제되지 않게(codex 2026-09-29).
    """
    bad = []
    for sent in SENTENCE.split(text):
        if SOURCED.search(sent):
            continue
        for clause in CLAUSE.split(sent):
            mark = RETRACTION_MARK.search(clause)
            quotes = [q.span() for q in QUOTED.finditer(clause)]
            if any(not (mark and mark.end() <= m.start()
                        and any(lo < m.start() and m.end() < hi for lo, hi in quotes))
                   for m in MEMORY_BENCHMARK.finditer(clause)):
                bad.append(sent)
                break
    return bad


def test_detector_catches_the_known_case():
    """게이트가 살아 있나 — 실사고 원문(2026-09 게시본)을 그대로 넣으면 걸려야 한다."""
    original = ("1분기 매출 133.9조·영업이익 57.2조는 영업이익률 42.7%(역사적 밴드 5~25% 초과)이자 "
                "역대 최고 분기 영업이익(약 17.6조)의 3배이고")
    assert _unsourced(original), "실사고 원문을 못 잡는다 — 게이트가 죽었다"
    assert not _unsourced("[2026-09-28 정정] 종전 문장은 '역대 최고 분기 영업이익(약 17.6조)'을 잣대로 삼은 오판이었다")
    # 표식 없는 '정정'·'종전'·'오판' 낱말은 거둬들임이 아니다
    assert _unsourced("정정할 필요가 없다 — 역대 최고 분기 영업이익(약 17.6조)의 3배다")
    assert _unsourced("종전 역대 최고치는 17.6조이므로 57.2조는 오류다")
    assert _unsourced("종전 역대 최고치 판단은 오판, 즉 잘못이 아니었다")
    # 표식은 같은 문장, 기준값 앞에만 — 딴 문장의 표식은 이 문장을 풀어 주지 않는다
    assert _unsourced("[2026-09-28 정정] 종전 판정을 유지한다. 역대 최고 분기 영업이익(약 17.6조)의 3배다")
    # 표식은 자기 절, 따옴표 안의 기준값만 푼다 — 같은 문장 뒤 새 판정은 면제되지 않는다(codex 2026-09-29)
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고 분기'는 오판이었다; 그러나 역대 최고치는 17.6조다")
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고 분기'는 오판이었다; '역대 최고치'는 17.6조다")
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고 분기'는 오판이었다 그러나 '역대 최고치'는 17.6조다")
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고'는 오판이었다,그러나 '역대 최고'는 맞다")
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고 분기'는 오판이었다 — 역대 최고치는 17.6조다")
    assert _unsourced("[2026-09-28 정정] 종전 '역대 최고 분기'는 오판이었다, 역대 최고치는 17.6조다")
    assert _unsourced("[2026-09-28 정정] 종전 판정은 오판이었다, 역대 최고치는 17.6조다")
    assert _unsourced("'역대 최고치' [2026-09-28 정정] 종전 판정은 오판이었다")
    # 실제 정정문 형태 — 여러 기준값을 따옴표로 인용하고 줄표로 풀어 쓴다
    assert not _unsourced("[2026-09-28 정정] 종전 문장은 '역사적 밴드 5~25%'·'역대 최고 분기 영업이익(약 17.6조)'"
                          "을 잣대로 삼았다 — 도구를 다시 불러 대조하지 않은 판정")
    # 출처는 번호·주소가 붙어야 출처다
    assert _unsourced("도구를 다시 불러 대조하지 않았지만 역대 최고치(약 17.6조)의 3배라 오류다")
    assert _unsourced("rcpNo 확인 필요: 역대 최고치의 3배")
    assert not _unsourced("DART rcpNo 20260730800103 기준 역대 최고 분기 실적이다")


def test_grades_scanned():
    assert sum(1 for _ in _texts()) > 20, "grades/에서 채점 문장을 거의 못 읽었다 — 파서 드리프트"


def test_no_memory_benchmark_without_source():
    """과거 기준값을 출처 없이 잣대로 쓴 채점 문장이 있으면 실패."""
    bad = [(where, near[:160]) for where, text in [*_texts(), *_ranking_texts()] for near in _unsourced(text)]
    assert not bad, (
        "채점 모델의 기억(과거 기준값)으로 남의 서버 수치를 판정한 문장이 있다 — 도구를 다시 불러 "
        f"대조하고 출처를 같은 자리에 적어라(mcp-index-grade-prompt.md): {bad[:3]}")
