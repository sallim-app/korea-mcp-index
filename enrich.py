#!/usr/bin/env python3
"""GitHub-only 후보에서 엔드포인트·패키지를 찾아낸다 (2026-08-18, D-2026W34-21).

왜 필요한가: 첫 측정에서 후보 133건 중 **106건을 못 쟀다** — 원격 주소도 배포 패키지도
없었기 때문이다. 그런데 그건 "안 돈다"가 아니라 "레지스트리에 등록을 안 했다"였다.
저장소 안에는 대개 실행법이 적혀 있다. 그걸 읽어내면 잴 수 있다.

신뢰 등급을 구분해 붙인다 — **추정을 사실인 척하지 않는다**:
  manifest  package.json `name` / pyproject `[project] name` — 저자가 선언한 값. 권위 있다.
  readme    README의 `npx …` `uvx …` `pip install …` `https://…/mcp` — **추정**이다.
            남의 서버를 예시로 적어둔 것일 수 있다.
판정은 여기서 하지 않는다. 뽑아만 두고 measure.py의 실호출이 가른다 —
응답하면 진짜고, 아니면 후보에서 빠진다. 그것이 이 파이프라인의 규칙이다.

제외: localhost·127.0.0.1·example.com·modelcontextprotocol.io 등 남의 것이 확실한 주소.

실행: python3 enrich.py  →  candidates_enriched.json
"""
import base64
import json
import re
import time
import urllib.error
import urllib.request

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app)"
# **배지 이미지가 엔드포인트로 둔갑한다.** 2026-08-18 실측: korean-law-mcp(★2,476)의
# 엔드포인트로 `https://img.shields.io/badge/MCP`가 잡혔고 이미지라 200이 떠서
# "작동하는 서버"로 실릴 뻔했다. README에서 뽑는 이상 이 계열은 계속 나온다.
# 2026-08-19 추가(T-2026W34-107): 배지 이미지 다음으로 새는 것이 **디렉터리·문서 사이트**다.
# README의 "이 서버를 Glama/LobeHub에 추가하기" 안내문에 적힌 그 사이트 주소가 서버 주소로
# 잡혔다 — 실측 12건. `server.smithery.ai/@user/x/mcp`는 진짜 호스팅 주소라 살리고
# `smithery.ai/servers/...` 목록 페이지만 막는다. 측정 쪽(measure.py)에도 같은 그물이 있다 —
# 여기서 새면 거기서 잡고, 거기 명단이 뒤처지면 '같은 주소 2곳 이상' 규칙이 잡는다.
SKIP_HOST = re.compile(
    r"localhost|127\.0\.0\.1|0\.0\.0\.0|example\.(com|org)|your-|<|\{|"
    r"modelcontextprotocol\.io|github\.com|npmjs\.com|readthedocs|"
    r"shields\.io|badge|\.svg|\.png|img\.|raw\.githubusercontent|"
    r"glama\.ai|lobehub\.com|//(?:www\.)?smithery\.ai|mcp\.so|pulsemcp\.com|"
    r"mcpservers\.org|antigravity\.google|home-assistant\.io|huggingface\.co|"
    r"cursor\.com|claude\.ai|openai\.com|/docs/|"
    # README가 "여기에 당신 주소를" 로 남겨 둔 자리 — 실제로 xxxx.ngrok.io를 두드렸다.
    r"//(?:xxx+|yyy+|host|domain)[\w-]*\.", re.I)
RE_ENDPOINT = re.compile(r"https://[\w.-]+(?::\d+)?(?:/[\w./-]*)?/(?:mcp|sse)\b", re.I)
RE_NPX = re.compile(r"npx\s+(?:-y\s+|--yes\s+)?(@?[\w.@/-]+)", re.I)
RE_UVX = re.compile(r"uvx\s+(?:--from\s+)?([\w.-]+)", re.I)
RE_PIP = re.compile(r"pip\s+install\s+([\w.-]+)", re.I)


def _api(path: str, token: str):
    req = urllib.request.Request("https://api.github.com" + path,
                                 headers={"Authorization": f"Bearer {token}",
                                          "Accept": "application/vnd.github+json",
                                          "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            time.sleep(10)
        return {"_err": e.code}
    except Exception as e:
        return {"_err": type(e).__name__}


def _content(repo: str, path: str, token: str) -> str | None:
    d = _api(f"/repos/{repo}/contents/{path}", token)
    if "_err" in d or not isinstance(d, dict) or d.get("encoding") != "base64":
        return None
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "replace")
    except (ValueError, KeyError):
        return None


def _readme(repo: str, token: str) -> str | None:
    d = _api(f"/repos/{repo}/readme", token)
    if "_err" in d:
        return None
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "replace")
    except (ValueError, KeyError, TypeError):
        return None


