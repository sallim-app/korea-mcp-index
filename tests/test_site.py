#!/usr/bin/env python3
"""정적 사이트 산출물의 회귀 고정 (2026-08-29).

이 사이트가 존재하는 이유는 **검색엔진과 AI가 이 측정값을 읽게 하는 것**이다. 그래서
여기서 고정하는 것은 예쁜 마크업이 아니라 그 이유가 깨지는 자리들이다:

① **본문이 초기 HTML에 있는가** — 클라이언트 JS가 그리면 크롤러는 빈 껍데기를 가져간다.
   이 조직엔 그 사고 이력이 있다. 그래서 서버 이름·측정값이 파일에 실제로 몇 개 들어
   있는지를 센다.
② **날짜가 잰 날인가** — `bbfaaa8`은 "마지막 측정"에 문서를 뽑은 날을 찍고 있었다.
   같은 실수를 페이지에서 반복하지 않는다. `measured_at`이 없으면 렌더가 실패해야 한다.
③ **기치** — 우리 것만 싣지 않았는가, 우리가 지는 축을 실었는가.
④ **색인 배관** — canonical과 sitemap의 주소가 같은가, robots가 막지 않는가.
   생산자만 있고 소비자가 0이던 사고를 막으려면 둘이 같은 값이어야 한다.
"""
import collections
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://example.test/idx"


def build(tmp, extra=None, data_patch=None):
    """실물 렌더를 돌린다 — 함수를 흉내 내면 게시본이 아니라 흉내를 검사하게 된다."""
    out = pathlib.Path(tmp) / "site"
    cwd = ROOT
    if data_patch is not None:
        cwd = pathlib.Path(tmp) / "repo"
        cwd.mkdir()
        for f in ROOT.iterdir():
            if f.name in {"site", "__pycache__", ".git", "tests", "node_modules"}:
                continue
            (shutil.copytree if f.is_dir() else shutil.copy2)(f, cwd / f.name)
        d = json.loads((cwd / "measured.json").read_text(encoding="utf-8"))
        d.update(data_patch)
        (cwd / "measured.json").write_text(json.dumps(d, ensure_ascii=False),
                                           encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                        "--base", BASE, "--out", str(out)] + (extra or []),
                       cwd=cwd, capture_output=True, text=True, check=False)
    return r, out


def test_renders_and_body_is_in_the_html():
    """①: JS 없이 받은 HTML 안에 서버 이름과 측정값이 실제로 들어 있는가."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        idx = (out / "index.html").read_text(encoding="utf-8")
        assert "<script" not in idx.replace('<script type="application/ld+json">', ""), \
            "구조화데이터 말고 실행 스크립트가 있다 — 본문을 JS로 그리면 크롤러가 못 읽는다"
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        named = [s for s in m["servers"] if s["name"] in idx or
                 s["name"].split("/")[-1] in idx]
        assert len(named) >= 15, f"초기 HTML에 든 서버 이름 {len(named)}개 — 너무 적다"
        assert re.search(r"\d+\s*ms|웜 ms", idx), "측정값(지연)이 본문에 없다"


def test_every_server_has_its_own_url():
    """목록 앵커가 아니라 각자 주소여야 그 서버 이름으로 검색에 잡힌다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        assert len(m["servers"]) >= 40
        for s in m["servers"]:
            assert s["page"].startswith(BASE + "/servers/"), s
            f = out / (s["page"][len(BASE) + 1:] + ".html")
            assert f.exists(), f"상세 페이지 없음: {f}"
            assert s["name"] in f.read_text(encoding="utf-8")


def test_dates_are_measurement_dates_not_render_dates():
    """②: 게시된 측정일은 원자료의 `measured_at`이다. 오늘 날짜로 밀리면 안 된다."""
    d = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    ts = d["measured_at"]
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        assert m["measured_at"] == ts
        idx = (out / "index.html").read_text(encoding="utf-8")
        assert f"가동 측정일 <strong>{ts}</strong>" in idx
        assert "이 페이지 생성" in idx, "생성일이 측정일과 구별돼 적혀 있어야 한다"
        for s in m["servers"]:
            assert s["measured_at"] == ts


