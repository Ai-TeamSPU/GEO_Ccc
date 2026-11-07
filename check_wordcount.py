import re, sys
from pythainlp.tokenize import word_tokenize
txt = open(sys.argv[1], encoding='utf-8').read()
pages = re.split(r'<!-- PAGE: (\S+) -->', txt)
rows=[]
for i in range(1, len(pages), 2):
    page, body = pages[i], pages[i+1]
    secs = re.split(r'\n## ', body)
    for s in secs[1:]:
        head, *rest = s.split('\n', 1)
        para = ''
        for line in (rest[0] if rest else '').split('\n'):
            l=line.strip()
            if not l:
                if para: break
                continue
            if l.startswith(('|','[รอของจริง','**')) and not para: continue
            if re.match(r'^\d+\.|^- ', l) and not para: continue
            para += l+' '
        para = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', para)
        toks=[t for t in word_tokenize(para, engine='newmm') if t.strip() and not re.fullmatch(r'[\W_]+', t)]
        n=len(toks)
        rows.append((page, head[:50], n, 'OK' if 40<=n<=60 else 'FIX'))
for r in rows: print(*r, sep=' | ')
print('FIX count:', sum(1 for r in rows if r[3]=='FIX'), '/', len(rows))
