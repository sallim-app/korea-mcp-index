#!/usr/bin/env python3
"""채점받은 4위 이하가 '채점하지 않았다'로 게시되던 결함의 회귀 (2026-10-11).

계기: `rebuild_ranking.py`가 `"top": top[:3]`만 등수 레코드로 넘겼고 렌더러(사이트·README·
index.json)는 `top`만 읽었다. 그래서 실제로 채점받아 분야 4위가 된 서버가 공개면에서
"답변 품질을 채점하지 않았다 — 못 재서이지 나빠서가 아니다"로 나가고, index.json엔
rank_in_category=null·fact_errors=null로 나갔다(2026-10-07 감사·2026-10-11 라이브 재확인:
MosslandOpenDevs/alpha 금융 4위·사실오류 1 등 3건). **잰 것을 안 쟀다고 공시**한 셈이다.

불변식(시점 사실을 박지 않는다 — 특정 서버 이름 대신 원자료 grades/에서 파생):
  grades/의 `권장순위`에 오른 서버(분야 교정 제외)는 전부 ranking.json에 등수·사실오류
  레코드를 갖고, 사이트·index.json·README에서 '채점됨'으로 나간다.
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
BASE = "https://example.test/idx"


def _graded_ranks() -> dict[str, tuple[str, int, int]]:
    """grades/에서 직접: name → (분야, 등수, 사실오류 건수). rebuild_ranking과 같은 규칙."""
    from observed import MISFILED
    out = {}
    for f in sorted((ROOT / "grades").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if "servers" not in d:
            continue
        by = {s["server"]: s for s in d["servers"]}
        n = 0
        for name in d.get("권장순위") or []:
            s = by.get(name)
            if not s or name in MISFILED:
                continue
            n += 1
            errs = sum(len(q.get("사실오류") or []) for q in s["questions"])
            out[name] = (d["category"], n, errs)
    return out


def test_ranking_json_keeps_every_graded_rank():
    """ranking.json이 3위까지만 레코드를 갖고 나머지를 이름만 남기면 렌더러가 미채점으로 읽는다."""
    rk = json.loads((ROOT / "ranking.json").read_text(encoding="utf-8"))["items"]
    for v in rk.values():
        recs = {t["name"] for t in v["top"]}
        missing = [n for n in v.get("전체순위") or [] if n not in recs]
        assert not missing, f"{v['category']}: 전체순위엔 있는데 등수 레코드가 없다 {missing}"


def test_graded_below_top3_published_as_graded():
    graded = _graded_ranks()
    deep = {n: v for n, v in graded.items() if v[1] > 3}
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "site"
        r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                            "--base", BASE, "--out", str(out)],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr
        idx = json.loads((out / "index.json").read_text(encoding="utf-8"))
        rows = {s["name"]: s for s in idx["servers"]}
        bad = []
        for name, (_cat, rank, errs) in graded.items():
            s = rows.get(name)
            if not s:
                continue  # 이번 주 목록에 없는 서버(개명·소멸)는 이 회귀의 대상이 아니다
            if s["rank_in_category"] != rank or s["fact_errors"] != errs:
                bad.append((name, rank, errs, s["rank_in_category"], s["fact_errors"]))
        assert not bad, f"index.json 등수·사실오류가 grades/와 다르다(이름·기대·실제): {bad}"
        for name, (_cat, rank, _errs) in deep.items():
            s = rows.get(name)
            if not s:
                continue
            page = out / s["page"][len(BASE):].lstrip("/")
            if not page.suffix:
                page = page.with_suffix(".html")
            html = page.read_text(encoding="utf-8")
            assert "답변 품질을 채점하지 않았다" not in html, f"{name}: 채점받았는데 미채점 문구"
            assert f"<strong>{rank}위</strong>" in html, f"{name}: 페이지에 {rank}위가 없다"


def test_readme_ranks_below_top3():
    """README 순위 줄에 4위 이하도 번호로 나가고, '채점하지 않은' 접힘에 들어가지 않는다."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    import render_readme
    for name, (_cat, rank, _errs) in _graded_ranks().items():
        if rank <= 3 or f"[{render_readme.disp(name)}]" not in readme \
                and render_readme.disp(name) not in readme:
            continue
        assert re.search(rf"^{rank}\. \*\*{re.escape(render_readme.disp(name))}\*\*",
                         readme, re.M), f"{name}: README 순위 줄에 {rank}위가 없다"
        for blk in re.findall(r"<details><summary>채점하지 않은.*?</details>", readme, re.S):
            assert render_readme.disp(name) not in blk, f"{name}: 채점받았는데 '채점하지 않은'에 있다"
