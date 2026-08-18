#!/usr/bin/env python3
"""실제로 써 보고 응답 품질을 잰다 (2026-08-19).

계기(사장님): *"도구에서 제공한다고 하는 것에 대해 MCP 써보고 답변 품질이나 데이터 품질
검사하면 되지 않아? 지금은 너무 아쉬운데"* — 맞다. 우리는 `tools/list`만 두드리고 끝냈다.
"도구 47종·설명 100%"까지 재놓고 **그 도구를 한 번도 불러본 적이 없었다.** 목록이 200을
줘도 도구를 부르면 500일 수 있고, 빈 배열만 올 수도 있고, 없는 것을 물으면 지어낼 수도 있다.

재는 것 4종 — **전부 도메인 지식 없이 판정된다**:
  ① 진짜 데이터가 나오나   대표 도구를 `{}`로 호출 → 레코드·빈배열·에러
  ② 없는 것을 지어내나     필수 문자열 인자에 헛값 → not_found인가 그럴듯한 답인가
  ③ 출처·기준시각을 밝히나  응답에 data_as_of·출처가 있나
  ④ 잘렸을 때 밝히나       작은 limit → 총계·truncated 공시
②가 기치 ②(못 봄 ≠ 없음)의 핵심 시험이고 이 목록이 남과 갈라지는 지점이다.

**주석 없는 서버는 부르지 않는다.** `readOnlyHint`가 없으면 그 도구가 뭘 바꾸는지 알 수 없다.
읽기 전용이라는 선언이 없는 남의 서버를 우리가 임의로 호출하면 안 된다 — 주석을 재는 이유를
행동으로 보이는 자리이기도 하다.

예의: 서버당 최대 4회, 호출 간 간격, UA로 정체 공개. 헛값 호출은 상대 로그에 남으므로
왜 그렇게 부르는지 JUDGING.md에 적어 둔다.

사용: probe_quality.py run     호출·저장(probes/)
      probe_quality.py merge   judge 결과 병합 → probe_verdicts.json
"""
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app; probing response quality)"
EXCERPT = 500          # 남의 데이터를 재배포하는 셈이라 발췌 상한을 둔다
MAX_CALLS = 4          # 서버당
PAUSE = 1.5
NONSENSE = "존재하지않는항목ZZZ9999"
PROBE_DIR = pathlib.Path("probes")
# 발췌에서 지우는 것 — 경매·부동산 응답에 개인정보가 섞일 수 있다
MASK = [(re.compile(r"01[016-9]-?\d{3,4}-?\d{4}"), "[전화]"),
        (re.compile(r"\d{6}-?[1-4]\d{6}"), "[주민번호]"),
        (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[이메일]")]


def slug(name: str) -> str:
    return hashlib.sha256(name.encode()).hexdigest()[:10]


def mask(t: str) -> str:
    for rx, rep in MASK:
        t = rx.sub(rep, t)
    return t


def call(url: str, method: str, params: dict | None = None) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                       "params": params or {}}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream", "User-Agent": UA})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read(2_000_000).decode("utf-8", "replace")
            code = r.status
    except urllib.error.HTTPError as e:
        raw, code = e.read().decode("utf-8", "replace")[:4000], e.code
    except Exception as e:
        return {"ok": False, "why": f"{type(e).__name__}", "ms": int((time.monotonic() - t0) * 1000)}
    return {"ok": code == 200, "http": code, "raw": raw,
            "ms": int((time.monotonic() - t0) * 1000)}


def payload(raw: str) -> tuple[str, dict]:
    """SSE·JSON 양쪽에서 result를 꺼내고, 본문 텍스트도 같이 돌려준다."""
    for c in [raw] + [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]:
        try:
            d = json.loads(c)
        except (ValueError, TypeError):
            continue
        if "result" in d or "error" in d:
            res = d.get("result") or {}
            texts = [b.get("text", "") for b in (res.get("content") or []) if isinstance(b, dict)]
            return ("\n".join(texts) or json.dumps(res, ensure_ascii=False)), d
    return raw, {}


# 응답 **본문**에 담겨 오는 에러. MCP는 isError 플래그 없이 result 안에 에러 JSON을 넣는
# 방식도 정상으로 친다 — 실제로 우리 서버가 quota_exceeded를 그렇게 준다. 플래그만 보면
# "데이터 나옴 O"로 오판한다(2026-08-19, 우리 서버 대조로 발견).
ERROR_KEYS = ("error", "errorcode", "error_code", "detail", "message")


def body_error(text: str) -> str:
    """응답 본문이 에러면 그 코드를, 아니면 빈 문자열."""
    try:
        d = json.loads(text)
    except (ValueError, TypeError):
        return ""
    if not isinstance(d, dict):
        return ""
    for k in ("error", "errorCode", "error_code"):
        v = d.get(k)
        if isinstance(v, str) and v:
            return v[:40]
        if isinstance(v, dict):
            return str(v.get("code") or v.get("message") or k)[:40]
    # 데이터가 하나도 없고 message만 있는 응답도 에러로 본다
    if set(d.keys()) <= set(ERROR_KEYS) and d.get("message"):
        return "message_only"
    return ""


def shape(text: str) -> dict:
    """구조 요약 — 발췌만으로는 안 보이는 것(레코드 수·필드)을 따로 센다."""
    out = {"bytes": len(text)}
    try:
        d = json.loads(text)
    except (ValueError, TypeError):
        return {**out, "json": False}
    out["json"] = True
    if isinstance(d, dict):
        out["fields"] = sorted(d.keys())[:14]
        for k, v in d.items():
            if isinstance(v, list):
                out["records"] = len(v)
                out["record_key"] = k
                break
    elif isinstance(d, list):
        out["records"] = len(d)
    return out


def pick(specs: list) -> tuple[dict | None, dict | None]:
    """(①④용 무인자 도구, ②용 문자열 1개 도구). 읽기 전용만 고른다."""
    ro = [t for t in specs if t.get("read_only")]
    free = next((t for t in ro if not t["required"]), None)
    one = next((t for t in ro if len(t["required"]) == 1), None)
    return free, one


def probe(name: str, url: str, specs: list) -> dict:
    free, one = pick(specs)
    rec: dict = {"server": name, "url": url, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "calls": [], "machine": {}}
    if not any(t.get("read_only") for t in specs):
        rec["skipped"] = "읽기전용 주석이 없어 호출하지 않았다 — 부작용을 알 수 없다"
        return rec

    def run(label: str, tool: str, args: dict) -> str:
        r = call(url, "tools/call", {"name": tool, "arguments": args})
        time.sleep(PAUSE)
        text, envelope = payload(r.get("raw", "")) if r.get("raw") else ("", {})
        rec["calls"].append({
            "label": label, "tool": tool, "arguments": args,
            "http": r.get("http"), "ms": r.get("ms"),
            "is_error": bool((envelope.get("result") or {}).get("isError") or envelope.get("error")
                             or body_error(text)),
            "error_code": body_error(text) or None,
            "shape": shape(text),
            "excerpt": mask(text)[:EXCERPT],
            "excerpt_truncated": len(text) > EXCERPT})
        return text

    if free:
        run("①데이터", free["name"], {})
        sh = rec["calls"][-1]["shape"]
        c0 = rec["calls"][-1]
        rec["machine"]["has_data"] = (not c0["is_error"]) and (
            bool(sh.get("records")) or sh.get("bytes", 0) > 80)
        if c0.get("error_code"):
            rec["machine"]["blocked_by"] = c0["error_code"]
        # ④ 같은 도구에 작은 limit — 잘랐다고 말하는가
        if "limit" in (free.get("props") or []):
            run("④절단공시", free["name"], {"limit": 1})
    if one:
        run("②환각", one["name"], {one["required"][0]: NONSENSE})
    return rec


def run_all() -> int:
    specs_all = json.load(open("schemas/tools.json", encoding="utf-8"))["items"]
    m = json.load(open("measured.json", encoding="utf-8"))["items"]
    cls = {v["name"]: v for v in json.load(open("classification.json", encoding="utf-8"))["items"].values()}
    PROBE_DIR.mkdir(exist_ok=True)
    targets = [i for i in m
               if (i.get("remote") or {}).get("tool_count")
               and cls.get(i["name"], {}).get("is_data_provider")
               and specs_all.get(i["name"])]
    print(f"검사 대상 {len(targets)}건")
    done = skipped = 0
    for n, i in enumerate(targets, 1):
        f = PROBE_DIR / f"{slug(i['name'])}.json"
        if f.exists():
            continue
        rec = probe(i["name"], i["remote"]["url"], specs_all[i["name"]])
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        if rec.get("skipped"):
            skipped += 1
        else:
            done += 1
        assert len(rec["calls"]) <= MAX_CALLS, f"{i['name']} 호출 상한 초과"
        if n % 5 == 0:
            print(f"  … {n}/{len(targets)}")
    print(f"호출 {done}건 · 주석 없어 건너뜀 {skipped}건 · 총 파일 {len(list(PROBE_DIR.glob('*.json')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all() if (len(sys.argv) < 2 or sys.argv[1] == "run") else 0)
