from pathlib import Path
from html import escape
from bs4 import BeautifulSoup
import re, runpy

# Rebuild once, then apply the visual system and semantic mathematical layout.
data=runpy.run_path('tmp/analysis/build_html.py')
runpy.run_path('tmp/analysis/polish_html.py')
EX=data['EX']; ROOT=Path('output/html')

def row(expr):
 tokens=re.findall(r'\d+(?:[ \u00a0]\d{3})*(?:/\d+)?|(?:mm|cm|dm|m)[²³]|[^\W\d_]+|[^\s]',expr)
 out=[]
 for index,token in enumerate(tokens):
  if re.fullmatch(r'\d+/\d+',token):
   a,b=token.split('/');out.append(f'<mfrac><mn>{a}</mn><mn>{b}</mn></mfrac>')
  elif token[-1:] in ['²','³']:
   out.append(f'<mspace width="0.25em"/><msup><mi mathvariant="normal">{token[:-1]}</mi><mn>{2 if token[-1]=="²" else 3}</mn></msup>')
  elif re.fullmatch(r'\d[\d \u00a0]*',token):
   n=token.replace(' ','').replace('\u00a0','');n=f'{int(n):,}'.replace(',','\u2009');out.append(f'<mn>{n}</mn>')
  elif token in '()[]':out.append(f'<mo lspace="0" rspace="0" stretchy="true">{token}</mo>')
  elif token in '+−-×÷:=<>≥≤⇒⊗':out.append(f'<mo lspace="0.25em" rspace="0.25em">{escape("−" if token=="-" else token)}</mo>')
  elif token in ['cm','mm','dm','kg','tạ','yến','tấn','phút','giây','đồng','lít','tuổi'] or (token=='m' and index>0 and tokens[index-1][0].isdigit()):out.append('<mspace width="0.25em"/><mtext>'+escape(token)+'</mtext>')
  elif token=='abc':out.append('<mover><mrow><mi>a</mi><mi>b</mi><mi>c</mi></mrow><mo>¯</mo></mover>')
  elif len(token)==1 and token.isalpha():out.append(f'<mi>{token}</mi>')
  else:out.append(f'<mtext>{escape(token)}</mtext><mspace width="0.25em"/>')
 return '<mrow>'+''.join(out)+'</mrow>'

def math(expr,aligned=False):
 expr=expr.strip().rstrip('.')
 if aligned and expr.count('=')>1:
  bits=expr.split('='); rows=[]
  for i,bit in enumerate(bits[1:]):
   rows.append('<mtr><mtd>'+ (row(bits[0]) if i==0 else '<mrow/>')+'</mtd><mtd><mo>=</mo></mtd><mtd>'+row(bit)+'</mtd></mtr>')
  inner='<mtable columnalign="right center left" columnspacing="0.6em" rowspacing="0.65em">'+''.join(rows)+'</mtable>'
 else:inner=row(expr)
 return '<div class="math-display"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'+inner+'</math></div>'

def rule(title,words,exprs=(),example=None):
 body=f'<div class="rule"><h4>{title}</h4><p>{words}</p>'
 for e in exprs:body+=math(e)
 if example:
  body+='<div class="worked-example"><p class="example-label">Ví dụ trong tài liệu</p>'+example+'</div>'
 return body+'</div>'