def test_render_date_never_substitutes_for_measurement_date():
    """`bbfaaa8`의 진짜 회귀 — 렌더 날짜가 측정일 자리에 들어가면 잡힌다.

    종전 검사는 `assert ... or True` 라는 죽은 단정이었다(codex 교차검증 2026-08-29).
    이제 원자료의 측정일을 **오늘일 수 없는 날짜**로 바꿔 넣고, 게시본이 그 날짜를
    그대로 내는지 본다. 렌더가 오늘로 때우면 여기서 깨진다.
    """
    sentinel = "2019-03-07"
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp, data_patch={"measured_at": sentinel})
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        assert m["measured_at"] == sentinel
        assert m["generated_at"] != sentinel, "생성일이 측정일로 덮였다"
        idx = (out / "index.html").read_text(encoding="utf-8")
        assert f"가동 측정일 <strong>{sentinel}</strong>" in idx
        assert m["generated_at"] in idx, "생성일이 페이지에 따로 적혀 있어야 한다"
        assert "오래된 값이다" in idx, "7년 지난 값을 오래됐다고 말하지 않는다"
        for s in m["servers"]:
            assert s["measured_at"] == sentinel


def test_renamed_servers_disclose_the_old_name_everywhere():
    """개명 서버의 등수는 옛 이름으로 받은 것이다 — 상세·기계 표면 둘 다에서 밝힌다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        renamed = [s for s in m["servers"] if s["rank_graded_as"]]
        assert renamed, "이 원자료엔 개명 서버가 실제로 있다 — 검사가 헛돌고 있다"
        for s in renamed:
            body = (out / "servers" / (s["page"].rsplit("/", 1)[1] + ".html")).read_text(
                encoding="utf-8")
            assert s["rank_graded_as"] in body, s["name"]
            assert "옛 이름" in body, s["name"]


def test_structured_data_keeps_the_real_rank_numbers():
    """빈자리를 위로 당기지 않는 규약은 구조화데이터에도 적용된다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        rank_of = {s["name"]: s["rank_in_category"] for s in m["servers"]}
        seen = 0
        for f in (out / "category").glob("*.html"):
            for blob in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>',
                    f.read_text(encoding="utf-8"), re.S):
                d = json.loads(blob)
                if d.get("@type") != "ItemList":
                    continue
                for it in d["itemListElement"]:
                    assert it["position"] == rank_of[it["name"]], (f.name, it)
                    seen += 1
        assert seen >= 10


def test_out_dir_is_not_recursively_deleted_without_a_stamp():
    """`--out .` 한 번에 저장소가 날아가지 않는가(codex 교차검증 2026-08-29)."""
    with tempfile.TemporaryDirectory() as tmp:
        victim = pathlib.Path(tmp) / "notours"
        victim.mkdir()
        (victim / "소중한파일.txt").write_text("지우면 안 된다", encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                            "--base", BASE, "--out", str(victim)],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        assert r.returncode != 0, "표식 없는 디렉토리를 지우고 덮어썼다"
        assert (victim / "소중한파일.txt").exists(), "남의 파일이 사라졌다"
        # 두 번째 회차는 자기가 만든 디렉토리를 정상적으로 다시 쓴다
        mine = pathlib.Path(tmp) / "mine"
        for _ in range(2):
            r = subprocess.run([sys.executable, str(ROOT / "render_site.py"),
                                "--base", BASE, "--out", str(mine)],
                               cwd=ROOT, capture_output=True, text=True, check=False)
            assert r.returncode == 0, r.stderr


def test_render_stops_when_measurement_date_is_missing():
    """②의 fail-closed: 잰 날을 모르면 오늘로 때우지 말고 멈춰라."""
    with tempfile.TemporaryDirectory() as tmp:
        r, _ = build(tmp, data_patch={"measured_at": None})
        assert r.returncode != 0, "측정일 없이도 사이트가 나왔다"
        assert "measured_at" in r.stderr


