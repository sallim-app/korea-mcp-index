#!/usr/bin/env python3
"""자사 서버 자기공시가 상세 페이지·index.json까지 간다 (2026-10-31, 야간 품질 스윕 F1).

`observed.SOURCE_CLOSED`는 "우리 서버에는 '미확인'을 쓰지 않는다"는 규칙인데, 그 값이
홈 운영자 칸에만 쓰이고 상세 페이지 셀프호스팅 칸·'우리가 재지 않은 것' 목록·index.json에는
안 갔다 — 라이브 /servers/app-sallim-korea-stay 가 "셀프호스팅 미확인 — 불가가 아니라
미확인이다"라고 적었다. 우리가 답을 아는 축에서 '미확인' 뒤에 숨는 것이 PROTOCOL ②가
막으려는 동작이다.

고정하는 것:
① 자사 SOURCE_CLOSED 서버의 상세 페이지 셀프호스팅 칸에 자기공시 문구가 있고 '미확인'이 없다.
② '우리가 재지 않은 것' 목록에도 그 공시가 실린다.
③ index.json 그 행에 `self_hosting_note`로 같은 문구가 실리고, 기존 `self_hosting` 축 값은
   그대로다(축 어휘 변경은 PROTOCOL 개정 판단이라 여기서 안 한다).
④ **남의 서버에는 절대 안 간다** — SOURCE_CLOSED에 남의 이름을 억지로 넣어도 그 서버는
   여전히 '미확인'이고 note는 null이다.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://example.test/idx"
sys.path.insert(0, str(ROOT))
from observed import SOURCE_CLOSED  # noqa: E402

OURS = ("app.sallim/", "sallim-app/")
STAY = "app.sallim/korea-stay"


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _render(tmp, extra_closed=None):
    cwd = ROOT
    if extra_closed:
        cwd = pathlib.Path(tmp) / "repo"
        cwd.mkdir()
        for f in ROOT.iterdir():
            if f.name in {"site", "__pycache__", ".git", "tests", "node_modules"}:
                continue
            (shutil.copytree if f.is_dir() else shutil.copy2)(f, cwd / f.name)
        src = (cwd / "observed.py").read_text(encoding="utf-8")
        add = "".join(f"    {k!r}: {v!r},\n" for k, v in extra_closed.items())
        src = src.replace("SOURCE_CLOSED: dict[str, str] = {\n",
                          "SOURCE_CLOSED: dict[str, str] = {\n" + add, 1)
        (cwd / "observed.py").write_text(src, encoding="utf-8")
    out = pathlib.Path(tmp) / "site"
    r = subprocess.run([sys.executable, str(cwd / "render_site.py"),
                        "--base", BASE, "--out", str(out)],
                       cwd=cwd, capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    return out


def _sh_cell(html):
    m = re.search(r"<dt>셀프호스팅</dt><dd>(.*?)</dd>", html, re.S)
    assert m, "셀프호스팅 칸이 없다"
    return m.group(1)


def _unknowns(html):
    i = html.index("우리가 재지 않은 것</h2>")
    return html[i:html.index("</ul>", i)]


def test_our_closed_server_publishes_self_disclosure_not_unknown():
    assert STAY in SOURCE_CLOSED
    note = SOURCE_CLOSED[STAY]
    with tempfile.TemporaryDirectory() as tmp:
        out = _render(tmp)
        html = (out / "servers" / f"{_slug(STAY)}.html").read_text(encoding="utf-8")
        cell = _sh_cell(html)
        assert note in cell, cell
        assert "미확인" not in cell, cell
        assert "불가가 아니라 미확인" not in html
        assert note in _unknowns(html)

        d = json.loads((out / "index.json").read_text(encoding="utf-8"))
        rows = {s["name"]: s for s in d["servers"]}
        assert rows[STAY]["self_hosting_note"] == note
        # 축 값은 그대로 — 어휘 변경은 PROTOCOL 개정 판단이다
        assert rows[STAY]["self_hosting"] == "unknown"
        for name, s in rows.items():
            if not (name.startswith(OURS) and name in SOURCE_CLOSED):
                assert s["self_hosting_note"] is None, name


def test_self_disclosure_never_applies_to_other_servers():
    with tempfile.TemporaryDirectory() as tmp:
        base = json.loads((_render(tmp) / "index.json")
                          .read_text(encoding="utf-8"))
    foreign = next(s["name"] for s in base["servers"]
                   if not s["operated_by_us"] and s["self_hosting"] == "unknown")
    fake = "공개 저장소가 없다 — 남의 이름에 붙이면 안 되는 문구"
    with tempfile.TemporaryDirectory() as tmp:
        out = _render(tmp, extra_closed={foreign: fake})
        html = (out / "servers" / f"{_slug(foreign)}.html").read_text(encoding="utf-8")
        assert fake not in html
        assert _sh_cell(html).startswith("미확인")
        d = json.loads((out / "index.json").read_text(encoding="utf-8"))
        row = next(s for s in d["servers"] if s["name"] == foreign)
        assert row["self_hosting_note"] is None
