#!/usr/bin/env python3
"""두드리개가 MCP 규격을 지키는가 — 그리고 못 본 것을 사망으로 적지 않는가.

계기(2026-09-03, T-2026W35-119 · fresh-eyes 검수 2026-08-29). 우리 두드리개는 세션도
열지 않고 `tools/list`를 생짜로 던졌고, 307을 안 따라갔고, SSE 전송을 몰랐고, 4xx를
즉시 사망으로 판정했다. 그래서 **살아 있는 남의 서버 여러 건이 우리 공개 목록의
'응답 없음' 명단에 올라 있었다.** 실측: 그 명단에서 HTTP 코드를 돌려준 23건을 고친
두드리개로 다시 두드리니 12건이 도구 목록까지 정상 응답했다.

이건 남의 제품에 대한 대외 공시라 오판 비용이 우리 쪽 비용보다 크고, 회사 기치 ②
(인식 경계 계약 — **못 봄 ≠ 없음**)의 대외판이 정확히 이 자리다. 그래서 네 결함마다
회귀를 박고, **판정 어휘가 셋으로 갈려 있는지**까지 같이 건다.

바깥을 두드리지 않는다 — 전송은 전부 목이다(외부 의존 테스트 금지).

실행: python3 -m pytest tests/test_mcp_probe.py -q
"""
import email.message
import io
import json
import pathlib
import sys
import urllib.error
import urllib.request

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import measure  # noqa: E402
import render_readme  # noqa: E402

INIT_RESULT = {"protocolVersion": "2025-06-18", "capabilities": {},
               "serverInfo": {"name": "FakeServer", "version": "1.0.0"}}
TOOLS = [{"name": "t1", "description": "x" * 30, "inputSchema": {"properties": {"a": {}}}},
         {"name": "t2", "description": "y" * 30, "inputSchema": {"properties": {"b": {}}}}]


def _msg(pairs) -> email.message.Message:
    m = email.message.Message()
    for k, v in pairs.items():
        m[k] = v
    return m


class FakeResponse(io.BytesIO):
    """urlopen이 돌려주는 것의 최소 대역 — 컨텍스트 매니저·readline 둘 다 쓴다."""

    def __init__(self, status: int, body: bytes, headers: dict | None = None):
        super().__init__(body)
        self.status = status
        self.headers = _msg(headers or {"Content-Type": "application/json"})

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
        return False


def http_error(url: str, code: int, headers: dict | None = None, body: bytes = b"") -> Exception:
    return urllib.error.HTTPError(url, code, "err", _msg(headers or {}), io.BytesIO(body))


class Recorder:
    """요청을 전부 기록하는 가짜 전송. 서버 역할은 `handler`가 한다."""

    def __init__(self, handler):
        self.handler = handler
        self.calls = []

    def __call__(self, req, timeout=None):
        body = None
        if req.data:
            try:
                body = json.loads(req.data.decode())
            except ValueError:
                body = req.data.decode("utf-8", "replace")
        call = {"url": req.full_url, "method": req.get_method(), "body": body,
                "headers": {k.lower(): v for k, v in req.header_items()}}
        self.calls.append(call)
        return self.handler(call)

    @property
    def methods(self) -> list:
        return [(c["body"] or {}).get("method") for c in self.calls
                if isinstance(c["body"], dict)]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(measure.time, "sleep", lambda *_a: None)


def install(monkeypatch, handler) -> Recorder:
    rec = Recorder(handler)
    monkeypatch.setattr(urllib.request, "urlopen", rec)
    return rec


def rpc_ok(rid, result) -> FakeResponse:
    return FakeResponse(200, json.dumps({"jsonrpc": "2.0", "id": rid,
                                         "result": result}).encode())


