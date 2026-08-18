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
{ts} UTC 측정 기준, 원격 주소를 확인한 한국 MCP **{n_remote}건 중 {n_dead}건({pct}%)이
응답하지 않았다.** 등록은 가동의 증거가 아니다.

**주소의 출처를 갈라 읽어라.** 관리자가 공식 레지스트리에 **직접 등록한** 주소 {n_reg}건 중
{n_reg_dead}건이 무응답이고, 나머지 {n_rme}건은 우리가 README에서 뽑은 **추정** 주소다(무응답 {n_rme_dead}건).
추정 주소의 무응답은 "그 서버가 죽었다"보다 약한 주장이다 — 우리가 주소를 잘못 짚었을 수 있다.

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


def dedupe_by_endpoint(items: list) -> tuple[list, int]:
    """**같은 주소를 부르면 같은 서버다** — 표에 두 줄로 실으면 안 된다.

    수집 시점 중복 제거로는 못 잡는다(2026-08-19 실측): 레지스트리 항목은 처음부터 주소를
    갖지만 GitHub 항목은 **보강 단계에서야** README로 주소가 붙는다. 그래서 우리
    contract-compass가 두 줄로 실렸다 — 하나는 저장소가 `sallim-app`, 다른 하나는
    레지스트리 옛 버전이 들고 있던 **개인 계정 경로**였다. 표에 그 링크가 그대로 나갔다.

    합칠 때 저장소 주소는 **더 나은 쪽**을 고른다: 레지스트리 옛 판이 들고 있는 이전 경로보다
    실제로 살아 있는 소스 저장소가 맞다(GitHub 이전 리디렉트 때문에 옛 경로도 200을 준다 —
    200은 그 주소가 최신이라는 증거가 아니다).
    """
    by_ep: dict[str, dict] = {}
    out, merged = [], 0
    for it in items:
        ep = ((it.get("remote") or {}).get("url") or "").split("?")[0].rstrip("/").lower()
        if not ep:
            out.append(it)
            continue
        prev = by_ep.get(ep)
        if prev is None:
            by_ep[ep] = it
            out.append(it)
            continue
        merged += 1
        # 도구 수·품질은 같은 서버니 같다. 저장소 주소와 셀프호스팅 가능 여부만 나은 쪽으로.
        if it.get("self_hostable") and not prev.get("self_hostable"):
            prev["self_hostable"] = True
        cand, cur = it.get("repo_url") or "", prev.get("repo_url") or ""
        if cand and (not cur or ("sallim-app/" in cand and "sallim-app/" not in cur)):
            prev["repo_url"] = cand
        prev.setdefault("also_known_as", []).append(it["name"])
    return out, merged


def main() -> int:
    d = json.load(open("measured.json", encoding="utf-8"))
    items, merged = dedupe_by_endpoint(d["items"])
    if merged:
        print(f"  같은 주소를 부르는 항목 {merged}건을 한 줄로 합쳤다")
    rem = [r for r in items if r.get("remote")]
    live = [r for r in rem if r["remote"].get("reachable")]
    dead = [r for r in rem if not r["remote"].get("reachable")]
    live.sort(key=lambda r: (r["remote"].get("needs_key") or False,
                             -(r["remote"].get("tool_count") or 0)))

    reg = [r for r in rem if r["remote"].get("url_source") != "readme"]
    rme = [r for r in rem if r["remote"].get("url_source") == "readme"]
    out = [HDR.format(ts=datetime.now(UTC).strftime("%Y-%m-%d"), n_remote=len(rem),
                      n_dead=len(dead), pct=round(100 * len(dead) / max(len(rem), 1)),
                      n_reg=len(reg), n_reg_dead=sum(1 for r in reg if not r["remote"].get("reachable")),
                      n_rme=len(rme), n_rme_dead=sum(1 for r in rme if not r["remote"].get("reachable")))]
    out.append("\n## 응답하는 서버\n")
    out.append("| 서버 | 도구 | 웜(ms) | 콜드(ms) | 키 | 셀프호스팅 |")
    out.append("|---|---|---|---|---|---|")
    out += [_fmt(r) for r in live]

    out.append("\n## 응답하지 않는 서버\n")
    out.append("측정 시점에 그 주소가 응답하지 않았다. 일시적 장애일 수 있으니 "
               "**폐기 판정이 아니라 관측 기록**으로 읽어라.\n")
    out.append("주소 출처를 같이 싣는다. `레지스트리`는 관리자가 직접 등록한 주소라 "
               "무응답이 그 서버에 대한 관측이지만, `README 추정`은 우리가 문서에서 뽑은 "
               "주소여서 **우리가 잘못 짚었을 가능성이 남아 있다**. 둘을 같은 무게로 읽지 마라.\n")
    out.append("| 서버 | 증상 | 주소 출처 |")
    out.append("|---|---|---|")
    for r in dead:
        rm = r["remote"]
        origin = "README 추정" if rm.get("url_source") == "readme" else "레지스트리"
        out.append(f"| {r['name']} | {rm.get('why') or ('HTTP ' + str(rm.get('http')))} | {origin} |")

    # **집계와 문장이 어긋나면 그것도 거짓말이다**(codex 교차검증 2026-08-19).
    # 종전 문장은 원격 없는 건을 전부 "패키지도 없다"고 적었으나 실제로는 대부분 패키지가 있었다.
    nore = [r for r in items if not r.get("remote")]
    withpkg = [r for r in nore if r.get("package")]
    inst = [r for r in withpkg if r["package"].get("installable")]
    unmeasured = len(nore)
    out.append(f"\n## 못 잰 것 — {unmeasured}건\n")
    out.append(f"후보 {len(items)}건 중 **{unmeasured}건은 원격 주소를 확인하지 못해 "
               "'지금 되냐'를 재지 못했다.** 이것은 '작동하지 않는다'가 아니라 "
               "'우리가 확인하지 못했다'는 뜻이다.\n")
    out.append(f"그중 {len(withpkg)}건은 배포 패키지가 있어 **직접 띄울 수는 있고**"
               f"(설치 가능 {len(inst)}건), 나머지 {unmeasured - len(withpkg)}건은 원격 주소도 "
               "패키지도 없다 — 저장소만 있고 레지스트리에 등록하지 않은 경우다. "
               "등록하면 다음 회차에 자동으로 잡힌다.\n")
    out.append("여기엔 **주소 미상**도 들어 있다. README에서 뽑은 주소가 그 서버의 것이 아니라 "
               "디렉터리·문서 사이트(Glama·LobeHub 등)이거나 문서의 placeholder였던 건들이다. "
               "그런 주소로 얻은 응답은 살았다는 증거도 죽었다는 증거도 아니라서 판정에서 뺐다.\n")
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
