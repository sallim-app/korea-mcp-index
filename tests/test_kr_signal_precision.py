"""한국 신호 판정의 오탐 두 가지 — 남의 서버를 우리 목록에 잘못 싣는 자리 (2026-09-07).

이 목록은 **한국 데이터 MCP**를 게시한다. 그러니 "한국 관련이다"는 판정 자체가
남의 저장소에 대한 공개 주장이다. 주간 재측정 2026-09-07 회차에서 그 주장이 두 번
거짓이었다.

  ① `de`**molit**`ion` — `molit`(국토교통부)이 부분문자열로 걸려 시카고 철거업체와
     영국 철거견적 서버가 "한국 관련은 맞으나…"로 공개 원자료에 실렸다.
  ② 언어 목록의 `한국어` — 러시아 데이터 서버(EGRUL/INN 조회·러시아우편 추적)가
     설명 끝의 "🌏 EN/中文/日本語/한국어" 하나로 **keep까지 올라와 게시본에
     「기타」 구역을 통째로 만들었다.**

둘 다 조용한 고장이다. 아무것도 실패하지 않고, 표가 한 줄 늘 뿐이다.

실행: pytest tests/test_kr_signal_precision.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import filter_candidates as fc  # noqa: E402


def verdict(name: str, desc: str) -> dict:
    return fc.classify({"name": name, "description": desc})


# ── ① molit 단어 경계 ──────────────────────────────────────────────
# (이름, 설명, 한국 신호가 있어야 하나)
MOLIT_CASES = [
    ("uk.co.demolitionquotes/site",
     "Demolition Quotes: the site's own MCP server — enquiry and quotes", False),
    ("com.salvagesignal/salvage-signal",
     "Chicago demolition and reclaimed-brick leads, pricing, and a Daily Drop", False),
    ("io.github.HyosikPark/kr-apt-trades",
     "Official Korean apartment sale prices (MOLIT). Clean JSON.", True),
    ("io.github.choiyounggi/korea-data-mcp",
     "Korean public holidays, business-day math, and MOLIT real-estate transactions", True),
]


@pytest.mark.parametrize("name,desc,want_kr", MOLIT_CASES)
def test_molit_needs_word_boundary(name: str, desc: str, want_kr: bool) -> None:
    got = bool(verdict(name, desc)["kr"])
    assert got is want_kr, (
        f"{name}: 한국 신호 {got} (기대 {want_kr}) — "
        "`molit`이 부분문자열로 잡히면 demolition이 국토교통부가 된다"
    )


def test_molit_is_in_ambiguous() -> None:
    """경계를 거는 명단에서 빠지면 ①이 그대로 되돌아온다."""
    assert "molit" in fc.AMBIGUOUS


# ── ② 언어 목록의 한국어 ───────────────────────────────────────────
LOCALE_CASES = [
    # 실제로 게시까지 갔던 원문
    ("saymon-agent/payforapi",
     "Saymon RU Data API — Russian-language data endpoints for AI agents: EGRUL/INN "
     "company check, Cyrillic search, research, Russian Post tracking. "
     "Pay-per-call via x402 in USDC (Base). 🌏 EN/中文/日本語/한국어", False),
    ("androidZzT/harness-engineering-practice",
     "Harness Engineering — a practical guide to the platform layer of coding agents "
     "(Claude Code & Codex): skills, hooks, config, permissions, reasoning effort. "
     "EN / 한국어 / 日本語 / 中文.", False),
    # 좁게 막는지 — 진짜 한국어를 다루는 서버는 살아 있어야 한다
    ("Alfex4936/Hangul-MCP", "한국어 맞춤법 고치기/글자 수 세기 MCP", True),
    ("SolarLLM/human-proofreader-mcp",
     "사람 편집자가 손본 것처럼 한국어 원고를 교정하는 MCP 서버", True),
    ("someone/korean-nlp-mcp", "Korean NLP tools (한국어 지원)", True),
]


@pytest.mark.parametrize("name,desc,want_kr", LOCALE_CASES)
def test_locale_list_hangul_is_not_a_korea_signal(name: str, desc: str, want_kr: bool) -> None:
    got = bool(verdict(name, desc)["kr"])
    assert got is want_kr, (
        f"{name}: 한국 신호 {got} (기대 {want_kr}) — "
        "언어 목록 안의 `한국어`는 번역 지원 표시이지 한국 데이터 신호가 아니다"
    )


def test_russian_server_does_not_reach_keep() -> None:
    """게시본에 「기타」 구역을 만든 그 경로 전체를 못박는다 — kr 신호만이 아니라 verdict."""
    v = verdict(
        "saymon-agent/payforapi",
        "Saymon RU Data API — Russian-language data endpoints for AI agents: EGRUL/INN "
        "company check, Cyrillic search, research, Russian Post tracking. 🌏 EN/中文/日本語/한국어",
    )
    assert v["verdict"] == "drop", f'keep/review로 올라왔다: {v}'


# ── 탐지기 생존 ────────────────────────────────────────────────────
def test_detectors_are_alive() -> None:
    """통과시키는 쪽 고장은 조용하다 — 판별기 자체가 살아 있는지 합성 입력으로 본다."""
    # molit 경계: 되돌린 형태(부분문자열)는 반드시 걸려야 한다
    assert fc._hit("demolition quotes", ["molit"]) == [], "경계가 안 걸린다"
    assert fc._hit("MOLIT real-estate", ["molit"]) == ["molit"], "진짜 MOLIT을 놓친다"
    # 로케일 목록 판별기
    assert "한국어" not in fc.strip_locale_list("EN/中文/日本語/한국어")
    assert "한국어" in fc.strip_locale_list("한국어 맞춤법 교정"), "너무 넓게 지운다"
