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


def endpoint_key(rec: dict) -> str:
    """중복 판정에 쓰는 엔드포인트 키. 질의문자열·끝슬래시·대소문자를 무시한다."""
    return ((rec.get("remote") or {}).get("url") or "").split("?")[0].rstrip("/").lower()


def merge_by_endpoint(items: list) -> tuple[list, int]:
    """같은 엔드포인트를 가리키는 줄을 하나로 합친다. `(합친 목록, 이번에 옮긴 수)`.

    **합치는 것은 지우는 것이 아니다.** 합쳐진 이름은 살아남은 줄의 `also_known_as`에
    반드시 남는다 — 그 자리가 없으면 항목이 흔적 없이 사라지고, 그건 우리가 고치러 간
    결함('못 본 것을 사망으로 적음')보다 나쁘다(아예 없는 것이 된다).

    2026-09-03: 두드리개가 리다이렉트를 따라가게 되자 `contract.naru.build/mcp`(308)가
    `contract.sallim.app/mcp`로 밝혀져 우리 서버 두 줄이 여기서 합쳐졌다. 합쳐진 쪽은
    우리 것이었지만 규칙은 남의 서버에도 똑같이 걸리므로, 흔적을 남기는 것이 규칙이다.
    """
    seen: dict[str, dict] = {}
    dedup: list = []
    dropped = 0
    for i in items:
        ep = endpoint_key(i)
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
    return dedup, dropped


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
    dedup, dropped = merge_by_endpoint(m["items"])
    m["items"] = dedup
    # **기록한 건수를 센다**(2026-09-03, T-2026W35-119 후속).
    #
    # 여기서 items를 줄여 놓고 `measured`는 measure.py가 적어 둔 값 그대로 뒀다. 그래서
    # 공개 원자료가 "측정 277건"이라 말하면서 275줄만 싣고 있었다(8/31 커밋본에서 이미
    # 277 vs 275). 두 숫자가 어긋나는 것을 아무도 못 본 이유는 **아무도 그 필드를 읽지
    # 않기 때문**이다 — 소비자가 없는 값이라 조용히 틀리고, 그래도 게시는 된다.
    # 우리가 남의 목록에서 잡아내는 종류의 부정직 공시라 여기서 끊는다(기치 ②).
    #
    # 합친 것은 **지우는 것이 아니라 옮기는 것**이다. 옮긴 자리(`also_known_as`)를 세서
    # 총계로 같이 싣는다 — 델타가 아니라 상태를 공시하므로 이 스크립트를 두 번 돌려도
    # 숫자가 흔들리지 않는다(dropped 는 이번 런에서 옮긴 수라 재실행하면 0이 된다).
    m["measured"] = len(dedup)
    merged = [{"kept": i["name"], "endpoint": (i.get("remote") or {}).get("url"),
               "merged": list(i["also_known_as"])}
              for i in dedup if i.get("also_known_as")]
    m["merged_endpoints"] = merged
    n_merged = sum(len(x["merged"]) for x in merged)
    m["merge_note"] = (
        f"같은 엔드포인트를 가리키는 항목 {n_merged}건을 한 줄로 합쳤다. "
        "합친 이름은 버리지 않고 그 줄의 `also_known_as`에 남긴다 — "
        "`measured`는 합친 뒤의 줄 수이고, 후보 총수가 아니다. "
        "리다이렉트를 따라가면 서로 다르게 적혀 있던 주소가 같은 곳으로 밝혀질 수 있어 "
        "이 수는 회차마다 달라진다.")
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

    # **공개 표를 여기서 다시 편다.** axes.csv는 measured.json의 함수인데, 문서화된 실행
    # 순서가 `recompute.py` → `export_candidates.py`라 이 병합이 axes.csv 뒤에 일어난다.
    # 합칠 것이 0건인 회차에는 그 어긋남이 안 보이고(8/31이 그랬다), 1건이라도 생기면
    # 공개 원자료 두 개가 서로 다른 건수를 싣는다. **순서를 지키라고 적는 대신 순서에
    # 무관하게 만든다**(프롬프트가 아니라 도구로 고친다 — D-2026W32-19).
    import recompute
    _d, _items = recompute.rows()
    recompute.write_csv(_items)

    print(f"candidates.json — keep+review {len(keep)}건 · drop 사유 {len(drops)}종 · 주소 교정 {rewritten}건")
    print(f"measured.json  — 주소 교정 {mfix}건 · 이번 런에서 합친 중복 {dropped}건 · "
          f"합쳐진 이름 누계 {n_merged}건 · 기록한 줄 {len(dedup)}건")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
