#!/usr/bin/env python3
"""codex 사후 재검증(T-2026W42-10) 지적 4건의 회귀.

① 주소 출처 판정이 저장소가 추적하지 않는 candidates_filtered.json에 기대고 있었다 —
   새 체크아웃에서 등록 주소까지 전부 'README 추정'이 되고 등록 주소 집계가 0이 됐다.
② 분야 교정(MISFILED)으로 무효화한 등수를 llms.txt만 그대로 게시했다.
③ 일시적 DNS 실패(EAI_AGAIN)를 '죽음 확인'으로 판정했다 — 못 봄 ≠ 없음.
④ 구 SSE endpoint 대기에 벽시간 상한이 없어 heartbeat가 잦으면 64KiB까지 붙잡혔다.

바깥을 두드리지 않는다 — 렌더는 리포 복사본에서, 전송은 목으로.
"""
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import measure  # noqa: E402
import render_readme  # noqa: E402

BASE = "https://example.test/idx"


def _copy_repo(tmp) -> pathlib.Path:
    cwd = pathlib.Path(tmp) / "repo"
    cwd.mkdir()
    for f in ROOT.iterdir():
        if f.name in {"site", "__pycache__", ".git", "tests", "node_modules"}:
            continue
        (shutil.copytree if f.is_dir() else shutil.copy2)(f, cwd / f.name)
    return cwd


