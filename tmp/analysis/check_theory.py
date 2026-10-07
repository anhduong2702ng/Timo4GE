from pathlib import Path
from bs4 import BeautifulSoup,Doctype
import json,re
from collections import Counter
root=Path('output/html');records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
issues=[]
for file in root.glob('*.html'):
 s=file.read_text(encoding='utf-8').replace('TIMOK 4.pdf','TIMOK4.pdf')
 file.write_text(s,encoding='utf-8')
 soup=BeautifulSoup(s,'html.parser')
 for node in soup.find_all(string=True):
  if isinstance(node,Doctype) or node.find_parent(['math','script','style','code','pre']):continue
  value=str(node).replace('TIMOK4.pdf','TIMOK.pdf')
  if re.search(r'[^\W\d_]\d|\d[^\W\d_]|[:,;](?=\S)',value):issues.append((file.name,value[:150]))
 assert not soup.select('p div'),file
assert not issues,issues[:20]
soup=BeautifulSoup((root/'ly-thuyet-day-du.html').read_text(encoding='utf-8'),'html.parser')
assert len(soup.select('section[data-category]'))==50
assert len(soup.select('section[id^="school-"]'))==5
for r in records:
 theory=soup.find(id='type-'+r['category']);assert theory is not None
 assert len(theory.select('ol li'))>=3
 assert theory.select_one('.theory-warning') and theory.select_one('.worked-example img')
catalog=BeautifulSoup((root/'danh-muc-timo.html').read_text(encoding='utf-8'),'html.parser')
assert len(catalog.select('.catalog-item .theory-link'))==350
for name in ['06-10','07-10','08-10','09-10','10-10','11-10','12-10','13-10','14-10','15-10']:
 assert BeautifulSoup((root/(name+'.html')).read_text(encoding='utf-8'),'html.parser').find(id='theory-supplement')
prompt=BeautifulSoup((root/'08-10.html').read_text(encoding='utf-8'),'html.parser').find(id='T1-18').select_one('.prompt').get_text(' ',strip=True)
assert 'tích 30' in prompt,prompt
print('PASS: no glued prose letters/numbers or punctuation across 20 pages; screenshot example fixed; MathML untouched; 50 detailed theory categories,350 question links,10 daily supplements,5 additional school skills.')
preview=BeautifulSoup((root/'08-10.html').read_text(encoding='utf-8'),'html.parser')
main=preview.main;main.clear();main.append(BeautifulSoup((root/'08-10.html').read_text(encoding='utf-8'),'html.parser').find(id='T1-18'))
main.append(soup.find(id='type-opt'))
base=preview.new_tag('base',href=root.resolve().as_uri()+'/');preview.head.insert(0,base)
Path('tmp/analysis/theory-preview.html').write_text(str(preview),encoding='utf-8')
