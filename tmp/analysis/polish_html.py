from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Doctype
import re

ROOT=Path('output/html')
FORMULAS={
'Biểu thức, tính nhanh và tìm x':['a × b + a × c = a × (b + c)','Tổng dãy = (số đầu + số cuối) × số số hạng : 2','Số số hạng = (số cuối − số đầu) : khoảng cách + 1'],
'Cấu tạo số, hàng/lớp và làm tròn':['Số mới khi thêm d bên phải = 10 × số cũ + d','Chữ số bên phải ≥ 5 → tăng 1 ở hàng làm tròn'],
'Chia hết, tận cùng, chu kì và quy luật':['Chia hết cho 3 hoặc 9 → xét tổng các chữ số','Chia số vị trí cho độ dài chu kì → xét phần dư'],
'Chu vi, diện tích và hình ghép':['Hình vuông: P = 4 × a   •   S = a × a','Hình chữ nhật: P = 2 × (a + b)   •   S = a × b','1 m² = 100 dm² = 10 000 cm²'],
'Bài nhiều bước, tiền và sơ đồ đoạn thẳng':['Số lớn = (tổng + hiệu) : 2','Số bé = (tổng − hiệu) : 2','Thành tiền = số lượng × đơn giá'],
'Góc, khối lượng, thời gian và thế kỉ':['1 tấn = 10 tạ = 1 000 kg   •   1 yến = 10 kg','1 giờ = 60 phút   •   1 phút = 60 giây','1 thế kỉ = 100 năm'],
'Đếm hình, đếm số, chắc chắn và đường đi':['Số cách = số cách từ các vị trí đi tới nó','Chắc chắn → xét trường hợp bất lợi nhất']}

