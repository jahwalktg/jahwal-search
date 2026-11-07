# -*- coding: utf-8 -*-
"""본문 추출 txt(쪽 경계 \f) → data/*.json
사용: py -X utf8 tools/make_data.py <txt> <key> <제목> <발행> <off> [잡음줄,잡음줄…]
  off = pdf쪽 − 인쇄쪽 (인쇄 1쪽이 pdf 37쪽이면 36)
  잡음줄 = 쪽마다 반복되는 머리말 글자(그 줄과 똑같으면 지움)
새해엔 새 PDF → jahwal-tool/scripts/pdf2txt.cjs 로 txt → 이 스크립트.
"""
import sys, json, re, os
txt, key, title, pub, off = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
noise = set(sys.argv[6].split(',')) if len(sys.argv) > 6 else set()
noise |= {'MINISTRY OF HEALTH AND WELFARE', 'Ministry of Health and Welfare'}
def roman(n):
    out=''; 
    for v,s in [(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: out+=s; n-=v
    return out
pages=[]
raw=open(txt,encoding='utf-8').read().split('\f')
for i,p in enumerate(raw):
    n=i+1
    lines=[]
    for l in p.split('\n'):
        s=l.strip()
        if not s: continue
        if s in noise: continue
        lines.append(re.sub(r'[ \t　]{2,}',' ',l.strip()))
    t='\n'.join(lines).strip()
    if not t: continue
    pr=n-off
    lab=str(pr) if pr>=1 else (roman(n-1) if n-1>=1 else '앞')
    if pr<1 and n<=5: lab='앞'
    pages.append({'n':n,'p':lab,'t':t})
out={'key':key,'title':title,'pub':pub,'off':off,'pages':pages}
dst=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data',key+'.json')
json.dump(out,open(dst,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(key, len(pages),'쪽', os.path.getsize(dst),'bytes')
