import json,glob,sys,os
R='/data/apps/mcp-index-kr'; D='/tmp/mcpidx-1103'
cat=sys.argv[1]
old=json.load(open(f'{R}/grades/{cat}.json'))
new=[]
for f in sorted(glob.glob(f'{D}/grades/{cat}-[A-Z].json')):
    new+=json.load(open(f))['servers']
rank=json.load(open(f'{D}/grades/{cat}-RANK.json'))
names={s['server'] for s in new}
fix=[]; servers=[]
for s in new:
    p=s.pop('분야판정',None)
    if isinstance(p,dict):
        fix.append((s['server'],p['교정'],p['근거']))
    elif p=='측정불가':
        s['이번회차']='2026-11-03 회차에서 도구가 인증·결제·에이전트 프로필 같은 자격을 요구했다(무엇이었는지는 아래 _why에 있다) — 측정하지 못했으므로 점수를 매기지 않고 순위에서 뺐다.'
    servers.append(s)
carried=[]
for s in old['servers']:
    if s['server'] in names: continue
    s=dict(s)
    if s['server']=='kr.gronox/finbridge':
        s['이번회차']='2026-11-03 회차에도 1회차에서 전 도구가 HTTP 401(인증 필요)이라 측정하지 못했다 — 아래 점수·문장은 2026-10-01 회차 기록 그대로다.'
        servers.append(s); carried.append(s['server']); continue
    s['이번회차']=('2026-11-03 회차에서 다시 묻지 않았다 — 지난 채점 회차에 분야 교정·키 없이 측정 불가로 순위에서 빠진 서버라 '
        '같은 질문을 다시 던지지 않았다. 아래 점수·문장은 그 회차 기록 그대로다.')
    servers.append(s); carried.append(s['server'])
order=list(rank['권장순위'])
order+=[n for n,_,_ in fix if n not in order]
order+=[n for n in old.get('권장순위',[]) if n in carried and n not in order]
out={'category':cat,'grader':'opus','회차수':3,'servers':servers,
     '분야_총평':rank['분야_총평'],
     '분류_교정_제안':[f"{n} → {c} — {w}" for n,c,w in fix]+[x for x in old.get('분류_교정_제안',[]) if x.split(' → ')[0] in carried],
     '권장순위':order,'순위_근거':rank['순위_근거']}
json.dump(out,open(f'{R}/grades/{cat}.json','w'),ensure_ascii=False,indent=1)
json.dump(fix,open(f'{D}/fix-{cat}.json','w'),ensure_ascii=False)
print(cat,'servers',len(servers),'new',len(new),'carried',carried,'fix',[(n,c) for n,c,_ in fix])
print(' rank',rank['권장순위'])