# ── ① initialize 핸드셰이크 ────────────────────────────────────────────────
def test_handshake_precedes_tools_list(monkeypatch):
    """**세션을 열지 않고 tools/list를 던지면 규격 준수 서버는 400을 준다.**

    실측 2026-09-03: mcp.finlab.finance가 정확히 그랬고, 우리는 그 400을 '응답 없음'으로
    공시하고 있었다. 여기 목 서버도 똑같이 군다 — 핸드셰이크를 안 하면 절대 안 살아난다.
    """
    def handler(c):
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            return rpc_ok(1, INIT_RESULT)
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        if m == "tools/list":
            if not handler.initialized:
                raise http_error(c["url"], 400, body=b'{"error":"session required"}')
            return rpc_ok(c["body"]["id"], {"tools": TOOLS})
        raise http_error(c["url"], 400)
    handler.initialized = False

    def wrapper(c):
        r = handler(c)
        if (c["body"] or {}).get("method") == "notifications/initialized":
            handler.initialized = True
        return r

    rec = install(monkeypatch, wrapper)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.LIVE, out
    assert out["tool_count"] == 2
    assert rec.methods[0] == "initialize", "initialize가 첫 요청이어야 한다"
    assert "notifications/initialized" in rec.methods, "초기화 완료 통지를 안 보냈다"
    # 규격이 요구하는 헤더가 실제로 나갔는가 — 이름만 맞고 안 보내는 일이 흔하다
    assert "text/event-stream" in rec.calls[0]["headers"]["accept"]
    assert "application/json" in rec.calls[0]["headers"]["accept"]


def test_session_id_and_protocol_version_are_carried(monkeypatch):
    """서버가 준 `Mcp-Session-Id`와 협상된 프로토콜 버전을 이어 써야 한다."""
    def handler(c):
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            return FakeResponse(200, json.dumps(
                {"jsonrpc": "2.0", "id": 1,
                 "result": {**INIT_RESULT, "protocolVersion": "2025-03-26"}}).encode(),
                {"Content-Type": "application/json", "Mcp-Session-Id": "SID-42"})
        if c["headers"].get("mcp-session-id") != "SID-42":
            raise http_error(c["url"], 400, body=b"missing session")
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        return rpc_ok(c["body"]["id"], {"tools": TOOLS})

    rec = install(monkeypatch, handler)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.LIVE, out
    assert out["protocol_version"] == "2025-03-26"
    after = [c for c in rec.calls[1:]]
    assert all(c["headers"].get("mcp-session-id") == "SID-42" for c in after)
    assert all(c["headers"].get("mcp-protocol-version") == "2025-03-26" for c in after)


# ── ② POST 307/308 추적 ────────────────────────────────────────────────────
@pytest.mark.parametrize("code", [307, 308])
def test_post_redirect_is_followed_with_method_and_body(monkeypatch, code):
    """**서버는 옮긴 자리를 알려줬는데 우리가 안 갔다.**

    파이썬 urllib은 POST에서 307·308을 안 따라간다. 실측: contract.naru.build는 308,
    dartpoint.ai는 307이었고 둘 다 우리 '응답 없음' 명단에 있었다. 리다이렉트를 따라갈 때
    method(POST)와 본문이 보존돼야 한다 — GET으로 바꾸면 POST 전용 엔드포인트에서 405다.
    """
    def handler(c):
        if c["url"] == "https://old.test/mcp":
            raise http_error(c["url"], code, {"Location": "https://new.test/mcp"})
        assert c["method"] == "POST", "리다이렉트에서 method가 GET으로 바뀌었다"
        m = (c["body"] or {}).get("method")
        assert m, "리다이렉트에서 본문이 사라졌다"
        if m == "initialize":
            return rpc_ok(1, INIT_RESULT)
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        return rpc_ok(c["body"]["id"], {"tools": TOOLS})

    install(monkeypatch, handler)
    out = measure.measure_remote("https://old.test/mcp")
    assert out["status"] == measure.LIVE, out
    assert out["tool_count"] == 2
    assert out["redirected_from"] == "https://old.test/mcp"
    assert out["url"] == "https://new.test/mcp", "이어지는 요청이 옛 주소로 갔다"


