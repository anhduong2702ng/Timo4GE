from pathlib import Path
from html import escape as h
from urllib.parse import quote
from collections import Counter,defaultdict
import fitz,json,re,csv,shutil

ROOT=Path('output/html');AS=ROOT/'assets/timo-catalog';AS.mkdir(parents=True,exist_ok=True)
d=fitz.open('inputdata/TIMOK4.pdf')
records=json.loads(Path('tmp/analysis/all-timo.json').read_text(encoding='utf-8'))
RANGES={'VL':[(6,10),(11,15),(16,20),(21,24),(25,28),(29,32),(33,37)],'QG':[(38,41),(42,44),(45,47),(48,50),(51,54),(55,57),(58,60)]}
SOL={'VL':[(61,65),(66,70),(71,74),(75,78),(79,83),(84,88),(89,94)],'QG':[(95,100),(101,106),(107,111),(112,116),(117,121),(122,126),(127,131)]}
# Categories assigned after reading all14papers, not solely by section position.
SEQ={
('VL',1):'seq calendar reverse cycle assume basic sum factor pair crypt div last op div ratio grid area opt view area worst form multiples stairs path',
('VL',2):'cycle calendar assume seq reverse basic sum factor pair crypt div last op ratio div grid area opt view area worst form multiples stairs path',
('VL',3):'cycle calendar assume seq reverse basic sum factor pair crypt div last op ratio div grid area opt view area form worst multiples stairs path',
('VL',4):'cycle calendar assume seq reverse basic sum factor pair crypt div last op ratio div grid geo view opt area form worst multiples stairs path',
('VL',5):'cycle calendar assume seq reverse basic sum factor pair basic div last op ratio div grid geo opt solid area multiples form color form path',
('VL',6):'cycle age reverse calendar place sum factor basic basic factor div last divisors ratio multiples grid geo geo solid regions ratio path form form optimize',
('VL',7):'basic calendar seq table table factor basic sum crypt geosum ratio union div op place area surface geo grid geo worst stairs concat form table',
('QG',1):'average calendar cuts table assume factor basic basic sum pair divisors div op ratio union grid grid opt view solid digitprod form worst form path',
('QG',2):'average age reverse calendar cuts factor geosum basic sum sum last div div op consecutive grid opt opt pyth segments stairs form path worst eliminate',
('QG',3):'cuts seq calendar reverse assume sum geosum basic basic factor ratio div consecutive last div geo geo opt solid grid digitprod worst ratio form permutation',
('QG',4):'cuts assume seq calendar reverse sum geosum basic basic factor productratio multiples consecutive last div segments grid geo opt grid digitprod worst form form permutation',
('QG',5):'calendar cycle assume reverse pattern basic factor basic sum geosum consecutive op last div remainder pyth opt view pattern grid worst form digitprod optimize path',
('QG',6):'calendar assume cuts reverse pattern basic basic factor sum geosum div last op ratio divisors grid triangles opt geo opt pigeon optimize ratio stairs form',
('QG',7):'seq cycle cuts calendar reverse basic pair sum factor basic div last op productratio div grid pyth opt geo triangles optimize ratio work assume form',
}
META={
'seq':('Dãy có quy luật / dãy hiệu','Dãy số PDF1; CĐ1 PDF1','Đặt dãy hiệu; chỉ dùng công thức cách đều khi hiệu không đổi.','Nền tảng TIMO'),
'calendar':('Lịch, thứ trong tuần, tháng/năm','Giữa kì TN8,10,11; TL5','Tính số ngày/tháng chênh lệch rồi xét chu kì7/12; phân biệt tiến và lùi.','Nối một phần'),
'reverse':('Làm ngược / tìm số ban đầu','Giữa kì TL6; CĐ1 PDF3','Đi từ kết quả cuối, đảo phép toán và đảo thứ tự.','Nối trực tiếp'),
'cycle':('Chu kì hình / chữ / vị trí','Cấu tạo số bài14 PDF2; Dãy số bài15–16 PDF2','Chia vị trí cho độ dài nhóm; xét cả nhóm đủ và phần dư.','Nền tảng TIMO'),
'assume':('Giả thiết tạm: chân, vé, tiền','Đề cương ôn nâng cao; sơ đồ bài lời văn','Giả sử cùng một loại; phần chênh chia cho chênh lệch mỗi vật.','Bổ sung TIMO'),
'basic':('Thứ tự phép tính / nhân chia','Giữa kì TN12,15; CĐ1 PDF1','Tính ngoặc, nhân/chia, cộng/trừ; rút gọn khi hợp lệ.','Nối trực tiếp'),
'sum':('Tổng dãy cách đều','CĐ1 bài10 PDF2; Dãy số PDF1','Đếm số hạng rồi lấy tổng số đầu và cuối nhân số hạng, chia2.','Nối trực tiếp'),
'factor':('Tính nhanh / thừa số chung / bù tròn','Giữa kì TN20,TL7; CĐ1 bài2–6 PDF1–2','Nhận thừa số chung; ghép các phần để tạo số tròn.','Nối trực tiếp'),
'pair':('Ghép cặp với dấu cộng trừ','CĐ1 bài8–9 PDF2; ảnh bài8','Giữ dấu đi với từng số, đếm số cặp.','Nối trực tiếp'),
'crypt':('Chữ thay chữ số trong phép tính','Cấu tạo số PDF1–2','Xét hàng đơn vị và số nhớ; giữ điều kiện khác nhau.','Nối một phần'),
'div':('Chia hết / tìm chữ số / số lớn nhỏ','Phiếu Chia hết PDF1; cấu tạo số; TN4','Phối hợp dấu hiệu2,3,5,9; nâng cao4,8,12,45.','Nối một phần'),
'last':('Chữ số tận cùng của tích','Phiếu Chữ số tận cùng PDF1','Lập chu kì tận cùng và xét số lượng thừa số.','Nối một phần'),
'op':('Phép toán mới, có thể lồng nhau','Topic4 theo nhật kí; giữa kì TN12','Thay số đúng vị trí; nếu lồng nhau tính trong trước.','Nối trực tiếp'),
'ratio':('Tổng–tỉ / hiệu–tỉ / phần bằng nhau','Math Comparison theo nhật kí; giữa kì TL10','Vẽ phần bằng nhau; tổng chia tổng phần, hiệu chia hiệu phần.','Nối một phần'),
'age':('Tuổi kết hợp tổng–hiệu','Giữa kì TN18,TL13; phiếu Tổng hiệu','Hiệu tuổi không đổi; suy hiệu rồi dùng tổng–hiệu.','Nối trực tiếp'),
'grid':('Đếm hình chữ nhật, có/không điều kiện','Topic5 Counting theo nhật kí; thiếu phiếu cụ thể','Chọn hai đường ngang/hai đường dọc hoặc bốn biên quanh vùng phải chứa.','Bổ sung TIMO'),
'area':('Diện tích phần tô / cắt ghép / ô vuông','Giữa kì TN14,17,TL5,TT16–17','Tính diện tích một ô; cộng phần hoặc lấy hình bao trừ phần khuyết.','Nối trực tiếp'),
'opt':('Chu vi–diện tích với cạnh nguyên / cực trị','Giữa kì TN14,17; mở rộng hình chữ nhật','Liệt kê các cặp cạnh nguyên thỏa diện tích hoặc nửa chu vi.','Nối một phần'),
'view':('Nhìn hình khối từ một phía','Chưa thấy bài lớp tương ứng','Chỉ đếm các mặt nhìn thấy từ hướng đề yêu cầu; bỏ mặt bị che.','Bổ sung TIMO'),
'geo':('Chu vi / suy cạnh / hình ghép','Giữa kì TN14,17; TL10,12; TT16–18','Suy các cạnh bằng nhau từ hình và chu vi, không đo bằng mắt.','Nối trực tiếp'),
'worst':('Chắc chắn / trường hợp xấu nhất','Chưa thấy bài lớp tương ứng','Tìm nhiều nhất vẫn chưa đạt yêu cầu, rồi thêm đủ để bắt buộc đạt.','Bổ sung TIMO'),
'form':('Đếm số theo điều kiện chữ số','Cấu tạo số; Topic5 Counting theo nhật kí','Hàng đầu khác0; chia trường hợp, xét lặp/không lặp.','Nối một phần'),
'multiples':('Đếm các số chia hết','CĐ1/Dãy số; phiếu Chia hết','Tìm bội đầu/bội cuối rồi đếm dãy cách đều.','Nối trực tiếp'),
'stairs':('Bậc thang / tổng bước / truy hồi','Chưa thấy bài lớp tương ứng','Số cách bằng tổng số cách từ các bậc đi tới; bậc hỏng có0cách.','Bổ sung TIMO'),
'path':('Đếm đường đi trên sơ đồ','Chưa thấy bài lớp tương ứng','Tại mỗi nút cộng số cách từ các nút đi tới được nó.','Bổ sung TIMO'),
'color':('Đếm cách tô màu','Chưa thấy bài lớp tương ứng','Xét màu ô đầu rồi số lựa chọn của các ô tiếp theo.','Mở rộng'),
'solid':('Cạnh / mặt hình lập phương, hình chóp','Chưa thấy bài lớp tương ứng','Phân biệt đỉnh,cạnh,mặt; xem số cạnh đáy hình chóp.','Mở rộng'),
'regions':('Số phần lớn nhất do đường thẳng cắt','Chưa thấy bài lớp tương ứng','Thêm từng đường và đếm số phần mới có thể tạo.','Mở rộng'),
'surface':('Đếm mặt cần sơn / diện tích bề mặt','Chưa thấy bài lớp tương ứng','Đếm mặt lộ ra; mặt ghép kín không sơn.','Mở rộng'),
'place':('Giá trị chữ số / thêm chữ số / sai hàng','Giữa kì TN1–2,TL2–3,8; Cấu tạo số','Viết theo giá trị hàng; thêm bên phải nhân10 rồi cộng chữ số.','Nối trực tiếp'),
'geosum':('Tổng dãy nhân / nhân rồi trừ','Mở rộng từ CĐ1','Nhân tổng theo công bội, trừ tổng cũ để triệt tiêu số hạng.','Mở rộng'),
'union':('Đếm chia hết cho A hoặc B','Chia hết và đếm dãy','Cộng hai nhóm rồi trừ giao; không đếm đôi.','Mở rộng'),
'divisors':('Đếm ước của một số','Phiếu Chia hết; chưa thấy chuyên đề đếm ước','Liệt kê cặp ước hoặc phân tích số; không nhầm đếm bội.','Mở rộng'),
'optimize':('Lập số để tổng/hiệu lớn nhỏ nhất','Cấu tạo số; mở rộng','Ưu tiên các hàng lớn; kiểm tra chữ số đầu và điều kiện không lặp.','Mở rộng'),
'concat':('Chữ số thứ n của dãy số viết liền','Dãy số bài14 PDF2','Tách nhóm số một/hai/ba chữ số rồi xác định vị trí trong số.','Mở rộng'),
'table':('Bảng quy luật / tổng các ô liên tiếp','Cấu tạo số bài15 PDF2; Topic3 theo nhật kí','So sánh hàng/cột; với tổng3ô cố định, ô cách3vị trí bằng nhau.','Bổ sung TIMO'),
'average':('Trung bình cộng, tìm số thiếu','Phiếu Trung bình cộng PDF1; chưa xác nhận đã học','Tổng bằng trung bình nhân số lượng; trừ các số đã biết.','Tham khảo QG'),
'cuts':('Cắt gỗ / dây: số nhát cắt','Chưa thấy bài lớp tương ứng','Cắt một vật thành nphần cần n−1nhát, nếu không chồng vật.','Tham khảo QG'),
'consecutive':('Tổng các số chẵn/lẻ liên tiếp','CĐ1/Dãy số; nâng cao','Dùng số ở giữa/trung bình và khoảng cách2 để suy dãy.','Tham khảo QG'),
'pyth':('Tam giác vuông: cạnh huyền / ghép hình','Chưa thấy trong phạm vi giữa kì','Nội dung vòng quốc gia; không đưa vào khung ôn gấp nếu chưa học.','Để sau'),
'segments':('Đếm đoạn nối hai điểm','Chưa thấy bài lớp tương ứng','Mỗi cặp hai điểm xác định một đoạn; không đếm đôi.','Tham khảo QG'),
'digitprod':('Đếm số có tích chữ số cho trước','Cấu tạo số; mở rộng','Phân tích tích thành các bộ chữ số, rồi xét hoán vị/parity.','Tham khảo QG'),
'eliminate':('Khử hai tổ hợp khối lượng','Giữa kì bài lời văn; nâng cao','Trừ hai tổng để loại đại lượng có cùng số lượng.','Tham khảo QG'),
'permutation':('Sắp xếp chữ / nhóm chữ liền nhau','Chưa thấy trong phạm vi giữa kì','Gộp nhóm yêu cầu; xét các chữ trùng để không đếm lặp.','Để sau'),
'productratio':('Tích–tỉ / tìm hai số từ tích','Chưa thấy trong phạm vi giữa kì','Suy bình phương một phần từ tích và tỉ số; kiểm tra nghiệm dương.','Để sau'),
'remainder':('Chia có dư / hai cách chia vật','Chưa thấy chuyên đề tương ứng','So chênh lệch lượng phân phối và chênh số dư để tìm số người.','Tham khảo QG'),
'pattern':('Quy luật hình phát triển / số khối','Topic3 theo nhật kí; chưa có phiếu đầy đủ','Lập bảng vị trí và số phần tử của từng hình; tách phần cố định/phần tăng.','Tham khảo QG'),
'triangles':('Đếm tam giác vuông','Góc trong đề cương; mở rộng','Liệt kê cặp cạnh vuông và nối đỉnh, chỉ dùng cạnh có trong hình.','Tham khảo QG'),
'pigeon':('Chia nhóm để đảm bảo tối thiểu','Chưa thấy trong phạm vi giữa kì','Nếu tất cả nhóm ít hơn m thì tổng tối đa bao nhiêu; so với tổng thực tế.','Tham khảo QG'),
'work':('Số người và số ngày làm việc','Chưa thấy trong phạm vi giữa kì','Cùng công việc và năng suất: số người nhân số ngày không đổi.','Để sau')}
for (rnd,no),seq in SEQ.items():assert len(seq.split())==25,(rnd,no,len(seq.split()))

