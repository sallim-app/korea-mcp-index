#!/usr/bin/env bash
# 웹판 게시 — 렌더 → Cloudflare Pages 배포 → **라이브 재검증** (2026-09-22, T-2026W39-28)
#
# **왜 스크립트인가.** 이 세 단계는 여태 회차 프롬프트 한 곳(주간 재측정)에만 명령어로
# 적혀 있었다. 그 프롬프트가 2026-09-17 멈추자 **게시하는 주체가 0이 됐다** — 그리고
# 아무것도 빨개지지 않았다: 회차는 완주하고, 커밋·푸시도 되고, README도 최신인데
# `mcp-index.sallim.app`만 조용히 낡는다(실측 2026-09-21: 라이브 generated_at 2026-09-16,
# 저장소 HEAD는 09-19 — 모바일 표 수리 두 건과 채점 정정 한 건이 라이브 밖에 있었다).
# 월간 채점 회차(매월 1일)는 순위를 바꾸는 유일한 회차인데 배포 단계가 **아예 없었다.**
#
# 그래서 배포를 프롬프트 문장에서 **저장소 안의 길목**으로 옮긴다 — 어느 회차가 돌든,
# 사람이 돌리든, 한 명령이다. 프롬프트는 이 스크립트를 부르기만 한다.
#
# 사용:
#   ./deploy-pages.sh                # 렌더 → 배포 → 라이브 재검증 (정상 경로)
#   ./deploy-pages.sh --dry-run      # 렌더 + 사전검사까지만 (배포 안 함)
#   ./deploy-pages.sh --verify-only  # 이미 있는 site/ 기준으로 라이브만 재검증
#
# 자격: `CLOUDFLARE_API_TOKEN`·`CLOUDFLARE_ACCOUNT_ID`가 환경에 있으면 그것을, 없으면
#   `tokens.credential_file()`이 `.tokenpath.local` 배선으로 찾은 env 파일을 서브셸에서만
#   읽는다. **경로도 값도 이 저장소에 들어오지 않는다**(tests/test_public_surface.py).
#
# 롤백: Cloudflare Pages `korea-mcp-index` → Deployments → 직전 배포 → Rollback (1회).
set -euo pipefail
cd "$(dirname "$0")"

SITE_URL="${SITE_URL:-https://mcp-index.sallim.app}"
PROJECT="${CF_PAGES_PROJECT:-korea-mcp-index}"
OUT="${SITE_OUT:-site}"

do_render=1; do_deploy=1; do_verify=1
for arg in "$@"; do
  case "$arg" in
    --dry-run)     do_deploy=0; do_verify=0 ;;
    --verify-only) do_render=0; do_deploy=0 ;;
    -h|--help)     sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "!! 모르는 인자: $arg" >&2; exit 2 ;;
  esac
done

# ── [1/4] 렌더 ──────────────────────────────────────────────────────────────
# `site/`는 gitignore다(커밋하면 diff가 49만 줄이라 교차검증이 죽는다) — 즉 **배포
# 직전에 다시 만드는 것이 정본**이고, 작업트리에 남아 있던 낡은 산출물을 올리지 않는다.
if [ "$do_render" = 1 ]; then
  echo "[1/4] 렌더 (render_site.py → $OUT)"
  python3 render_site.py --out "$OUT"
else
  echo "[1/4] 렌더 건너뜀(--verify-only)"
fi

# ── [2/4] 사전검사 — 올릴 것이 원자료와 같은 날인가 ──────────────────────────
# 렌더는 measured_at이 없으면 이미 멈춘다(fail-closed). 여기서 보는 것은 다른 것이다:
# **지금 올리려는 디렉토리**가 지금의 measured.json에서 나온 것인가. --verify-only로
# 남의 회차 산출물을 올리거나, 렌더가 다른 --out에 떨어진 채 옛 site/를 올리는 길을 막는다.
echo "[2/4] 사전검사"
python3 - "$OUT" <<'PY'
import json, pathlib, sys
out = pathlib.Path(sys.argv[1])
idx = out / "index.json"
if not idx.exists():
    sys.exit(f"생성물이 없다: {idx} — 먼저 `python3 render_site.py`를 돌려라.")
