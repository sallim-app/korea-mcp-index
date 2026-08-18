#!/usr/bin/env python3
"""측정값 → README.md 생성 (2026-08-18, D-2026W34-21/22).

**사람이 순위를 손으로 쓰지 않는다.** 손으로 쓰는 순간 재현이 끊기고, 재현이 끊기면
이해충돌을 방어할 수단이 사라진다(D-2026W34-22). 여기서 나오는 표는 measured.json의
함수이며, 같은 입력이면 같은 표가 나온다.

싣는 것과 안 싣는 것:
  - 우리 제품도 순위에 넣는다. 대신 소유를 밝히고, 우리가 지는 항목을 같이 싣는다.
  - '못 잰 것'을 숨기지 않는다 — 목록 아래에 미확인 건수를 그대로 적는다.
  - 등수는 매기지 않는다. 재현 가능한 값으로 정렬만 한다(가중치를 우리가 고르면 그게 편향이다).

실행: python3 render_readme.py  →  README.md
"""
import json
from datetime import UTC, datetime

OURS = ("app.sallim/", "sallim-app/")
HDR = """# 한국 데이터 MCP — 실측 목록

한국의 데이터를 AI에게 주는 MCP 서버를 **직접 붙여서 재고** 그 값을 공개한다.

다른 목록은 "있다"를 말한다. 이 목록은 **"지금 되냐"**를 잰다.
{ts} 측정 기준, 공식 MCP 레지스트리에 원격 주소를 등록한 한국 MCP **{n_remote}건 중
{n_dead}건({pct}%)이 응답하지 않았다.** 등록은 가동의 증거가 아니다.

## 이 목록을 믿어도 되는 이유 (그리고 믿으면 안 되는 부분)

- **측정 스크립트와 원자료가 이 저장소에 있다.** `measure.py`를 돌리면 아래 표를 다시 만들 수 있다.
  우리가 1위여도 당신이 직접 재서 반박할 수 있다.
- **우리도 이 목록에 있다.** `sallim-app`이 이 목록의 운영자이며, 우리 서버 `korea-realty`가
  표에 들어 있다. 빼지 않는 대신 **밝히고**, 우리가 지는 항목(셀프호스팅 가능 여부)을 같이 싣는다.
- **측정 항목은 결과를 보기 전에 고정했다.** 사후에 우리에게 유리하게 바꾸지 않는다.
- **남는 편향**: 어떤 항목을 재기로 골랐는지 자체는 우리가 정했다. 원자료를 공개하는 것으로
  줄일 수는 있어도 없앨 수는 없다. 없는 척하지 않는다.
- **측정 지점**: 한국(Oracle Cloud) 두 지점에서 쟀다. 국외에서 재면 값이 다를 수 있고
  그건 아직 확인하지 않았다.

## 무엇을 재는가

| 항목 | 뜻 |
|---|---|
| 도구 수 | `tools/list` 응답에 실제로 들어 있는 도구 개수. 0개면 껍데기다 |
| 웜 | 연달아 부를 때의 왕복(ms). 이미 쓰고 있는 사용자의 체감 |
| 콜드 | 첫 호출(ms). 서버리스는 기동 시간이 붙는다. **처음 붙는 사용자의 체감이라 버리지 않는다** |
| 키 | 키·가입 없이 도구 목록을 볼 수 있는가 |
| 셀프호스팅 | 패키지가 배포돼 직접 띄울 수 있는가. **원격 전용인 우리 서버는 여기서 진다** |
"""


def _fmt(r: dict) -> str:
    rm = r["remote"]
    name = r["name"]
    ours = " **(이 목록 운영자)**" if name.startswith(OURS) else ""
    repo = r.get("repo_url") or ""
    label = f"[{name}]({repo})" if repo else name
    tools = rm.get("tool_count")
    warm, cold = rm.get("warm_ms"), rm.get("cold_ms")
    coldtxt = f"{cold}" if cold is not None else "—"
    if warm and cold and cold > warm * 3:
        coldtxt = f"**{cold}**"
    return (f"| {label}{ours} | {tools if tools is not None else '—'} | "
            f"{warm if warm is not None else '—'} | {coldtxt} | "
            f"{'필요' if rm.get('needs_key') else '불필요'} | "
            f"{'가능' if r.get('self_hostable') else '불가'} |")


def main() -> int:
    d = json.load(open("measured.json", encoding="utf-8"))
    items = d["items"]
    rem = [r for r in items if r.get("remote")]
    live = [r for r in rem if r["remote"].get("reachable")]
    dead = [r for r in rem if not r["remote"].get("reachable")]
    live.sort(key=lambda r: (r["remote"].get("needs_key") or False,
                             -(r["remote"].get("tool_count") or 0)))

    out = [HDR.format(ts=datetime.now(UTC).strftime("%Y-%m-%d"), n_remote=len(rem),
                      n_dead=len(dead), pct=round(100 * len(dead) / max(len(rem), 1)))]
    out.append("\n## 응답하는 서버\n")
    out.append("| 서버 | 도구 | 웜(ms) | 콜드(ms) | 키 | 셀프호스팅 |")
    out.append("|---|---|---|---|---|---|")
    out += [_fmt(r) for r in live]

    out.append("\n## 응답하지 않는 서버\n")
    out.append("공식 레지스트리에 원격 주소가 등록돼 있으나 측정 시점에 응답하지 않았다. "
               "일시적 장애일 수 있으니 **폐기 판정이 아니라 관측 기록**으로 읽어라.\n")
    out.append("| 서버 | 증상 |")
    out.append("|---|---|")
    for r in dead:
        rm = r["remote"]
        out.append(f"| {r['name']} | {rm.get('why') or ('HTTP ' + str(rm.get('http')))} |")

    unmeasured = len(items) - len(rem)
    out.append(f"\n## 못 잰 것 — {unmeasured}건\n")
    out.append(f"후보 {len(items)}건 중 **{unmeasured}건은 원격 주소도 배포 패키지도 없어 "
               "가동 여부를 재지 못했다.** 이것은 '작동하지 않는다'가 아니라 "
               "'우리가 확인하지 못했다'는 뜻이다. 저장소만 있고 레지스트리에 등록하지 않은 "
               "경우가 대부분이다 — 등록하면 다음 회차에 자동으로 잡힌다.\n")
    for b in d.get("boundaries", [])[:5]:
        out.append(f"- {b}")

    out.append("\n## 우리 목록에 넣어 달라면\n")
    out.append("공식 MCP 레지스트리에 등록하면 다음 회차 수집에 자동으로 들어온다. "
               "PR로 직접 제안해도 된다 — **우리 경쟁 서비스여도 받는다.** "
               "좋은 MCP는 남의 것이어도 알리는 것이 이 목록의 목적이다.\n")
    out.append("---\n")
    out.append(f"생성: `render_readme.py` · 측정: `measure.py` · 원자료: `measured.json` "
               f"· 마지막 측정 {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}")

    open("README.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"README.md 생성 — 응답 {len(live)} · 무응답 {len(dead)} · 미확인 {unmeasured}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
