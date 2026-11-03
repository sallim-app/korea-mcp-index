import os,sys
D='/tmp/mcpidx-1103'; A='/data/apps/mcp-index-kr/answers'
skip=set(open(D+'/skip.txt').read().split())
why={'myfss':'모든 도구가 HTTP 401(토큰 필요)이라 1회차에서 멈췄다',
     'crossfin':'tools/call이 MCP 응답 대신 웹페이지(HTML)를 돌려줘 우리 호출기가 결과를 읽지 못했다(rc=3) — 1회차에서 멈췄다',
     'finbridge':'모든 도구가 HTTP 401(인증 필요)이라 1회차에서 멈췄다',
     'korea-finance-mcp':'tools/call 응답이 HTTP 청크 중간에서 끊겨(IncompleteRead) 우리 호출기가 읽지 못했다(rc=3) — 1회차에서 멈췄다',
     'open-proxy-mcp':'도구가 사용자 본인의 DART API 키를 요구해 키 없이는 답하지 않았다 — 1회차에서 멈췄다',
     'stockdrifts':'도구가 API 키(STOCKDRIFTS_API_KEY)를 요구해 키 없이는 답하지 않았다 — 2회차에서 멈췄다'}
n=0
for l in open(D+'/names.tsv'):
    c,name,slug,url,cur=l.rstrip('\n').split('\t')
    rs=[r for r in (1,2,3) if os.path.exists(f'{D}/runs/{slug}/r{r}.md')]
    if not rs: print('NO RUNS',slug); continue
    k=len(rs)
    alias=f' 지금 표기 이름은 `{cur}`(같은 주소의 같은 서버).' if cur!=name else ''
    if slug in skip:
        head=(f"# {name}\n\n> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 호출 주소 `{url}`.{alias}\n"
              f"> **측정하지 못했다** — {why.get(slug,'')}. 채점·순위에 넣지 않았다.\n")
    else:
        head=(f"# {name}\n\n> 2026-11-03 정규 월간 채점 회차 · 답변자 Haiku · 같은 질문을 서로 못 보는 독립 세션으로 "
              f"**{k}회** 물었다({'·'.join(map(str,rs))}회차). 호출 주소 `{url}`.{alias}\n")
    body="\n\n---\n\n".join(open(f'{D}/runs/{slug}/r{r}.md').read().strip() for r in rs)
    open(f'{A}/{slug}.md','w').write(head+"\n\n---\n\n"+body+"\n"); n+=1
print('wrote',n)
