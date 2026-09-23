#!/usr/bin/env python3
"""게시한 서버가 조용히 사라지지 않는가 — 이어받기 회귀 (2026-09-14, T-2026W38-309).

계기. 2026-09-14 회차에서 지난주 게시본의 `TheNaham/koreafood-mcp` ·
`josanku/wehome-insight` · `leadbrain/korean-data-mcp`가 후보 30,508건에서 빠졌는데
**셋 다 GitHub 200으로 살아 있었다.** GitHub 검색이 질의당 상위 100건(별 순)만 주므로
별 0~2개짜리는 새 저장소가 늘어나는 것만으로 밀려난다. 수집기는 `truncated`를 정직하게
적었지만 **어느 줄이 밀려났는지는 말하지 않았다** — 그것이 이 회귀가 지키는 침묵이다.

**통과시키는 쪽 고장은 조용하다**(스킬 guard-liveness). 그래서 산출물만 보지 않고
`collect_candidates.main`·`export_candidates.main`을 실제로 돌려 **배선**을 태운다 —
모듈만 있고 아무도 부르지 않는 상태에서도 통과하는 검사는 이 사고를 다시 못 잡는다.

실행: python3 -m pytest tests/test_carryover.py -q
"""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import carryover  # noqa: E402
import filter_candidates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 실제 사건의 세 줄. 이름을 박아 두는 것이 아니라 **모양**을 박아 둔다 —
# 지난 회차에 게시됐고, 이번 회차 수집에 없고, 저장소는 200이다.
PUBLISHED = ["TheNaham/koreafood-mcp", "josanku/wehome-insight", "leadbrain/korean-data-mcp"]


def ledger_of(*names, **kw):
    led = carryover.empty_ledger()
    for n in names:
        led["items"][n] = {"name": n, "repo_url": f"https://github.com/{n}",
                           "last_remote": kw.get("remote", ""),
                           "first_published": "2026-09-07", "last_published": "2026-09-07",
                           "rounds": 1, "retired": None, "renamed_to": None}
    return led


def publish_round(led, day, name="some/other"):
    """그 날 회차가 **게시까지 성사됐다**고 원장에 적는다(export_candidates가 하는 일).

    은퇴 계수는 실행이 아니라 회차를 센다. 원장은 수집 직후·게시 전에 저장되므로,
    게시가 없으면 다음 날 재실행도 같은 회차다(codex 2026-09-16). 그래서 회차가 넘어가는
    시험은 그 사이에 게시가 있었음을 이렇게 모사한다.
    """
    carryover.record(led, {"measured_at": day, "items": [
        {"name": name, "repo_url": f"https://github.com/{name}",
         "remote": {"url": f"https://{name.split('/')[0]}.test/mcp"}}]})
    return led


def alive(path, **kw):
    return {"state": "alive", "full_name": kw.get("full_name", path),
            "repo_url": f"https://github.com/{kw.get('full_name', path)}",
            "description": kw.get("description", "korean public data search"),
            "stars": 1, "pushed": "2026-06-12", "archived": False, "why": "HTTP 200"}


# ── 되살리는가 ──────────────────────────────────────────────────────────────
def test_published_server_absent_from_sources_is_carried_forward():
    """**이 회귀가 지키는 실제 사건.** 게시했는데 안 잡히면 후보로 되살아난다."""
    led = ledger_of(*PUBLISHED)
    collected = [{"name": "other/unrelated", "repo_url": "https://github.com/other/unrelated"}]
    carried, notes = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert sorted(i["name"] for i in carried) == sorted(PUBLISHED)
    assert all(i["sources"] == ["carryover"] for i in carried)
    assert all(i["carryover"]["last_published"] == "2026-09-07" for i in carried)
    assert any("이어받기 3건" in n for n in notes), "되살렸으면 값으로 말해야 한다"
    assert all(n in " ".join(notes) for n in PUBLISHED), "어느 줄인지 이름으로 공시해야 한다"


def test_carried_item_still_faces_the_filter():
    """이어받기는 **침묵만** 면제한다 — 판정은 그대로 받는다."""
    led = ledger_of("someone/framework-thing")
    carried, _ = carryover.carry_forward(
        led, [], day="2026-09-21",
        resolve=lambda p: alive(p, description="A boilerplate framework starter for agents"))
    assert len(carried) == 1
    c = filter_candidates.classify(carried[0])
    assert c["verdict"] == "drop", "게시 이력이 판정을 면제하면 목록이 썩는다"


def test_real_incident_descriptions_pass_the_filter():
    """사건 3건이 실제 설명으로 keep까지 오는가 — 되살려 놓고 필터에서 또 떨어지면 소용없다."""
    descs = {"TheNaham/koreafood-mcp": "🇰🇷 NAHAM K-Food Export MCP — search Korean red ginseng",
             "josanku/wehome-insight": "K-STAY: 한국 숙박·관광·문화 데이터 종합 플랫폼",
             "leadbrain/korean-data-mcp": "🇰🇷 MCP server for Korean web data — Naver, Melon"}
    led = ledger_of(*PUBLISHED)
    carried, _ = carryover.carry_forward(
        led, [], day="2026-09-21", resolve=lambda p: alive(p, description=descs[p]))
    for it in carried:
        assert filter_candidates.classify(it)["verdict"] == "keep", it["name"]


