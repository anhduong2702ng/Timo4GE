from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as h
import json,re

root=Path('output/html')
records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
data={r['id']:r for r in records}
def source(r,solution=False):
    page=r['solution_page'] if solution else r['page']
    return f'sources/TIMOK4.pdf#page={page}'
def images(r,solution=False):
    key='solution_images' if solution else 'question_images'
    return ''.join(f'<a href="{source(r,solution)}" target="_blank" rel="noopener" title="Mở đúng trang PDF {x.rsplit("-",1)[-1].split(".")[0]}"><img class="source-crop" loading="lazy" src="{x}" alt="{h(r["label"])} — {"lời giải" if solution else "đề tiếng Anh gốc"}"></a>' if not solution else f'<a href="sources/TIMOK4.pdf#page={x.rsplit("-",1)[-1].split(".")[0]}" target="_blank" rel="noopener"><img class="source-crop" loading="lazy" src="{x}" alt="{h(r["label"])} — lời giải gốc"></a>' for x in r[key])
def links(r):
    return f'<p class="source">{h(r["label"])} · <a href="{source(r)}" target="_blank" rel="noopener">Đề gốc: trang PDF {r["page"]} (trang in {r["printed_page"]})</a> · <a href="{source(r,True)}" target="_blank" rel="noopener">Lời giải: trang PDF {r["solution_page"]} (trang in {r["solution_page"]-1})</a></p>'

selected={
'tinh':('VL-1-8','Calculate = tính; dấu cộng/trừ phải đi cùng tích của nó.','Con chỉ ra số xuất hiện ở cả ba tích. Có bao nhiêu nhóm 45 được thêm vào và bớt đi?','45 × (15 + 17 − 12) = 45 × 20 = 900. Chọn A. Phải giữ dấu trừ trước 12.'),
'x':('VL-6-3','adds = cộng; multiples (cách dùng trong bản gốc) = nhân; minuses = trừ; divides by = chia cho; this year = năm nay.','Viết đường đi của tuổi bà bằng đúng thứ tự trong câu tiếng Anh. Bắt đầu từ 60 và đi ngược; chưa chọn đáp án ngay.','60 × 10 = 600; 600 + 79 = 679; 679 : 7 = 97; 97 − 4 = 93 tuổi. Thử: (93 + 4) × 7 = 679; trừ 79 được 600; chia 10 được 60. Chọn D.'),
'so':('VL-6-5','tens digit = chữ số hàng chục; hundreds digit = chữ số hàng trăm; wrong sum = tổng sai; correct sum = tổng đúng.','Lập hai dòng: viết nhầm 4 thành 8 ở hàng chục làm tăng bao nhiêu? Viết nhầm 6 thành 2 ở hàng trăm làm giảm bao nhiêu?','Số A bị tăng 40; số B bị giảm 400. Tổng sai ít hơn tổng đúng 360. Tổng đúng = 7328 − 40 + 400 = 7688. Chọn B.'),
'chu-so':('VL-7-15','2-digit number = số có hai chữ số; to the right = bên phải; increases 856 = tăng thêm 856.','Thử viết thêm 1 vào bên phải 23: 231 = 10 × 23 + 1. Số mới gồm 10 lần số cũ và thêm 1, nên phần tăng gồm mấy lần số cũ và thêm 1?','Phần tăng là 9 lần số cũ cộng 1. Bớt 1 khỏi 856, còn 855 là 9 lần số cũ. Số cũ = 855 : 9 = 95. Thử 951 − 95 = 856. Chọn A.'),
'hinh':('VL-1-17','perimeter = chu vi; area = diện tích; combined = ghép; total area = tổng diện tích; rectangles = các hình chữ nhật.','Chỉ vào hình vuông lớn và nhỏ trên hình gốc. Hai hình chữ nhật chiếm phần nào? Con cần tính cạnh hay lấy luôn chu vi làm cạnh?','Cạnh lớn 24 : 4 = 6 cm, diện tích 36 cm². Cạnh nhỏ 16 : 4 = 4 cm, diện tích 16 cm². Hai hình chữ nhật phủ phần còn lại: 36 − 16 = 20 cm². Chọn B.'),
'loi-van':('VL-6-2','currently / now = hiện nay; years later = năm nữa; the sum = tổng; the same as = bằng.','Sau 4 năm bố có tuổi bằng mẹ sau 7 năm. Mẹ cần thêm nhiều hơn bố 3 năm để đạt cùng tuổi, vậy ai lớn hơn hiện nay? Vẽ hai đoạn có hiệu 3.','Bố hơn mẹ 7 − 4 = 3 tuổi. Bớt phần hơn khỏi tổng: 79 − 3 = 76; tuổi mẹ = 76 : 2 = 38. Bố 41. Thử 41 + 4 = 38 + 7 = 45. Chọn A.'),
'don-vi':('VL-1-2','today = hôm nay; days ago = ngày trước; day of the week = thứ trong tuần.','Gạch dưới ago để nhớ đi lùi. Bỏ các tuần đầy đủ, rồi đếm lùi số ngày còn lại. Không đổi ngày theo hệ 10 hoặc 100.','44 : 7 = 6 dư 2. Lùi 6 tuần vẫn là thứ Sáu; lùi thêm 2 ngày: thứ Năm rồi thứ Tư (Wednesday). Chọn A.'),
'quy-luat':('VL-1-4','pattern = quy luật; squares = hình vuông; the first 50 figures = 50 hình đầu tiên.','Khoanh một nhóm lặp trong hình gốc. Đề hỏi số hình vuông, không hỏi hình ở vị trí thứ 50. Phần dư có chứa hình vuông không?','50 : 3 = 16 dư 2. Mỗi nhóm đầy đủ có 1 hình vuông; hai hình còn lại có thêm 1 hình vuông. Tổng 16 + 1 = 17. Chọn B.'),
'dem':('VL-1-22','2-digit = có hai chữ số; even = chẵn; both digits smaller than 5 = cả hai chữ số nhỏ hơn 5.','Viết các lựa chọn cho hàng chục và đơn vị thành hai dòng. Đề có yêu cầu hai chữ số khác nhau không? Hàng chục có thể bằng 0 không?','Hàng chục: 1, 2, 3, 4 (4 cách); đơn vị: 0, 2, 4 (3 cách). Đề không cấm lặp. Có 4 × 3 = 12 số. Chọn B.')}

