#!/usr/bin/env python3
"""분야별 순위 — 블라인드 심사 입력 준비와 결과 병합 (2026-08-19, D-2026W34-22 정정).

**왜 지표 정렬을 버렸나**(사장님 지적 "순위가 신뢰가 안 가는데?"):
  · 도구 수는 **크기**지 품질이 아니다. 125종(설명 76%·주석 0%)이 82종(100%·100%)을 이겼다.
  · 완비도 같은 비율 지표는 **포화**한다 — 상위 6개가 100% 동점이었고 그 최상단이 우리 서버였다.
  · 설명 길이 중앙값은 **표본 크기를 무시**한다 — 도구 3개짜리가 125개짜리를 이겼다.
지표를 더 정교하게 만드는 길은 막혀 있다(포화하거나·크기를 재거나·도메인 지식이 필요하다).
남은 정직한 길은 **판단을 하되 그 판단을 검증 가능하게 공개**하는 것이다.

**블라인드인 이유**: 심사자가 어느 것이 우리 것인지 모르면 "자기가 자기를 올렸다"는 반박이
성립하지 않는다. 이름·저장소 주소·운영자 표시를 지우고 설명과 측정값만 준다.
**완전 블라인드는 아니다** — 설명에 브랜드가 드러날 수 있다. 그 한계는 README에 공시한다.

**재현성**: 캐시 키 = sha256(분야 | 프롬프트 | 입력 전체). 입력이 안 바뀌면 재호출하지 않고,
캐시를 저장소에 커밋한다. 프롬프트 전문은 JUDGING.md에 싣는다 — 기준을 우리가 정했다는
사실 자체가 편향이고, 그것을 숨기지 않는 유일한 방법은 기준을 공개하는 것이다.

사용: judge_ranking.py prepare   심사 입력 생성(judge/in_*.txt)
      judge_ranking.py merge     judge/out_*.json → ranking.json
"""
import hashlib
import json
import pathlib
import sys

MIN_CANDIDATES = 3   # 3건이면 심사한다(사장님 2026-08-19). 3건일 때는 "고른 것"이 아니라
                     # "줄 세운 것"이므로 README가 그렇게 밝힌다 — 선택과 정렬은 다른 주장이다.
JUDGE_DIR = pathlib.Path("judge")
PROMPT = pathlib.Path("JUDGING.md")


def comparable(items: list, cls: dict) -> list:
    """심사 대상 — 응답했고, 데이터 제공형이고, **도구가 실제로 있는** 것.

    키가 있어야 도구 목록도 못 보는 서버(401/403)와 규격 이탈 서버는 지표가 전부 비어 있어
    비교가 성립하지 않는다. 버리지 않고 README의 `측정 못 함` 구역으로 보낸다.
    """
    out = []
    for i in items:
        rm = i.get("remote") or {}
        if not rm.get("reachable") or not (rm.get("tool_count") or 0):
            continue
        c = cls.get(i["name"])
        if c and c.get("is_data_provider"):
            out.append(i)
    return out


def blind(rec: dict, sid: str, desc: str) -> str:
    """심사자에게 보이는 한 줄. 이름·주소는 지운다."""
    rm = rec["remote"]
    q = rm.get("quality") or {}
    return (f"{sid}\t도구 {rm.get('tool_count')}종\t웜 {rm.get('warm_ms')}ms\t"
            f"콜드 {rm.get('cold_ms')}ms\t설명 {q.get('described_pct', '?')}%"
            f"(중앙 {q.get('desc_median', '?')}자)\t스키마 {q.get('input_schema_pct', '?')}%\t"
            f"주석 {q.get('annotated_pct', '?')}%\t{desc[:200]}")


def key_of(cat: str, lines: list) -> str:
    p = PROMPT.read_text(encoding="utf-8") if PROMPT.exists() else ""
    return hashlib.sha256(("|".join([cat, p] + lines)).encode()).hexdigest()[:16]