def test_render_stops_when_our_losing_axes_are_missing():
    """빈 축을 0건으로 게시하면 남의 저장소를 '라이선스 없음'으로 낙인찍는다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, _ = build(tmp, data_patch={"axes_at": None})
        assert r.returncode != 0
        assert "축" in r.stderr


def test_creed_not_only_ours_and_we_publish_where_we_lose():
    """③: 우리 것만 싣지 않는다 · 우리가 지는 축을 우리가 먼저 싣는다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        ours = [s for s in m["servers"] if s["operated_by_us"]]
        theirs = [s for s in m["servers"] if not s["operated_by_us"]]
        assert ours, "운영자 서버가 빠졌다 — 자기 것을 뺀 목록도 정직하지 않다"
        assert len(theirs) > len(ours) * 5, "남의 서버가 너무 적다 — 우리 것만 싣는 목록"
        idx = (out / "index.html").read_text(encoding="utf-8")
        # 절의 순서로 본다 — 본문 문장에 같은 낱말이 섞이면 문자열 위치는 거짓이 된다
        # (우리 서버 총평에 "억원 표기"가 들어 있어 실제로 그렇게 깨졌다).
        heads = re.findall(r'<h2 id="([^"]+)"', idx)
        assert "지는-항목" in heads, "「우리가 지는 항목」이 없다"
        assert heads.index("지는-항목") < heads.index("표기"), \
            "지는 축이 문서 끝으로 밀렸다 — 안 실은 것과 같다"
        assert "셀프호스팅은 우리가 제일 나쁘다" in idx
        # 요약표에서 우리 총평만 잘리면 화면 효과는 "우리 행만 순수 칭찬"이다.
        ours_names = {s["name"] for s in ours}
        for row in re.findall(r"<tr>(.*?)</tr>", idx, re.S):
            for name in ours_names:
                if name.split("/")[-1] in row and "왜 이것이 1위인가" not in row:
                    assert "…" not in row, "우리 행의 총평이 잘렸다: " + row[:120]
        # 1위가 전부 우리이면 그 표는 판정이 아니라 광고지다.
        firsts = [s for s in m["servers"] if s["rank_in_category"] == 1]
        assert any(not s["operated_by_us"] for s in firsts), \
            "모든 분야 1위가 우리다 — 축 설계를 다시 봐야 한다"


def test_stale_ranks_are_labelled_in_the_machine_feed():
    """가동은 매주·순위는 매월 — 회차가 다르다. 기계 표면이 그 사실을 숨기면 거짓말이 된다.

    codex 교차검증 지적(2026-08-29): 무응답 서버가 `index.json`에는 2위·3위로 남는데
    HTML 순위표에는 없어, 사람용과 기계용이 어긋났다. 등수를 지우는 대신 회차를 밝힌다.
    """
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        html = (out / "index.html").read_text(encoding="utf-8")
        stale = [s for s in m["servers"] if s["rank_in_category"] and not s["rank_is_current"]]
        for s in m["servers"]:
            if s["rank_in_category"]:
                assert s["rank_is_current"] is not None
            if s["rank_is_current"] is False:
                assert s["rank_note"], s
                body = (out / "servers" / (s["page"].rsplit("/", 1)[1] + ".html")).read_text(
                    encoding="utf-8")
                assert "지난 채점 회차의 것이다" in body, s["name"]
                assert s["name"] not in html or "빠진 등수" in html
            if s["rank_is_current"]:
                assert s["rank_note"] is None
        assert stale, "이 원자료엔 회차가 어긋난 등수가 실제로 있다 — 검사가 헛돌고 있다"
        b = " ".join(m["boundaries"])
        assert "rank_is_current=false" in b


def test_structured_data_cannot_escape_its_script_tag():
    """남의 서버 이름·URL이 그대로 들어가는 자리다 — `</script>`로 태그를 못 빠져나가야 한다.

    codex 교차검증 지적(2026-08-29). 우리가 수집하는 이름은 남의 README에서 온 것이라
    우리 손을 안 거친다 — 신뢰할 근거가 없다.
    """
    sys.path.insert(0, str(ROOT))
    import render_site
    hostile = {"name": "a</script><img src=x onerror=alert(1)>", "x": "a&b"}
    blob = render_site.jsonld(hostile)
    assert "</script>" not in blob and "<" not in blob and ">" not in blob
    assert json.loads(blob) == hostile, "이스케이프가 값을 바꿨다"
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        for f in out.rglob("*.html"):
            body = f.read_text(encoding="utf-8")
            for blob in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
                assert "<" not in blob and ">" not in blob, f
                json.loads(blob)


