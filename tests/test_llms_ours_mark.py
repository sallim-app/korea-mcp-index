#!/usr/bin/env python3
"""llms.txt 서버 행에 운영자 표시가 붙는다 (2026-10-31, 야간 품질 스윕 F2).

index.json은 `operated_by_us`로 우리 서버를 가르는데 llms.txt — AI가 읽는 표면 — 의
서버 행에는 그 표시가 없었다. 경계 절에 "이 목록을 만든 곳도 여기에 서버를 운영한다"는
문장은 있지만 **어느 행이 그것인지**는 행에서 안 보였다. 판정은 index.json과 같은
`name.startswith(OURS)`다.
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "이 목록 운영자의 서버"


def test_llms_txt_marks_our_rows_and_only_ours():
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "site"
        r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                            "--base", "https://example.test/idx", "--out", str(out)],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr
        llms = (out / "llms.txt").read_text(encoding="utf-8")
        ours = {s["name"] for s in json.loads((out / "index.json").read_text(
            encoding="utf-8"))["servers"] if s["operated_by_us"]}
    rows = re.findall(r"^- \[([^\]]+)\]\(https://example\.test/idx/servers/[^)]*\): (.*)$",
                      llms, re.M)
    assert rows
    marked = {n for n, rest in rows if MARK in rest}
    listed_ours = {n for n, _ in rows if n in ours}
    assert listed_ours, "자사 행이 llms.txt에 하나도 없다"
    assert marked == listed_ours, (marked, listed_ours)
    # 개수(지금 3)는 박지 않는다 — 시점 사실이라 서버가 늘면 회귀가 오보를 지킨다
