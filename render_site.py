#!/usr/bin/env python3
"""측정값 → 정적 웹사이트 (2026-08-29).

**원장 하나, 출력 둘.** README(마크다운)와 이 사이트(HTML)는 같은 원자료의 함수다 —
`measured.json` · `classification.json` · `ranking.json` · `observed.py`. 파생 코드도
`render_readme.py`에서 그대로 가져다 쓴다(`clip`·`disp`·`dedupe_by_endpoint`·`q`).
README를 손으로 옮기지 않는다. 옮기면 두 문서가 갈라지고, 갈라지는 순간 어느 쪽이
사실인지 말할 수 없게 된다.

**왜 웹페이지인가**: 저장소 README는 검색엔진이 사실상 안 읽는다(★0 저장소).
"한국 MCP"를 검색하는 사람에게 이 측정값이 도달하려면 색인 경쟁에 들어가야 하고,
그러려면 ①서버가 내려주는 정적 HTML ②목록과 상세가 각자 URL ③sitemap·robots·
구조화데이터가 필요하다. 이 스크립트가 그 셋을 만든다.

**날짜(2026-08-21 `bbfaaa8`의 재발 방지)**: 이 파일은 *생성일*을 *측정일*로 쓰지 않는다.
- 가동 지표의 날짜 = `measured.json:measured_at`. 없으면 **멈춘다**(fail-closed).
- 패키지 축 = `repackaged_at`, 우리가 지는 축 = `axes_at`. 다르면 각각 따로 적는다.
- 채점(순위) 날짜는 `ranking.json`에 필드가 없다. 그래서 **지어내지 않고** 저장소
  이력에서 `grades/`가 마지막으로 바뀐 날을 읽어 "채점 원자료 최종 변경(저장소 이력)"
  이라고 그 정체를 밝혀 적는다. 이력을 못 읽으면 그 줄을 통째로 뺀다.
- 페이지 생성일은 측정일과 **다른 줄에** 적고, 각 측정값 옆에 며칠 지난 값인지 붙인다.

실행: python3 render_site.py [--base https://sallim.app/mcp-index] [--out site] [--ext .html]
"""
import argparse
import collections
import datetime as dt
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys

from observed import MISFILED, RENAMED, SCOPE
from render_readme import CAT_EN, CATS, OURS, clip, dedupe_by_endpoint, disp, q

REPO = "https://github.com/sallim-app/korea-mcp-index"


def e(x) -> str:
    """HTML 이스케이프. 남의 서버 이름·채점자 문장이 그대로 들어오는 자리라 예외 없이 통과시킨다."""
    return html.escape("" if x is None else str(x), quote=True)


