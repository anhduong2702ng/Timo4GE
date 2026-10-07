import json
from pathlib import Path
r=json.loads(Path('tmp/analysis/all-timo.json').read_text(encoding='utf-8'))
for x in r:
 if x['round']=='QG' and x['exam'] in [2,3]:
  t=x['source_text'].splitlines();text=' '.join(t)
  print(x['id']+' p'+str(x['page'])+': '+text[:450])
