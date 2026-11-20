"""Split EQB Monitor bulletins into one entry per project (deterministic, no AI)."""
import json,re,sys
def clean(t):
    t=re.sub(r'[ \t\xa0]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t); return t
def date_of(t):
    m=re.search(r'EQB Monitor, (\w+ \d{1,2}, \d{4})',t); return m.group(1) if m else None
def entries(b):
    lines=[l.strip() for l in clean(b['text']).split('\n') if l.strip()]
    idx=[i-1 for i,l in enumerate(lines) if re.match(r'Location( \(city|:)',l) and i>0]
    out=[]
    for k,s in enumerate(idx):
        e=idx[k+1] if k+1<len(idx) else min(len(lines),s+12)
        block=lines[s:e]
        # stop at footer-ish lines
        cut=[j for j,l in enumerate(block) if re.match(r'(Submit a notice|Questions\?|EQB Monitor submission|Stay connected)',l)]
        if cut: block=block[:cut[0]]
        out.append({"title":block[0],"text":"\n".join(block)})
    return out
if __name__=="__main__":
    B=json.load(open(sys.argv[1]))
    allE=[]
    for b in B:
        d=date_of(clean(b['text']))
        for e in entries(b): allE.append({"volume":b['vol'],"date":d,"url":b['url'],**e})
    json.dump(allE,open(sys.argv[2],"w"),indent=1)
    print(len(B),"bulletins",len(allE),"entries")
