#!/usr/bin/env python3
"""축③(조인·계산·판정) 판정의 회귀 고정 (2026-08-21, T-2026W34-107).

**이 축은 남의 서버를 "단순 래퍼"라고 부를 수 있는 축이다.** 그러니 틀리는 방식이 정해져
있고, 이 저장소는 그 방식으로 이미 두 번 당했다 — 부분문자열 오탐(`dart` ⊂ agent`data`-nl)과
못 본 것을 없는 것으로 게시한 것(못 읽은 패키지명 → 남의 서버 `설치 불가`). 축③을 만들면서
같은 두 함정을 실제로 다시 밟았고(2026-08-21 실측: `get_checkout`이 `check`에 걸려 결제
액션 서버가 '판정형'이 됐다), 그래서 아래를 회귀로 박는다:

  1. **못 봄 ≠ 없음** — 도구 목록이 없으면 `unknown`이다. `retrieval_only`가 아니다
  2. **부분문자열 금지** — `checkout`·`cart`는 `check`에 걸리지 않는다(조각 단위로 맞춘다)
  3. **원천이 직접 주는 피드는 파생이 아니다** — recommend·rank는 애매로 남긴다
  4. **이름이 못 가른 것만 설명으로 가른다** — check_price_adjustment(계산) vs check_email_valid
  5. **축③은 keep/drop을 바꾸지 않는다** — 선정은 축①②만으로 결정된다
  6. **판정값이 원자료와 어긋나지 않는다** — "전부 조회형"이라 쓰면 세어서 맞아야 한다

실행: python3 -m pytest tests/test_value_add.py -q
"""
import json
import pathlib

import filter_candidates
import measure
import value_add

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _t(name, desc=""):
    return {"name": name, "desc": desc, "required": [], "props": [], "read_only": True}


# 1. 못 봄 ≠ 없음
def test_no_tools_is_unknown_not_zero():
    for arg in (None, []):
        a = value_add.axis3(arg)
        assert a["signal"] == "unknown", arg
    assert "없다는 뜻이 아니다" in value_add.axis3(None)["why"]


def test_unknown_is_not_retrieval_only():
    """모르는 것과 파생이 없는 것은 다른 판정이다 — 섞이면 208건이 '가치 없음'으로 게시된다."""
    assert value_add.axis3(None)["signal"] != value_add.axis3([_t("get_x"), _t("list_y")])["signal"]


# 2. 부분문자열 오탐
def test_checkout_is_not_check():
    """`get_checkout`·`create_cart`가 `check`에 걸리면 결제 액션 서버가 '판정형'이 된다."""
    # `check`에 걸려 '판정형'이 되면 안 된다. `checkout`은 거래 표면 명사라 action이다 —
    # 읽어도 사실이 아니라 내 장바구니를 주기 때문이다(value_add.ACTION 주석).
    assert value_add._cls("get_checkout") == "action"
    assert value_add._cls("create_checkout") == "action"
    assert value_add._cls("update_cart") == "action"
    assert value_add._cls("check_pccc") == "ambiguous"


def test_commerce_server_is_action_heavy():
    tools = [_t(n) for n in ("get_checkout", "create_checkout", "update_checkout",
                             "complete_checkout", "cancel_checkout", "get_cart",
                             "create_cart", "update_cart", "cancel_cart", "get_order",
                             "search_catalog", "lookup_catalog", "get_product")]
    assert value_add.axis3(tools)["signal"] == "action_heavy"


def test_exactly_half_action_is_not_majority():
    """정확히 반은 과반이 아니다 — `>=`로 쓰면 2종 중 1종짜리가 '과반'으로 게시된다."""
    a = value_add.axis3([_t("create_order"), _t("get_price")])
    assert a["signal"] != "action_heavy"
    assert value_add.axis3([_t("create_order"), _t("cancel_order"), _t("get_price")]
                           )["signal"] == "action_heavy"


def test_action_heavy_needs_majority():
    """3종 중 1종이 상태 변경형인 서버를 '상태 변경 위주'라 부르는 것도 근거 없이 깎는 것이다."""
    a = value_add.axis3([_t("transfer_1won"), _t("account_realname"), _t("bank_code")])
    assert a["signal"] == "retrieval_only"


# 3. 원천이 직접 주는 피드
def test_recommend_and_rank_stay_ambiguous():
    """언론사 '추천 기사'·거래소 '거래량 순위'는 원천이 그대로 주는 피드다."""
    assert value_add._cls("list_recommended_articles") == "ambiguous"
    assert value_add._cls("get_rankings") == "ambiguous"
    assert value_add._cls("suggest_law_names") == "ambiguous"
    # 반면 이것들은 원천 엔드포인트로 오기 어렵다
    for n in ("compare_datasets", "estimate_delay_penalty", "get_linked_ordinances",
              "find_references", "get_delegated_laws", "decide_contract_method"):
        assert value_add._cls(n) == "derive", n