# ── ③ 구 HTTP+SSE 전송(GET) ────────────────────────────────────────────────
def test_legacy_sse_transport_is_tried_when_post_is_rejected(monkeypatch):
    """**SSE 엔드포인트가 POST에 405를 주는 것은 정상 동작이다.**

    실측: eddmpython/dartlab(.../mcp/sse)과 nokelan/health-fee-mcp가 405였고, 구 전송으로
    물어보니 각각 도구 26종·12종을 정상 공개했다. 405를 사망으로 적던 것이 우리 결함이다.
    """
    sse_head = (b"event: endpoint\ndata: /messages?sessionId=abc\n\n")
    pending = []

    def handler(c):
        if c["method"] == "GET":
            assert "text/event-stream" in c["headers"]["accept"]
            return FakeResponse(200, sse_head + b"".join(pending),
                                {"Content-Type": "text/event-stream"})
        if c["method"] == "POST" and c["url"].endswith("/mcp"):
            raise http_error(c["url"], 405, body=b"method not allowed")
        # 구 전송에서 응답은 POST 본문이 아니라 열린 GET 스트림으로 온다
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            pending.append(b"event: message\ndata: "
                           + json.dumps({"jsonrpc": "2.0", "id": 1,
                                         "result": INIT_RESULT}).encode() + b"\n\n")
        elif m == "tools/list":
            pending.append(b"event: message\ndata: "
                           + json.dumps({"jsonrpc": "2.0", "id": 2,
                                         "result": {"tools": TOOLS}}).encode() + b"\n\n")
        return FakeResponse(202, b"")

    # 스트림을 미리 채워 둔다 — 목에서는 POST 후 스트림이 다시 열리지 않으므로
    pending.append(b"event: message\ndata: "
                   + json.dumps({"jsonrpc": "2.0", "id": 1, "result": INIT_RESULT}).encode()
                   + b"\n\n")
    pending.append(b"event: message\ndata: "
                   + json.dumps({"jsonrpc": "2.0", "id": 2,
                                 "result": {"tools": TOOLS}}).encode() + b"\n\n")

    rec = install(monkeypatch, handler)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.LIVE, out
    assert out["transport"] == "sse"
    assert out["tool_count"] == 2
    assert "sse" in out["transports_tried"]
    assert any(c["method"] == "GET" for c in rec.calls), "GET(SSE)을 아예 시도하지 않았다"


# ── ④ 4xx는 사망이 아니다 ──────────────────────────────────────────────────
@pytest.mark.parametrize("code", [400, 404, 405, 406, 415])
def test_4xx_is_never_death_and_gets_a_second_transport(monkeypatch, code):
    """4xx는 **전송 방식이 틀렸다**는 신호다. 다른 전송으로 한 번 더 묻고, 그래도
    못 보면 '죽음'이 아니라 '확인 못 함'으로 적는다."""
    def handler(c):
        if c["method"] == "GET":
            raise http_error(c["url"], 405)
        raise http_error(c["url"], code, body=b'{"error":"nope"}')

    rec = install(monkeypatch, handler)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.UNVERIFIED, out
    assert out["status"] != measure.DOWN, "4xx를 사망으로 판정했다"
    assert out["status_label"] == "확인 못 함"
    assert "sse" in out["transports_tried"], "4xx인데 다른 전송을 안 시도했다"
    assert any(c["method"] == "GET" for c in rec.calls)
    # 그쪽 해명을 버리지 않는다
    assert "nope" in (out.get("error_body") or "")


def test_5xx_is_unverified_not_death(monkeypatch):
    """실측: onrender.com 3건이 503이었고 재시도에서 전부 도구 목록을 줬다."""
    state = {"n": 0}

    def handler(c):
        state["n"] += 1
        if state["n"] == 1:
            raise http_error(c["url"], 503)
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            return rpc_ok(1, INIT_RESULT)
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        return rpc_ok(c["body"]["id"], {"tools": TOOLS})

    install(monkeypatch, handler)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.LIVE, out
    assert out["retried"] is True


def test_auth_wall_is_proof_of_life(monkeypatch):
    """401/403은 **살아있음의 증거**다 — 키가 없어 도구 목록을 못 볼 뿐이다."""
    def handler(c):
        raise http_error(c["url"], 401)

    install(monkeypatch, handler)
    out = measure.measure_remote("https://example.test/mcp")
    assert out["status"] == measure.LIVE
    assert out["needs_key"] is True
    assert out["tool_count"] is None


