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

from categories import queries

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; building a measured MCP index)"
REGISTRY = "https://registry.modelcontextprotocol.io/v0/servers"
# 4차 원천(2026-08-18): mcpmoa가 **스스로 공개한** 기계 판독 API다. 긁는 게 아니라 초대에
# 응하는 것이다 — robots는 `User-agent: * / Allow: /`이고 Content-Signal이
# `search=yes, use=reference`(우리 용도)이며 ai-train은 no(우리는 학습을 안 한다).
# 나머지 한국 MCP 스토어는 원천으로 쓰지 않는다: playmcp는 SPA 껍데기라 본문이 없고
# (HTML 2.6KB·키워드 0), mcpmarket은 403이며, mcphub는 robots에서 anthropic-ai·GPTBot을
# 명시 차단한다 — UA 이름으로 우회하지 않는다.
# 우리가 빌리는 것은 **발견**이지 판정이 아니다. 그들의 25건도 우리 실호출이 다시 가른다.
MCPMOA = "https://mcpmoa.com/api/v1/servers.json"
GITHUB = "https://api.github.com/search/repositories"
PAGE = 100
# 서버당 1행(version=latest) 기준 실측 259페이지에서 커서가 소진된다. 상한은 폭주 방지용
# 여유값이고, 걸리면 숨기지 않고 `truncated`로 공시한다.
MAX_PAGES = 400

# ASCII만 걸린다(레지스트리 한글 미지원 실측). 한글 전용 항목은 3차가 맡는다.
REGISTRY_TERMS = ["korea", "korean", "kr-", "molit", "kosis", "naver", "kakao",
                  "hangul", "seoul", "krx", "dart"]
# 질의는 categories.py가 낳는다 — 분야가 검색어를 정하고, 찾아낸 검색어가 곧 분야다
# (사장님 지적 2026-08-18: "우리가 분야를 어떻게 나눌지 고려해서 거기 맞는 키워드를 써야").
# 그래서 분류가 수집과 어긋날 수 없고, 커버리지가 분야별로 측정된다.


def _get(url: str, token: str | None = None, tries: int = 3):
    # **UA를 반드시 보낸다.** 없으면 Cloudflare 앞단이 막는다(2026-08-18 mcpmoa 수집
    # HTTPError 실측 — 손으로 UA를 붙이면 200이었다). 정체를 밝히는 것은 예의이자 실용이다.
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
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