live = json.loads(idx.read_text(encoding="utf-8"))
src = json.loads(pathlib.Path("measured.json").read_text(encoding="utf-8"))
if live.get("measured_at") != src.get("measured_at"):
    sys.exit(f"생성물이 원자료와 다른 회차다 — site {live.get('measured_at')} ≠ "
             f"measured.json {src.get('measured_at')}. 다시 렌더하라.")
pages = len(list(out.rglob("*.html")))
if pages < 20:
    sys.exit(f"생성된 페이지가 {pages}건뿐이다 — 렌더가 중간에 깨진 것이지 "
             "목록이 빈 것이 아니다. 올리지 않는다.")
print(f"    측정일 {live['measured_at']} · 생성일 {live.get('generated_at')} · HTML {pages}건")
PY
[ -f "$OUT/sitemap.xml" ] || { echo "!! $OUT/sitemap.xml 이 없다 — 색인 배관 없이 올리지 않는다" >&2; exit 1; }

if [ "$do_deploy" = 0 ] && [ "$do_verify" = 0 ]; then
  echo "[3/4] 배포 건너뜀(--dry-run) · [4/4] 검증 건너뜀"
  exit 0
fi

# ── [3/4] Cloudflare Pages 배포 ─────────────────────────────────────────────
if [ "$do_deploy" = 1 ]; then
  echo "[3/4] Cloudflare Pages 배포 ($PROJECT)"
  if command -v wrangler >/dev/null 2>&1; then WRANGLER=(wrangler)
  else WRANGLER=(npx --yes wrangler@4); fi
  MSG="mcp-index $(git rev-parse --short HEAD 2>/dev/null || echo nogit) $(date '+%F %T')"
  if [ -n "${CLOUDFLARE_API_TOKEN:-}" ] && [ -n "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
    "${WRANGLER[@]}" pages deploy "$OUT" --project-name="$PROJECT" --branch=main \
      --commit-dirty=true --commit-message "$MSG"
  else
    # 경로는 소스에 없다 — 배선(.tokenpath.local)이 가리키는 파일을 **이 서브셸에서만** 읽는다.
    CF_ENV_FILE="${CF_ENV_FILE:-$(python3 -c 'import tokens; print(tokens.credential_file("CLOUDFLARE_API_TOKEN") or "")')}"
    [ -n "$CF_ENV_FILE" ] && [ -f "$CF_ENV_FILE" ] || {
      echo "!! Cloudflare 자격을 못 찾았다. 환경에 CLOUDFLARE_API_TOKEN·CLOUDFLARE_ACCOUNT_ID를 두거나," >&2
      echo "   .tokenpath.local 에 CLOUDFLARE_API_TOKEN_FILE=<env파일 경로> 를 적어라(값이 아니라 경로)." >&2
      exit 1; }
    ( set -a; . "$CF_ENV_FILE"; set +a
      "${WRANGLER[@]}" pages deploy "$OUT" --project-name="$PROJECT" --branch=main \
        --commit-dirty=true --commit-message "$MSG" )
  fi
else
  echo "[3/4] 배포 건너뜀(--verify-only)"
fi

# ── [4/4] 라이브 재검증 — **200을 봤다고 끝이 아니다** ──────────────────────
# 업로드 성공은 "우리 쪽이 보냈다"는 사실이고, 우리가 주장하려는 것은 "독자가 새 값을
# 본다"이다. 그래서 라이브 index.json이 **방금 만든 것과 같은 파일인지** 바이트로 본다.
# measured_at만 보면 회차가 바뀌지 않은 재배포(문구·표 수리)가 전부 통과한다 —
# 라이브가 낡은 채로 "검증됨"이 되는 정확히 그 구멍이다.
echo "[4/4] 라이브 재검증 ($SITE_URL)"
want="$(md5sum < "$OUT/index.json" | cut -d' ' -f1)"
got=""; code=000; body="$(mktemp)"; trap 'rm -f "$body"' EXIT
# 재시도는 CF 엣지 전파를 기다리는 장치다. 회귀 테스트는 로컬 서버를 두드리므로 기다릴
# 것이 없다 — 횟수를 주입할 수 있어야 **실패하는 길**도 검사 가능한 시간 안에 들어온다.
for i in $(seq 1 "${VERIFY_TRIES:-5}"); do
  code="$(curl -s -o "$body" -w '%{http_code}' --max-time 20 "$SITE_URL/index.json?cb=$$-$i")" || code=000
  got="$(md5sum < "$body" | cut -d' ' -f1)"
  echo "    index.json → HTTP $code (시도 $i/5)"
  [ "$code" = 200 ] && [ "$got" = "$want" ] && break
  sleep "${VERIFY_SLEEP:-6}"
done
# **본문만 보면 상태코드를 버린다**(codex 교차검증 2026-09-23). 같은 바이트를 500으로
# 돌려주는 엣지가 있어도 md5만 맞으면 통과해 `DONE`을 찍는다 — 우리가 주장하려는 것은
# "독자가 새 값을 **받는다**"이므로 200도 같이 성립해야 한다. 루프의 탈출 조건과 같은 식이다.
if [ "$code" != 200 ] || [ "$got" != "$want" ]; then
  echo "!! 라이브 index.json이 방금 만든 것과 다르다(HTTP $code) — 배포가 도달하지 않았다." >&2
  echo "   라이브: $(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("measured_at",d.get("measured_at"),"generated_at",d.get("generated_at"))' "$body" 2>/dev/null || echo '판독 불가')" >&2
  echo "   방금 만든 것: $(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("measured_at",d.get("measured_at"),"generated_at",d.get("generated_at"))' "$OUT/index.json")" >&2
  echo "   롤백: Cloudflare Pages $PROJECT → 직전 배포로 Rollback" >&2
  exit 1
fi

# 사이트맵에 적은 주소는 **우리가 색인해 달라고 제출한 주소**다. 하나라도 404면 그건
# 남에게 하는 거짓 약속이라 배포 실패로 센다. 판정 목록의 정본은 방금 만든 sitemap.xml이다.
mapfile -t paths < <(grep -o '<loc>[^<]*</loc>' "$OUT/sitemap.xml" \
                     | sed -e 's|<loc>||' -e 's|</loc>||' -e "s|^$SITE_URL||" | sed 's|^$|/|')
echo "    사이트맵 ${#paths[@]}건 전수 확인"
bad="$(printf '%s\n' "${paths[@]}" | grep . | timeout 180 xargs -P 8 -I{} sh -c \
  'c=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$1{}?cb=$2") || c=000
   [ "$c" = 200 ] || echo "{} → $c"' _ "$SITE_URL" "$$")" || {
  echo "!! 사이트맵 검증이 완주하지 못했다 — 미검증분을 200으로 세지 않는다" >&2; exit 1; }
