#!/usr/bin/env python3
"""자격증명을 **소스에 경로를 박지 않고** 찾는다 (T-2026W34-199, 2026-09-06).

**계기**: 이 저장소는 공개된다(github.com/sallim-app/korea-mcp-index). 그런데
`collect_candidates.py`·`enrich.py`가 토큰 파일의 **절대경로를 문자열로 들고 있었다** —
토큰 값은 없지만 "이 조직이 시크릿을 어디에 어떤 이름으로 보관하는가"는 공개된 셈이다.
값이 안 샜으니 저강도지만, 공격자에게 공짜로 주는 정보를 코드에 남길 이유가 없다.

**값을 저장소로 옮기지 않는다.** 흔한 오답이 `.env`에 토큰을 복사해 넣는 것인데, 그러면
경로 노출(저강도)을 값 복제(고강도)로 바꾸는 거래다. 시크릿의 단일 진실원은 서버의
시크릿 보관소 하나여야 한다. 그래서 저장소에는 **가리키는 파일**만 두고(gitignore 대상),
그 안에 값이 아니라 경로를 적는다.

찾는 순서 (먼저 잡히는 것이 이긴다):
  1. 환경변수 `<KEY>`            — 값 자체. CI·일회성 실행용.
  2. 환경변수 `<KEY>_FILE`       — env 형식 파일 경로. `:`로 여러 개(먼저 있는 것 우선).
  3. `.tokenpath.local`의 `<KEY>_FILE`  — 이 서버의 배선. 저장소에 커밋되지 않는다.
  4. 못 찾으면 None.

**키 이름을 credential마다 다르게 두는 것이 fail-closed의 전부다.** 수집기는 조직 접근이
없는 공개 전용 자격을 써야 하고(안 그러면 우리 비공개 저장소가 후보로 딸려 들어온다 —
collect_candidates.main 주석의 2026-08-18 실측), 보강기는 조직 자격을 쓴다. 두 곳이 같은
`GITHUB_TOKEN` 하나를 보면 주변 환경에 그 변수가 떠 있는 것만으로 그 구분이 무너진다.
그래서 수집기는 `GITHUB_TOKEN_PUBLIC`, 보강기는 `GITHUB_TOKEN`을 본다.
"""
from __future__ import annotations

import os
from pathlib import Path

# 저장소 안의 배선 파일. 값이 아니라 **경로만** 적는다 — .gitignore에 있다.
POINTER_FILE = Path(__file__).resolve().parent / ".tokenpath.local"


def _read_env_file(path: str | os.PathLike[str], key: str) -> str | None:
    """`KEY=값` 줄만 보는 최소 파서. 못 읽으면 None(없음 ≠ 실패로 취급하지 않는다)."""
    try:
        with open(path, encoding="utf-8") as fh:
            found = None
            for line in fh:
                line = line.strip()
                if line.startswith(f"{key}="):
                    found = line.split("=", 1)[1].strip()
            return found or None
    except OSError:
        return None


def _pointer(key: str) -> str | None:
    """`.tokenpath.local`이 `<key>`에 대해 가리키는 경로 목록(`:` 구분) — 없으면 None."""
    return _read_env_file(POINTER_FILE, key)


def token(key: str = "GITHUB_TOKEN") -> str | None:
    """`key` 자격증명의 값. 못 찾으면 None — 호출부가 인증 없이 돌지 결정한다.

    None을 예외로 바꾸지 않는 이유: 이 파이프라인은 인증 없이도(속도 제한 안에서) 돈다.
    공개 저장소를 clone한 사람이 토큰 없이 재현을 시도하는 것이 정상 경로다.
    """
    direct = os.environ.get(key)
    if direct and direct.strip():
        return direct.strip()

    paths = os.environ.get(f"{key}_FILE") or _pointer(f"{key}_FILE")
    if not paths:
        return None
    for path in paths.split(":"):
        path = path.strip()
        if not path:
            continue
        # 파일 안의 키 이름은 배선 파일이 가리키는 **원본 파일의 관례**를 따른다.
        # 공개/조직 자격이 같은 형식(`GITHUB_TOKEN=…`)이라 우리 키 이름으로 찾으면
        # 공개 자격 파일에서 아무것도 못 읽는다 — 실제 키 이름으로도 한 번 더 본다.
        got = _read_env_file(path, key) or _read_env_file(path, "GITHUB_TOKEN")
        if got:
            return got
    return None
