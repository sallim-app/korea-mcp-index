#!/usr/bin/env python3
"""후보 MCP를 실제로 두드려 판정값을 만든다 (2026-08-18, D-2026W34-21/22).

**목록이 못 하는 일이 이것 하나다.** 남의 목록은 "있다"만 말한다. 우리는 "지금 되냐"를 잰다.
실측 계기: 대표 한국 목록 57개 중 살아있는 것이 23개(40%)뿐인데 목록은 그걸 표시하지 않았다.

재는 것 (D-2026W34-22 신뢰 규약 — 결과 보기 전에 고정, 사후 변경 금지):
  reachable    원격 서버에 JSON-RPC `tools/list`를 실제로 보낸다. 200이면 살아 있다.
  tool_count   응답에 도구가 몇 개 들어 있나. 0개면 껍데기다.
  latency_ms   그 한 번의 왕복. 리랭커에서 배웠듯 느린 의존은 없느니만 못하다.
  needs_key    키 없이 되는가. **우리가 지는 항목이 아니라 이기는 항목이라 더 조심해서 잰다.**
  installable  패키지가 실제로 배포돼 있나(npm/PyPI). 저장소만 있고 설치 못 하는 것이 많다.
  alive        저장소 최종 푸시·archived.

**우리가 불리한 항목도 같이 싣는다**(D-2026W34-22 ②): self_hostable — 원격 전용인 우리
서버는 여기서 진다. 유리한 축만 재면 그 순위는 광고지 판정이 아니다.

예의: 서버당 `tools/list` 1회, 사이에 간격을 두고, User-Agent로 우리를 밝힌다. 남의 서버를
두드리는 일이니 정체를 숨기지 않는다(기치 3절 상생).

실행: python3 measure.py [--limit N]
"""
import argparse
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; measuring MCP availability)"
TIMEOUT = 15
MAX_BODY = 8 * 1024 * 1024   # 폭주 방어 상한. 걸리면 숨기지 않고 공시한다.
PAUSE = 1.0


def _post_jsonrpc(url: str, method: str) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": {}}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": UA})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            # **자르지 않는다.** 20,000자로 자르던 초판은 도구 설명이 긴 서버(우리 것 포함)의
            # JSON을 반토막 내고 파싱에 실패해 "도구 ?개"로 보고했다 — 우리가 제품에서 금지하는
            # 조용한 절단을 측정기가 저지른 것이다(2026-08-18, 우리 서버 대조로 발견).
            # 상한은 폭주 방어용으로만 두고, 걸리면 값으로 공시한다.
            raw = r.read(MAX_BODY + 1).decode("utf-8", "replace")
            return {"status": r.status, "ms": int((time.monotonic() - t0) * 1000),
                    "raw": raw, "body_truncated": len(raw) > MAX_BODY}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ms": int((time.monotonic() - t0) * 1000),
                "raw": e.read().decode("utf-8", "replace")[:800]}
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return {"status": None, "ms": int((time.monotonic() - t0) * 1000),
                "error": f"{type(e).__name__}: {e}"[:120]}


def _tools_from(raw: str) -> int | None:
    """SSE(`data: {...}`)와 순수 JSON 둘 다 받는다."""
    for chunk in ([raw] + [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]):
        try:
            d = json.loads(chunk)
        except (ValueError, TypeError):
            continue
        tools = ((d.get("result") or {}).get("tools"))
        if isinstance(tools, list):
            return len(tools)
    return None


