"""공개 산출물의 모델 표기는 **별칭**이어야 한다 — 세대 고정은 조용히 거짓이 된다 (2026-09-02).

계기: `judge_ranking.py:136`이 `ranking.json`에 `"model": "claude-haiku-4-5"`를 박고
있었는데, 실제 호출은 별칭(`mcp-index-grade-prompt.md`의 `model: haiku`)이다. 같은
`ranking.json`을 쓰는 writer가 둘인데 `rebuild_ranking.py:74`는 별칭형이라 표기가
갈렸다. `classification.json`도 세대 id로 게시돼 있었다 — 이 파일은 **코드 writer가
없고 세션이 손으로 쓰는** 파생 산출물이라, 코드 게이트만으로는 못 막는다.

왜 조용한가: 세대가 바뀌어도 아무것도 실패하지 않는다. 그냥 공개 저장소의 방법론
표기가 사실과 달라질 뿐이고, 그걸 알려주는 것은 아무 데도 없다. 이 저장소는 남의
MCP 서버를 채점해 공개하는 곳이라 "무엇으로 쟀는가"가 우리 근거의 절반이다.

계약:
  ① `ranking.json`을 쓰는 파이썬 writer의 실행 라인에 세대 박힌 모델 id가 없어야 한다.
  ② git 추적되는(=공개되는) 산출물 JSON의 `model` 필드가 별칭형이어야 한다.
주석은 예외다 — 과거 회차 기록 인용은 사실이므로 지우면 안 된다.

실행: pytest tests/test_model_alias_not_pinned.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# 세대·날짜가 박힌 id: claude-haiku-4-5, claude-opus-4-8, claude-sonnet-4-5-20250929 …
PINNED = re.compile(r"claude-(opus|sonnet|haiku|fable|mythos)-[0-9][0-9a-z.\-]*")

# ranking.json 을 쓰는 파이썬 writer 전부
WRITERS = ["judge_ranking.py", "rebuild_ranking.py"]

# git 추적되는(=공개되는) 산출물 JSON 중 model 필드를 갖는 것
ARTIFACTS = ["ranking.json", "classification.json"]


def _code_lines(text: str):
    """주석 줄(#로 시작)을 뺀 실행 라인만 돌려준다."""
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        yield i, line


@pytest.mark.parametrize("fname", WRITERS)
def test_writer_has_no_pinned_id(fname: str) -> None:
    path = ROOT / fname
    assert path.exists(), f"{fname} 없음 — writer가 사라졌으면 WRITERS를 갱신하라"
    hits = [
        f"{fname}:{n}: {line.strip()[:120]}"
        for n, line in _code_lines(path.read_text(encoding="utf-8"))
        if PINNED.search(line)
    ]
    assert not hits, (
        "실행 라인에 세대 고정 모델 id:\n" + "\n".join(hits)
        + "\n별칭(claude-haiku / claude-opus)으로 적어라 — 세대가 바뀌어도 표기가 참으로 남는다."
    )


@pytest.mark.parametrize("fname", ARTIFACTS)
def test_published_artifact_model_is_alias(fname: str) -> None:
    """공개 산출물의 model 필드 — classification.json은 코드 writer가 없으므로 여기가 유일한 게이트다."""
    path = ROOT / fname
    assert path.exists(), f"{fname} 없음"
    model = json.loads(path.read_text(encoding="utf-8")).get("model")
    assert model, f"{fname}에 model 필드가 없다 — 무엇으로 쟀는지 공시가 사라졌다"
    assert not PINNED.search(model), (
        f'{fname}: "model": "{model}" — 세대 고정 금지. '
        "다음 세대가 나오는 순간 공개 저장소의 방법론 표기가 거짓이 된다."
    )


def test_writers_agree_on_notation() -> None:
    """같은 ranking.json에 두 writer가 쓴다 — 표기 방식이 갈리면 회차마다 다른 말을 게시한다."""
    for fname in WRITERS:
        src = (ROOT / fname).read_text(encoding="utf-8")
        m = re.search(r'"model":\s*"([^"]+)"', src)
        assert m, f"{fname}에서 model 리터럴을 못 찾았다 — 구조가 바뀌었으면 이 테스트를 갱신하라"
        assert not PINNED.search(m.group(1)), f"{fname}: {m.group(1)} 이 세대 고정형이다"


def test_detector_is_alive() -> None:
    """탐지기 생존 확인 — 통과시키는 쪽 고장은 조용하다.

    합성 입력으로 '세대 id는 반드시 걸린다'와 '별칭·주석은 안 걸린다'를 같이 못박는다.
    이게 없으면 정규식이 아무것도 안 잡게 망가져도 테스트는 계속 초록이다.
    """
    # 되돌린 형태(회귀 원본)는 반드시 걸려야 한다
    assert PINNED.search('"model": "claude-haiku-4-5",'), "탐지기가 고정 id를 못 잡는다"
    assert PINNED.search('"model": "claude-opus-4-8"'), "탐지기가 다른 계열 고정 id를 못 잡는다"
    # 현행 별칭 표기는 통과해야 한다
    for ok in ("claude-haiku (분류)", "claude-haiku (블라인드 심사)",
               "claude-opus (채점) / claude-haiku (답변 생성)"):
        assert not PINNED.search(ok), f"별칭 표기를 반려한다: {ok}"
    # 주석 줄은 스캔에서 빠진다(과거 회차 기록 보호)
    comment = "  # 2026-08 회차는 claude-haiku-4-5 로 돌았다\ncode = 1"
    assert not any(PINNED.search(l) for _, l in _code_lines(comment)), "주석까지 잡는다"
