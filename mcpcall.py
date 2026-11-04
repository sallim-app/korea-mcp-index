#!/usr/bin/env python3
"""MCP 서버에 도구 목록을 묻거나 도구를 부르는 최소 CLI.

**왜 CLI인가**: 답변 품질 평가는 서브에이전트가 *실제 AI 클라이언트처럼* 도구를 골라
부르면서 질문에 답하는 방식이다(2026-08-19 사장님: "그냥 mcp 호출해서 질문에 잘 응답하는지
답변을 기록해놓고 그 답변이 정확한지 평가하면 되는 거 아냐"). 서브에이전트가 매번 JSON-RPC를
손으로 짜면 실수가 섞이므로 호출 경로를 하나로 고정한다.

사용:
  mcpcall.py list <url>
  mcpcall.py call <url> <tool> '<json arguments>'

종료 코드: 0=응답 받음 · 1=도구가 isError로 답함 · 2=사용법 오류 · 3=우리 호출 실패
(핸드셰이크·HTTP·JSON-RPC 오류 — **서버의 답이 아니므로 오답으로 채점하지 마라**) ·
4=상대 응답 절단(서버가 200을 보내고 본문 도중에 끊었고, 받은 조각으로는 응답을 못 읽었다 —
역시 오답이 아니라 '측정 못 함'이다). 절단됐어도 받은 조각에서 응답을 읽었으면 rc는 0/1이고
stderr에 `[mcpcall] 응답 절단 후 부분 수신`을 공시한다.
"""
import json
import sys

import measure

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; answer-quality evaluation)"
CALL_TIMEOUT = 40

# 종료 코드. **실패를 rc=0으로 내지 않는다** — 채점 서브에이전트가 rc만 보고 "도구가 이렇게
# 답했다"로 적으면 우리 호출 실패가 남의 서버 오답으로 게시된다(2026-09-29 codex 지적:
# 세션을 요구하는 서버는 HTTP 400인데 rc=0이었다).
RC_OK = 0
RC_TOOL_ERROR = 1      # 도구가 isError로 답했다 — 서버 응답은 받았다
RC_USAGE = 2
RC_TRANSPORT = 3       # 우리 호출이 실패했다(핸드셰이크·HTTP·JSON-RPC) — 서버 답이 아니다
RC_PEER_TRUNCATED = 4  # 상대가 200 뒤 본문 도중에 끊었고 받은 조각으로는 못 읽었다 — 서버 답이 아니다


def _reply(raw: str, rid: int) -> dict | None:
    """SSE·순수 JSON 어느 쪽이든 `id`가 맞는 응답 메시지. 중간 통지는 건너뛴다."""
    for d in measure._rpc_messages(raw):
        if d.get("id") == rid and ("result" in d or "error" in d):
            return d
    return None


def rpc(url: str, method: str, params: dict) -> dict:
    """**measure.py와 같은 규격 핸드셰이크**(initialize → notifications/initialized → 세션
    헤더 유지 · POST 리다이렉트 추적)를 거쳐 메서드 하나를 부른다.

    종전엔 세션 없이 생짜로 던졌다 — 두드리개(measure.py)가 2026-09-03에 고친 결함을 호출기가
    그대로 안고 있었다. 실패는 `{"error": ...}`로, 성공은 JSON-RPC 응답 그대로 돌려준다.
    """
    measure.UA = UA   # 두드리개와 같은 전송을 쓰되 남의 서버 로그엔 용도를 바로 적는다
    sess, r0 = measure._handshake(url, timeout=CALL_TIMEOUT)  # 종전 40초 허용을 핸드셰이크에도
    if sess is None:
        st = r0.get("status")
        why = r0.get("error") or (f"HTTP {st}" if st else "응답 없음")
        return {"error": f"initialize 실패: {why}", "body": (r0.get("raw") or "")[:600]}
    r = measure._jsonrpc(sess["endpoint"],
                         {"jsonrpc": "2.0", "id": 2, "method": method, "params": params},
                         session=sess["session_id"], protocol=sess["protocol"],
                         timeout=CALL_TIMEOUT)
    raw = r.get("raw") or ""
    if r.get("status") != 200:
        why = r.get("error") or f"HTTP {r.get('status')}"
        return {"error": f"{method} 실패: {why}", "body": raw[:600]}
    d = _reply(raw, 2)
    inc = r.get("body_incomplete")
    if d is None:
        if inc:
            # 우리 호출 실패가 아니라 상대 응답 절단이다 — 원인을 갈라 적는다(못 봄 ≠ 없음)
            return {"error": f"{method} 상대 응답 절단: HTTP 200 뒤 본문이 "
                             f"{inc['received_bytes']}바이트에서 끊겼고 그 조각으로는 응답을 읽지 못했다",
                    "peer_truncated": inc, "body": raw[:400]}
        return {"error": f"{method} 응답을 읽지 못했다", "body": raw[:400]}
    if inc:
        d["_incomplete"] = inc
    if r.get("body_truncated"):
        d["_truncated"] = True
    return d


def _fail(d: dict) -> int:
    print(json.dumps(d, ensure_ascii=False)[:3000], file=sys.stderr)
    return RC_PEER_TRUNCATED if d.get("peer_truncated") else RC_TRANSPORT


def _disclose_incomplete(d: dict) -> None:
    inc = d.get("_incomplete")
    if inc:
        print(f"[mcpcall] 응답 절단 후 부분 수신 — 상대가 HTTP 200 뒤 본문 도중에 끊었다"
              f"({inc['received_bytes']}바이트 수신). 받은 조각에서 응답 메시지는 읽었으나 "
              f"그 뒤에 무엇이 더 왔을지는 미확인", file=sys.stderr)


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] not in ("list", "call") or (
            sys.argv[1] == "call" and len(sys.argv) < 4):
        print(__doc__)
        return RC_USAGE
    cmd, url = sys.argv[1], sys.argv[2]
    if cmd == "list":
        d = rpc(url, "tools/list", {})
        tools = (d.get("result") or {}).get("tools")
        if not isinstance(tools, list):
            return _fail(d)
        for t in tools:
            req = (t.get("inputSchema") or {}).get("required") or []
            print(f"{t['name']}\t필수={','.join(req) or '-'}\t{(t.get('description') or '')[:150]}")
        if not tools:
            print("(도구 0개)")
        _disclose_incomplete(d)
        return RC_OK
    try:
        args = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    except ValueError as e:
        print(f"인자 JSON을 못 읽었다: {e}", file=sys.stderr)
        return RC_USAGE
    d = rpc(url, "tools/call", {"name": sys.argv[3], "arguments": args})
    res = d.get("result")
    if not isinstance(res, dict):
        return _fail(d)
    texts = [b.get("text", "") for b in (res.get("content") or []) if isinstance(b, dict)]
    print("\n".join(texts) if texts else json.dumps(res, ensure_ascii=False)[:3000])
    if d.get("_truncated"):
        print("[mcpcall] 응답이 측정기 상한을 넘어 잘렸다 — 뒷부분 미확인", file=sys.stderr)
    _disclose_incomplete(d)
    return RC_TOOL_ERROR if res.get("isError") else RC_OK


if __name__ == "__main__":
    raise SystemExit(main())
