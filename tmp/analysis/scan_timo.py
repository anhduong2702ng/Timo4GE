from pathlib import Path
import fitz,re,json
d=fitz.open('inputdata/TIMOK4.pdf')
RANGES={'VL':[(6,10),(11,15),(16,20),(21,24),(25,28),(29,32),(33,37)],'QG':[(38,41),(42,44),(45,47),(48,50),(51,54),(55,57),(58,60)]}
SOL={'VL':[(61,65),(66,70),(71,74),(75,78),(79,83),(84,88),(89,94)],'QG':[(95,100),(101,106),(107,111),(112,116),(117,121),(122,126),(127,131)]}
records=[];report=[]
def split_pages(start,end):
 items=[]
 expected=1
 for page in range(start,end+1):
  text=d[page-1].get_text()
  matches=list(re.finditer(r'(?m)^\s*(\d{1,2})\.[ \t]*(.*)$',text))
  for j,m in enumerate(matches):
   n=int(m.group(1))
   if n!=expected:continue
   expected+=1
   endpos=matches[j+1].start() if j+1<len(matches) else len(text)
   # Next actual numbered question, excluding numeric fragments from equations.
   following=next((z for z in matches[j+1:] if int(z.group(1))==n+1),None)
   endpos=following.start() if following else len(text)
   content=text[m.end(1)+1:endpos].strip()
   content=re.sub(r'(?m)^.*(?:KỲ THI OLYMPIC|BỘ ĐỀ ÔN THI|FERMAT Education).*$', '', content)
   content=re.sub(r'(?m)^(Logical [Tt]hinking|Arithmetic|Number [Tt]heory|Geometry|Combinatorics).*$', '',content).strip()
   items.append((n,page,content))
 return items
for rnd,ranges in RANGES.items():
 for no,(a,b) in enumerate(ranges,1):
  items=split_pages(a,b)
  assert [x[0] for x in items]==list(range(1,26)),(rnd,no,[x[0] for x in items])
  si=split_pages(*SOL[rnd][no-1]);smap={n:(p,t) for n,p,t in si}
  report.append(f'\n=== {rnd} DE {no} ===')
  for n,page,text in items:
   vi=[]
   for line in text.splitlines():
    line=line.strip()
    if re.search('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]',line) and not re.match(r'^[A-D][. ]',line):vi.append(line)
   desc=' '.join(vi) or ' '.join(text.split())[:220]
   sp,st=smap.get(n,(None,''))
   rec=dict(id=f'{rnd}-{no}-{n}',round=rnd,exam=no,question=n,page=page,printed_page=page-1,source_text=text,summary=desc,solution_page=sp,solution_text=st)
   records.append(rec);report.append(f'{n:02d} PDF{page} SOL{sp}: {desc}')
Path('tmp/analysis/all-timo.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
Path('tmp/analysis/all-timo-summary.txt').write_text('\n'.join(report),encoding='utf-8')
print('Extracted:',len(records),'questions; solutions located:',sum(x['solution_page'] is not None for x in records))
