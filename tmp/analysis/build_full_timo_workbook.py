"""Build complete source-based worksheets without changing source questions."""
from pathlib import Path
from html import escape as h
from bs4 import BeautifulSoup
import ast,json,re
from collections import Counter

root=Path('output/html')
records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
tree=ast.parse(Path('tmp/analysis/complete_theory.py').read_text(encoding='utf-8'))
T=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='T' for t in n.targets)))
vocab={
'find':'tìm','calculate':'tính','value':'giá trị','sum':'tổng','difference':'hiệu','product':'tích','sequence':'dãy số','term':'số hạng','pattern':'quy luật','first':'đầu tiên','last':'cuối / tận cùng','digit':'chữ số','number':'số','greatest':'lớn nhất','smallest':'nhỏ nhất','even':'chẵn','odd':'lẻ','divisible':'chia hết','remainder':'số dư','factor':'thừa số / ước (theo ngữ cảnh)','multiple':'bội','perimeter':'chu vi','area':'diện tích','square':'hình vuông','rectangle':'hình chữ nhật','triangle':'tam giác','shaded':'được tô màu','unshaded':'không tô màu','length':'chiều dài','width':'chiều rộng','side':'cạnh','figure':'hình vẽ','identical':'giống hệt nhau','combined':'được ghép','cube':'hình lập phương','face':'mặt','edge':'cạnh','vertex':'đỉnh','vertices':'các đỉnh','ways':'cách','different':'khác nhau','at least':'ít nhất','at most':'nhiều nhất','how many':'có bao nhiêu','must':'phải / chắc chắn theo điều kiện','without':'không có / không được','right':'bên phải / vuông (theo ngữ cảnh)','left':'bên trái / còn lại (theo ngữ cảnh)','ago':'trước đây','later':'sau / nữa','now':'hiện nay','today':'hôm nay','tomorrow':'ngày mai','yesterday':'hôm qua','years':'năm','days':'ngày','hours':'giờ','minutes':'phút','operation':'phép toán','define':'định nghĩa','symbol':'ký hiệu','average':'trung bình','consecutive':'liên tiếp','total':'tổng cộng','remaining':'còn lại','increases':'tăng thêm','decreases':'giảm đi','both':'cả hai','each':'mỗi','all':'tất cả','least':'ít nhất / nhỏ nhất','maximum':'lớn nhất','minimum':'nhỏ nhất','path':'đường đi','routes':'các đường đi','steps':'bước / bậc','colours':'màu sắc','colors':'màu sắc'}
def page_name(rnd,exam):return f'timo-{rnd.lower()}-{exam}.html'
def crops(r,key):
    return ''.join(f'<a href="sources/TIMOK4.pdf#page={re.search(r"-(\d+)\.png$",p)[1]}" target="_blank" rel="noopener"><img class="source-crop" src="{p}" loading="lazy" alt="{h(r["label"])} — {"đề tiếng Anh gốc" if key=="question_images" else "lời giải gốc"}"></a>' for p in r[key])
def sources(r):return f'<p class="source">{h(r["label"])} · <a target="_blank" rel="noopener" href="sources/TIMOK4.pdf#page={r["page"]}">Đề: PDF {r["page"]} / trang in {r["printed_page"]}</a> · <a target="_blank" rel="noopener" href="sources/TIMOK4.pdf#page={r["solution_page"]}">Lời giải: PDF {r["solution_page"]} / trang in {r["solution_page"]-1}</a></p>'
def frame(title,body):return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h(title)}</title><link href="style.css" rel="stylesheet"></head><body><header><nav><a href="index.html">Buổi học</a><a href="timo-day-du.html">350 bài TIMO</a><a href="bai-hoc-toan-4.html">Bài học nền</a><a href="ly-thuyet-day-du.html">Tra cứu cách làm</a></nav><h1>{h(title)}</h1></header><main>{body}</main><script src="app.js"></script></body></html>'