T={}
T['Biểu thức, tính nhanh và tìm x']=rule('1. Thứ tự thực hiện phép tính','Tính trong ngoặc trước. Sau đó nhân và chia, cuối cùng cộng và trừ. Các phép cùng mức thực hiện từ trái sang phải. Với biểu thức chứa chữ, thay giá trị của chữ trước khi tính.',example='<p>Đề cương giữa kì, câu 12: thay m bằng 2.</p>'+math('12 : (3 − 2) = 12 : 1 = 12',True))
T['Biểu thức, tính nhanh và tìm x']+=rule('2. Đặt thừa số chung','Tìm số xuất hiện trong từng tích và đưa số đó ra ngoài ngoặc. Một số đứng riêng được coi là tích của chính nó với 1.',('a × b + a × c = a × (b + c)','a × b − a × c = a × (b − c)'),'<p>Chuyên đề 1, bài 6a:</p>'+math('54 × 113 + 45 × 113 + 113 = 113 × (54 + 45 + 1) = 113 × 100 = 11 300',True))
T['Biểu thức, tính nhanh và tìm x']+=rule('3. Tổng dãy cách đều','Kiểm tra khoảng cách giữa hai số liên tiếp có cố định hay không. Đếm đủ cả số đầu và số cuối rồi mới tính tổng.',('Số số hạng = (số cuối − số đầu) : khoảng cách + 1','Tổng = (số đầu + số cuối) × số số hạng : 2'),'<p>TIMO đề 1, câu 7: dãy từ 2 đến 38, cách nhau 4 đơn vị.</p>'+math('(38 − 2) : 4 + 1 = 10')+math('(2 + 38) × 10 : 2 = 200'))
T['Biểu thức, tính nhanh và tìm x']+=rule('4. Ghép cặp và tìm x','Ghép cặp phải giữ nguyên dấu của từng số. Khi tìm x, xác định cả cụm chứa x đang là thành phần nào của phép tính. Cuối cùng thay kết quả vào đề để kiểm tra.',example='<p>Đề cương giữa kì, bài 6a:</p>'+math('x × 2 + 375 = 5 867')+math('x × 2 = 5 867 − 375 = 5 492',True)+math('x = 5 492 : 2 = 2 746',True))

T['Cấu tạo số, hàng/lớp và làm tròn']=rule('1. Giá trị chữ số','Giá trị của chữ số phụ thuộc vào hàng mà chữ số đó đứng. Mỗi lớp có ba hàng. Phân biệt chữ số với giá trị của chữ số.',('abc = 100 × a + 10 × b + c',),'<p>Đề cương giữa kì, câu 2: chữ số 5 trong số 35 624 000 ở hàng triệu.</p>'+math('5 × 1 000 000 = 5 000 000'))
T['Cấu tạo số, hàng/lớp và làm tròn']+=rule('2. So sánh và số liền sau','Số có nhiều chữ số hơn thì lớn hơn. Nếu cùng số chữ số, so sánh từ trái sang phải. Số liền sau hơn số đã cho một đơn vị. Số chẵn tận cùng bằng 0, 2, 4, 6 hoặc 8.',example='<p>Đề cương giữa kì, câu 6:</p>'+math('888 889 + 1 = 888 890'))
T['Cấu tạo số, hàng/lớp và làm tròn']+=rule('3. Làm tròn số','Xác định hàng cần làm tròn. Nhìn chữ số ngay bên phải: nhỏ hơn 5 thì giữ nguyên; từ 5 trở lên thì tăng 1. Các chữ số phía sau đổi thành 0.',example='<p>Đề cương giữa kì, bài 2b: làm tròn 751 243 đến hàng trăm nghìn. Chữ số hàng chục nghìn là 5, nên kết quả là:</p>'+math('800 000'))
T['Cấu tạo số, hàng/lớp và làm tròn']+=rule('4. Thêm một chữ số','Thêm chữ số d bên phải số N làm mọi chữ số của N dịch sang trái một hàng. Thêm một chữ số bên trái phải xét số chữ số của N; không dùng nhầm công thức thêm bên phải.',('Số mới = 10 × N + d','Số tăng thêm = 9 × N + d'),'<p>TIMO đề 7, câu 15: thêm chữ số 1 bên phải thì tăng 856.</p>'+math('9 × N + 1 = 856')+math('N = (856 − 1) : 9 = 95',True))

