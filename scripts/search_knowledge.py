"""Simple proof-of-data keyword retriever. Requires Python 3 standard library only.

Not a substitute for a production vector/BM25 retrieval service.
"""
import json,re,sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
  'data/onet/occupation_profiles.jsonl',
  'data/bls/occupational_outlook_2025_2035.jsonl',
  'data/pbs/lfs_2024_25_facts.jsonl',
  'data/wef/future_jobs_2025_facts.jsonl',
  'data/anthropic/occupation_ai_exposure.jsonl',
]
STOP = {'and','the','of','in','to','an','a','for','is','what','are','do','does','on','me','tell','about','how'}
def words(s):
 return {w for w in re.findall(r'[a-z0-9]+',s.lower()) if len(w)>2 and w not in STOP}
def find(query,limit=5):
 term=words(query);hits=[]
 for name in SOURCES:
  with (ROOT/name).open(encoding='utf8') as fh:
   for line in fh:
    doc=json.loads(line)
    lead=' '.join(str(doc.get(k,'')) for k in ('title','indicator','finding','description'))
    content=' '.join(str(doc.get(k,'')) for k in ('country','detail','tasks','essential_skills','knowledge','bls_outlook'))
    score=7*len(term & words(lead)) + len(term & words(content))
    q=' '.join(query.lower().split())
    title=str(doc.get('title','')).lower().strip()
    indicator=str(doc.get('indicator','')).lower().strip()
    if q == title: score += 60
    elif title and title in q: score += 30
    if 'unemployment' in term and ('comparison' not in term and 'methodology' not in term):
     if doc.get('id') == 'pbs:unemployment_2024_25': score += 22
     if doc.get('id') == 'pbs:comparability_13th_icls': score -= 12
    if score:hits.append((score,name,doc))
 for score,name,doc in sorted(hits,key=lambda r:-r[0])[:limit]:
  print(json.dumps({'score':score,'file':name,'record':doc},ensure_ascii=False,indent=2))
if __name__=='__main__':
 if len(sys.argv)<2:raise SystemExit('Usage: python scripts/search_knowledge.py "your question"')
 find(' '.join(sys.argv[1:]))