# ── 판정 어휘 세 갈래 ──────────────────────────────────────────────────────
def test_only_host_absence_earns_the_word_death(monkeypatch):
    """'죽음 확인'은 DNS 미해결·연결 거부에만 붙는다. 타임아웃·TLS 오류는 '확인 못 함'이다."""
    def dns(_c):
        raise urllib.error.URLError("[Errno -2] Name or service not known")

    install(monkeypatch, dns)
    out = measure.measure_remote("https://gone.test/mcp")
    assert out["status"] == measure.DOWN, out
    assert out["status_label"] == "죽음 확인"

    def tls(_c):
        raise urllib.error.URLError("[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred")

    install(monkeypatch, tls)
    out = measure.measure_remote("https://tls.test/mcp")
    assert out["status"] == measure.UNVERIFIED, "TLS 오류를 사망으로 판정했다"

    def slow(_c):
        raise TimeoutError("timed out")

    install(monkeypatch, slow)
    out = measure.measure_remote("https://slow.test/mcp")
    assert out["status"] == measure.UNVERIFIED, "타임아웃을 사망으로 판정했다"


def test_status_vocabulary_is_three_way_everywhere():
    """어휘가 측정기와 산출물에서 갈리면 화면 문구만 고친 것이 된다."""
    assert set(measure.STATUS_LABEL) == {"live", "unverified", "down"}
    assert measure.STATUS_LABEL == render_readme.STATUS_LABEL
    assert measure.STATUS_LABEL["unverified"] == "확인 못 함"


def test_renderer_reads_the_three_way_verdict():
    """옛 회차 원자료(`status` 없음)도 세 갈래로 읽혀야 한다 — 그래야 재생성이 안 깨진다."""
    live = {"remote": {"reachable": True, "status": "live"}}
    unver = {"remote": {"reachable": False, "http": 400, "why": "HTTP 400"}}
    dead = {"remote": {"reachable": False,
                       "why": "URLError: [Errno -2] Name or service not known"}}
    assert render_readme.status_of(live) == "live"
    assert render_readme.status_of(unver) == "unverified"
    assert render_readme.status_of(dead) == "down"


def test_published_wording_never_calls_unverified_dead(tmp_path, monkeypatch):
    """**산출물 문구까지 건다.** 측정기만 고치고 화면이 '응답 없음'이면 대외 공시는 그대로다."""
    dead = [
        {"name": "a/unverified", "repo_url": "https://github.com/a/unverified",
         "addr_registered": True,
         "remote": {"url": "https://a.test/mcp", "http": 400, "reachable": False,
                    "status": "unverified", "why": "HTTP 400"}},
        {"name": "b/gone", "repo_url": "https://github.com/b/gone",
         "addr_registered": False,
         "remote": {"url": "https://b.test/mcp", "reachable": False, "status": "down",
                    "why": "DNS에 그 이름이 없다 — 호스트가 사라졌다"}},
    ]
    monkeypatch.chdir(tmp_path)
    render_readme.write_down(dead, "2026-09-03")
    md = (tmp_path / "DOWN.md").read_text(encoding="utf-8")
    assert "# 응답하지 않는 서버" not in md, "여전히 '응답하지 않는 서버'로 게시한다"
    assert "확인 못 함" in md and "죽음 확인" in md
    assert "사망 명단이 아니다" in md
    # 확인 못 함 줄이 사망 절에 실리면 안 된다
    unver_at = md.index("a/unverified")
    down_at = md.index("b/gone")
    death_head = md.index("## 죽음 확인")
    assert down_at > death_head
    assert unver_at > md.index("## 확인 못 함 — 등록된 주소")


def test_axis_is_pre_registered_in_protocol():
    """새 축 `status`를 사전공개 없이 게시하면 신뢰 규약 ①을 어긴 것이다."""
    root = pathlib.Path(__file__).resolve().parent.parent
    proto = (root / "PROTOCOL.md").read_text(encoding="utf-8")
    assert "`status`" in proto
    assert "2026-09-03" in proto, "축을 바꿔 놓고 개정 이력에 안 적었다"
