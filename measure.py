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
import collections
import json
import re
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


def tool_specs(tools: list) -> list:
    """호출에 필요한 최소 스키마만 남긴다.

    지금까지 tools 배열을 받아 집계(_tool_quality)만 내고 **버렸다**. 그래서 "도구 47종"까지
    재놓고 정작 그 도구를 부를 수 없었다 — 어떤 인자가 필요한지 모르니까(2026-08-19).
    설명 본문은 크므로 뺀다. 필요한 것은 이름·필수 인자·읽기전용 여부 셋이다.
    """
    out = []
    for t in tools:
        sch = t.get("inputSchema") or {}
        ann = t.get("annotations") or {}
        out.append({"name": t.get("name"),
                    "required": list(sch.get("required") or []),
                    "props": list((sch.get("properties") or {}).keys())[:12],
                    "read_only": bool(ann.get("readOnlyHint"))})
    return out


def _tool_quality(tools: list) -> dict:
    """**도메인 지식 없이 잴 수 있는 품질** — 기치 ②(인식 경계 계약)의 측정 가능한 부분.

    "좋은 서버인가"에서 **도메인 정확성은 우리가 전 분야에서 판정할 수 없다.** 부동산·
    공공계약은 정답을 알지만 의료·교통은 모른다. 모르면서 점수를 매기면 우리가 경계하는
    '그럴듯한 요약'을 우리가 생산하는 것이다. 그래서 그건 재지 않고 그렇다고 공시한다.

    대신 **분야와 무관하게** 잴 수 있는 것이 있다: 이 서버가 자기를 LLM에게 제대로
    설명하는가. 설명이 없거나 스키마가 없으면 모델은 그 도구를 언제 어떻게 쓸지 모르고,
    그러면 데이터가 아무리 정확해도 답에 도달하지 못한다. 어노테이션(readOnlyHint 등)이
    없으면 클라이언트가 안전하게 다룰 수 없다(비대화 codex가 자동 취소하는 실측 사례가 있다).

    전부 `tools/list` 한 번에 이미 들어 있는 값이다 — 남의 서버에 추가 부담을 주지 않는다.
    """
    n = len(tools)
    if not n:
        return {}
    # **남의 서버 하나가 규격을 어겨도 전체 측정이 죽으면 안 된다**(codex 교차검증 2026-08-19).
    # tools 원소가 dict가 아닌 서버가 하나만 있어도 여기서 AttributeError로 233건이 통째로
    # 중단됐다. 걸러내되 **몇 개를 걸렀는지 값으로 공시한다** — 조용히 줄이면 우리가 제품에서
    # 금지하는 그 절단이다.
    bad = [t for t in tools if not isinstance(t, dict)]
    tools = [t for t in tools if isinstance(t, dict)]
    if not tools:
        return {"malformed": len(bad), "note": "도구 항목이 전부 규격 이탈이라 품질을 못 쟀다"}
    n = len(tools)
    desc = sorted(len(t.get("description") or "") for t in tools)

    def pct(f) -> int:
        return round(100 * sum(1 for t in tools if f(t)) / n)

    return {
        **({"malformed": len(bad)} if bad else {}),   # 조용히 줄이지 않는다 — 걸렀으면 공시한다
        "described_pct": pct(lambda t: len(t.get("description") or "") >= 20),
        "desc_median": desc[n // 2],
        "input_schema_pct": pct(lambda t: ((t.get("inputSchema") or {}).get("properties"))),
        "output_schema_pct": pct(lambda t: t.get("outputSchema")),
        "annotated_pct": pct(lambda t: t.get("annotations")),
        "readonly_pct": pct(lambda t: (t.get("annotations") or {}).get("readOnlyHint")),
    }


def _tools_from(raw: str) -> list | None:
    """SSE(`data: {...}`)와 순수 JSON 둘 다 받는다. **목록을 그대로 돌려준다** —
    개수만 세고 버리면 품질 지표를 다시 받으러 가야 한다(남의 서버에 두 번 묻는 셈)."""
    for chunk in ([raw] + [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]):
        try:
            d = json.loads(chunk)
        except (ValueError, TypeError):
            continue
        tools = ((d.get("result") or {}).get("tools"))
        if isinstance(tools, list):
            return tools
    return None


def measure_remote(url: str) -> dict:
    """한 번만 재면 콜드 스타트를 재게 된다.

    실측 2026-08-18: `gateway.pipeworx.io/dart-kr`가 1회 측정에서 2,057ms였는데
    연달아 부르니 57ms였다(36배). 서버리스(Workers·Render)는 첫 호출이 기동 시간을
    포함하므로 1회 값으로 순위를 매기면 **느린 서버가 아니라 안 쓰이는 서버**를 벌주게 된다.
    그렇다고 콜드를 버리면 안 된다 — 처음 붙는 사용자에겐 그게 실제 체감이다.
    그래서 **둘 다 싣는다**: cold_ms(첫 호출) · warm_ms(이후 최소).

    측정 지점 편향도 확인했다(사장님 지적): 우리 서버를 우리 서버에서 재면 유리하지 않냐 —
    naru·quant 두 지점 대조 결과 우리 서버 79ms vs 64ms로 **오히려 quant가 빨랐다**.
    다만 두 지점 다 우리 것이고 같은 클라우드라 **국외 지점 편향은 여전히 미확인**이다.
    """
    r = _post_jsonrpc(url, "tools/list")
    # **1회 실패로 남의 서버를 죽었다고 공표하지 않는다.** 실측 2026-08-18: mydart가
    # 15초 타임아웃으로 무응답 판정됐는데 직후 재시도에서 208ms로 정상이었다. 이 목록의
    # "무응답" 줄은 남의 제품에 대한 공개 주장이므로 오판 비용이 우리 쪽 비용보다 크다.
    retried = False
    if r.get("status") is None or (r.get("status") or 0) >= 500:
        time.sleep(3)
        r2 = _post_jsonrpc(url, "tools/list")
        retried = True
        if r2.get("status") == 200 or ("error" not in r2 and r.get("status") is None):
            r = r2
    out = {"url": url, "http": r.get("status"), "cold_ms": r["ms"], "latency_ms": r["ms"],
           "retried": retried}
    if r.get("status") == 200:
        warm = []
        for _ in range(2):
            time.sleep(0.4)
            w = _post_jsonrpc(url, "tools/list")
            if w.get("status") == 200:
                warm.append(w["ms"])
        if warm:
            out["warm_ms"] = min(warm)
            out["latency_ms"] = min(warm)
    if "error" in r:
        return {**out, "reachable": False, "why": r["error"]}
    if r["status"] in (401, 403):
        return {**out, "reachable": True, "needs_key": True, "tool_count": None,
                "why": "인증 필요 — 키 없이는 도구 목록도 못 본다"}
    if r["status"] != 200:
        return {**out, "reachable": False, "why": f"HTTP {r['status']}"}
    tools = _tools_from(r["raw"])
    n = None if tools is None else len(tools)
    if n is None:
        why = ("응답이 상한을 넘어 잘렸다 — 도구 수 미확인(측정기 한계, 서버 문제 아님)"
               if r.get("body_truncated") else "200이지만 tools/list 응답을 못 읽었다 — 규격 이탈 의심")
        return {**out, "reachable": True, "needs_key": False, "tool_count": None, "why": why}
    return {**out, "reachable": True, "needs_key": False, "tool_count": n,
            "quality": _tool_quality(tools), "specs": tool_specs(tools),
            "why": "" if n else "도구 0개 — 껍데기"}


# **주소의 출처가 판정의 강도를 정한다** (2026-08-19, T-2026W34-107).
#
# 레지스트리 주소는 **관리자가 직접 등록한 것**이다 — 응답이 없으면 "등록한 주소가 죽었다"고
# 말할 자격이 있다. 그러나 README에서 정규식으로 뽑은 주소는 **우리 추정**이고, 응답이 없을 때
# 그것은 "이 서버가 죽었다"가 아니라 **"우리가 이 서버의 주소를 못 찾았다"**이다. 둘을 한 표에
# 실으면 남의 제품에 근거 없는 사망 선고를 하게 된다(기치 ②: 못 봄 != 없음, 기치 ③: 남의 것도 알린다).
#
# 실측 2026-08-19 — 양방향으로 틀렸다. README 추정 41건 중 12건이 그 서버의 주소가 아니었다:
#   거짓 사망 8건  glama.ai/mcp(2·우리 contract-compass 포함) · lobehub.com/mcp(2) ·
#                  home-assistant.io · huggingface.co/spaces/MCP · smithery.ai 목록페이지 ·
#                  xxxx.ngrok.io(README의 placeholder를 그대로 두드렸다)
#   거짓 생존 4건  narajangteo-* 4건이 antigravity.google/docs/mcp(구글 문서 페이지)의 HTTP 200을
#                  근거로 "응답하는 서버" 표에 실렸다. 문서 페이지는 무엇이든 200을 준다.
#
# 그물을 두 겹 친다. 하나는 썩고 하나는 안 썩는다 — 그래서 둘 다 둔다.
#   (1) 알려진 디렉터리·문서 호스트 명단. 정확하지만 새 사이트가 생기면 뒤처진다(썩는다).
#       `server.smithery.ai/@user/x/mcp`는 실제 호스팅 엔드포인트라 통과시킨다 — 막는 것은
#       `smithery.ai/servers/...` 목록 페이지 쪽이다.
#   (2) **같은 README 추정 주소가 서로 다른 프로젝트 2곳 이상에 나오면 그건 남의 주소다.**
#       명단 없이 스스로 갱신되는 규칙이라 새 디렉터리 사이트도 잡는다. 단 tools/list가 실제로
#       읽힌 주소는 예외로 남긴다 — 포크·중복 프로젝트가 진짜 엔드포인트를 공유하는 경우가 있고
#       (korean-law-mcp.fly.dev, service.datahub.kr) 그때는 증거가 명단을 이긴다.
THIRD_PARTY = re.compile(
    r"^https://(?:www\.)?(?:glama\.ai|lobehub\.com|smithery\.ai|mcp\.so|pulsemcp\.com|"
    r"mcpservers\.org|antigravity\.google|home-assistant\.io|huggingface\.co|"
    r"cursor\.com|claude\.ai|openai\.com|docs\.[\w.-]+)/", re.I)
# README가 "여기에 당신 주소를 넣으세요"로 남겨 둔 자리. 실제로 xxxx.ngrok.io를 두드렸다.
PLACEHOLDER = re.compile(r"//(?:xxx+|yyy+|your|my|host|domain)[\w-]*\.", re.I)


def third_party_addr(url: str) -> str:
    """이 주소가 그 서버의 것이 아니라고 볼 근거가 있으면 사유를, 없으면 빈 문자열."""
    if THIRD_PARTY.search(url):
        return "제3자 디렉터리·문서 사이트 주소"
    if PLACEHOLDER.search(url):
        return "README의 placeholder 주소"
    return ""


# **한 README가 /mcp 주소를 여러 개 뱉으면 그건 설치 안내문이다**(codex 교차검증 2026-08-19).
# 실측: narajangteo-* 4건의 README에 "당신의 클라이언트에 추가하기" 블록이 있어 Claude·Cursor·
# VS Code·Zed·Warp 등 **클라이언트 문서 주소 16개**가 전부 엔드포인트 후보로 잡혔다. 첫 주소만
# 막고 다음으로 넘어가면 이번엔 OpenAI 문서를 두드린다 — 명단으로는 끝이 없다.
# 진짜 서버는 자기 주소를 1~2개 적는다. 이 규칙은 명단과 달리 썩지 않는다.
BOILERPLATE_MIN = 4


def protocol_confirmed(rm: dict) -> bool:
    """이 주소가 정말 MCP 서버인지 **관측으로** 확인됐나.

    tools/list가 읽혔거나(도구 수를 셌다) 인증 벽에 막혔다면(401/403) 그 주소는 MCP를 말한다.
    200을 주지만 tools/list를 못 읽는 것은 확인이 아니다 — 문서 페이지가 정확히 그렇게 생겼다.
    """
    return rm.get("tool_count") is not None or bool(rm.get("needs_key"))


def pick_endpoint(remotes: list, shared: dict) -> tuple:
    """이 프로젝트의 주소로 무엇을 두드릴지 고른다. `(고른 것, 못 고른 사유)`.

    레지스트리 수집분에는 confidence가 없다 = 관리자 자기신고 주소라 그대로 믿는다.
    README 추정분은 세 규칙을 거친다(전부 codex 교차검증 2026-08-19에서 나온 결함):
      1. README가 /mcp 주소를 여러 개 뱉으면 그건 클라이언트 설치 안내문이다 → 전부 버린다.
      2. **막힌 주소에서 멈추지 않는다** — 뒤에 진짜 주소가 있다(contract-compass는
         glama.ai 다음 줄이 contract.sallim.app/mcp였다).
      3. 여러 프로젝트에 같이 적힌 주소는 뒤로 미룬다 — 그런 건 대개 남의 것이다.
    """
    readme = [r for r in remotes if r.get("confidence") == "readme"]
    if len(readme) >= BOILERPLATE_MIN and len(readme) == len(remotes):
        return None, (f"README에 /mcp 주소가 {len(readme)}개 있다 — 자기 주소가 아니라 "
                      "클라이언트 설치 안내문이다")
    usable = [r for r in remotes
              if r.get("confidence") != "readme" or not third_party_addr(r["url"])]
    usable.sort(key=lambda r: shared.get(r["url"], 0) if r.get("confidence") == "readme" else 0)
    if usable:
        return usable[0], ""
    if remotes:
        return None, f"{third_party_addr(remotes[0]['url'])}({remotes[0]['url']})"
    return None, ""


def measure_paid_disclosure(mcp_url: str) -> dict:
    """유료 게이트를 **서버가 스스로 밝히는가**.

    왜 이 축이 필요한가(2026-08-18 사장님 지적): `tools/list`는 유료 도구도 그냥 보여준다.
    그래서 "무인증 · 47종"이라고만 적으면 **47종을 공짜로 다 쓴다**는 뜻으로 읽힌다 —
    우리 서버가 실은 무료 37 / 유료 10인데도 그랬다. 우리 자신을 부풀리는 표기였다.

    **밖에서는 판정할 수 없다.** 유료인지 알려면 실제로 불러서 거절당해야 하는데 그건
    남의 서버에 부담이고 오판 위험이다. 그래서 재는 것은 유료 여부가 아니라
    **공시 여부**다 — 밝히는 서버가 모델에게 정직한 서버다. 못 읽으면 `None`이고,
    `None`은 "무료"가 아니라 "확인 못 했다"는 뜻이다(표에도 그렇게 쓴다).
    """
    base = mcp_url.split("?")[0].rstrip("/")
    try:
        req = urllib.request.Request(base + "/health", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
    except Exception:
        return {"disclosed": False}
    t = d.get("tools")
    if isinstance(t, dict) and "free" in t:
        return {"disclosed": True, "total": t.get("total"),
                "free": t.get("free"), "paid": t.get("paid")}
    return {"disclosed": False}


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
            d = json.load(r)
        # 설치형(stdio) 서버는 원격 호출로 잴 수 없다. 대신 **배포가 실제로 있고 언제인지**가
        # 그 서버의 '지금 되냐'다 — 패키지가 없으면 README가 뭐라 하든 설치가 안 된다.
        last = ""
        if kind == "npm":
            last = ((d.get("time") or {}).get("modified") or "")[:10]
            ver = (d.get("dist-tags") or {}).get("latest", "")
        else:
            last = (((d.get("urls") or [{}])[0]).get("upload_time") or "")[:10]
            ver = (d.get("info") or {}).get("version", "")
        return {"type": kind, "id": ident, "installable": True,
                "last_publish": last or None, "version": ver or None}
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

    # 측정 **전에** 센다 — 여러 프로젝트에 같이 적힌 주소를 뒤로 미루려면 미리 알아야 한다.
    shared_readme = collections.Counter(
        r["url"] for it in items for r in (it.get("remotes") or [])
        if r.get("url") and r.get("confidence") == "readme")

    out, notes, noted = [], [], set()
    for i, it in enumerate(items, 1):
        rec = {"name": it["name"], "repo_url": it.get("repo_url", ""),
               "stars": it.get("stars"), "pushed": it.get("pushed"),
               "archived": it.get("archived"), "sources": it["sources"]}
        remotes = [r for r in (it.get("remotes") or []) if r.get("url")]
        rec["remote"] = None
        pick, why = pick_endpoint(remotes, shared_readme)
        url_src = (pick or {}).get("confidence") or "registry"
        if why:
            # 두드리지도 않는다 — 남의 문서 사이트에 POST를 날릴 이유가 없다.
            notes.append(f"{it['name']}: {why}라 **측정 대상에서 뺐다** — 이 서버가 "
                         "안 된다는 뜻이 아니라 우리가 이 서버의 주소를 모른다는 뜻이다")
            noted.add(it["name"])
        if pick:
            rec["remote"] = measure_remote(pick["url"])
            rec["remote"]["url_source"] = url_src
            if rec["remote"].get("reachable"):
                rec["paid_disclosure"] = measure_paid_disclosure(pick["url"])
            time.sleep(PAUSE)
        pkgs = it.get("packages") or []
        rec["package"] = measure_package(pkgs[0]) if pkgs else None
        # 우리가 지는 항목 — 원격 전용은 셀프호스팅 불가
        rec["self_hostable"] = bool(pkgs) or None
        if rec["remote"] is None and rec["package"] is None and it["name"] not in noted:
            notes.append(f"{it['name']}: 원격 주소도 배포 패키지도 없어 **가동 여부를 못 쟀다**(레지스트리 미등록)")
        out.append(rec)
        if i % 10 == 0:
            print(f"  … {i}/{len(items)}")

    # **2차 그물 — 명단 없이 스스로 갱신되는 쪽**(위 THIRD_PARTY 주석 (2)).
    # 같은 README 추정 주소가 서로 다른 프로젝트에 2번 이상 나오면 그건 누구의 것도 아닌
    # 디렉터리·문서 주소다. 단 tools/list가 실제로 읽힌 주소는 남긴다(포크가 진짜 엔드포인트를
    # 공유하는 경우 — 증거가 명단을 이긴다).
    shared = shared_readme
    for r in out:
        rm = r.get("remote") or {}
        if (rm.get("url_source") == "readme" and shared[rm.get("url")] > 1
                and not protocol_confirmed(rm)):
            notes.append(f"{r['name']}: README 추정 주소 {rm['url']}가 다른 프로젝트 "
                         f"{shared[rm['url']] - 1}곳에도 같이 적혀 있고 MCP 응답도 없다 — "
                         "그 서버의 주소가 아니라고 보고 **측정 대상에서 뺐다**")
            r["remote"] = None
            r.pop("paid_disclosure", None)

    # 스키마는 별도 파일로 — measured.json에 넣으면 원자료가 매주 그만큼 불어난다
    # (candidates 5MB 때 배운 것). 프로브만 읽으므로 분리해도 손해가 없다.
    import os
    os.makedirs("schemas", exist_ok=True)
    specs = {}
    for r in out:
        sp = (r.get("remote") or {}).pop("specs", None)
        if sp:
            specs[r["name"]] = sp
    json.dump({"note": "호출에 필요한 최소 스키마(이름·필수인자·읽기전용). probe_quality.py가 읽는다.",
               "items": specs}, open("schemas/tools.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    json.dump({"measured": len(out), "unmeasurable": len(notes), "boundaries": notes,
               "criteria_note": "항목은 D-2026W34-22로 결과 보기 전에 고정됐다. 사후 변경 금지.",
               "items": out}, open("measured.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    live = [r for r in out if (r.get("remote") or {}).get("reachable")]
    keyed = [r for r in live if (r.get("remote") or {}).get("needs_key")]
    disc = [r for r in live if (r.get("paid_disclosure") or {}).get("disclosed")]
    print(f"\n측정 {len(out)}건 · 원격 응답 {len(live)}건 · 그중 키 필요 {len(keyed)}건")
    print(f"무료/유료를 스스로 공시하는 서버 {len(disc)}건 — 나머지는 '확인 못 함'이지 '무료'가 아니다")
    print(f"측정 불가 {len(notes)}건 (원격 주소도 패키지도 없음 — 0건이 아니라 미확인)")
    print("\n■ 실제로 응답한 서버 (키 없이 되는 것 우선)")
    for r in sorted(live, key=lambda x: (x["remote"].get("needs_key") or False,
                                         -(x["remote"].get("tool_count") or 0)))[:15]:
        rm = r["remote"]
        key = "키필요" if rm.get("needs_key") else "무인증"
        warm = rm.get("warm_ms")
        cold = rm.get("cold_ms")
        gap = f"  (콜드 {cold}ms)" if warm and cold and cold > warm * 3 else ""
        print(f"  {key}  도구{str(rm.get('tool_count') or '?'):>4}개  "
              f"{str(warm or cold):>5}ms{gap:<16}  {r['name'][:38]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
