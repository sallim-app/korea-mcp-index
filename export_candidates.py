#!/usr/bin/env python3
"""판정 원자료 내보내기 (2026-08-19).

왜 간추리나: `candidates_filtered.json`은 5~7MB다. 주간 재생성이라 그대로 실으면 이력이
매주 그만큼 불어난다. 검증에 필요한 것은 **keep·review의 판정 사유**와 **drop의 사유 분포**다.
전체가 필요하면 파이프라인을 직접 돌리면 같은 결과가 나온다 — 그것이 재현 가능성이다.

**저장소 주소 정규화**(2026-08-19): 같은 엔드포인트를 부르는 항목이 서로 다른 저장소를
가리킬 수 있다. 공식 레지스트리의 옛 버전이 **이전 전 경로**를 들고 있기 때문이다
(GitHub 이전 리디렉트가 200을 주므로 그 주소도 살아 보인다 — 200은 최신이라는 증거가 아니다).
실제로 우리 contract-compass가 개인 계정 경로로 내보내졌다. 생성 단계(README)만 고치면
원자료에는 그대로 남으므로, 여기서도 같은 규칙을 건다.
"""
import collections
import json

from observed import fix_repo_url


def best_repo(items: list) -> dict[str, str]:
    """엔드포인트별로 가장 나은 저장소 주소. 조직 경로를 우선한다."""
    pick: dict[str, str] = {}
    for i in items:
        for r in (i.get("remotes") or []):
            ep = (r.get("url") or "").split("?")[0].rstrip("/").lower()
            ru = i.get("repo_url") or ""
            if not ep or not ru:
                continue
            cur = pick.get(ep)
            if not cur or ("sallim-app/" in ru and "sallim-app/" not in cur):
                pick[ep] = ru
    return pick


def main() -> int:
    d = json.load(open("candidates_filtered.json", encoding="utf-8"))
    items = d["items"]
    pick = best_repo(items)
    rewritten = 0
    for i in items:
        for r in (i.get("remotes") or []):
            ep = (r.get("url") or "").split("?")[0].rstrip("/").lower()
            better = pick.get(ep)
            if better and better != i.get("repo_url"):
                i["repo_url"] = better
                rewritten += 1
            break
        # 옮겨간 저장소 경로를 현재 경로로 고친다(observed.MOVED_REPO). 옛 경로는 지금
        # 없는 곳을 가리키고, 우리 옛 개인 계정 경로가 공개본에 실리는 통로이기도 했다.
        moved = fix_repo_url(i.get("repo_url"))
        if moved != i.get("repo_url"):
            i["repo_url"] = moved
            rewritten += 1

    keep = [i for i in items if i["verdict"] in ("keep", "review")]
    drops = collections.Counter(i["why"][:60] for i in items if i["verdict"] == "drop")
    out = {
        "note": ("판정 원자료(간추림). keep·review는 판정 사유째로, drop은 사유별 건수만 싣는다. "
                 "전체가 필요하면 collect_candidates.py부터 직접 돌려라 — 같은 입력이면 같은 결과다."),
        "buckets": d["buckets"], "boundaries": d.get("boundaries", []),
        "drop_reasons": [{"why": w, "n": n} for w, n in drops.most_common()],
        "items": [{k: i.get(k) for k in ("name", "repo_url", "verdict", "why", "categories",
                                         "sources", "stars", "pushed", "kr_domains")} for i in keep],
    }
    json.dump(out, open("candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # **공개되는 모든 산출물에 같은 규칙을 건다.** 정규화를 세 곳(생성·내보내기·측정본)에
    # 흩어 두었더니 한 곳을 빠뜨려 measured.json으로 개인 계정 경로가 공개됐다
    # (2026-08-19). 규칙이 여러 곳에 있으면 반드시 한 곳이 뒤처진다.
    m = json.load(open("measured.json", encoding="utf-8"))

    # **엔드포인트 중복은 원자료에서 합친다.** 지금까지 render 안에서만 합쳐서 measured.json에는
    # 같은 서버가 두 줄로 남아 있었다(contract-compass·korean-law-mcp·public-data-lens 3쌍).
    # 심사 입력이 원자료에서 나오므로 여기서 안 합치면 **같은 서버를 두 번 심사한다**.
    seen: dict[str, dict] = {}
    dedup: list = []
    dropped = 0
    for i in m["items"]:
        ep = ((i.get("remote") or {}).get("url") or "").split("?")[0].rstrip("/").lower()
        if not ep:
            dedup.append(i)
            continue
        prev = seen.get(ep)
        if prev is None:
            seen[ep] = i
            dedup.append(i)
            continue
        dropped += 1
        if i.get("self_hostable") and not prev.get("self_hostable"):
            prev["self_hostable"] = True
        cand, cur = i.get("repo_url") or "", prev.get("repo_url") or ""
        if cand and (not cur or ("sallim-app/" in cand and "sallim-app/" not in cur)):
            prev["repo_url"] = cand
        prev.setdefault("also_known_as", []).append(i["name"])
    m["items"] = dedup
    mfix = 0
    for i in m["items"]:
        ep = ((i.get("remote") or {}).get("url") or "").split("?")[0].rstrip("/").lower()
        better = pick.get(ep)
        if better and better != i.get("repo_url"):
            i["repo_url"] = better
            mfix += 1
        moved = fix_repo_url(i.get("repo_url"))
        if moved != i.get("repo_url"):
            i["repo_url"] = moved
            mfix += 1
    json.dump(m, open("measured.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"candidates.json — keep+review {len(keep)}건 · drop 사유 {len(drops)}종 · 주소 교정 {rewritten}건")
    print(f"measured.json  — 주소 교정 {mfix}건 · 엔드포인트 중복 {dropped}건 합침")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