T['Chia hết, tận cùng, chu kì và quy luật']=rule('1. Dấu hiệu chia hết','Chia hết cho 2: chữ số tận cùng là 0, 2, 4, 6 hoặc 8. Chia hết cho 5: tận cùng là 0 hoặc 5. Chia hết cho 3 hoặc 9: xét tổng các chữ số. Có nhiều điều kiện thì phải thỏa đồng thời.',example='<p>TIMO đề 1, câu 14: số 2025A là số lẻ, chia hết cho 3. Tổng các chữ số là:</p>'+math('2 + 0 + 2 + 5 + A = 9 + A')+'<p>A có thể là 0, 3, 6, 9. Giữ các chữ số lẻ: 3 hoặc 9. Chữ số nhỏ nhất là 3.</p>')
T['Chia hết, tận cùng, chu kì và quy luật']+=rule('2. Chữ số tận cùng','Chỉ theo dõi chữ số hàng đơn vị của tích. Tích các thừa số 9 có tận cùng lặp theo nhóm 9, 1; thừa số 4 lặp theo nhóm 4, 6; thừa số 3 lặp theo nhóm 3, 9, 7, 1. Chia số thừa số cho độ dài chu kì; dư 0 lấy vị trí cuối nhóm.',example='<p>TIMO đề 1, câu 12: có 2025 thừa số 9. Số thừa số là số lẻ, nên chữ số tận cùng là 9.</p>')
T['Chia hết, tận cùng, chu kì và quy luật']+=rule('3. Chu kì ngày trong tuần','Mỗi tuần có 7 ngày. Bỏ các tuần trọn vẹn, chỉ tiến hoặc lùi số ngày bằng phần dư. Đọc rõ đề hỏi trước hay sau hôm nay.',example='<p>TIMO đề 1, câu 2:</p>'+math('44 = 6 × 7 + 2')+'<p>Lùi 44 ngày tương đương lùi 2 ngày. Từ thứ Sáu lùi 2 ngày là thứ Tư.</p>')
T['Chia hết, tận cùng, chu kì và quy luật']+=rule('4. Dãy có hiệu thay đổi','Nếu dãy không cách đều, lập dãy hiệu giữa các số liên tiếp. Tìm quy luật của dãy hiệu rồi viết tiếp dãy gốc.',example='<p>TIMO đề 1, câu 1: dãy 3, 4, 8, 15, 25 có các hiệu 1, 4, 7, 10. Hai hiệu tiếp theo là 13 và 16.</p>'+math('25 + 13 = 38')+math('38 + 16 = 54'))

T['Chu vi, diện tích và hình ghép']=rule('1. Hình vuông','Gọi cạnh hình vuông là a, chu vi là P và diện tích là S. Chu vi dùng đơn vị độ dài; diện tích dùng đơn vị vuông.',('P = 4 × a','a = P : 4','S = a × a'),'<p>Đề cương giữa kì, câu 14: chu vi 36 cm.</p><p>Cạnh hình vuông:</p>'+math('36 : 4 = 9 cm')+'<p>Diện tích hình vuông:</p>'+math('9 × 9 = 81 cm²'))
T['Chu vi, diện tích và hình ghép']+=rule('2. Hình chữ nhật','Gọi chiều dài là a và chiều rộng là b. Muốn tính diện tích phải biết cả hai kích thước và dùng cùng đơn vị.',('P = 2 × (a + b)','S = a × b'),'<p>Đề cương giữa kì, câu 17: rộng 4 m, dài gấp 3 lần rộng.</p><p>Chiều dài:</p>'+math('4 × 3 = 12 m')+'<p>Diện tích:</p>'+math('12 × 4 = 48 m²'))
T['Chu vi, diện tích và hình ghép']+=rule('3. Đổi đơn vị diện tích','Hai đơn vị diện tích liền nhau gấp hoặc kém nhau 100 lần. Đổi từ lớn sang nhỏ thì nhân; từ nhỏ sang lớn thì chia. Không dùng hệ số 10 của đơn vị độ dài.',('1 m² = 100 dm²','1 dm² = 100 cm²','1 cm² = 100 mm²'),'<p>Đề cương giữa kì, bài 5:</p>'+math('34 dm² 12 cm² = 34 × 100 cm² + 12 cm² = 3 412 cm²',True))
T['Chu vi, diện tích và hình ghép']+=rule('4. Hình ghép và cạnh nguyên','Đánh dấu cạnh bằng nhau rồi chia hình thành các phần quen thuộc, hoặc lấy hình bao trừ phần khuyết. Khi diện tích cố định và cạnh là số tự nhiên, liệt kê đủ cặp cạnh rồi so sánh chu vi. Không đoán chiều dài bằng mắt.',example='<p>TIMO đề 1, câu 18: diện tích 30. Các cặp cạnh là (1; 30), (2; 15), (3; 10), (5; 6). Cặp cuối cho chu vi nhỏ nhất:</p>'+math('2 × (5 + 6) = 22'))

