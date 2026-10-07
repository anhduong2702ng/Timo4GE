from pathlib import Path
from bs4 import BeautifulSoup
import json
root=Path('output/html');s=BeautifulSoup((root/'06-10.html').read_text(encoding='utf-8'),'html.parser')
q=s.select_one('#T1-7 .prompt')
assert len(q.find_all('math'))==1
assert q.find('math').get_text().replace('\u2009','')=='2+6+10+…+30+34+38',q.find('math').get_text()
for file in root.glob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 assert not soup.select('p div.math-display'),file.name
 assert not soup.select('b div.math-display'),file.name
 for art in soup.select('article.exercise'):
  if art.select_one('.prompt'):
   assert art.select_one('.solution-flow'),(file.name,art.get('id'))
 # No leaked single multiplication symbol inside an identifier/text token.
 for t in soup.find_all(['mi','mtext']):
  assert '×' not in t.get_text(),(file.name,t)
blocks=[]
for ident in ['T1-7','T1-8','TL6']:
 art=s.select_one('#'+ident)
 art.select_one('details.solution')['open']=''
 blocks.append(str(art))
preview='<!doctype html><html lang="vi"><head><meta charset="utf-8"><base href="'+root.resolve().as_uri()+'/"><link rel="stylesheet" href="style.css"></head><body><main><h1>Kiểm tra biểu thức nguyên vẹn</h1>'+''.join(blocks)+'</main></body></html>'
Path('tmp/analysis/exact-preview.html').write_text(preview,encoding='utf-8')
print('PASS: complete sum in one formula; valid block nesting; explicit solutions on all exercise pages; math operators not swallowed into words.')