def test_misfiled_servers_are_not_published_under_the_wrong_field():
    """분야 교정 서버는 실제 분야로 적고, 무효화한 등수를 현재 등수로 내지 않는다.

    codex 교차검증 지적(2026-08-29): 순위에서는 뺐다고 써 놓고 제목·breadcrumb·구조화
    데이터·기계 피드는 틀린 분야와 그 등수를 그대로 게시하고 있었다.
    """
    sys.path.insert(0, str(ROOT))
    from observed import MISFILED
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        rows = {s["name"]: s for s in m["servers"]}
        seen = 0
        for name, (collected, real, _why) in MISFILED.items():
            s = rows.get(name)
            if not s:
                continue
            seen += 1
            assert s["category"] == real, s
            assert s["category_corrected_from"] == collected, s
            assert s["rank_is_current"] is not True, "무효 등수를 현재 등수로 배포했다"
            body = (out / "servers" / (s["page"].rsplit("/", 1)[1] + ".html")).read_text(
                encoding="utf-8")
            assert "분야 교정" in body
            assert f"이 서버는 <strong>{real}</strong>이다" in body
            assert "이 서버의 성적이 아니다" in body or not s["rank_in_category"]
        assert seen >= 3, f"분야 교정 서버를 {seen}건밖에 못 봤다 — 검사가 헛돌고 있다"
        # 구조화데이터에도 남으면 안 된다
        for f in (out / "category").glob("*.html"):
            for blob in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>',
                    f.read_text(encoding="utf-8"), re.S):
                d = json.loads(blob)
                if d.get("@type") == "ItemList":
                    for it in d["itemListElement"]:
                        assert it["name"] not in MISFILED, (f.name, it)


def test_fact_errors_never_shows_zero_for_ungraded():
    """`—`(안 쟀다)를 `0건`(오류 없음)으로 바꾸면 그건 거짓 라벨이다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        graded_zero = {s["name"] for s in m["servers"] if s["fact_errors"] == 0}
        idx = (out / "index.html").read_text(encoding="utf-8")
        rows = re.findall(r"<tr>(.*?)</tr>", idx, re.S)
        for row in rows:
            if ">0건<" not in row:
                continue
            assert any(n.split("/")[-1] in row for n in graded_zero), \
                "채점하지 않은 줄에 0건이 붙었다: " + re.sub(r"<[^>]+>", " ", row)[:120]


def test_negative_claims_ship_with_our_client_limits():
    """남의 서버에 부정적인 줄을 내는 화면에는 **우리 두드리개의 한계**가 같이 있어야 한다.

    fresh-eyes 검수(2026-08-29)가 잡은 자리다. `tools/list` 200을 못 받은 28건 중 22건은
    HTTP 상태코드를 돌려줬다 — 서버는 살아 있었고 우리 호출 방식이 안 맞았을 수 있다.
    그 사실 없이 "응답 없음"만 내면 관측이 아니라 판정이 된다.
    """
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        assert m["client_limits"], "기계 표면에 한계 공시가 없다"
        assert any("initialize" in x for x in m["client_limits"])
        for page in ("index.html", "down.html", "method.html"):
            body = (out / page).read_text(encoding="utf-8")
            assert "initialize" in body, page
            assert "우리 두드리개가 못 하는 것" in body or "못 하는 것" in body, page
        # 부정 판정을 실은 상세 페이지에도 붙어야 한다
        dead = [s for s in m["servers"] if s["bucket"] == "unreachable"]
        assert dead
        for s in dead:
            body = (out / "servers" / (s["page"].rsplit("/", 1)[1] + ".html")).read_text(
                encoding="utf-8")
            assert "initialize" in body, s["name"]
            desc = re.search(r'<meta name="description" content="([^"]*)"', body).group(1)
            assert "우리 호출의 결과" in desc, s["name"]


def test_headline_carries_the_caveat_into_meta_and_machine_surfaces():
    """검색·AI가 물어가는 문장에 caveat이 없으면 caveat은 없는 것과 같다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        idx = (out / "index.html").read_text(encoding="utf-8")
        desc = re.search(r'<meta name="description" content="([^"]*)"', idx).group(1)
        assert "HTTP 상태코드" in desc and "등록한 주소만" in desc, desc
        llms = (out / "llms.txt").read_text(encoding="utf-8")
        assert "추정" in llms and "initialize" in llms


def test_counts_reproduce_from_the_servers_array():
    """총계가 배열에서 재현되지 않으면, 통과하는 검사 뒤에서 조용히 어긋난다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        got = collections.Counter(s["bucket"] for s in m["servers"])
        for k in ("comparable", "unmeasurable", "unreachable", "off_topic"):
            assert got[k] == m["counts"][k], (k, got[k], m["counts"][k])
        c = m["counts"]
        assert (len(m["servers"]) + c["install_only"] + c["no_address_no_package"]
                == c["candidates_total"])
        idx = (out / "index.html").read_text(encoding="utf-8")
        assert str(c["candidates_total"]) in idx, "총계가 사람 화면에 없다"


def test_tables_are_reachable_by_keyboard():
    """가로 스크롤 컨테이너를 키보드로 못 움직이면 그 열은 없는 것이다(WCAG 2.1.1)."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        for f in out.rglob("*.html"):
            body = f.read_text(encoding="utf-8")
            for div in re.findall(r'<div class="tw"[^>]*>', body):
                assert 'tabindex="0"' in div and 'role="region"' in div, (f.name, div)
                assert "aria-label" in div, (f.name, div)


