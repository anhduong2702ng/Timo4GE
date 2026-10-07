from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageChops
import json,re
root=Path('output/html');records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
blank=[]
for r in records:
 for key in ['question_images','solution_images']:
  keep=[]
  for p in r[key]:
   im=Image.open(root/p).convert('L')
   if im.point(lambda x:255 if x<210 else 0).getbbox():keep.append(p)
   else:blank.append(p)
  assert keep,(r['id'],key)
  r[key]=keep
(root/'danh-muc-timo.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['lo-trinh.html','danh-muc-timo.html']:
 p=root/name;soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for img in soup.find_all('img'):
  if img.get('src') in blank:img.decompose()
 for node in list(soup.find_all(string=True)):
  if node.parent.name in ['script','style']:continue
  s=str(node)
  if node.parent==soup and s.strip()=='html':node.extract();continue
  s=re.sub(r'([:,;])(?=\S)',r'\1 ',s)
  s=re.sub(r'(\d)(?=[^\W\d_])',r'\1 ',s)
  s=re.sub(r'([^\W\d_])(?=\d)',r'\1 ',s)
  node.replace_with(s)
 for script in soup.find_all('script'):
  if script.string:script.string=script.string.replace('tổng350câu','tổng 350 câu')
 p.write_text('<!DOCTYPE html>\n'+str(soup),encoding='utf-8')
print('Removed',len(blank),'empty continuation crops from display. Kept all 350 question/solution pairs.')