T['Bài nhiều bước, tiền và sơ đồ đoạn thẳng']=rule('1. Tiền và đơn giá','Tính tiền từng loại trước rồi cộng. Muốn tìm đơn giá thì chia số tiền cho số lượng. Giảm một phần tư hóa đơn nghĩa là trừ đi một phần tư tổng tiền.',('Thành tiền = số lượng × đơn giá','Đơn giá = thành tiền : số lượng'),'<p>Đề cương giữa kì, bài 15b: tổng tiền 460 000 đồng.</p><p>Số tiền giảm:</p>'+math('460 000 : 4 = 115 000 đồng')+'<p>Số tiền phải trả:</p>'+math('460 000 − 115 000 = 345 000 đồng'))
T['Bài nhiều bước, tiền và sơ đồ đoạn thẳng']+=rule('2. Tổng và hiệu','Vẽ hai đoạn thẳng để thấy số lớn hơn số bé bao nhiêu. Nếu lấy hai lượng khác nhau mà còn bằng nhau, hiệu ban đầu bằng chênh lệch hai lượng lấy đi.',('Số lớn = (tổng + hiệu) : 2','Số bé = (tổng − hiệu) : 2'),'<p>Đề cương giữa kì, bài 13: bao thứ hai nhiều hơn bao thứ nhất:</p>'+math('22 − 5 = 17 kg'))
T['Bài nhiều bước, tiền và sơ đồ đoạn thẳng']+=rule('3. Tổng và tỉ; bài toán tuổi','Nếu A gấp k lần B, biểu diễn B bằng một phần, A bằng k phần. Chia tổng cho tổng số phần để tìm một phần. Hai người cùng tăng tuổi nên hiệu tuổi không đổi.',example='<p>TIMO đề 1, câu 15: tổng 18, Ashley gấp đôi Bell.</p>'+math('18 : (2 + 1) = 6')+'<p>Bell có 6 dây buộc tóc.</p>')
T['Bài nhiều bước, tiền và sơ đồ đoạn thẳng']+=rule('4. Bài nhiều bước và làm ngược','Bài sản lượng: tìm kích thước, tính diện tích, tìm lượng trên một đơn vị diện tích, tính tổng lượng rồi đổi đơn vị. Bài làm ngược: bắt đầu từ kết quả cuối và thực hiện phép ngược theo thứ tự ngược.',example='<p>TIMO đề 6, câu 3: từ kết quả 60, lần lượt nhân 10, cộng 79, chia 7 rồi trừ 4.</p>'+math('60 × 10 = 600')+math('600 + 79 = 679')+math('679 : 7 = 97')+math('97 − 4 = 93'))

T['Góc, khối lượng, thời gian và thế kỉ']=rule('1. Nhận biết và đếm góc','Góc nhọn nhỏ hơn 90°; góc vuông bằng 90°; góc tù lớn hơn 90° và nhỏ hơn 180°; góc bẹt bằng 180°. Đếm theo từng đỉnh. Mỗi cặp tia tạo một góc nhỏ hoặc góc bẹt; không đảo tên góc để đếm lần nữa. Chú ý điểm nằm trên một đoạn thẳng tạo hai tia đối nhau.')
T['Góc, khối lượng, thời gian và thế kỉ']+=rule('2. Đơn vị khối lượng','Đổi về cùng đơn vị trước khi cộng. Đơn vị hỗn hợp cần đổi từng phần rồi cộng lại.',('1 yến = 10 kg','1 tạ = 100 kg','1 tấn = 1 000 kg'),'<p>Đề cương giữa kì, bài 4:</p>'+math('3 tạ 50 kg = 3 × 100 kg + 50 kg = 350 kg',True))
T['Góc, khối lượng, thời gian và thế kỉ']+=rule('3. Giờ, phút, giây','Đổi thời gian theo hệ số 60. Khi đổi về đơn vị hỗn hợp, thương là đơn vị lớn và số dư là phần còn lại.',('1 giờ = 60 phút','1 phút = 60 giây'),'<p>Đề cương giữa kì, bài 5:</p>'+math('145 = 2 × 60 + 25')+'<p>Vậy 145 giây bằng 2 phút 25 giây.</p>'+math('1/4 giờ = 60 : 4 phút = 15 phút',True))
T['Góc, khối lượng, thời gian và thế kỉ']+=rule('4. Năm và thế kỉ','Một thế kỉ có 100 năm. Thế kỉ I từ năm 1 đến 100; thế kỉ XIII từ 1201 đến 1300. Năm 1226 thuộc thế kỉ XIII. Năm 1900 thuộc thế kỉ XIX, còn năm 1901 thuộc thế kỉ XX. Không cộng thêm một thế kỉ với năm kết thúc bằng 00.',('1 thế kỉ = 100 năm',))

