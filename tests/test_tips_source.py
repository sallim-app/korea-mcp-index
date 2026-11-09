#!/usr/bin/env python3
"""제보 원천(tips.json)이 수집→판정 길목을 실제로 타는지 고정한다 (2026-11-09, T-2026W46-05).

**계기.** 줍고(`www.jupgo.co.kr/mcp`)는 레지스트리 `search=jupgo` 0건 · 공개 저장소 없음 ·
playmcp/ChatGPT 앱 스토어에만 있다 — 원천 4층이 구조적으로 못 보는 서버다. 사람이 알려 준
것을 파일에 적어 두기만 하고 수집기가 안 읽거나, 읽어도 필터가 떨어뜨리면 "편입했다"는
말이 거짓이 된다. 네트워크를 타지 않는다.

실행: python3 -m pytest tests/test_tips_source.py -q
"""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


collect = _load("collect_candidates")
filt = _load("filter_candidates")


def test_tips_file_is_read_and_jupgo_is_kept():
    tips, notes = collect.from_tips(str(ROOT / "tips.json"))
    assert notes == []
    assert "kr.co.jupgo/mcp" in tips
    merged = collect.merge_sources({}, {}, {}, tips)
    row = merged["kr.co.jupgo/mcp"]
    assert row["sources"] == ["tip"]
    assert row["remotes"][0]["url"] == "https://www.jupgo.co.kr/mcp"
    # 제보는 판정을 면제받지 않는다 — 같은 판정기가 keep을 내야 측정 모집단에 든다.
    assert filt.classify(row)["verdict"] == "keep"


def test_tip_merges_with_registry_by_endpoint():
    """나중에 운영자가 레지스트리에 등록하면 같은 주소로 한 줄이 된다(두 줄 금지)."""
    tips, _ = collect.from_tips(str(ROOT / "tips.json"))
    reg = {"co.jupgo/x": {"name": "co.jupgo/x", "description": "", "repo_url": "",
                          "remotes": [{"url": "https://www.jupgo.co.kr/mcp"}],
                          "sources": {"registry"}, "terms": {"전수"}}}
    merged = collect.merge_sources(reg, tips)
    assert len(merged) == 1
    assert list(merged.values())[0]["sources"] == ["registry", "tip"]


def test_missing_or_broken_tips_file(tmp_path):
    assert collect.from_tips(str(tmp_path / "none.json")) == ({}, [])
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    found, notes = collect.from_tips(str(bad))
    assert found == {} and notes and "미확인" in notes[0]


def test_tips_rows_have_evidence():
    for t in json.load(open(ROOT / "tips.json", encoding="utf-8"))["items"]:
        assert t["tip"]["date"] and t["tip"]["evidence"], t["name"]
