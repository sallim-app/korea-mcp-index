#!/usr/bin/env python3
"""신뢰 규약 3조를 기계로 건다 (2026-08-21, T-2026W34-110).

**규약은 지키겠다고 쓴 문장이 아니라 어길 수 없게 만든 배관일 때만 규약이다.**
이 목록은 우리 제품을 순위에 넣은 채로 게시하므로, 세 가지가 조용히 무너질 수 있다.

  ① 축을 결과 본 뒤에 바꾼다 — 게시된 축과 사전공개 문서가 어긋나면 아무도 모른다
  ② 불리한 축을 뺀다 — 유리한 축만 남은 표는 판정이 아니라 광고지다
  ③ "원자료 공개"라고 써 두고 게시본이 그 원자료에서 재현되지 않는다

셋 다 사람 눈으로는 안 잡힌다(문서는 길고 축은 20종이다). 그래서 회귀로 박는다.

실행: python3 -m pytest tests/test_trust_protocol.py -q
"""
import csv
import json
import pathlib
import subprocess
import sys

import pytest

import recompute

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
MEASURED = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))

# 서버를 가리키는 열은 측정 항목이 아니다 — 사전공개 대상은 **잰 것**뿐이다.
IDENTITY = {"name", "category", "ours", "repo_url"}
AXES = [c for c in recompute.COLUMNS if c not in IDENTITY]


# ── ① 결과 보기 전에 공개·고정 ────────────────────────────────────────────
@pytest.mark.parametrize("axis", AXES)
def test_every_published_axis_is_pre_registered(axis):
    """게시하는 축은 전부 PROTOCOL.md에 적혀 있어야 한다 — 몰래 늘릴 수 없게."""
    assert f"`{axis}`" in PROTOCOL, (
        f"축 `{axis}`를 게시하면서 PROTOCOL.md에 안 적었다 — "
        "사전공개 없이 축을 늘리는 것이 규약 ①이 막는 바로 그것이다")


def test_no_phantom_axis_in_protocol():
    """반대 방향 — PROTOCOL.md의 측정 항목 표에 있는 축은 실제로 게시돼야 한다.

    적어만 두고 안 재면 사전공개가 장식이 된다.
    """
    import re
    declared = set()
    inside = False
    for ln in PROTOCOL.splitlines():
        if ln.startswith("## 고정된 측정 항목"):
            inside = True
            continue
        if inside and ln.startswith("## "):
            break
        if inside and ln.startswith("| `"):
            declared |= set(re.findall(r"`(\w+)`", ln.split("|")[1]))
    missing = declared - set(recompute.COLUMNS)
    assert not missing, f"PROTOCOL.md가 선언했는데 게시되지 않는 축: {sorted(missing)}"
    assert len(declared) >= 15, f"측정 항목 표를 못 읽었다({len(declared)}개) — 파서가 깨졌나"


def test_amendment_log_keeps_the_admission():
    """**결과를 본 뒤에 축을 바꾼 그 한 건**이 이력에서 지워지지 않았는가.

    가장 지우고 싶은 줄이라 가장 단단히 박는다. 이 테스트가 빨개졌는데 개정 사유가
    없다면, 그건 규약을 고친 것이 아니라 규약을 어긴 흔적을 지운 것이다.
    """
    assert "2026-08-19" in PROTOCOL
    assert "①을 어긴 것이다" in PROTOCOL, "①을 어겼다는 자인이 사라졌다"
    assert "블라인드 채점" in PROTOCOL


def test_readme_points_at_the_protocol_next_to_ownership():
    """편향 공시가 **소유 공시와 같은 자리**에 있는가 — 각주로 밀려나지 않았는가.

    규약이 요구하는 것은 '어딘가에 적혀 있다'가 아니라 '🏠를 읽는 자리에서 같이 읽힌다'다.
    """
    own = README.index("이 목록의 운영자(🏠 표시)도 같은 표에서")
    bias = README.index("그 표를 설계한 것도 우리다")
    first_section = README.index("## 한눈에")
    assert own < bias < first_section, "편향 공시가 소유 공시 옆에 없다"
    assert README.count("PROTOCOL.md") >= 3


