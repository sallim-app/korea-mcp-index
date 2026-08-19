#!/usr/bin/env python3
"""패키지 축(①배포 여부·최신 배포일)의 회귀 고정 (2026-08-20, T-2026W34-107).

**이 축은 틀린 채로 게시돼 있었다.** `pip install -r requirements.txt`의 `-r`이 패키지명으로
잡히고, 그 이름이 레지스트리에 없자 남의 서버 15건이 공개 `measured.json`에 `설치 불가`로
박혔다. 우리가 이름을 못 읽은 것을 그 서버의 결함으로 게시한 것이다 — 이 목록이 남의 목록에서
잡아내려는 바로 그 종류의 거짓이고, 기치②(못 봄 ≠ 없음)를 측정기가 자기 손으로 위반한 자리다.

그래서 세 가지를 회귀로 박는다:
  1. 설치 명령에서 이름을 못 고르면 **None**이다(플래그·파일·주소·설치기를 이름으로 쓰지 않는다)
  2. 이름이 이름답지 않으면 레지스트리에 **묻지도 않고** `installable=null`이다(false 아님)
  3. 게시본 `measured.json`에 `-r`류 식별자와 그로 인한 `installable=false`가 **없다**

실행: python3 -m pytest tests/test_package_axis.py -q
"""
import json
import pathlib

import pytest

import enrich
import measure

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEASURED = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))


def _extract(text: str):
    """enrich이 README에서 패키지명을 고르는 경로 그대로."""
    for rx, kind in ((enrich.RE_NPX, "npm"), (enrich.RE_UVX, "pypi"), (enrich.RE_PIP, "pypi")):
        pkg = next((p for p in (enrich._pkg_from_cmd(m.group(1)) for m in rx.finditer(text)) if p),
                   None)
        if pkg:
            return kind, pkg
    return None, None


@pytest.mark.parametrize("cmd", [
    "pip install -r requirements.txt",              # 실측 15건의 원인 — `-r`이 잡혔다
    "pip3 install -r requirements.txt && python server.py",
    "uvx --from git+https://github.com/a/b mcp-server-b",   # 배포판이 아니라 git 설치
    "npx -y @smithery/cli install @snaiws/DART-mcp-server", # 설치기 — 이 서버의 배포판이 아니다
    "npx @anthropic-ai/mcpb pack",                  # 번들러
    "npx tsx src/server.ts",                        # 런너
    "python -m venv .venv && pip install -e .",     # 로컬 편집설치는 배포가 아니다
])
def test_no_name_is_none_not_a_flag(cmd):
    """이름을 못 고르는 명령에서 플래그·파일·설치기를 패키지명으로 만들지 않는다."""
    kind, pkg = _extract(cmd)
    assert pkg is None, f"{cmd!r} → {pkg!r}를 패키지명으로 잡았다"


@pytest.mark.parametrize("cmd,expect", [
    ("pip install dart-mcp", "dart-mcp"),
    ("pip install -U hospital-fee-mcp", "hospital-fee-mcp"),
    ("uvx korea-law-mcp", "korea-law-mcp"),
    ("uvx --from realestate-stats-mcp rs-mcp", "realestate-stats-mcp"),
    ("npx -y @opendata-kr/core", "@opendata-kr/core"),
    ("npx --yes @leokim90/gov-data-mcp", "@leokim90/gov-data-mcp"),
])
def test_real_names_still_extracted(cmd, expect):
    """고치면서 잘 되던 것을 깨지 않았는가 — 실제 후보 README의 명령 모양이다."""
    assert _extract(cmd)[1] == expect


@pytest.mark.parametrize("ident", ["-r", "--from", "requirements.txt", "git+https://x/y",
                                   "@smithery/cli", "tsx", "my-mcp-server", "./server.py"])
def test_implausible_ids_are_unmeasured_not_false(ident):
    """이름이 이름답지 않으면 `null`(못 쟀다)이다 — `false`(설치 불가)로 적으면 남을 깎는다."""
    assert measure._implausible(ident), f"{ident!r}를 정상 패키지명으로 통과시켰다"
    got = measure.measure_package({"type": "pypi", "id": ident})
    assert got["installable"] is None
    assert got["why"]


@pytest.mark.parametrize("ident", ["dart-mcp", "@opendata-kr/core", "korea-unipass-mcp"])
def test_plausible_ids_are_looked_up(ident):
    """정상 이름은 그대로 조회 대상이다(네트워크 없이 게이트만 확인)."""
    assert measure._implausible(ident) is None


def test_published_measured_has_no_flag_ids():
    """게시본에 옵션·파일·주소가 패키지명으로 남아 있지 않다."""
    bad = [(i["name"], i["package"]["id"]) for i in MEASURED["items"]
           if (i.get("package") or {}).get("id") and measure._implausible(i["package"]["id"])]
    assert not bad, f"게시본에 읽을 수 없는 패키지 식별자 {len(bad)}건: {bad[:5]}"


def test_published_measured_has_no_false_uninstallable_from_parse_failure():
    """`설치 불가`로 단정한 건은 전부 **읽을 수 있는 이름**을 실제로 조회한 결과여야 한다."""
    wrong = [i["name"] for i in MEASURED["items"]
             if (i.get("package") or {}).get("installable") is False
             and measure._implausible(i["package"].get("id") or "")]
    assert not wrong, f"우리 파싱 실패를 남의 서버 '설치 불가'로 게시: {wrong}"


@pytest.mark.parametrize("readme", [
    # 재측정에서 실제로 걸린 것 — 인자 열이 **다음 줄까지** 넘어가 뒷줄 토큰을 패키지명으로 썼다.
    "pip install -r requirements.txt\npython server.py",
    "pip install -r requirements.txt\nSUPABASE_URL=xxx\nSUPABASE_KEY=yyy",
    "npx tsx src/index.ts\ncp .env.example .env",
    "uvx --from git+https://github.com/a/b srv\nexport API_KEY=...",
])
def test_args_do_not_span_lines(readme):
    """설치 명령의 인자는 그 줄에서 끝난다 — 다음 줄은 다른 명령이다."""
    assert _extract(readme)[1] is None, f"{readme!r} → {_extract(readme)[1]!r}"
