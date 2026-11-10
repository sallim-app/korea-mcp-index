#!/usr/bin/env python3
"""순위 밖 사유 불변식 (2026-11-10, T-2026W46-14).

사장님 지적: "순위 밖인 것도 왜 순위 밖인지 있어야 될 것 같다." 실측(라이브 2026-11-10)으로
부동산 순위 밖 7곳 중 4곳은 사유 칸이 전부 비어 있었다.

여기서 고정하는 것은 **이름이 아니라 불변식**이다 — 특정 서버의 사유 코드를 박으면 다음
회차에 그 서버가 바뀌는 순간 회귀가 낡은 사실을 지킨다. 그래서:
  ① 순위표에 서 있지 않은 **모든** 줄(rank null 또는 rank_is_current=false)에 코드·문장·근거가
     있고, 서 있는 줄엔 없다 — 전 분야, 전 줄.
  ② 코드는 어휘(unranked.VOCAB) 안에 있고 스키마 enum과 같다.
  ③ 분야별 건수가 배열·counts와 재현된다(배열 밖 셋 포함).
  ④ 사람 페이지에도 나온다 — 순위 밖 줄이 있는 분야 페이지에 「순위 밖」 절, 그 서버 상세에
     「순위에 없는 이유」.
  ⑤ 이름 예외표가 없다 — unranked.py 소스에 측정 대상 서버 이름이 하나도 없다.
  ⑥ 우리 서버도 같은 규칙 — 등수 있는 운영자 서버를 응답 없음으로 만들면 사유가 붙는다.
"""
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import unranked  # noqa: E402
from test_site import build  # noqa: E402

_CACHE: dict = {}


def _site():
    if "out" not in _CACHE:
        tmp = tempfile.mkdtemp()
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        _CACHE["out"] = out
        _CACHE["idx"] = json.loads((out / "index.json").read_text(encoding="utf-8"))
    return _CACHE["out"], _CACHE["idx"]


def _unranked_rows(idx):
    return [s for s in idx["servers"]
            if s["rank_in_category"] is None or s["rank_is_current"] is False]


def test_every_unranked_row_has_a_reason_and_ranked_rows_have_none():
    _, idx = _site()
    rows = _unranked_rows(idx)
    assert rows, "순위 밖 줄이 0건 — 렌더가 비었거나 판정이 바뀌었다"
    missing = [s["name"] for s in rows
               if not (s.get("unranked_reason") and s.get("unranked_reason_text")
                       and s.get("unranked_reason_basis"))]
    assert missing == [], f"사유 없는 순위 밖 줄 {len(missing)}건: {missing[:5]}"
    bad_code = [(s["name"], s["unranked_reason"]) for s in rows
                if s["unranked_reason"] not in unranked.VOCAB
                or s["unranked_reason"] in unranked.OUTSIDE]
    assert bad_code == []
    standing = [s for s in idx["servers"] if s not in rows]
    leaked = [s["name"] for s in standing
              if s.get("unranked_reason") or s.get("unranked_reason_text")]
    assert leaked == [], f"순위표에 서 있는데 사유가 붙은 줄: {leaked[:5]}"


def test_vocabulary_published_and_matches_schema():
    _, idx = _site()
    assert idx["unranked_vocabulary"] == unranked.VOCAB
    schema = json.loads((ROOT / "index.schema.json").read_text(encoding="utf-8"))
    enum = schema["properties"]["servers"]["items"]["properties"]["unranked_reason"]["enum"]
    assert set(enum) - {None} == set(unranked.VOCAB) - set(unranked.OUTSIDE)
    try:
        import jsonschema
    except ImportError:
        return
    jsonschema.validate(idx, schema)


def test_counts_by_category_reproduce_from_array_and_counts():
    _, idx = _site()
    by = idx["unranked_by_category"]
    total_in = sum(n for c in by.values() for k, n in c.items() if k not in unranked.OUTSIDE)
    assert total_in == len(_unranked_rows(idx))
    for k in ("install_only", "no_address_no_package"):
        assert sum(c.get(k, 0) for c in by.values()) == idx["counts"][k], k
    assert sum(c.get("not_measured", 0) for c in by.values()) == idx["counts"]["not_measured"]
    for cat, codes in by.items():
        arr = [s for s in _unranked_rows(idx) if (s["category"] or "분야 미분류") == cat]
        for code in set(codes) - set(unranked.OUTSIDE):
            assert codes[code] == sum(1 for s in arr if s["unranked_reason"] == code), (cat, code)


