#!/usr/bin/env python3
"""산출물 회귀 고정 (2026-08-19).

**이 목록의 상품은 표다.** 표가 깨지면 값이 맞아도 상품이 아니다. 2026-08-19 사장님 검수에서
7건이 지적됐고, 그중 넷은 사람이 눈으로 봐야만 잡히는 종류였다(볼드 깨짐·링크 없음·
무응답 혼입·분야 없음). 그래서 산출물 자체를 검사한다 — 다음에 조용히 재발하지 않도록.

실행: python3 -m pytest tests/test_render.py -q
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
DOWN = (ROOT / "DOWN.md").read_text(encoding="utf-8")
MEASURED = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))

# 닫는 `**` 앞이 문장부호이고 뒤가 글자면 CommonMark가 강조를 닫지 않는다.
BROKEN_EMPH = re.compile(r'[)\]}"\'.,!?:;][*]{2}[0-9A-Za-z가-힣]')
def _server_rows(md: str) -> list[str]:
    """서버 표(헤더가 `| 서버 |`)의 데이터 줄만. 요약·축별 표는 대상이 아니다."""
    rows, inside = [], False
    for ln in md.splitlines():
        if ln.startswith("| 서버 |"):
            inside = True
            continue
        if inside:
            if not ln.startswith("|"):
                inside = False
            elif not ln.startswith("|---"):
                rows.append(ln.split("|")[1].strip())
    return rows


def test_no_broken_emphasis():
    """볼드가 실제로 닫히는가 — 게시본에서 깨졌던 자리."""
    for name, md in (("README", README), ("DOWN", DOWN)):
        assert not BROKEN_EMPH.findall(md), f"{name}에 깨지는 강조: {BROKEN_EMPH.findall(md)[:3]}"


def test_every_server_row_has_a_link():
    """링크 없는 줄은 독자가 그 서버로 갈 방법이 없다 — 목록의 기능이 죽는다."""
    rows = _server_rows(README) + _server_rows(DOWN)
    assert rows, "서버 표를 못 찾았다 — 파서가 산출물과 어긋났다"
    bad = [r for r in rows if "](" not in r]
    assert not bad, f"링크 없는 항목: {bad[:3]}"


def test_down_servers_are_not_in_the_main_list():
    """무응답은 본문에서 빠져야 한다(별도 DOWN.md)."""
    dead = {i["name"] for i in MEASURED["items"]
            if i.get("remote") and not i["remote"].get("reachable")}
    leaked = [n for n in dead if f"[{n}]" in README]
    assert not leaked, f"무응답이 본문에 남음: {leaked[:3]}"


def test_categories_exist_and_top3_is_capped():
    """분야별로 나뉘고 상위 3개만 먼저 보여야 한다."""
    cats = re.findall(r"^## ([^\n(]+?) \(", README, re.M)
    assert len(cats) >= 4, f"분야 섹션이 너무 적다: {cats}"
    for block in re.split(r"^## ", README, flags=re.M)[1:]:
        if "|---|" not in block:
            continue
        head = block.split("<details>")[0]
        rows = [ln for ln in head.splitlines() if ln.startswith("| [") or ln.startswith("| ")]
        rows = [r for r in rows if "](" in r]
        assert len(rows) <= 3, f"Top 3를 넘김({len(rows)}): {block[:40]}"


def test_operator_is_disclosed():
    """우리 서버는 표에 있고 운영자 표시가 붙어야 한다 — 빼는 것도 숨기는 것도 안 된다."""
    assert "korea-realty" in README, "운영자 서버가 표에서 빠졌다"
    assert "🏠" in README, "운영자 표시가 없다"


def test_no_private_or_personal_paths():
    """비공개 저장소·개인 계정 경로가 공개본에 새면 안 된다(2026-08-19 실사고)."""
    for name, md in (("README", README), ("DOWN", DOWN)):
        for leak in ("kwenhwang", "sallim-app/realty-mcp"):
            assert leak not in md, f"{name}에 {leak} 유출"
