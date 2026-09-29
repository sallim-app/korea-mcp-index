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
