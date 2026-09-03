#!/usr/bin/env python3
"""남이 **다른 가중치로 다시 계산**할 수 있게 하는 경로 (2026-08-21, T-2026W34-110 ③).

신뢰 규약 3조 중 셋째다(PROTOCOL.md). 원자료를 올려 두는 것만으로는 재계산이 되지 않는다 —
`measured.json`은 233건 × 중첩 딕셔너리라 사람이 열어서 다른 가중치를 매겨 볼 물건이 아니다.
그래서 두 가지를 준다.

  axes.csv     게시된 모든 축을 서버 1행 × 축 1열로 편 표. 스프레드시트에 그대로 들어간다.
  --weights    독자가 자기 가중치로 순서를 다시 매긴다. **그 결과는 우리 순위가 아니다.**

우리 순위는 지표 가중합이 아니라 실제 질문·답변의 채점이다(JUDGING.md). 지표로 줄 세우는
방식은 우리가 실측으로 폐기했다 — 도구 수는 크기지 품질이 아니었고 비율 지표는 포화했다.
그래서 `--weights`는 "우리 순위를 재현하는 도구"가 아니라 **"우리 축 선정에 동의하지 않는
독자가 자기 계산을 해 보는 도구"**다. 그 차이를 출력 머리에 매번 박는다.

  python3 recompute.py                      # axes.csv 생성
  python3 recompute.py --verify             # 게시본 숫자가 원자료에서 재현되는지 검사
  python3 recompute.py --weights tool_count=1,warm_ms=-0.01
"""
import argparse
import csv
import json
import re
import sys

OURS = ("app.sallim/", "sallim-app/")

# 게시되는 축 전부. 여기 없는 값으로 README를 쓰면 재계산이 성립하지 않으므로,
# 축을 늘릴 때는 PROTOCOL.md 개정 이력과 같이 늘린다.
COLUMNS = [
    "name", "category", "ours", "repo_url",
    "status", "reachable", "needs_key", "tool_count", "warm_ms", "cold_ms",
    "described_pct", "desc_median", "input_schema_pct", "output_schema_pct",
    "annotated_pct", "readonly_pct",
    "self_hosting", "license", "repo_public",
    "paid_disclosed", "tools_total", "tools_free", "tools_paid",
    "rank_in_category", "factual_errors",
]


def load():
    d = json.load(open("measured.json", encoding="utf-8"))
    try:
        cls = {v["name"]: v for v in json.load(open("classification.json", encoding="utf-8"))["items"].values()}
    except OSError:
        cls = {}
    rank, errs = {}, {}
    try:
        for v in json.load(open("ranking.json", encoding="utf-8"))["items"].values():
            for t in v["top"]:
                rank[t["name"]] = t["rank"]
                if t.get("사실오류") is not None:
                    errs[t["name"]] = t["사실오류"]
    except OSError:
        pass
    return d, cls, rank, errs


def rows():
    d, cls, rank, errs = load()
    out = []
    for r in d["items"]:
        rm = r.get("remote") or {}
        qy = rm.get("quality") or {}
        oss = r.get("open_source") or {}
        pd = r.get("paid_disclosure") or {}
        out.append({
            "name": r["name"],
            "category": (cls.get(r["name"]) or {}).get("category", ""),
            "ours": int(r["name"].startswith(OURS)),
            "repo_url": r.get("repo_url", ""),
            # **세 갈래 판정**(2026-09-03, T-2026W35-119). `reachable`은 두 갈래라
            # "확인 못 함"을 "응답 없음"으로 접어 넣을 수밖에 없었다 — 남의 서버를 우리
            # 클라이언트의 한계로 죽었다고 공시한 자리가 정확히 여기다. `status`가 정본이고
            # `reachable`은 남의 재계산이 깨지지 않게 남기는 파생값(= status가 live인가)이다.
            "status": rm.get("status", "") if rm else "",
            "reachable": "" if not rm else int(bool(rm.get("reachable"))),
            "needs_key": "" if not rm else int(bool(rm.get("needs_key"))),
            "tool_count": rm.get("tool_count", ""),
            "warm_ms": rm.get("warm_ms", ""),
            "cold_ms": rm.get("cold_ms", ""),
            "described_pct": qy.get("described_pct", ""),
            "desc_median": qy.get("desc_median", ""),
            "input_schema_pct": qy.get("input_schema_pct", ""),
            "output_schema_pct": qy.get("output_schema_pct", ""),
            "annotated_pct": qy.get("annotated_pct", ""),
            "readonly_pct": qy.get("readonly_pct", ""),
            "self_hosting": (r.get("self_hosting") or {}).get("state", ""),
            "license": oss.get("license") or "",
            "repo_public": "" if oss.get("public") is None else int(oss["public"]),
            "paid_disclosed": int(bool(pd.get("disclosed"))),
            "tools_total": pd.get("total", ""),
            "tools_free": pd.get("free", ""),
            "tools_paid": pd.get("paid", ""),
            "rank_in_category": rank.get(r["name"], ""),
            "factual_errors": errs.get(r["name"], ""),
        })
    # 측정 안 된 자리는 `None`이 아니라 빈 칸으로 통일한다 — CSV에서 `None` 문자열이 되고,
    # 재계산에서는 0으로 오해된다. **빈 칸은 0이 아니라 "안 쟀다"**이고 그 둘을 섞으면
    # 재계산 결과가 조용히 틀린다(실측: warm_ms가 None인 서버에서 --weights가 죽었다).
    for r in out:
        for k, v in r.items():
            if v is None:
                r[k] = ""
    out.sort(key=lambda x: x["name"])
    return d, out


