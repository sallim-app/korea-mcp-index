#!/usr/bin/env python3
"""README 추정 주소 추출 그물의 경계 회귀 (2026-10-11, 야간 품질 함대 codex 지적 F1).

두 주소가 README 추정 엔드포인트로 잡혀 `unverified`(확인 못 함)로 /down·홈 집계에 실렸다:
  - `https://pypi.org/project/mcp-korea-tourism-api/` → `\\b`가 `-` 앞에서 끝나
    `https://pypi.org/project/mcp`로 잘렸다. 실제로는 PyPI 패키지 페이지다(설치형 서버).
  - `https://.../mcp` → 호스트 문자군이 `.`만으로 된 이름을 허용했다. README의 생략 표기다.
측정 쪽(third_party_addr)도 둘 다 통과시켰다 — 두 그물을 같은 주소로 함께 두드린다.
네트워크를 타지 않는다.
"""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


measure = _load("measure")
enrich = _load("enrich")

README = """
설치: pip install mcp-korea-tourism-api
패키지 페이지 https://pypi.org/project/mcp-korea-tourism-api/ 참고.
npm: https://www.npmjs.com/package/sse-kr-server
배포 후 주소는 https://.../mcp 형태가 됩니다.
원격 서버: https://korean-law-mcp.fly.dev/mcp
레거시: https://mcp.example-kr.dev/api/sse.
"""
BAD = ["https://pypi.org/project/mcp", "https://.../mcp"]
# 추출기가 지금 잡는 정상 주소. (`@`가 든 smithery 호스팅 경로는 추출 문자군 밖이라 종전에도
# 안 잡혔다 — 이 회귀의 범위가 아니어서 측정 쪽 허용 검사에만 둔다.)
GOOD = ["https://korean-law-mcp.fly.dev/mcp", "https://mcp.example-kr.dev/api/sse"]
GOOD_MEASURE = GOOD + ["https://server.smithery.ai/@isnow890/data4library-mcp/mcp"]


def _extracted(text: str) -> list:
    return [u for u in dict.fromkeys(enrich.RE_ENDPOINT.findall(text))
            if not enrich.SKIP_HOST.search(u)]


def test_enrich_does_not_extract_bad_addresses():
    got = _extracted(README)
    for u in BAD:
        assert u not in got, f"enrich가 {u}를 엔드포인트로 뽑았다: {got}"
    assert not any("pypi.org" in u or "npmjs.com" in u or "//." in u for u in got), got


def test_enrich_still_extracts_real_addresses():
    got = _extracted(README)
    for u in GOOD:
        assert u in got, f"정상 주소 {u}를 놓쳤다(과잉 차단): {got}"


def test_measure_rejects_bad_addresses():
    for u in BAD + ["https://www.npmjs.com/package/x/mcp", "https://registry.npmjs.org/x/mcp"]:
        assert measure.third_party_addr(u), f"measure가 {u}를 통과시켰다"
        pick, why = measure.pick_endpoint([{"url": u, "confidence": "readme"}], {})
        assert pick is None and why, (u, pick, why)


def test_measure_allows_real_addresses():
    for u in GOOD_MEASURE:
        assert not measure.third_party_addr(u), f"정상 주소 {u}를 막았다"


def test_measured_json_has_no_bad_readme_addresses():
    d = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    bad = [(i["name"], i["remote"]["url"]) for i in d["items"]
           if i.get("remote") and i["remote"].get("url_source") == "readme"
           and measure.third_party_addr(i["remote"]["url"])]
    assert not bad, f"게시 원자료에 남의·가짜 주소로 잰 줄이 있다: {bad}"
