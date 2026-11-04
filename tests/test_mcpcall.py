#!/usr/bin/env python3
"""채점 호출기(mcpcall.py)가 규격 핸드셰이크를 하고, 실패를 rc=0으로 내지 않는가 (2026-09-29).

계기(T-2026W40-66 · codex 지적): mcpcall.py는 initialize도 `Mcp-Session-Id`도 없이 `tools/call`을
생짜로 던졌다. 세션을 요구하는 서버(실측 mcp.finlab.finance)는 HTTP 400을 주는데 rc=0이었다 —
채점 서브에이전트가 그 오류문을 '서버의 답'으로 읽으면 **우리 호출 실패가 남의 서버 오답으로
게시된다.** 두드리개(measure.py)는 2026-09-03에 같은 결함을 고쳤는데 호출기만 남아 있었다.

바깥을 두드리지 않는다 — 전송은 test_mcp_probe.py의 목을 그대로 쓴다.

실행: python3 -m pytest tests/test_mcpcall.py -q
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import mcpcall  # noqa: E402
from test_mcp_probe import INIT_RESULT, TOOLS, FakeResponse, http_error, install, rpc_ok  # noqa: E402


def session_server(tool_result):
    """세션을 요구하는 규격 서버 — 핸드셰이크 없이 오면 400(finlab 실측 본문)."""
    def handler(c):
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            return FakeResponse(200, json.dumps({"jsonrpc": "2.0", "id": 1, "result": INIT_RESULT}).encode(),
                                {"Content-Type": "application/json", "Mcp-Session-Id": "SID-7"})
        if c["headers"].get("mcp-session-id") != "SID-7":
            raise http_error(c["url"], 400, body=b'{"error":{"code":-32000,"message":"Bad Request: '
                                                 b'Mcp-Session-Id header is required"}}')
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        if m == "tools/list":
            return rpc_ok(c["body"]["id"], {"tools": TOOLS})
        # SSE로, 결과 앞에 진행 통지를 끼워 보낸다 — id가 맞는 응답을 골라야 한다
        body = ("event: message\ndata: " + json.dumps({"jsonrpc": "2.0", "method": "notifications/progress",
                                                       "params": {}}) + "\n\n"
                "event: message\ndata: " + json.dumps({"jsonrpc": "2.0", "id": c["body"]["id"],
                                                       "result": tool_result}) + "\n\n")
        return FakeResponse(200, body.encode(), {"Content-Type": "text/event-stream"})
    return handler


def run(monkeypatch, capsys, argv):
    monkeypatch.setattr(sys, "argv", ["mcpcall.py", *argv])
    rc = mcpcall.main()
    out = capsys.readouterr()
    return rc, out.out, out.err


def test_call_does_handshake_and_carries_session(monkeypatch, capsys):
    rec = install(monkeypatch, session_server({"content": [{"type": "text", "text": "답 42"}]}))
    rc, out, _ = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", '{"a": 1}'])
    assert rc == 0 and out.strip() == "답 42"
    assert rec.methods == ["initialize", "notifications/initialized", "tools/call"]
    assert rec.calls[-1]["headers"].get("mcp-session-id") == "SID-7"
    assert rec.calls[-1]["body"]["params"] == {"name": "t1", "arguments": {"a": 1}}


def test_list_does_handshake(monkeypatch, capsys):
    install(monkeypatch, session_server({}))
    rc, out, _ = run(monkeypatch, capsys, ["list", "https://x.test/mcp"])
    assert rc == 0 and out.startswith("t1\t")


@pytest.mark.parametrize("argv", [["call", "https://x.test/mcp", "t1", "{}"], ["list", "https://x.test/mcp"]])
def test_http_failure_is_nonzero(monkeypatch, capsys, argv):
    """우리 호출이 실패하면 rc≠0 — 오류문을 서버의 답으로 내보내지 않는다(stdout 비움)."""
    def handler(c):
        raise http_error(c["url"], 400, body=b"Mcp-Session-Id header is required")
    install(monkeypatch, handler)
    rc, out, err = run(monkeypatch, capsys, argv)
    assert rc == mcpcall.RC_TRANSPORT
    assert out == "" and "HTTP 400" in err


def test_jsonrpc_error_is_nonzero(monkeypatch, capsys):
    def handler(c):
        m = (c["body"] or {}).get("method")
        if m == "initialize":
            return rpc_ok(1, INIT_RESULT)
        if m == "notifications/initialized":
            return FakeResponse(202, b"")
        return FakeResponse(200, json.dumps({"jsonrpc": "2.0", "id": c["body"]["id"],
                                             "error": {"code": -32602, "message": "bad"}}).encode())
    install(monkeypatch, handler)
    rc, out, err = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", "{}"])
    assert rc == mcpcall.RC_TRANSPORT and out == "" and "-32602" in err


def test_tool_is_error_is_nonzero_but_text_shown(monkeypatch, capsys):
    install(monkeypatch, session_server({"isError": True, "content": [{"type": "text", "text": "없는 종목"}]}))
    rc, out, _ = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", "{}"])
    assert rc == mcpcall.RC_TOOL_ERROR and "없는 종목" in out


def test_handshake_gets_the_call_timeout(monkeypatch, capsys):
    """핸드셰이크도 종전 호출 허용(40초)을 쓴다 — measure 기본 15초로 줄이면 느린 서버가 호출 실패로 오판된다."""
    rec = install(monkeypatch, session_server({"content": [{"type": "text", "text": "ok"}]}))
    seen = []
    orig = rec.__call__
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: (seen.append(timeout), orig(req, timeout))[1])
    rc, _, _ = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", "{}"])
    assert rc == 0 and seen and all(t == mcpcall.CALL_TIMEOUT for t in seen), seen


# ── 상대 응답 절단(2026-11-04, IN-0b3d6746717d) ─────────────────────────────────────────
# 실측: emceeKim/korea-finance-mcp는 tools/list는 답하고 tools/call만 HTTP 200 머리 뒤 청크 스트림을
# 끝맺지 않고 끊는다(HTTP/1.1 = IncompleteRead(0 bytes read) · HTTP/2 = stream INTERNAL_ERROR).
# 종전엔 예외가 새어 호출기가 트레이스백으로 죽었고(rc=1 — 하필 '도구 isError'와 같은 값이다)
# 2026-11-03 월간 채점에 '우리 호출 실패'로 적혔다. 받은 조각을 살려 읽고, 못 읽으면 원인을
# '상대 응답 절단'으로 갈라 rc=4로 낸다.

class TruncatedResponse(FakeResponse):
    """read()가 받은 조각을 담은 IncompleteRead를 올리는 응답 — 청크 스트림 도중 끊김의 대역."""

    def __init__(self, partial: bytes, headers=None):
        super().__init__(200, b"", headers or {"Content-Type": "text/event-stream"})
        self._partial = partial

    def read(self, *a):
        import http.client
        raise http.client.IncompleteRead(self._partial)


def truncating_server(partial: bytes):
    base = session_server({})

    def handler(c):
        if (c["body"] or {}).get("method") == "tools/call":
            return TruncatedResponse(partial)
        return base(c)
    return handler


def test_peer_truncation_with_readable_partial_is_used_and_disclosed(monkeypatch, capsys):
    """끊겼어도 조각 안에 id가 맞는 응답이 온전히 있으면 그것을 쓰고, 절단을 공시한다."""
    msg = json.dumps({"jsonrpc": "2.0", "id": 2,
                      "result": {"content": [{"type": "text", "text": "삼성전자 00126380"}]}})
    partial = ("event: message\ndata: " + msg + "\n\n").encode()
    install(monkeypatch, truncating_server(partial))
    rc, out, err = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", "{}"])
    assert rc == mcpcall.RC_OK and out.strip() == "삼성전자 00126380"
    assert "응답 절단 후 부분 수신" in err and f"{len(partial)}바이트" in err


@pytest.mark.parametrize("partial", [b"", b'event: message\ndata: {"jsonrpc":"2.0","id":2,"resu'])
def test_peer_truncation_unreadable_is_peer_cause_not_ours(monkeypatch, capsys, partial):
    """조각으로 못 읽으면 rc=4(상대 응답 절단) — 우리 호출 실패(3)도 도구 오류(1)도 아니고, stdout은 비운다."""
    install(monkeypatch, truncating_server(partial))
    rc, out, err = run(monkeypatch, capsys, ["call", "https://x.test/mcp", "t1", "{}"])
    assert rc == mcpcall.RC_PEER_TRUNCATED == 4
    assert out == "" and "상대 응답 절단" in err and f"{len(partial)}바이트" in err


def test_measure_request_keeps_partial_instead_of_raising(monkeypatch):
    """두드리개 전송층이 IncompleteRead를 예외로 흘리지 않고 부분 수신을 값으로 공시한다."""
    import measure
    install(monkeypatch, lambda c: TruncatedResponse(b"data: {}\n"))
    r = measure._request("https://x.test/mcp", body=b"{}")
    assert r["status"] == 200 and r["raw"] == "data: {}\n"
    assert r["body_incomplete"]["received_bytes"] == 9
