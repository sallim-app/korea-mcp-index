#!/usr/bin/env python3
"""후보를 다 재지도 않고 「후보 전체」라고 적지 않는가 (2026-09-14, T-2026W38-18).

계기. **판정기가 둘인데 모집단은 하나만 읽었다.** 키워드 판정기(`filter_candidates.py`)가
`review`로 미룬 218건은 한 번도 두드리지 않았는데, 그중 **105건은 같은 회차의 LLM 분류기가
이미 `is_data_provider: true`라고 판정**해 둔 것이었다(KOSIS·DART·특허청·법령, 그리고 우리
`app.sallim/korea-stay`). 그 상태로 게시본은 잰 줄 수 282를 **「후보 전체」**라고 적었다.

"못 본 것을 없는 것으로 적지 않는다"(기치 ②)를 이 목록이 자기 계수기에서 어긴 자리다.
그래서 둘을 못박는다.
  ① 모집단 규칙 — `measure.py`가 `keep`만 읽지 않고 승격분을 같이 잰다(배선까지 본다)
  ② 공시 — 게시본이 잰 것과 안 잰 것을 **둘 다 값으로** 싣는다

실행: python3 -m pytest tests/test_population_disclosure.py -q
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import population  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _items(verdicts):
    return [{"name": n, "verdict": v} for n, v in verdicts]


def _cls(pairs):
    return {n: {"name": n, "is_data_provider": d} for n, d in pairs}


# ── ① 모집단 규칙 ─────────────────────────────────────────────────────────
def test_review_that_llm_calls_a_data_provider_is_measured():
    """**이 회귀가 지키는 실제 사건.** review인데 LLM이 데이터 제공형이라 한 것은 잰다."""
    items = _items([("k/keep", "keep"), ("r/data", "review"), ("r/not", "review")])
    cls = _cls([("k/keep", True), ("r/data", True), ("r/not", False)])
    got = {i["name"] for i in population.measurable(items, cls)}
    assert got == {"k/keep", "r/data"}, got


def test_review_without_classification_is_not_promoted():
    """모르는 것을 '맞다'로 읽으면 모집단이 조용히 넓어진다 — 승격은 판정이 있을 때만."""
    items = _items([("r/unknown", "review")])
    assert population.measurable(items, {}) == []
    assert population.promoted(items, {}) == []


def test_drop_is_never_promoted():
    """한국 관련 신호가 0이라 떨어진 것은 분류기가 뭐라 하든 후보가 아니다."""
    items = _items([("d/dropped", "drop")])
    cls = _cls([("d/dropped", True)])
    assert population.measurable(items, cls) == []


def test_measure_py_reads_both_classifiers():
    """배선을 태운다 — 규칙만 있고 `measure.py`가 안 부르면 다음 회차에 또 빠진다."""
    src = (ROOT / "measure.py").read_text(encoding="utf-8")
    assert "population.measurable(" in src, (
        "measure.py가 모집단을 population.measurable로 고르지 않는다 — "
        "키워드 판정기의 keep만 읽으면 LLM이 데이터 제공형이라 한 것이 또 측정 밖에 남는다")
    assert 'i["verdict"] == a.bucket]' not in src, "옛 keep-only 선택이 남아 있다"
    # **분류가 없으면 멈춘다**(codex 2026-09-14): 경고만 찍고 keep만 재면 이 커밋이
    # 고치러 온 누락이 그대로 재발하는데 measured.json은 처음부터 다시 쓰인다.
    tail = src[src.index("population.load_classification()"):]
    assert "측정 중단" in tail[:500], (
        "classification.json이 없을 때 measure.py가 멈추지 않는다 — 좁아진 모집단이 "
        "조용히 게시본이 된다")


# ── ② 공시 ────────────────────────────────────────────────────────────────
def test_summary_matches_the_public_raw_files():
    """집계가 공개 원자료(candidates.json·classification.json)에서 그대로 나온다."""
    s = population.summary(str(ROOT / "candidates.json"), str(ROOT / "classification.json"),
                               str(ROOT / "measured.json"))
    assert s, "공개 원자료로 모집단을 못 센다"
    assert s["total"] == len(s["keep"]) + len(s["review"])
    assert s["total"] == len(s["measured"]) + len(s["not_measured"])
    assert (len(s["promoted"]) + len(s["review_off"]) + len(s["unclassified"])
            == len(s["not_measured"]))
    # 승격분은 전부 **안 잰 것**이고 전부 데이터 제공형 판정이어야 한다
    done = {i["name"] for i in s["measured"]}
    for i in s["promoted"]:
        assert i["name"] not in done
        assert s["cls"][i["name"]]["is_data_provider"] is True


def test_renderers_publish_what_they_did_not_measure():
    """게시본이 **안 잰 것을 값으로** 싣는가. 잰 것의 합계를 후보 전체로 적지 않는다."""
    s = population.summary(str(ROOT / "candidates.json"), str(ROOT / "classification.json"),
                               str(ROOT / "measured.json"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"| **후보 전체** | {s['total']}건 |" in readme, (
        f"README의 「후보 전체」가 {s['total']}건이 아니다 — 잰 줄 수를 후보 총수로 적고 있다")
    assert f"{len(s['promoted'])}건" in readme
    assert "재지 않은 후보" in readme
    for src_name in ("render_site.py", "render_readme.py"):
        src = (ROOT / src_name).read_text(encoding="utf-8")
        assert "population.summary()" in src, f"{src_name}가 안 잰 모집단을 안 읽는다"


def test_the_published_total_is_bigger_than_what_we_measured():
    """수가 같아지면 둘 중 하나다 — 다 쟀거나, 계수기가 또 거짓말하거나.

    다 잰 회차라면 이 회귀는 스스로 비켜선다(그때는 `review`가 0이다). 지금은 0이 아니다.
    """
    s = population.summary(str(ROOT / "candidates.json"), str(ROOT / "classification.json"),
                               str(ROOT / "measured.json"))
    measured = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    if not s["not_measured"]:
        return
    assert len(measured["items"]) < s["total"]

def test_the_disclosure_shrinks_itself_once_we_actually_measure_them():
    """**승격이 적용된 회차엔 이 공시가 스스로 0으로 줄어야 한다.**

    통 이름(`review`)으로 "안 잰 것"을 세면 105건을 다 재 놓고도 "재지 않은 218건"이라고
    적게 된다 — 고친 결함과 방향만 반대인 같은 거짓말이다. 그래서 measured.json에 이름이
    있는가로 가르고, 그 성질을 여기서 태운다(막는 쪽 고장은 시끄럽고 통과시키는 쪽 고장은
    조용하다 — 스킬 guard-liveness).
    """
    import tempfile

    now = population.summary(str(ROOT / "candidates.json"),
                             str(ROOT / "classification.json"),
                             str(ROOT / "measured.json"))
    assert now["promoted"], "지금 회차엔 승격 대상이 있어야 이 회귀가 의미가 있다"
    m = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    m["items"] = m["items"] + [{"name": i["name"]} for i in now["promoted"]]
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8",
                                     delete=False) as f:
        json.dump(m, f, ensure_ascii=False)
        fake = f.name
    after = population.summary(str(ROOT / "candidates.json"),
                               str(ROOT / "classification.json"), fake)
    assert after["promoted"] == [], "다 재고도 '재지 않았다'고 적는다"
    assert len(after["not_measured"]) == len(now["not_measured"]) - len(now["promoted"])


def test_every_unmeasured_candidate_has_a_row_not_just_a_count():
    """「전체 명단」이라 써 놓고 표에 없는 줄이 생기면, 이 페이지가 고치러 온 결함이다.

    계기(codex 교차검증 2026-09-14): 초판은 `promoted`·`review_off` 두 표만 돌고
    분류가 없는 줄은 **건수만** 적었다. 지금은 0건이라 화면에 안 보이지만, 다음 회차에
    분류 단계가 몇 건을 못 보면 그 서버들이 조용히 사라진다.
    """
    import subprocess
    import tempfile

    s = population.summary(str(ROOT / "candidates.json"),
                           str(ROOT / "classification.json"),
                           str(ROOT / "measured.json"))
    covered = {i["name"] for i in s["promoted"]} | {i["name"] for i in s["review_off"]} \
        | {i["name"] for i in s["unclassified"]}
    assert covered == {i["name"] for i in s["not_measured"]}, "집계가 명단을 덮지 못한다"
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "site"   # 없는 디렉토리여야 한다(rmtree 자물쇠)
        r = subprocess.run([sys.executable, "render_site.py", "--out", str(out)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        html = (out / "not-measured.html").read_text(encoding="utf-8")
    missing = [n for n in covered if n not in html]
    assert not missing, f"안 잰 후보가 명단에 없다: {missing[:5]}"
