#!/usr/bin/env python3
"""한국 데이터 MCP 후보 수집 — 원천 3층 + 경계 공시 (2026-08-18, D-2026W34-21).

왜 3층인가: **목록을 목록에서 베끼면 남의 맹점을 그대로 물려받는다.** 원천마다 못 보는
것이 다르므로 겹쳐야 한다.
  1차 registry — 공식 MCP 레지스트리. 자기신고 1차 자료이고 packages·remotes가 붙어 있어
                 "지금 되냐" 측정의 입력이 여기서 바로 나온다. **한글 검색이 안 된다**
                 (실측 2026-08-18: `한국` 0건 · `kakao` 0건) — 그래서 3차가 필요하다.
  2차 github   — 레지스트리에 등록하지 않은 코드 실체를 잡는다. 별·최종푸시로 생사가 보인다.
  3차 awesome  — 사람 큐레이션. 위 둘이 못 읽는 한글 설명 항목을 잡는다. 대신 썩는다
                 (실측: 57개 중 살아있는 것 23개).

npm 검색은 쓰지 않는다 — "mcp korea" 총계가 94,855건이다(퍼지 OR). 개수로 쓰면 거짓이 된다.

**총계·절단을 정직 공시한다.** 검색 상한에 걸린 질의는 `truncated`로 표시한다. 우리가
제품에서 금지하는 조용한 절단을 우리 수집기가 저지르면 안 된다(기치 ②).

실행: python3 collect_candidates.py   →  candidates.json + 표준출력 커버리지 표
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

REGISTRY = "https://registry.modelcontextprotocol.io/v0/servers"
GITHUB = "https://api.github.com/search/repositories"
PAGE = 100

# ASCII만 걸린다(레지스트리 한글 미지원 실측). 한글 전용 항목은 3차가 맡는다.
REGISTRY_TERMS = ["korea", "korean", "kr-", "molit", "kosis", "naver", "kakao",
                  "hangul", "seoul", "krx", "dart"]
GITHUB_QUERIES = ["topic:mcp korea", "topic:mcp-server korea", "mcp korea in:name",
                  "mcp korean in:description", "mcp 한국 in:readme"]


def _get(url: str, token: str | None = None, tries: int = 3):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and i < tries - 1:
                time.sleep(8 * (i + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def from_registry() -> tuple[dict, list]:
    """공식 레지스트리 — nextCursor로 끝까지 판다. 절단하면 공시한다."""
    found, notes = {}, []
    for term in REGISTRY_TERMS:
        cursor, seen, pages = None, 0, 0
        while True:
            q = {"search": term, "limit": PAGE}
            if cursor:
                q["cursor"] = cursor
            try:
                d = _get(f"{REGISTRY}?{urllib.parse.urlencode(q)}")
            except Exception as e:  # 실패는 0건이 아니다 — 그렇게 적는다
                notes.append(f"registry:{term} 수집 실패({type(e).__name__}) — 0건 아님, 미확인")
                break
            rows = d.get("servers") or []
            for e in rows:
                s = e.get("server") or {}
                name = s.get("name")
                if not name:
                    continue
                found.setdefault(name, {
                    "name": name, "description": s.get("description") or "",
                    # 측정 입력: remotes[].url은 실제로 두드릴 주소, repository.url은
                    # GitHub 원천과 합칠 열쇠다(이게 없으면 슬러그 추측으로 합쳐야 한다).
                    "packages": [{"type": p.get("registryType"), "id": p.get("identifier"),
                                  "version": p.get("version")} for p in (s.get("packages") or [])],
                    "remotes": [{"type": r.get("type"), "url": r.get("url"),
                                 "needs_auth": bool(r.get("headers"))} for r in (s.get("remotes") or [])],
                    "repo_url": (s.get("repository") or {}).get("url") or "",
                    "sources": set(), "terms": set()})
                found[name]["sources"].add("registry")
                found[name]["terms"].add(term)
            seen += len(rows)
            pages += 1
            cursor = (d.get("metadata") or {}).get("nextCursor")
            if not cursor or not rows or pages >= 20:
                if cursor and pages >= 20:
                    notes.append(f"registry:{term} 20페이지 상한에서 중단 — truncated(총계 미상)")
                break
    return found, notes


def from_github(token: str | None) -> tuple[dict, list]:
    found, notes = {}, []
    for q in GITHUB_QUERIES:
        url = f"{GITHUB}?{urllib.parse.urlencode({'q': q, 'per_page': PAGE, 'sort': 'stars'})}"
        try:
            d = _get(url, token)
        except Exception as e:
            notes.append(f"github:{q!r} 수집 실패({type(e).__name__}) — 0건 아님, 미확인")
            continue
        total, items = d.get("total_count", 0), d.get("items") or []
        if total > len(items):
            notes.append(f"github:{q!r} 총 {total}건 중 {len(items)}건만 수집 — truncated")
        for r in items:
            key = r["full_name"]
            found.setdefault(key, {
                "name": key, "description": r.get("description") or "",
                "stars": r["stargazers_count"], "pushed": r["pushed_at"][:10],
                "archived": r["archived"], "repo_url": r["html_url"],
                "sources": set(), "terms": set()})
            found[key]["sources"].add("github")
            found[key]["terms"].add(q)
        time.sleep(2.5)   # search API 30/min
    return found, notes


def main() -> int:
    token = None
    for line in open("/data/secrets/github-sallim.env", encoding="utf-8"):
        if line.startswith("GITHUB_TOKEN="):
            token = line.split("=", 1)[1].strip()

    reg, n1 = from_registry()
    gh, n2 = from_github(token)
    notes = n1 + n2

    # repo_url이 같으면 같은 서버다 — 레지스트리 이름 규칙(app.sallim/…)과 GitHub
    # 경로(sallim-app/…)가 달라 이름으로는 절대 안 합쳐진다(실측 겹침 0건).
    merged: dict = {}
    by_repo: dict = {}
    for d in list(reg.values()) + list(gh.values()):
        ru = (d.get("repo_url") or "").rstrip("/").lower()
        key = by_repo.get(ru) if ru else None
        if key:
            tgt = merged[key]
            tgt["sources"] |= d["sources"]
            tgt["terms"] |= d["terms"]
            for f in ("stars", "pushed", "archived", "packages", "remotes"):
                if f in d and f not in tgt:
                    tgt[f] = d[f]
            continue
        merged[d["name"]] = d
        if ru:
            by_repo[ru] = d["name"]
    for d in merged.values():
        d["sources"] = sorted(d["sources"])
        d["terms"] = sorted(d["terms"])

    json.dump({"generated_note": "재실행 가능. sources·terms로 어느 원천이 잡았는지 추적된다.",
               "boundaries": notes, "count": len(merged),
               "items": sorted(merged.values(), key=lambda x: x["name"])},
              open("candidates_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"레지스트리 {len(reg)}건 · GitHub {len(gh)}건 · 합집합 {len(merged)}건")
    print(f"repo_url로 병합해 {len(reg) + len(gh) - len(merged)}건이 합쳐졌다")
    print("\n■ 경계 공시 — 못 본 것 (없다가 아니라 미확인)")
    if not notes:
        print("  (절단·실패 없음)")
    for n in notes:
        print(f"  - {n}")
    print("  - 레지스트리 검색은 한글을 못 읽는다(실측: `한국` 0건·`kakao` 0건) → 한글 전용 항목 누락, 3차(awesome)가 보완")
    print("  - npm 검색은 총계가 무의미해 원천에서 제외했다(\"mcp korea\" 94,855건)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