def merge_sources(*groups: dict) -> dict:
    """원천들을 한 명단으로 합친다 — **주소가 신원이고 저장소는 거처다**.

    함수로 떼어 둔 이유: 이 규칙이 틀리면 남의 서버가 표에서 조용히 사라지거나
    한 서버가 두 줄로 실린다. 둘 다 실제로 일어났으므로 회귀가 직접 태운다
    (`tests/test_registry_sweep.py`).
    """
    # 이름으로는 절대 안 합쳐진다 — 레지스트리 이름 규칙(app.sallim/…)과 GitHub
    # 경로(sallim-app/…)가 달라 실측 겹침이 0건이다. 그래서 주소와 저장소로 합친다:
    # **주소가 같으면 무조건 같은 서버**이고, 저장소가 같은 것은 **주소가 어긋나지 않을 때만**
    # 같은 서버다(아래 두 주석이 각각의 근거와 실사고를 든다).
    merged: dict = {}
    by_repo: dict = {}
    for d in [d for g in groups for d in g.values()]:
        ru = (d.get("repo_url") or "").rstrip("/").lower()
        # **엔드포인트가 같으면 같은 서버다.** 저장소가 달라도(레지스트리 등록 저장소 vs
        # 소스 저장소) 같은 주소를 부르면 하나로 센다 — 2026-08-18 실측: 우리 서버가
        # korea-realty와 realty-mcp 두 줄로 실려 도구 47종이 중복 계상됐다.
        eps = [(r.get("url") or "").split("?")[0].rstrip("/").lower()
               for r in (d.get("remotes") or []) if r.get("url")]
        # **같은 저장소라고 같은 서버는 아니다**(2026-08-31 실측). 한 저장소에서 여러 서버를
        # 발행하는 곳이 있다 — `lead788/apick-mcp` 하나가 `app.apick/{ai,all,business,finance,
        # identity,ocr,vision,convert,web}` 9개를 내고, 주소가 `/mcp/ai`·`/mcp/all`처럼 전부
        # 다르며 도구 수도 80·16·3으로 제각각이다. 저장소만 보고 합치면 그 9개가 한 줄이 되고
        # **지난주 도구 80개로 게시·채점했던 `app.apick/all`이 표에서 그냥 사라진다.**
        # 이 규칙의 근거는 처음부터 "엔드포인트가 같으면 같은 서버"였다 — 저장소는 코드가 있는
        # 곳이지 돌아가는 서버의 신원이 아니다. 그래서 **주소가 서로 다르면 저장소가 같아도
        # 합치지 않는다**(양쪽 다 주소를 밝혔을 때만 갈라진다 — 한쪽이 아직 주소가 없는
        # 레지스트리↔GitHub 병합은 그대로 살려야 한다).
        key = None
        for e in eps:
            key = key or by_repo.get("ep:" + e)
        if key is None and ru:
            cand = by_repo.get(ru)
            if cand is not None:
                prev_eps = {(r.get("url") or "").split("?")[0].rstrip("/").lower()
                            for r in (merged[cand].get("remotes") or []) if r.get("url")}
                if not (eps and prev_eps and prev_eps.isdisjoint(eps)):
                    key = cand
        if key:
            tgt = merged[key]
            tgt["sources"] |= d["sources"]
            tgt["terms"] |= d["terms"]
            tgt["categories"] = tgt.get("categories", set()) | d.get("categories", set())
            for f in ("stars", "pushed", "archived", "packages", "remotes"):
                if f in d and f not in tgt:
                    tgt[f] = d[f]
            continue
        merged[d["name"]] = d
        if ru:
            by_repo[ru] = d["name"]
        for e in eps:
            by_repo.setdefault("ep:" + e, d["name"])
    for d in merged.values():
        d["sources"] = sorted(d["sources"])
        d["terms"] = sorted(d["terms"])
        d["categories"] = sorted(d.get("categories") or [])
    return merged


