#!/usr/bin/env python3
"""MCP 서버에 도구 목록을 묻거나 도구를 부르는 최소 CLI.

**왜 CLI인가**: 답변 품질 평가는 서브에이전트가 *실제 AI 클라이언트처럼* 도구를 골라
부르면서 질문에 답하는 방식이다(2026-08-19 사장님: "그냥 mcp 호출해서 질문에 잘 응답하는지
답변을 기록해놓고 그 답변이 정확한지 평가하면 되는 거 아냐"). 서브에이전트가 매번 JSON-RPC를
손으로 짜면 실수가 섞이므로 호출 경로를 하나로 고정한다.

사용:
  mcpcall.py list <url>
  mcpcall.py call <url> <tool> '<json arguments>'
"""
import json
import sys
import urllib.error
import urllib.request

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; answer-quality evaluation)"


def rpc(url: str, method: str, params: dict) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read(3_000_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode("utf-8", "replace")[:600]}
    except Exception as e:
        return {"error": type(e).__name__}
    for c in [raw] + [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]:
        try:
            d = json.loads(c)
        except (ValueError, TypeError):
            continue
        if "result" in d or "error" in d:
            return d
    return {"error": "unparsable", "body": raw[:400]}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, url = sys.argv[1], sys.argv[2]
    if cmd == "list":
        d = rpc(url, "tools/list", {})
        tools = (d.get("result") or {}).get("tools") or []
        for t in tools:
            req = (t.get("inputSchema") or {}).get("required") or []
            print(f"{t['name']}\t필수={','.join(req) or '-'}\t{(t.get('description') or '')[:150]}")
        if not tools:
            print(json.dumps(d, ensure_ascii=False)[:400])
        return 0
    args = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    d = rpc(url, "tools/call", {"name": sys.argv[3], "arguments": args})
    res = d.get("result") or {}
    texts = [b.get("text", "") for b in (res.get("content") or []) if isinstance(b, dict)]
    print("\n".join(texts) if texts else json.dumps(d, ensure_ascii=False)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