for rnd in ('VL','QG'):
 for exam in range(1,8):
    subset=[r for r in records if r['round']==rnd and r['exam']==exam]
    title=f'TIMO {"vòng loại" if rnd=="VL" else "vòng quốc gia"} — Đề {exam} — đủ 25 câu'
    intro='<section class="card"><p>Đọc tiếng Anh trên ảnh gốc trước. Viết dữ kiện và điều cần tìm vào vở hoặc ô bài làm. Chỉ mở từng gợi ý khi cần; sau khi đối chiếu lời giải, che mẫu và tự giải lại.</p><p>Gợi ý được viết theo dạng toán của từng câu. Lời giải và hình trong phần đối chiếu giữ nguyên từ tài liệu nguồn; đây không phải 350 lời giải mới đã được kiểm chứng độc lập.</p>'
    if rnd=='VL' and exam==2:intro+='<p><b>Đề dành cho thi thử:</b> chưa đọc gợi ý hoặc lời giải trước buổi thi thử. <a href="thi-thu-timo.html">Mở phiên bản thi thử</a>.</p>'
    if rnd=='QG':intro+='<p>Vòng quốc gia có dạng nâng cao. Khi gặp kiến thức chưa học, mở mục lý thuyết tương ứng và học cùng người lớn trước khi tự làm.</p>'
    intro+='</section><div class="toolbar"><button onclick="printPack(false)">In bài tập</button> <button onclick="printPack(true)">In kèm hướng dẫn</button></div><nav class="lesson-links">'+''.join(f'<a href="#{r["id"]}">Câu {r["question"]}</a>' for r in subset)+'</nav>'
    body=[]
    for r in subset:
        recognition,steps,formulas,warning=T[r['category']]
        words=[f'<li><span lang="en">{h(en)}</span>: {h(vi)}</li>' for en,vi in vocab.items() if re.search(r'\b'+re.escape(en)+r'\b',r['source_text'],re.I)]
        vocabulary='<ul class="word-list">'+''.join(words)+'</ul>' if words else '<p>Đọc câu hỏi và ký hiệu trên ảnh gốc; dùng bản dịch trong ảnh để kiểm tra từ chưa hiểu.</p>'
        correction='<p class="note"><b>Lưu ý khi đối chiếu:</b> hình thuyền còn có 5 tam giác ở cột buồm. Tổng là 5 + 4 + 14 = 23. <a href="chua-timo.html#mock-20">Xem phần chữa đã bổ sung</a>.</p>' if r['id']=='VL-2-20' else ''
        body.append(f'''<article class="exercise full-timo" id="{r['id']}" data-category="{r['category']}"><span class="tag">{r['id']} · {h(r['category_name'])}</span><h2>Câu {r['question']}</h2>{sources(r)}<h3>1. Đọc đề tiếng Anh</h3>{crops(r,'question_images')}<details class="reading-help"><summary>Từ khóa để con đọc lại đề</summary>{vocabulary}<p><b>Yêu cầu bằng tiếng Việt:</b> {h(r['summary'])}</p><p>Ảnh gốc là căn cứ cho đầy đủ dữ kiện, hình và phương án.</p></details><h3>2. Con tự làm</h3><p>Con cần tìm gì? Dữ kiện nào giúp tìm? Vẽ hình, lập bảng hoặc viết phép tính; cuối cùng kiểm tra điều kiện của đề.</p><textarea aria-label="Bài làm {r['id']}" data-save="full-work-{r['id']}" placeholder="Con ghi cách nghĩ và lời giải ở đây, hoặc làm vào vở…"></textarea><div class="write-lines print-only"></div><details class="solution hint"><summary>Gợi ý 1 — nhận ra dạng toán</summary><p>{h(recognition)}</p><p>Đánh dấu dữ kiện trong câu này phù hợp với dấu hiệu trên. <a href="ly-thuyet-day-du.html#type-{r['category']}">Học lại cách làm của dạng này</a>.</p></details><details class="solution hint"><summary>Gợi ý 2 — bắt đầu một bước</summary><p>{h(steps[0])}</p><p>Con tự thực hiện bước này bằng số hoặc hình trong đề rồi dừng lại kiểm tra.</p></details><details class="solution hint"><summary>Gợi ý 3 — nối các bước và tự kiểm tra</summary><ol>{''.join('<li>'+h(x)+'</li>' for x in steps[1:])}</ol><p><b>Điểm cần kiểm tra:</b> {h(warning)}</p></details><details class="solution original-solution"><summary>3. Đối chiếu lời giải gốc sau khi đã thử</summary>{correction}{sources(r)}{crops(r,'solution_images')}<p>So từng bước với bài của con. Nếu khác đáp án, xác định bước đầu tiên khác nhau, sửa bước đó rồi giải lại khi đã che mẫu.</p></details><div class="status"><label>Kết quả: <select data-save="full-status-{r['id']}"><option>Chưa làm</option><option>Tự làm đúng và giải thích được</option><option>Đúng nhưng chưa giải thích được</option><option>Cần gợi ý</option><option>Sai — cần làm lại</option></select></label></div><label>Lỗi cần sửa / ngày làm lại:<input data-save="full-error-{r['id']}" aria-label="Lỗi và ngày làm lại {r['id']}" placeholder="Ví dụ: nhầm số dư; làm lại ngày…"></label><p><b>Kiểm tra hiểu:</b> con nói vì sao chọn cách làm này; tự làm lại không nhìn gợi ý.</p></article>''')
    (root/page_name(rnd,exam)).write_text(frame(title,intro+''.join(body)),encoding='utf-8')

