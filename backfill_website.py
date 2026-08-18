#!/usr/bin/env python3
"""레지스트리 항목의 websiteUrl 소급 채움 (2026-08-19, 일회성).

`collect_candidates.py`가 이제 websiteUrl을 보존하지만, 이미 수집해 둔 산출물에는 없다.
표에 링크 없는 줄을 만들지 않으려고 그 항목만 소급해 채운다. 다음 수집부터는 불필요하다.
"""
import json
import time
import urllib.parse
import urllib.request

REG = "https://registry.modelcontextprotocol.io/v0/servers"
UA = "sallim-mcp-index/0.1 (+https://github.com/sallim-app)"


def lookup(name: str) -> str:
    q = urllib.parse.urlencode({"search": name.split("/")[-1], "limit": 50})
    try:
        req = urllib.request.Request(f"{REG}?{q}", headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.load(r)
    except Exception:
        return ""
    hit = ""
    for e in d.get("servers") or []:
        s = e.get("server") or {}
        if s.get("name") == name and s.get("websiteUrl"):
            hit = s["websiteUrl"]      # 뒤쪽(최신 버전)을 우선
    return hit


def main() -> int:
    path = "candidates_filtered.json"
    d = json.load(open(path, encoding="utf-8"))
    need = [i for i in d["items"]
            if not i.get("repo_url") and not i.get("website_url") and "registry" in (i.get("sources") or [])]
    print(f"소급 대상 {len(need)}건")
    got = 0
    for i in need:
        u = lookup(i["name"])
        if u:
            i["website_url"] = u
            got += 1
        time.sleep(0.4)
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"websiteUrl 확보 {got}건 / {len(need)}건")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