def jsonld(obj) -> str:
    """`<script>` 안에 넣을 JSON. **남의 서버 이름·URL이 그대로 들어오는 자리다.**

    `json.dumps`는 `<`·`>`를 그대로 내보내므로, 값에 `</script>`가 섞이면 태그를 탈출해
    저장형 XSS가 된다(codex 교차검증 2026-08-29). 우리가 수집하는 이름·URL은 남의 저장소
    README에서 온 것이라 우리 손을 거치지 않는다 — 신뢰할 근거가 없다.
    JSON 문자열 안의 `\u003c` 는 같은 값으로 파싱되므로 구조화데이터는 그대로 읽힌다.
    """
    return (json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def slug(name: str) -> str:
    """서버 이름 → URL 조각. 충돌하면 그 자리에서 멈춘다(조용히 덮어쓰면 남의 페이지가 사라진다)."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "server"


def ago(day: str, today: dt.date) -> str:
    """며칠 지난 값인지. 이 목록의 값은 '지금 되느냐'라서 나이가 값의 일부다."""
    try:
        d0 = dt.date.fromisoformat(day)
    except (TypeError, ValueError):
        return ""
    n = (today - d0).days
    if n <= 0:
        return "오늘"
    if n == 1:
        return "하루 전"
    if n < 14:
        return f"{n}일 전"
    if n < 60:
        return f"{n}일 전 — 주간 회차를 한 번 이상 걸렀다"
    return f"{n}일 전 — <strong>오래된 값이다</strong>"


def graded_at() -> str | None:
    """채점 원자료가 마지막으로 바뀐 날 (저장소 이력). 못 읽으면 None — 오늘로 때우지 않는다."""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", "grades"],
                           capture_output=True, text=True, timeout=10, check=False)
        out = r.stdout.strip()
        return out if re.fullmatch(r"\d{4}-\d{2}-\d{2}", out) else None
    except (OSError, subprocess.SubprocessError):
        return None


# MCP 규격이 공개된 날. **이보다 먼저 배포된 패키지는 MCP 서버일 수 없다** — 우리 수집기가
# 이름이 같은 남의 패키지를 잘못 붙인 것이다. README는 이 축을 건수로만 실어서 이 오류가
# 안 보였는데, 서버별로 펴는 순간 **특정 남의 저장소에 대한 틀린 주장**이 된다.
# 2026-08-20에 우리는 정확히 반대 방향의 같은 사고를 냈다(못 읽은 패키지명 → '설치 불가').
# 그래서 지우지 않고 **의심스럽다고 적는다**(기치 ②: 못 봄 ≠ 없음, 그리고 오판도 공시한다).
MCP_BORN = "2024-11-25"


def pkg_suspect(rec: dict) -> str:
    """패키지 매칭이 의심스러운 이유. 없으면 빈 문자열."""
    p = rec.get("package") or {}
    lp = p.get("last_publish")
    if lp and lp < MCP_BORN:
        return (f"이 패키지의 최근 배포일({lp})이 MCP 규격 공개({MCP_BORN})보다 앞선다 — "
                f"이름이 같은 다른 패키지를 우리가 잘못 붙였을 가능성이 크다")
    return ""


CSS = """*,*::before,*::after{box-sizing:border-box}
:root{--bg:#fafaf7;--raised:#fff;--sunken:#f3f1ec;--ink1:#18181b;--ink2:#3f3f46;--ink3:#52525b;
--line:#ebe7df;--line2:#d4cfc4;--link:#0b6473;--ok:#047857;--warn:#854d0e;--bad:#b91c1c;
--font:-apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Noto Sans KR",
"Malgun Gothic",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink1);font-family:var(--font);
font-size:16px;line-height:1.7;word-break:keep-all;overflow-wrap:anywhere}
.wrap{max-width:56rem;margin:0 auto;padding:1.5rem 1.1rem 5rem}
a{color:var(--link)}
a:focus-visible,summary:focus-visible{outline:2px solid #0e8fa6;outline-offset:2px}
h1{font-size:1.85rem;line-height:1.35;margin:.6rem 0 .5rem;letter-spacing:-.01em}
h2{font-size:1.3rem;margin:2.6rem 0 .7rem;padding-top:.9rem;border-top:1px solid var(--line)}
h3{font-size:1.05rem;margin:1.6rem 0 .4rem}
p{margin:.7rem 0}
.lede{font-size:1.06rem;color:var(--ink2)}
.crumb{font-size:.82rem;color:var(--ink3);margin:0 0 .3rem}
.crumb a{color:var(--ink3)}
.meta{font-size:.85rem;color:var(--ink3)}
.card{background:var(--raised);border:1px solid var(--line);border-radius:12px;
padding:.9rem 1.1rem;margin:1rem 0}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0;border:1px solid var(--line);
border-radius:12px;background:var(--raised);
background-image:linear-gradient(to right,var(--raised),transparent 12px),
linear-gradient(to left,var(--raised),transparent 12px),
linear-gradient(to right,rgba(0,0,0,.10),transparent 10px),
linear-gradient(to left,rgba(0,0,0,.10),transparent 10px);
background-position:0 0,100% 0,0 0,100% 0;background-repeat:no-repeat;
background-size:26px 100%,26px 100%,10px 100%,10px 100%;
background-attachment:local,local,scroll,scroll}
.tw:focus-visible{outline:2px solid #0e8fa6;outline-offset:2px}
.tw::before{content:"← 좌우로 넘겨서 보세요";display:none;font-size:.78rem;color:var(--ink3);
padding:.4rem .7rem 0}
@media (max-width:640px){.tw::before{display:block}}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--sunken);font-weight:600;white-space:nowrap;font-size:.84rem;color:var(--ink2)}
tbody tr:last-child td{border-bottom:0}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
code,.mono{font-family:var(--mono);font-size:.86em;background:var(--sunken);
padding:.1rem .3rem;border-radius:4px}
blockquote{margin:1rem 0;padding:.1rem 0 .1rem 1rem;border-left:3px solid var(--line2);
color:var(--ink2)}
ul,ol{padding-left:1.3rem}
li{margin:.35rem 0}
small,.sub{font-size:.82rem;color:var(--ink3);line-height:1.55}
.tag{display:inline-block;font-size:.75rem;padding:.1rem .45rem;border-radius:999px;
border:1px solid var(--line2);color:var(--ink3);background:var(--raised);white-space:nowrap}
.tag.ours{border-color:#0e8fa6;color:#0b6473;background:rgba(14,143,166,.10)}
.tag.ok{border-color:#047857;color:var(--ok);background:rgba(4,120,87,.10)}
.tag.bad{border-color:#b91c1c;color:var(--bad);background:rgba(185,28,28,.10)}
.tag.warn{border-color:#a16207;color:var(--warn);background:rgba(161,98,7,.12)}
details{margin:1rem 0;border:1px solid var(--line);border-radius:12px;background:var(--raised);
padding:.2rem .9rem}
summary{cursor:pointer;padding:.6rem 0;font-weight:600;font-size:.93rem}
.kv{display:grid;grid-template-columns:9.5rem 1fr;gap:.35rem .9rem;font-size:.92rem;margin:.8rem 0}
.kv dt{color:var(--ink3);font-size:.85rem;padding-top:.1rem}
.kv dd{margin:0}
.nav{display:flex;flex-wrap:wrap;gap:.4rem .9rem;font-size:.9rem;margin:1.2rem 0 0;
padding:.8rem 0 0;border-top:1px solid var(--line)}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.84rem;
color:var(--ink3)}
@media (max-width:640px){.wrap{padding:1rem .8rem 4rem}h1{font-size:1.5rem}
.kv{grid-template-columns:1fr;gap:.05rem .5rem}.kv dd{margin-bottom:.5rem}}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#141413;--raised:#1c1c1a;
--sunken:#232320;--ink1:#f0efea;--ink2:#c9c6bf;--ink3:#a09d95;--line:#2e2e2a;--line2:#43423d;
--link:#5fc7da;--ok:#4ade80;--warn:#e3b341;--bad:#f87171}}
"""


class Page:
    """한 페이지. 본문은 서버가 그대로 내려준다 — 클라이언트 JS가 그리는 부분은 없다."""

    def __init__(self, site, name, title, desc, crumbs=(), jsonld=None,
                 changefreq="weekly", priority="0.5"):
        self.site, self.name, self.title, self.desc = site, name, title, desc
        self.crumbs, self.jsonld = list(crumbs), jsonld
        self.changefreq, self.priority = changefreq, priority
        self.body: list[str] = []
        site.pages.append(self)
        if name in site.by_name:
            raise SystemExit(f"생성 중단 — 페이지 이름 충돌: {name}")
        site.by_name[name] = self

    def w(self, *lines):
        self.body.extend(lines)

    @property
    def url(self):
        return self.site.url_of(self.name)

    def render(self) -> str:
        s = self.site
        ld = [self.jsonld] if self.jsonld else []
        if self.crumbs:
            ld.append({
                "@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": n,
                     "item": s.url_of(p)} for i, (n, p) in enumerate(self.crumbs)],
            })
        o = ['<!doctype html>', '<html lang="ko">', '<head>', '<meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             f'<title>{e(self.title)}</title>',
             f'<meta name="description" content="{e(self.desc)}">',
             f'<link rel="canonical" href="{e(self.url)}">',
             '<meta name="robots" content="index,follow,max-snippet:-1">',
             '<meta property="og:type" content="website">',
             f'<meta property="og:title" content="{e(self.title)}">',
             f'<meta property="og:description" content="{e(self.desc)}">',
             f'<meta property="og:url" content="{e(self.url)}">',
             '<meta property="og:site_name" content="한국 데이터 MCP 실측 목록">',
             '<meta property="og:locale" content="ko_KR">',
             '<meta name="twitter:card" content="summary">',
             '<meta name="author" content="sallim">',
             f'<link rel="alternate" type="text/plain" href="{e(s.url_of("llms.txt"))}">',
             f'<style>{CSS}</style>']
        for j in ld:
            o.append('<script type="application/ld+json">' + jsonld(j) + '</script>')
        o += ['</head>', '<body>', '<div class="wrap">']
        if self.crumbs:
            o.append('<nav class="crumb">'
                     + ' › '.join(f'<a href="{e(s.url_of(p))}">{e(n)}</a>' for n, p in self.crumbs)
                     + '</nav>')
        o += self.body
        o += ['<footer>',
              f'<p>측정값과 원자료 전부 공개 — <a href="{REPO}">저장소</a> · '
              f'<a href="{REPO}/blob/main/measured.json">measured.json</a> · '
              f'<a href="{REPO}/blob/main/axes.csv">axes.csv</a> · '
              f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a></p>',
              f'<p>{s.date_footer}</p>',
              '<p>코드·문서·우리가 만든 측정값은 MIT. <strong>응답 발췌</strong>는 각 서버 '
              '운영자의 것이고 측정 근거로 인용했을 뿐이다 — 내려 달라고 하면 내린다.</p>',
              f'<p><strong>등재 자체에 대한 이의도 같은 창구로 받는다</strong>'
              f'(<a href="{REPO}/issues">이슈</a>). 값이 틀렸으면 고치고, 우리가 잘못 짚은 '
              f'것이면 뺀다. 다만 “고쳤으니 등수를 올려 달라”는 다음 채점 회차에 전원 '
              f'동시에만 반영한다 — 우리도 예외가 아니다.</p>',
              '</footer>', '</div>', '</body>', '</html>']
        return "\n".join(o) + "\n"


class Site:
    """이름 하나로 출력 파일과 URL을 동시에 정한다 — 둘이 갈라지면 canonical이 거짓이 된다."""

    def __init__(self, base, out, ext):
        self.base = base.rstrip("/")
        self.out = pathlib.Path(out)
        self.ext = ext
        self.pages: list[Page] = []
        self.by_name: dict[str, Page] = {}
        self.extra: list[tuple[str, str]] = []   # (파일명, 내용) — sitemap·robots·llms.txt
        self.date_footer = ""

    def rel(self, name):
        if name == "index":
            return "index.html"
        return name if "." in name.rsplit("/", 1)[-1] else name + (self.ext or ".html")

    def url_of(self, name):
        if name == "index":
            return f"{self.base}/"
        tail = name if "." in name.rsplit("/", 1)[-1] else name + self.ext
        return f"{self.base}/{tail}"

    def write(self):
        # **재귀 삭제 앞에 자물쇠를 건다**(codex 교차검증 2026-08-29). 종전엔 `--out`을 그대로
        # rmtree했다 — 크론·배포 설정에서 `--out .` 한 번이면 저장소가 통째로 사라진다.
        # 지울 수 있는 것은 "우리가 만든 산출물 디렉토리"뿐이고, 그 증거는 우리가 남긴
        # 표식 파일이다. 없으면 지우지 않고 **멈춘다**(fail-closed).
        out = self.out.resolve()
        stamp = out / ".rendered-by-render_site"
        if out.exists():
            if out == pathlib.Path.cwd().resolve() or out.parent == out:
                raise SystemExit(f"생성 중단 — --out 이 작업 디렉토리나 루트다: {out}")
            if not stamp.exists():
                raise SystemExit(
                    f"생성 중단 — {out} 는 이 스크립트가 만든 디렉토리가 아니다"
                    f"(표식 {stamp.name} 없음). 지우지 않는다 — 직접 비우고 다시 실행하라.")
            shutil.rmtree(out)
        self.out = out
        for pg in self.pages:
            f = self.out / self.rel(pg.name)
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(pg.render(), encoding="utf-8")
        for fname, text in self.extra:
            f = self.out / fname
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text("render_site.py 산출물. 이 파일이 있어야 다음 회차가 이 디렉토리를 "
                         "지우고 다시 쓴다.\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# 조각들 — 모두 원자료의 함수다. 여기서 새 사실을 만들지 않는다.
# ─────────────────────────────────────────────────────────────────────────────

def name_link(ctx, rec, ours_tag=True) -> str:
    """서버 이름 → 상세 페이지 링크. 상세가 없으면 저장소로 나간다(막다른 이름을 안 만든다)."""
    nm = e(disp(rec["name"]))
    pg = ctx["page_of"].get(rec["name"])
    if pg:
        inner = f'<a href="{e(ctx["site"].url_of(pg))}">{nm}</a>'
    else:
        u = rec.get("repo_url") or rec.get("website_url")
        inner = f'<a href="{e(u)}" rel="noopener">{nm}</a>' if u else nm
    if ours_tag and rec["name"].startswith(OURS):
        inner += ' <span class="tag ours" title="이 목록의 운영자가 만든 서버">운영자</span>'
    return inner


def measure_row(ctx, rec) -> str:
    rm = rec.get("remote") or {}
    warm, cold = rm.get("warm_ms"), rm.get("cold_ms")
    slow = cold and warm and cold > warm * 3
    pd = rec.get("paid_disclosure") or {}
    bits = []
    if pd.get("disclosed"):
        bits.append(f'<div class="sub">무료 {e(pd.get("free"))}/{e(pd.get("total"))}종 '
                    f'(스스로 공시)</div>')
    if SCOPE.get(rec["name"]):
        bits.append(f'<div class="sub">{e(SCOPE[rec["name"]])}</div>')
    if RENAMED.get(rec["name"]):
        bits.append(f'<div class="sub">저장소가 <code>{e(RENAMED[rec["name"]])}</code> → '
                    f'<code>{e(rec["name"])}</code>로 옮겨졌다 — 주소가 같아 같은 서버로 이었고, '
                    f'등수는 옛 이름으로 받은 것이다</div>')
    err = ctx["err_of"].get(rec["name"])
    return ("<tr><td>" + name_link(ctx, rec) + "".join(bits) + "</td>"
            f'<td class="n">{e(rm.get("tool_count") or "—")}</td>'
            f'<td class="n">{e(warm or "—")}</td>'
            f'<td class="n">{("<strong>" + e(cold) + "</strong>") if slow else e(cold or "—")}</td>'
            f'<td class="n">{e(q(rec, "described_pct"))}%</td>'
            f'<td class="n">{e(q(rec, "annotated_pct"))}%</td>'
            f'<td class="n">{e(err if err is not None else "—")}</td></tr>')


def measure_table(ctx, rows) -> list[str]:
    return (['<div class="tw" tabindex="0" role="region" aria-label="측정값 표"><table>',
             '<thead><tr><th>서버</th><th>도구</th><th>웜 ms</th><th>콜드 ms</th>'
             '<th>설명</th><th>주석</th><th>사실오류</th></tr></thead><tbody>']
            + [measure_row(ctx, r) for r in rows]
            + ['</tbody></table></div>'])


def legend(ctx) -> list[str]:
    return ['<h2 id="표기">표기</h2>', '<ul>',
            '<li><strong>도구</strong> — <code>tools/list</code>에 실제로 들어 있는 개수. '
            '0이면 껍데기다</li>',
            '<li><strong>웜 / 콜드</strong> — 연달아 부를 때 / 첫 호출(ms). 서버리스는 첫 호출에 '
            '기동 시간이 붙는다. 콜드가 웜의 3배를 넘으면 굵게 표시한다</li>',
            '<li><strong>설명 / 주석</strong> — 도구에 설명이 붙은 비율 / '
            '<code>readOnlyHint</code> 같은 주석이 붙은 비율. <strong>둘 다 없으면 모델이 그 도구를 '
            '언제 어떻게 쓸지 모른다</strong> — 데이터가 정확해도 답에 도달하지 못한다</li>',
            '<li><strong>사실오류</strong> — 그 서버로 답한 내용 중 채점자가 <strong>실제와 다르다고 '
            '확인한</strong> 건수. 서버가 틀린 값을 준 경우와 모델이 옮겨 적다 틀린 경우가 섞여 있고, '
            f'어느 쪽인지는 <a href="{REPO}/tree/main/grades">grades/</a>에 문장째 적혀 있다. '
            '<code>—</code>는 채점하지 않았다는 뜻이다</li>',
            '<li>이름 옆 <span class="tag">무료 N/M</span> — 서버가 유료 게이트를 '
            '<strong>스스로 공시</strong>할 때만 붙는다. 없다고 무료라는 뜻이 아니다 — '
            '밖에서는 판정할 수 없다</li>',
            '<li><span class="tag ours">운영자</span> — 이 목록을 만든 곳이 운영하는 서버. '
            '<strong>이 목록의 축을 고른 것도 같은 운영자다</strong> — 축과 그 개정 이력은 '
            f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a>에 있다</li>', '</ul>']


# 여러 서버가 함께 쓰는 공용 게이트웨이. 여기서 나온 오류는 그 주소를 등록한 개인·팀의
# 결함이 아닐 수 있다 — 401은 게이트웨이의 것이지 그 저장소의 것이 아니다.
SHARED_GATEWAYS = ("playmcp.kakao.com", "server.smithery.ai", "glama.ai", "mcp.so",
                   "mcp.pipedream.net")


def gateway_of(rec: dict) -> str:
    url = ((rec.get("remote") or {}).get("url") or "")
    return next((g for g in SHARED_GATEWAYS if g in url), "")


def client_limits(ctx, heading=True) -> list[str]:
    """**우리 두드리개가 못 하는 것**을 남의 결함 옆에 같이 적는다.

    fresh-eyes 검수(2026-08-29)가 잡은 자리다. `tools/list`에 200이 안 온 28건 중 22건은
    HTTP 상태코드를 돌려줬다 — 서버는 살아 있었고 우리 부르는 방식이 안 맞았을 수 있다.
    그 가능성을 안 적으면 "응답 없음"은 관측이 아니라 남의 제품에 대한 판정이 된다.
    코드로 확인한 한계만 적는다(추정 금지).
    """
    o = ["<h2 id=\"한계\">우리 두드리개가 못 하는 것</h2>"] if heading else []
    o += ['<div class="card">',
          '<p><strong>“응답 없음”은 그 서버의 판정이 아니라 <em>우리 호출의 결과</em>다.</strong> '
          '우리 클라이언트는 아래를 못 한다 — 코드로 확인한 것만 적는다. 이 중 하나에 걸린 '
          '서버는 <strong>살아 있는데 우리 명단에 올라 있을 수 있다.</strong></p>',
          '<ul>',
          '<li><strong><code>initialize</code> 핸드셰이크를 하지 않는다.</strong> 세션을 열지 '
          '않고 <code>tools/list</code>를 바로 보낸다 — Streamable HTTP 규격을 지키는 서버가 '
          '여기에 <strong>HTTP 400을 주는 것은 정상 동작</strong>이다</li>',
          '<li><strong>POST + 307 리다이렉트를 따라가지 않는다.</strong> 파이썬 표준 '
          'urllib이 POST에서 안 따라간다 — 서버는 옮긴 자리를 알려준 것이다</li>',
          '<li><strong>SSE(GET)를 시도하지 않는다.</strong> POST 고정이라 SSE 엔드포인트는 '
          '<strong>405를 주는 것이 맞다</strong></li>',
          '<li><strong>4xx는 재시도하지 않는다.</strong> 재시도는 연결 실패·5xx일 때만이라, '
          '아래 명단의 상당수는 <strong>단 한 번 부른 결과</strong>다</li>',
          '<li><strong>서버가 보낸 오류 본문을 저장하지 않는다.</strong> 그쪽 해명을 '
          '버리고 상태코드만 남겼다</li>',
          '</ul>',
          '<p class="sub">고칠 것은 이 목록이 아니라 우리 두드리개다 — 다음 회차 과제로 '
          '올려 두었다. 그 전까지 아래 숫자는 <strong>이 한계를 포함한 값</strong>으로 '
          '읽어야 한다.</p>',
          '</div>']
    return o


def dead_breakdown(ctx) -> list[str]:
    """무응답 명단의 정체를 숫자로 편다 — 22건이 상태코드를 돌려줬다는 사실을 숨기지 않는다."""
    dead = ctx["dead"]
    codes = collections.Counter(r["remote"].get("http") for r in dead)
    answered = sum(v for k, v in codes.items() if k)
    silent = codes.get(None, 0)
    reg = [r for r in dead if r.get("addr_registered")]
    bits = " · ".join(f"HTTP {k} {v}건" for k, v in sorted(codes.items(), key=lambda x: -x[1])
                      if k)
    return ['<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><tbody>',
            f'<tr><td>상태코드를 돌려준 것</td><td class="n"><strong>{answered}건</strong> '
            f'<span class="sub">{bits}</span></td></tr>',
            f'<tr><td>정말 아무 응답이 없던 것</td><td class="n">{silent}건 '
            f'<span class="sub">연결 실패·타임아웃</span></td></tr>',
            f'<tr><td>관리자가 레지스트리에 <strong>등록한</strong> 주소</td>'
            f'<td class="n">{len(reg)}건</td></tr>',
            f'<tr><td>우리가 README에서 <strong>추정한</strong> 주소</td>'
            f'<td class="n">{len(dead) - len(reg)}건 <span class="sub">우리가 주소를 잘못 '
            f'짚었을 수 있다</span></td></tr>',
            '</tbody></table></div>']


def loses_section(ctx) -> list[str]:
    """우리가 지는 항목. 위치가 규약이다 — 순위 바로 밑, 한계 절로 미루지 않는다."""
    items = ctx["items"]
    sh = collections.Counter((r.get("self_hosting") or {}).get("state") for r in items)
    lic = collections.Counter((r.get("open_source") or {}).get("license") for r in items)
    paid = [r for r in items if (r.get("paid_disclosure") or {}).get("disclosed")]
    ours_paid = [r for r in paid if r["name"].startswith(OURS)]
    lic_named = " · ".join(f"{e(k)} {v}건" for k, v in lic.most_common() if k)
    o = ['<h2 id="지는-항목">우리가 지는 항목</h2>',
         '<p><strong>유리한 축만 재면 그 순위는 판정이 아니라 광고지다.</strong> 원격 MCP인 우리가 '
         '불리한 축을 같이 잰다 — 무엇을 잴지는 결과를 보기 전에 '
         f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a>에 고정했고, 여기서 뺄 수 없게 '
         '회귀 테스트로 묶어 두었다.</p>',
         '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>축</th><th>이 목록 전체</th>'
         '<th>운영자(살림)</th></tr></thead><tbody>',
         f'<tr><td>셀프호스팅</td><td>배포판 확인 {sh["packaged"]}건 · 소스만 '
         f'{sh["source_only"]}건 · 미확인 {sh["unknown"]}건</td>'
         '<td><strong>소스만</strong> — 그리고 클론해도 답이 안 나온다</td></tr>',
         f'<tr><td>오픈소스</td><td>{lic_named} · 라이선스 확인 못 함 {lic[None]}건</td>'
         '<td>MIT — <strong>이 축에서는 우리가 지지 않는다</strong></td></tr>',
         f'<tr><td>무료 한도</td><td>스스로 공시한 서버 {len(paid)}건</td><td>'
         + (f'그 {len(paid)}건이 우리다 — 도구 {e(ours_paid[0]["paid_disclosure"]["total"])}종 중 '
            f'<strong>{e(ours_paid[0]["paid_disclosure"]["paid"])}종 유료</strong>'
            if ours_paid else '—')
         + '</td></tr>', '</tbody></table></div>', '<ul>',
         '<li><strong>셀프호스팅은 우리가 제일 나쁘다.</strong> 우리 저장소는 MIT로 열려 있지만 '
         '도구들이 우리 비공개 데이터 API를 부르므로 '
         '<a href="https://github.com/sallim-app/korea-realty" rel="noopener">클론해서 띄우면 '
         '거의 다 실패한다</a> — 우리 README가 먼저 적어 둔 것이고, 여기서도 적는다. '
         '축의 값(<code>소스만</code>)보다 실질이 나쁘다</li>',
         '<li><strong><code>소스만</code>은 “띄우면 같은 답이 나온다”가 아니다.</strong> 코드가 '
         '공개돼 있다는 뜻일 뿐이고, 남의 서버도 우리처럼 자기 데이터에 묶여 있을 수 있다 — '
         '그건 우리가 재지 않았다</li>',
         '<li><strong><code>라이선스 확인 못 함</code>을 “오픈소스 아님”으로 읽지 말라.</strong> '
         '저장소가 비공개거나 지워졌거나 이름이 바뀐 것도 여기 들어온다. 다만 <strong>공개 '
         '저장소인데 라이선스 파일이 없는 것</strong>은 기본값이 저작권 전부 유보라 실제로 '
         '가져다 쓸 수 없다</li>',
         f'<li><strong>유료 공시가 {len(paid)}건뿐인 것은 나머지가 무료라는 뜻이 아니다.</strong> '
         '밖에서는 판정할 수 없다. 밝힌 쪽만 표에 유료 게이트가 보이고, 지금 그 쪽은 우리다</li>',
         '</ul>',
         '<p>축이 모자란다고 보면 다른 가중치로 직접 재계산할 수 있다 — '
         f'<a href="{REPO}/blob/main/axes.csv">axes.csv</a>가 서버 1행 × 축 1열이고, '
         f'<code>python3 recompute.py --weights tool_count=1,warm_ms=-0.01</code>이 그 계산기다. '
         '<strong>그 결과는 우리 순위가 아니다</strong> — 지표로 줄 세우는 방식은 우리가 실측으로 '
         f'폐기했다(<a href="{REPO}/blob/main/JUDGING.md">JUDGING.md</a>).</p>']
    return o


def cat_block(ctx, c, full=True) -> list[str]:
    """분야 하나. 목록 페이지와 분야 페이지가 **같은 함수**를 쓴다 — 둘이 어긋날 수 없다."""
    live, cls, rank_of = ctx["live"], ctx["cls"], ctx["rank_of"]
    group = [r for r in live if cls.get(r["name"], {}).get("category") == c]
    mis = [r for r in group if r["name"] in MISFILED]
    group = [r for r in group if r not in mis]
    judged = sorted([r for r in group if r["name"] in rank_of],
                    key=lambda r: rank_of[r["name"]][0])
    rest = sorted([r for r in group if r["name"] not in rank_of],
                  key=lambda r: -(r["remote"].get("tool_count") or 0))
    o: list[str] = []
    if not judged:
        _n = len(group)
        o.append(f'<p>후보가 {_n}건뿐이라 순위를 매기지 않았다. '
                 + ('이 분야에서 응답한 서버가 하나라 비교할 상대가 없다.</p>'
                    if _n == 1 else
                    f'{_n}개 중 {_n}개를 고르는 것은 순위가 아니라 목록이다.</p>'))
    else:
        if len(group) <= 3:
            o.append(f'<p class="sub">이 분야는 후보가 {len(group)}건뿐이라 '
                     f'<strong>고른 것이 아니라 줄 세운 것</strong>이다.</p>')
        if ctx["cat_note"].get(c):
            o.append(f'<blockquote>{e(clip(ctx["cat_note"][c], 260))}</blockquote>')
        if mis:
            o.append(f'<p class="sub">위 총평의 서버 수는 <strong>분야 교정 전</strong> 기준이다 — '
                     f'이 분야에서 {len(mis)}건이 아래 「분야 교정」으로 빠졌다.</p>')
    o += measure_table(ctx, judged or rest[:3])
    if judged:
        o.append("<ol>")
        for r in judged:
            rank, why = rank_of[r["name"]]
            o.append(f'<li value="{rank}"><strong>{e(disp(r["name"]))}</strong> — '
                     f'{e(clip(why, 300 if full else 160))}</li>')
        o.append("</ol>")
        here = {r["name"] for r in judged} | {r["name"] for r in mis}
        here |= {RENAMED[n] for n in here if n in RENAMED}
        gone = [(rk_, n) for rk_, n in sorted(set(ctx["graded_of"].get(c, [])))
                if n not in here]
        if gone:
            bits = []
            for rk_, n in gone:
                why_gone = ("이번 주 응답 없음" if n in ctx["dead_names"]
                            else "이번 주 후보에서 빠졌다")
                bits.append(f"{rk_}위 {e(disp(n))}({why_gone})")
            o.append('<p class="sub"><strong>빠진 등수</strong> — 지난 채점 회차의 '
                     + " · ".join(bits)
                     + '. 순위는 매월 1일에만 다시 매기므로 그때까지 번호는 그대로 둔다 — '
                       '빈자리를 위로 당기면 재채점 없이 등수가 오른 것처럼 보인다.</p>')
        n = ctx["cat_runs"].get(c, 1)
        runs = (f"서버당 <strong>{n}회</strong> 물어 재현성까지 채점했다." if n >= 2 else
                "이 회차는 서버당 <strong>1회</strong>만 물었다 — <strong>재현성은 재지 "
                "않았다</strong>(다시 물으면 등수가 갈릴 수 있다). 다음 채점 회차부터 3회로 잰다.")
        o.append('<p class="sub">순위는 <strong>실제로 물어본 결과</strong>다 — 같은 질문을 각 '
                 f'서버에 던지고 답변을 채점했다. {runs} 질문·호출기록·답변은 '
                 f'<a href="{REPO}/tree/main/answers">answers/</a>에, 채점은 '
                 f'<a href="{REPO}/tree/main/grades">grades/</a>에, 기준은 '
                 f'<a href="{REPO}/blob/main/JUDGING.md">JUDGING.md</a>에 있다.</p>')
    if judged and rest:
        o.append(f'<details><summary>채점하지 않은 {len(rest)}건</summary>')
        o += measure_table(ctx, rest)
        o.append('</details>')
    if mis:
        o.append(f'<p><strong>분야 교정 {len(mis)}건</strong> — 이 분야 검색어에 걸려 수집됐지만 '
                 '<strong>불러 보니 다른 것을 하는</strong> 서버다. 남의 분야 질문으로 매긴 등수는 '
                 '그 서버를 잰 값이 아니라서 순위에서 뺐다. 지우지는 않는다 — 찾는 사람이 있다.</p>')
        o.append('<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>서버</th><th>실제 분야</th>'
                 '<th>채점자가 확인한 것</th></tr></thead><tbody>')
        for r in sorted(mis, key=lambda x: x["name"]):
            _, now, why = MISFILED[r["name"]]
            tail = "…" if not why.rstrip().endswith("다.") else ""
            o.append(f'<tr><td>{name_link(ctx, r)}</td><td>{e(now)}</td>'
                     f'<td>“{e(why.rstrip())}{tail}”</td></tr>')
        o.append('</tbody></table></div>')
    return o


def server_page(ctx, rec) -> None:
    """서버 하나 = URL 하나. 앵커가 아니라 진짜 주소여야 검색에서 그 서버 이름으로 잡힌다."""
    site, cls = ctx["site"], ctx["cls"]
    name = rec["name"]
    nm = disp(name)
    # **분야 교정된 서버는 실제 분야로 적는다**(codex 교차검증 2026-08-29). 종전엔 수집기가
    # 잘못 넣은 분야를 제목·breadcrumb·설명·구조화데이터에 그대로 썼다 — 순위에서는 뺐다고
    # 써 놓고 정체는 틀린 채로 게시한 셈이라, 그 서버를 찾는 사람을 계속 잘못 보낸다.
    misfiled = MISFILED.get(name)
    cat = misfiled[1] if misfiled else (cls.get(name) or {}).get("category")
    rm = rec.get("remote") or {}
    ours = name.startswith(OURS)
    reachable = bool(rm.get("reachable"))
    tools = rm.get("tool_count") or 0
    ts = ctx["ts"]

    if reachable and tools:
        state = f"{ts} 측정에서 응답했고 도구 {tools}종을 공개한다"
    elif reachable:
        state = f"{ts} 측정에서 응답은 했지만 도구 목록을 얻지 못했다"
    elif rm:
        state = (f"{ts} 측정에서 우리가 부른 주소가 "
                 + (f"HTTP {rm.get('http')}를 돌려줬다(도구 목록은 못 받았다)"
                    if rm.get("http") else "응답하지 않았다"))
    else:
        state = "원격 주소가 없어 가동을 재지 못했다"
    caveat = ""
    if rm and not reachable:
        caveat = (" 이것은 그 서버의 판정이 아니라 우리 호출의 결과다 — "
                  + ("우리가 README에서 추정한 주소이고, " if not rec.get("addr_registered")
                     else "")
                  + "우리 클라이언트는 initialize 핸드셰이크·307 추적·SSE를 못 한다.")
    if gateway_of(rec):
        caveat += (f" 이 주소는 여러 서버가 함께 쓰는 공용 게이트웨이"
                   f"({gateway_of(rec)})다.")
    desc = f"{nm} — {cat or '분야 미상'} MCP 서버. {state}.{caveat} 측정값·근거 전부 공개."

    pg = Page(site, ctx["page_of"][name], f"{nm} — 한국 데이터 MCP 실측", desc,
              crumbs=[("한국 데이터 MCP 실측 목록", "index")]
              + ([(cat, ctx["cat_page"][cat])] if cat in ctx["cat_page"] else [])
              + [(nm, ctx["page_of"][name])],
              jsonld={"@context": "https://schema.org", "@type": "SoftwareApplication",
                      "name": name, "applicationCategory": "DeveloperApplication",
                      "description": desc,
                      **({"url": rec["repo_url"]} if rec.get("repo_url") else {}),
                      **({"softwareVersion": (rec.get("package") or {}).get("version")}
                         if (rec.get("package") or {}).get("version") else {})},
              priority="0.6")
    W = pg.w
    W(f'<h1>{e(nm)}</h1>')
    if nm != name:
        W(f'<p class="sub">정본 이름 <code>{e(name)}</code> '
          f'<span class="sub">(기계용 <a href="{e(site.url_of("index.json"))}">index.json</a>· '
          f'<a href="{e(site.url_of("llms.txt"))}">llms.txt</a>가 쓰는 키다 — 표에 짧게 적은 '
          f'이름과 같은 서버다)</span></p>')
    tags = [f'<span class="tag">{e(cat)}</span>'] if cat else []
    tags.append('<span class="tag ok">응답함</span>' if reachable
                else ('<span class="tag bad">응답 없음</span>' if rm
                      else '<span class="tag">가동 미측정</span>'))
    if ours:
        tags.append('<span class="tag ours">이 목록의 운영자가 만든 서버</span>')
    W('<p>' + " ".join(tags) + '</p>')
    W(f'<p class="lede">{e(state)}. 이 페이지의 값은 <strong>그 순간의 기록</strong>이고, '
      f'판정이 아니라 관측이다.</p>')
    if gateway_of(rec):
        W(f'<div class="card"><p><strong>우리가 부른 주소는 여러 서버가 함께 쓰는 공용 '
          f'게이트웨이({e(gateway_of(rec))})다.</strong> 여기서 나온 오류는 게이트웨이의 '
          f'것이지 이 저장소의 결함이 아닐 수 있다 — 우리가 그 둘을 갈라 재지 못했다.</p>'
          f'</div>')
    if rm and not reachable:
        pg.w(*client_limits(ctx, heading=False))
    if ours:
        W('<div class="card"><p><strong>이해충돌 공시.</strong> 이 서버는 이 목록을 만든 곳이 '
          '운영한다. 무엇을 잴지 고른 것도 우리다 — 원자료를 다 공개해도 그 편향은 안 없어진다. '
          f'무엇을 재기로 했는지는 결과를 보기 전에 <a href="{REPO}/blob/main/PROTOCOL.md">신뢰 '
          '규약</a>에 고정해 두었다.</p></div>')

    # ── 측정값 ──
    W('<h2>측정값</h2>')
    kv = [("측정일", f'{e(ts)} <span class="sub">({ctx["ts_ago"]})</span>')]
    if rm:
        kv.append(("우리가 부른 주소", f'<code>{e(rm.get("url") or "—")}</code>'))
        kv.append(("주소 출처", "관리자가 공식 레지스트리에 등록한 주소"
                   if rec.get("addr_registered")
                   else "우리가 README에서 뽑은 <strong>추정</strong> 주소 — 우리가 잘못 짚었을 수 있다"))
        kv.append(("HTTP", e(rm.get("http") or "—")))
    if reachable and tools:
        kv += [("도구 수", f"{tools}종"),
               ("웜 응답", f'{e(rm.get("warm_ms"))} ms <span class="sub">(연달아 부를 때)</span>'),
               ("콜드 응답", f'{e(rm.get("cold_ms"))} ms <span class="sub">(첫 호출 1회 — '
                            f'그 순간 자고 있었을 수 있다)</span>'),
               ("설명 붙은 도구", f'{e(q(rec, "described_pct"))}%'),
               ("주석 붙은 도구", f'{e(q(rec, "annotated_pct"))}% '
                                f'<span class="sub">(readOnlyHint 등)</span>'),
               ("입력 스키마", f'{e(q(rec, "input_schema_pct"))}%'),
               ("출력 스키마", f'{e(q(rec, "output_schema_pct"))}%')]
    elif rm:
        kv.append(("증상", e(clip(rm.get("why") or f'HTTP {rm.get("http")}', 200))))
    pd = rec.get("paid_disclosure") or {}
    if pd.get("disclosed"):
        kv.append(("유료 게이트 공시", f'도구 {e(pd.get("total"))}종 중 무료 {e(pd.get("free"))}종 '
                                    f'· 유료 {e(pd.get("paid"))}종 <span class="sub">(서버가 '
                                    f'스스로 공시)</span>'))
    W('<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in kv) + '</dl>')
    if SCOPE.get(name):
        W(f'<div class="card"><p><strong>불러 보고 알게 된 성질</strong> — {e(SCOPE[name])}. '
          f'몰라서 헛짚는 자리라 값 옆에 적는다.</p></div>')

    # ── 순위·채점 ──
    rk = ctx["rank_of"].get(name)
    if rk and misfiled:
        # 무효로 본 등수를 「순위와 채점」으로 내면 한 페이지가 서로 모순된 판정을 게시한다.
        # 아래 「분야 교정」 절에서 그 등수의 정체와 함께 적는다.
        rk = None
    if rk:
        rank, why = rk
        err = ctx["err_of"].get(name)
        W('<h2>순위와 채점</h2>')
        W(f'<p>{e(cat)} 분야 <strong>{rank}위</strong>'
          + (f' · 채점자가 실제와 다르다고 확인한 사실오류 <strong>{err}건</strong>'
             if err is not None else "")
          + (f' <span class="sub">(채점 원자료 최종 변경 {e(ctx["graded"])})</span>'
             if ctx["graded"] else "") + '</p>')
        # **가동은 매주, 순위는 매월** — 두 값의 회차가 다르다. 이번 회차에 응답하지 않은
        # 서버에 지난 회차 등수만 크게 적어 두면, 그 등수가 지금 판정처럼 읽힌다(codex
        # 교차검증 지적 2026-08-29). 등수는 지우지 않고 회차를 밝힌다.
        if not (reachable and tools):
            W('<div class="card"><p><strong>이 등수는 지난 채점 회차의 것이다.</strong> '
              f'{e(ts)} 가동 측정에서 '
              + ("응답하지 않아" if not reachable else "비교할 값을 얻지 못해")
              + ' 이번 회차 순위표에는 서 있지 않다. 그래도 번호를 지우지 않는 이유는, '
              '빈자리를 위로 당기면 재채점 없이 등수가 오른 것처럼 보이기 때문이다.</p></div>')
        if RENAMED.get(name):
            W(f'<p class="sub"><strong>이 등수는 옛 이름 <code>{e(RENAMED[name])}</code>으로 '
              f'받은 것이다.</strong> 저장소가 <code>{e(name)}</code>로 옮겨졌고 엔드포인트가 '
              f'같아 같은 서버로 이었다 — 채점 원자료(<a href="{REPO}/tree/main/grades">grades/'
              f'</a>)에는 옛 이름으로만 적혀 있다.</p>')
        W(f'<blockquote>{e(why)}</blockquote>')
        runs = ctx["cat_runs"].get(cat, 1)
        W('<p class="sub">순위는 지표 가중합이 아니라 <strong>실제로 물어본 답변을 채점한 '
          '결과</strong>다. '
          + (f'서버당 {runs}회 물었다.' if runs >= 2 else
             '이 회차는 서버당 1회만 물었다 — <strong>재현성은 재지 않았다</strong>. '
             '다시 물으면 등수가 갈릴 수 있다.')
          + f' 질문·호출기록·답변은 <a href="{REPO}/tree/main/answers">answers/</a>, 채점 전문은 '
            f'<a href="{REPO}/tree/main/grades">grades/</a>에 있다.</p>')
    if misfiled:
        collected, real, why = misfiled
        tail = "…" if not why.rstrip().endswith("다.") else ""
        old_rank = ctx["rank_of"].get(name)
        W('<h2>분야 교정</h2>',
          f'<p>이 서버는 <strong>{e(real)}</strong>이다. 우리 수집기가 '
          f'<strong>{e(collected)}</strong> 검색어로 잡아 그 분야 질문으로 채점했는데, '
          f'그렇게 매긴 등수는 이 서버를 잰 값이 아니라서 순위에서 뺐다. '
          f'<strong>지우지 않는 이유는 찾는 사람이 있어서다.</strong></p>')
        if old_rank:
            W(f'<p class="sub">참고로 그때 받은 등수는 {e(collected)} 분야 '
              f'{old_rank[0]}위였다 — <strong>이 서버의 성적이 아니다.</strong> 남의 분야 '
              f'질문에 못 답했다고 매긴 번호라, 이 페이지 어디에서도 현재 등수로 쓰지 '
              f'않는다.</p>')
        W(f'<blockquote>“{e(why.rstrip())}{tail}” <span class="sub">— 채점자</span></blockquote>')

    # ── 축 ──
    os_ = rec.get("open_source") or {}
    shh = rec.get("self_hosting") or {}
    pkg = rec.get("package") or {}
    lic_caveat = ("" if os_.get("license") else
                  ' <span class="sub">이 판정의 근거는 GitHub이 알려주는 라이선스 필드 '
                  '하나다 — 파일 이름이 표준과 다르거나 전문을 손봤거나 하위 폴더에 있으면 '
                  '거기서 빈칸이 나온다. <strong>“오픈소스가 아니다”가 아니라 “우리가 확인 '
                  '못 했다”</strong>이고, 아니라면 알려 달라.</span>')
    ax = [("라이선스", (e(os_.get("license")) if os_.get("license") else "확인 못 함")
           + (f' <span class="sub">{e(os_.get("why"))}</span>' if os_.get("why") else "")
           + lic_caveat),
          ("셀프호스팅", {"packaged": "배포판 확인", "source_only": "소스만",
                       "unknown": "미확인"}.get(shh.get("state"), e(shh.get("state") or "—"))
           + (f' <span class="sub">{e(shh.get("why"))}</span>' if shh.get("why") else ""))]
    if pkg:
        ax.append(("배포 패키지",
                   f'{e(pkg.get("type"))} <code>{e(pkg.get("id"))}</code>'
                   + (f' {e(pkg.get("version"))}' if pkg.get("version") else "")
                   + (f' <span class="sub">최근 배포 {e(pkg.get("last_publish"))}</span>'
                      if pkg.get("last_publish") else "")
                   + ("" if pkg.get("installable") is not False
                      else ' <span class="tag warn">배포판 없음</span>')
                   + (f'<br><span class="tag warn">매칭 의심</span> '
                      f'<span class="sub">{e(pkg_suspect(rec))}</span>'
                      if pkg_suspect(rec) else "")))
    if rec.get("stars") is not None:
        ax.append(("저장소", f'★ {e(rec.get("stars"))}'
                          + (f' · 최종 푸시 {e(rec.get("pushed"))}' if rec.get("pushed") else "")
                          + (' · <span class="tag warn">보관됨(archived)</span>'
                             if rec.get("archived") else "")))
    if rec.get("sources"):
        ax.append(("어디서 찾았나", e(" · ".join(rec["sources"]))))
    W('<h2>우리가 잰 다른 축</h2>',
      f'<p class="sub">축 측정일 {e(ctx["axes_ts"])}. 무엇을 재기로 했는지는 결과를 보기 전에 '
      f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a>에 고정했다.</p>',
      '<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in ax) + '</dl>')

    # ── 경계 공시 (기치 ②) ──
    unknowns = ["이 서버가 주는 <strong>값이 맞는지</strong>는 채점한 분야의 질문 두 개 밖에서는 "
                "재지 않았다"]
    if not rk and misfiled:
        unknowns.append("<strong>이 서버의 분야로는 아직 채점하지 않았다</strong> — 받은 "
                        "채점은 우리가 잘못 넣은 분야의 질문이었고, 그건 이 서버를 잰 값이 "
                        "아니다")
    elif not rk:
        unknowns.append("<strong>답변 품질을 채점하지 않았다</strong> — 표에 도구·지연만 있는 "
                        "것은 못 재서이지 나빠서가 아니다")
    if shh.get("state") == "source_only":
        unknowns.append("소스가 공개돼 있다는 것과 <strong>클론해 띄우면 같은 답이 나온다</strong>는 "
                        "것은 다르다 — 후자는 재지 않았다")
    if not (rec.get("paid_disclosure") or {}).get("disclosed"):
        unknowns.append("유료 게이트가 있는지 <strong>밖에서는 판정할 수 없다</strong> — "
                        "공시가 없다고 무료라는 뜻이 아니다")
    if rm and not rec.get("addr_registered"):
        unknowns.append("우리가 부른 주소는 README에서 뽑은 <strong>추정</strong>이다 — "
                        "서버가 아니라 우리가 틀렸을 수 있다")
    unknowns.append("측정 지점은 한국 두 곳이다. 국외에서 재면 값이 다를 수 있고 확인하지 않았다")
    W('<h2>우리가 재지 않은 것</h2>',
      '<p><strong>못 봄은 없음이 아니다.</strong> 이 페이지가 말하지 <em>않는</em> 것을 적는다.</p>',
      '<ul>' + "".join(f"<li>{u}</li>" for u in unknowns) + '</ul>')

    links = []
    if rec.get("repo_url"):
        links.append(f'<a href="{e(rec["repo_url"])}" rel="noopener">저장소</a>')
    if rec.get("website_url"):
        links.append(f'<a href="{e(rec["website_url"])}" rel="noopener">공식 웹</a>')
    if rm.get("url"):
        root = "/".join(str(rm["url"]).split("/")[:3])
        links.append(f'<a href="{e(root)}" rel="noopener">엔드포인트 도메인</a>')
    W('<h2>바로 가기</h2>',
      '<p>' + (" · ".join(links) if links else "공개된 주소를 찾지 못했다.") + '</p>',
      f'<p class="sub">값이 틀렸거나 고쳤다면 <a href="{REPO}/issues">이슈</a>로 알려 달라 — '
      '다음 회차에 다시 잰다. 경쟁 서비스여도 받는다. 분야가 틀렸다·주소를 잘못 짚었다·채점이 '
      '틀렸다도 같은 창구다.</p>')
    W(f'<nav class="nav"><a href="{e(site.url_of("index"))}">← 전체 목록</a>'
      + (f' <a href="{e(site.url_of(ctx["cat_page"][cat]))}">{e(cat)} 분야</a>'
         if cat in ctx["cat_page"] else "") + '</nav>')


def build_index(ctx) -> None:
    site = ctx["site"]
    ts, rem, dead, live = ctx["ts"], ctx["rem"], ctx["dead"], ctx["live"]
    pct = round(100 * len(dead) / max(len(rem), 1))
    reg_all = [r for r in rem if r.get("addr_registered")]
    reg_dead = [r for r in dead if r.get("addr_registered")]
    reg_pct = round(100 * len(reg_dead) / max(len(reg_all), 1))
    answered = sum(1 for r in dead if r["remote"].get("http"))
    # **헤드라인에 caveat을 넣는다**(fresh-eyes 2026-08-29). 종전엔 48%만 meta·og·JSON-LD에
    # 실리고 "추정 주소였다"는 한 클릭 안쪽에만 있었다 — 검색·AI가 물어가는 문장에는 caveat이
    # 한 글자도 없었다. 그 48%에는 우리가 주소를 잘못 짚었을 수 있는 건이 섞여 있다.
    desc = (f"한국의 데이터를 다루는 MCP 서버를 직접 붙여서 잰 목록. {ts} 기준 주소를 확인한 "
            f"{len(rem)}건 중 {len(dead)}건이 우리 호출에 도구 목록을 주지 않았다 — 다만 그중 "
            f"{answered}건은 HTTP 상태코드를 돌려줬고, 관리자가 직접 등록한 주소만 세면 "
            f"{len(reg_dead)}/{len(reg_all)}({reg_pct}%)다. 도구 수·응답 지연·설명 비율과 "
            f"실제 질문 채점 결과를 분야별로 공개한다.")
    pg = Page(site, "index", "한국 데이터 MCP 실측 목록 — 지금 되는 서버가 어디까지인가",
              desc, changefreq="weekly", priority="1.0",
              jsonld={"@context": "https://schema.org", "@type": "Dataset",
                      "name": "한국 데이터 MCP 실측 목록",
                      "description": desc,
                      "url": site.url_of("index"),
                      "inLanguage": "ko",
                      "license": "https://opensource.org/licenses/MIT",
                      "isAccessibleForFree": True,
                      "dateModified": ts,
                      "temporalCoverage": ts,
                      "creator": {"@type": "Organization", "name": "sallim",
                                  "url": "https://sallim.app/"},
                      "distribution": [
                          {"@type": "DataDownload", "encodingFormat": "application/json",
                           "contentUrl": f"{REPO}/blob/main/measured.json"},
                          {"@type": "DataDownload", "encodingFormat": "text/csv",
                           "contentUrl": f"{REPO}/blob/main/axes.csv"},
                          {"@type": "DataDownload", "encodingFormat": "application/json",
                           "contentUrl": site.url_of("index.json")}]})
    W = pg.w
    W('<h1>한국 데이터 MCP — 실측 목록</h1>')
    W('<p class="lede">한국의 데이터를 AI에게 주는 <strong>MCP</strong>(Model Context '
      'Protocol — AI가 바깥 데이터·도구를 부르는 규격) 서버를 '
      '<strong>직접 붙여서 재고</strong> 그 값을 공개한다.</p>')
    W(f'<p>다른 목록은 “있다”를 말한다. 이 목록은 <strong>지금 되냐</strong>를 잰다. '
      f'{e(ts)} 기준 주소를 확인한 {len(rem)}건 중 '
      f'<strong>{len(dead)}건({pct}%)이 우리 호출에 도구 목록을 주지 않았다</strong>.</p>',
      f'<p>그 {len(dead)}건을 그대로 “죽었다”로 읽으면 안 된다 — '
      f'<strong>{answered}건은 HTTP 상태코드를 돌려줬고</strong>(서버는 살아 있었다), '
      f'{len(dead) - len(reg_dead)}건은 우리가 README에서 <strong>추정한</strong> 주소였다. '
      f'관리자가 레지스트리에 직접 등록한 주소만 세면 '
      f'<strong>{len(reg_dead)}/{len(reg_all)}({reg_pct}%)</strong>다. '
      f'<a href="{e(site.url_of("down"))}">그 명단과 상태코드 분해</a>를 그대로 공개한다.</p>')
    W(f'<p class="meta">가동 측정일 <strong>{e(ts)}</strong> ({ctx["ts_ago"]}) · '
      f'이 페이지 생성 {e(ctx["today"].isoformat())}'
      + (f' · 패키지 축 재측정 {e(ctx["pkg_ts"])}' if ctx["pkg_ts"] and ctx["pkg_ts"] != ts else "")
      + (f' · 채점 원자료 최종 변경 {e(ctx["graded"])} (저장소 이력)' if ctx["graded"] else "")
      + '</p>')

    inst = ctx["inst"]
    ipub = [r for r in inst if (r.get("package") or {}).get("installable") is True]
    inone = [r for r in inst if (r.get("package") or {}).get("installable") is False]
    iunk = [r for r in inst if (r.get("package") or {}).get("installable") is None]
    W('<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><tbody>',
      f'<tr><td>비교 가능한 서버</td><td class="n"><strong>{len(live)}</strong>건</td></tr>',
      f'<tr><td>응답했으나 못 잼(키 필요·규격 이탈)</td>'
      f'<td class="n">{len(ctx["unmeasured"])}건</td></tr>',
      f'<tr><td>응답 없음</td><td class="n">'
      f'<a href="{e(site.url_of("down"))}">{len(dead)}건</a></td></tr>',
      f'<tr><td>주제 밖(데이터 제공형 아님)</td><td class="n">{len(ctx["off"])}건</td></tr>')
    if inst:
        W(f'<tr><td>설치형(원격 주소 없음)</td><td class="n">'
          f'<a href="{e(site.url_of("self-hosted"))}">배포 확인 {len(ipub)}건 · '
          f'배포판 없음 {len(inone)}건 · 이름을 못 읽어 미측정 {len(iunk)}건</a></td></tr>')
    # **총계를 적는다**(fresh-eyes 2026-08-29). 종전엔 58과 133만 있어서, 후보 241건 중
    # 50건이 아무 설명 없이 사라졌다 — 우리가 남의 목록에서 잡아내는 종류의 은닉이다.
    nothing = [r for r in ctx["items"] if not r.get("remote") and not r.get("package")]
    W(f'<tr><td>주소도 패키지도 못 찾음</td><td class="n">{len(nothing)}건 '
      f'<span class="sub">“작동하지 않는다”가 아니라 <strong>확인하지 못했다</strong></span>'
      f'</td></tr>',
      f'<tr><td><strong>후보 전체</strong></td>'
      f'<td class="n"><strong>{len(ctx["items"])}건</strong> '
      f'<span class="sub">{len(ctx["rem"])} + {len(inst)} + {len(nothing)}</span></td></tr>',
      '</tbody></table></div>')

    W('<h2 id="왜">왜 만드나</h2>',
      '<p><strong>AI가 좋은 MCP를 못 찾는다.</strong> 한국 MCP 스토어들은 대부분 AI가 읽을 수 '
      '없다 — 화면을 JS로 그리거나(가져가면 빈 껍데기), robots로 AI 크롤러를 막는다. 정작 MCP는 '
      'AI가 쓰라고 만든 것인데.</p>',
      '<p>그래서 이 목록은 <strong>AI가 읽을 수 있게</strong> 만든다. 이 페이지도 서버가 그대로 '
      '내려주는 HTML이고, 같은 값이 '
      f'<a href="{e(site.url_of("index.json"))}">JSON</a>과 '
      f'<a href="{e(site.url_of("llms.txt"))}">llms.txt</a>로도 있다. '
      '그리고 <strong>있다고 말하지 않고 두드려 본다</strong> — 등록은 가동의 증거가 아니다.</p>',
      '<p><strong>우리 것만 싣지 않는다.</strong> 남의 MCP가 더 나으면 더 낫다고 쓴다. '
      '이 목록의 운영자가 만든 서버도 같은 표에서 같은 잣대로 잰다.</p>',
      '<p><strong>그리고 그 표를 설계한 것도 우리다.</strong> 원자료를 다 공개해도 이 편향은 '
      '안 없어진다 — 축을 하나 넣고 빼는 것만으로 등수는 바뀌고, 그 선택권을 쥔 쪽이 순위에 '
      '자기 제품을 올린 쪽이다. 그래서 이 문장을 각주가 아니라 소유 공시 바로 옆에 둔다. '
      '무엇을 재기로 했는지는 결과를 보기 전에 '
      f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a>에 고정해 두었고, 바꾼 적이 있으면 '
      '그 이력도 거기 있다 — <strong>한 번 있다.</strong></p>')

    pg.w(*client_limits(ctx))
    pg.w(*dead_breakdown(ctx))
    W('<h2 id="한눈에">한눈에</h2>',
      '<p>분야마다 1위 하나씩. 아래 각 분야의 채점 결과와 <strong>같은 값에서 나온다</strong> — '
      '여기와 본문이 어긋날 수 없다.</p>',
      '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>분야</th><th>1위</th><th>사실오류</th>'
      '<th>왜 이것이 1위인가</th></tr></thead><tbody>')
    for c in ctx["cats_live"]:
        winner = next((r for r in live
                       if ctx["cls"].get(r["name"], {}).get("category") == c
                       and ctx["rank_of"].get(r["name"], (9, ""))[0] == 1), None)
        if not winner:
            continue
        why = ctx["rank_of"][winner["name"]][1]
        n_err = ctx["err_of"].get(winner["name"])
        W(f'<tr><td><a href="{e(site.url_of(ctx["cat_page"][c]))}">{e(c)}</a></td>'
          f'<td>{name_link(ctx, winner)}</td>'
          f'<td class="n">{"—" if n_err is None else f"{n_err}건"}</td>'
          # **자르지 않는다**(fresh-eyes 2026-08-29). `clip(why,110)`은 기계적이지만
          # 총평의 길이가 서버마다 달라서, 우리 행은 41%만 보이고(남은 107자가 전부 칭찬,
          # 잘린 156자가 전부 감점) 남의 행은 82~100%가 보였다. 화면 효과는
          # "우리 행만 순수 칭찬"이다. 표가 길어지는 대가로 편향을 없앤다.
          f'<td>{e(why)}</td></tr>')
    W('</tbody></table></div>',
      '<p>종합 1등은 없다. 가중치를 우리가 정하면 우리가 상위권인 이 표에서 그 설계를 반박할 '
      '방법이 없기 때문이다. 순위는 분야 안에서만 매긴다.</p>')

    pg.w(*loses_section(ctx))

    for c in ctx["cats_live"]:
        W(f'<h2 id="{e(c.replace("·", ""))}">{e(c)} '
          f'<span class="sub">({e(CAT_EN.get(c, c))})</span></h2>')
        pg.w(*cat_block(ctx, c, full=True))
        W(f'<p class="sub"><a href="{e(site.url_of(ctx["cat_page"][c]))}">'
          f'{e(c)} 분야만 따로 보기 →</a></p>')

    pg.w(*legend(ctx))

    if ctx["unmeasured"]:
        W('<h2 id="측정-못-함">측정 못 함</h2>',
          f'<p>응답은 했지만 <strong>비교할 값을 얻지 못한 {len(ctx["unmeasured"])}건.</strong> '
          '지우지 않고 여기 둔다 — “없다”가 아니라 <strong>“우리가 못 봤다”</strong>이기 '
          '때문이다. 대부분 도구 목록을 보는 데도 키를 요구한다. 키가 있으면 잘 도는 서버일 수 '
          '있다.</p>',
          '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>서버</th><th>증상</th></tr></thead><tbody>')
        for r in sorted(ctx["unmeasured"], key=lambda x: x["name"]):
            why = (r["remote"].get("why") or "").strip() or f'HTTP {r["remote"].get("http")}'
            W(f'<tr><td>{name_link(ctx, r)}</td><td>{e(clip(why, 90))}</td></tr>')
        W('</tbody></table></div>')

    if ctx["off"]:
        W('<h2 id="주제-밖">주제 밖</h2>',
          f'<p>응답은 했지만 <strong>한국 데이터를 주는 서버가 아니라고 분류한 '
          f'{len(ctx["off"])}건.</strong> 이 목록의 주제가 아니라서 순위에 넣지 않았다 — '
          f'조용히 버리지 않고 이름과 함께 남긴다. <strong>분류가 틀렸으면 알려 달라.</strong>'
          f'</p>',
          '<div class="tw" tabindex="0" role="region" aria-label="주제 밖 서버 표"><table>'
          '<thead><tr><th>서버</th><th>우리 분류기가 본 것</th></tr></thead><tbody>')
        for r in sorted(ctx["off"], key=lambda x: x["name"]):
            W(f'<tr><td>{name_link(ctx, r)}</td>'
              f'<td>{e((ctx["cls"].get(r["name"]) or {}).get("why") or "—")}</td></tr>')
        W('</tbody></table></div>')

    W('<h2 id="넣으려면">우리 목록에 넣으려면</h2>',
      '<p><strong>우리에게 올릴 필요가 없다.</strong> '
      '<a href="https://registry.modelcontextprotocol.io" rel="noopener">공식 MCP 레지스트리</a>에 '
      '등록하면 다음 회차에 자동으로 들어온다. 그쪽이 나은 이유는 우리만 읽는 게 아니라서다.</p>',
      f'<p>이미 등록했는데 여기 없다면 <strong>우리 수집기의 버그일 수 있다</strong> — '
      f'<a href="{REPO}/issues">이슈</a>로 알려 달라. 경쟁 서비스여도 받는다.</p>',
      '<p>제출은 등재가 아니다. 실제로 <code>tools/list</code>에 응답해야 표에 오른다 — 우리가 '
      '통과시키고 말고 할 것이 없다.</p>',
      '<h2 id="고쳤다면">고쳤다면 다시 잰다</h2>',
      f'<p>이 표의 값은 <strong>{e(ts)} 그 순간의 기록</strong>이다. 고쳤다면 '
      f'<a href="{REPO}/issues">이슈</a>로 알려 달라 — 다음 회차에 다시 잰다.</p>',
      '<p><strong>우리가 먼저 다시 두드리지는 않는다.</strong> 바뀐 게 없는 서버를 주기적으로 '
      '재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다. 그래서 두드리는 대신 신호를 '
      '받는다.</p>',
      '<p><strong>순위는 전원 동시에만 다시 잰다 — 운영자인 우리도 예외가 아니다.</strong> '
      '우리는 고칠 때마다 다시 잴 수 있고 남은 그럴 수 없다. 개별 재측정을 순위에 반영하면 우리 '
      '서버만 계단식으로 올라가고 남은 자기 최악의 순간에 박제된다.</p>',
      f'<p class="sub">방법론과 한계는 <a href="{e(site.url_of("method"))}">어떻게 재나 · 믿으면 '
      f'안 되는 부분</a>에 따로 있다.</p>')
    W(f'<nav class="nav"><a href="{e(site.url_of("method"))}">어떻게 재나</a>'
      f'<a href="{e(site.url_of("down"))}">응답 없는 서버 {len(dead)}건</a>'
      f'<a href="{e(site.url_of("self-hosted"))}">설치형 {len(inst)}건</a>'
      f'<a href="{e(site.url_of("index.json"))}">JSON</a>'
      f'<a href="{REPO}">저장소</a></nav>')


def build_category(ctx, c) -> None:
    site = ctx["site"]
    n = len([r for r in ctx["live"] if ctx["cls"].get(r["name"], {}).get("category") == c])
    desc = (f"{c} 분야 한국 MCP 서버 {n}건을 {ctx['ts']}에 직접 호출해 잰 결과 — 도구 수, 응답 "
            f"지연, 설명·주석 비율, 그리고 실제 질문에 답하게 하고 채점한 순위.")
    pg = Page(site, ctx["cat_page"][c], f"{c} 한국 MCP 서버 실측 순위", desc,
              crumbs=[("한국 데이터 MCP 실측 목록", "index"), (c, ctx["cat_page"][c])],
              priority="0.8",
              jsonld={"@context": "https://schema.org", "@type": "ItemList",
                      "name": f"{c} 한국 MCP 서버 실측 순위", "description": desc,
                      "numberOfItems": n,
                      # position은 **채점이 준 등수 그대로**다. 종전엔 `i+1`로 다시 매겼는데,
                      # 2위가 이번 회차에 빠지면 HTML은 1·3위인데 JSON-LD만 1·2위가 됐다
                      # (codex 교차검증 2026-08-29) — 빈자리를 위로 당기지 않는다는 규약을
                      # 구조화데이터에서만 어기고 있었던 셈이다.
                      "itemListElement": [
                          {"@type": "ListItem", "position": ctx["rank_of"][r["name"]][0],
                           "name": r["name"],
                           "url": site.url_of(ctx["page_of"][r["name"]])}
                          for r in sorted([r for r in ctx["live"]
                                           if ctx["cls"].get(r["name"], {}).get("category") == c
                                           and r["name"] in ctx["rank_of"]
                                           and r["name"] not in MISFILED],
                                          key=lambda r: ctx["rank_of"][r["name"]][0])]})
    pg.w(f'<h1>{e(c)} — 한국 MCP 서버 실측</h1>',
         f'<p class="meta">가동 측정일 <strong>{e(ctx["ts"])}</strong> ({ctx["ts_ago"]}) · '
         f'이 페이지 생성 {e(ctx["today"].isoformat())}'
         + (f' · 채점 원자료 최종 변경 {e(ctx["graded"])} (저장소 이력)' if ctx["graded"] else "")
         + '</p>')
    pg.w(*cat_block(ctx, c, full=True))
    pg.w(*legend(ctx))
    pg.w(f'<nav class="nav"><a href="{e(site.url_of("index"))}">← 전체 목록</a>'
         f'<a href="{e(site.url_of("method"))}">어떻게 재나</a></nav>')


def build_down(ctx) -> None:
    site, dead, ts = ctx["site"], ctx["dead"], ctx["ts"]
    answered = sum(1 for r in dead if r["remote"].get("http"))
    desc = (f"{ts} 측정에서 우리 호출에 도구 목록을 주지 않은 한국 MCP 서버 {len(dead)}건. "
            f"그중 {answered}건은 HTTP 상태코드를 돌려줬다 — 폐기 판정이 아니라 관측 기록이고, "
            "우리 클라이언트의 한계이거나 우리가 주소를 잘못 짚은 것일 수 있다.")
    pg = Page(site, "down", "도구 목록을 못 받은 한국 MCP 서버 — 상태코드까지 공개", desc,
              crumbs=[("한국 데이터 MCP 실측 목록", "index"), ("도구 목록 못 받음", "down")],
              priority="0.6")
    W = pg.w
    W(f'<h1>도구 목록을 못 받은 서버 {len(dead)}건</h1>',
      f'<p class="lede">{e(ts)} 측정에서 우리가 <code>tools/list</code>를 보냈을 때 도구 '
      f'목록이 오지 않은 목록. <strong>폐기 판정이 아니라 관측 기록이다</strong> — '
      f'그중 <strong>{answered}건은 HTTP 상태코드를 돌려줬다</strong>. 서버는 살아 있었고 '
      f'우리 부르는 방식이 그 서버와 안 맞았을 수 있다.</p>',
      f'<p class="meta">측정일 {e(ts)} ({ctx["ts_ago"]}) · 이 페이지 생성 '
      f'{e(ctx["today"].isoformat())}</p>',
      f'<p>고쳤거나 우리가 주소를 잘못 짚었다면 <a href="{REPO}/issues">이슈</a>로 알려 달라. '
      '다음 회차에 다시 잰다.</p>')
    pg.w(*dead_breakdown(ctx))
    # **개인별로 흩어 놓으면 원인을 놓친다.** 명단의 절반 이상이 몇 개 무료 호스팅에
    # 몰려 있는데, 그 콜드스타트는 우리 타임아웃(15초)보다 길 수 있다(fresh-eyes 2026-08-29).
    hosts = collections.Counter()
    for r in dead:
        u = r["remote"].get("url") or ""
        for h in ("server.smithery.ai", "up.railway.app", "onrender.com", "fly.dev",
                  "hf.space", "vercel.app"):
            if h in u:
                hosts[h] += 1
    top = [(h, n) for h, n in hosts.most_common() if n >= 2]
    if top:
        W(f'<p><strong>이 명단은 사람별로 흩어져 보이지만 실제로는 몇 개 플랫폼에 몰려 '
          f'있다</strong> — {len(dead)}건 중 {sum(n for _h, n in top)}건이 '
          + " · ".join(f"<code>{e(h)}</code> {n}건" for h, n in top)
          + '이다. 무료 티어의 콜드스타트가 우리 타임아웃(15초)보다 길 수 있고, 플랫폼이 '
            '앞단에서 통째로 끊었을 수도 있다. <strong>개인의 서버가 나빠서라고 읽지 '
            '마라.</strong></p>')
    pg.w(*client_limits(ctx))
    strong = [r for r in dead if r.get("addr_registered")]
    weak = [r for r in dead if r not in strong]
    for title, group, note in (
            ("등록된 주소가 응답하지 않음", strong,
             "관리자가 공식 레지스트리에 <strong>직접 등록한</strong> 주소다. 주장이 강하다."),
            ("추정 주소가 응답하지 않음", weak,
             "우리가 README에서 뽑은 <strong>추정</strong> 주소다. <strong>우리가 주소를 잘못 "
             "짚었을 수 있다</strong> — 그 서버가 죽었다는 뜻으로 읽지 마라.")):
        if not group:
            continue
        W(f'<h2>{e(title)} — {len(group)}건</h2>', f'<p>{note}</p>',
          '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>서버</th><th>증상</th><th>우리가 부른 주소</th>'
          '</tr></thead><tbody>')
        for r in sorted(group, key=lambda x: x["name"]):
            rm = r["remote"]
            why = rm.get("why") or f'HTTP {rm.get("http")}'
            # 상태코드가 우리 한계 때문일 수 있는 경우를 그 줄에서 바로 밝힌다.
            hint = {400: "세션을 안 열고 tools/list를 보낸 우리 탓일 수 있다",
                    405: "SSE 자리에 POST를 보낸 우리 탓일 수 있다",
                    307: "서버가 옮긴 자리를 알려줬는데 우리가 안 따라갔다",
                    503: "그 순간 자고 있었을 수 있다"}.get(rm.get("http"), "")
            gw = gateway_of(r)
            if gw:
                hint = (hint + " · " if hint else "") + f"공용 게이트웨이({gw})의 응답이다"
            W(f'<tr><td>{name_link(ctx, r)}</td>'
              f'<td>{e(clip(why, 80))}'
              + (f'<br><span class="sub">{e(hint)}</span>' if hint else "")
              + f'{"<br><span class=\'sub\'>재시도 없이 한 번만 불렀다</span>" if r["remote"].get("retried") is False else ""}</td>'
              f'<td><code>{e(rm.get("url") or "")}</code></td></tr>')
        W('</tbody></table></div>')
    W(f'<nav class="nav"><a href="{e(site.url_of("index"))}">← 전체 목록</a></nav>')


def build_selfhosted(ctx) -> None:
    """설치형 — 원격 주소가 없어 가동을 못 잰 서버. **못 잼과 안 됨을 가른다.**"""
    site, inst = ctx["site"], ctx["inst"]
    desc = (f"원격 주소 없이 설치해 쓰는 한국 MCP 서버 {len(inst)}건의 배포 패키지·라이선스 "
            f"실측({ctx['axes_ts']} 기준). 가동은 재지 못했다 — 못 잰 것과 안 되는 것은 다르다.")
    pg = Page(site, "self-hosted", "설치해서 쓰는 한국 MCP 서버 — 배포·라이선스 실측", desc,
              crumbs=[("한국 데이터 MCP 실측 목록", "index"), ("설치형", "self-hosted")],
              priority="0.6")
    W = pg.w
    W(f'<h1>설치형 {len(inst)}건</h1>',
      '<p class="lede">원격 주소가 없어 <code>tools/list</code>로 <strong>가동을 재지 '
      '못한</strong> 서버다. 재지 못한 것은 안 된다는 뜻이 아니다 — 대신 잴 수 있는 것(배포 '
      '패키지·라이선스)을 잰다.</p>',
      f'<p class="meta">패키지 축 측정일 {e(ctx["pkg_ts"] or ctx["axes_ts"])} · 라이선스 축 '
      f'{e(ctx["axes_ts"])} · 이 페이지 생성 {e(ctx["today"].isoformat())}</p>',
      '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>서버</th><th>배포 패키지</th><th>최근 배포</th>'
      '<th>라이선스</th><th>★</th></tr></thead><tbody>')
    def k(r):
        p = r.get("package") or {}
        return (0 if p.get("installable") is True else 1 if p.get("installable") is None else 2,
                -(r.get("stars") or 0), r["name"])
    for r in sorted(inst, key=k):
        p = r.get("package") or {}
        os_ = r.get("open_source") or {}
        if p.get("installable") is True:
            state = f'{e(p.get("type"))} <code>{e(p.get("id"))}</code>'
            sus = pkg_suspect(r)
            if sus:
                state += (f'<br><span class="tag warn">매칭 의심</span> '
                          f'<span class="sub">{e(sus)}</span>')
        elif p.get("installable") is False:
            state = '<span class="tag warn">배포판 없음</span>'
        else:
            state = '<span class="tag">이름을 못 읽어 미측정</span>'
        W(f'<tr><td>{name_link(ctx, r)}</td><td>{state}</td>'
          f'<td class="n">{e(p.get("last_publish") or "—")}</td>'
          f'<td>{e(os_.get("license") or "확인 못 함")}</td>'
          f'<td class="n">{e(r.get("stars") if r.get("stars") is not None else "—")}</td></tr>')
    W('</tbody></table></div>',
      '<p class="sub"><strong><code>확인 못 함</code>을 “오픈소스 아님”으로 읽지 말라.</strong> '
      '저장소가 비공개거나 지워졌거나 이름이 바뀐 것도 여기 들어온다. 다만 공개 저장소인데 '
      '라이선스 파일이 없는 것은 기본값이 저작권 전부 유보라 실제로 가져다 쓸 수 없다.</p>',
      '<p class="sub"><strong><code>배포판 없음</code>은 “우리가 그 이름으로 npm·PyPI를 '
      '조회했더니 없더라”는 뜻이다.</strong> 다른 이름으로 냈거나 컨테이너(ghcr 등)로 '
      '배포했으면 우리 조회 경로(npm·PyPI 둘뿐)에는 안 잡힌다 — 그건 그 저장소의 결함이 '
      '아니라 우리 조회 범위의 한계다.</p>',
      '<p class="sub"><strong>패키지는 <em>이름</em>으로 맞춘다.</strong> 저장소가 배포판을 '
      '선언하지 않으면 우리는 이름으로 찾는데, 이름은 겹친다 — 그래서 남의 패키지가 붙을 수 '
      '있다. 우리가 기계로 잡을 수 있는 경우(MCP 공개보다 앞선 배포일)는 「매칭 의심」으로 '
      '표시했고, 나머지는 못 잡는다. 자기 서버 줄이 틀렸으면 알려 달라 — 지우거나 고친다.</p>',
      '<p class="sub"><strong><code>이름을 못 읽어 미측정</code>은 우리 파서의 실패다.</strong> '
      '2026-08-20에 우리는 못 읽은 패키지명을 남의 서버 “설치 불가”로 게시한 적이 있다. '
      '그래서 셋을 갈라 적는다.</p>',
      f'<nav class="nav"><a href="{e(site.url_of("index"))}">← 전체 목록</a></nav>')


def build_method(ctx) -> None:
    site, ts, items = ctx["site"], ctx["ts"], ctx["items"]
    desc = ("이 목록을 어떻게 재는지와 믿으면 안 되는 부분 — 수집·측정·질문·채점 절차, 재현되는 "
            "값과 재현되지 않는 값의 구분, 우리가 재지 않은 것.")
    pg = Page(site, "method", "어떻게 재나 · 믿으면 안 되는 부분 — 한국 MCP 실측", desc,
              crumbs=[("한국 데이터 MCP 실측 목록", "index"), ("어떻게 재나", "method")],
              priority="0.7")
    W = pg.w
    W('<h1>어떻게 재나</h1>',
      '<div class="tw" tabindex="0" role="region" aria-label="가로로 스크롤되는 표"><table><thead><tr><th>단계</th><th>하는 일</th><th>주기</th></tr></thead>'
      '<tbody>',
      '<tr><td>collect</td><td>공식 레지스트리 전수 + GitHub 검색 + mcpmoa 공개 API</td>'
      '<td>—</td></tr>',
      '<tr><td>filter</td><td>한국 관련성(한글·.go.kr·기관명) → 후보 좁히기</td><td>—</td></tr>',
      '<tr><td>enrich</td><td>README에서 엔드포인트·패키지·기관 도메인 추출</td><td>—</td></tr>',
      '<tr><td>classify</td><td>분야·데이터제공형 판정(LLM, 결과는 classification.json에 고정)'
      '</td><td>—</td></tr>',
      '<tr><td>measure</td><td><code>tools/list</code> 실호출 — 가동·도구수·지연·설명·주석</td>'
      '<td>매주</td></tr>',
      '<tr><td>answer</td><td>분야별 실제 질문을 서버에 던져 답하게 한다(Haiku)</td>'
      '<td>매월</td></tr>',
      '<tr><td>grade</td><td>그 답을 원문과 대조해 채점한다(Opus) → 순위</td><td>매월</td></tr>',
      '</tbody></table></div>',
      '<p><strong>가동은 매주, 순위는 매월 1일</strong>에 다시 잰다. 서버가 안 바뀌면 채점 결과도 '
      '안 바뀌는데 매주 재호출하는 것은 새 정보가 아니라 남의 서버에 지우는 부하다.</p>',
      '<p>두드릴 때는 <code>tools/list</code>를 보내고, <strong>200이 온 서버에 한해</strong> '
      '간격을 두고 2회 더 불러 웜을 잰다(콜드 1 + 웜 2). User-Agent로 우리를 밝힌다.</p>',
      '<p><strong>200이 안 온 서버는 그렇지 않다.</strong> 재시도는 연결 실패·5xx일 때만 '
      '1회이고, 4xx는 <strong>한 번 부른 결과가 그대로 명단에 오른다</strong>. 종전에 이 '
      '자리에 “3회”라고만 적어 두었는데, 실패한 서버에는 사실이 아니었다 — '
      'fresh-eyes 검수가 잡아 고쳤다(2026-08-29).</p>',
      f'<p><strong>가동 지표는 돌리면 같은 값이 나온다</strong> — 원자료가 '
      f'<a href="{REPO}/blob/main/measured.json">measured.json</a>에 있다. '
      f'<strong>순위는 그렇지 않다</strong> — 채점이 모델 판단이라 같은 입력에도 흔들린다. '
      f'얼마나 흔들리는지를 우리가 직접 재서 '
      f'<a href="{REPO}/tree/main/variance">variance/</a>에 공개해 두었다. 우리가 1위인 '
      f'자리일수록 이 두 문장을 함께 읽어 달라.</p>')
    no_addr_no_pkg = [r for r in items if not r.get("remote") and not r.get("package")]
    pkg_only = [r for r in items
                if not r.get("remote") and (r.get("package") or {}).get("installable") is True]
    pg.w(*client_limits(ctx))
    W('<h2>믿으면 안 되는 부분</h2>', '<ul>',
      '<li><strong>정확성은 분야마다 질문 두 개로만 봤다.</strong> 그 두 문항이 그 분야를 '
      '대표한다는 보장은 없다. 질문은 공개돼 있으니 더 나은 질문을 알려 달라</li>',
      f'<li><strong>채점자도 모델이다.</strong> 근거를 전부 공개하는 것으로 줄일 수는 있어도 '
      f'없앨 수는 없다 — 이유와 실측 근거는 '
      f'<a href="{REPO}/blob/main/JUDGING.md">JUDGING.md</a>에 있다</li>',
      '<li><strong>한 번 물어본 순위다.</strong> 다시 물으면 등수가 갈릴 수 있다 — 우리 서버로 '
      '재 보니 질문 네 자리 중 두 곳이 갈렸다. 다음 채점 회차부터 3회로 잰다</li>',
      f'<li><strong>측정 항목을 우리가 골랐다.</strong> 원자료 공개로 줄일 수는 있어도 없앨 수는 '
      f'없다 — 무엇을 고정했고 무엇을 언제 왜 바꿨는지는 '
      f'<a href="{REPO}/blob/main/PROTOCOL.md">신뢰 규약</a>에 있다. '
      f'<strong>결과를 본 뒤에 바꾼 적이 한 번 있고</strong>, 그 건도 거기 적어 두었다</li>',
      '<li><strong>측정 지점은 한국 두 곳이다.</strong> 국외에서 재면 값이 다를 수 있고 아직 '
      '확인하지 않았다</li>',
      '<li><strong>콜드는 한 번뿐이다.</strong> 그 순간 그 서버가 자고 있었을 수 있다</li>',
      f'<li><strong>못 잰 것이 더 많다.</strong> 후보 중 {len(no_addr_no_pkg)}건은 주소도 '
      f'패키지도 찾지 못했다. “작동하지 않는다”가 아니라 <strong>확인하지 못했다</strong>는 '
      f'뜻이다 — 그 밖에 {len(pkg_only)}건은 배포 패키지는 확인했으나 원격 주소가 없어 응답을 '
      f'못 쟀다</li>',
      '</ul>',
      '<h2>날짜를 어떻게 적나</h2>',
      f'<p>이 사이트의 모든 값에는 <strong>잰 날</strong>이 붙는다 — 문서를 뽑은 날이 아니다. '
      f'가동 지표는 {e(ts)}, 축(오픈소스·셀프호스팅)은 {e(ctx["axes_ts"])}'
      + (f', 패키지 축은 {e(ctx["pkg_ts"])}' if ctx["pkg_ts"] else "")
      + f'에 쟀고, 이 페이지 자체는 {e(ctx["today"].isoformat())}에 생성됐다. '
        '한때 우리는 “마지막 측정”에 <em>문서를 뽑은 날</em>을 찍고 있었다. 그 자리는 지금 '
        '원자료에 측정일이 없으면 <strong>생성이 실패하도록</strong> 막혀 있다.</p>',
      f'<nav class="nav"><a href="{e(site.url_of("index"))}">← 전체 목록</a></nav>')


def build_machine(ctx) -> None:
    """기계가 읽는 표면. 사람 페이지와 **같은 값**이어야 한다 — 따로 쓰면 따로 썩는다."""
    site, ts = ctx["site"], ctx["ts"]
    rows = []
    # **counts가 배열에서 재현돼야 한다**(fresh-eyes 2026-08-29). 종전엔 「주제 밖」 2건이
    # 아무 표시 없이 섞여 있어서, 기계가 배열로 세면 comparable 20·unmeasurable 10이
    # 나오는데 counts는 19·9였다. 총계 검사가 통과하는 종류의 조용한 어긋남이다.
    bucket_of = {}
    for name_, b in [(r["name"], "comparable") for r in ctx["live"]] \
            + [(r["name"], "off_topic") for r in ctx["off"]] \
            + [(r["name"], "unmeasurable") for r in ctx["unmeasured"]] \
            + [(r["name"], "unreachable") for r in ctx["dead"]]:
        bucket_of[name_] = b
    # 사람 페이지에서 순위표에 실제로 서 있는 서버. **여기 없는데 등수만 있는 줄**은
    # 지난 채점 회차의 등수를 이번 회차 판정처럼 보이게 한다 — codex 교차검증이 잡은
    # 자리다(2026-08-29). 등수를 지우지는 않는다(빈자리를 위로 당기지 않는 규약과 같다).
    # 대신 **그 등수가 어느 회차 것이고 왜 지금 순위표에 없는지**를 같은 줄에 적는다.
    ranked_now = {r["name"] for r in ctx["live"]
                  if r["name"] in ctx["rank_of"] and r["name"] not in MISFILED}
    for r in ctx["live"] + ctx["unmeasured"] + ctx["dead"] + ctx["off"]:
        rm = r.get("remote") or {}
        rk = ctx["rank_of"].get(r["name"])
        stale = bool(rk) and r["name"] not in ranked_now
        rows.append({
            "name": r["name"],
            "bucket": bucket_of[r["name"]],
            "page": site.url_of(ctx["page_of"][r["name"]]),
            "category": (MISFILED[r["name"]][1] if r["name"] in MISFILED
                         else (ctx["cls"].get(r["name"]) or {}).get("category")),
            "category_corrected_from": (MISFILED[r["name"]][0]
                                        if r["name"] in MISFILED else None),
            "repo_url": r.get("repo_url"),
            "endpoint": rm.get("url"),
            "endpoint_source": "registry" if r.get("addr_registered") else "readme_guess",
            "measured_at": ts,
            "reachable": bool(rm.get("reachable")),
            "tool_count": rm.get("tool_count"),
            "warm_ms": rm.get("warm_ms"), "cold_ms": rm.get("cold_ms"),
            "described_pct": (rm.get("quality") or {}).get("described_pct"),
            "annotated_pct": (rm.get("quality") or {}).get("annotated_pct"),
            "rank_in_category": rk[0] if rk else None,
            "rank_round": (ctx["graded"] if rk else None),
            "rank_graded_as": (RENAMED.get(r["name"]) if rk else None),
            "rank_is_current": (None if not rk else not stale),
            "rank_note": (None if not stale else
                          (f"이 등수는 무효다 — 우리 수집기가 '{MISFILED[r['name']][0]}' 분야로 "
                           f"잘못 넣어 그 분야 질문으로 채점한 결과이고, 실제 분야는 "
                           f"'{MISFILED[r['name']][1]}'이다. 이 서버를 잰 값이 아니다"
                           if r["name"] in MISFILED else
                           "지난 채점 회차의 등수다 — 이번 회차엔 응답하지 않아 사람용 "
                           "순위표에서는 빠져 있다. 다시 채점하기 전까지 번호는 그대로 둔다"
                           if not rm.get("reachable") else
                           "지난 채점 회차의 등수다 — 이번 회차엔 비교 가능한 값을 얻지 못해 "
                           "사람용 순위표에서는 빠져 있다")),
            "fact_errors": ctx["err_of"].get(r["name"]),
            "license": (r.get("open_source") or {}).get("license"),
            "self_hosting": (r.get("self_hosting") or {}).get("state"),
            "package_match_suspect": pkg_suspect(r) or None,
            "operated_by_us": r["name"].startswith(OURS),
            "symptom": (rm.get("why") or None) if not rm.get("reachable") else None,
            "http_status": rm.get("http"),
            "retried": rm.get("retried"),
            "shared_gateway": gateway_of(r) or None,
        })
    rows.sort(key=lambda x: (x["category"] or "힣", x["rank_in_category"] or 99, x["name"]))
    doc = {
        "name": "한국 데이터 MCP 실측 목록",
        "url": site.url_of("index"),
        "source_repo": REPO,
        "license": "MIT (측정값·문서). 응답 발췌는 각 서버 운영자의 것.",
        "measured_at": ts,
        "axes_measured_at": ctx["axes_ts"],
        "package_axis_measured_at": ctx["pkg_ts"],
        "generated_at": ctx["today"].isoformat(),
        "boundaries": [
            "측정일은 잰 날이다 — 이 파일을 만든 날(generated_at)과 다르다.",
            "reachable=false 는 폐기 판정이 아니라 그 시점의 관측이고, **우리 호출의 결과**다 "
            "— http_status 가 있는 줄은 서버가 살아서 상태코드를 돌려준 것이다. "
            "client_limits 를 먼저 읽어라.",
            "retried=false 는 단 한 번 부른 결과라는 뜻이다.",
            "shared_gateway 가 있으면 그 오류는 공용 게이트웨이의 것이지 그 저장소의 결함이 "
            "아닐 수 있다 — 우리가 둘을 갈라 재지 못했다.",
            "counts 는 servers 배열의 bucket 으로 재현된다. install_only·"
            "no_address_no_package 는 배열 밖이다(가동을 못 쟀다).",
            "endpoint_source=readme_guess 는 우리가 주소를 잘못 짚었을 수 있다는 뜻이다.",
            "rank_in_category 는 지표 가중합이 아니라 실제 질문 답변을 모델이 채점한 결과이고, "
            "같은 입력에도 흔들린다.",
            "rank_graded_as 가 있으면 그 등수는 **옛 이름으로 받은 것**이다 — 저장소가 옮겨져 "
            "이름이 바뀌었고 엔드포인트가 같아 이었다. 채점 원자료에는 옛 이름만 있다.",
            "가동은 매주·순위는 매월이라 두 값의 회차가 다르다 — rank_is_current=false 인 줄은 "
            "지난 회차의 등수이고 이번 회차 순위표에는 없다(사유는 rank_note). 등수를 지우지 "
            "않는 이유는, 빈자리를 위로 당기면 재채점 없이 등수가 오른 것처럼 보이기 때문이다.",
            "license=null 은 '오픈소스 아님'이 아니라 '확인 못 함'이다.",
            "배포 패키지는 이름으로 맞춘 것이라 남의 패키지가 붙을 수 있다 — 기계로 잡히는 "
            "경우만 package_match_suspect 에 사유가 들어간다(못 잡는 경우가 더 많다).",
            "이 목록을 만든 곳도 이 안에 서버를 운영한다(operated_by_us=true) — 축을 고른 것도 "
            "같은 곳이다.",
            f"원격 주소가 없어 가동을 재지 못한 서버 {len(ctx['inst'])}건은 이 배열에 없다: "
            + site.url_of("self-hosted"),
        ],
        "counts": {"comparable": len(ctx["live"]), "unmeasurable": len(ctx["unmeasured"]),
                   "unreachable": len(ctx["dead"]), "off_topic": len(ctx["off"]),
                   "install_only": len(ctx["inst"]),
                   "no_address_no_package": len([r for r in ctx["items"]
                                                 if not r.get("remote")
                                                 and not r.get("package")]),
                   "candidates_total": len(ctx["items"])},
        "client_limits": [
            "initialize 핸드셰이크를 하지 않는다 — 규격을 지키는 서버가 HTTP 400을 주는 것이 "
            "정상 동작이다",
            "POST + 307 리다이렉트를 따라가지 않는다",
            "SSE(GET)를 시도하지 않는다 — POST 고정이라 SSE 엔드포인트는 405를 준다",
            "4xx는 재시도하지 않는다(재시도는 연결 실패·5xx일 때만 1회)",
            "서버가 보낸 오류 본문을 저장하지 않는다 — 상태코드만 남겼다",
        ],
        "servers": rows,
    }
    site.extra.append(("index.json", json.dumps(doc, ensure_ascii=False, indent=1) + "\n"))

    lines = ["# 한국 데이터 MCP — 실측 목록", "",
             "> 한국의 데이터를 AI에게 주는 MCP 서버를 직접 붙여서 재고 그 값을 공개한다.",
             f"> 가동 측정일 {ts} · 이 파일 생성 {ctx['today'].isoformat()}.",
             "> 측정일은 잰 날이다 — 파일을 뽑은 날이 아니다.", "",
             f"- [전체 목록]({site.url_of('index')}): 분야별 순위와 측정값",
             f"- [기계용 JSON]({site.url_of('index.json')}): 같은 값의 구조화본",
             f"- [어떻게 재나 · 믿으면 안 되는 부분]({site.url_of('method')})",
             f"- [응답하지 않는 서버]({site.url_of('down')}): {len(ctx['dead'])}건 — 폐기 판정이 "
             "아니라 관측 기록",
             f"- [설치형]({site.url_of('self-hosted')}): {len(ctx['inst'])}건 — 가동을 재지 못했다",
             f"- [원자료 저장소]({REPO})", "", "## 분야별", ""]
    for c in ctx["cats_live"]:
        lines.append(f"### {c}")
        lines.append(f"- [분야 페이지]({site.url_of(ctx['cat_page'][c])})")
        for r in sorted([r for r in ctx["live"]
                         if (ctx["cls"].get(r["name"]) or {}).get("category") == c],
                        key=lambda r: ctx["rank_of"].get(r["name"], (99, ""))[0]):
            rk = ctx["rank_of"].get(r["name"])
            tag = f"{rk[0]}위" if rk else "미채점"
            ep = (r.get("remote") or {}).get("url") or ""
            lines.append(f"- [{r['name']}]({site.url_of(ctx['page_of'][r['name']])}): {tag} · "
                         f"도구 {(r.get('remote') or {}).get('tool_count') or '—'}종 · "
                         f"{ts} 측정" + (f" · 엔드포인트 {ep}" if ep else ""))
        lines.append("")
    answered = sum(1 for r in ctx["dead"] if r["remote"].get("http"))
    reg_dead = [r for r in ctx["dead"] if r.get("addr_registered")]
    lines += ["## 경계", "",
              f"- 도구 목록을 못 받은 {len(ctx['dead'])}건 중 {answered}건은 HTTP 상태코드를 "
              f"돌려줬다 — 서버는 살아 있었다. 관리자가 직접 등록한 주소만 세면 "
              f"{len(reg_dead)}건이고, 나머지는 우리가 README에서 **추정**한 주소다.",
              "- 우리 클라이언트는 initialize 핸드셰이크·POST 307 추적·SSE(GET)를 못 하고, "
              "4xx를 재시도하지 않는다. 그 한계에 걸린 서버가 명단에 섞여 있다.",
              "- 못 봄은 없음이 아니다. 재지 못한 축은 재지 못했다고 적는다.",
              "- 순위는 모델 채점이라 같은 입력에도 흔들린다. 가동 지표는 재현된다.",
              "- 이 목록을 만든 곳도 여기에 서버를 운영한다 — 축을 고른 것도 같은 곳이다.",
              "- 우리 것만 싣지 않는다. 남의 MCP가 더 나으면 더 낫다고 쓴다.", ""]
    site.extra.append(("llms.txt", "\n".join(lines)))

    urls = []
    for pg in site.pages:
        # lastmod는 **이 문서가 마지막으로 바뀐 날**이다. 측정일을 쓰면 문서를 고쳐도
        # 크롤러에겐 안 바뀐 것으로 보인다(측정일은 본문에 따로 적혀 있다).
        urls.append(f"<url><loc>{e(pg.url)}</loc>"
                    f"<lastmod>{ctx['today'].isoformat()}</lastmod>"
                    f"<changefreq>{pg.changefreq}</changefreq>"
                    f"<priority>{pg.priority}</priority></url>")
    site.extra.append(("sitemap.xml",
                       '<?xml version="1.0" encoding="UTF-8"?>\n'
                       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                       + "\n".join(urls) + "\n</urlset>\n"))
    site.extra.append(("robots.txt",
                       "User-agent: *\n"
                       "Allow: /\n\n"
                       "# AI 크롤러도 막지 않는다 — 이 목록은 AI가 읽으라고 만든 것이다.\n"
                       "# (한국 MCP 스토어 다수가 robots로 AI 봇을 막고 있고, 그것이 이 목록의\n"
                       "#  존재 이유 중 하나다.)\n\n"
                       f"Sitemap: {site.url_of('sitemap.xml')}\n"
                       f"# LLM-Index: {site.url_of('llms.txt')}\n"
                       f"# JSON: {site.url_of('index.json')}\n"))
    # **없는 주소에 200을 주지 않는다(소프트 404).** CF Pages는 매칭되지 않은 경로에
    # `/404.html`이 있으면 그것을 404로 내려준다 — 없으면 첫 페이지를 200으로 내려서
    # 오타·스크레이퍼가 만든 주소가 전부 첫 화면의 복제본이 된다(실측: `/nope` → 200).
    # 이 조직은 같은 것을 아펙스에서 이미 한 번 봉합했다(2026-08-16, T-2026W33-236).
    site.extra.append(("404.html",
                       '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
                       '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
                       '<title>없는 주소 — 한국 데이터 MCP 실측 목록</title>\n'
                       '<meta name="robots" content="noindex,follow">\n'
                       f'<style>{CSS}</style>\n</head>\n<body><div class="wrap">\n'
                       '<h1>여기엔 아무것도 없다</h1>\n'
                       '<p class="lede">주소가 바뀌었거나 오타일 수 있다. '
                       '<strong>없는 주소에 200을 주지 않는다</strong> — 이 응답의 상태코드는 '
                       '404다.</p>\n'
                       f'<nav class="nav"><a href="{site.url_of("index")}">전체 목록</a>'
                       f'<a href="{site.url_of("index.json")}">기계용 JSON</a>'
                       f'<a href="{REPO}/issues">이슈로 알리기</a></nav>\n'
                       '</div></body></html>\n'))

    # `/.well-known/mcp.json`은 만들지 않는다. 그 스키마(ServerDetail)는 **서버 한 개**를
    # 기술하는 형식인데 이 사이트는 서버가 아니라 목록이다 — 목록을 서버인 척 실으면
    # 클라이언트가 붙으려 하다 실패하고, 그건 우리가 남에게서 지적하는 종류의 거짓말이다.
    # 아펙스(sallim.app)가 같은 이유로 이 경로를 비워 둔 것과 같은 판단이다(D-2026W35-09·10).


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://mcp-index.sallim.app")
    ap.add_argument("--out", default="site")
    ap.add_argument("--ext", default="", help="URL의 확장자. CF Pages는 확장자 없는 쪽이 정본이다")
    # IndexNow 키는 **공개 호스팅이 규격**이다(엔진이 이 파일을 읽어 소유를 확인한다) —
    # 시크릿이 아니다. 없으면 조용히 건너뛴다: 색인 핑은 best-effort고, 없다고 사이트가
    # 안 나가는 것이 더 나쁘다.
    ap.add_argument("--indexnow-key-file", default="/data/ops/.indexnow-key")
    a = ap.parse_args()

    d = json.load(open("measured.json", encoding="utf-8"))
    cls = {v["name"]: v for v in json.load(open("classification.json",
                                               encoding="utf-8"))["items"].values()}
    try:
        src = {i["name"]: i for i in json.load(open("candidates_filtered.json",
                                                    encoding="utf-8"))["items"]}
    except OSError:
        src = {}
    try:
        rk = json.load(open("ranking.json", encoding="utf-8"))["items"]
    except OSError:
        rk = {}

    # ── 날짜: 잰 날만 쓴다. 없으면 멈춘다(render_readme.py와 같은 fail-closed) ──
    ts = d.get("measured_at")
    if not ts:
        print("생성 중단 — measured.json에 `measured_at`이 없다. 렌더 날짜를 측정일로 "
              "게시하지 않는다.", file=sys.stderr)
        return 1
    if not d.get("axes_at") or not any(i.get("open_source") for i in d["items"]):
        print("생성 중단 — 우리가 지는 축(오픈소스·셀프호스팅)이 measured.json에 없다. "
              "`python3 measure.py --measure-axes`를 돌려라.", file=sys.stderr)
        return 1

    rank_of, err_of, cat_note, cat_runs = {}, {}, {}, {}
    for v in rk.values():
        cat_note[v["category"]] = v.get("note", "")
        cat_runs[v["category"]] = int(v.get("회차수") or 1)
        for t in v["top"]:
            rank_of[t["name"]] = (t["rank"], t.get("why", ""))
            if t.get("사실오류") is not None:
                err_of[t["name"]] = t["사실오류"]
    for _new, _old in RENAMED.items():
        if _old in rank_of and _new not in rank_of:
            rank_of[_new] = rank_of[_old]
        if _old in err_of and _new not in err_of:
            err_of[_new] = err_of[_old]
    graded_of: dict[str, list[tuple[int, str]]] = {}
    for v in rk.values():
        graded_of.setdefault(v["category"], []).extend(
            (t["rank"], t["name"]) for t in v["top"])

    items, _merged = dedupe_by_endpoint(d["items"])
    for it in items:
        s0 = src.get(it["name"]) or {}
        it.setdefault("website_url", s0.get("website_url"))
        r0 = (s0.get("remotes") or [{}])[0]
        it["addr_registered"] = bool(r0.get("url")) and r0.get("confidence") != "readme"
    rem = [r for r in items if r.get("remote")]
    live = [r for r in rem if r["remote"].get("reachable")]
    dead = [r for r in rem if not r["remote"].get("reachable")]
    off = [r for r in live if cls.get(r["name"]) and not cls[r["name"]]["is_data_provider"]]
    live = [r for r in live if r not in off]
    unmeasured = [r for r in live if not (r["remote"].get("tool_count") or 0)]
    live = [r for r in live if r not in unmeasured]
    inst = [r for r in items if not r.get("remote") and r.get("package")]
    cats_live = [c for c in CATS
                 if any(cls.get(r["name"], {}).get("category") == c for r in live)]

    site = Site(a.base, a.out, a.ext)
    today = dt.date.today()
    # 상세 페이지를 가지는 서버 = 우리가 **실제로 두드려 본** 것. 두드리지 않은 서버에
    # 페이지를 만들면 측정값 없는 페이지가 남의 이름으로 검색에 뜬다.
    probed = live + unmeasured + dead + off
    page_of, taken = {}, {}
    for r in sorted(probed, key=lambda x: x["name"]):
        s = slug(r["name"])
        if s in taken:
            raise SystemExit(f"생성 중단 — URL 조각 충돌: {taken[s]} vs {r['name']} → {s}")
        taken[s] = r["name"]
        page_of[r["name"]] = f"servers/{s}"
    cat_page = {c: f"category/{slug(CAT_EN.get(c, c))}" for c in cats_live}

    ctx = {"site": site, "items": items, "live": live, "dead": dead, "off": off, "rem": rem,
           "inst": inst, "unmeasured": unmeasured, "cls": cls, "rank_of": rank_of,
           "err_of": err_of, "cat_note": cat_note, "cat_runs": cat_runs,
           "graded_of": graded_of, "cats_live": cats_live, "page_of": page_of,
           "cat_page": cat_page, "dead_names": {r["name"] for r in dead}, "ts": ts,
           "today": today, "ts_ago": ago(ts, today), "axes_ts": d.get("axes_at"),
           "pkg_ts": d.get("repackaged_at"), "graded": graded_at()}
    site.date_footer = (
        f'가동 측정 {e(ts)} · 축 측정 {e(ctx["axes_ts"])}'
        + (f' · 패키지 축 {e(ctx["pkg_ts"])}' if ctx["pkg_ts"] else "")
        + (f' · 채점 원자료 최종 변경 {e(ctx["graded"])}(저장소 이력)' if ctx["graded"] else "")
        + f' · 이 페이지 생성 {today.isoformat()} — <strong>측정일은 잰 날이고 생성일과 '
          f'다르다</strong>')

    build_index(ctx)
    for c in cats_live:
        build_category(ctx, c)
    for r in probed:
        server_page(ctx, r)
    build_down(ctx)
    build_selfhosted(ctx)
    build_method(ctx)
    build_machine(ctx)
    try:
        key = pathlib.Path(a.indexnow_key_file).read_text(encoding="utf-8").strip()
    except OSError:
        key = ""
    if key:
        site.extra.append((f"{key}.txt", key + "\n"))
    site.write()
    print(f"site/ — 페이지 {len(site.pages)}개(서버 상세 {len(probed)}) · 분야 {len(cats_live)} · "
          f"부속 {len(site.extra)}개 · base {site.base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