# ── ② 우리가 지는 항목 ────────────────────────────────────────────────────
def test_losing_axes_section_is_published():
    """불리한 축 절이 살아 있고 세 축을 다 싣는가."""
    assert "## 우리가 지는 항목" in README
    sec = README[README.index("## 우리가 지는 항목"):]
    sec = sec[:sec.index("\n## ", 3)]
    for label in ("셀프호스팅", "오픈소스", "무료 한도"):
        assert label in sec, f"불리 축 `{label}`이 절에서 빠졌다"


def test_losing_axes_section_precedes_the_rankings():
    """**순위보다 먼저** 나오는가 — 문서 끝으로 밀면 싣지 않은 것과 신뢰 효과가 같다."""
    assert README.index("## 우리가 지는 항목") < README.index("## 공공데이터")


def test_every_item_has_the_losing_axes_measured():
    """측정 자체가 비어 있지 않은가 — 절만 있고 값이 없으면 공시가 아니다."""
    items = MEASURED["items"]
    for r in items:
        assert (r.get("self_hosting") or {}).get("state") in ("packaged", "source_only", "unknown"), \
            f"{r['name']}: self_hosting 미측정"
        assert "open_source" in r, f"{r['name']}: open_source 미측정"


def test_unreadable_repo_is_not_published_as_not_open_source():
    """못 본 것을 '없다'로 게시하지 않는가 (기치② — 못 봄 ≠ 없음).

    404는 비공개·삭제·개명 중 하나이지 '오픈소스가 아니다'가 아니다.
    """
    for r in MEASURED["items"]:
        oss = r.get("open_source") or {}
        if oss.get("public") is None and not oss.get("license"):
            assert oss.get("why"), f"{r['name']}: 못 읽은 이유를 안 남겼다"
    assert "“오픈소스 아님”으로 읽지 말라" in README


def test_our_own_worse_than_the_axis_says_is_disclosed():
    """우리 셀프호스팅이 축 값보다 실질이 나쁘다는 자기공시가 남아 있는가."""
    ours = [r for r in MEASURED["items"] if r["name"].startswith(recompute.OURS)]
    assert ours, "운영자 서버가 측정본에 없다"
    assert all((r.get("self_hosting") or {}).get("state") == "source_only" for r in ours)
    assert "클론해도 답이 안 나온다" in README
    # 규약 문서에도 같은 자기공시가 있어야 한다 — README만 고치고 규약을 방치하면
    # 다음 렌더에서 조용히 빠진다.
    assert "클론해도 답이 안 나온다" in PROTOCOL
    assert "10종이 유료" in PROTOCOL, "무료 한도(우리가 지는 축)의 구체값이 규약에서 빠졌다"


# ── ③ 재계산 가능 ─────────────────────────────────────────────────────────
def test_axes_csv_matches_the_published_columns():
    """공개 표의 열이 사전공개 축과 같은가, 그리고 전 서버가 들어 있는가."""
    with open(ROOT / "axes.csv", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    rows = list(csv.DictReader(lines))
    assert list(rows[0]) == recompute.COLUMNS
    assert len(rows) == len(MEASURED["items"])


def test_published_numbers_reproduce_from_raw_data():
    """③의 핵심 — 원자료를 올린 것이 아니라 **그 원자료로 게시본이 재현되는가**."""
    r = subprocess.run([sys.executable, "recompute.py", "--verify"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"게시본이 원자료에서 재현되지 않는다:\n{r.stderr}"


def test_reweighting_runs_and_disclaims():
    """독자 가중치 계산이 실제로 돌고, 그 결과를 우리 순위라 부르지 않는가."""
    r = subprocess.run([sys.executable, "recompute.py", "--weights", "tool_count=1,warm_ms=-0.5"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "우리 순위가 아니다" in r.stdout
    assert len([ln for ln in r.stdout.splitlines() if ln.startswith(" ")]) > 3


def test_blank_is_not_zero_in_the_recompute_table():
    """빈 칸이 0으로 새지 않는가 — 안 잰 것을 0점으로 계산하면 재계산이 조용히 틀린다."""
    _, rows = recompute.rows()
    assert all(v is not None for r in rows for v in r.values())
    unreach = [r for r in rows if r["reachable"] in ("", 0)]
    assert any(r["tool_count"] == "" for r in unreach), \
        "응답 없는 서버의 도구 수가 빈 칸이 아니다 — 0으로 게시되면 '도구가 없다'는 거짓이 된다"
