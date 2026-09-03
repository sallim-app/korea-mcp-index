#!/usr/bin/env python3
"""항목이 흔적 없이 사라지지 않는가 — 그리고 계수기가 거짓말하지 않는가.

계기(2026-09-03, T-2026W35-119 후속 · 본선 재검증). 두드리개가 리다이렉트를 따라가게
되자 `contract.naru.build/mcp`(308)가 `contract.sallim.app/mcp`로 밝혀졌고, 같은 주소를
가리키던 우리 서버 두 줄이 `export_candidates.py`의 엔드포인트 병합에서 하나로 합쳐졌다.
본선이 "서버 3건이 조용히 떨어진다"로 잡았고, 파고들자 **더 오래된 결함 둘**이 나왔다.

  ① **계수기가 거짓말한다.** 병합이 `items`를 줄이면서 `measured` 필드는 measure.py가
     적어 둔 값 그대로였다. 8/31 커밋본이 이미 `measured: 277 / items: 275`였다.
     아무도 그 필드를 안 읽어서(소비자 0) 조용히 틀린 채 공개 원자료로 나갔다.
  ② **공개 표 두 개가 서로 다른 건수를 싣는다.** 문서화된 실행 순서가 `recompute.py`
     → `export_candidates.py`라, 병합이 axes.csv 뒤에 일어난다. 합칠 것이 0건인 회차에는
     안 보이고, 1건이라도 생기면 axes.csv와 measured.json의 행수가 갈린다.

셋 다 같은 뿌리다 — **줄이 사라지는데 그 사실을 값으로 말하지 않는다**(기치 ②).
못 본 것을 사망으로 적는 것보다 나쁘다: 사망으로도 안 적히고 아예 없는 것이 된다.

실행: python3 -m pytest tests/test_no_silent_item_loss.py -q
"""
import csv
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import export_candidates  # noqa: E402
import recompute  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEASURED = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))


def rec(name, url, **kw):
    return {"name": name, "remote": ({"url": url} if url else None), **kw}


# ── 합치는 것은 지우는 것이 아니다 ─────────────────────────────────────────
def test_merged_names_survive_in_also_known_as():
    """합쳐진 이름이 `also_known_as`에 남아야 한다 — 없으면 흔적 없는 증발이다."""
    items = [rec("a/one", "https://x.test/mcp"),
             rec("b/two", "https://x.test/mcp?via=official"),
             rec("c/three", "https://y.test/mcp")]
    dedup, dropped = export_candidates.merge_by_endpoint(items)
    assert dropped == 1
    assert len(dedup) == 2
    names = {i["name"] for i in dedup}
    aka = {n for i in dedup for n in (i.get("also_known_as") or [])}
    assert names | aka == {"a/one", "b/two", "c/three"}, "합치면서 이름을 잃었다"
    assert "b/two" in aka


def test_redirect_revealed_duplicate_is_merged_not_dropped():
    """**이 회귀가 지키는 실제 사건.** 308을 따라가자 두 줄이 같은 주소로 밝혀졌다."""
    items = [rec("app.sallim/contract-compass", "https://contract.sallim.app/mcp?via=official"),
             rec("build.naru/contract-compass", "https://contract.sallim.app/mcp")]
    dedup, dropped = export_candidates.merge_by_endpoint(items)
    assert dropped == 1
    assert dedup[0]["also_known_as"] == ["build.naru/contract-compass"]


def test_items_without_endpoint_are_never_merged():
    """주소가 없는 줄끼리 합쳐지면 안 된다 — 빈 문자열은 같은 서버라는 근거가 아니다."""
    items = [rec("a/none", None), rec("b/none", None), rec("c/empty", "")]
    dedup, dropped = export_candidates.merge_by_endpoint(items)
    assert dropped == 0
    assert len(dedup) == 3


# ── 계수기는 기록한 줄을 센다 ──────────────────────────────────────────────
def test_measured_counter_equals_recorded_rows():
    """게시된 `measured`는 **실제로 실린 줄 수**여야 한다.

    8/31 커밋본은 277이라 적고 275줄을 실었다. 이 값에는 소비자가 없어서 아무도
    안 멈췄다 — 소비자 없는 값이 조용히 틀리는 자리라 회귀로 소비자를 만든다.
    """
    assert MEASURED["measured"] == len(MEASURED["items"]), (
        f"measured={MEASURED['measured']} 인데 실린 줄은 {len(MEASURED['items'])}건이다 — "
        "공개 원자료가 자기 건수를 틀리게 말하고 있다")


def test_merge_is_disclosed_not_hidden():
    """합쳤으면 **합쳤다고 값으로 말한다**. 조용히 줄이면 그것이 절단 미공시다."""
    merged = MEASURED.get("merged_endpoints")
    assert merged is not None, "병합 공시 필드가 없다"
    assert "merge_note" in MEASURED
    for row in merged:
        assert row["merged"], row
        assert row["kept"] in {i["name"] for i in MEASURED["items"]}
    # 공시된 병합 이름은 실제 줄의 also_known_as와 일치해야 한다
    from_items = {n for i in MEASURED["items"] for n in (i.get("also_known_as") or [])}
    from_note = {n for row in merged for n in row["merged"]}
    assert from_items == from_note, (from_items ^ from_note)