# ── 중복을 만들지 않는가 ────────────────────────────────────────────────────
def test_renamed_repo_already_collected_is_not_carried_twice():
    """**개명 확인이 없으면 같은 서버가 두 줄이 된다.**

    실측 2026-09-14: `hwain-hwang/Real-Estate-Location-Analyzer_MCP`가 원장에서
    사라진 것처럼 보였지만 `hwain-ai/…`로 개명해 이번 회차에 이미 들어와 있었다.
    GitHub이 옛 경로를 301로 이어 주므로 옛 이름도 200으로 살아 보인다.
    """
    old, new = "hwain-hwang/Real-Estate_MCP", "hwain-ai/Real-Estate_MCP"
    led = ledger_of(old)
    collected = [{"name": new, "repo_url": f"https://github.com/{new}"}]
    carried, notes = carryover.carry_forward(
        led, collected, resolve=lambda p: alive(p, full_name=new), day="2026-09-21")
    assert carried == [], "개명 후 이름으로 이미 있는데 옛 이름을 또 실었다"
    assert led["items"][old]["renamed_to"] == new
    assert any("개명" in n for n in notes)


def test_repo_url_match_prevents_duplicate_under_another_name():
    """이름이 달라도 저장소가 같으면 이미 있는 것이다(레지스트리명 ↔ GitHub명)."""
    led = ledger_of("sallim-app/contract-compass")
    collected = [{"name": "app.sallim/contract-compass",
                  "repo_url": "https://github.com/sallim-app/contract-compass/"}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert carried == [], "주소가 같은데 이름이 다르다고 한 줄 더 실었다"


def test_sibling_servers_from_one_repo_do_not_mask_each_other():
    """**저장소가 같다고 같은 서버는 아니다**(merge_sources의 2026-08-31 실측).

    `lead788/apick-mcp` 한 저장소가 `app.apick/{all,business,…}` 9개를 내고 주소가 전부
    다르다. 저장소만 보고 '이미 있다'로 읽으면 그중 하나가 빠진 회차에 **형제 줄이 남아
    있다는 이유로 이어받기가 조용히 안 걸린다** — 이어받기가 막으려는 바로 그 증발이다.
    """
    repo = "https://github.com/lead788/apick-mcp"
    led = ledger_of("app.apick/all", remote="https://apick.app/mcp/all")
    led["items"]["app.apick/all"]["repo_url"] = repo
    collected = [{"name": "app.apick/business", "repo_url": repo,
                  "remotes": [{"url": "https://apick.app/mcp/business"}]}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert [i["name"] for i in carried] == ["app.apick/all"], "형제 줄이 이어받기를 가렸다"


def test_address_less_repo_row_does_not_mask_its_sibling_servers():
    """**주소를 안 밝힌 저장소 줄 하나가 형제 전부를 가리면 안 된다**(T-2026W39-49).

    종전 식은 "저장소가 같고 이번 회차 그 저장소 줄들이 주소를 안 밝혔으면(`not their`)
    같은 서버"로 읽었다. GitHub 검색 줄에는 주소가 없으므로(주소는 보강 단계가 찾는다),
    레지스트리가 `app.apick/*`를 통째로 못 돌려준 회차에 소스 저장소 한 줄만 잡히면
    `their`가 빈 집합이 되고 **형제 셋이 다 '이미 있다'로 읽혀 경계 공시 한 줄 없이
    표에서 증발한다.** 그 상태는 다음 회차에도 같아서 영구 누락이다.
    """
    repo = "https://github.com/lead788/apick-mcp"
    led = ledger_of("app.apick/all", remote="https://apick.app/mcp/all")
    for n, ep in (("app.apick/business", "https://apick.app/mcp/business"),
                  ("app.apick/finance", "https://apick.app/mcp/finance")):
        led["items"][n] = {**led["items"]["app.apick/all"], "name": n, "last_remote": ep}
    for n in led["items"]:
        led["items"][n]["repo_url"] = repo
    # 이번 회차에 잡힌 것은 소스 저장소 한 줄뿐이고, 그 줄은 주소를 안 밝혔다.
    collected = [{"name": "lead788/apick-mcp", "repo_url": repo}]
    carried, notes = carryover.carry_forward(
        led, collected, resolve=lambda p: alive(p, full_name="lead788/apick-mcp"),
        day="2026-09-21")
    assert sorted(i["name"] for i in carried) == ["app.apick/all", "app.apick/business",
                                                  "app.apick/finance"], \
        "주소 없는 저장소 줄 하나가 형제 서버 전부를 조용히 가렸다"
    assert all(i["remotes"][0]["url"].startswith("https://apick.app/mcp/") for i in carried)
    assert any("이어받기 3건" in n for n in notes), "되살렸으면 값으로 공시해야 한다"


def test_alias_pair_without_addresses_still_counts_as_present():
    """주소가 **양쪽 다** 없으면 저장소가 유일한 신원이다 — 별칭 쌍은 그대로 안 이어받는다.

    원장 430건 중 300건이 주소 없이 남아 있고, 그중 상당수가 레지스트리명↔GitHub명
    별칭 쌍이다(`io.github.fieldcure/publicdata-kr` ↔ `fieldcure/fieldcure-mcp-publicdata`).
    위 수리가 이쪽까지 열면 매 회차 별칭이 한 줄씩 더 실린다.
    """
    repo = "https://github.com/fieldcure/fieldcure-mcp-publicdata"
    led = ledger_of("io.github.fieldcure/publicdata-kr")
    led["items"]["io.github.fieldcure/publicdata-kr"]["repo_url"] = repo
    collected = [{"name": "fieldcure/fieldcure-mcp-publicdata", "repo_url": repo}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert carried == [], "주소가 양쪽 다 없는 별칭 쌍을 한 줄 더 실었다"


def test_single_address_repo_alias_is_not_revived_as_a_second_row():
    """저장소로 게시된 주소가 **하나뿐**이면 이름이 둘이어도 한 서버다 — 안 이어받는다.

    위 수리의 반대쪽 난간(실측 2026-09-23). 무조건 되살리게 고치면 지금 원장·후보에서
    `smilemin07/korean-rnd-regs-mcp`·`kokogo100/ragalgo-mcp-server` 2건이 매 회차 한 줄씩
    더 실린다 — 둘 다 형제가 아니라 레지스트리명↔GitHub명 별칭이다. 추측하지 않고
    **원장이 아는 주소 수**로 가른다.
    """
    repo = "https://github.com/smilemin07/korean-rnd-regs-mcp"
    ep = "https://mcp.rndmanagers.org/mcp"
    led = ledger_of("smilemin07/korean-rnd-regs-mcp", remote=ep)
    led["items"]["io.github.smilemin07/korean-rnd-regs-mcp"] = {
        **led["items"]["smilemin07/korean-rnd-regs-mcp"],
        "name": "io.github.smilemin07/korean-rnd-regs-mcp", "last_remote": ""}
    for n in led["items"]:
        led["items"][n]["repo_url"] = repo
    # 이번 회차엔 레지스트리 이름만 잡혔고, 그 줄은 주소를 안 밝혔다(패키지형 등록).
    collected = [{"name": "io.github.smilemin07/korean-rnd-regs-mcp", "repo_url": repo}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert carried == [], "한 주소짜리 저장소의 별칭을 한 줄 더 실었다"


def test_same_endpoint_under_another_name_counts_as_present():
    """주소가 같으면 같은 서버다 — 이름이 달라도 이어받지 않는다(질의문자열은 무시)."""
    led = ledger_of("sallim-app/contract-compass", remote="https://contract.sallim.app/mcp")
    collected = [{"name": "app.sallim/contract-compass", "repo_url": "",
                  "remotes": [{"url": "https://contract.sallim.app/mcp?via=official"}]}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert carried == []


def test_also_known_as_counts_as_present():
    """엔드포인트 병합으로 옮겨진 이름도 '이번 회차에 있다'로 친다."""
    led = ledger_of("b/two")
    collected = [{"name": "a/one", "repo_url": "https://github.com/a/one",
                  "also_known_as": ["b/two"]}]
    carried, _ = carryover.carry_forward(led, collected, resolve=alive, day="2026-09-21")
    assert carried == []


# ── 은퇴는 실측으로만 ───────────────────────────────────────────────────────
def test_gone_repo_is_retired_only_after_repeated_evidence():
    """404는 소멸의 *징후*이지 증거가 아니다 — 연속 회차가 같아야 은퇴다."""
    led = ledger_of("dead/repo")
    led["items"]["dead/repo"]["last_remote"] = ""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    carried, notes = carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    assert carried == []
    assert led["items"]["dead/repo"]["retired"] is None, "한 번 보고 끊었다"
    assert any("확인 중" in n for n in notes), "보류를 값으로 말해야 한다"
    publish_round(led, "2026-09-21")
    carried, notes = carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["dead/repo"]["retired"]["why"] == "저장소 소멸 실측(HTTP 404 × 2회차)"
    assert any("은퇴" in n and "HTTP 404" in n for n in notes)


def test_private_flip_does_not_erase_a_server_with_a_known_address():
    """**공개 자격에는 비공개 전환도 404다**(codex 2026-09-15).

    잴 주소가 있으면 저장소가 무엇이든 서버는 두드려 보면 답한다 — 404 하나로
    살아서 돌아가는 남의 서버를 우리 목록에서 영구히 지우지 않는다.
    """
    led = ledger_of("went/private", remote="https://still.test/mcp")
    for _ in range(3):
        carried, notes = carryover.carry_forward(
            led, [], resolve=lambda p: {"state": "gone", "why": "HTTP 404"}, day="2026-09-21")
    assert [i["name"] for i in carried] == ["went/private"]
    assert carried[0]["remotes"][0]["url"] == "https://still.test/mcp"
    assert led["items"]["went/private"]["retired"] is None
    assert any("비공개 전환 가능" in n for n in notes)


def test_alive_again_clears_the_gone_streak():
    """중간에 한 번 살아 있으면 연속이 끊긴다 — 누적이 아니라 연속이다."""
    led = ledger_of("flaky/repo")
    led["items"]["flaky/repo"]["last_remote"] = ""
    carryover.carry_forward(led, [], day="2026-09-21",
                            resolve=lambda p: {"state": "gone", "why": "HTTP 404"})
    assert led["items"]["flaky/repo"]["gone_streak"] == 1
    carryover.carry_forward(led, [], resolve=alive, day="2026-09-28")
    assert led["items"]["flaky/repo"]["gone_streak"] == 0


def test_reappearing_in_collection_clears_the_gone_streak():
    """이번 회차에 다시 잡혔으면 연속이 끊긴다(codex 2026-09-16).

    되살리기 대상이 아니라 `continue`로 빠지는 길이라 계수 초기화가 빠져 있었다.
    그대로 두면 옛 404 하나가 원장에 남아 몇 회차 뒤 404 하나와 붙어 **연속 2회차**로
    읽히고, 살아 있는 남의 서버가 은퇴한다.
    """
    led = ledger_of("flaky/repo")
    led["items"]["flaky/repo"]["last_remote"] = ""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    assert led["items"]["flaky/repo"]["gone_streak"] == 1
    # 이번 회차 수집에 다시 들어왔다 — 두드릴 것도 없다.
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [{"name": "flaky/repo",
                                   "repo_url": "https://github.com/flaky/repo"}],
                            resolve=gone, day="2026-09-28")
    assert led["items"]["flaky/repo"]["gone_streak"] == 0, "다시 잡혔는데 연속을 안 끊었다"
    publish_round(led, "2026-09-28")
    carryover.carry_forward(led, [], resolve=gone, day="2026-10-05")
    assert led["items"]["flaky/repo"]["retired"] is None, "비연속 404 두 번으로 은퇴시켰다"


def test_unknown_between_two_404s_does_not_retire():
    """404·unknown·404는 '연속 2회차 같은 답'이 아니다(codex 2026-09-16).

    은퇴 공시가 그렇게 말하는데 계수는 누적이었다 — 공시와 코드가 갈리면 공시가 거짓이 된다.
    """
    led = ledger_of("flappy/repo")
    led["items"]["flappy/repo"]["last_remote"] = ""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    unknown = lambda p: {"state": "unknown", "why": "HTTP 403"}    # noqa: E731
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=unknown, day="2026-09-28")
    assert led["items"]["flappy/repo"]["gone_streak"] == 0, "404가 아닌 답이 연속을 안 끊었다"
    publish_round(led, "2026-09-28")
    carryover.carry_forward(led, [], resolve=gone, day="2026-10-05")
    assert led["items"]["flappy/repo"]["retired"] is None, "비연속 404 두 번으로 은퇴시켰다"


def test_budget_exhaustion_neither_counts_nor_clears_the_streak():
    """**안 물어본 회차는 답이 아니다**(codex 2026-09-16).

    예산이 소진돼 확인을 미룬 회차가 연속을 끊으면, 물어보지도 않고 지난 회차의 404
    증거를 우리가 지우는 것이다 — 세는 쪽으로도 지우는 쪽으로도 움직이지 않는다.
    """
    led = ledger_of("dead/repo")
    led["items"]["dead/repo"]["last_remote"] = ""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    assert led["items"]["dead/repo"]["gone_streak"] == 1
    publish_round(led, "2026-09-21")
    _, notes = carryover.carry_forward(led, [], resolve=gone, day="2026-09-28", budget=0)
    assert any("확인 미룸" in n for n in notes), "미룬 것을 공시하지 않았다"
    assert led["items"]["dead/repo"]["gone_streak"] == 1, "안 물어보고 연속을 끊었다"
    assert led["items"]["dead/repo"]["retired"] is None, "안 물어보고 회차를 셌다"


def test_unknown_is_not_death():
    """403 한도·네트워크 실패로 사망 선고를 하지 않는다(기치 ②: 못 봄 ≠ 없음)."""
    led = ledger_of("maybe/alive")
    carried, notes = carryover.carry_forward(
        led, [], resolve=lambda p: {"state": "unknown", "why": "HTTP 403"}, day="2026-09-21")
    assert [i["name"] for i in carried] == ["maybe/alive"]
    assert led["items"]["maybe/alive"]["retired"] is None
    assert any("미확인" in n for n in notes)


def test_retired_entry_is_not_probed_again():
    """은퇴한 줄은 매주 다시 두드리지 않는다 — 남의 서버에 대한 예의이자 속도다."""
    led = ledger_of("dead/repo")
    led["items"]["dead/repo"]["retired"] = {"day": "2026-09-14",
                                            "why": "저장소 소멸 실측(HTTP 404)"}
    called = []
    carryover.carry_forward(led, [], resolve=lambda p: called.append(p) or alive(p),
                            day="2026-09-21")
    assert called == []


def test_republished_server_un_retires():
    """다시 게시되면 은퇴가 풀린다 — 은퇴는 상태이지 낙인이 아니다."""
    led = ledger_of("back/again")
    led["items"]["back/again"]["retired"] = {"day": "2026-09-14",
                                             "why": "저장소 소멸 실측(HTTP 404)"}
    carryover.record(led, {"measured_at": "2026-09-21",
                           "items": [{"name": "back/again",
                                      "repo_url": "https://github.com/back/again"}]})
    assert led["items"]["back/again"]["retired"] is None


def test_registry_only_entry_carries_its_last_endpoint():
    """GitHub 저장소가 없는 등록은 소멸을 확인할 통로가 없다 — 마지막 주소째로 이어받는다."""
    led = ledger_of("app.example/thing", remote="https://ex.test/mcp")
    led["items"]["app.example/thing"]["repo_url"] = ""
    carried, notes = carryover.carry_forward(led, [], resolve=alive, day="2026-09-21")
    assert carried[0]["remotes"] == [{"type": "streamable-http",
                                      "url": "https://ex.test/mcp", "needs_auth": False}]
    assert any("미확인" in n for n in notes)


# ── 원장이 게시본보다 뒤처지지 않는가 ──────────────────────────────────────
def test_record_is_idempotent_within_a_round():
    """같은 회차를 두 번 적어도 rounds가 부풀지 않는다(export를 두 번 돌릴 수 있다)."""
    led = carryover.empty_ledger()
    m = {"measured_at": "2026-09-21", "items": [{"name": "a/one", "repo_url": "u"}]}
    carryover.record(led, m)
    carryover.record(led, m)
    assert led["items"]["a/one"]["rounds"] == 1


def test_ledger_covers_every_published_row():
    """**게시본에 있는데 원장에 없으면 그 줄은 다음 회차에 못 이어받는다.**"""
    led = carryover.load(str(ROOT / "published_history.json"))
    published = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    missing = [i["name"] for i in published["items"] if i["name"] not in led["items"]]
    assert not missing, f"게시본에 실렸는데 게시 이력 원장에 없다: {missing[:5]}"


# ── 배선을 태운다 ───────────────────────────────────────────────────────────
def test_collect_actually_calls_carryover(tmp_path, monkeypatch):
    """`collect_candidates.main`이 실제로 이어받는가 — 모듈만 있고 안 부르면 사고는 반복된다."""
    import collect_candidates
    monkeypatch.setattr(collect_candidates, "from_registry", lambda: ({}, []))
    monkeypatch.setattr(collect_candidates, "from_github", lambda t: ({}, []))
    monkeypatch.setattr(collect_candidates, "from_mcpmoa", lambda: ({}, []))
    monkeypatch.setattr(carryover, "resolve_github", lambda p, tok=None, **kw: alive(p))
    led = ledger_of("lost/but-alive")
    (tmp_path / "published_history.json").write_text(json.dumps(led, ensure_ascii=False),
                                                     encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert collect_candidates.main() == 0
    raw = json.loads((tmp_path / "candidates_raw.json").read_text(encoding="utf-8"))
    names = [i["name"] for i in raw["items"]]
    assert names == ["lost/but-alive"], f"이어받기가 수집 산출물에 안 들어갔다: {names}"
    assert any("이어받기" in b for b in raw["boundaries"]), "경계 공시에 없다"


def test_export_records_the_ledger_and_lists_dropped_carryovers(tmp_path):
    """게시하면서 원장을 적고, 이어받은 줄은 drop이어도 이름째로 싣는가."""
    m = {"measured": 1, "unmeasurable": 0, "boundaries": [], "criteria_note": "t",
         "measured_at": "2026-09-21", "axes_at": "2026-09-21",
         "items": [{"name": "a/one", "repo_url": "https://github.com/a/one",
                    "remote": {"url": "https://a.test/mcp", "status": "live",
                               "reachable": True, "tool_count": 1}}]}
    (tmp_path / "measured.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "candidates_filtered.json").write_text(json.dumps({
        "buckets": {}, "boundaries": [],
        "items": [{"name": "gone/topic", "repo_url": "https://github.com/gone/topic",
                   "verdict": "drop", "why": "데이터 제공형이 아니다(framework)",
                   "carryover": {"last_published": "2026-09-07", "state": "alive"}},
                  {"name": "plain/drop", "repo_url": "https://github.com/plain/drop",
                   "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림"}]},
        ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "export_candidates.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    led = json.loads((tmp_path / "published_history.json").read_text(encoding="utf-8"))
    assert "a/one" in led["items"], "게시하고도 원장에 안 적었다 — 다음 회차에 못 이어받는다"
    assert led["items"]["a/one"]["last_published"] == "2026-09-21"
    cand = json.loads((tmp_path / "candidates.json").read_text(encoding="utf-8"))
    listed = {i["name"] for i in cand["items"]}
    assert "gone/topic" in listed, "이어받은 줄이 drop 통에서 또 조용히 사라졌다"
    assert "plain/drop" not in listed, "보통 drop까지 싣게 되면 3만 건이 실린다"


def test_previously_published_row_is_named_even_when_collected_and_dropped(tmp_path):
    """이번 회차에 **수집은 됐는데** 필터에서 떨어진 옛 게시 줄도 이름째 실린다.

    `carryover` 표식은 수집 원천이 안 돌려준 줄에만 붙는다 — 그래서 표식만 보면
    '수집됐지만 drop'인 줄이 사유별 건수로만 남아 독자에게는 똑같이 조용히 사라진다
    (codex 교차검증 2026-09-16, 실측 1건). 기준은 표식이 아니라 게시 이력이다.
    """
    (tmp_path / "measured.json").write_text(json.dumps(
        {"measured": 0, "unmeasurable": 0, "boundaries": [], "criteria_note": "t",
         "measured_at": "2026-09-21", "axes_at": "2026-09-21", "items": []},
        ensure_ascii=False), encoding="utf-8")
    led = carryover.empty_ledger()
    led["items"]["old/published"] = {
        "name": "old/published", "repo_url": "https://github.com/old/published",
        "last_remote": "", "first_published": "2026-09-07", "last_published": "2026-09-14",
        "rounds": 2, "retired": None, "renamed_to": None}
    (tmp_path / "published_history.json").write_text(json.dumps(led, ensure_ascii=False),
                                                     encoding="utf-8")
    (tmp_path / "candidates_filtered.json").write_text(json.dumps({
        "buckets": {}, "boundaries": [],
        "items": [{"name": "old/published", "repo_url": "https://github.com/old/published",
                   "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림"},
                  {"name": "plain/drop", "repo_url": "https://github.com/plain/drop",
                   "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림"}]},
        ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "export_candidates.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    cand = json.loads((tmp_path / "candidates.json").read_text(encoding="utf-8"))
    listed = {i["name"] for i in cand["items"]}
    assert "old/published" in listed, "한 번 게시한 줄이 표식이 없다는 이유로 또 조용히 사라졌다"
    assert "plain/drop" not in listed, "게시한 적 없는 drop까지 실으면 3만 건이 실린다"


def test_renamed_published_row_is_named_under_its_new_name(tmp_path):
    """개명한 옛 게시 줄이 새 이름으로 수집돼 drop되어도 이름째 실린다.

    원장에는 옛 이름만 있으므로 이름만 대조하면 개명 한 번으로 다시 조용해진다
    (codex 교차검증 2026-09-16). 이어받기가 확인해 둔 `renamed_to`가 그 다리다.
    """
    (tmp_path / "measured.json").write_text(json.dumps(
        {"measured": 0, "unmeasurable": 0, "boundaries": [], "criteria_note": "t",
         "measured_at": "2026-09-21", "axes_at": "2026-09-21", "items": []},
        ensure_ascii=False), encoding="utf-8")
    led = carryover.empty_ledger()
    led["items"]["old/name"] = {
        "name": "old/name", "repo_url": "https://github.com/old/name", "last_remote": "",
        "first_published": "2026-09-07", "last_published": "2026-09-14", "rounds": 2,
        "retired": None, "renamed_to": "new/name"}
    (tmp_path / "published_history.json").write_text(json.dumps(led, ensure_ascii=False),
                                                     encoding="utf-8")
    (tmp_path / "candidates_filtered.json").write_text(json.dumps({
        "buckets": {}, "boundaries": [],
        "items": [{"name": "new/name", "repo_url": "https://github.com/new/name",
                   "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림"}]},
        ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "export_candidates.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    cand = json.loads((tmp_path / "candidates.json").read_text(encoding="utf-8"))
    assert "new/name" in {i["name"] for i in cand["items"]}, "개명한 게시 줄이 또 조용히 사라졌다"


def _export_run(tmp_path, led, items):
    """`export_candidates`를 tmp에서 실제로 돌리고 `candidates.json`의 이름들을 준다."""
    (tmp_path / "measured.json").write_text(json.dumps(
        {"measured": 0, "unmeasurable": 0, "boundaries": [], "criteria_note": "t",
         "measured_at": "2026-09-21", "axes_at": "2026-09-21", "items": []},
        ensure_ascii=False), encoding="utf-8")
    (tmp_path / "published_history.json").write_text(json.dumps(led, ensure_ascii=False),
                                                     encoding="utf-8")
    (tmp_path / "candidates_filtered.json").write_text(json.dumps(
        {"buckets": {}, "boundaries": [], "items": items}, ensure_ascii=False),
        encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "export_candidates.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    cand = json.loads((tmp_path / "candidates.json").read_text(encoding="utf-8"))
    return {i["name"] for i in cand["items"]}


def test_renamed_row_is_named_by_its_address_when_renamed_to_was_never_written(tmp_path):
    """**이름은 개명 한 번에 끊긴다 — 주소는 안 끊긴다**(T-2026W39-49).

    `renamed_to`는 이어받기가 저장소를 두드려 개명을 확인했을 때만 적힌다. 그런데
    이어받기는 그 서버가 이번 회차에 이미 들어와 있으면 두드리기 전에 빠지고, 개명한
    서버가 새 이름으로 수집된 회차가 바로 그 경우다 — 그래서 원장에는 옛 이름만 남는다
    (실측: 원장 430건 중 `renamed_to`가 붙은 줄 0건). 그 상태에서 새 이름이 필터에
    떨어지면 이름 대조가 실패해 다시 사유별 건수로만 남는다.
    """
    ep = "https://svc.test/mcp"
    led = carryover.empty_ledger()
    led["items"]["old/name"] = {
        "name": "old/name", "repo_url": "https://github.com/old/name", "last_remote": ep,
        "first_published": "2026-09-07", "last_published": "2026-09-14", "rounds": 2,
        "retired": None, "renamed_to": None}          # ← 개명이 원장에 안 적혔다
    listed = _export_run(tmp_path, led, [
        {"name": "new/name", "repo_url": "https://github.com/new/name", "verdict": "drop",
         "why": "한국 관련 신호 0 — 검색어에 우연히 걸림",
         "remotes": [{"url": ep + "?via=official"}]},
        {"name": "plain/drop", "repo_url": "https://github.com/plain/drop",
         "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림",
         "remotes": [{"url": "https://never.test/mcp"}]}])
    assert "new/name" in listed, "개명한 게시 줄이 이름만 대조하다 또 조용히 사라졌다"
    assert "plain/drop" not in listed, "게시한 적 없는 drop까지 실으면 3만 건이 실린다"


def test_retired_row_collected_again_is_still_named_when_dropped(tmp_path):
    """은퇴는 "이어받기를 끝냈다"이지 "게시한 적 없다"가 아니다.

    은퇴한 줄이 이번 회차에 **다시 수집됐다면** 은퇴의 전제(저장소 소멸)가 이미 뒤집힌
    것이다 — 그 줄이야말로 drop 사유를 달고 이름째 보여야 한다.
    """
    led = carryover.empty_ledger()
    led["items"]["was/retired"] = {
        "name": "was/retired", "repo_url": "https://github.com/was/retired",
        "last_remote": "", "first_published": "2026-08-31", "last_published": "2026-09-07",
        "rounds": 2, "renamed_to": None,
        "retired": {"day": "2026-09-14", "round": "2026-09-07", "why": "저장소 소멸 실측"}}
    listed = _export_run(tmp_path, led, [
        {"name": "was/retired", "repo_url": "https://github.com/was/retired",
         "verdict": "drop", "why": "한국 관련 신호 0 — 검색어에 우연히 걸림"}])
    assert "was/retired" in listed, "은퇴했다는 이유로 게시 이력이 지워졌다"


def test_registry_named_row_keeps_its_name_when_source_repo_is_alive():
    """레지스트리 이름으로 게시된 줄은 저장소 이름으로 바뀌지 않는다 — 신원이 주소이기 때문."""
    led = ledger_of("app.apick/all", remote="https://apick.app/mcp/all")
    led["items"]["app.apick/all"]["repo_url"] = "https://github.com/lead788/apick-mcp"
    carried, _ = carryover.carry_forward(
        led, [], resolve=lambda p: alive(p, full_name="lead788/apick-mcp"), day="2026-09-21")
    assert [i["name"] for i in carried] == ["app.apick/all"]
    assert carried[0]["remotes"][0]["url"] == "https://apick.app/mcp/all"


def test_source_repo_404_does_not_kill_a_registry_named_server():
    """**저장소는 거처이고 주소가 신원이다.** 소스가 지워져도 서버가 죽은 것이 아니다."""
    led = ledger_of("app.apick/all", remote="https://apick.app/mcp/all")
    led["items"]["app.apick/all"]["repo_url"] = "https://github.com/lead788/apick-mcp"
    carried, notes = carryover.carry_forward(
        led, [], resolve=lambda p: {"state": "gone", "why": "HTTP 404"}, day="2026-09-21")
    assert [i["name"] for i in carried] == ["app.apick/all"]
    assert led["items"]["app.apick/all"]["retired"] is None, "남의 서버에 사망 선고를 했다"
    assert any("미확인" in n for n in notes)


def test_github_named_row_does_not_inherit_a_stale_endpoint():
    """GitHub으로 신원이 확인된 줄엔 옛 주소를 안 붙인다 — 보강이 지금 주소를 찾는다."""
    led = ledger_of("a/one", remote="https://old.test/mcp")
    carried, _ = carryover.carry_forward(led, [], resolve=alive, day="2026-09-21")
    assert "remotes" not in carried[0]


def test_aliases_of_one_server_are_not_all_revived(tmp_path):
    """**이어받기의 반대쪽 실패** — 한 서버를 여러 줄로 되살리지 않는다(codex 2026-09-15).

    원장에는 같은 서버가 여러 이름으로 남는다(엔드포인트 병합으로 옮겨진 이름을 게시
    이력으로 같이 적으므로). 레지스트리 스윕이 한 번 실패해 셋이 동시에 안 잡히는
    회차에 순회 중 누적을 안 하면 셋을 다 되살려 같은 서버가 세 줄이 된다.
    """
    ep = "https://contract.sallim.app/mcp"
    led = ledger_of("app.sallim/contract-compass", "build.naru/contract-compass",
                    "sallim-app/contract-compass", remote=ep)
    for n in led["items"]:
        led["items"][n]["repo_url"] = "https://github.com/sallim-app/contract-compass"
    carried, _ = carryover.carry_forward(led, [], resolve=alive, day="2026-09-21")
    assert len(carried) == 1, [i["name"] for i in carried]


def test_accumulation_does_not_mask_real_siblings():
    """누적이 형제 서버를 가리면 안 된다 — 주소가 다르면 둘 다 되살아난다."""
    repo = "https://github.com/lead788/apick-mcp"
    led = ledger_of("app.apick/all", remote="https://apick.app/mcp/all")
    led["items"]["app.apick/business"] = {**led["items"]["app.apick/all"],
                                          "name": "app.apick/business",
                                          "last_remote": "https://apick.app/mcp/business"}
    for n in led["items"]:
        led["items"][n]["repo_url"] = repo
    carried, _ = carryover.carry_forward(led, [], resolve=alive, day="2026-09-21")
    assert sorted(i["name"] for i in carried) == ["app.apick/all", "app.apick/business"]


def test_dropped_carryover_is_listed_but_not_counted_as_population(tmp_path):
    """**싣는 것과 세는 것은 다르다**(codex 2026-09-15).

    이어받았다가 주제 밖으로 판정된 줄은 독자에게 이름째 보여야 하지만(침묵 방지),
    측정 모집단에 들어가면 "한국 관련성은 통과했는데 안 잰 것"에 거짓 라벨이 붙는다.
    """
    import population
    (tmp_path / "candidates.json").write_text(json.dumps({"items": [
        {"name": "keep/one", "verdict": "keep"},
        {"name": "review/two", "verdict": "review"},
        {"name": "carried/off-topic", "verdict": "drop",
         "carryover": {"last_published": "2026-09-07"}}]}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "classification.json").write_text(
        json.dumps({"items": {}}, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "measured.json").write_text(
        json.dumps({"items": []}, ensure_ascii=False), encoding="utf-8")
    pop = population.summary(str(tmp_path / "candidates.json"),
                             str(tmp_path / "classification.json"),
                             str(tmp_path / "measured.json"))
    assert pop["total"] == 2, "drop된 이어받기 줄이 후보 총계를 부풀렸다"
    assert "carried/off-topic" not in {i["name"] for i in pop["not_measured"]}


def test_unreadable_carryover_is_review_not_drop():
    """**없는 근거로 내리는 판정이 `drop`이면 이어받기가 스스로를 무효로 만든다.**

    저장소가 404(비공개 전환 포함)면 설명이 빈 채로 되살아난다. 그 상태의 `drop`은
    그 서버에 대한 판정이 아니라 우리가 입력을 못 구했다는 사실이다
    (실측: `haklaekim/public-data-lens` — 한국 공공데이터 카탈로그 서버).
    """
    led = ledger_of("haklaekim/public-data-lens", remote="https://service.test/mcp")
    carried, _ = carryover.carry_forward(
        led, [], resolve=lambda p: {"state": "gone", "why": "HTTP 404"}, day="2026-09-21")
    c = filter_candidates.classify(carried[0])
    assert c["verdict"] == "review", c
    assert "설명을 못 읽어" in c["why"]


def test_readable_carryover_is_still_judged_normally():
    """설명이 있으면 이어받기여도 보통대로 판정한다 — 면제가 아니다."""
    led = ledger_of("someone/framework-thing")
    carried, _ = carryover.carry_forward(
        led, [], day="2026-09-21",
        resolve=lambda p: alive(p, description="A boilerplate framework starter for agents"))
    assert filter_candidates.classify(carried[0])["verdict"] == "drop"


def test_same_day_rerun_does_not_count_as_a_second_round():
    """**회차를 세는 것이지 실행을 세는 것이 아니다**(codex 2026-09-15)."""
    led = ledger_of("dead/repo")
    led["items"]["dead/repo"]["last_remote"] = ""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    for _ in range(3):
        carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    assert led["items"]["dead/repo"]["gone_streak"] == 1, "같은 날 재실행을 회차로 셌다"
    assert led["items"]["dead/repo"]["retired"] is None
    # **게시 전 재실행은 날짜가 달라도 같은 회차다**(codex 2026-09-16). 원장은 수집 직후에
    # 저장되므로, 뒤 단계가 깨져 게시가 안 된 회차를 다음 날 다시 돌리는 것은 실행 두 번이지
    # 회차 두 번이 아니다 — 그걸 회차로 세면 살아 있을지 모르는 서버가 하루 만에 은퇴한다.
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-22")
    assert led["items"]["dead/repo"]["gone_streak"] == 1, "게시 없는 다음 날 재실행을 회차로 셌다"
    assert led["items"]["dead/repo"]["retired"] is None
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["dead/repo"]["retired"] is not None


def test_retirement_written_before_publishing_is_not_final():
    """**게시되지 않은 회차의 은퇴는 확정이 아니다**(T-2026W39-49).

    원장은 수집 직후·게시 전에 저장된다. `retired`가 박히는 순간 순회가 맨 위에서
    건너뛰므로 다시는 두드리지 않는데, 뒤 단계가 깨져 그 회차가 끝내 게시되지 않아도
    은퇴만은 남는다 — 은퇴한 줄은 이어받지도, drop 이름으로 싣지도 않으니 그 서버는
    **경계 공시 한 줄 없이 공개 목록에서 영구히 사라진다.** 게시가 성사될 때까지는
    보통 줄처럼 다시 확인해야 한다.
    """
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    led = ledger_of("flipped/private")
    led["items"]["flipped/private"]["last_remote"] = ""
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["flipped/private"]["retired"] is not None, "연속 2회차인데 안 적었다"

    # 이 회차(09-28)는 끝내 게시되지 않았다 — 다음 날 재실행하면 다시 확인해야 한다.
    called = []
    _, notes = carryover.carry_forward(
        led, [], resolve=lambda p: called.append(p) or alive(p), day="2026-09-29")
    assert "flipped/private" in called, "게시 전 은퇴를 확정으로 읽고 다시 안 두드렸다"
    assert led["items"]["flipped/private"]["retired"] is None, "200을 받고도 은퇴가 안 풀렸다"
    assert any("은퇴 재확인" in n for n in notes), "재확인을 값으로 공시하지 않았다"


def test_round_counter_waits_for_the_deploy_stamp(tmp_path):
    """**'게시'는 `record()`가 아니라 독자가 새 값을 본 것이다**(codex 교차검증 2026-09-23).

    `record()`는 `export_candidates.py`가 렌더·배포보다 먼저 부른다 — 그것만으로 회차를
    넘기면 배포가 실패해 라이브가 낡은 채로 남은 회차에도 계수가 전진해 잠정 은퇴가
    굳는다. 도장(`mark_deployed`)이 찍힌 원장은 그 도장을 회차의 신원으로 쓴다.
    """
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    path = str(tmp_path / "published_history.json")
    led = ledger_of("maybe/dead")
    led["items"]["maybe/dead"]["last_remote"] = ""
    led["last_deployed"] = "2026-09-07"
    carryover.save(led, path)

    led = carryover.load(path)
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    assert led["items"]["maybe/dead"]["gone_streak"] == 1
    # export는 돌았지만(=record) 배포가 실패했다 — 도장이 없으니 같은 회차다.
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["maybe/dead"]["gone_streak"] == 1, "배포가 실패한 회차를 회차로 셌다"
    assert led["items"]["maybe/dead"]["retired"] is None

    # 라이브 재검증까지 통과했다 — 이제 회차가 넘어간다.
    carryover.save(led, path)
    carryover.mark_deployed("2026-09-28", path)
    led = carryover.load(path)
    carryover.carry_forward(led, [], resolve=gone, day="2026-10-05")
    assert led["items"]["maybe/dead"]["gone_streak"] == 2
    assert led["items"]["maybe/dead"]["retired"] is not None, "도장을 찍었는데도 안 셌다"


def test_retirement_becomes_final_once_its_round_is_published():
    """유예이지 무효화가 아니다 — 회차가 게시되면 은퇴는 그대로 확정이고 다시 안 두드린다."""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    led = ledger_of("really/dead")
    led["items"]["really/dead"]["last_remote"] = ""
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["really/dead"]["retired"]["round"] == "2026-09-21"
    publish_round(led, "2026-09-28")                     # 그 회차가 게시됐다
    called = []
    carryover.carry_forward(led, [], resolve=lambda p: called.append(p) or alive(p),
                            day="2026-10-05")
    assert "really/dead" not in called, "확정된 은퇴를 매주 다시 두드린다"
    assert led["items"]["really/dead"]["retired"] is not None


def test_reappearing_in_collection_undoes_an_unconfirmed_retirement():
    """게시 전 은퇴인데 그 서버가 이번 회차 수집에 다시 들어왔다 — 은퇴가 풀려야 한다."""
    gone = lambda p: {"state": "gone", "why": "HTTP 404"}          # noqa: E731
    led = ledger_of("came/back")
    led["items"]["came/back"]["last_remote"] = ""
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-21")
    publish_round(led, "2026-09-21")
    carryover.carry_forward(led, [], resolve=gone, day="2026-09-28")
    assert led["items"]["came/back"]["retired"] is not None
    carryover.carry_forward(led, [{"name": "came/back",
                                   "repo_url": "https://github.com/came/back"}],
                            resolve=gone, day="2026-09-29")
    assert led["items"]["came/back"]["retired"] is None, "다시 잡혔는데 은퇴가 남았다"
    assert led["items"]["came/back"]["gone_streak"] == 0


def test_resolve_budget_defers_instead_of_dropping():
    """수집 원천이 통째로 실패한 회차 — 확인은 미루되 **버리지는 않는다**.

    요청당 20초를 원장 전체에 직렬로 곱하면 파이프라인이 몇 시간 멈춘다(codex 2026-09-15).
    상한을 걸되, 상한 밖의 줄을 버리면 이어받기가 정작 필요한 회차에 무력해진다.
    """
    led = ledger_of(*[f"o/r{i}" for i in range(10)])
    calls = []
    carried, notes = carryover.carry_forward(
        led, [], resolve=lambda p: calls.append(p) or alive(p), day="2026-09-21", budget=3)
    assert len(calls) == 3, "상한을 안 지켰다"
    assert len(carried) == 10, "상한 밖의 줄을 버렸다"
    assert any("확인 미룸 7건" in n for n in notes), notes
