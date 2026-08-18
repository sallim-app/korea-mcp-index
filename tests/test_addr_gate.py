#!/usr/bin/env python3
"""주소 판정 그물의 회귀 고정 (2026-08-19, T-2026W34-107).

**이 목록의 유일한 상품은 판정값이다.** 판정이 틀리면 남의 제품에 사망 선고를 하거나
문서 페이지를 살아있는 서버로 싣는다 — 2026-08-19에 양쪽 다 실제로 일어났고(거짓 사망 8건·
거짓 생존 4건) 그걸 고친 것이 이 그물이다. 그래서 그 12건을 그대로 케이스로 박는다.
고치는 것만으로는 다음 회차에 다시 통과한다.

네트워크를 타지 않는다 — 순수 함수만 검사한다.
실행: python3 tests/test_addr_gate.py   (rc=0 통과)
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


measure = _load("measure")
enrich = _load("enrich")

# 2026-08-19 실측에서 실제로 잘못 판정된 주소들. 앞의 값이 "빼야 한다".
BLOCK = [
    ("https://glama.ai/mcp", "거짓 사망 2건 — 우리 contract-compass 포함"),
    ("https://lobehub.com/mcp", "거짓 사망 2건"),
    ("https://smithery.ai/servers/greennuri/mcp", "목록 페이지"),
    ("https://antigravity.google/docs/mcp", "거짓 생존 4건 — 구글 문서 페이지가 200을 준다"),
    ("https://www.home-assistant.io/integrations/mcp", "남의 문서"),
    ("https://huggingface.co/spaces/MCP", "남의 문서"),
    ("https://xxxx.ngrok.io/mcp", "README placeholder"),
]
# 반대편 — 이건 진짜 엔드포인트라 막으면 안 된다(과잉 차단 회귀 방지).
ALLOW = [
    "https://server.smithery.ai/@isnow890/data4library-mcp/mcp",   # 호스팅 실주소
    "https://korean-law-mcp.fly.dev/mcp",
    "https://service.datahub.kr/projects/public-data-lens/mcp",
    "https://mcp.koreanpulse.dev/mcp",
    "https://academyinfo-mcp-433006350023.asia-northeast3.run.app/mcp",
]


def main() -> int:
    fails = []
    for url, why in BLOCK:
        if not measure.third_party_addr(url):
            fails.append(f"measure가 통과시킴: {url} ({why})")
        if not enrich.SKIP_HOST.search(url):
            fails.append(f"enrich가 통과시킴: {url} ({why})")
    for url in ALLOW:
        if measure.third_party_addr(url):
            fails.append(f"measure가 실주소를 막음: {url}")
        if enrich.SKIP_HOST.search(url):
            fails.append(f"enrich가 실주소를 막음: {url}")

    # 프로토콜 증거 — 200뿐인 것은 확인이 아니다(문서 페이지가 정확히 그렇게 생겼다).
    if not measure.protocol_confirmed({"tool_count": 0}):
        fails.append("도구 0개도 tools/list가 읽힌 것이므로 확인이다")
    if not measure.protocol_confirmed({"tool_count": None, "needs_key": True}):
        fails.append("401/403 인증 벽은 MCP 응답의 증거다")
    if measure.protocol_confirmed({"tool_count": None, "reachable": True}):
        fails.append("200이지만 tools/list를 못 읽은 것을 확인으로 처리했다")

    for f in fails:
        print("FAIL", f)
    print(f"{'실패 ' + str(len(fails)) + '건' if fails else '통과'} — "
          f"차단 {len(BLOCK)} · 허용 {len(ALLOW)} · 증거규칙 3")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
