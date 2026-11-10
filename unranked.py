#!/usr/bin/env python3
"""순위 밖 사유 — **순위에 없는 모든 서버에 왜 없는지를 붙인다** (2026-11-10, T-2026W46-14).

계기(사장님 지적 2026-11-10): "순위 밖인 것도 왜 순위 밖인지 있어야 될 것 같다." 실측으로
부동산 13곳 중 순위 없는 7곳 가운데 4곳은 사유 칸(rank_note·status_note)이 **전부 비어**
있었다 — 결제 요구로 측정 불가 처리된 서버, 채점 회차 뒤에 새로 응답한 서버, 키를 요구하는
서버가 순위표에서 말없이 빠져 있었다. 독자는 "나빠서 빠졌다"와 "못 재서 빠졌다"를 가를
수 없다(기치 ②: 못 봄 ≠ 없음).

**사유는 지어내지 않고 파생한다.** 서버 이름을 적은 예외표는 없다. 근거는 이미 있는 판정
기록뿐이다:
  ① 가동 측정의 갈래 — `bucket`(comparable·unmeasurable·off_topic·unverified·down)과
     HTTP 상태코드·`measure.TRANSPORT_MISMATCH`
  ② 채점 회차의 기록 — `ranking.json`(분야·분야교정·총평), `grades/`(서버별 채점과
     `이번회차` 표지), `rounds/<날짜>/targets.tsv`(그 회차에 물어본 명단),
     `answers/<slug>.md`(측정하지 못한 서버의 머리말)
  ③ 회차 당시의 측정본 — 채점 회차 날짜 이전 마지막 `measured.json`·`classification.json`
     (git 이력). 명단에 없던 서버가 **그때 없었는지** 아니면 **있었는데 빠졌는지**를 가른다.

채점 기록 문장에서 결제(402·x402)·인증(401·403·키·토큰)·우리 호출기 한계를 정규식으로
고르는 자리가 있다. 이것은 남의 서버를 판정하는 것이 아니라 **우리 채점자가 이미 적은 근거를
갈래로 옮기는 것**이고, 그 문장의 출처 파일을 `basis`로 같이 낸다.

우리 서버도 같은 규칙이다 — 이름으로 갈리는 분기가 이 파일에 없다.
"""
from __future__ import annotations

import glob
import json
import pathlib
import re
import subprocess

from measure import TRANSPORT_MISMATCH
from observed import MISFILED, RENAMED, classification_with_renames

# ── 어휘 ─────────────────────────────────────────────────────────────────────
# 코드 → 짧은 이름. index.json `unranked_vocabulary`·사이트 「순위 밖」 절·README가 같은
# 표를 쓴다. 배열 밖(가동을 못 잰) 갈래 셋도 여기 있다 — 분야별 건수로만 공시한다.
VOCAB: dict[str, str] = {
    "payment_required": "결제 요구(HTTP 402·x402) — 결제 없이 데이터가 오지 않아 측정 불가",
    "credential_required": "키·인증 요구 — 키 없이 부르면 데이터가 오지 않아 측정 불가",
    "client_unsupported": "우리 호출기 한계 — 응답을 우리 쪽이 읽지 못했다(서버 결함 판정 아님)",
    "no_tools": "도구 목록 없음 — 응답은 했지만 비교할 값을 얻지 못했다",
    "category_corrected": "분야 교정 — 다른 분야 질문으로 매긴 점수는 쓰지 않는다",
    "category_not_graded": "채점하지 않는 분야 — 이 분야는 아직 순위를 매기지 않는다",
    "awaiting_round": "다음 채점 회차 대기 — 마지막 채점 회차 뒤에 새로 응답·편입됐다",
    "round_skipped": "채점 회차에서 제외 — 그 회차 당시 응답했지만 채점 명단에 들지 않았다",
    "round_unmeasured": "채점 회차에서 측정 못 함 — 채점 기록에 사유가 있다",
    "off_topic": "주제 밖 — 데이터를 주는 서버가 아니라고 분류됐다",
    "transport_mismatch": "전송 방식 불일치 가능 — 우리 호출에 4xx(규격 서버도 주는 코드)가 왔다",
    "unverified": "응답 확인 못 함 — 우리 호출로 확인이 안 됐다(사망 아님)",
    "down": "죽음 확인 — DNS 미해결·연결 거부처럼 호스트가 없다는 직접 증거가 있다",
    # 아래 셋은 servers 배열 밖이다(가동을 재지 못해 상세 줄이 없다) — 건수만 낸다.
    "install_only": "설치형 — 원격 주소가 없어 우리가 부를 수 없다(배포 패키지는 있다)",
    "no_address_no_package": "주소·패키지 없음 — 원격 주소도 배포 패키지도 찾지 못했다",
    "not_measured": "미측정 후보 — 수집은 했지만 아직 한 번도 두드리지 않았다",
}
OUTSIDE = ("install_only", "no_address_no_package", "not_measured")