def positions(a,b):
 found=[];expected=1
 for pn in range(a,b+1):
  lines=[]
  for block in d[pn-1].get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    t=''.join(x['text'] for x in line['spans']).strip();m=re.match(r'^(\d{1,2})\.',t)
    if m and line['bbox'][0]<80:lines.append((int(m.group(1)),line['bbox'][1]))
  for n,y in sorted(lines,key=lambda x:x[1]):
   if n==expected:found.append((n,pn,y));expected+=1
 assert [x[0] for x in found]==list(range(1,26)),(a,b,found)
 return found
def crop(pos,i,last,prefix):
 n,start,y=pos[i]; nxt=pos[i+1] if i+1<len(pos) else (26,last+1,0)
 end=nxt[1];imgs=[]
 for pn in range(start,min(end,last)+1):
  if pn==end:
   bottom=nxt[2]-3
   if bottom<36:continue
  else:bottom=d[pn-1].rect.height-48
  top=max(0,y-3) if pn==start else 28
  if bottom<=top:continue
  name=f'{prefix}-{n}-{pn}.png';path=AS/name
  d[pn-1].get_pixmap(matrix=fitz.Matrix(1.75,1.75),clip=fitz.Rect(42,top,min(558,d[pn-1].rect.width-28),bottom)).save(path)
  imgs.append('assets/timo-catalog/'+name)
 return imgs