CSS=r'''
@import url('');
:root{--ink:#20314d;--blue:#225ec8;--teal:#08796e;--purple:#7044ad;--orange:#a95707;--line:#dbe4ef}
*{box-sizing:border-box}body{margin:0;background:#f3f6fc;color:var(--ink);font:18px/1.85 "Segoe UI",Arial,sans-serif;letter-spacing:.12px}header{background:linear-gradient(115deg,#183658,#245878);color:white;padding:36px max(24px,calc((100vw - 1040px)/2))}header a{color:#ecf5ff}header h1{font-size:34px;line-height:1.35;margin:20px 0 10px;font-weight:800}header p{color:#dcecff;font-size:17px}nav{display:flex;flex-wrap:wrap;gap:10px}nav a{padding:6px 13px;border:1px solid #7596ad;border-radius:9px;text-decoration:none;font-size:15px}main{max-width:1040px;margin:24px auto;padding:0 24px}h2{font-size:27px;line-height:1.4;color:#183e66;border-left:7px solid #3187c5;padding:8px 16px;margin:38px 0 22px}h3{font-size:23px;line-height:1.5;margin:12px 0 18px;color:#173c63}a{color:#245da5;text-underline-offset:4px}p{margin:16px 0}b,strong{font-weight:800;color:#163d6a}.card,.exercise,.theory{background:#fff;border:1px solid var(--line);border-radius:16px;padding:28px;margin:24px 0;box-shadow:0 4px 18px #20314d08}.theory{border:2px solid #89b4e7;background:#f8fbff;padding:26px}.theory>h3{color:#194f9e;border-bottom:2px solid #c5d9f1;padding-bottom:14px;font-size:25px}.rule{background:white;border:1px solid #d1e0f1;border-left:5px solid #5b8ed5;border-radius:10px;padding:18px 22px;margin:18px 0}.rule-title{display:block;color:#184e9d;font-size:20px;font-weight:800;margin-bottom:10px}.rule p{margin:8px 0}.formula-list{display:grid;gap:10px;margin:20px 0 25px}.formula{background:#e4f3ec;border:1px solid #a4d3be;border-left:5px solid var(--teal);border-radius:9px;padding:15px 20px;color:#075e55;font-weight:800;font-size:20px;line-height:1.65}.formula small{display:block;font-size:13px;letter-spacing:1px;color:#347461;font-weight:700}.source{font-size:14px;line-height:1.6;color:#57708d;margin:12px 0 20px}.source a{color:#57708d}.tag{display:inline-block;background:#e9e2fa;color:#5f3892;border:1px solid #cdbbea;font-size:14px;font-weight:700;border-radius:7px;padding:6px 12px}.exercise{border-left:6px solid #8d6bc4}.exercise>h3{margin-top:16px}.prompt{background:#f5f0fc;border:1px solid #e2d6f5;border-radius:10px;padding:18px 22px;font-size:20px;font-weight:600;line-height:1.9;margin:20px 0}.prompt-label{display:block;color:#7044ad;font-weight:800;font-size:13px;letter-spacing:1px;margin-bottom:8px}.work-label{font-size:14px;font-weight:700;color:#607590;margin:20px 0 8px}.note{background:#fff5df;border:1px solid #e9c785;border-left:6px solid #d38c26;border-radius:10px;padding:20px 24px;line-height:1.9}.note b{color:#88530a}.attention{background:#fff0d4;padding:1px 5px;border-radius:4px;color:#8a4b06;font-weight:750}details{margin:22px 0 10px;border-top:1px solid #dde5ee;padding-top:18px}summary{cursor:pointer;font-size:18px;font-weight:800;color:var(--teal);padding:7px 0}details.solution[open]{background:#f0faf5;border:1px solid #b6d8c4;border-radius:10px;padding:18px 22px}ol.steps{padding-left:30px;margin:18px 0}ol.steps li{padding:7px 8px 12px;line-height:1.9;border-bottom:1px dashed #c7ddd1;margin-bottom:9px}ol.steps li:last-child{border:0}ol.steps li::marker{font-weight:800;color:#08796e}details.solution b{display:inline-block;background:#c9ecd9;border:1px solid #94ceb0;border-radius:6px;padding:2px 8px;color:#085c39;font-size:20px}textarea{width:100%;min-height:130px;border:1px solid #bdcddd;border-radius:9px;font:17px/1.8 "Segoe UI",Arial,sans-serif;padding:14px;background:#fcfdff;color:var(--ink)}textarea:focus{outline:3px solid #c3defb}.status{margin-top:20px;padding:12px 0;border-top:1px dashed #dbe4ef;font-size:15px;color:#536b86}button,select{font:15px/1.6 "Segoe UI",Arial,sans-serif;border:1px solid #abc0d5;border-radius:8px;padding:10px 14px;background:white;color:#204971;cursor:pointer}button:hover{background:#e8f1fd;border-color:#5685c1}.toolbar{display:flex;flex-wrap:wrap;gap:9px;position:sticky;top:0;z-index:3;padding:13px 0;background:#f3f6fcf5;border-bottom:1px solid #dde5ef}.toolbar button:first-child{background:#245daf;color:white;border-color:#245daf}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px}.grid .card{margin:0;border-top:5px solid #5f93cc}.card h3 a{text-decoration:none}.card p{font-size:16px;line-height:1.85}table{width:100%;border-collapse:separate;border-spacing:0;background:white;border:1px solid var(--line);border-radius:10px;overflow:hidden}th,td{padding:15px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#e8eff9;color:#214b7c;font-size:16px}tr:nth-child(even) td{background:#f8faff}td{font-size:16px}img{max-width:100%;height:auto;border-radius:6px}.figure{display:block;max-height:440px;width:auto;margin:24px auto;border:1px solid #dae3ec;padding:12px;background:white}.print-only{display:none}.write-lines{height:95px;background:repeating-linear-gradient(white,white 29px,#d7dfe3 30px)}footer{max-width:1040px;margin:30px auto;padding:24px;font-size:14px;color:#61768e;line-height:1.8;border-top:1px solid #d8e3ee}@media(max-width:600px){body{font-size:17px}header{padding:24px}header h1{font-size:27px}main{padding:0 14px}.card,.exercise,.theory{padding:20px}.rule{padding:16px}.formula,.prompt{font-size:18px}.toolbar{position:static}td,th{padding:10px}h2{font-size:23px}}
@media print{@page{size:A4;margin:16mm}body{background:white;font-size:12pt;color:#15273a;-webkit-print-color-adjust:exact;print-color-adjust:exact}header{padding:0 0 10px;background:white;color:#173c63}header h1{font-size:22pt}header p{color:#345271}nav,.toolbar,button,.status,textarea,.no-print{display:none}main{max-width:none;padding:0;margin:0}h2{font-size:17pt;margin-top:22px}.theory,.exercise,.card{box-shadow:none;padding:15px;border-radius:8px}.rule,.formula{break-inside:avoid}.theory{break-inside:auto}.exercise{break-inside:avoid}.formula,.prompt{font-size:13pt}.rule-title,h3{font-size:14pt}.source{font-size:9pt}.print-only{display:block}.answers-hidden details.solution{display:none}.source-page{break-before:page}img{max-height:245mm}.figure{max-height:85mm}a{color:inherit;text-decoration:none}details.solution b{font-size:13pt}footer{font-size:9pt}}
'''
(ROOT/'style.css').write_text(CSS.replace("@import url('');\n",''),encoding='utf-8')

