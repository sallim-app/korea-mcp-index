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
그 자리 주변에 그 기준을 **이번에 확인한 출처**(재호출·공시 번호·URL)가 있거나, 그 말이 옛
판정을 인용해 정정하는 자리여야 한다. 둘 다 없으면 기억 판정으로 보고 실패한다.

실행: python3 -m pytest tests/test_memory_verdict.py -q
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRADES = ROOT / "grades"

# 과거 기준값을 잣대로 꺼내는 말투 — 이 말이 나오면 그 문장은 '세상이 어땠는가'를 주장한다.
MEMORY_BENCHMARK = re.compile(r"역사적|역대\s*(최고|최대|최저)|사상\s*(최고|최대|최저)")

# 이번에 확인한 출처, 또는 옛 판정을 인용해 거둬들이는 자리.
SOURCED_OR_RETRACTED = re.compile(
    r"재호출|다시\s*불러|rcpNo|https?://|공시\s*번호"
    r"|정정|종전|반박|오판"
)

WINDOW = 120


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


def _unsourced(text: str) -> list[str]:
    bad = []
    for m in MEMORY_BENCHMARK.finditer(text):
        near = text[max(0, m.start() - WINDOW):m.end() + WINDOW]
        if not SOURCED_OR_RETRACTED.search(near):
            bad.append(near)
    return bad


def test_detector_catches_the_known_case():
    """게이트가 살아 있나 — 실사고 원문(2026-09 게시본)을 그대로 넣으면 걸려야 한다."""
    original = ("1분기 매출 133.9조·영업이익 57.2조는 영업이익률 42.7%(역사적 밴드 5~25% 초과)이자 "
                "역대 최고 분기 영업이익(약 17.6조)의 3배이고")
    assert _unsourced(original), "실사고 원문을 못 잡는다 — 게이트가 죽었다"
    assert not _unsourced("종전 문장은 '역대 최고 분기 영업이익(약 17.6조)'을 잣대로 삼은 오판이었다")


def test_grades_scanned():
    assert sum(1 for _ in _texts()) > 20, "grades/에서 채점 문장을 거의 못 읽었다 — 파서 드리프트"


def test_no_memory_benchmark_without_source():
    """과거 기준값을 출처 없이 잣대로 쓴 채점 문장이 있으면 실패."""
    bad = [(where, near[:160]) for where, text in _texts() for near in _unsourced(text)]
    assert not bad, (
        "채점 모델의 기억(과거 기준값)으로 남의 서버 수치를 판정한 문장이 있다 — 도구를 다시 불러 "
        f"대조하고 출처를 같은 자리에 적어라(mcp-index-grade-prompt.md): {bad[:3]}")