[ -z "$bad" ] || { echo "!! 사이트맵 주소가 200이 아니다:"$'\n'"$bad" >&2
                   echo "   롤백: Cloudflare Pages $PROJECT → 직전 배포로 Rollback" >&2; exit 1; }

# 없는 주소가 200이면 라우팅이 모든 요청에 같은 페이지를 주고 있다는 뜻 — 위 전수 200이
# 통째로 무의미해진다(통과시키는 쪽 고장은 조용하다). 404 하나로 그 가정을 실측한다.
nf="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$SITE_URL/__no-such-page-$$")" || nf=000
[ "$nf" = 404 ] || { echo "!! 없는 주소가 HTTP $nf 다 — 전수 200 판정을 믿을 수 없다" >&2; exit 1; }
echo "    없는 주소 → 404 (전수 200 판정이 유효)"

# **여기까지 와야 '게시'다.** 회차 계수(carryover)가 이 도장을 본다 — `record()`는 배포보다
# 먼저 돌므로, 그것만으로 회차를 넘기면 배포가 실패한 회차도 회차로 세어져 아직 확정되지
# 않은 은퇴가 굳는다(codex 교차검증 2026-09-23). --verify-only 재검증에는 안 찍는다.
if [ "$do_deploy" = 1 ]; then
  python3 -c 'import carryover,sys; print("    게시 도장:", carryover.mark_deployed(sys.argv[1]))' \
    "$(date +%F)"
fi

echo "DONE — $SITE_URL 가 방금 만든 산출물과 같다(index.json md5 $want)"
