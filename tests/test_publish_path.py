#!/usr/bin/env python3
"""게시 경로의 회귀 고정 — 표가 갱신됐는데 **사이트만 안 바뀌는 길**을 막는다 (T-2026W39-28).

**계기(실측 2026-09-21).** 렌더·배포·라이브 확인 세 단계가 저장소가 아니라 주간 회차
프롬프트 한 곳에만 명령어로 적혀 있었다. 그 회차가 2026-09-17 멈추자 게시하는 주체가
0이 됐는데 **아무것도 빨개지지 않았다** — 순위를 바꾸는 유일한 회차(매월 1일 채점)에는
애초에 배포 단계가 없었고, README는 커밋되니 최신인데 `mcp-index.sallim.app`만 조용히
낡았다(라이브 generated_at 2026-09-16 vs 저장소 HEAD 09-19).

**그래서 여기서 고정하는 것은 "스크립트가 있다"가 아니다.** 그건 파일 존재 검사이지
게이트 검사가 아니다. 이 파일이 재는 것은 **배포가 도달하지 않았을 때 실제로 빨개지는가**
— 로컬 HTTP 서버를 라이브인 척 세워 놓고 ①낡은 값을 주면 ②사이트맵 주소가 404면
③없는 주소까지 200을 주면, 세 경우 모두 `deploy-pages.sh`가 rc≠0으로 멈추는지 본다.
통과시키는 쪽 고장은 조용하므로, 초록만 확인하면 검사한 것이 없다.

실행: python3 -m pytest tests/test_publish_path.py -q
"""
import http.server
import json
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "deploy-pages.sh"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):   # 테스트 출력에 접근 로그를 흘리지 않는다
        pass


def _serve(directory: pathlib.Path, port: int, handler=_Quiet):
    cls = type("H", (handler,), {"__init__": lambda self, *a, **kw:
                                 handler.__init__(self, *a, directory=str(directory), **kw)})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), cls)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def _verify(out: pathlib.Path, port: int) -> subprocess.CompletedProcess:
    """`--verify-only`로 '라이브'를 두드린다 — 배포 단계는 타지 않는다."""
    env = {"PATH": "/usr/bin:/bin", "HOME": str(out),
           "SITE_OUT": str(out), "SITE_URL": f"http://127.0.0.1:{port}",
           # 로컬 서버엔 기다릴 엣지 전파가 없다. 실패하는 길도 시간 안에 끝나야 검사가 된다.
           "VERIFY_TRIES": "1", "VERIFY_SLEEP": "0"}
    return subprocess.run(["bash", str(SCRIPT), "--verify-only"], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=300)


@pytest.fixture(scope="module")
def rendered():
    """실물 렌더 1회. `--ext .html`인 이유: 로컬 http.server는 CF Pages의 확장자 생략
    라우팅을 흉내 내지 않는다 — 검사 대상은 그 라우팅이 아니라 **게시 판정 논리**다."""
    tmp = tempfile.mkdtemp()
    port = _free_port()
    out = pathlib.Path(tmp) / "site"
    r = subprocess.run([sys.executable, "render_site.py", "--out", str(out),
                        "--base", f"http://127.0.0.1:{port}", "--ext", ".html"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    yield out, port
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def live(rendered):
    """방금 만든 산출물의 **사본**을 라이브인 척 서빙한다(원본은 안 건드린다)."""
    out, port = rendered
    tmp = tempfile.mkdtemp()
    served = pathlib.Path(tmp) / "live"
    shutil.copytree(out, served)
    srv = _serve(served, port)
    yield out, served, port
    srv.shutdown()
    shutil.rmtree(tmp, ignore_errors=True)


def test_script_is_executable():
    """프롬프트가 `./deploy-pages.sh`로 부른다 — 실행 비트가 빠지면 회차가 거기서 죽는다."""
    assert SCRIPT.exists(), "게시 스크립트가 없다 — 배포 명령이 다시 프롬프트로 흩어졌다"
    assert SCRIPT.stat().st_mode & 0o111, f"{SCRIPT.name}에 실행 비트가 없다"


def test_green_when_live_matches(live):
    """라이브가 방금 만든 것과 같으면 통과한다 — 게이트가 상시 빨갛지 않은지부터 본다."""
    out, _served, port = live
    r = _verify(out, port)
    assert r.returncode == 0, f"정상인데 실패했다:\n{r.stdout}\n{r.stderr}"
    assert "DONE" in r.stdout


def test_red_when_live_is_stale(live):
    """**이 파일의 존재 이유.** 라이브가 낡았는데 배포가 '성공'으로 끝나는 길을 막는다."""
    out, served, port = live
    doc = json.loads((served / "index.json").read_text(encoding="utf-8"))
    doc["generated_at"] = "2026-01-01"          # 지난 회차가 아직 떠 있는 상태
    (served / "index.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8")
    r = _verify(out, port)
    assert r.returncode != 0, f"낡은 라이브를 통과시켰다:\n{r.stdout}"
    assert "라이브 index.json" in r.stderr


def test_red_when_a_sitemap_url_is_404(live):
    """사이트맵에 적은 주소는 색인해 달라고 남에게 한 약속이다 — 404면 배포 실패로 센다."""
    out, served, port = live
    # **사이트맵에 실린 주소**를 골라야 이 검사가 뜻을 갖는다 — 아무 .html이나 지우면
    # 색인 대상이 아닌 `404.html` 같은 것을 지우고 초록으로 통과한다(실측: 첫 판본이 그랬다).
    locs = re.findall(r"<loc>([^<]+)</loc>", (served / "sitemap.xml").read_text(encoding="utf-8"))
    victim = next(served / u.split(f"127.0.0.1:{port}/", 1)[1]
                  for u in locs if u.rstrip("/").endswith(".html"))
    assert victim.exists(), f"사이트맵이 없는 파일을 가리킨다: {victim}"
    victim.unlink()
    r = _verify(out, port)
    assert r.returncode != 0, f"404를 통과시켰다:\n{r.stdout}"
    assert "사이트맵" in r.stderr


def test_red_when_everything_returns_200(rendered):
    """모든 요청에 같은 페이지를 주는 라우팅이면 '전수 200'은 아무것도 뜻하지 않는다.

    이 검사가 없으면 위 404 테스트는 **서버가 고장 난 방향에 따라** 조용히 무력해진다.
    """
    class _Spa(_Quiet):
        """없는 주소에 index를 돌려주는 흔한 정적 호스팅 오설정."""
        def send_head(self):
            if not pathlib.Path(self.translate_path(self.path)).exists():
                self.path = "/index.html"
            return super().send_head()

    # 사이트맵 주소가 이 서버를 가리켜야 하므로 이 검사용으로 한 번 더 렌더한다.
    port = _free_port()
    tmp = pathlib.Path(tempfile.mkdtemp())
    out = tmp / "site"
    r = subprocess.run([sys.executable, "render_site.py", "--out", str(out),
                        "--base", f"http://127.0.0.1:{port}", "--ext", ".html"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    served = tmp / "live"
    shutil.copytree(out, served)
    srv = _serve(served, port, handler=_Spa)
    try:
        res = _verify(out, port)
        assert res.returncode != 0, f"없는 주소가 200인데 통과시켰다:\n{res.stdout}"
        assert "없는 주소" in res.stderr
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