groups=[]
for rnd in ('VL','QG'):
    cards=''.join(f'<article class="card"><h3><a href="{page_name(rnd,i)}">Đề {i} — 25 câu</a></h3><p>Đề tiếng Anh gốc · từ khóa · ô bài làm · 3 mức gợi ý · lời giải và trang PDF.</p></article>' for i in range(1,8))
    groups.append(f'<h2>{"Vòng loại — 175 câu" if rnd=="VL" else "Vòng quốc gia — 175 câu"}</h2><div class="grid">{cards}</div>')
categories=Counter(r['category'] for r in records)
by_type=[]
for category,n in categories.items():
    subset=[r for r in records if r['category']==category]
    by_type.append(f'<details class="card"><summary><b>{h(subset[0]["category_name"])} — {n} câu</b></summary><p><a href="ly-thuyet-day-du.html#type-{category}">Học cách làm</a></p><div class="lesson-links">'+''.join(f'<a href="{page_name(r["round"],r["exam"])}#{r["id"]}">{r["id"]}</a>' for r in subset)+'</div></details>')
landing='<section class="card"><p><b>Đủ 350 câu / 14 đề:</b> 175 câu vòng loại và 175 câu vòng quốc gia. Chọn theo đề hoặc theo dạng ở bên dưới; mỗi liên kết mở thẳng câu cần làm.</p><p>Đây là bộ bài tập đầy đủ để học dần. Trong lịch thi hiện tại, ưu tiên vòng loại và các lỗi của con; đề vòng loại 2 giữ cho thi thử. Không mở hết đáp án trước khi làm.</p><p><a href="#theo-dang">Chọn bài theo 50 dạng toán</a> · <a href="danh-muc-timo.html">Tra cứu danh mục và nguồn</a></p></section>'
(root/'timo-day-du.html').write_text(frame('Bộ bài tập TIMO đầy đủ — 350 câu',landing+''.join(groups)+'<h2 id="theo-dang">Chọn đúng dạng cần luyện</h2>'+''.join(by_type)),encoding='utf-8')

for name in ['index.html','bai-hoc-toan-4.html','danh-muc-timo.html','lo-trinh.html','ly-thuyet-day-du.html']:
    file=root/name;s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    s.main.insert(0,BeautifulSoup('<section class="card full-workbook-link"><h2><a href="timo-day-du.html">Mở toàn bộ 350 bài tập TIMO</a></h2><p>14 đề đầy đủ, có đề tiếng Anh gốc, phần tự làm, gợi ý và lời giải theo từng câu. Chọn theo đề hoặc dạng toán.</p></section>','html.parser'))
    if name=='danh-muc-timo.html':
        for r in records:
            node=s.find(id=r['id'])
            node.select_one('.catalog-body').insert(0,BeautifulSoup(f'<p><a href="{page_name(r["round"],r["exam"])}#{r["id"]}"><b>Làm câu này với gợi ý và ghi kết quả</b></a></p>','html.parser'))
    file.write_text(str(s),encoding='utf-8')
with (root/'style.css').open('a',encoding='utf-8') as f:f.write('\n.full-timo{scroll-margin-top:20px}.full-timo input{display:block;width:100%;padding:12px;font:inherit;border:1px solid #b6c8d7;border-radius:6px}.word-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:4px 20px}.reading-help{background:#eef4fb;padding:16px;margin:16px 0}.hint{border-left:4px solid #b98a35}.full-timo .source-crop{padding:0}.full-timo h2{margin-top:12px}@media print{.full-timo{break-before:page}.full-timo textarea,.full-timo input{display:none}.full-timo .reading-help{display:none}}\n')
plan=Path('output/Phan-tich-va-ke-hoach-on-TIMO.md')
with plan.open('a',encoding='utf-8') as f:f.write('\n## Bộ bài tập TIMO đầy đủ\n\n[Mở 350 câu TIMO](html/timo-day-du.html): 14 đề, mỗi đề đủ 25 câu, chia 175 câu vòng loại và 175 câu quốc gia. Mỗi câu có ảnh đề tiếng Anh gốc, từ khóa, ô tự làm, ba mức gợi ý theo dạng, ảnh lời giải nguồn, liên kết chính xác tới trang PDF và trạng thái làm bài. Có chỉ mục chọn theo 50 dạng. Hướng dẫn theo dạng không thay thế lời giải cụ thể; lời giải nguồn được giữ nguyên, chưa khẳng định đã giải kiểm chứng độc lập 350 câu.\n')
print('Built 14 complete worksheets, 350 exercises and 50-category index.')