def measure_remote(url: str) -> dict:
    r = _post_jsonrpc(url, "tools/list")
    out = {"url": url, "http": r.get("status"), "latency_ms": r["ms"]}
    if "error" in r:
        return {**out, "reachable": False, "why": r["error"]}
    if r["status"] in (401, 403):
        return {**out, "reachable": True, "needs_key": True, "tool_count": None,
                "why": "인증 필요 — 키 없이는 도구 목록도 못 본다"}
    if r["status"] != 200:
        return {**out, "reachable": False, "why": f"HTTP {r['status']}"}
    n = _tools_from(r["raw"])
    if n is None:
        why = ("응답이 상한을 넘어 잘렸다 — 도구 수 미확인(측정기 한계, 서버 문제 아님)"
               if r.get("body_truncated") else "200이지만 tools/list 응답을 못 읽었다 — 규격 이탈 의심")
        return {**out, "reachable": True, "needs_key": False, "tool_count": None, "why": why}
    return {**out, "reachable": True, "needs_key": False, "tool_count": n,
            "why": "" if n else "도구 0개 — 껍데기"}


def measure_package(p: dict) -> dict:
    kind, ident = (p.get("type") or "").lower(), p.get("id") or ""
    if not ident:
        return {"type": kind, "installable": None, "why": "식별자 없음"}
    url = (f"https://registry.npmjs.org/{urllib.parse.quote(ident, safe='@')}" if kind == "npm"
           else f"https://pypi.org/pypi/{ident}/json" if kind in ("pypi", "python") else None)
    if not url:
        return {"type": kind, "id": ident, "installable": None, "why": f"조회 경로 없음({kind})"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            json.load(r)
        return {"type": kind, "id": ident, "installable": True}
    except urllib.error.HTTPError as e:
        return {"type": kind, "id": ident, "installable": e.code != 404,
                "why": "레지스트리에 없다(설치 불가)" if e.code == 404 else f"HTTP {e.code}"}
    except Exception as e:
        return {"type": kind, "id": ident, "installable": None, "why": f"미확인 {type(e).__name__}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bucket", default="keep")
    a = ap.parse_args()

    src = json.load(open("candidates_filtered.json", encoding="utf-8"))
    items = [i for i in src["items"] if i["verdict"] == a.bucket]
    if a.limit:
        items = items[:a.limit]

    out, notes = [], []
    for i, it in enumerate(items, 1):
        rec = {"name": it["name"], "repo_url": it.get("repo_url", ""),
               "stars": it.get("stars"), "pushed": it.get("pushed"),
               "archived": it.get("archived"), "sources": it["sources"]}
        remotes = it.get("remotes") or []
        rec["remote"] = measure_remote(remotes[0]["url"]) if remotes and remotes[0].get("url") else None
        if remotes and remotes[0].get("url"):
            time.sleep(PAUSE)
        pkgs = it.get("packages") or []
        rec["package"] = measure_package(pkgs[0]) if pkgs else None
        # 우리가 지는 항목 — 원격 전용은 셀프호스팅 불가
        rec["self_hostable"] = bool(pkgs) or None
        if rec["remote"] is None and rec["package"] is None:
            notes.append(f"{it['name']}: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)")
        out.append(rec)
        if i % 10 == 0:
            print(f"  … {i}/{len(items)}")

    json.dump({"measured": len(out), "unmeasurable": len(notes), "boundaries": notes,
               "criteria_note": "항목은 D-2026W34-22로 결과 보기 전에 고정됐다. 사후 변경 금지.",
               "items": out}, open("measured.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    live = [r for r in out if (r.get("remote") or {}).get("reachable")]
    keyed = [r for r in live if (r.get("remote") or {}).get("needs_key")]
    print(f"\n측정 {len(out)}건 · 원격 응답 {len(live)}건 · 그중 키 필요 {len(keyed)}건")
    print(f"측정 불가 {len(notes)}건 (원격 주소도 패키지도 없음 — 0건이 아니라 미확인)")
    print("\n■ 실제로 응답한 서버 (키 없이 되는 것 우선)")
    for r in sorted(live, key=lambda x: (x["remote"].get("needs_key") or False,
                                         -(x["remote"].get("tool_count") or 0)))[:15]:
        rm = r["remote"]
        key = "키필요" if rm.get("needs_key") else "무인증"
        print(f"  {key}  도구{str(rm.get('tool_count') or '?'):>4}개  {rm['latency_ms']:>5}ms  {r['name'][:40]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