_PAY = re.compile(r"x402|\b402\b")
_KEY = re.compile(r"\b40[13]\b|UNAUTHORIZED|auth_required|BYOK|인증|토큰|키(?!워드)")
_CLIENT = re.compile(r"호출기")


def _classify(text: str, default: str) -> str:
    """채점자가 적은 근거 문장 → 갈래. 결제 > 인증 > 우리 호출기 순(겹치면 앞이 이긴다)."""
    if _PAY.search(text):
        return "payment_required"
    if _KEY.search(text):
        return "credential_required"
    if _CLIENT.search(text):
        return "client_unsupported"
    return default


def _pay_evidence(rm: dict) -> bool:
    """HTTP 402 **상태코드만으로는** 결제 요구라 적지 않는다 — 서버가 다른 뜻으로 402를 쓰기도
    한다(codex 교차검증 2026-11-10: 본문이 'Unavailable Shop'인 402). 응답 본문에 결제 신호
    (x402·payment·결제)가 있을 때만 결제 요구로 옮긴다. 없으면 '확인 못 함'에 남는다."""
    body = " ".join(str(rm.get(k) or "") for k in ("error_body", "why", "sse_why"))
    return bool(re.search(r"x402|payment|결제", body, re.I))


def _git_json(root: pathlib.Path, rev: str, path: str):
    try:
        r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=root, capture_output=True,
                           text=True, timeout=30, check=False)
        return json.loads(r.stdout) if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


