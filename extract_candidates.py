#!/usr/bin/env python3
"""awesome-mcp-korea README에서 후보와 카테고리를 뽑는다.

왜 스크립트인가: 목록은 계속 바뀐다. 사람이 옮겨 적으면 그 순간부터 우리 목록도
'6개월 뒤 정체된 29개' 중 하나가 된다 — 재측정이 해자라면 입력도 재수집이어야 한다.
"""
import json
import re
import sys
import urllib.request

SRC = "https://raw.githubusercontent.com/darjeeling/awesome-mcp-korea/main/README.md"
# 목록 섹션이 아닌 문서 섹션 — 후보로 세면 안 된다.
SKIP = {"MCP란 무엇인가?", "선정 기준 (Inclusion Criteria)", "목록 (List)",
        "기여 방법 (Contributing)", "라이선스 (License)", "관련 프로젝트 (Related Projects)"}


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode("utf-8")


def parse(md: str) -> list[dict]:
    out, cat, seen = [], None, set()
    for line in md.splitlines():
        h = re.match(r"^##+\s+(.+?)\s*$", line)
        if h:
            title = re.sub(r"^[^\w가-힣]+", "", h.group(1)).strip()
            cat = None if title in SKIP else title
            continue
        if not cat:
            continue
        m = re.search(r"\[([^\]]+)\]\(https://github\.com/([\w.-]+)/([\w.-]+)", line)
        if not m:
            continue
        repo = f"{m.group(2)}/{m.group(3).rstrip('/')}"
        if repo in seen:
            continue
        seen.add(repo)
        out.append({"name": m.group(1).strip(), "repo": repo, "category": cat})
    return out


def main() -> int:
    items = parse(fetch(SRC))
    if not items:
        print("후보 0건 — README 구조가 바뀌었다(파서 점검 필요)", file=sys.stderr)
        return 2
    json.dump({"source": SRC, "count": len(items), "items": items},
              open("candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cats: dict[str, int] = {}
    for it in items:
        cats[it["category"]] = cats.get(it["category"], 0) + 1
    print(f"후보 {len(items)}건 / 카테고리 {len(cats)}개")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {n:2d}  {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