def test_human_pages_show_the_reason():
    out, idx = _site()
    rows = _unranked_rows(idx)
    cats_with = {s["category"] for s in rows}
    pages = {p.stem: p.read_text(encoding="utf-8") for p in (out / "category").glob("*.html")}
    checked = 0
    for html in pages.values():
        m = re.search(r"<h1>(.+?) — 한국 MCP 서버 실측</h1>", html)
        cat = m and __import__("html").unescape(m.group(1))
        if cat in cats_with:
            assert 'id="unranked"' in html and "순위 밖" in html, cat
            checked += 1
    assert checked >= 1
    base = "https://example.test/idx/"
    for s in rows:
        rel = s["page"].replace(base, "")
        p = out / (rel + ".html") if (out / (rel + ".html")).exists() else out / rel
        text = p.read_text(encoding="utf-8")
        assert "순위에 없는 이유" in text and s["unranked_reason"] in text, s["name"]


def test_no_name_exceptions_in_source():
    src = (ROOT / "unranked.py").read_text(encoding="utf-8")
    names = [i["name"] for i in json.loads((ROOT / "measured.json")
                                           .read_text(encoding="utf-8"))["items"]]
    hits = [n for n in names if n in src]
    assert hits == [], f"unranked.py에 서버 이름이 박혀 있다(예외표 금지): {hits}"


def test_reason_mapping_from_probe_buckets():
    j = unranked.Judging(ROOT)
    assert j.reason("x/y", "down", {"why": "DNS"}, "부동산")[0] == "down"
    assert j.reason("x/y", "unverified", {"http": 404}, "부동산")[0] == "transport_mismatch"
    # 402 상태코드만으로는 결제 요구라 적지 않는다(본문 근거가 있어야) — codex 지적 2026-11-10
    assert j.reason("x/y", "unverified", {"http": 402}, "부동산")[0] == "unverified"
    assert j.reason("x/y", "unverified", {"http": 402, "error_body": "Unavailable Shop"},
                    "부동산")[0] == "unverified"
    assert j.reason("x/y", "unverified", {"http": 402, "error_body": '{"x402Version":1}'},
                    "부동산")[0] == "payment_required"
    assert j.reason("x/y", "unverified", {"http": 502}, "부동산")[0] == "unverified"
    assert j.reason("x/y", "unmeasurable", {"http": 401}, "부동산")[0] == "credential_required"
    assert j.reason("x/y", "unmeasurable", {"http": 400}, "부동산")[0] == "no_tools"
    assert j.reason("x/y", "off_topic", {}, "부동산")[0] == "off_topic"
    # 채점하지 않는 분야
    assert j.reason("x/y", "comparable", {"http": 200}, "없는 분야")[0] == "category_not_graded"
    # 채점 분야인데 회차 명단·기록 어디에도 없는 새 서버 → 다음 회차 대기
    if j.graded_cats and j.round:
        assert j.reason("x/never-seen", "comparable", {"http": 200},
                        j.graded_cats[0])[0] == "awaiting_round"


def test_operator_server_gets_the_same_rule():
    """⑥: 등수 있는 운영자 서버를 응답 없음으로 만들면 우리 서버도 사유가 붙는다."""
    _, idx = _site()
    ours = [s["name"] for s in idx["servers"]
            if s["operated_by_us"] and s["rank_in_category"] is not None
            and s["rank_is_current"]]
    if not ours:
        return
    target = ours[0]
    d = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    items = d["items"]
    for it in items:
        if it["name"] == target:
            it["remote"] = {**it["remote"], "reachable": False, "status": "unverified",
                            "http": 502, "why": "HTTP 502", "tool_count": None}
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp, data_patch={"items": items})
        assert r.returncode == 0, r.stderr
        row = next(s for s in json.loads((out / "index.json").read_text(encoding="utf-8"))
                   ["servers"] if s["name"] == target)
        assert row["rank_is_current"] is False
        assert row["unranked_reason"] == "unverified" and row["unranked_reason_text"]