for rnd,ranges in RANGES.items():
 for no,(a,b) in enumerate(ranges,1):
  qp=positions(a,b);sa,sb=SOL[rnd][no-1];sp=positions(sa,sb)
  for i in range(25):
   r=next(x for x in records if x['id']==f'{rnd}-{no}-{i+1}')
   assert r['page']==qp[i][1],(r['id'],r['page'],qp[i])
   assert r['solution_page']==sp[i][1],(r['id'],r['solution_page'],sp[i])
   cat=SEQ[(rnd,no)].split()[i];r['category']=cat;r['category_name']=META[cat][0];r['connection']=META[cat][1];r['method']=META[cat][2]
   r['question_images']=crop(qp,i,b,f'{rnd}-{no}-q');r['solution_images']=crop(sp,i,sb,f'{rnd}-{no}-s')
   r['label']=f'{"Vòng loại" if rnd=="VL" else "Vòng quốc gia"} · Đề {no} · Câu {i+1}'
   # Short labels classify the problem; they do not reconstruct broken formula extraction.
   r['title']=META[cat][0]

lookup={r['id']:r for r in records}
CORE=['VL-1-8','VL-1-7','VL-1-9','VL-1-6','VL-1-13','VL-7-15','VL-1-11','VL-1-14','VL-1-12','VL-1-1','VL-1-4','VL-1-2','VL-1-3','VL-1-5','VL-7-4','VL-1-15','VL-6-2','VL-1-16','VL-1-17','VL-1-18','VL-1-19','VL-7-16','VL-1-21','VL-1-22','VL-1-23','VL-1-24','VL-1-25']
EXT=['VL-6-13','VL-7-10','VL-7-12','VL-7-23','VL-6-19','VL-7-17','VL-5-23','VL-6-20','VL-6-25','VL-7-25']
for r in records:
 r['selection']='Bài đại diện' if r['id'] in CORE else 'Mở rộng tùy sức' if r['id'] in EXT else 'Giữ đề thi thử' if r['round']=='VL' and r['exam']==2 else 'Để sau TIMO/giữa kì' if r['round']=='QG' else 'Thay thế/củng cố cùng dạng'
 r['alternatives']=[x['id'] for x in records if x['category']==r['category'] and x['round']=='VL' and x['exam']!=2 and x['id']!=r['id']][:4]