T['Đếm hình, đếm số, chắc chắn và đường đi']=rule('1. Đếm số theo từng hàng','Hàng đầu của một số không được bằng 0. Đọc rõ chữ số có được lặp lại hay không. Nếu các lựa chọn độc lập, nhân số cách chọn từng hàng.',example='<p>TIMO đề 1, câu 22: hàng chục có 4 cách (1, 2, 3, 4); hàng đơn vị có 3 cách (0, 2, 4).</p>'+math('4 × 3 = 12')+'<p>Có 12 số thỏa mãn.</p>')
T['Đếm hình, đếm số, chắc chắn và đường đi']+=rule('2. Đếm bội và đếm hình','Đếm bội bằng cách tìm số đầu, số cuối và khoảng cách. Đếm hình chữ nhật chứa một ô: chọn đường trên, dưới, trái, phải rồi nhân số cách; chỉ dùng khi các cạnh liên tục.',example='<p>TIMO đề 1, câu 23: các số hai chữ số chia hết cho 3 chạy từ 12 đến 99.</p>'+math('(99 − 12) : 3 + 1 = 30'))
T['Đếm hình, đếm số, chắc chắn và đường đi']+=rule('3. Trường hợp bất lợi nhất','Từ “chắc chắn” yêu cầu xét tình huống lấy các vật không mong muốn trước. Tính mức vẫn có thể chưa đạt yêu cầu, rồi lấy thêm đủ để buộc yêu cầu xảy ra.',example='<p>TIMO đề 1, câu 21: có thể lấy hết 9 lá xanh và 10 lá vàng trước, sau đó cần 4 lá đỏ.</p>'+math('9 + 10 + 4 = 23')+'<p>Phải lấy ít nhất 23 lá.</p>')
T['Đếm hình, đếm số, chắc chắn và đường đi']+=rule('4. Đường đi và bậc thang','Ghi 1 cách ở điểm xuất phát. Tại mỗi nút, cộng số cách từ những nút có đường nối đi tới nó. Đường không có thì không cộng. Với bước dài 1 hoặc 2 bậc, số cách đến một bậc bằng tổng số cách đến hai bậc trước; bậc hỏng có 0 cách.')

# Find whole arithmetic expressions, including parentheses. Keep prose outside math.
operand=r'(?:\(?\s*)*(?:\d+(?:\s+\d{3})*|[aAbBcCdDxXmMNPS])(?:\s*\)?)*'
pattern=re.compile(r'(?<![A-Za-zÀ-ỹ0-9])'+operand+r'(?:\s*[+−×:=⇒]\s*'+operand+r')+(?:\s*(?:mm²|cm²|dm²|m²|kg|cm|m|tạ|yến|tấn|phút|giây|đồng|lít|tuổi))?(?![A-Za-zÀ-ỹ0-9])')
def content(text):
 # Keep inline markup on final answers, but transform each text node only.
 sp=BeautifulSoup(text,'html.parser')
 for node in list(sp.find_all(string=True)):
  value=str(node)
  value=re.sub(r'(?<=\d)(?=[A-Za-zÀ-ỹ])',' ',value)
  value=re.sub(r'(?<=[²³])(?=\d)',' ',value)
  value=re.sub(r'(?<=[,;])(?=\S)',' ',value)
  cursor=0;pieces=[]
  for m in pattern.finditer(value):
   if value[cursor:m.start()]:pieces.append(escape(value[cursor:m.start()]))
   pieces.append(math(m.group(),True));cursor=m.end()
  if not pieces:
   node.replace_with(value)
   continue
  if cursor<len(value):pieces.append(escape(value[cursor:]))
  new=BeautifulSoup(''.join(pieces),'html.parser')
  for child in list(new.contents):node.insert_before(child)
  node.extract()
 return str(sp)

