#!/usr/bin/env python3
"""게시 이력 이어받기 — **한 번 실은 서버는 조용히 사라지지 않는다** (2026-09-14, T-2026W38-309).

계기. 2026-09-14 회차에서 지난주 게시본에 있던 `TheNaham/koreafood-mcp` ·
`josanku/wehome-insight` · `leadbrain/korean-data-mcp`가 후보 30,508건에 없었다.
**셋 다 GitHub에 그대로 살아 있었다(HTTP 200).** 세상이 바뀐 게 아니라 **우리 그물이
이번에 그것들을 안 돌려준 것**이다 — GitHub 검색은 질의당 상위 100건(별 순)만 주므로,
별이 0~2개인 서버는 같은 질의에 새 저장소가 늘어나는 것만으로 그 100건 밖으로 밀린다.
수집기는 그 절단을 `truncated`로 정직하게 적어 두었지만, **어느 줄이 밀려났는지는 아무도
말하지 않았다.** "지금 되냐"를 파는 목록에서 줄이 흔적 없이 사라지는 것은 죽었다고 잘못
쓰는 것과 같은 계열의 거짓이다(PROTOCOL 기치 ②: 못 봄 ≠ 없음).

**규칙.** 우리가 한 번이라도 게시한 서버는 원장(`published_history.json`)에 남고, 이후
회차의 수집 원천에 안 잡히면 **후보로 이어받는다**. 이어받은 줄도 필터·측정을 똑같이
통과해야 하므로 이 규칙은 판정을 면제하지 않는다 — 면제하는 것은 **침묵**뿐이다.
빠질 때는 사유가 붙는다: 저장소가 사라졌으면 404 실측으로 원장에서 은퇴하고, 필터가
주제 밖이라 판정하면 그 사유가 공개 원자료에 이름째로 실린다.

**이어받기 전에 반드시 지금 이름을 확인한다.** GitHub은 개명된 저장소를 301로 이어 주므로
옛 이름도 살아 보인다. 확인 없이 이어받으면 같은 서버가 두 줄이 된다 — 실측 2026-09-14:
`hwain-hwang/Real-Estate-Location-Analyzer_MCP`는 원장에서 사라진 것처럼 보였지만
`hwain-ai/…`로 개명해 **이번 회차에 이미 들어와 있었다**. 개명 확인이 없으면 이 줄이
중복으로 실린다(merge_sources 주석의 `app.apick` 사고와 같은 계열).

실행:
  python3 carryover.py --bootstrap   # 게시 이력(git의 measured.json 회차들)로 원장 첫 적재
  python3 carryover.py               # 원장 요약
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

LEDGER = "published_history.json"
# 저장소 404가 **연속 몇 회차** 같아야 은퇴로 읽는가. 1이면 비공개 전환 한 번에 남의
# 서버가 우리 목록에서 영구히 지워진다(codex 교차검증 2026-09-15).
GONE_ROUNDS = 2
# 한 회차에 지금 이름을 확인할 최대 건수. 수집 원천이 통째로 실패한 회차에는 원장 전체가
# "안 잡힘"이 되는데, 요청당 20초를 직렬로 곱하면 파이프라인이 몇 시간 멈춘다(codex
# 2026-09-15). 상한을 넘은 줄은 **확인을 미루고 그대로 이어받는다** — 못 본 것을 버리는
# 쪽이 아니라 확인을 미루는 쪽으로 넘어져야 한다(기치 ②). 넘어간 건수는 공시한다.
RESOLVE_BUDGET = 80
GITHUB_REPO = "https://api.github.com/repos/"
UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; building a measured MCP index)"


def norm_repo(url: str | None) -> str:
    """저장소 주소 비교용 정규화. 끝슬래시·대소문자·질의문자열을 무시한다."""
    return (url or "").split("?")[0].rstrip("/").lower()


def is_github(name_or_url: str) -> bool:
    return "github.com/" in (name_or_url or "").lower()


def gh_path(entry: dict) -> str | None:
    """원장 항목에서 GitHub `owner/repo` 경로를 뽑는다. 없으면 None(레지스트리 전용 항목)."""
    ru = entry.get("repo_url") or ""
    if is_github(ru):
        return ru.split("github.com/", 1)[1].strip("/").removesuffix(".git")
    # 레지스트리 이름(app.sallim/…)은 GitHub 경로가 아니다 — 슬래시가 있다고 경로로 읽지 않는다.
    return None


# ── 원장 ────────────────────────────────────────────────────────────────────
def empty_ledger() -> dict:
    return {"note": ("게시 이력 원장 — 우리가 한 번이라도 게시한 서버. 이후 회차의 수집 "
                     "원천에 안 잡히면 후보로 이어받는다(carryover.py). 은퇴는 실측 근거가 "
                     "있을 때만 적는다."),
            "items": {}}


def load(path: str = LEDGER) -> dict:
    if not os.path.exists(path):
        return empty_ledger()
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    d.setdefault("items", {})
    return d


def save(ledger: dict, path: str = LEDGER) -> None:
    ledger["count"] = len(ledger["items"])
    ledger["retired_count"] = sum(1 for e in ledger["items"].values() if e.get("retired"))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")


def record(ledger: dict, measured: dict, day: str | None = None) -> int:
    """게시본(measured.json)을 원장에 적는다. 새로 적은 건수를 돌려준다.

    `also_known_as`(엔드포인트 병합으로 옮겨진 이름)도 같이 적는다 — 그 이름으로 게시된
    회차가 실재하고, 다음 회차에 그 이름으로만 잡히면 이어받기의 열쇠가 되기 때문이다.
    """
    day = day or measured.get("measured_at") or ""
    new = 0
    for i in measured.get("items", []):
        remote = (i.get("remote") or {}).get("url") or ""
        for n in [i["name"], *(i.get("also_known_as") or [])]:
            e = ledger["items"].get(n)
            if e is None:
                # `last_published`를 빈 값으로 두고 아래 갱신부가 채운다 — 여기서 미리
                # 채우면 첫 회차가 `day > last_published`에 걸려 rounds가 0으로 남는다.
                e = {"name": n, "repo_url": i.get("repo_url") or "",
                     "last_remote": remote, "first_published": day,
                     "last_published": "", "rounds": 0, "retired": None, "renamed_to": None}
                ledger["items"][n] = e
                new += 1
            # 게시된 값이 더 새롭다 — 주소는 최신 게시본을 따른다
            e["repo_url"] = i.get("repo_url") or e.get("repo_url") or ""
            e["last_remote"] = remote or e.get("last_remote") or ""
            if day:
                if not e.get("first_published") or day < e["first_published"]:
                    e["first_published"] = day
                if day > (e.get("last_published") or ""):
                    e["last_published"] = day
                    e["rounds"] = e.get("rounds", 0) + 1
            # 다시 게시됐으면 은퇴를 취소한다 — 은퇴는 상태이지 낙인이 아니다
            e["retired"] = None
            e["gone_streak"], e["gone_last_day"], e["gone_round"] = 0, "", ""
    return new


# ── 지금 이름 확인 ──────────────────────────────────────────────────────────
def resolve_github(path: str, token: str | None = None, timeout: int = 20) -> dict:
    """GitHub 저장소의 **지금** 상태. 판정은 세 가지뿐이다.

      alive   — 200. `full_name`이 개명 후 이름이다(301을 따라간 결과).
      gone    — 404/410. 저장소가 없다. **이것만이 은퇴의 근거다.**
      unknown — 그 외(403 한도·네트워크). 없다가 아니라 미확인이다(기치 ②).
    """
    req = urllib.request.Request(
        GITHUB_REPO + urllib.parse.quote(path, safe="/"),
        headers={"Accept": "application/vnd.github+json", "User-Agent": UA})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
        return {"state": "alive", "full_name": d.get("full_name") or path,
                "repo_url": d.get("html_url") or f"https://github.com/{path}",
                "description": d.get("description") or "",
                "stars": d.get("stargazers_count", 0),
                "pushed": (d.get("pushed_at") or "")[:10],
                "archived": bool(d.get("archived")),
                "why": "HTTP 200"}
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return {"state": "gone", "why": f"HTTP {e.code}"}
        return {"state": "unknown", "why": f"HTTP {e.code}"}
    except Exception as e:                                    # noqa: BLE001
        return {"state": "unknown", "why": type(e).__name__}


# ── 이어받기 ────────────────────────────────────────────────────────────────
def present_keys(items) -> tuple[set, dict, set]:
    """이번 회차가 이미 들고 있는 신원 — `(이름, 저장소→주소들, 주소들)`.

    이름만 보면 안 된다: 같은 서버가 레지스트리에서는 `app.sallim/contract-compass`,
    GitHub에서는 `sallim-app/contract-compass`로 잡히고 원장에는 두 이름이 다 남는다.
    주소로도 안 맞춰 보면 우리 서버가 매주 이어받기로 한 줄 더 실린다.

    **저장소가 같다고 같은 서버는 아니다**(merge_sources 주석의 2026-08-31 실측).
    `lead788/apick-mcp` 한 저장소가 `app.apick/{all,business,finance,…}` 9개를 내고
    주소가 전부 다르다. 저장소만 보고 '이미 있다'로 읽으면, 그중 하나가 레지스트리에서
    빠진 회차에 **형제 줄이 남아 있다는 이유로 이어받기가 조용히 안 걸린다** — 이어받기가
    막으려는 바로 그 증발이다. 그래서 저장소별로 그 줄들의 주소를 같이 들고 다닌다.
    """
    names, repo_eps, eps = set(), {}, set()
    for i in items:
        names.add(i["name"])
        for n in (i.get("also_known_as") or []):
            names.add(n)
        mine = {norm_repo(r.get("url")) for r in (i.get("remotes") or []) if r.get("url")}
        mine |= {norm_repo((i.get("remote") or {}).get("url"))} - {""}
        eps |= mine
        if i.get("repo_url"):
            repo_eps.setdefault(norm_repo(i["repo_url"]), set()).update(mine)
    return names, repo_eps, eps


def absorb(it: dict, names: set, repo_eps: dict, eps: set) -> None:
    """이어받은 줄을 **그 자리에서** 이번 회차의 신원에 더한다.

    계기(2026-09-15 codex 교차검증). 원장에는 같은 서버가 여러 이름으로 남는다 —
    엔드포인트 병합으로 옮겨진 이름(`also_known_as`)을 게시 이력으로 같이 적기 때문이다
    (`app.sallim/contract-compass` · `build.naru/contract-compass` · `sallim-app/…` 셋이
    한 주소다). 레지스트리 스윕이 한 번 실패해 셋이 동시에 안 잡히는 회차에, 순회 중
    누적을 안 하면 **셋을 다 되살려 같은 서버를 세 줄로 싣는다** — 이어받기가 고치러 간
    증발의 반대쪽 실패이고, 후보 총계까지 부풀린다.
    """
    n2, r2, e2 = present_keys([it])
    names |= n2
    eps |= e2
    for k, v in r2.items():
        repo_eps.setdefault(k, set()).update(v)


def already_here(e: dict, names: set, repo_eps: dict, eps: set) -> bool:
    """원장 항목이 이번 회차에 **이미 들어와 있는가**(present_keys 주석의 규칙)."""
    if e["name"] in names:
        return True
    le = norm_repo(e.get("last_remote"))
    if le and le in eps:
        return True
    ru = norm_repo(e.get("repo_url"))
    if ru and ru in repo_eps:
        their = repo_eps[ru]
        # 주소가 서로 어긋나지 않을 때만 같은 서버로 읽는다
        if not le or not their or le in their:
            return True
    return False


def _streak_reset(e: dict) -> None:
    """404가 **아닌 답을 실제로 받았으면** 소멸 연속 계수를 끊는다.

    답을 받은 때만이다 — 확인 예산 소진처럼 **안 물어본** 회차는 끊지 않는다
    (codex 2026-09-16). 물어보지도 않고 끊으면 지난 회차의 404 증거를 우리가 지운다.

    은퇴 공시는 **연속 회차가 같은 답일 때만**이라고 말한다. 그 말이 참이려면 404가
    아닌 답이 하나라도 끼는 순간 계수가 0으로 돌아가야 한다 — 누적이면 비연속 404
    두 번으로 살아 있는 서버가 영구 은퇴한다.
    """
    if e.get("gone_streak"):
        e["gone_streak"], e["gone_last_day"], e["gone_round"] = 0, "", ""


def carry_forward(ledger: dict, collected, resolve=None, day: str = "",
                  token: str | None = None, budget: int = RESOLVE_BUDGET) -> tuple[list, list]:
    """수집 결과에 **게시 이력만 있고 이번엔 안 잡힌** 서버를 되살린다.

    `(이어받은 항목들, 경계 공시 줄들)`. `ledger`는 제자리에서 갱신된다(은퇴·개명 기록).

    **저장소는 거처이고 주소가 신원이다.** 그래서 GitHub 404는 원장 이름이 그 저장소
    경로일 때만 은퇴 근거가 된다 — 레지스트리 이름(`app.apick/all`)으로 게시된 줄은
    소스 저장소가 사라져도 서버가 죽은 것이 아니므로, 마지막 주소째로 이어받아
    측정이 답하게 한다(collect_candidates.merge_sources의 같은 규칙).
    """
    resolve = resolve or (lambda p: resolve_github(p, token))
    names, repo_eps, eps = present_keys(collected)
    # **회차의 신원 = 마지막으로 게시가 성사된 날.** 원장은 게시 전에 저장되므로 실행
    # 날짜로는 회차를 셀 수 없다(아래 404 분기 주석). 게시가 한 번도 없으면 실행 날짜뿐이다.
    round_key = max((x.get("last_published") or "") for x in ledger["items"].values()) if ledger["items"] else ""
    round_key = round_key or day
    carried, notes = [], []
    retired, renamed, unresolved, pending, deferred = [], [], [], [], []
    budget_left = budget

    for name, e in sorted(ledger["items"].items()):
        if e.get("retired"):
            continue
        if already_here(e, names, repo_eps, eps):
            # 이번 회차에 다시 잡혔다 = 404가 아닌 답이다. **연속 계수를 끊는다**
            # (codex 교차검증 2026-09-16). 안 끊으면 지난 회차의 404 하나가 원장에
            # 남아, 몇 회차 뒤의 404 하나와 붙어 **연속 2회차로 읽히고** 살아 있는
            # 남의 서버가 은퇴한다 — 아래 404 분기가 공시하는 '연속'이 거짓이 된다.
            _streak_reset(e)
            continue

        path = gh_path(e)
        # 원장 이름이 그 GitHub 경로 자신인가 — 아니면 레지스트리 이름으로 게시된 줄이다.
        name_is_repo = path is not None and name.lower() == path.lower()

        if path is None:
            # GitHub 저장소가 없는 등록(레지스트리 전용). 소멸을 확인할 통로가 없으므로
            # **확인 못 함을 사망으로 읽지 않는다** — 마지막 게시 기록대로 이어받고 공시한다.
            # 예산 소진과 같은 이유로 계수를 건드리지 않는다 — 두드릴 곳이 없어 못 물어본
            # 것이지, 404가 아닌 답을 받은 것이 아니다.
            unresolved.append(name)
            carried.append(_item(name, e, {"state": "unknown", "why": "GitHub 저장소 없음"},
                                 day, with_remote=True))
            absorb(carried[-1], names, repo_eps, eps)
            continue

        if budget_left <= 0:
            # 확인 예산 소진. **버리지 않고 미룬다** — 마지막 기록대로 이어받고 공시한다.
            # **여기서는 연속 계수를 건드리지 않는다**(codex 2026-09-16). 예산 소진은
            # 답이 아니라 **안 물어본 것**이다 — 끊는 것도 관측이라, 물어보지도 않고
            # 끊으면 지난 회차의 404 증거를 우리가 지우는 셈이 된다. 늘리지도 줄이지도
            # 않고 그대로 두는 것이 '못 봄 ≠ 없음'의 양쪽 방향이다.
            deferred.append(name)
            carried.append(_item(name, e, {"state": "unknown", "why": "확인 예산 소진"},
                                 day, with_remote=True))
            absorb(carried[-1], names, repo_eps, eps)
            continue
        budget_left -= 1
        r = resolve(path)
        if r["state"] == "gone":
            # **404는 소멸의 증거가 아니라 소멸의 *징후*다**(codex 교차검증 2026-09-15).
            # 공개 전용 자격에는 **비공개로 돌린 저장소도 404로 보인다** — 그것을 소멸로
            # 읽으면 살아서 돌아가는 남의 서버를 우리가 영구히 지우게 된다. 우리가 고치러
            # 온 결함(살아 있는 것을 조용히 없앰)을 은퇴 규칙이 다시 저지르는 자리다.
            if e.get("last_remote"):
                # 잴 주소가 있다. 저장소가 무엇이든 **서버는 두드려 보면 답한다** —
                # 저장소는 거처이고 주소가 신원이다. 은퇴시키지 않는다.
                unresolved.append(f"{name}(소스 저장소 {r['why']}·비공개 전환 가능, "
                                  "주소로 계속 잰다)")
                carried.append(_item(name, e, {"state": "unknown",
                                               "why": f"소스 저장소 {r['why']}"}, day,
                                     with_remote=True))
                absorb(carried[-1], names, repo_eps, eps)
                continue
            if not name_is_repo:
                unresolved.append(f"{name}(소스 저장소 {r['why']}, 서버는 미확인)")
                carried.append(_item(name, e, {"state": "unknown",
                                               "why": f"소스 저장소 {r['why']}"}, day))
                absorb(carried[-1], names, repo_eps, eps)
                continue
            # 잴 주소도 없고 저장소도 404다. 그래도 **한 번 보고 끊지 않는다** — 연속
            # 두 회차에서 같은 답이 나와야 은퇴다(일시적 비공개·이전 중일 수 있다).
            # **회차를 세는 것이지 실행을 세는 것이 아니다**(codex 2026-09-15). 같은 날
            # 수집기를 두 번 돌리면 연속 2회차로 읽혀 살아 있을지 모르는 서버가 은퇴한다.
            #
            # 날짜만으로는 절반만 막힌다(codex 2026-09-16). 원장은 **수집 직후·게시 전에**
            # 저장되므로, 뒤 단계(필터·측정·내보내기)가 깨져 그 회차가 게시되지 않은 채
            # 다음 날 다시 돌리면 날짜가 달라 새 회차로 세어진다 — 실행 두 번이 회차
            # 두 번으로 둔갑한다. 그래서 회차의 신원을 **마지막으로 게시된 날**로 잡는다:
            # 게시가 성사되기 전의 재시도는 전부 같은 회차다.
            if day and (e.get("gone_last_day") == day or e.get("gone_round") == round_key):
                pending.append(f"{name}({r['why']} {e.get('gone_streak', 0)}/{GONE_ROUNDS}회차, "
                               "게시 전 재실행이라 세지 않음)")
                continue
            e["gone_streak"] = e.get("gone_streak", 0) + 1
            e["gone_last_day"], e["gone_round"] = day, round_key
            if e["gone_streak"] >= GONE_ROUNDS:
                e["retired"] = {"day": day,
                                "why": f"저장소 소멸 실측({r['why']} × {e['gone_streak']}회차)"}
                retired.append(f"{name}({r['why']}×{e['gone_streak']})")
            else:
                pending.append(f"{name}({r['why']} {e['gone_streak']}/{GONE_ROUNDS}회차)")
            continue

        if r["state"] == "alive":
            e["gone_streak"], e["gone_last_day"] = 0, ""
            if not name_is_repo:
                # 저장소는 살아 있다. 이름은 원장 것(= 게시된 신원)을 그대로 쓴다.
                carried.append(_item(name, e, {**r, "full_name": name,
                                               "repo_url": e["repo_url"]},
                                     day, with_remote=True))
                absorb(carried[-1], names, repo_eps, eps)
                continue
            full = r["full_name"]
            if full != name:
                e["renamed_to"] = full
            # **개명 후 이름으로 이미 들어와 있으면 이어받지 않는다** — 중복이 된다.
            if already_here({**e, "name": full, "repo_url": r["repo_url"]},
                            names, repo_eps, eps):
                if full != name:
                    renamed.append(f"{name} → {full}")
                continue
            carried.append(_item(full, e, r, day))
            absorb(carried[-1], names, repo_eps, eps)
            continue

        # 404도 alive도 아닌 답(403 한도·네트워크 실패 등). **이것도 404가 아니므로
        # 연속을 끊는다**(codex 교차검증 2026-09-16) — 안 끊으면 404·unknown·404가
        # '연속 2회차 같은 답'으로 계산돼 공시와 어긋난 은퇴가 난다.
        unresolved.append(f"{name}({r['why']})")
        _streak_reset(e)
        carried.append(_item(name, e, r, day, with_remote=True))
        absorb(carried[-1], names, repo_eps, eps)

    if carried:
        notes.append(
            "게시 이력 이어받기 " + str(len(carried)) + "건 — 지난 게시본에 있었으나 이번 "
            "수집 원천이 안 돌려준 서버다(GitHub 검색은 질의당 상위 100건만 준다). "
            "판정·측정은 면제되지 않는다: " + ", ".join(i["name"] for i in carried))
    if retired:
        notes.append("게시 이력 은퇴 " + str(len(retired)) + "건 — 저장소 소멸을 실측으로 "
                     "확인해 이어받기를 끝냈다: " + ", ".join(retired))
    if renamed:
        notes.append("게시 이력 개명 " + str(len(renamed)) + "건 — 옛 이름이 사라진 것처럼 "
                     "보였으나 개명이고 새 이름으로 이미 수집됐다(중복 방지): "
                     + ", ".join(renamed))
    if pending:
        notes.append("게시 이력 소멸 확인 중 " + str(len(pending)) + "건 — 저장소가 404이고 "
                     "잴 주소도 없다. 공개 자격에는 비공개 전환도 404로 보이므로 "
                     f"연속 {GONE_ROUNDS}회차가 같은 답일 때만 은퇴시킨다: " + ", ".join(pending))
    if deferred:
        notes.append("게시 이력 확인 미룸 " + str(len(deferred)) + f"건 — 한 회차 확인 상한"
                     f"({budget}건)을 넘어 지금 이름을 확인하지 못했다. 버리지 않고 마지막 "
                     "기록대로 이어받았다(수집 원천이 크게 실패한 회차의 신호다)")
    if unresolved:
        notes.append("게시 이력 미확인 " + str(len(unresolved)) + "건 — 생사를 확인하지 "
                     "못해 마지막 기록대로 이어받았다(없다가 아니다): " + ", ".join(unresolved))
    return carried, notes


def _item(name: str, e: dict, r: dict, day: str, with_remote: bool = False) -> dict:
    """이어받은 후보 1건. 수집기 산출물과 **같은 모양**이어야 필터가 그대로 판정한다."""
    it = {"name": name,
          "description": r.get("description") or "",
          "repo_url": r.get("repo_url") or e.get("repo_url") or "",
          "sources": ["carryover"], "terms": ["게시이력"], "categories": [],
          "carryover": {"last_published": e.get("last_published"),
                        "rounds": e.get("rounds"), "state": r["state"], "why": r["why"],
                        "carried_at": day}}
    for k in ("stars", "pushed", "archived"):
        if k in r:
            it[k] = r[k]
    # 마지막으로 게시된 주소가 유일한 측정 입력인 줄(레지스트리 등록·생사 미확인)에만 붙인다.
    # GitHub으로 신원이 확인된 줄에는 안 붙인다 — 보강 단계가 README에서 지금 주소를 찾는다.
    if with_remote and e.get("last_remote"):
        it["remotes"] = [{"type": "streamable-http", "url": e["last_remote"], "needs_auth": False}]
    return it


# ── 첫 적재 ─────────────────────────────────────────────────────────────────
def bootstrap(path: str = LEDGER) -> dict:
    """git에 남은 게시본(measured.json) 회차들로 원장을 처음 채운다.

    이력을 손으로 적지 않는 이유: 원장이 "우리가 실제로 게시한 것"을 뜻해야 하는데,
    손으로 적으면 그건 우리가 기억하는 것이 된다. 게시본은 커밋에 있다.
    """
    import subprocess
    ledger = load(path)
    shas = subprocess.run(["git", "log", "--format=%H", "--", "measured.json"],
                          capture_output=True, text=True, check=True).stdout.split()
    for sha in reversed(shas):                       # 오래된 회차부터
        blob = subprocess.run(["git", "show", f"{sha}:measured.json"],
                              capture_output=True, text=True)
        if blob.returncode != 0:
            continue
        try:
            m = json.loads(blob.stdout)
        except json.JSONDecodeError:
            continue
        if not m.get("measured_at"):
            continue                                  # 회차 날짜가 없는 초기 커밋은 건너뛴다
        record(ledger, m)
    return ledger


def main() -> int:
    import sys
    if "--bootstrap" in sys.argv:
        led = bootstrap()
        save(led)
        print(f"published_history.json — 게시 이력 {len(led['items'])}건 적재")
    else:
        led = load()
        alive = [e for e in led["items"].values() if not e.get("retired")]
        print(f"게시 이력 {len(led['items'])}건 · 이어받기 대상 {len(alive)}건 · "
              f"은퇴 {len(led['items']) - len(alive)}건")
        for e in sorted(led["items"].values(), key=lambda x: x["name"]):
            if e.get("retired"):
                print(f"  은퇴 {e['name']:<48} {e['retired']['why']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