def load():
    m = json.load(open("measured.json", encoding="utf-8"))
    cls = {v["name"]: v for v in json.load(open("classification.json", encoding="utf-8"))["items"].values()}
    try:
        src = {i["name"]: i for i in json.load(open("candidates_filtered.json", encoding="utf-8"))["items"]}
    except OSError:
        src = {}
    return m, cls, src


def prepare() -> int:
    m, cls, src = load()
    JUDGE_DIR.mkdir(exist_ok=True)
    cache = json.load(open("ranking.json", encoding="utf-8"))["items"] if pathlib.Path("ranking.json").exists() else {}
    comp = comparable(m["items"], cls)
    bycat: dict[str, list] = {}
    for i in comp:
        bycat.setdefault(cls[i["name"]]["category"], []).append(i)

    todo = 0
    plan = {}
    for cat, group in sorted(bycat.items()):
        if len(group) < MIN_CANDIDATES:
            print(f"  {cat:<14} {len(group)}건 — 심사 안 함(후보 {MIN_CANDIDATES}건 미만)")
            continue
        group.sort(key=lambda r: r["name"])          # 입력 순서를 고정 — 재현성
        ids = {f"S{n + 1}": r["name"] for n, r in enumerate(group)}
        lines = [blind(r, sid, (src.get(r["name"]) or {}).get("description") or "")
                 for sid, r in zip(ids, group, strict=True)]
        k = key_of(cat, lines)
        plan[cat] = {"key": k, "ids": ids}
        if k in cache:
            print(f"  {cat:<14} {len(group)}건 — 캐시 적중, 재호출 없음")
            continue
        todo += 1
        # **슬러그는 분야 이름에서 나온다 — 위치가 아니라.** 위치 기반(cat1·cat2…)이었을 때
        # 분야 하나가 중간에 끼어들자 번호가 밀려, 이미 나온 다른 분야의 심사 결과를
        # 새 분야 것으로 읽을 뻔했다(2026-08-19). 순서가 바뀌어도 파일이 안 섞여야 한다.
        slug = hashlib.sha256(cat.encode()).hexdigest()[:8]
        (JUDGE_DIR / f"in_{slug}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        plan[cat]["slug"] = slug
        print(f"  {cat:<14} {len(group)}건 — judge/in_{slug}.txt")
    json.dump(plan, open(JUDGE_DIR / "plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n심사 필요 {todo}개 분야")
    return 0


def merge() -> int:
    plan = json.load(open(JUDGE_DIR / "plan.json", encoding="utf-8"))
    cache = json.load(open("ranking.json", encoding="utf-8"))["items"] if pathlib.Path("ranking.json").exists() else {}
    added = 0
    for cat, p in plan.items():
        slug = p.get("slug")
        f = JUDGE_DIR / f"out_{slug}.json" if slug else None
        if not f or not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        top = []
        for e in (d.get("top") or [])[:3]:
            name = p["ids"].get(e.get("id"))
            if not name:
                continue
            top.append({"name": name, "rank": len(top) + 1, "why": (e.get("why") or "")[:120]})
        if not top:
            print(f"  {cat}: 심사 결과를 못 읽었다 — 건너뜀")
            continue
        cache[p["key"]] = {"category": cat, "top": top, "note": (d.get("note") or "")[:160],
                           "candidates": len(p["ids"]), "by": "llm:haiku(blind)"}
        added += 1
    json.dump({"note": "분야별 블라인드 심사 결과. 키=sha256(분야|프롬프트|입력). "
                       "입력이 안 바뀌면 재호출하지 않는다. 심사 기준 전문은 JUDGING.md.",
               "model": "claude-haiku-4-5", "min_candidates": MIN_CANDIDATES, "items": cache},
              open("ranking.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ranking.json — 분야 {added}개 반영, 누적 {len(cache)}개")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    raise SystemExit(prepare() if cmd == "prepare" else merge())