for file in ROOT.glob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for section in soup.select('section.theory'):
  title=section.h3.get_text()
  if title not in T:continue
  for child in list(section.contents):
   if getattr(child,'name',None)=='h3' or (getattr(child,'name',None)=='p' and 'source' in child.get('class',[])):continue
   child.extract()
  for child in list(BeautifulSoup(T[title],'html.parser').contents):section.append(child)
 for article in soup.select('article.exercise'):
  k=article.get('id','')
  if k in EX:
   e=EX[k];prompt=article.select_one('.prompt')
   if prompt:
    prompt.clear();lab=soup.new_tag('span',attrs={'class':'prompt-label'});lab.string='ĐỀ BÀI';prompt.append(lab)
    # Put expressions on their own lines only; ordinary quantities remain in prose.
    for child in list(BeautifulSoup(content(e['q']),'html.parser').contents):prompt.append(child)
   sol=article.select_one('details.solution')
   if sol:
    old=sol.find('ol')
    if old:old.decompose()
    box=soup.new_tag('div',attrs={'class':'solution-flow'})
    for segment in re.split(r'<br\s*/?>',e['sol']):
     para=soup.new_tag('div',attrs={'class':'solution-step'})
     for child in list(BeautifulSoup(content(segment),'html.parser').contents):para.append(child)
     box.append(para)
    sol.append(box)
  elif k.startswith('mock-'):
   for para in article.find_all('p',recursive=False):
    if 'source' in para.get('class',[]):continue
    new=soup.new_tag('div',attrs={'class':'solution-step'})
    for child in list(BeautifulSoup(content(para.decode_contents()),'html.parser').contents):new.append(child)
    para.replace_with(new)
 for sol in soup.select('.solution-flow'):
  for bold in sol.find_all('b'):
   bold['class']=['final-result']
  for text in list(sol.find_all(string=True)):
   if text.parent.name in ['div'] and str(text).strip() in ['.',';','⇒']:text.extract()
 file.write_text(str(soup),encoding='utf-8')

extra='''
/* Mathematical typography: prose and expressions have separate reading lines. */
math{font-family:"Cambria Math","STIX Two Math",serif;font-size:1.22em;line-height:1.7;color:#1c314d} .math-display{display:block;overflow-x:auto;text-align:center;padding:14px 16px;margin:14px 0;background:#f8faff;border:1px solid #e2e8f2;border-radius:7px;white-space:normal}.math-display math{margin:auto}.solution-step{padding:14px 4px;border-bottom:1px solid #d9e8df;line-height:1.95}.solution-step:last-child{border:0}.solution-step .math-display{background:white;border-color:#caddd0}.solution-flow b{font-weight:800}.rule h4{margin:0 0 12px;font-size:20px;color:#194f9e}.worked-example{border-top:1px dashed #bdcfe4;margin-top:18px;padding-top:12px}.example-label{color:#6a4c98;font-weight:800;font-size:15px}.prompt .math-display{background:white;text-align:left}.prompt .math-display math{margin:0 auto}.rule p{margin:12px 0}.rule{padding:22px 25px}.rule .math-display{background:#edf6f2;border-color:#bfd9cb}.rule .math-display math{color:#165443}.worked-example .math-display{background:white}.formula-list{display:none}@media print{math{font-size:1.1em}.math-display{padding:8px;overflow:visible;break-inside:avoid}.solution-step{break-inside:avoid}.rule{padding:14px}}
'''
with (ROOT/'style.css').open('a',encoding='utf-8') as f:f.write(extra)
with (ROOT/'style.css').open('a',encoding='utf-8') as f:f.write('''
.math-display{overflow:visible;padding:20px 16px;min-height:62px}math{line-height:normal}.final-result{display:block!important;width:fit-content;max-width:100%;margin:18px auto!important;padding:9px 18px!important}.final-result .math-display{padding:4px;margin:0;border:0;background:transparent}.solution-step{line-height:2}@media(max-width:600px){.math-display{overflow-x:auto;overflow-y:hidden;padding-top:24px;padding-bottom:24px}}@media print{.math-display{min-height:0;padding:12px}}
''')
print('Semantic MathML added; theory rewritten as prose/formula/example blocks; exercise expressions separated.')
