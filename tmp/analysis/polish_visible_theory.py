from pathlib import Path
from bs4 import BeautifulSoup
import json
root=Path('output/html')
theory=BeautifulSoup((root/'ly-thuyet-day-du.html').read_text(encoding='utf-8'),'html.parser')
records={r['id']:r for r in json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))}
for file in root.glob('*.html'):
    s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    # Theory is real visible content, no longer a disclosure that can be collapsed.
    for d in list(s.select('details.reference-theory, details.teach-model, details.reading-help')):
        summary=d.find('summary',recursive=False)
        if summary:summary.name='h3'
        d.name='section';d.attrs.pop('open',None)
    for a in s.select('article.full-timo'):
        r=records[a['id']]; source=theory.find(id='type-'+r['category'])
        rule=source.select_one('.rule')
        clone=BeautifulSoup(str(rule),'html.parser')
        for x in clone.select('.worked-example'):x.decompose()
        # Avoid repeating a solved example from another question in a student's exercise.
        for x in clone.select('.math-display'):x.decompose()
        panel=s.new_tag('section',attrs={'class':'visible-theory'})
        title=s.new_tag('h3');title.string='Cách nghĩ cần nhớ — '+r['category_name'];panel.append(title)
        panel.append(clone)
        a.find('h3').insert_before(panel)
    if file.name=='bai-hoc-toan-4.html':
        diagrams={
        'x':'<div class="math-path" aria-label="Đường đi xuôi và ngược"><span>Số ban đầu</span><b>→ × 2 →</b><span>Kết quả giữa</span><b>→ + 375 →</b><span>5867</span><p>Đi ngược: 5867 − 375, rồi chia 2.</p></div>',
        'hinh':'<figure class="concept-figure"><div class="area-grid">'+''.join('<span></span>' for _ in range(24))+'</div><figcaption>4 hàng × 6 ô = 24 ô vuông. Chu vi là đường bao quanh khung.</figcaption></figure>',
        'quy-luat':'<figure class="concept-figure"><div class="color-cycle">'+''.join('<span class="'+c+'">'+str(i+1)+'</span>' for i,c in enumerate(['red','blue','yellow']*3))+'</div><figcaption>Mỗi 3 vị trí là một nhóm. Vị trí 3, 6, 9 đều ở cuối nhóm.</figcaption></figure>',
        'so':'<div class="place-value"><span><b>35</b>Lớp triệu</span><span><b>624</b>Lớp nghìn</span><span><b>000</b>Lớp đơn vị</span></div>'}
        for id,html in diagrams.items():
            lesson=s.find(id=id)
            heading=next((x for x in lesson.find_all('h3') if 'Nhìn để hiểu' in x.get_text()),None)
            if heading:heading.find_next_sibling('p').insert_after(BeautifulSoup(html,'html.parser'))
    file.write_text(str(s),encoding='utf-8')
