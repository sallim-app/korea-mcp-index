#!/usr/bin/env python3
"""공개 저장소에 나가면 안 되는 두 가지를 고정한다 — 대용량 산출물과 시크릿 경로 (T-2026W34-199).

**계기(실측 2026-08-21).** 이 저장소는 공개된다. 그런데 두 종류가 새고 있었다.

1. **gitignore 대상인데 추적되던 산출물.** `candidates_filtered.json`(7,077,263B)과
   `candidates_raw.json`(5,172,625B)이 .gitignore에 이름이 있으면서 동시에 인덱스에
   있었다. `.gitignore`는 **이미 추적 중인 파일에 아무 힘이 없다** — 그것이 이 고장이
   조용한 이유다. 대가는 저장소 무게만이 아니었다: 그 파일을 읽는 테스트가 **내 작업
   트리에서만 통과**했고(codex 교차검증이 잡았다, test_value_add 주석 참조), 커밋
   diff가 49만 줄이 되어 배포 전 교차검증이 타임아웃으로 죽었다(2026-08-29 rc=124).
   2026-08-31 커밋 1bc8e3d가 인덱스에서 뺐고, 이 테스트가 되돌아오는 것을 막는다.

2. **시크릿 보관 경로 문자열.** `collect_candidates.py`·`enrich.py`·`answers/`가 토큰
   env 파일의 절대경로를 들고 있었다. 토큰 **값**은 없었지만 "이 조직이 시크릿을 어디에
   어떤 이름으로 두는가"는 공개된 셈이다. 배선은 `tokens.py`가 저장소 밖에서 찾는다.

**둘 다 "돌려놓기"가 쉬운 종류다.** 대용량 파일은 `git add .` 한 번, 경로 문자열은
디버깅하다 박은 한 줄이면 돌아온다. 그래서 고친 것으로 끝내지 않고 여기 박는다.

실행: python3 -m pytest tests/test_public_surface.py -q
"""
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 우리 시크릿 보관소. 리터럴을 쪼개 둔 이유는 **이 파일도 스캔 대상이기 때문**이다 —
# 가드가 자기 자신에 걸리면 예외 목록을 만들게 되고, 예외 목록은 곧 구멍이 된다.
SECRET_STORE = "/" + "data/" + "secrets"

# 어느 디렉토리든 **절대경로로 가리킨 env 파일**. `cp .env.example .env`처럼 남의 README에서
# 인용한 상대경로 명령은 잡지 않는다(test_package_axis의 실제 표본이 그렇다).
ABS_ENV_FILE = re.compile(r"(?<![\w.-])/(?:data|home|etc|opt|mnt|srv|root)/[\w./-]*\.env\b")

# 이 가드가 **못 보는 것**을 적어 둔다(경계 공시): 과거 커밋의 blob은 여기서 안 본다.
# 이력에 이미 들어간 것은 force push 금지(D-2026W32-36)라 소급 불가이고, 이 테스트의
# 목적은 "더 늘지 않게"다.


def _git(*args: str) -> str:
    p = subprocess.run(["git", "-C", str(ROOT), *args],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, f"git {' '.join(args)} 실패: {p.stderr.strip()}"
    return p.stdout


def _tracked() -> list[str]:
    files = [f for f in _git("ls-files", "-z").split("\0") if f]
    assert len(files) > 50, f"추적 파일이 {len(files)}건 — 스캔이 비었다면 통과는 무의미하다"
    return files


def test_no_tracked_file_is_gitignored():
    """`.gitignore`에 있는데 추적 중인 파일이 0건인가.

    `git ls-files -i -c --exclude-standard`가 판정기다 — 우리가 패턴을 다시 해석하지
    않는다. 재해석하면 git과 우리 사이의 차이가 그대로 맹점이 된다.
    """
    offenders = [f for f in _git("ls-files", "-i", "-c", "--exclude-standard",
                                 "-z").split("\0") if f]
    assert not offenders, (
        "gitignore 대상인데 인덱스에 있다 — `git rm --cached <파일>`로 뺀다. "
        f"해당: {offenders}")


def test_token_pointer_file_is_never_tracked():
    """`.tokenpath.local`(시크릿 위치 배선)이 추적되면 순화의 목적이 통째로 무너진다."""
    assert ".tokenpath.local" not in _tracked()
    # 존재 여부와 무관하게 **패턴이 살아 있는지**까지 본다. 파일이 없는 체크아웃에서
    # check-ignore는 종료코드로만 답하므로 그것을 읽는다(0=무시됨).
    p = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", ".tokenpath.local"],
                       capture_output=True, text=True, timeout=30)
    assert p.returncode == 0, ".gitignore에 .tokenpath.local 패턴이 없다"


def test_no_secret_store_paths_in_tracked_files():
    """추적 파일 어디에도 시크릿 보관소 경로·절대 env 경로가 없는가."""
    hits = []
    for rel in _tracked():
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue   # 바이너리·심링크는 경로 문자열의 매개가 아니다
        for n, line in enumerate(text.splitlines(), 1):
            if SECRET_STORE in line or ABS_ENV_FILE.search(line):
                hits.append(f"{rel}:{n}: {line.strip()[:100]}")
    assert not hits, (
        "공개 소스에 시크릿 보관 경로가 있다 — 값을 저장소로 복사하지 말고 "
        "tokens.py 배선(.tokenpath.local)으로 옮겨라.\n" + "\n".join(hits))


def test_guard_actually_fires():
    """가드가 **지금 이 환경에서** 무언가를 잡는지 확인한다.

    통과시키는 쪽 고장은 조용하다 — 위 세 테스트는 "0건"으로 통과하므로, 스캐너가
    깨져 아무것도 안 읽어도 똑같이 초록이다. 그래서 실제 위반 표본을 만들어 걸리는지 본다.
    """
    # **표본도 쪼개 쓴다.** 처음엔 리터럴로 적었다가 이 파일이 추적된 순간 위 스캐너가
    # 자기 픽스처를 위반으로 잡았다(커밋 직전 실측). 표본이 스캔에 걸리면 남는 선택지는
    # 파일 예외 목록뿐이고, 예외 목록은 곧 이 가드의 구멍이 된다.
    live = SECRET_STORE + "/github-sallim" + ".env"
    other = "/" + "home/ubuntu/.creds/gh" + ".env"     # 보관소가 바뀌어도 잡는가
    dead = "cp .env.example .env"          # 남의 README 인용 — 잡으면 안 된다
    assert SECRET_STORE in live
    assert ABS_ENV_FILE.search(live)
    assert ABS_ENV_FILE.search(f"token = open({other!r}).read()")
    assert SECRET_STORE not in dead and not ABS_ENV_FILE.search(dead)
