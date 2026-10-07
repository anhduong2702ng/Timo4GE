from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
import json, shutil
p=Path('output/html'); pages={f.name:BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser') for f in p.glob('*.html')}; errors=[]
for name,s in pages.items():
 ids=[x['id'] for x in s.find_all(id=True)]
 if len(ids)!=len(set(ids)):errors.append((name,'duplicate IDs'))
 for tag in s.find_all(['a','img','script','link']):
  v=tag.get('href') or tag.get('src')
  if not v:continue
  parts=v.split('#',1);dest=unquote(parts[0]);f=p/dest
  if dest and not f.exists():errors.append((name,'missing',v))
  if len(parts)>1 and dest.endswith('.html') and parts[1] not in [x['id'] for x in pages[dest].find_all(id=True)]:errors.append((name,'fragment',v))
bank=pages['toan-bo-de-cuong.html'];ids={x['id'] for x in bank.select('article.exercise')}
expected={f'TN{i}' for i in range(1,21)}|{f'TL{i}' for i in range(1,16)}|{f'TT{i}' for i in range(16,19)}
assert ids==expected
assert len(pages['thi-thu-timo.html'].select('select[data-save]'))==25
assert len(pages['chua-timo.html'].select('article.exercise'))==25
assert len(pages['theo-doi.html'].select('select[data-save]'))==56
for name in [f'{d:02}-10.html' for d in range(6,16)]:
 assert pages[name].select('section.theory') and pages[name].select('article.exercise')
assert not errors,errors
# Recalculate representative multi-step results, all x equations and the flawed source boat sum.
assert [2746*2+375,1353+2970/3,2246*4-725,9035-1655*5]==[5867,2343,8259,760]
assert 590+2590==3180 and int('2'+'590')==2590
assert 210*(210/3)*(9/3)/100==441
assert (4*55000+3*80000)*3/4==345000
assert (9+5)*2/2+2*4/2+1*5==23
print('PASS:',len(pages),'HTML pages; links/anchors valid;38midterm exercises;56checklist entries;25mock questions;daily theory/exercises present; representative math checked.')
shutil.make_archive('output/Bo-on-TIMO-va-giua-ki-HTML','zip',root_dir='output',base_dir='html')
print('ZIP created.')