class Judging:
    """채점 회차 기록을 한 번 읽어 둔다. 파일이 없으면 그 근거만 빠진다(지어내지 않는다)."""

    def __init__(self, root: pathlib.Path | None = None):
        # 렌더러들처럼 **작업 디렉토리**의 원자료를 읽는다(render_site는 cwd 상대경로로 읽는다)
        root = pathlib.Path(root) if root else pathlib.Path.cwd()
        self.root = root
        try:
            rk = json.loads((root / "ranking.json").read_text(encoding="utf-8"))["items"]
        except (OSError, ValueError, KeyError):
            rk = {}
        self.graded_cats = sorted({v["category"] for v in rk.values()})
        self.corrected: dict[str, tuple[str, str, str]] = {}
        self.notes: dict[str, str] = {}
        for v in rk.values():
            self.notes[v["category"]] = v.get("note", "") or ""
            for m in v.get("분야교정") or []:
                self.corrected[m["name"]] = (v["category"], m.get("실제분야") or "",
                                             m.get("근거") or "")
        for n, (was, now, why) in MISFILED.items():
            self.corrected.setdefault(n, (was, now, why))
        self.grades: dict[str, tuple[dict, str]] = {}
        for f in sorted(glob.glob(str(root / "grades" / "*.json"))):
            try:
                g = json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            self.notes[g.get("category", "")] = (self.notes.get(g.get("category", ""), "")
                                                 + " " + (g.get("분야_총평") or ""))
            for s in g.get("servers") or []:
                self.grades[s["server"]] = (s, "grades/" + pathlib.Path(f).name)
        # 가장 최근 채점 회차 = targets.tsv가 있는 rounds/<YYYY-MM-DD>
        rounds = sorted(p for p in (root / "rounds").glob("*/targets.tsv")
                        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.parent.name))
        self.round = rounds[-1].parent.name if rounds else None
        self.targets: set[str] = set()
        self.slug: dict[str, str] = {}
        if rounds:
            for line in rounds[-1].read_text(encoding="utf-8").splitlines():
                p = line.split("\t")
                if len(p) < 3:
                    continue
                for n in (p[1], p[5] if len(p) > 5 else ""):
                    if n:
                        self.targets.add(n)
                        self.slug[n] = p[2]
        self.at_round = self._snapshot()

    def _snapshot(self) -> dict[str, str] | None:
        """채점 회차 당시 「비교 가능」이던 서버 → 분야. git 이력을 못 읽으면 None."""
        if not self.round:
            return None
        try:
            r = subprocess.run(["git", "log", "-1", f"--until={self.round} 23:59:59",
                                "--format=%H", "--", "measured.json"], cwd=self.root,
                               capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.SubprocessError):
            return None
        rev = r.stdout.strip()
        m = _git_json(self.root, rev, "measured.json") if rev else None
        c = _git_json(self.root, rev, "classification.json") if rev else None
        if not m or not c:
            return None
        cls = classification_with_renames({v["name"]: v for v in c["items"].values()})
        out = {}
        for it in m.get("items") or []:
            rm = it.get("remote") or {}
            k = cls.get(it["name"]) or {}
            if rm.get("reachable") and rm.get("tool_count") and k.get("is_data_provider", True):
                out[it["name"]] = k.get("category")
        return out

    def _grade(self, name: str):
        return self.grades.get(name) or self.grades.get(RENAMED.get(name, "")) or (None, None)

    def _in_targets(self, name: str) -> bool:
        return name in self.targets or RENAMED.get(name) in self.targets

    def _answers_head(self, name: str) -> str | None:
        slug = self.slug.get(name) or self.slug.get(RENAMED.get(name, ""))
        if not slug:
            return None
        p = self.root / "answers" / f"{slug}.md"
        try:
            head = p.read_text(encoding="utf-8")[:1200]
        except OSError:
            return None
        m = re.search(r"측정하지 못했다\*\*\s*—\s*([^\n]+?)\.?\s*채점·순위에 넣지 않았다", head)
        return m.group(1).strip().rstrip(".") if m else None

    def _note_mention(self, name: str, cat: str | None) -> str | None:
        for n in (name, RENAMED.get(name)):
            if not n:
                continue
            for txt in ([self.notes.get(cat or "", "")] + list(self.notes.values())):
                m = re.search(re.escape(n) + r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)", txt)
                if m:
                    return m.group(1).strip()
        return None

    # ── 본체 ──────────────────────────────────────────────────────────────────
    def reason(self, name: str, bucket: str, remote: dict | None,
               category: str | None) -> tuple[str, str, str]:
        """(코드, 한 문장, 근거 위치). **순위표에 서 있지 않은 줄에만** 부른다."""
        rm = remote or {}
        http = rm.get("http")
        sym = (rm.get("why") or (f"HTTP {http}" if http else "") or "").strip()
        rnd = self.round or "최근"
        if bucket == "down":
            return ("down", f"가동 측정에서 {VOCAB['down'].split(' — ')[0]}이다"
                    + (f"({sym})" if sym else "") + " — 응답을 받을 수 없어 채점하지 않는다.",
                    "measured.json")
        if bucket == "unverified":
            if http == 402 and _pay_evidence(rm):
                return ("payment_required",
                        "가동 측정에서 우리 호출에 HTTP 402와 결제 요구 본문이 와 MCP 응답을 "
                        "확인하지 못했다 — 사망 판정이 아니고, 결제 없이 부르는 우리 방식으로는 "
                        "잴 수 없다.", "measured.json")
            if http in TRANSPORT_MISMATCH:
                return ("transport_mismatch",
                        f"가동 측정에서 우리 호출에 HTTP {http}가 왔다 — 전송 방식이 안 맞았을 수 "
                        "있고 규격을 지키는 서버도 이 코드를 준다. 응답을 확인해야 채점하므로 "
                        "순위에 넣지 않았다(사망 판정 아님).", "measured.json")
            return ("unverified",
                    "가동 측정에서 우리 호출로 MCP 응답을 확인하지 못했다"
                    + (f"({sym})" if sym else "") + " — 사망 판정이 아니다. 응답을 확인해야 "
                    "채점하므로 순위에 넣지 않았다.", "measured.json")
        if bucket == "off_topic":
            return ("off_topic", "데이터를 주는 서버가 아니라고 분류돼(이 목록의 주제 밖) 순위 "
                    "대상이 아니다 — 서버 품질 판정이 아니다.", "classification.json")
        if bucket == "unmeasurable":
            if http == 402 and _pay_evidence(rm):
                return ("payment_required", "키 없이 부르자 HTTP 402와 결제 요구 본문으로 도구 목록을 "
                        "받지 못했다 — 우리는 결제·키 없이 재므로 비교할 값이 없다(서버 결함 판정 "
                        "아님).", "measured.json")
            if http in (401, 403) or rm.get("needs_key"):
                return ("credential_required",
                        f"키 없이 부르자 {('HTTP ' + str(http)) if http else '인증 요구'}로 도구 "
                        "목록을 보지 못했다 — 우리는 키 없이 재므로 비교할 값이 없다(서버 결함 "
                        "판정 아님).", "measured.json")
            return ("no_tools", "응답은 했지만 도구 목록을 얻지 못해"
                    + (f"({sym})" if sym else "") + " 비교할 값이 없다.", "measured.json")

        # ── comparable(가동·도구 확인) 인데 순위표에 없다 ──
        if name in self.corrected or RENAMED.get(name) in self.corrected:
            was, now, _why = self.corrected.get(name) or self.corrected[RENAMED[name]]
            tail = ("" if now in self.graded_cats else
                    f" '{now}' 분야는 아직 순위를 매기지 않는 분야다.")
            return ("category_corrected",
                    f"채점 회차에서 '{was}' 분야 질문으로 불렀는데 채점자가 실제 분야를 '{now}'(으)로 "
                    f"교정했다 — 다른 분야 질문으로 매긴 점수는 이 서버를 잰 값이 아니라 순위에 "
                    f"넣지 않는다.{tail}", "ranking.json")
        if category not in self.graded_cats:
            return ("category_not_graded",
                    f"'{category or '분야 미분류'}' 분야는 아직 순위를 매기지 않는다 — 지금 채점하는 "
                    f"분야는 {len(self.graded_cats)}개({'·'.join(self.graded_cats)})다. 가동 "
                    "측정값은 그대로 싣는다.", "ranking.json")
        g, gfile = self._grade(name)
        if g is not None and g.get("이번회차"):
            text = " ".join([g.get("이번회차") or ""] + [
                str(q.get(k) or "") for q in g.get("questions") or []
                for k in ("정확성_why", "근거성_why", "완결성_why")])
            code = _classify(text, "round_unmeasured")
            what = {"payment_required": "데이터 도구가 결제(HTTP 402·x402)를 요구해 값을 받지 못했다",
                    "credential_required": "키 없이 부르자 도구가 인증(키)을 요구해 답을 받지 못했다",
                    "client_unsupported": "우리 호출기가 응답을 읽지 못했다",
                    }.get(code, "측정하지 못했다")
            return (code, f"채점 회차에서 {what} — 자격(키·결제) 없이 데이터가 나오지 않거나 우리가 "
                    "읽지 못한 서버는 점수를 매기지 않고 순위에서 뺀다(서버 결함 판정 아님).",
                    gfile)
        if self._in_targets(name):
            head = self._answers_head(name)
            if head:
                code = _classify(head, "round_unmeasured")
                return (code, f"{rnd} 채점 회차에서 측정하지 못했다 — 채점 기록: “{head}”. 점수를 "
                        "매기지 않고 순위에서 뺐다.", f"answers/{self.slug.get(name) or self.slug.get(RENAMED.get(name, ''))}.md")
            m = self._note_mention(name, category)
            if m:
                return (_classify(m, "round_unmeasured"),
                        f"{rnd} 채점 회차에서 측정하지 못했다 — 채점 기록: “{m}”. 점수를 매기지 "
                        "않고 순위에서 뺐다.", "ranking.json")
            return ("round_unmeasured", f"{rnd} 채점 회차에 물어봤지만 채점 기록에 점수가 없다 — "
                    "순위에서 뺐다.", f"rounds/{rnd}/targets.tsv")
        # 명단에 없었다 — 그때 없었나, 있었는데 빠졌나
        if self.at_round is not None and (name in self.at_round
                                          or RENAMED.get(name) in self.at_round):
            m = self._note_mention(name, category)
            if m:
                code = _classify(m, "round_skipped")
                return (code, f"{rnd} 채점 회차에서 채점하지 않았다 — 채점 기록: “{m}”.",
                        "ranking.json")
            return ("round_skipped", f"{rnd} 채점 회차 당시 응답했지만 채점 명단에 들지 않았다 — "
                    "다음 월간 채점 회차(매월 첫 화요일) 대상이다.", f"rounds/{rnd}/targets.tsv")
        return ("awaiting_round",
                f"마지막 채점 회차({rnd})의 채점 명단에 없었다 — 그 회차 뒤에 새로 응답했거나 이 "
                "분야로 분류된 서버다. 다음 월간 채점 회차(매월 첫 화요일)에 같은 질문으로 채점한다.",
                f"rounds/{rnd}/targets.tsv")