def test_axes_csv_row_count_tracks_measured_items():
    """공개 표 두 개가 서로 다른 건수를 실으면 재계산의 기준이 무너진다."""
    with open(ROOT / "axes.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader([ln for ln in f if not ln.startswith("#")]))
    assert len(rows) == len(MEASURED["items"]), (
        f"axes.csv {len(rows)}행 ≠ measured.json {len(MEASURED['items'])}줄 — "
        "병합이 axes.csv 뒤에 일어났다(실행 순서 의존)")


def test_export_reemits_axes_so_order_does_not_matter(tmp_path, monkeypatch):
    """**순서를 지키라고 적는 대신 순서에 무관하게 만든다**(D-2026W32-19).

    `export_candidates.py`가 measured.json을 줄인 뒤 axes.csv를 다시 펴지 않으면,
    문서화된 순서(recompute → export)에서 두 파일이 갈린다.
    """
    src = json.loads((ROOT / "measured.json").read_text(encoding="utf-8"))
    dup = dict(src["items"][0])
    dup["name"] = "dup/for-test"
    # 첫 줄과 같은 주소를 가진 가짜 한 줄을 넣어 병합이 일어나게 만든다
    if not (src["items"][0].get("remote") or {}).get("url"):
        for i in src["items"]:
            if (i.get("remote") or {}).get("url"):
                dup = {**i, "name": "dup/for-test"}
                break
    src["items"] = [*src["items"], dup]
    for name in ("measured.json", "classification.json", "ranking.json"):
        p = ROOT / name
        if p.exists():
            (tmp_path / name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "measured.json").write_text(json.dumps(src, ensure_ascii=False),
                                            encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    # 문서화된 순서 그대로: 먼저 axes.csv를 편다(= 병합 전 건수)
    d0, items0 = recompute.rows()
    recompute.write_csv(items0)
    before = len(list(csv.DictReader(
        [ln for ln in (tmp_path / "axes.csv").read_text(encoding="utf-8").splitlines()
         if not ln.startswith("#")])))
    assert before == len(src["items"]), "선행 axes.csv가 병합 전 건수여야 한다"
    # 그다음 병합 단계가 돈다
    m = json.loads((tmp_path / "measured.json").read_text(encoding="utf-8"))
    dedup, dropped = export_candidates.merge_by_endpoint(m["items"])
    assert dropped == 1
    m["items"] = dedup
    m["measured"] = len(dedup)
    (tmp_path / "measured.json").write_text(json.dumps(m, ensure_ascii=False),
                                            encoding="utf-8")
    d1, items1 = recompute.rows()
    recompute.write_csv(items1)
    after = len(list(csv.DictReader(
        [ln for ln in (tmp_path / "axes.csv").read_text(encoding="utf-8").splitlines()
         if not ln.startswith("#")])))
    assert after == len(dedup), "병합 뒤 axes.csv를 다시 펴지 않으면 두 파일이 갈린다"


def test_export_rewrites_the_counter_end_to_end(tmp_path):
    """**배선을 태운다.** 산출물만 검사하면 코드를 되돌려도 회귀가 안 빨개진다.

    실측(2026-09-03): `m["measured"] = len(dedup)` 을 옛 동작으로 되돌리는 변이를 넣었는데
    산출물 검사 9건이 전부 통과했다 — 디스크의 measured.json은 이미 고쳐진 상태였으니까.
    막는 쪽 고장은 시끄럽고 통과시키는 쪽 고장은 조용하다(스킬 guard-liveness). 그래서
    실제로 스크립트를 돌려 **계수기가 다시 계산되는지**를 본다.
    """
    ep = "https://same.test/mcp"
    m = {"measured": 999, "unmeasurable": 0, "boundaries": [],
         "criteria_note": "t", "measured_at": "2026-09-03", "axes_at": "2026-09-03",
         "items": [
             {"name": "a/one", "repo_url": "https://github.com/a/one",
              "remote": {"url": ep, "status": "live", "reachable": True, "tool_count": 1}},
             {"name": "b/two", "repo_url": "https://github.com/b/two",
              "remote": {"url": ep + "?via=x", "status": "live", "reachable": True,
                         "tool_count": 1}},
             {"name": "c/three", "repo_url": "https://github.com/c/three",
              "remote": {"url": "https://other.test/mcp", "status": "unverified",
                         "reachable": False}}]}
    (tmp_path / "measured.json").write_text(json.dumps(m, ensure_ascii=False),
                                            encoding="utf-8")
    (tmp_path / "candidates_filtered.json").write_text(
        json.dumps({"items": [], "buckets": {}, "boundaries": []}), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "export_candidates.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    got = json.loads((tmp_path / "measured.json").read_text(encoding="utf-8"))
    assert len(got["items"]) == 2, "같은 엔드포인트 두 줄이 안 합쳐졌다"
    assert got["measured"] == 2, (
        f"계수기가 {got['measured']}로 남았다 — 줄을 줄이고도 건수를 다시 세지 않는다")
    assert got["measured"] == len(got["items"])
    aka = {n for i in got["items"] for n in (i.get("also_known_as") or [])}
    assert aka == {"b/two"}, "합쳐진 이름의 흔적이 없다"
    assert sum(len(x["merged"]) for x in got["merged_endpoints"]) == 1
    rows = list(csv.DictReader(
        [ln for ln in (tmp_path / "axes.csv").read_text(encoding="utf-8").splitlines()
         if not ln.startswith("#")]))
    assert len(rows) == 2, "병합 뒤 axes.csv를 다시 펴지 않았다"


def test_export_candidates_calls_recompute_at_the_end():
    """도구가 실제로 그렇게 배선돼 있는가 — 주석만 있고 배선이 없으면 다음에 또 갈린다."""
    src = (ROOT / "export_candidates.py").read_text(encoding="utf-8")
    tail = src[src.index('json.dump(m, open("measured.json"'):]
    assert "recompute.write_csv" in tail, (
        "measured.json을 다시 쓴 뒤 axes.csv를 다시 펴지 않는다 — 실행 순서에 의존한다")


def test_pipeline_artifacts_agree(tmp_path):
    """마지막 그물 — 게시본 재현 검사가 통과하는가."""
    r = subprocess.run([sys.executable, "recompute.py", "--verify"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