def test_forecast_history_stats_are_not_derive():
    """기상 예보·시세 이력·통계는 원천 엔드포인트다 — 넣으면 '파생을 준다'가 부풀려진다."""
    for n in ("get_forecast", "get_history", "get_law_statistics"):
        assert value_add._cls(n) != "derive", n


# 4. 설명은 이름이 못 가른 자리에만 쓴다
def test_desc_resolves_only_ambiguous():
    calc = value_add.axis3([_t("check_price_adjustment", "물가변동에 따른 계약금액 조정률을 계산한다")])
    assert calc["signal"] == "derived"
    assert calc["resolved_by_desc"] == ["check_price_adjustment(설명: 계산)"]
    plain = value_add.axis3([_t("check_email_valid", "이메일 주소가 유효한지 확인합니다")])
    assert plain["signal"] == "ambiguous"
    assert "resolved_by_desc" not in plain


def test_desc_does_not_promote_retrieval_tools():
    """조회형 도구는 설명에 '비교'가 있어도 파생이 아니다 — 산문 매칭은 애매한 자리에만."""
    a = value_add.axis3([_t("get_price", "다른 단지와 비교할 때 쓰세요")])
    assert a["signal"] == "retrieval_only"


def test_basis_is_disclosed():
    """설명 없이 판정한 회차임을 값으로 밝힌다 — 안 밝히면 다음 회차와 비교가 안 된다."""
    assert value_add.axis3([_t("get_x")])["basis"].startswith("이름만")
    assert value_add.axis3([_t("get_x", "설명 있음")])["basis"] == "이름+설명"


def test_measure_keeps_truncated_desc_and_says_so():
    """설명을 앞 200자만 남기되 **잘랐다고 값으로 말한다**(기치 ②)."""
    spec = measure.tool_specs([{"name": "t", "description": "가" * 300,
                                "inputSchema": {}, "annotations": {}}])[0]
    assert len(spec["desc"]) == 200 and spec["desc_truncated"] is True
    assert "desc_truncated" not in measure.tool_specs(
        [{"name": "t", "description": "짧다", "inputSchema": {}, "annotations": {}}])[0]


# 5. 축③은 선정을 바꾸지 않는다
def test_axis3_never_changes_keep_drop():
    """도구 목록을 본 25건과 못 본 208건이 **같은 기준으로** keep/drop 돼야 한다."""
    item = {"name": "someone/korea-law-mcp", "description": "한국 법령 조회 MCP"}
    assert filter_candidates.classify(item)["verdict"] == "keep"
    for tools in (None, [], [_t("get_x")], [_t("compare_x")]):
        assert value_add.axis3(tools)["signal"] in {
            "unknown", "derived", "retrieval_only", "ambiguous", "action_heavy"}
        # classify는 도구 목록을 인자로 받지도 않는다 — 구조적으로 섞일 수 없다
    assert "axis3" not in filter_candidates.classify(item)


def test_pipeline_discloses_axis3_boundary(tmp_path, monkeypatch):
    """산출물이 축③의 경계를 스스로 말하는가 — unknown 건수와 '떨어뜨리지 않는다'를 공시한다.

    **게시본 파일을 읽어서 검사하지 않는다.** 처음엔 `candidates_filtered.json`을 열어
    boundaries를 봤는데, 그 파일은 gitignore 대상이면서 옛 버전이 추적돼 있어 **내 작업
    트리에서만 통과하는 테스트**였다(codex 교차검증 2026-08-21이 잡았다: 깨끗한 체크아웃에서
    실패한다). 7MB 산출물을 커밋해 통과시키는 것은 저장소가 export_candidates.py로 피하려던
    바로 그 이력 오염이다. 그래서 **코드 경로를 돌려** 공시를 검사한다.
    """
    src = tmp_path / "in.json"
    src.write_text(json.dumps({"boundaries": [], "items": [
        {"name": "someone/korea-law-mcp", "description": "한국 법령 조회 MCP"},
        {"name": "other/kr-stats-mcp", "description": "한국 통계 조회"}]}), encoding="utf-8")
    out = tmp_path / "out.json"
    monkeypatch.chdir(ROOT)   # schemas/tools.json을 실제 경로에서 읽게 둔다
    monkeypatch.setattr("sys.argv", ["filter_candidates.py", "--input", str(src),
                                     "--output", str(out)])
    assert filter_candidates.main() == 0
    d = json.loads(out.read_text(encoding="utf-8"))
    b = " ".join(d["boundaries"])
    assert "축③" in b and "파생이 없다는 뜻이 아니다" in b
    assert "후보를 떨어뜨리지 않는다" in b
    assert "원천이 이미 주는지는 대조하지 않았다" in b
    # 라벨은 붙었고, 판정은 축①②가 정했다
    assert all("axis3" in i for i in d["items"])
    assert d["buckets"]["keep"] == 2


# 6. 판정값이 원자료와 어긋나지 않는다
def test_why_counts_match_raw():
    a = value_add.axis3([_t("transfer_1won"), _t("account_realname"), _t("bank_code")])
    assert "전부" not in a["why"]
    assert f"/{a['tool_count']}종" in a["why"]
    assert sum(a["counts"].values()) == a["tool_count"]
