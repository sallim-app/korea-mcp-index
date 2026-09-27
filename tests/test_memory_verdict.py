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
**같은 문장에** 그 기준을 이번에 확인한 출처(공시 번호·URL)가 있거나, 기준값 앞에 '종전'이 와서
옛 판정을 인용하고 그 판정을 틀렸다고 끝맺는 자리여야 한다. 둘 다 없으면 기억 판정으로 보고 실패한다.

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

# 옛 판정을 인용해 거둬들이는 자리 — 같은 문장에서 기준값 **앞에** '종전'이 오고, 그 문장이
# 그 판정을 **틀렸다고 끝맺어야** 한다(codex 교차검증 2026-09-28, 두 차례): '정정' 낱말만으로는
# "정정할 필요가 없다"가 통과하고, '종전'만으로는 "종전 역대 최고치는 17.6조이므로 오류다"처럼
# 옛 오판을 그대로 되풀이한 문장이 통과한다.
RETRACTED_BEFORE = re.compile(r"종전")

# 거둬들임을 말하는 낱말. 부정형은 낱말 뒤 꼬리로 따로 가른다 — lookahead로 낱낱이 막으면
# '오판은 결코 아니었다'·'오판이라고 볼 수 없다'처럼 부사·인용형이 낄 때마다 새로 뚫린다(codex 2026-09-28).
RETRACTION_VERDICT = re.compile(r"오판|틀렸|반박(돼|됐)|거둔다|거뒀")
# 거둬들임 낱말 뒤, 같은 문장 안에 이것이 있으면 부정된 것으로 본다.
NEGATED_AFTER = re.compile(r"아니|없|않|못")


def _retracted(sent: str) -> bool:
    """문장이 옛 판정을 틀렸다고 끝맺는가 — 거둬들임 낱말이 있고 그 뒤가 부정되지 않았다."""
    return any(not NEGATED_AFTER.search(sent[m.end():]) for m in RETRACTION_VERDICT.finditer(sent))


# 문장 경계. 소수점(17.6조)·URL의 점은 뒤에 공백이 없어 쪼개지지 않는다.
SENTENCE = re.compile(r"(?<=[.!?])\s+")


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
    """
    bad = []
    for sent in SENTENCE.split(text):
        for m in MEMORY_BENCHMARK.finditer(sent):
            if SOURCED.search(sent) or (RETRACTED_BEFORE.search(sent[:m.start()]) and _retracted(sent)):
                continue
            bad.append(sent)
            break
    return bad


def test_detector_catches_the_known_case():
    """게이트가 살아 있나 — 실사고 원문(2026-09 게시본)을 그대로 넣으면 걸려야 한다."""
    original = ("1분기 매출 133.9조·영업이익 57.2조는 영업이익률 42.7%(역사적 밴드 5~25% 초과)이자 "
                "역대 최고 분기 영업이익(약 17.6조)의 3배이고")
    assert _unsourced(original), "실사고 원문을 못 잡는다 — 게이트가 죽었다"
    assert not _unsourced("종전 문장은 '역대 최고 분기 영업이익(약 17.6조)'을 잣대로 삼은 오판이었다")
    # 판정을 유지하면서 '정정'이란 낱말만 품은 문장은 통과시키지 않는다
    assert _unsourced("정정할 필요가 없다 — 역대 최고 분기 영업이익(약 17.6조)의 3배다")
    # 거둬들임은 같은 문장 안에서만 — 딴 문장의 '종전'은 이 문장을 풀어 주지 않는다
    assert _unsourced("종전 판정을 유지한다. 역대 최고 분기 영업이익(약 17.6조)의 3배다")
    # '종전'이 앞에 있어도 옛 오판을 되풀이하면 통과시키지 않는다
    assert _unsourced("종전 역대 최고치는 17.6조이므로 57.2조는 오류다")
    # 부정문 속 '다시 불러'는 출처가 아니다
    assert _unsourced("도구를 다시 불러 대조하지 않았지만 역대 최고치(약 17.6조)의 3배라 오류다")
    # 번호 없는 'rcpNo' 낱말은 출처가 아니다
    assert _unsourced("rcpNo 확인 필요: 역대 최고치의 3배")
    assert not _unsourced("DART rcpNo 20260730800103 기준 역대 최고 분기 실적이다")
    # 부정된 거둬들임은 거둬들임이 아니다
    assert _unsourced("종전 역대 최고치 판단은 오판이 아니었다")
    assert _unsourced("종전 역대 최고치 판단은 오판은 아니었다")
    assert _unsourced("종전 역대 최고치 판단은 오판은 결코 아니었다")
    assert _unsourced("종전 역대 최고치 판단을 오판이라고 볼 수 없다")
    assert _unsourced("종전 역대 최고치 판단이 틀렸다고 하기 어렵지 않다")


def test_grades_scanned():
    assert sum(1 for _ in _texts()) > 20, "grades/에서 채점 문장을 거의 못 읽었다 — 파서 드리프트"


def test_no_memory_benchmark_without_source():
    """과거 기준값을 출처 없이 잣대로 쓴 채점 문장이 있으면 실패."""
    bad = [(where, near[:160]) for where, text in [*_texts(), *_ranking_texts()] for near in _unsourced(text)]
    assert not bad, (
        "채점 모델의 기억(과거 기준값)으로 남의 서버 수치를 판정한 문장이 있다 — 도구를 다시 불러 "
        f"대조하고 출처를 같은 자리에 적어라(mcp-index-grade-prompt.md): {bad[:3]}")