def outside_counts(items: list[dict], cls: dict, pop: dict | None) -> dict[str, dict[str, int]]:
    """servers 배열 밖(가동을 못 잰) 후보의 분야별 건수 — {분야: {코드: 건수}}."""
    out: dict[str, dict[str, int]] = {}

    def add(cat, code):
        d = out.setdefault(cat or "분야 미분류", {})
        d[code] = d.get(code, 0) + 1
    for r in items:
        if r.get("remote"):
            continue
        add((cls.get(r["name"]) or {}).get("category"),
            "install_only" if r.get("package") else "no_address_no_package")
    for i in (pop or {}).get("not_measured") or []:
        add((cls.get(i.get("name")) or {}).get("category")
            or (i.get("categories") or [None])[0], "not_measured")
    return out


def derive_all(judging: Judging, *, live, unmeasured, dead, off, rank_of, cat_of,
               status_of) -> dict[str, tuple[str, str, str]]:
    """두드려 본 모든 줄 중 **순위표에 서 있지 않은** 줄 → (코드, 문장, 근거).

    「서 있다」= 비교 가능(live)이고 등수가 있고 분야 교정 대상이 아니다 — render_site의
    `ranked_now`와 같은 정의다. 지난 회차 등수만 남은 줄(rank_is_current=false)도 여기 든다.
    """
    ranked_now = {r["name"] for r in live if r["name"] in rank_of and r["name"] not in MISFILED}
    out = {}
    for rows, bucket in ((live, "comparable"), (off, "off_topic"),
                         (unmeasured, "unmeasurable"), (dead, None)):
        for r in rows:
            if r["name"] in ranked_now:
                continue
            out[r["name"]] = judging.reason(r["name"], bucket or status_of(r),
                                            r.get("remote"), cat_of(r))
    return out