soup=BeautifulSoup((root/'bai-hoc-toan-4.html').read_text(encoding='utf-8'),'html.parser')
for id,(rid,vocab,prompt,answer) in selected.items():
    r=data[rid]; lesson=soup.find(id=id)
    heading=next(x for x in lesson.find_all('h3') if x.get_text().startswith('5.'))
    following=heading.find_next_sibling('p')
    following.replace_with(BeautifulSoup(f'''<div class="timo-bridge"><h4>TIMO — đọc đề tiếng Anh gốc</h4>{links(r)}<p>Đọc phần tiếng Anh trước, khoanh dữ kiện và câu hỏi. Nếu chưa hiểu một từ, xem từ khóa dưới đây rồi đọc lại. Ảnh gốc giữ cả phương án, ký hiệu và hình vẽ; bản dịch tiếng Việt có sẵn trong tài liệu.</p>{images(r)}<p><b>Từ khóa:</b> {vocab}</p><p><b>Con thử trước:</b> {prompt}</p><details class="solution"><summary>Hướng dẫn sau khi con đã thử</summary><p>{answer}</p>{links(r)}<details><summary>Đối chiếu lời giải gốc</summary>{images(r,True)}</details></details></div>''','html.parser'))
toc=soup.select_one('.lesson-links')
extra=[
('chia-het','Lý thuyết số: phối hợp điều kiện','VL-1-11','greatest = lớn nhất; 3-digit = có ba chữ số; even = chẵn; divisible by 3 = chia hết cho 3.','Con bắt đầu từ số chẵn lớn nhất có ba chữ số. Kiểm tra tổng chữ số; nếu không chia hết cho 3, giảm đi 2 để vẫn giữ số chẵn.','998 có tổng chữ số 26 nên không chia hết cho 3. Số chẵn ngay trước là 996, tổng chữ số 24 nên chia hết cho 3. Đây là số lớn nhất đạt cả hai điều kiện. Chọn C.'),
('phep-moi','Phép toán mới: đọc định nghĩa trước','VL-1-13','Define = định nghĩa; operation symbol = ký hiệu phép toán; find the value = tìm giá trị.','Ký hiệu trong đề có quy tắc riêng. Con đọc công thức trên ảnh; đánh dấu a và b, rồi thay a bằng 9, b bằng 5 vào mọi vị trí.','9 × 5 + 5 × (9 − 3) + 2 = 45 + 30 + 2 = 77. Chọn B. Ký hiệu mới không tự động là phép nhân; phải dùng định nghĩa.'),
('tan-cung','Chữ số tận cùng: theo dõi một chữ số','VL-1-12','last digit = chữ số tận cùng; 2025 numbers 9 = có 2025 thừa số đều bằng 9.','Thử các tích có 1, 2, 3, 4 thừa số 9. Chỉ ghi chữ số tận cùng để tìm chu kì.','9 có tận cùng 9; 9 × 9 có tận cùng 1; nhân thêm 9 có tận cùng 9; tiếp tục có tận cùng 1. Số thừa số lẻ cho tận cùng 9; chẵn cho tận cùng 1. 2025 lẻ nên đáp án là 9 (D).')]
for id,title,rid,vocab,prompt,answer in extra:
    r=data[rid]
    toc.append(BeautifulSoup(f'<a href="#{id}">{title}</a>','html.parser'))
    soup.main.append(BeautifulSoup(f'<section class="teach-lesson" id="{id}"><h2>{title}</h2><p>Học sau khi con đã chắc phép tính và cấu tạo số. Mỗi lần chọn một câu.</p>{links(r)}<h3>Đọc đề tiếng Anh</h3>{images(r)}<p><b>Từ khóa:</b> {vocab}</p><h3>Con nghĩ và làm thử</h3><p>{prompt}</p><details class="solution"><summary>Xem cách làm sau khi thử</summary><p>{answer}</p>{links(r)}{images(r,True)}</details><p><b>Kiểm tra hiểu:</b> che lời giải, con nhắc lại điều kiện cần kiểm tra hoặc quy luật vừa tìm; rồi tự giải lại.</p></section>','html.parser'))