def from_registry() -> tuple[dict, list]:
    """공식 레지스트리 **전수 스윕**.

    검색어 스윕을 버린 이유(2026-08-18 실측): 레지스트리 `search=`는 **이름만** 본다.
    우리 `app.sallim/contract-compass`는 설명이 "Korean public procurement law…"인데
    `search=korean`에 안 잡히고 `search=contract`에만 잡혔다. 즉 이름에 한국 단어가 없는
    한국 서버는 검색어를 아무리 늘려도 **구조적으로** 못 본다.
    전체가 수천 건 규모라 커서로 다 넘길 수 있으니, 받아서 우리가 거른다.

    **`version=latest`가 없으면 전수 스윕이 전수가 아니다**(2026-08-31 실측). 기본 응답은
    서버 1개당 **발행한 판마다 한 줄**이라, 페이지를 옛 판으로 채우고 상한에서 끊긴다 —
    40,000행(400페이지)을 받고도 고유 이름은 12,463개였고 커서가 남아 있었다. `version=latest`를
    붙이면 서버당 1행이 되어 **259페이지에서 커서가 소진되고 25,829개**가 나온다. 즉 종전
    스윕은 레지스트리의 48%만 보고 있었다.

    이 결함은 조용하다 — `truncated` 공시가 정직하게 떠 있었으므로 아무도 멈추지 않았고,
    대신 **지난주에 실었던 서버가 이번 주 표에서 그냥 사라졌다**(`app.apick/all`, 지난주 도구
    80개로 게시). 레지스트리에 그대로 살아 있는데 우리가 못 본 것이다. 경계를 공시하는 것과
    경계를 넓힐 수 있는데 안 넓히는 것은 다르다(기치 ②: 못 봄 != 없음).
    """
    found, notes = {}, []
    cursor, pages = None, 0
    while pages < MAX_PAGES:
        # version=latest — 서버당 1행. 빼면 옛 판이 페이지를 먹어 뒤쪽을 못 본다(위 docstring).
        q = {"limit": PAGE, "version": "latest"}
        if cursor:
            q["cursor"] = cursor
        try:
            d = _get(f"{REGISTRY}?{urllib.parse.urlencode(q)}")
        except Exception as e:
            notes.append(f"registry 전수 스윕 {pages}페이지에서 중단({type(e).__name__}) — 이후 미확인")
            break
        rows = d.get("servers") or []
        for e in rows:
            s = e.get("server") or {}
            name = s.get("name")
            if not name:
                continue
            found.setdefault(name, {
                "name": name, "description": s.get("description") or "",
                "packages": [{"type": p.get("registryType"), "id": p.get("identifier"),
                              "version": p.get("version")} for p in (s.get("packages") or [])],
                "remotes": [{"type": r.get("type"), "url": r.get("url"),
                             "needs_auth": bool(r.get("headers"))} for r in (s.get("remotes") or [])],
                "repo_url": (s.get("repository") or {}).get("url") or "",
                # 레지스트리 등록에 repository가 없는 항목이 많다(응답 33건 중 11건). 그때
                # websiteUrl이 유일한 링크원인데 버리고 있었다 — 표에 링크 없는 줄이 생긴 원인.
                "website_url": s.get("websiteUrl") or "",
                "sources": set(), "terms": set()})
            found[name]["sources"].add("registry")
            found[name]["terms"].add("전수")
        pages += 1
        cursor = (d.get("metadata") or {}).get("nextCursor")
        if not cursor or not rows:
            break
    if cursor:
        notes.append(f"registry 전수 스윕이 {MAX_PAGES}페이지 상한에서 멈췄다 — truncated(뒤쪽 미확인)")
    return found, notes


def from_mcpmoa() -> tuple[dict, list]:
    """mcpmoa 공개 API — korean_apis 필드가 우리 문자열 필터보다 정확한 한국 신호다."""
    found, notes = {}, []
    try:
        d = _get(MCPMOA)
    except Exception as e:
        return {}, [f"mcpmoa 수집 실패({type(e).__name__}) — 0건 아님, 미확인"]
    rows = d if isinstance(d, list) else (d.get("servers") or d.get("data") or [])
    for m in rows:
        gh = (m.get("github_url") or "").strip()
        if not gh:
            notes.append(f"mcpmoa:{m.get('name')} github_url 없음 — 병합 열쇠가 없어 건너뜀")
            continue
        name = gh.split("github.com/", 1)[-1].strip("/") if "github.com/" in gh else gh
        desc = " ".join(filter(None, [m.get("description_ko"), m.get("tagline_ko"),
                                      " ".join(m.get("korean_apis") or []),
                                      " ".join(m.get("tags") or [])]))
        found[name] = {"name": name, "description": desc, "repo_url": gh,
                       "korean_apis": m.get("korean_apis") or [],
                       "sources": {"mcpmoa"}, "terms": {"mcpmoa:" + (m.get("category") or "?")}}
    return found, notes