def tidy(text):
 text=re.sub(r'(?<=[²³])(?=\d)',' ',text)
 text=re.sub(r'(?<=\d)(?=[A-Za-zÀ-ỹ])',' ',text)
 text=re.sub(r'(?<=[A-Za-zÀ-ỹ])(?=\d)',' ',text)
 text=re.sub(r'\s*([×÷=→⇒+−])\s*',r' \1 ',text)
 text=re.sub(r'(?<=\d)\s*:\s*(?=\d)', ' : ', text)
 text=re.sub(r'(?<=[,;])(?=\S)',' ',text)
 return re.sub(r' {2,}',' ',text)

for file in ROOT.glob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for node in list(soup.find_all(string=True)):
  if isinstance(node,Doctype):continue
  if node.parent.name in ['script','style','title'] or node.parent.name=='a':continue
  node.replace_with(tidy(str(node)))
 for theory in soup.select('section.theory'):
  title=theory.h3.get_text()
  if title in FORMULAS:
   box=soup.new_tag('div',attrs={'class':'formula-list'})
   for formula in FORMULAS[title]:
    row=soup.new_tag('div',attrs={'class':'formula'});label=soup.new_tag('small');label.string='CÔNG THỨC / QUY TẮC';row.append(label);row.append(NavigableString(formula));box.append(row)
   theory.select_one('.source').insert_after(box)
  for para in list(theory.find_all('p',recursive=False)):
   if 'source' in para.get('class',[]):continue
   rule=soup.new_tag('div',attrs={'class':'rule'})
   first=para.find('b')
   if first:
    head=soup.new_tag('span',attrs={'class':'rule-title'});head.string=first.get_text().rstrip(':');first.decompose();rule.append(head)
   para.replace_with(rule);rule.append(para)
 for ex in soup.select('article.exercise'):
  solution=ex.select_one('details.solution')
  if solution:
   paragraphs=solution.find_all('p',recursive=False)
   for para in paragraphs:
    fragments=re.split(r'<br\s*/?>|(?<=\.)\s+(?=[A-ZÀ-Ỹ])',para.decode_contents())
    steps=soup.new_tag('ol',attrs={'class':'steps'})
    for frag in fragments:
     if not BeautifulSoup(frag,'html.parser').get_text().strip():continue
     li=soup.new_tag('li');parsed=BeautifulSoup(frag,'html.parser')
     for child in list(parsed.contents):li.append(child)
     steps.append(li)
    para.replace_with(steps)
  prompt=next((p for p in ex.find_all('p',recursive=False) if 'source' not in p.get('class',[])),None)
  if prompt:
   prompt['class']=['prompt'];lab=soup.new_tag('span',attrs={'class':'prompt-label'});lab.string='ĐỀ BÀI';prompt.insert(0,lab)
  area=ex.find('textarea')
  if area:
   lab=soup.new_tag('div',attrs={'class':'work-label'});lab.string='BÀI LÀM CỦA CON';area.insert_before(lab)
 for text in list(soup.find_all(string=True)):
  if isinstance(text,Doctype):continue
  if text.parent.name in ['script','style','a','title','summary']:continue
  if 'Không ' in str(text) or 'Đừng ' in str(text):
   chunks=re.split(r'((?:Không |Đừng )[^.!?]+[.!?]?)',str(text))
   if len(chunks)>1:
    for ch in chunks:
     if ch.startswith(('Không ','Đừng ')):
      mark=soup.new_tag('mark',attrs={'class':'attention'});mark.string=ch;text.insert_before(mark)
     else:text.insert_before(NavigableString(ch))
    text.extract()
 file.write_text(str(soup),encoding='utf-8')
print('Redesigned all16pages: rule boxes, formula callouts, numbered solutions, spacing, responsive/print styles.')