HEADER = ("# 이 표는 우리 순위가 아니다. 우리 순위는 지표 가중합이 아니라 실제 질문·답변의\n"
          "# 채점이다(JUDGING.md). 지표로 줄 세우는 방식은 우리가 실측으로 폐기했다.\n"
          "# 여기 있는 것은 **재계산에 필요한 원자료를 편 것**이다.\n")


def write_csv(items) -> None:
    with open("axes.csv", "w", encoding="utf-8", newline="") as f:
        f.write(HEADER)
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(items)
    print(f"axes.csv — {len(items)}행 × {len(COLUMNS)}열")


def verify(d, items) -> int:
    """게시본 README의 머릿수가 원자료에서 그대로 나오는가.

    ③의 핵심은 "원자료를 올렸다"가 아니라 **"올린 원자료로 게시본이 재현된다"**이다.
    재현되지 않으면 독자의 재계산은 우리 것과 비교할 기준을 잃는다.
    """
    md = open("README.md", encoding="utf-8").read()
    # **게시본이 쓰는 경로 그대로 센다.** 렌더는 같은 엔드포인트를 가리키는 포크를 합친 뒤에
    # 세는데(dedupe_by_endpoint), 여기서 원본 233건을 그냥 세면 검사기가 게시본을 틀렸다고
    # 말한다 — 재현 검사가 재현 방법을 달리 쓰면 그건 검사가 아니라 잡음이다.
    import render_readme
    items_dd, _ = render_readme.dedupe_by_endpoint([dict(r) for r in d["items"]])
    rem = [r for r in items_dd if r.get("remote")]
    dead = [r for r in rem if not r["remote"].get("reachable")]
    downs = [r for r in dead if render_readme.status_of(r) == "down"]
    bad = []

    # **세 갈래 머리 문장을 검사한다**(2026-09-03, T-2026W35-119). 종전 검사는
    # "M건이 응답하지 않았다" 한 숫자만 봤고, 그 문장이 우리 두드리개의 한계를 남의
    # 사망으로 옮겨 적던 바로 그 문장이다. 재현 검사가 옛 문장을 요구하면 어휘를
    # 고치는 순간 검사가 빨개진다 — 그래서 검사도 같이 옮긴다.
    m = re.search(r"확인한 (\d+)건 중 \*\*(\d+)건이 살아있음 확인\*\*, "
                  r"(\d+)건은 \*\*확인 못 함\*\*, (\d+)건만 \*\*죽음 확인\*\*", md)
    if not m:
        bad.append("README에서 '확인한 N건 중 … 살아있음/확인 못 함/죽음 확인' 문장을 못 찾았다")
    else:
        got = tuple(int(m.group(i)) for i in (1, 2, 3, 4))
        exp = (len(rem), len(rem) - len(dead), len(dead) - len(downs), len(downs))
        if got != exp:
            bad.append(f"머리 문장 {got} ≠ 원자료 {exp}")

    for state in ("packaged", "source_only", "unknown"):
        n = sum(1 for r in d["items"] if (r.get("self_hosting") or {}).get("state") == state)
        if n == 0:
            bad.append(f"self_hosting={state} 이 0건 — 축이 안 측정됐다")

    for b in bad:
        print("✗", b, file=sys.stderr)
    if bad:
        return 1
    print(f"✓ 게시본 머릿수가 원자료에서 재현된다 (원격 {len(rem)}건 · "
          f"확인 못 함 {len(dead) - len(downs)}건 · 죽음 확인 {len(downs)}건)")
    return 0


def reweight(items, spec: str) -> None:
    ws = {}
    for part in spec.split(","):
        k, _, v = part.partition("=")
        k = k.strip()
        if k not in COLUMNS:
            print(f"모르는 축: {k}\n쓸 수 있는 축: {', '.join(COLUMNS)}", file=sys.stderr)
            raise SystemExit(2)
        ws[k] = float(v)
    # 축마다 단위가 달라 그대로 더하면 ms가 전부를 먹는다 — 축별 최대치로 나눠 0~1로 맞춘다.
    scale = {}
    for k in ws:
        vals = [abs(float(r[k])) for r in items if r[k] != "" and not isinstance(r[k], str)]
        scale[k] = max(vals) or 1.0
    scored = []
    for r in items:
        if not r["reachable"]:
            continue
        s = 0.0
        for k, w in ws.items():
            v = r[k]
            if v == "" or isinstance(v, str):
                continue
            s += w * float(v) / scale[k]
        scored.append((s, r))
    scored.sort(key=lambda x: -x[0])
    print(HEADER)
    print(f"# 독자 가중치: {spec}")
    print(f"{'점수':>8}  {'분야':<12} 서버")
    for s, r in scored[:30]:
        print(f"{s:8.3f}  {r['category'][:12]:<12} {r['name']}{'  🏠' if r['ours'] else ''}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", help="예: tool_count=1,warm_ms=-0.01")
    ap.add_argument("--verify", action="store_true", help="게시본 숫자가 원자료에서 재현되는지 검사")
    a = ap.parse_args()
    d, items = rows()
    if a.weights:
        reweight(items, a.weights)
        return 0
    if a.verify:
        return verify(d, items)
    write_csv(items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