RE_KRDOMAIN = re.compile(r"\b[\w.-]+\.(go|or|re)\.kr\b", re.I)


def enrich(repo: str, token: str) -> dict:
    found = {"packages": [], "remotes": [], "evidence": [], "kr_domains": []}

    pj = _content(repo, "package.json", token)
    if pj:
        try:
            name = json.loads(pj).get("name")
            if name:
                found["packages"].append({"type": "npm", "id": name, "confidence": "manifest"})
                found["evidence"].append("package.json name")
        except ValueError:
            pass
    for f in ("pyproject.toml", "setup.py"):
        txt = _content(repo, f, token)
        if not txt:
            continue
        m = re.search(r'^\s*name\s*=\s*["\']([\w.-]+)["\']', txt, re.M)
        if m:
            found["packages"].append({"type": "pypi", "id": m.group(1), "confidence": "manifest"})
            found["evidence"].append(f"{f} name")
            break

    rm = _readme(repo, token)
    if rm:
        # README가 부르는 한국 정부·기관 도메인 — 설명이 영어뿐인 서버를 잡는 유일한 신호다.
        found["kr_domains"] = sorted({m.group(0).lower() for m in RE_KRDOMAIN.finditer(rm)})[:6]
        for u in dict.fromkeys(RE_ENDPOINT.findall(rm)):
            if not SKIP_HOST.search(u):
                found["remotes"].append({"type": "streamable-http", "url": u,
                                         "confidence": "readme"})
        if not found["packages"]:
            for rx, kind in ((RE_NPX, "npm"), (RE_UVX, "pypi"), (RE_PIP, "pypi")):
                m = rx.search(rm)
                if m and not m.group(1).startswith("@modelcontextprotocol"):
                    found["packages"].append({"type": kind, "id": m.group(1),
                                              "confidence": "readme"})
                    found["evidence"].append(f"README {kind} 명령")
                    break
    return found


def main() -> int:
    token = None
    for line in open("/data/secrets/github-sallim.env", encoding="utf-8"):
        line = line.strip()
        if line.startswith("GITHUB_TOKEN="):
            token = line.split("=", 1)[1].strip()

    src = json.load(open("candidates_filtered.json", encoding="utf-8"))
    # **review도 보강한다.** review는 "한국 관련은 맞은데 데이터형 신호가 없다"거나
    # "설명이 비었다"는 뜻이고, 그 답이 대개 README에 있다. keep만 보강하면 판정을
    # 못 바꾸는 곳만 파는 셈이다(2026-08-18: README의 .go.kr 신호를 도입하며 발견).
    todo = [i for i in src["items"]
            if i["verdict"] in ("keep", "review")
            and not i.get("remotes") and not i.get("packages")
            and i.get("repo_url", "").startswith("https://github.com/")]
    print(f"보강 대상 {len(todo)}건 (keep+review 중 원격·패키지 둘 다 없는 것)")

    hit_r = hit_p = 0
    for n, it in enumerate(todo, 1):
        repo = it["repo_url"].split("github.com/", 1)[1].strip("/")
        f = enrich(repo, token)
        if f["remotes"]:
            it["remotes"] = f["remotes"]
            hit_r += 1
        if f["packages"]:
            it["packages"] = f["packages"]
            hit_p += 1
        it["enrich_evidence"] = f["evidence"]
        if f.get("kr_domains"):
            it["kr_domains"] = f["kr_domains"]
        if n % 20 == 0:
            print(f"  … {n}/{len(todo)}  (엔드포인트 {hit_r} · 패키지 {hit_p})")
        time.sleep(0.3)

    json.dump(src, open("candidates_enriched.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    still = len([i for i in src["items"]
                 if i["verdict"] == "keep" and not i.get("remotes") and not i.get("packages")])
    krd = len([i for i in src["items"] if i.get("kr_domains")])
    print(f"\n엔드포인트 발견 {hit_r}건 · 패키지 발견 {hit_p}건 · 한국 도메인(.go.kr 등) {krd}건")
    print(f"여전히 못 재는 keep {still}건 — 저장소에 실행법이 안 적혀 있다(미확인이지 부재가 아니다)")
    print("\n주의: readme 신뢰도는 **추정**이다. 실호출·레지스트리 조회가 가른다 — measure.py 몫.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