def test_boundaries_are_published_not_hidden():
    """못 봄 ≠ 없음. 기계 표면에도 경계가 실려야 한다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        b = " ".join(m["boundaries"])
        assert "폐기 판정이 아니라" in b
        assert "확인 못 함" in b or "오픈소스 아님" in b
        assert any(s["endpoint_source"] == "readme_guess" for s in m["servers"])
        down = (out / "down.html").read_text(encoding="utf-8")
        assert "폐기 판정이 아니라 관측 기록" in down


def test_index_plumbing_canonical_sitemap_robots():
    """④: canonical == sitemap의 loc == 실제 파일 위치. 셋 중 하나만 어긋나도 색인이 샌다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        sm = (out / "sitemap.xml").read_text(encoding="utf-8")
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sm))
        assert len(locs) >= 60
        html_files = [p for p in out.rglob("*.html") if p.name != "404.html"]
        assert len(html_files) == len(locs), \
            f"페이지 {len(html_files)}개인데 sitemap엔 {len(locs)}개"
        for f in html_files:
            t = f.read_text(encoding="utf-8")
            can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
            assert can, f"canonical 없음: {f}"
            assert can.group(1) in locs, f"canonical이 sitemap에 없다: {can.group(1)}"
            assert 'name="robots" content="index' in t, f"noindex가 박혔다: {f}"
            assert '<meta name="description"' in t
            assert '<title>' in t
        rb = (out / "robots.txt").read_text(encoding="utf-8")
        assert "Disallow:" not in rb, "우리 목록을 우리가 막고 있다"
        assert f"Sitemap: {BASE}/sitemap.xml" in rb
        assert BASE + "/llms.txt" in rb


def test_no_broken_internal_links():
    """죽은 내부 링크는 크롤러에게도 사람에게도 막다른 길이다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        known = {BASE + "/"} | {
            BASE + "/" + str(p.relative_to(out)).removesuffix(".html")
            for p in out.rglob("*.html")} | {
            BASE + "/" + p.name for p in out.iterdir() if p.suffix in (".json", ".txt", ".xml")}
        bad = []
        for f in out.rglob("*.html"):
            for u in re.findall(r'href="([^"]+)"', f.read_text(encoding="utf-8")):
                if u.startswith(BASE) and u not in known:
                    bad.append((f.name, u))
        assert not bad, bad[:5]


def test_llms_txt_agrees_with_the_html():
    """기계 표면과 사람 표면이 갈라지면 둘 중 하나가 거짓이 된다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        llms = (out / "llms.txt").read_text(encoding="utf-8")
        m = json.loads((out / "index.json").read_text(encoding="utf-8"))
        assert m["measured_at"] in llms
        assert "측정일은 잰 날이다" in llms
        for s in m["servers"]:
            if s["rank_in_category"] == 1:
                assert s["name"] in llms, f"1위가 llms.txt에 없다: {s['name']}"


def test_unknown_paths_are_not_a_copy_of_the_front_page():
    """소프트 404 금지 — 없는 주소가 첫 화면의 200 복제본이 되면 색인이 희석된다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        f = out / "404.html"
        assert f.exists(), "404.html이 없다 — CF Pages가 첫 페이지를 200으로 내려준다"
        t = f.read_text(encoding="utf-8")
        assert 'content="noindex' in t
        assert "<loc>" not in (out / "sitemap.xml").read_text(encoding="utf-8").replace(
            "", "") or "404" not in (out / "sitemap.xml").read_text(encoding="utf-8")


def test_no_wellknown_mcp_json_is_published():
    """이 사이트는 MCP 서버가 아니라 목록이다 — 서버인 척하는 카드를 두지 않는다."""
    with tempfile.TemporaryDirectory() as tmp:
        r, out = build(tmp)
        assert r.returncode == 0, r.stderr
        assert not (out / ".well-known" / "mcp.json").exists()