def from_github(token: str | None) -> tuple[dict, list]:
    found, notes = {}, []
    for kw, cat in queries():
        q = f"mcp {kw}"
        url = f"{GITHUB}?{urllib.parse.urlencode({'q': q, 'per_page': PAGE, 'sort': 'stars'})}"
        try:
            d = _get(url, token)
        except Exception as e:
            notes.append(f"github:{q!r}[{cat}] 수집 실패({type(e).__name__}) — 0건 아님, 미확인")
            continue
        total, items = d.get("total_count", 0), d.get("items") or []
        if total > len(items):
            notes.append(f"github:{q!r}[{cat}] 총 {total}건 중 {len(items)}건만 — truncated")
        for r in items:
            if r.get("private") or r.get("fork"):
                continue   # 비공개는 공개 목록에 실을 수 없고, 포크는 원본이 이미 있다
            key = r["full_name"]
            found.setdefault(key, {
                "name": key, "description": r.get("description") or "",
                "stars": r["stargazers_count"], "pushed": r["pushed_at"][:10],
                "archived": r["archived"], "repo_url": r["html_url"],
                "categories": set(), "sources": set(), "terms": set()})
            found[key]["sources"].add("github")
            found[key]["terms"].add(q)
            if cat != "기타":
                found[key]["categories"].add(cat)
        time.sleep(2.2)   # search API 30/min
    return found, notes


def main() -> int:
    # **공개 전용 토큰으로 수집한다(fail-closed).** 조직 접근이 있는 fine-grained 토큰을
    # 쓰면 우리 **비공개** 저장소가 후보로 딸려 들어온다 — 2026-08-18 실측:
    # sallim-app/realty-mcp(private=True)가 keep에 올라 공개 목록에 실릴 뻔했다.
    # 코드에서 걸러도 되지만, 애초에 못 보는 자격을 쓰는 쪽이 안전하다. 아래 private
    # 배제는 그래도 남겨 둔다(자격이 바뀌어도 막히도록).
    token = None
    for path in ("/data/secrets/github-sallim-classic.env", "/data/secrets/github-sallim.env"):
        try:
            for line in open(path, encoding="utf-8"):
                line = line.strip()
                if line.startswith("GITHUB_TOKEN="):
                    token = line.split("=", 1)[1].strip()
            if token:
                break
        except OSError:
            continue

    reg, n1 = from_registry()
    gh, n2 = from_github(token)
    moa, n3 = from_mcpmoa()
    notes = n1 + n2 + n3

    merged = merge_sources(reg, gh, moa)

    json.dump({"generated_note": "재실행 가능. sources·terms로 어느 원천이 잡았는지 추적된다.",
               "boundaries": notes, "count": len(merged),
               "items": sorted(merged.values(), key=lambda x: x["name"])},
              open("candidates_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"레지스트리(전수) {len(reg)} · GitHub {len(gh)} · mcpmoa {len(moa)} · 합집합 {len(merged)}건")
    print(f"repo_url로 병합해 {len(reg) + len(gh) - len(merged)}건이 합쳐졌다")
    import collections
    cov = collections.Counter(c for d in merged.values() for c in (d.get("categories") or []))
    print("\n■ 분야별 수확 (분야가 검색어를 낳는다)")
    from categories import CATEGORIES
    for cat in CATEGORIES:
        print(f"  {cat:<14} {cov.get(cat, 0):3d}건" + ("   ← 0건: 그 분야를 못 봤다" if not cov.get(cat) else ""))
    print("\n■ 경계 공시 — 못 본 것 (없다가 아니라 미확인)")
    if not notes:
        print("  (절단·실패 없음)")
    for n in notes:
        print(f"  - {n}")
    print("  - 레지스트리는 이제 전수 스윕이라 검색어 누락은 없다. 대신 한국 여부 판정을 "
          "우리 필터가 지므로, 필터가 놓치면 그대로 누락된다")
    print("  - npm 검색은 총계가 무의미해 원천에서 제외했다(\"mcp korea\" 94,855건)")
    print("  - playmcp(SPA 껍데기·본문 0)·mcpmarket(403)·mcphub(robots에서 AI 봇 차단)는 "
          "원천에서 제외 — 그쪽에만 있는 항목은 우리가 못 본다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