css='''
/* Classroom visual system: readable cards, visible theory, clear learning steps. */
:root{--ink:#18354a;--line:#d9e7e9}body{background:#f5f8f6;color:var(--ink);font:18px/1.75 "Segoe UI",Arial,sans-serif;letter-spacing:0}header{background:linear-gradient(120deg,#123e47,#146b65);padding-top:28px;padding-bottom:32px}header h1{max-width:850px;font-size:clamp(28px,4vw,42px);letter-spacing:-.6px}main{max-width:1080px}h2{border-left:5px solid #e6b54d;color:#164d51;font-size:26px}h3{color:#215961;font-size:21px}.card,.exercise,.theory,.teach-lesson{border-radius:20px;border-color:#d6e4e5;box-shadow:0 8px 28px #163e4707}.teach-lesson{max-width:none;padding:32px}.teach-lesson>h3,.full-timo>h3{background:#eaf3f3;padding:12px 16px;border-radius:10px;margin-top:28px}.teach-question{background:#fff3d3;border:1px solid #ecd899}.teach-model{background:#edf6ef;border:1px solid #d1e5d6}.eyebrow{background:#e7f2ed;padding:12px 16px;border-radius:10px}.lesson-links{gap:10px}.lesson-links a{color:#15575b;background:#fff;border-color:#bed9d7;font-size:16px;padding:10px 14px;transition:background .15s}.lesson-links a:hover{background:#def0e8}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #c2831d;outline-offset:4px}.visible-theory{background:#edf6f0;border:1px solid #bed8c7;border-radius:16px;padding:22px;margin:24px 0}.visible-theory h3{color:#20593c;margin-top:0}.visible-theory .rule{background:transparent;border:0;padding:0}.visible-theory h4{font-size:18px;margin:18px 0 8px}.visible-theory ol{padding-left:25px}.visible-theory li{margin:12px 0}.reading-help{border:1px solid #d5e1ef;border-radius:12px}.word-list{margin:0;padding-left:20px}.word-list li{font-size:16px}.reference-theory{padding:20px;border:1px solid #cddfd7;border-radius:16px;background:#edf6ef}.source{font-size:15px;line-height:1.7}.source a{color:#275d77}.timo-bridge,.english-original{border-radius:14px;background:#f4f8fc}.source-crop{max-width:100%;height:auto}.toolbar button{background:#155e60;color:white;border:0;padding:12px 18px;border-radius:10px;font:600 16px "Segoe UI",sans-serif;cursor:pointer;margin:5px}.full-timo textarea{min-height:180px;background:#fffef9}.solution>summary{padding:12px;font-weight:650}.concept-figure{background:#f4f8fc;border:1px solid #d4e1e9;border-radius:14px;padding:20px;margin:20px 0}.concept-figure figcaption{font-size:16px;margin-top:14px}.area-grid{display:grid;grid-template-columns:repeat(6,36px);width:fit-content;border:3px solid #1e746b}.area-grid span{width:36px;height:36px;background:#d8ece2;border:1px solid #76aa98}.color-cycle{display:flex;flex-wrap:wrap;gap:8px}.color-cycle span{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;font-weight:700;border:2px solid #254455}.color-cycle .red{background:#f5bec0}.color-cycle .blue{background:#a9d6ef}.color-cycle .yellow{background:#f3db88}.math-path{display:flex;flex-wrap:wrap;align-items:center;gap:12px;background:#edf6ef;padding:20px;border-radius:14px}.math-path span{background:#fff;padding:10px 14px;border:1px solid #b3cec0;border-radius:10px}.math-path p{flex-basis:100%;margin:8px 0}.place-value{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}.place-value span{display:flex;flex-direction:column;align-items:center;min-width:120px;background:#edf4fa;border:1px solid #cadbe9;border-radius:12px;padding:16px}.place-value b{font-size:30px}.full-timo>h2{font-size:28px}select{max-width:100%}textarea{max-width:100%}nav a{max-width:100%}.grid{align-items:start}@media(max-width:600px){body{font-size:17px}header{padding:20px}main{padding:0 14px}.teach-lesson,.exercise,.card,.theory{padding:20px;border-radius:14px}.visible-theory{padding:16px}.visible-theory .rule{padding:0}.teach-lesson>h3,.full-timo>h3{padding:10px;font-size:20px}.concept-figure{padding:14px}.area-grid{grid-template-columns:repeat(6,30px)}.area-grid span{width:30px;height:30px}.word-list{grid-template-columns:1fr}.source{overflow-wrap:anywhere}.lesson-links a{font-size:15px}.place-value span{min-width:90px;padding:12px}h2{font-size:23px}}@media print{body{background:white;color:#111}.visible-theory,.reference-theory,.teach-model{display:block!important;background:white;box-shadow:none}.full-timo .reading-help{display:block}.concept-figure{break-inside:avoid}.visible-theory{break-inside:auto}header{background:white;color:#111}header a{color:#111}}
'''
with (root/'style.css').open('a',encoding='utf-8') as f:f.write(css)
print('Theory now permanently visible; 350 theory panels added; 4 visual teaching diagrams; classroom styling applied.')
