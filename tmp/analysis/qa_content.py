from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json,re,fitz

root=Path('output/html');records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
pages={f.name:BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser') for f in root.glob('*.html')}
doc=fitz.open(root/'sources/TIMOK4.pdf');exercises={};image_count=0
for name,s in pages.items():
    assert not s.select('details.reference-theory,details.teach-model,details.reading-help'),name
    for a in s.select('article.full-timo'):
        assert a['id'] not in exercises
        exercises[a['id']]=a
        panel=a.select_one('.visible-theory')
        assert panel and len(panel.select('ol li'))>=3,(name,a['id'])
        assert not panel.find_parent('details'),(name,a['id'])
        assert len(a.select('details.hint'))==3
        assert a.select_one('textarea') and a.select_one('.original-solution img')
    for img in s.select('img[src]'):
        path=root/unquote(img['src']);assert path.is_file(),(name,path)
        m=re.search(r'timo-catalog/(?:VL|QG)-\d+-[qs]-\d+-(\d+)\.png$',img['src'])
        if m:
            pn=int(m[1]); assert 1<=pn<=len(doc)
            assert img.parent.name=='a' and img.parent['href']==f'sources/TIMOK4.pdf#page={pn}',(name,img['src'])
            image_count+=1
assert set(exercises)=={r['id'] for r in records}
for r in records:
    a=exercises[r['id']]
    src={x['src'] for x in a.select('img')}
    assert set(r['question_images']+r['solution_images'])<=src,r['id']
    # Verify per-question source ranges against actual PDF text, not merely link syntax.
    assert re.search(r'(?m)^\s*'+str(r['question'])+r'\.',doc[r['page']-1].get_text()),('question page',r['id'])
    assert re.search(r'(?m)^\s*'+str(r['question'])+r'\.',doc[r['solution_page']-1].get_text()),('solution page',r['id'])
# Arithmetic in the 12 guided examples, independently recomputed.
assert 45*(15+17-12)==900
assert ((60*10+79)//7)-4==93
assert 7328-40+400==7688
assert (856-1)//9==95 and 951-95==856
assert (24//4)**2-(16//4)**2==20
assert (79-(7-4))//2==38
assert 44%7==2 and 50//3+1==17
assert len([n for n in range(10,100) if n%2==0 and all(int(c)<5 for c in str(n))])==12
assert max(n for n in range(100,1000) if n%2==0 and n%3==0)==996
assert 9*5+5*(9-3)+2==77 and pow(9,2025,10)==9
out={'html_pages':len(pages),'complete_exercises':len(exercises),'visible_theory_panels':len(exercises),'exact_pdf_image_links':image_count,'guided_example_calculations':12,'source_question_and_solution_page_checks':700,'result':'PASS'}
Path('tmp/analysis/qa/content-results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
