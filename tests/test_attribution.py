#!/usr/bin/env python3
"""귀속 회귀 — 우리가 만든 오류를 남의 서버 결함으로 게시하지 않는다 (2026-09-16).

2026-08-20에 우리는 **못 읽은 패키지명**을 남의 서버 `설치 불가`로 게시했다
(`tests/test_package_axis.py`). 2026-09-16에 같은 축의 두 번째 사고가 드러났다 —
`com.aikstockdata/mcp` 질문 2의 채점 문장이 「16048조 0억원」을 **서버 원문 발췌**라
부르며 자릿수 결함을 서버 탓으로 적었는데, 그 질문은 MCP 도구가 아니라 공개 JSON을
**직접 HTTP로 받아** 답한 것이었다. 그 사실은 우리 자신의 기록 `answers/`에 이미
'직접 API 호출'이라고 적혀 있었고, 채점자가 그것을 읽지 않았을 뿐이다. 운영자 본인이
이슈 #1로 짚어 줘서야 알았다(https://github.com/sallim-app/korea-mcp-index/issues/1).

**사람 눈으로는 안 잡힌다** — 두 파일이 떨어져 있고, 채점 문장은 길고, 틀린 귀속도
문장 자체는 그럴듯하다. 그래서 배관으로 건다: `answers/`가 도구 호출이 아니라 직접
호출이라고 적은 질문에 대해, 그 질문의 채점 문장이 출력을 **서버에 귀속**하면서
직접 호출이었다는 사실을 같은 문장에 달지 않으면 실패한다.

**뭉쳐 보면 안 되는 것이 핵심이다.** 사고 당시에도 같은 질문의 `완결성_why`에는 '공개
JSON을 직접 받아 만든 것'이 적혀 있었다 — 질문 전체를 한 덩이로 보면 그대로 통과한다.
필드로 나눠도 부족하다(codex 교차검증 2026-09-16): 긴 필드 안에서 한 문장이 서버 탓을
하고 저 멀리 딴 문장이 직접 호출을 말해도 통과한다. 그래서 **귀속한 자리 주변**만 본다.

실행: python3 -m pytest tests/test_attribution.py -q
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANSWERS = ROOT / "answers"
GRADES = ROOT / "grades"

# `answers/`의 「호출한 도구」표에서 **MCP 도구가 아닌** 줄. 이 줄이 있으면 그 질문의
# 출력은 서버가 프로토콜로 내준 것이 아니라 우리가 URL을 직접 두드려 받은 것이다.
DIRECT_CALL = re.compile(r"직접\s*(API|HTTP|호출|요청|내려받|받)")

# 출력을 **서버에 귀속**하는 말투. 이 말이 붙는 순간 그 문장은 남의 제품에 대한 주장이다.
ATTRIBUTES_TO_SERVER = re.compile(
    r"서버\s*원문|서버\s*출력|서버\s*응답|서버\s*발췌|서버\s*데이터"
    r"|서버가\s*(준|낸|돌려준|내놓은)|서버의?\s*(서식|포맷|형식)|서버\s*탓"
)

# 귀속을 **거둬들이는** 말. 직접 호출이었다고 밝히거나, 서버 것이 아니라고 부정하거나,
# 옛 표현을 인용하며 정정한다고 적는 자리다.
RETRACTS = re.compile(
    r"직접\s*(API|HTTP|호출|요청|내려받|받)|공개\s*JSON|MCP\s*도구가\s*아니"
    r"|아니(다|라|고|며|었|야)|오귀속|정정|종전|틀린\s*것이다"
)

# 거둬들이는 말이 귀속에서 얼마나 떨어져 있어도 되나. **필드 전체를 뭉쳐 보면 안 된다**
# (codex 교차검증 2026-09-16) — 한 문장이 서버 탓을 하고 저 멀리 딴 문장이 직접 호출을
# 말해도 통과해 버려, 이 회귀가 막겠다고 한 바로 그 오귀속을 놓친다. 그래서 창을 건다.
WINDOW = 80


def _server_of(md: str) -> str:
    """`answers/*.md` 첫 줄의 서버 이름. '— 수정 후 재측정' 같은 꼬리는 뗀다."""
    head = md.splitlines()[0].lstrip("# ").strip()
    return head.split("—")[0].strip()


def _direct_call_questions(md: str) -> set[int]:
    """직접 호출이 섞인 질문 번호. 「호출한 도구」표의 도구 칸만 본다."""
    found, q = set(), None
    for ln in md.splitlines():
        m = re.match(r"##\s*질문\s*(\d+)", ln)
        if m:
            q = int(m.group(1))
            continue
        if q is not None and ln.startswith("|") and DIRECT_CALL.search(ln.split("|")[2] if ln.count("|") > 2 else ""):
            found.add(q)
    return found


def _grade_texts(server: str, q: int) -> dict[str, str]:
    """그 서버·그 질문의 채점 문장들 — 필드 이름 → 문장. 없으면 빈 dict."""
    out = {}
    for path in sorted(GRADES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for s in data.get("servers", []):
            if s.get("server") != server:
                continue
            for item in s.get("questions", []):
                if item.get("q") != q:
                    continue
                for key, val in item.items():
                    if key.endswith("_why") and isinstance(val, str):
                        out[f"{path.name}:{key}"] = val
                for i, err in enumerate(item.get("사실오류") or []):
                    out[f"{path.name}:사실오류[{i}]"] = err
    return out


def _cases() -> list[tuple[str, int, str, str]]:
    """(서버, 질문번호, 필드, 문장) — 직접 호출로 답한 질문의 채점 문장 전부."""
    cases = []
    for path in sorted(ANSWERS.glob("*.md")):
        md = path.read_text(encoding="utf-8")
        server = _server_of(md)
        for q in sorted(_direct_call_questions(md)):
            for field, text in _grade_texts(server, q).items():
                cases.append((server, q, field, text))
    return cases


def test_parser_still_sees_the_known_case():
    """파서가 산출물과 어긋나면 이 회귀는 조용히 0건을 검사한다 — 실사고 1건을 못박는다."""
    md = (ANSWERS / "aikstockdata.md").read_text(encoding="utf-8")
    assert 2 in _direct_call_questions(md), (
        "answers/aikstockdata.md 질문 2의 '직접 API 호출' 줄을 못 읽었다 — 파서가 표 형식과 어긋났다")
    assert _grade_texts("com.aikstockdata/mcp", 2), "그 질문의 채점 문장을 grades/에서 못 찾았다"


def test_direct_call_output_is_not_blamed_on_the_server():
    """`answers/`가 '직접 호출'이라 적은 질문의 출력을 `grades/`가 '서버 원문'으로 귀속하면 실패.

    우리가 옮겨 적다 틀린 값을 남의 서버 결함으로 공개하는 자리다. 귀속을 아예 금지하지는
    않는다 — 정정 문장은 옛 표현을 인용해야 하니까. 대신 **같은 문장 안에** 직접 호출이었다는
    사실이 함께 있어야 한다.
    """
    cases = _cases()
    assert cases, "직접 호출로 답한 질문의 채점 문장이 하나도 안 잡혔다 — 파서 드리프트"
    bad = []
    for server, q, field, text in cases:
        for m in ATTRIBUTES_TO_SERVER.finditer(text):
            near = text[max(0, m.start() - WINDOW):m.end() + WINDOW]
            if not RETRACTS.search(near):
                bad.append((server, q, field, m.group(0), near[:120]))
    assert not bad, (
        "직접 호출로 받은 출력을 서버 탓으로 적었다(= 남의 서버에 대한 틀린 공개 주장): "
        f"{bad[:3]}")