def _render(cwd: pathlib.Path) -> pathlib.Path:
    out = cwd.parent / "site"
    r = subprocess.run([sys.executable, str(cwd / "render_site.py"),
                        "--base", BASE, "--out", str(out)],
                       cwd=cwd, capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    return out


# ── ① 주소 출처 ────────────────────────────────────────────────────────────

def test_addr_registered_reads_measured_url_source_first():
    assert render_readme.addr_registered({"remote": {"url_source": "registry"}}, {}) is True
    assert render_readme.addr_registered({"remote": {"url_source": "readme"}}, {}) is False
    # 후보 파일이 반대로 말해도 측정본이 이긴다(실제로 두드린 주소의 출처다)
    s0 = {"remotes": [{"url": "https://x", "confidence": "readme"}]}
    assert render_readme.addr_registered({"remote": {"url_source": "registry"}}, s0) is True
    # url_source가 없는 옛 회차는 후보 파일로 폴백한다
    assert render_readme.addr_registered({"remote": {}}, {"remotes": [{"url": "https://x"}]})


def test_fresh_checkout_without_candidates_keeps_registered_addresses():
    """candidates_filtered.json은 추적되지 않는다 — 없어도 등록 주소 집계가 0이 되면 안 된다."""
    with tempfile.TemporaryDirectory() as tmp:
        cwd = _copy_repo(tmp)
        (cwd / "candidates_filtered.json").unlink(missing_ok=True)
        out = _render(cwd)
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        d = json.loads((cwd / "measured.json").read_text(encoding="utf-8"))
        src_of = {i["name"]: (i.get("remote") or {}).get("url_source") for i in d["items"]}
        rows = [s for s in m["servers"] if s.get("endpoint")]
        reg = [s for s in rows if s["endpoint_source"] == "registry"]
        assert reg, "후보 파일이 없으니 등록 주소가 0건이 됐다 — 측정본 url_source를 안 읽는다"
        for s in rows:
            us = src_of.get(s["name"])
            if us:
                assert s["endpoint_source"] == ("readme_guess" if us == "readme"
                                                else "registry"), s["name"]


# ── ② llms.txt의 분야 교정 등수 ─────────────────────────────────────────────

def test_llms_txt_does_not_publish_voided_misfiled_rank():
    from observed import MISFILED
    with tempfile.TemporaryDirectory() as tmp:
        cwd = _copy_repo(tmp)
        d = json.loads((cwd / "measured.json").read_text(encoding="utf-8"))
        cls = {v["name"]: v for v in json.loads(
            (cwd / "classification.json").read_text(encoding="utf-8"))["items"].values()}
        live = {i["name"] for i in d["items"]
                if (i.get("remote") or {}).get("reachable")
                and (i.get("remote") or {}).get("tool_count")}
        rk = json.loads((cwd / "ranking.json").read_text(encoding="utf-8"))
        by_cat = {v["category"]: v for v in rk["items"].values()}
        name = next(n for n in MISFILED
                    if n in live and n in cls and cls[n]["category"] in by_cat)
        entry = by_cat[cls[name]["category"]]
        entry["top"] = [t for t in entry["top"] if t["name"] != name]
        entry["top"].insert(0, {"name": name, "rank": 1, "why": "틀린 분야 질문으로 매긴 값"})
        (cwd / "ranking.json").write_text(json.dumps(rk, ensure_ascii=False), encoding="utf-8")
        out = _render(cwd)
        llms = (out / "llms.txt").read_text(encoding="utf-8")
        line = next(ln for ln in llms.splitlines() if f"[{name}]" in ln)
        assert "1위" not in line, f"무효 등수를 llms.txt에 게시했다: {line}"
        assert "무효" in line and MISFILED[name][1] in line, line


# ── ③ 일시적 DNS 실패는 죽음이 아니다 ──────────────────────────────────────

EAI_AGAIN = "URLError: <urlopen error [Errno -3] Temporary failure in name resolution>"
NXDOMAIN = "URLError: <urlopen error [Errno -2] Name or service not known>"


def test_transient_dns_failure_is_not_down_evidence():
    assert measure._down_evidence(EAI_AGAIN) == ""
    assert measure._down_evidence(NXDOMAIN)
    assert measure._down_evidence("ConnectionRefusedError: [Errno 111] Connection refused")


def test_render_side_shares_the_verdict_and_downgrades_stale_down():
    # 상태 없는 옛 측정본
    assert render_readme.status_of({"remote": {"why": EAI_AGAIN}}) == "unverified"
    assert render_readme.status_of({"remote": {"why": NXDOMAIN}}) == "down"
    # 규칙이 고쳐지기 전 회차가 'down'으로 적어 둔 일시 실패
    assert render_readme.status_of({"remote": {"status": "down", "why": EAI_AGAIN}}) == "unverified"
    assert render_readme.status_of({"remote": {"status": "down", "why": NXDOMAIN}}) == "down"


def test_measure_remote_marks_transient_dns_unverified(monkeypatch):
    def boom(*a, **k):
        raise urllib.error.URLError("[Errno -3] Temporary failure in name resolution")
    import urllib.error
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    monkeypatch.setattr(measure.time, "sleep", lambda s: None)
    r = measure.measure_remote("https://gone-for-a-moment.example/mcp")
    assert r["status"] == "unverified", r


# ── ④ SSE endpoint 대기 벽시간 상한 ────────────────────────────────────────

class _Heartbeat(io.RawIOBase):
    """endpoint는 영영 안 주고 heartbeat만 잦게 보내는 스트림."""

    def __init__(self, gap):
        self.gap, self.lines = gap, 0
        self.headers = {"Content-Type": "text/event-stream"}
        self.status = 200

    def readline(self, *a):
        self.lines += 1
        if self.lines > 200:
            return b""            # 상한이 없을 때 테스트가 영영 안 끝나지 않게
        time.sleep(self.gap)
        return b": ping\n"

    def close(self):
        pass


def test_sse_open_has_a_wall_clock_deadline(monkeypatch):
    hb = _Heartbeat(0.01)
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: hb)
    monkeypatch.setattr(measure, "SSE_TIMEOUT", 0.3)
    t0 = time.monotonic()
    stream, ep, meta = measure._sse_open("https://sse.example/sse")
    assert stream is None and ep is None
    assert hb.lines < 100, f"heartbeat {hb.lines}줄을 읽도록 붙잡혔다 — 벽시간 상한이 없다"
    assert time.monotonic() - t0 < 1.5
