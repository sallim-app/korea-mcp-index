#!/usr/bin/env python3
"""레지스트리 전수 스윕이 실제로 전수인지 고정한다 (2026-08-31).

**계기.** 스윕이 `version=latest` 없이 돌아 서버 1개당 발행판 수만큼 행을 받고 있었다.
페이지가 옛 판으로 채워져 400페이지 상한에서 끊겼고 — 40,000행을 받고도 고유 이름은
12,463개였다. 레지스트리 실제 규모는 25,829개(같은 날 `version=latest`로 259페이지,
커서 소진). 즉 **48%만 보고 "전수 스윕"이라 부르고 있었다.**

이 고장은 조용하다. `truncated` 경계 공시가 정직하게 떠 있어서 아무도 멈추지 않았고,
증상은 엉뚱한 데서 나왔다 — **지난주 도구 80개로 게시했던 `app.apick/all`이 이번 주
표에서 그냥 사라졌다.** 레지스트리엔 그대로 있는데 우리가 못 본 것이다. 남의 서버가
목록에서 사라지는 일이라 "못 봤다"를 "없다"로 게시한 셈이다(기치 ②).

고치는 것만으로는 다음 회차에 다시 통과하므로 여기 박는다. 네트워크를 타지 않는다 —
`_get`을 가짜로 갈아 끼워 **우리가 어떤 질의를 보내는지**만 본다.

실행: python3 -m pytest tests/test_registry_sweep.py -q
"""
import importlib.util
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


collect = _load("collect_candidates")


def _fake_registry(servers: int, per_page: int = 3, versions_per_server: int = 1):
    """레지스트리 흉내.

    **핵심은 페이지가 '행' 단위라는 것이다** — 실제 레지스트리가 그렇다. `version=latest`가
    없으면 한 서버가 판 수만큼 행을 차지하므로 같은 페이지 예산으로 **뒤쪽 서버까지 못 간다**.
    페이지를 서버 단위로 흉내 내면 이 결함이 재현되지 않는다(첫 판 실패의 원인).
    """
    seen: list[str] = []

    def _get(url: str, token=None, tries: int = 3):
        seen.append(url)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        latest = q.get("version", [None])[0] == "latest"
        offset = int(q.get("cursor", ["0"])[0])
        all_rows = []
        for s in range(servers):
            for v in range(1 if latest else versions_per_server):
                all_rows.append({"server": {
                    "name": f"io.example/s{s}", "description": f"v{v}",
                    "repository": {"url": f"https://github.com/example/s{s}"}}})
        rows = all_rows[offset:offset + per_page]
        nxt = offset + per_page
        return {"servers": rows,
                "metadata": {"nextCursor": str(nxt)} if nxt < len(all_rows) else {}}

    return _get, seen


def test_스윕은_판이_아니라_서버를_요청한다():
    """모든 페이지 요청에 `version=latest`가 붙어야 한다 — 빠지면 옛 판이 페이지를 먹는다."""
    fake, seen = _fake_registry(servers=12)
    orig = collect._get
    try:
        collect._get = fake
        collect.from_registry()
    finally:
        collect._get = orig
    assert seen, "레지스트리를 한 번도 부르지 않았다"
    for url in seen:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        assert q.get("version") == ["latest"], f"version=latest 없는 질의: {url}"


def test_결함_재주입__version이_빠지면_고유_서버를_덜_본다():
    """이 테스트가 지키는 값이 실재함을 보인다 — 판이 접히지 않으면 상한 안에서 덜 본다.

    `version=latest`가 빠진 세계에서는 같은 페이지 예산으로 고유 서버를 더 적게 본다.
    (실사고의 축소판: 40,000행 → 고유 12,463개.)
    """
    servers, per_page, vers = 18, 3, 4
    orig_max, orig_get = collect.MAX_PAGES, collect._get
    try:
        collect.MAX_PAGES = 3          # 상한을 좁혀 실사고와 같은 조건을 만든다
        fake_ok, _ = _fake_registry(servers, per_page, vers)
        collect._get = fake_ok
        good, _ = collect.from_registry()

        # 결함 재주입 — 질의에서 version을 떼면 가짜 레지스트리가 판을 그대로 돌려준다.
        fake_bad, _ = _fake_registry(servers, per_page, vers)
        collect._get = lambda u, token=None, tries=3: fake_bad(
            u.replace("&version=latest", "").replace("version=latest&", ""), token, tries)
        bad, _ = collect.from_registry()
    finally:
        collect.MAX_PAGES, collect._get = orig_max, orig_get

    assert len(good) > len(bad), (
        f"결함을 되돌려도 고유 서버 수가 안 줄었다(good={len(good)} bad={len(bad)}) — "
        "이 회귀는 아무것도 안 지키고 있다")


