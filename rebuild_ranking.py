#!/usr/bin/env python3
"""분야별 채점(grades/) → 순위(ranking.json) 재산출 (2026-08-19).

**왜 다시 쓰나**: 종전 순위는 `tools/list` 지표만 보고 매긴 블라인드 심사였다. 실제로
물어보니 그 순위가 틀렸다 — 도구 125종으로 "도구 최다 1위"였던 서버가 법령 도구 전체가
API 키 오류로 죽어 사실을 한 줄도 못 줬고, 부동산 2위는 실거래가 대신 산식 미공개 매매
신호를 답으로 냈다. **작동을 안 보고 매긴 순위는 순위가 아니다.**

이제 순위는 채점자의 `권장순위`를 그대로 쓴다. 우리가 가중치를 새로 만들지 않는다 —
가중치를 우리가 정하는 순간 우리가 상위권인 표에서 그 설계를 반박할 방법이 없어진다.
채점자는 분야마다 하나이고, 기준·근거·사실오류를 전부 공개한다(JUDGING.md).

`why`는 채점자의 총평을 쓰되, 사실오류가 있으면 **그것을 먼저 적는다** — 독자가 다른
데서 못 얻는 정보가 그것이고, 순위 위쪽에 있다고 흠이 가려지면 안 된다.

**분야가 틀린 서버는 순위에서 뺀다**(2026-08-19, `observed.py`). 뉴스 서버에게 상품
질문을 던지고 못 답했다고 순위를 내리는 것은 그 서버를 잰 것이 아니라 우리 수집기의
오분류를 그 서버 탓으로 돌린 것이다. 뺀 것은 감추지 않고 `분야교정`에 남겨 README가
「분야 교정」 구역으로 싣는다.
"""
import json
import pathlib

from observed import MISFILED


def main() -> int:
    items = {}
    for f in sorted(pathlib.Path("grades").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if "servers" not in d:
            continue
        cat = d["category"]
        by = {s["server"]: s for s in d["servers"]}
        top, moved = [], []
        for name in d.get("권장순위") or []:
            s = by.get(name)
            if not s:
                continue
            if name in MISFILED:
                moved.append({"name": name, "실제분야": MISFILED[name][1],
                              "근거": MISFILED[name][2]})
                continue
            rank = len(top) + 1
            errs = [e for q in s["questions"] for e in (q.get("사실오류") or [])]
            why = s.get("총평", "")
            if errs:
                why = f"사실오류 {len(errs)}건 — {errs[0][:60]} · {why}"
            top.append({"name": name, "rank": rank, "why": why[:200],
                        "사실오류": len(errs),
                        "점수": [{k: q.get(k) for k in ("q", "정확성", "근거성", "완결성")}
                                for q in s["questions"]]})
        if not top:
            continue
        items[f"graded:{cat}"] = {
            "category": cat, "top": top[:3], "전체순위": [t["name"] for t in top],
            "분야교정": moved,
            "note": d.get("분야_총평", "")[:200], "candidates": len(d["servers"]),
            "by": "opus(실제 질문·답변 채점)", "순위_근거": d.get("순위_근거", "")[:200]}

    json.dump({"note": "분야별 순위. 근거는 실제 질문에 대한 답변을 Opus가 채점한 결과이며, "
                       "질문·호출기록·답변·채점이 answers/·grades/에 전부 있다. "
                       "기준 전문은 JUDGING.md. 우리가 가중치를 새로 만들지 않는다 — "
                       "채점자의 권장순위를 그대로 쓴다.",
               "model": "claude-opus (채점) / claude-haiku (답변 생성)",
               "items": items},
              open("ranking.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ranking.json 재산출 — 분야 {len(items)}개")
    for v in items.values():
        errs = sum(t["사실오류"] for t in v["top"])
        print(f"  {v['category']:<14} {' › '.join(t['name'].split('/')[-1][:20] for t in v['top'])}"
              f"   (상위3 사실오류 {errs}건"
              + (f" · 분야교정 {len(v['분야교정'])}건 제외" if v["분야교정"] else "") + ")")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