(ROOT/'danh-muc-timo.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'danh-muc-timo.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Mã','Vòng','Đề','Câu','Dạng','Liên hệ bài lớp','Vai trò','Trang PDF đề','Trang in đề','Trang PDF lời giải','Trang in lời giải','Bài thay thế'])
 for r in records:w.writerow([r['id'],r['round'],r['exam'],r['question'],r['category_name'],r['connection'],r['selection'],r['page'],r['printed_page'],r['solution_page'],r['solution_page']-1,','.join(r['alternatives'])])

def href(rid):return 'danh-muc-timo.html#'+rid
def rowlink(rid):
 r=lookup[rid];return f'<a href="{href(rid)}">{r["label"]}</a> <small>(đề PDF{r["page"]}; lời giải PDF{r["solution_page"]})</small>'
def shell(title,body,script=''):
 return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"></head><body><header><nav><a href="index.html">Mục lục</a><a href="lo-trinh.html">Lộ trình</a><a href="danh-muc-timo.html">Danh mục toàn bộ TIMO</a><a href="theo-doi.html">Theo dõi giữa kì</a></nav><h1>{title}</h1></header><main>{body}</main><script>{script}</script></body></html>'

body='<p class="note"><b>Đã rà đủ 350 câu.</b> Danh mục để chọn bài; không yêu cầu con làm hết. Mỗi mục mở ảnh đề gốc và lời giải gốc, giữ đúng công thức/hình. Vòng loại:175câu; quốc gia:175câu. Đề vòng loại2 giữ cho thi thử. Các đề có dạng tương tự được gom chung; đây không phải chứng minh hai câu trùng hoàn toàn.</p><div class="catalog-controls"><label>Tìm theo mã hoặc dạng <input id="search" placeholder="VL-7-15, dãy, chia hết…"></label><label>Vòng <select id="round"><option value="">Tất cả</option><option value="VL" selected>Vòng loại</option><option value="QG">Quốc gia</option></select></label><label>Dạng <select id="category"><option value="">Tất cả dạng</option>'+''.join(f'<option value="{c}">{h(m[0])}</option>' for c,m in META.items())+'</select></label><label>Vai trò <select id="role"><option value="">Tất cả</option>'+''.join(f'<option>{h(x)}</option>' for x in ['Bài đại diện','Thay thế/củng cố cùng dạng','Mở rộng tùy sức','Giữ đề thi thử','Để sau TIMO/giữa kì'])+'</select></label></div><p id="count"></p><p class="note">Bấm mã câu từ lộ trình sẽ mở đúng mục. Không mở đề2 trước thi thử. Nội dung quốc gia chủ yếu tiếng Anh; ảnh giữ nguyên và có chú thích thuật ngữ từ tài liệu.</p>'
for r in records:
 content=f'<p><b>Cách nhận dạng:</b> {h(r["method"])}</p><p><b>Nối với lớp:</b> {h(r["connection"])}</p><p><b>Vai trò:</b> {r["selection"]}</p><p class="source">TIMOK4.pdf · đề:PDF{r["page"]}/trang in{r["printed_page"]} · lời giải:PDF{r["solution_page"]}/trang in{r["solution_page"]-1}. <a href="sources/TIMOK4.pdf#page={r["page"]}">Mở trang đề</a> · <a href="sources/TIMOK4.pdf#page={r["solution_page"]}">Mở trang giải</a></p>'
 content+='<h3>Đề gốc — giữ biểu thức và hình</h3>'+''.join(f'<img class="source-crop" loading="lazy" src="{x}" alt="{r["label"]}, đề gốc">' for x in r['question_images'])
 content+='<details class="solution"><summary>Mở lời giải gốc sau khi con thử</summary>'+''.join(f'<img class="source-crop" loading="lazy" src="{x}" alt="{r["label"]}, lời giải gốc">' for x in r['solution_images'])+'</details>'
 content+='<p><b>Bài cùng dạng để thay thế:</b> '+(' · '.join(f'<a href="#{x}">{x}</a>' for x in r['alternatives']) or 'Không có bài vòng loại thay thế trong danh mục.')+'</p>'
 body+=f'<details class="catalog-item" id="{r["id"]}" data-round="{r["round"]}" data-category="{r["category"]}" data-role="{r["selection"]}" data-search="{h((r["id"]+" "+r["title"]+" "+r["connection"]).lower())}"><summary><b>{r["id"]}</b> · {h(r["title"])} <span class="tag">{r["selection"]}</span></summary><div class="catalog-body">{content}</div></details>'
script='''const els=[...document.querySelectorAll('.catalog-item')];const inputs=['search','round','category','role'].map(id=>document.getElementById(id));function filter(){let n=0;els.forEach(el=>{const ok=(!inputs[0].value||el.dataset.search.includes(inputs[0].value.toLowerCase()))&&(!inputs[1].value||el.dataset.round===inputs[1].value)&&(!inputs[2].value||el.dataset.category===inputs[2].value)&&(!inputs[3].value||el.dataset.role===inputs[3].value);el.hidden=!ok;if(ok)n++});document.getElementById('count').textContent=n+' câu phù hợp bộ lọc · tổng350câu đã rà.'}inputs.forEach(x=>x.addEventListener('input',filter));function gotoHash(){const id=decodeURIComponent(location.hash.slice(1));const el=document.getElementById(id);if(!el)return;inputs.forEach(x=>x.value='');filter();el.hidden=false;el.open=true;el.scrollIntoView({block:'start'});}window.addEventListener('hashchange',gotoHash);filter();gotoHash();'''
(ROOT/'danh-muc-timo.html').write_text(shell('Danh mục TIMO — rà đủ14đề,350câu',body,script),encoding='utf-8')

vlcnt=Counter(r['category'] for r in records if r['round']=='VL');qgcnt=Counter(r['category'] for r in records if r['round']=='QG')
body='<p class="note"><b>TIMO:Chủ nhật11/10. Giữa kì:15/10.</b> Ngày thường60phút; thứ Bảy180phút học chia4phiên. Lộ trình này chọn dạng và bài theo lỗi thực tế, không giao toàn bộ350câu. Có27bài đại diện trong kho, nhưng mỗi buổi chỉ chọn bài chưa chắc; không mặc định phải làm cả27bài cộng đề thi thử.</p><h2>1. Chọn bài theo mức hiểu, không theo số lượng hiển thị</h2><ol><li>Chọn một bài đại diện của dạng chưa chắc, cho con tự làm trước.</li><li>Nếu đúng và giải thích được, đánh dấu dạng đó; bỏ các bài tương tự trong buổi này.</li><li>Nếu sai/cần gợi ý, chữa bài lớp cùng kiến thức, rồi chọn một bài thay thế; không giải liên tiếp nhiều bài chỉ khác số.</li><li>Nếu10phút vẫn không nắm được bài mới, ghi lại để chữa sau; trở về kiến thức nền.</li><li>Đề vòng loại2 chỉ làm khi thi thử; không chọn câu của đề này làm bài thay thế trước đó.</li></ol><h2>2. Lịch chọn bài 07–15/10</h2>'
days=[
('07/10 — số học và cấu tạo số','60phút:10nhắc lý thuyết,20bài lớp,5nghỉ,15TIMO,10chữa. Chọn3–4câu TIMO, ưu tiên dạng chưa chắc.','Giữa kì TN1–6,12,13,15,19,20; TL1–3,6–8. Câu lớp đã đúng kiểm tra nhanh; phần còn lại rà soát12–13/10.',['VL-1-8','VL-1-7','VL-1-9','VL-7-15','VL-1-14','VL-1-12'],'06-10.html'),
('08/10 — hình học nối giữa kì','60phút theo khung cũ. Chọn2–3câu TIMO.','Giữa kì TN14,17; TL5hai ý diện tích; TT16–18. TT18 trùng nội dung VL-7-20, không làm hai lần.',['VL-1-17','VL-1-18','VL-7-16','VL-1-16','VL-7-20'],'08-10.html'),
('09/10 — lời văn và logic','60phút; chọn2–3câu trong danh sách. Dạng mới ưu tiên làm ngược/giả thiết tạm trước câu bảng khó.','Giữa kì TN16,18; TL9,11,13,15. Dùng tìmx của lớp trước làmngược.',['VL-1-3','VL-1-5','VL-6-2','VL-1-15','VL-7-4'],'09-10.html'),
('10/10 — sáng phiên1,45phút','10phút lý thuyết,25bài lớp,10chữa.','Giữa kì TN7–11; TL4; TL5phần thời gian; TL14. TIMO chỉ chọn1câu lịch/chu kì nếu còn thời gian.',['VL-1-2','VL-1-4','VL-1-1'],'10-10.html'),
('10/10 — sáng phiên2,40phút','Nghỉ ít nhất30phút trước phiên này. Hoàn thành TL10,12; chọn2–3dạng tổ hợp/khối chưa chắc, không làm cả danh sách.','Giữa kì TL10,12 và bài chưa xong. Phần giữa kì còn thiếu chuyển sang12–13/10.',['VL-1-19','VL-1-21','VL-1-22','VL-1-23','VL-1-24','VL-1-25'],'10-10.html'),
('10/10 — chiều phiên3,60phút','Thi thử trọn đề vòng loại2; dùng thời lượngBTC nếu khác. Không mở đáp án.','Đề giữ nguyên25câu, đủ5nhóm. Đây là lúc kiểm tra những dạng chưa kịp luyện riêng.',['VL-2-1'],'thi-thu-timo.html'),
('10/10 — chiều phiên4,35phút','Nghỉ ít nhất30phút. Chữa tối đa3nhóm lỗi; chọn tối đa1bài thay thế cho lỗi quan trọng nhất.','Không dạy thêm toàn bộ dạng mới hoặc chuyển sang quốc gia trong phiên cuối.',['VL-6-13','VL-7-10','VL-7-12'],'chua-timo.html'),
('11/10 — thi TIMO','Khởi động5–10phút bằng1câu quen thuộc nếu thuận tiện; sau thi nghỉ.','Không giao thêm bài giữa kì bắt buộc.',['VL-1-8'],'11-10.html'),
('12/10 — quay lại giữa kì','60phút: rà soát bảng từng ý, làm câu sai/chưa làm.','TN1–13,19; TL1–5,8,14. Bài đã đúng không chép lại.',[],'12-10.html'),
('13/10 — giữa kì đầy đủ','60phút: tìmx,lời văn,hình ghép; hoàn tất mọi ý chưa làm.','TN14–18,20; TL6–7,9–13,15; TT16–18.',[],'13-10.html'),
('14/10 — kiểm tra tổng hợp','60phút theo phiếu có sẵn. Nếu còn bài chưa làm, hoàn tất trước.','Phiếu dùng lại bài nguồn. Ôn lỗi cuối, không mở chuyên đềTIMO mới.',[],'14-10.html'),
('15/10 — thi giữa kì','Khởi động nhẹ5–10phút nếu thuận tiện.','Xem công thức và đơn vị; không học một phiên dài.',[],'15-10.html')]
for title,time,school,ids,file in days:
 body+=f'<section class="card"><h3>{title}</h3><p><b>Thời lượng:</b> {time}</p><p><b>Bài lớp:</b> {school}</p>'
 if ids:body+='<p><b>Kho để chọn (không phải danh sách bắt làm hết):</b></p><ul>'+''.join('<li>'+rowlink(x)+'</li>' for x in ids)+'</ul>'
 body+=f'<p><a href="{file}">Mở buổi lý thuyết/bài lớp tương ứng</a></p></section>'
body+='<h2>3. Bản đồ dạng vòng loại sau khi rà hết175câu</h2><p>Chọn bài đại diện một lần; bài thay thế chỉ dùng khi con sai hoặc cần kiểm tra chuyển cách làm sang dữ kiện khác. Các số lượng dưới đây mô tả kho bài, không phải khối lượng phải làm.</p>'
for cat in [c for c in META if vlcnt[c]]:
 allids=[r['id'] for r in records if r['round']=='VL' and r['category']==cat]
 main=next((x for x in CORE+EXT if lookup[x]['category']==cat),next((x for x in allids if lookup[x]['exam']!=2),allids[0]))
 alternatives=[x for x in allids if x!=main and lookup[x]['exam']!=2][:3]
 body+=f'<details class="card"><summary>{h(META[cat][0])} · {vlcnt[cat]}câu vòng loại</summary><p><b>Lý thuyết/cách làm:</b> {h(META[cat][2])}</p><p><b>Nối với lớp:</b> {h(META[cat][1])}</p><p><b>Bài đại diện:</b> {rowlink(main)}</p><p><b>Thay thế:</b> '+(' · '.join(rowlink(x) for x in alternatives) or 'Không có câu vòng loại khác ngoài đề giữ thi thử.')+'</p><p><a href="danh-muc-timo.html#'+main+'">Mở ảnh đề và lời giải đúng dạng</a></p></details>'
body+='<h2>4. Những phần trước đây chưa được bao phủ</h2><p>Đã bổ sung vào bản đồ: giả thiết tạm; bảng quy luật; đếm hình; nhìn hình khối; đếm đường đi/bậc thang; đếm ước; tổng dãy nhân; hợp hai nhóm chia hết; tô màu; số phần do đường cắt; diện tích bề mặt; vị trí chữ số trong dãy viết liền; tối ưu khi lập số. Các dạng mở rộng được để riêng, không làm tất cả sát thi.</p><h2>5. Đối chiếu vòng quốc gia</h2><p>Đã rà đủ175câu quốc gia để phát hiện các dạng khác. Trung bình cộng,cắt gỗ,dãy liên tiếp nâng cao,tích–tỉ,tam giác vuông,hoán vị chữ,năng suất,… được đưa vào danh mục tham khảo sau hai kỳ thi. Không mặc định thêm vào quỹ60phút hiện tại.</p><p class="note"><b>Phát hiện nối bài lớp:</b> giữa kì TT16 trùng nội dung QG-6-19; giữa kì TT18 trùng nội dung VL-7-20. Chỉ giải một lần mỗi bài rồi đối chiếu hai nguồn.</p><p>'+rowlink('QG-6-19')+'<br>'+rowlink('VL-7-20')+'</p><h2>6. Tài liệu kiểm tra bao phủ</h2><p><a href="danh-muc-timo.html">Danh mục có bộ lọc đủ350câu</a> · <a href="danh-muc-timo.csv">BảngCSV để lọc trong Excel</a> · <a href="theo-doi.html">Theo dõi đủ từng ý giữa kì</a> · <a href="toan-bo-de-cuong.html">Ngân hàng38câu/bài giữa kì</a></p><p>Rà soát ở đây gồm nhận dạng và đối chiếu câu/trang lời giải, không phải giải lại độc lập toàn bộ350câu. Lời giải gốc có thể có lỗi; khi chọn một bài cần kiểm tra phép tính trước khi hướng dẫn. Lỗi đã biết ở VL-2-20 được giải thích trong trang chữa thi thử.</p>'
(ROOT/'lo-trinh.html').write_text(shell('Lộ trình chọn bài — TIMO và giữa kì',body),encoding='utf-8')

css='''\n.catalog-controls{display:flex;flex-wrap:wrap;gap:14px;background:#eaf1fb;padding:20px;border-radius:10px}.catalog-controls label{display:flex;flex-direction:column;font-size:14px;font-weight:700;gap:6px}.catalog-controls input{font:inherit;padding:10px;border:1px solid #abc0d5;border-radius:6px}.catalog-item{background:white;border:1px solid #d9e3ef;border-radius:10px;padding:14px 20px;margin:12px 0;scroll-margin-top:20px}.catalog-item[hidden]{display:none!important}.catalog-item summary{font-size:17px;line-height:1.8;color:#294765}.catalog-body{padding:10px 2px}.source-crop{display:block;max-width:100%;height:auto;margin:18px auto;background:white;border:1px solid #dce5ee;padding:10px}.catalog-item .tag{margin-left:8px;font-size:12px}li{margin:9px 0}small{font-size:13px;color:#59708b}@media print{.catalog-controls{display:none}.catalog-item:not([open]){display:none}.source-crop{max-height:none}.card{break-inside:avoid}}\n'''
with (ROOT/'style.css').open('a',encoding='utf-8') as f:f.write(css)
# Add navigation without regenerating existing carefully typeset lessons.
from bs4 import BeautifulSoup
for file in ROOT.glob('*.html'):
 if file.name in ['lo-trinh.html','danh-muc-timo.html']:continue
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser');nav=soup.find('nav')
 if nav and not nav.find('a',href='lo-trinh.html'):
  a=soup.new_tag('a',href='lo-trinh.html');a.string='Lộ trình chọn bài';nav.append(a)
 if file.name=='index.html':
  note=soup.new_tag('p',attrs={'class':'note'});note.append(BeautifulSoup('<b>Cập nhật rà toàn bộ TIMO:</b> <a href="lo-trinh.html">Mở lộ trình chọn bài</a> — danh mục350câu đã phân loại; chọn theo dạng và lỗi, không làm hết kho.','html.parser'));soup.main.insert(1,note)
 file.write_text(str(soup),encoding='utf-8')
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));manifest.update(timo_catalog_questions=350,timo_preliminary_questions=175,timo_national_questions=175,timo_categories=len(set(r['category'] for r in records)),timo_preliminary_categories=len(vlcnt),core_pool=len(CORE),extension_pool=len(EXT));(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Catalog:',len(records),'questions;',len(vlcnt),'preliminary categories;',len(META),'categories total; question+solution source crops:',len(list(AS.glob('*.png'))))