(root/'bai-hoc-toan-4.html').write_text(str(soup),encoding='utf-8')

# Every selected TIMO exercise shows the authoritative English source, not only a Vietnamese rewrite.
count=0
for file in root.glob('*.html'):
    if file.name=='bai-hoc-toan-4.html':continue
    s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser'); changed=False
    for a in s.select('article.exercise'):
        match=re.fullmatch(r'T(\d+)-(\d+)',a.get('id',''))
        mock=re.fullmatch(r'mock-(\d+)',a.get('id',''))
        rid=f'VL-{match[1]}-{match[2]}' if match else f'VL-2-{mock[1]}' if mock else None
        if not rid:continue
        r=data[rid]
        if not a.select_one('.english-original'):
            block=BeautifulSoup(f'<div class="english-original"><h4>Đề TIMO tiếng Anh gốc</h4>{links(r)}{images(r)}<p>Con đọc tiếng Anh và xác định yêu cầu trước. Phần diễn giải tiếng Việt bên dưới giúp kiểm tra cách hiểu.</p></div>','html.parser')
            target=a.select_one('.prompt')
            if target:target.insert_before(block)
            else:a.insert(2,block)
            solution=a.select_one('details.solution')
            if solution:solution.append(BeautifulSoup(links(r),'html.parser'))
            changed=True;count+=1
    # Make original images clickable, preserving the exact page even across split-page questions.
    for img in list(s.select('img[src]')):
        match=re.search(r'timo-catalog/(?:VL|QG)-\d+-[qs]-\d+-(\d+)\.png$',img['src'])
        if match and img.parent.name!='a':
            a=s.new_tag('a',href=f'sources/TIMOK4.pdf#page={match[1]}',target='_blank',rel='noopener')
            img.wrap(a);changed=True
    if changed:file.write_text(str(s),encoding='utf-8')

# Keep dense references secondary, and make the missing number-theory/operation lessons reachable by date.
for day in ('06','07','10','13'):
    file=root/f'{day}-10.html';s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    ids=['phep-moi'] if day=='06' else ['chia-het','tan-cung'] if day=='07' else ['chia-het','phep-moi','tan-cung']
    s.select_one('.teaching-start').append(BeautifulSoup('<p>TIMO bổ sung khi đã xong bài chính: '+' · '.join(f'<a href="bai-hoc-toan-4.html#{id}">{next(x[1] for x in extra if x[0]==id)}</a>' for id in ids)+'. Chọn theo lỗi, không bắt học hết trong buổi.</p>','html.parser'))
    file.write_text(str(s),encoding='utf-8')
with (root/'style.css').open('a',encoding='utf-8') as f:f.write('\n.timo-bridge,.english-original{padding:18px;border:1px solid #bfd3e5;background:#f8fbff;margin:20px 0}.timo-bridge h4,.english-original h4{font-size:20px;margin:0 0 12px}.timo-bridge .source-crop,.english-original .source-crop{padding:0}.source a{display:inline} @media(max-width:600px){.timo-bridge,.english-original{padding:10px}}\n')
plan=Path('output/Phan-tich-va-ke-hoach-on-TIMO.md')
text=plan.read_text(encoding='utf-8').replace('9 bài học có hướng dẫn','12 bài học có hướng dẫn')
text+='\n## Cập nhật TIMO: tiếng Anh và trang nguồn\n\nBài học đã có 12 câu TIMO vòng loại cụ thể, mỗi câu giữ ảnh đề tiếng Anh gốc, từ khóa, câu hỏi dẫn dắt và lời giải tiếng Việt. Ba mục bổ sung là chia hết, phép toán mới và chữ số tận cùng. Các câu TIMO trong trang ngày học/chữa thi thử cũng có ảnh đề gốc. Nhấp ảnh hoặc liên kết đề/lời giải để mở đúng trang TIMOK4.pdf; số trang dùng vị trí trong PDF tính từ 1, không dùng số trang in. Đề 2 tiếp tục dành riêng cho thi thử.\n'
plan.write_text(text,encoding='utf-8')
print(f'Updated 12 English-source teaching examples and {count} exercise instances; original crop images link to exact PDF pages.')
