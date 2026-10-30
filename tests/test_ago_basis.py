#!/usr/bin/env python3
"""'N일 전'이 기준 시점을 밝힌다 (2026-10-31, 야간 품질 스윕 F5).

정적 사이트라 `ago()`는 **렌더한 날** 기준으로 계산돼 HTML에 박힌다. 방문자는 그 문구를
'오늘 기준'으로 읽는데, 배포 후 며칠이 지나면 실제 나이와 어긋난다("28일 전"이 사실은
35일 전). 구조(JS)는 바꾸지 않고 문구가 기준을 스스로 밝히게 한다.
"""
import datetime as dt
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import render_site  # noqa: E402

BASIS = "이 페이지 생성일 기준"


def test_ago_names_its_reference_date():
    today = dt.date(2026, 10, 31)
    for days in (0, 1, 5, 28, 90):
        s = render_site.ago((today - dt.timedelta(days=days)).isoformat(), today)
        assert s.startswith(BASIS), (days, s)
    assert render_site.ago("not-a-date", today) == ""


def test_rendered_pages_disclose_generation_basis():
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "site"
        r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                            "--base", "https://example.test/idx", "--out", str(out)],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr
        bad = []
        for p in out.rglob("*.html"):
            h = p.read_text(encoding="utf-8")
            # 'N일 전'·'하루 전'·'오늘' 괄호 표기 앞에 기준이 없으면 박제다
            for m in re.finditer(r"\((?:\d+일 전|하루 전|오늘)", h):
                bad.append(f"{p.name}: {h[m.start():m.start() + 40]}")
        assert not bad, bad[:5]
        page = next((out / "servers").glob("*.html")).read_text(encoding="utf-8")
        assert BASIS in page
