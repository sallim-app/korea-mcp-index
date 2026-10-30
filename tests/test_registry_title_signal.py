"""레지스트리 `title`도 판정 입력이다 — 버리던 자기신고 필드 (2026-10-31, GitHub 이슈 #2).

**계기.** `io.boim/vendors`(보임 — 소상공인 상가정보·조달 업체·입찰 공고, 무키 원격,
도구 6종 전부 한글 설명)가 등재 누락으로 신고됐다. 수집은 됐다(레지스트리 전수 스윕이라
검색어와 무관하다). 한국 신호도 잡혔다(설명의 `Korean`·한글 `보임`). 떨어진 축은
**데이터 제공형**이었다 — 설명 "Korean businesses (2.7M, all industries), public-procurement
vendors and live public bids."에는 우리 데이터형 단어가 없고, 그 신호(`Directory`)는 레지스트리
`title` "BOIM Korea Vendor Directory"에만 있었는데 수집기가 `title`을 버리고 있었다.
그래서 `review`로 떨어졌고, review는 LLM 분류가 돌아 `is_data_provider`를 붙여야만 측정
모집단에 든다 — 분류가 안 돌면 조용히 안 잰다.

이름 하나 예외가 아니라 **필드 하나를 되살린 것**이라, 반대편(한국과 무관한 서버가 title
덕에 들어오는 것)도 같이 못박는다.

실행: python3 -m pytest tests/test_registry_title_signal.py -q
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import filter_candidates as fc  # noqa: E402


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


collect = _load("collect_candidates")

# 2026-10-31 레지스트리 실응답(`search=io.boim&version=latest`) 그대로.
BOIM_SERVER = {
    "name": "io.boim/vendors",
    "description": ("BOIM(보임): Korean businesses (2.7M, all industries), "
                    "public-procurement vendors and live public bids."),
    "title": "BOIM Korea Vendor Directory",
    "repository": {"url": "https://github.com/kikiyop1101/boim-mcp", "source": "github"},
    "version": "2.0.2",
    "websiteUrl": "https://boim.io/connect/",
    "remotes": [{"type": "streamable-http", "url": "https://boim.io/api/mcp"}],
}


def _sweep(servers: list[dict]) -> dict:
    def fake_get(url, token=None, tries=3):
        return {"servers": [{"server": s} for s in servers], "metadata": {}}
    orig = collect._get
    try:
        collect._get = fake_get
        found, _ = collect.from_registry()
    finally:
        collect._get = orig
    return found


def test_수집기는_title을_버리지_않는다():
    found = _sweep([BOIM_SERVER])
    assert found["io.boim/vendors"]["title"] == "BOIM Korea Vendor Directory"


def test_boim형_레코드는_keep이다():
    """수집 → 판정을 실제 경로로 태운다. review면 LLM 분류가 안 돌 때 측정 밖이다."""
    item = _sweep([BOIM_SERVER])["io.boim/vendors"]
    c = fc.classify(item)
    assert c["verdict"] == "keep", c
    assert "directory" in c["data"], c


def test_결함_재주입__title이_없으면_review로_떨어진다():
    """이 테스트가 지키는 값이 실재함을 보인다 — title을 빼면 종전 판정으로 돌아간다."""
    item = dict(_sweep([BOIM_SERVER])["io.boim/vendors"])
    item.pop("title")
    assert fc.classify(item)["verdict"] == "review"


# 한글도 한국 단어도 없는 외국 서버 — title에 데이터형 단어가 있어도 한국 신호는 안 생긴다.
FOREIGN = [
    {"name": "io.github.acme/vendor-directory",
     "title": "Acme Vendor Directory",
     "description": "Search US federal procurement vendors and SAM.gov opportunities."},
    {"name": "com.example/weather",
     "title": "Global Weather Data",
     "description": "Forecasts and historical observations for any city."},
    {"name": "io.github.someone/tz-tools",
     "title": "Time Zone Lookup",
     "description": "Current local time in Asia/Seoul and other IANA zones."},
]


def test_한글_없는_외국_서버는_title이_있어도_후보가_아니다():
    for s in FOREIGN:
        item = _sweep([s])[s["name"]]
        c = fc.classify(item)
        assert c["verdict"] == "drop", (s["name"], c)
        assert not c["kr"], (s["name"], c)


def test_title이_설명과_같으면_신호를_부풀리지_않는다():
    """title이 이미 설명 안에 있으면 덧붙이지 않는다 — 같은 단어를 두 번 세지 않는다."""
    base = {"name": "io.example/x", "description": "Korean stock price lookup"}
    a = fc.classify(base)
    b = fc.classify({**base, "title": "Korean stock price lookup"})
    assert a == b


# ── 같은 커밋의 짝: title을 넣자 생긴 오탐 1건을 같은 자리에서 막는다 ─────────────
def test_영어_언어목록의_Korean은_한국_신호가_아니다():
    """레지스트리 전량(53,287건) 대조에서 title 개정이 만든 유일한 외국 서버 승격.
    언어 목록 자리의 `Korean` 하나로 한국 신호가 났고 title의 `Catalog`로 keep이 됐다."""
    item = _sweep([{
        "name": "com.master-setter/pokemon-tcg",
        "title": "Master Setter Pokémon TCG Catalog",
        "description": ("Pokémon TCG cards in 14 languages: 196k cards, 272k printings, "
                        "deepest Korean/Thai/Chinese.")}])["com.master-setter/pokemon-tcg"]
    c = fc.classify(item)
    assert c["verdict"] == "drop" and not c["kr"], c


def test_언어목록이_아닌_Korean은_그대로_신호다():
    for desc in ("Korean stock prices and DART filings",
                 "Korean and Japanese market data search",
                 "Korean policy & finance facts with primary-source citations"):
        assert fc.classify({"name": "io.example/k", "description": desc})["kr"], desc


def test_스윕_상한은_관측된_레지스트리보다_크다():
    """2026-10-31 레지스트리는 533페이지(53,287개)에서 커서가 소진됐다. 상한이 그보다 작으면
    이름순 뒤쪽(`kr.*` 전부)이 통째로 빠진다 — 400이 그랬다. 하한만 고정한다."""
    assert collect.MAX_PAGES * collect.PAGE > 53_287