def test_상한에_걸리면_truncated를_공시한다():
    """경계 공시는 남는다 — 넓혔다고 지우면 다음에 또 조용히 끊긴다."""
    orig_max, orig_get = collect.MAX_PAGES, collect._get
    try:
        collect.MAX_PAGES = 2
        fake, _ = _fake_registry(servers=30)
        collect._get = fake
        _, notes = collect.from_registry()
    finally:
        collect.MAX_PAGES, collect._get = orig_max, orig_get
    assert any("truncated" in n for n in notes), f"상한에 걸렸는데 공시가 없다: {notes}"


def test_커서가_소진되면_truncated가_아니다():
    """반대편 — 다 본 회차에 truncated를 달면 그 공시가 의미를 잃는다."""
    orig_get = collect._get
    try:
        fake, _ = _fake_registry(servers=9)
        collect._get = fake
        _, notes = collect.from_registry()
    finally:
        collect._get = orig_get
    assert not any("truncated" in n for n in notes), f"다 봤는데 truncated가 붙었다: {notes}"


if __name__ == "__main__":
    test_스윕은_판이_아니라_서버를_요청한다()
    test_결함_재주입__version이_빠지면_고유_서버를_덜_본다()
    test_상한에_걸리면_truncated를_공시한다()
    test_커서가_소진되면_truncated가_아니다()
    print("ok")


# ── 저장소가 같아도 주소가 다르면 다른 서버다 (2026-08-31 실사고) ──────────────
#
# `lead788/apick-mcp` 한 저장소가 `app.apick/{ai,all,business,finance,…}` 9개를 발행한다.
# 주소는 `/mcp/ai`·`/mcp/all`처럼 전부 다르고 도구 수도 80·16·3으로 제각각인데, 저장소만
# 보고 합치면 9개가 한 줄이 된다 — 지난주 도구 80개로 게시·채점한 `app.apick/all`이
# 그렇게 사라질 뻔했다. 반대로 과잉 분리도 막아야 한다: 레지스트리 항목은 주소를 갖고
# GitHub 항목은 보강 전이라 주소가 없으므로, 그 둘은 여전히 합쳐져야 한다.

def _srv(name, repo, url=None):
    d = {"name": name, "description": "", "repo_url": repo,
         "sources": {"registry"}, "terms": {"전수"}, "categories": set()}
    if url:
        d["remotes"] = [{"type": "streamable-http", "url": url}]
    return d


def test_한_저장소가_낸_여러_서버는_갈라져야_한다():
    """실사고 그대로 — apick 형제 3개는 3줄로 남아야 한다."""
    rows = {s["name"]: s for s in [
        _srv("app.apick/ai", "https://github.com/lead788/apick-mcp", "https://apick.app/mcp/ai"),
        _srv("app.apick/all", "https://github.com/lead788/apick-mcp", "https://apick.app/mcp/all"),
        _srv("app.apick/finance", "https://github.com/lead788/apick-mcp",
             "https://apick.app/mcp/finance"),
    ]}
    merged = collect.merge_sources(rows)
    assert len(merged) == 3, (
        f"주소가 다른 형제 서버가 {len(merged)}줄로 접혔다 — 지난주 게시한 서버가 사라진다: "
        f"{sorted(merged)}")
    assert "app.apick/all" in merged, "도구 80개짜리가 병합에 먹혔다"


def test_주소가_같으면_저장소가_달라도_합친다():
    """반대편 과잉 분리 방지 — 같은 주소를 부르면 한 서버다(우리 contract-compass 실사고)."""
    reg = {"app.sallim/contract-compass": _srv(
        "app.sallim/contract-compass", "https://github.com/kwenhwang/contract-compass",
        "https://contract.sallim.app/mcp")}
    gh = {"sallim-app/contract-compass": _srv(
        "sallim-app/contract-compass", "https://github.com/sallim-app/contract-compass",
        "https://contract.sallim.app/mcp")}
    merged = collect.merge_sources(reg, gh)
    assert len(merged) == 1, f"같은 주소인데 두 줄로 남았다: {sorted(merged)}"


def test_주소가_아직_없는_쪽은_저장소로_합친다():
    """GitHub 항목은 보강 전이라 주소가 없다 — 그 병합까지 끊으면 후보가 두 배로 분열한다."""
    reg = {"io.github.x/y": _srv("io.github.x/y", "https://github.com/x/y",
                                 "https://x.example/mcp")}
    gh = {"x/y": _srv("x/y", "https://github.com/x/y")}          # 주소 없음
    merged = collect.merge_sources(reg, gh)
    assert len(merged) == 1, f"주소 없는 GitHub 항목이 안 합쳐졌다: {sorted(merged)}"
