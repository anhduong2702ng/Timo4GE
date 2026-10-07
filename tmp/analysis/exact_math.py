from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import re, runpy

ns=runpy.run_path('tmp/analysis/math_layout.py')
EX=ns['EX'];math=ns['math'];ROOT=Path('output/html')
def p(t):return '<p>'+t+'</p>'
def answer(t):return '<p class="answer-line"><strong>Đáp số:</strong> '+t+'</p>'
def flow(words,exprs=(),result=None):
 return p(words)+''.join(math(e,False) for e in exprs)+(answer(result) if result else '')
def part(label,words,exprs=(),result=None):return '<section class="subpart"><h4>'+label+'</h4>'+flow(words,exprs,result)+'</section>'
def normalize(html):
 s=BeautifulSoup(html,'html.parser')
 for node in list(s.find_all(string=True)):
  t=str(node)
  t=re.sub(r'([^\W\d_])(?=\d)',r'\1 ',t)
  t=re.sub(r'(\d)(?=[^\W\d_])',r'\1 ',t)
  t=re.sub(r'(?<=[²³])(?=\d)',' ',t)
  t=re.sub(r'(?<=[,;:])(?=\S)',' ',t)
  node.replace_with(t)
 return str(s)

# Expressions are explicit, complete records. Never infer a formula boundary from prose.
Q={
'TN12':p('Tính giá trị của biểu thức sau với m = 2:')+math('12 : (3 − m)'),
'TN15':p('Tính:')+math('50 000 + 2 000 × 5'),
'TN20':p('Tính:')+math('12 345 × 17 + 12 345 × 23 + 35 × 12 345 + 12 345 × 24 + 12 345'),
'TN19':p('Tìm số tròn chục x, biết:')+math('47 < x < 92'),
'TL6':p('Tìm x:')+''.join(part(label,'', [e]) for label,e in [('a)','x × 2 + 375 = 5 867'),('b)','1 353 + x : 3 = 2 343'),('c)','x × 4 − 725 = 8 259'),('d)','9 035 − x × 5 = 760')]),
'TL7':p('Tính bằng cách hợp lý nhất:')+part('a)','',['2 345 + 4 257 − 345'])+part('b)','',['2 024 × 14 + 2 024 × 85 + 2 024']),
'C1-6a':p('Tính bằng cách thuận tiện nhất:')+math('54 × 113 + 45 × 113 + 113'),
'C1-8a':p('Tính giá trị của biểu thức:')+math('2 − 4 + 6 − 8 + 10 − 12 + 14 − 16 + 18 − 20 + 22'),
'T1-1':p('Dựa vào quy luật dưới đây, tìm số thứ 7 trong dãy.')+math('3, 4, 8, 15, 25, …'),
'T1-7':p('Tìm giá trị của:')+math('2 + 6 + 10 + … + 30 + 34 + 38'),
'T1-8':p('Tính:')+math('45 × 15 + 45 × 17 − 45 × 12'),
'T1-9':p('Tìm giá trị của:')+math('40 − 37 + 34 − 31 + … + 10 − 7 + 4 − 1'),
'T1-12':p('Tìm chữ số tận cùng của tích sau (2025 thừa số 9):')+math('9 × 9 × 9 × … × 9'),
'T1-13':p('Định nghĩa phép toán:')+math('a ⊗ b = a × b + b × (a − 3) + 2')+p('Tìm giá trị của:')+math('9 ⊗ 5'),
}
S={}
S['TN1']=flow('Cộng giá trị của các hàng đã cho. Những hàng không được nêu có chữ số 0.',['3 000 000 + 800 000 + 30 + 6 = 3 800 036'],'3 800 036')
S['TN2']=flow('Chữ số 5 ở hàng triệu, lớp triệu.',['5 × 1 000 000 = 5 000 000'],'5 000 000')
S['TN3']=flow('Cùng phần 16 nghìn, so sánh ba chữ số cuối.',['16 624 < 16 642 < 16 742 < 16 743'],'16 624; 16 642; 16 742; 16 743')
S['TN4']=flow('Số lớn nhất có sáu chữ số là số lẻ 999 999. Giảm một đơn vị được số chẵn lớn nhất.',['999 999 − 1 = 999 998'],'999 998')
S['TN5']=flow('Chữ số hàng trăm nghìn là 1. Chữ số ngay bên phải là 0, nhỏ hơn 5: giữ nguyên hàng trăm nghìn và đổi các chữ số phía sau thành 0.',result='190 100 000')
S['TN6']=flow('Số liền sau hơn số đã cho một đơn vị.',['888 889 + 1 = 888 890'],'888 890')
S['TN7']=flow('Tại A, B, C, D: mỗi đỉnh có 1 góc vuông và 2 góc nhọn. Tại E: 2 góc vuông (AED, DEC), 1 góc nhọn (BEC), 2 góc tù (AEB, BED), 1 góc bẹt (AEC). Tại M: 1 góc bẹt (DMC). Cộng riêng từng loại; mỗi cặp tia chỉ đếm một lần.',result='6 góc vuông; 9 góc nhọn; 2 góc tù; 2 góc bẹt.')
S['TN8']=flow('Thế kỉ XIII gồm các năm từ 1201 đến 1300. Năm 1226 nằm trong khoảng đó.',result='Thế kỉ XIII')
S['TN9']=flow('A: 5 góc nhọn, 1 góc vuông. B, C, D: mỗi đỉnh 1 góc vuông. M: 2 góc nhọn (BMA, CMN), 3 góc tù (BMN, CMA, AMN), 1 góc bẹt (BMC). N: 3 góc nhọn (CNM, DNA, MNA), 2 góc tù (CNA, DNM), 1 góc bẹt (CND).',result='5 góc tù; 10 góc nhọn; 4 góc vuông; 2 góc bẹt.')
S['TN10']=flow('Một giờ có 60 phút. Một phần tư giờ bằng:',['60 : 4 = 15 phút'],'15 phút')
S['TN11']=flow('Đổi 3 phút ra giây rồi cộng 12 giây.',['3 × 60 + 12 = 192 giây'],'192 giây')
S['TN12']=flow('Thay m bằng 2 rồi tính trong ngoặc trước.',['12 : (3 − 2) = 12 : 1','12 : 1 = 12'],'12')
S['TN13']=flow('Số 1243 tận cùng bằng 3 nên là số lẻ. Dãy D gồm các số lẻ liên tiếp.',result='D. Dãy 1, 3, 5, 7, …')
S['TN14']=flow('Cạnh hình vuông:',['36 : 4 = 9 cm'])+flow('Diện tích hình vuông:',['9 × 9 = 81 cm²'],'81 cm²')
S['TN15']=flow('Thực hiện phép nhân trước, sau đó cộng.',['50 000 + 2 000 × 5 = 50 000 + 10 000','50 000 + 10 000 = 60 000'],'60 000')
S['TN16']=flow('Tiền mua vở:',['5 × 8 000 = 40 000 đồng'])+flow('Tiền mua bút chì:',['2 × 25 000 = 50 000 đồng'])+flow('Tổng số tiền:',['40 000 + 50 000 = 90 000 đồng'],'90 000 đồng')
S['TN17']=flow('Chiều dài hình chữ nhật:',['4 × 3 = 12 m'])+flow('Diện tích hình chữ nhật:',['12 × 4 = 48 m²'],'48 m²')
S['TN18']=flow('Số nhỏ nhất có hai chữ số là 10. Tuổi cháu năm nay:',['10 − 5 = 5 tuổi'])+flow('Tuổi ông năm nay:',['5 + 50 = 55 tuổi'],'55 tuổi')
S['TN19']=flow('Liệt kê các bội của 10 lớn hơn 47 và nhỏ hơn 92.',result='x = 50; 60; 70; 80; 90')
S['TN20']=flow('Đặt thừa số chung là 12 345. Số hạng cuối bằng 12 345 nhân 1.',['12 345 × (17 + 23 + 35 + 24 + 1)','12 345 × 100 = 1 234 500'],'1 234 500')
S['TL1']=part('a) Từ bé đến lớn','So sánh hàng nghìn trước, rồi các hàng tiếp theo.',result='2 312; 3 771; 4 333; 4 374; 8 951')+part('b) Từ lớn đến bé','Sắp xếp theo chiều ngược lại.',result='4 992; 3 182; 2 883; 2 471; 1 475')
S['TL2']=part('a) Hàng và lớp','Theo thứ tự bốn số trong đề: chữ số 2 thuộc hàng triệu, lớp triệu; hàng trăm, lớp đơn vị; hàng đơn vị, lớp đơn vị; hàng trăm nghìn, lớp nghìn.')+part('b) Làm tròn','Chữ số hàng chục nghìn lần lượt là 0, 5, 3, 1. Chỉ số thứ hai tăng hàng trăm nghìn.',result='132 000 000; 800 000; 6 900 000; 37 200 000')
S['TL3']=part('a) Giá trị của chữ số 9','Theo thứ tự: chữ số 9 ở hàng đơn vị, hàng chục nghìn, hàng triệu.',result='9; 90 000; 9 000 000')+part('b) Làm tròn','Chữ số hàng nghìn lần lượt là 4, 4, 2; đều nhỏ hơn 5.',result='850 000; 1 190 000; 19 430 000')
S['TL4']=flow('Dùng các quan hệ đơn vị khối lượng; với số hỗn hợp, đổi từng phần rồi cộng.',['1 yến = 10 kg','20 tấn = 200 tạ','1 000 kg = 10 tạ','2 yến 8 kg = 28 kg','3 tạ 50 kg = 350 kg','3 tạ = 300 kg'])
S['TL5']=flow('Đổi thời gian theo 60; thế kỉ theo 100 năm; hai đơn vị diện tích liền nhau theo 100.',['2 thế kỉ 25 năm = 225 năm','145 giây = 2 phút 25 giây','315 phút = 5 giờ 15 phút','3 phút 28 giây = 208 giây','34 dm² 12 cm² = 3 412 cm²','3 170 dm² = 31 m² 70 dm²'])
S['TL6']=part('a)','Chuyển phần cộng đã biết để tìm tích chứa x.',['x × 2 = 5 867 − 375','x × 2 = 5 492','x = 5 492 : 2','x = 2 746'],'x = 2 746')+part('b)','Tìm thương chứa x trước.',['x : 3 = 2 343 − 1 353','x : 3 = 990','x = 990 × 3','x = 2 970'],'x = 2 970')+part('c)','Tìm số bị trừ, sau đó tìm thừa số x.',['x × 4 = 8 259 + 725','x × 4 = 8 984','x = 8 984 : 4','x = 2 246'],'x = 2 246')+part('d)','Tìm số trừ, sau đó tìm thừa số x.',['x × 5 = 9 035 − 760','x × 5 = 8 275','x = 8 275 : 5','x = 1 655'],'x = 1 655')+p('Thay từng giá trị x vào phương trình ban đầu để kiểm tra.')
S['TL7']=part('a)','Ghép phép trừ để tạo số tròn nghìn.',['2 345 + 4 257 − 345 = (2 345 − 345) + 4 257','= 2 000 + 4 257','= 6 257'],'6 257')+part('b)','Đặt thừa số chung.',['2 024 × 14 + 2 024 × 85 + 2 024','= 2 024 × (14 + 85 + 1)','= 2 024 × 100','= 202 400'],'202 400')
S['TL8']=flow('Số bé phải có ba chữ số: nếu có một hoặc hai chữ số thì tổng quá nhỏ; nếu có bốn chữ số thì tổng ít nhất 22 000. Thêm chữ số 2 bên trái số có ba chữ số làm số đó tăng 2000. Số bé:',['(3 180 − 2 000) : 2 = 590'])+flow('Số lớn:',['590 + 2 000 = 2 590'],'590 và 2 590')+p('Kiểm tra: tổng là 3180; viết 2 trước 590 được 2590.')
S['TL9']=flow('Giá mỗi ki-lô-gam hôm qua:',['100 000 : 5 = 20 000 đồng'])+flow('Giá mỗi ki-lô-gam hôm nay:',['100 000 : 4 = 25 000 đồng'])+flow('Mức tăng giá:',['25 000 − 20 000 = 5 000 đồng'],'5 nghìn đồng mỗi ki-lô-gam')
S['TL10']=flow('Chiều rộng mảnh đất:',['210 : 3 = 70 m'])+flow('Diện tích mảnh đất:',['210 × 70 = 14 700 m²'])+flow('Số sắn thu được trên mỗi mét vuông:',['9 : 3 = 3 kg'])+flow('Tổng số sắn thu được và đổi ra tạ:',['14 700 × 3 = 44 100 kg','44 100 : 100 = 441 tạ'],'441 tạ')
S['TL11']=flow('Số dầu trong thùng thứ hai:',['435 − 15 = 420 lít'])+flow('Số dầu trong thùng thứ ba:',['435 + 58 = 493 lít'])+flow('Tổng số dầu:',['435 + 420 + 493 = 1 348 lít'],'1 348 lít')
S['TL12']=flow('Diện tích mảnh đất:',['15 × 8 = 120 m²'])+flow('Khối lượng cát cần dùng:',['120 × 2 = 240 tấn'])+flow('Số chuyến xe:',['240 : 8 = 30'],'30 chuyến')
S['TL13']=flow('Bao thứ hai ban đầu nhiều hơn bao thứ nhất:',['22 − 5 = 17 kg'])+flow('Khối lượng bao thứ nhất:',['(147 − 17) : 2 = 65 kg'])+flow('Khối lượng bao thứ hai:',['65 + 17 = 82 kg'],'Bao thứ nhất: 65 kg; bao thứ hai: 82 kg')+p('Kiểm tra: lấy đi theo đề thì mỗi bao còn 60 kg.')
S['TL14']=flow('Khối lượng khoai tây:',['7 × 30 = 210 kg'])+flow('Khối lượng khoai lang:',['5 × 20 = 100 kg'])+flow('Tổng khối lượng và đổi ra yến:',['210 + 100 = 310 kg','310 : 10 = 31 yến'],'31 yến')
S['TL15']=part('a)','Tính tiền mũ và áo choàng rồi cộng.',['4 × 55 000 = 220 000 đồng','3 × 80 000 = 240 000 đồng','220 000 + 240 000 = 460 000 đồng'],'460 000 đồng')+part('b)','Tính tiền được giảm, rồi lấy tổng tiền trừ đi.',['460 000 : 4 = 115 000 đồng','460 000 − 115 000 = 345 000 đồng'],'345 000 đồng')
S['TT16']=flow('Cạnh hình vuông lớn:',['64 : 4 = 16 cm'])+flow('Vì AB bằng BD nên mỗi đoạn dài:',['16 : 2 = 8 cm'])+flow('Vì BC bằng CD nên mỗi đoạn dài:',['8 : 2 = 4 cm'])+flow('Hai hình vuông ở góc trên bên phải có cạnh CD bằng 4 cm, hình vuông phía dưới có cạnh 8 cm. Diện tích hình vuông nhỏ nhất:',['4 × 4 = 16 cm²'],'16 cm²')
S['TT17']=flow('Hình bao có chiều rộng bằng tổng hai cột và khoảng giữa:',['2 + 4 + 2 = 8 cm'])+flow('Diện tích hình bao:',['8 × 8 = 64 cm²'])+flow('Diện tích hai phần khuyết:',['2 × (4 × 3) = 24 cm²'])+flow('Diện tích hình chữ H:',['64 − 24 = 40 cm²'],'40 cm²')
S['TT18']=flow('Gọi cạnh dài hình chữ nhật là a, cạnh ngắn là b. Theo chiều đứng, cạnh hình vuông lớn bằng 2a; theo chiều ngang, cạnh đó bằng a cộng hai lần b.',['2 × a = a + 2 × b','a = 2 × b'])+flow('Chu vi mỗi hình chữ nhật bằng 36.',['2 × (a + b) = 36','a + b = 18','3 × b = 18','b = 6','a = 12'])+flow('Cạnh và chu vi hình vuông lớn:',['2 × 12 = 24','4 × 24 = 96'],'96 (đề không ghi đơn vị)')
S['C1-6a']=flow('Đặt thừa số chung là 113.',['54 × 113 + 45 × 113 + 113','= 113 × (54 + 45 + 1)','= 113 × 100','= 11 300'],'11 300')
S['C1-8a']=flow('Ghép theo thứ tự từ cuối để mỗi phép trừ đều có kết quả dương.',['(22 − 20) + (18 − 16) + (14 − 12) + (10 − 8) + (6 − 4) + 2','= 2 + 2 + 2 + 2 + 2 + 2','= 12'],'12')
S['CS4']=flow('Gọi số ban đầu là N. Số mới là 10N cộng 2.',['10 × N + 2 − N = 4 106','9 × N = 4 104','N = 4 104 : 9','N = 456'],'456')
S['CS10']=flow('Gọi số ban đầu là N. Thêm chữ số 5 bên phải rồi trừ số cũ.',['10 × N + 5 − N = 230','9 × N = 225','N = 25'],'25')
S['T1-1']=flow('Các hiệu lần lượt là 1, 4, 7, 10, tăng đều 3 đơn vị. Hai hiệu tiếp theo là 13 và 16.',['25 + 13 = 38','38 + 16 = 54'],'54')
S['T1-2']=flow('Chia 44 ngày thành các tuần trọn vẹn và phần còn lại.',['44 = 6 × 7 + 2'])+p('Lùi hai ngày từ thứ Sáu được thứ Tư.')+answer('Thứ Tư')
S['T1-4']=flow('Mỗi nhóm có ba hình, trong đó một hình vuông.',['50 = 16 × 3 + 2'])+flow('Có 16 nhóm trọn vẹn. Hai hình dư gồm một hình tròn đặc và một hình vuông.',['16 + 1 = 17'],'17 hình vuông')
S['T1-7']=flow('Dãy cách đều 4 đơn vị. Số số hạng:',['(38 − 2) : 4 + 1 = 10'])+flow('Tổng dãy:',['(2 + 38) × 10 : 2 = 200'],'200')
S['T1-8']=flow('Đặt thừa số chung là 45.',['45 × 15 + 45 × 17 − 45 × 12','= 45 × (15 + 17 − 12)','= 45 × 20','= 900'],'900')
S['T1-9']=flow('Số số hạng:',['(40 − 1) : 3 + 1 = 14'])+flow('Có 7 cặp, mỗi cặp là hiệu của hai số cách nhau 3 đơn vị.',['(40 − 37) + (34 − 31) + … + (4 − 1)','= 7 × 3','= 21'],'21')
S['T1-11']=flow('Số chẵn lớn nhất có ba chữ số là 998 nhưng không chia hết cho 3. Số chẵn kế tiếp là 996, có tổng các chữ số chia hết cho 3.',['9 + 9 + 6 = 24'],'996')
S['T1-12']=flow('Chữ số tận cùng của các tích gồm một, hai, ba, bốn thừa số 9 lần lượt là 9, 1, 9, 1. Có 2025 thừa số, là số lẻ nên lấy chữ số đầu của nhóm.',result='9')
S['T1-13']=flow('Thay a bằng 9 và b bằng 5 đúng theo định nghĩa.',['9 ⊗ 5 = 9 × 5 + 5 × (9 − 3) + 2','= 45 + 30 + 2','= 77'],'77')
S['T1-14']=flow('Tổng các chữ số:',['2 + 0 + 2 + 5 + A = 9 + A'])+p('Để chia hết cho 3, A thuộc 0, 3, 6, 9. Để là số lẻ, A chỉ có thể là 3 hoặc 9.')+answer('A nhỏ nhất bằng 3')
S['T1-15']=flow('Bell có một phần, Ashley có hai phần. Tổng là ba phần.',['18 : (1 + 2) = 6'],'Bell có 6 dây buộc tóc')
S['T1-17']=flow('Cạnh hình vuông nhỏ và lớn:',['16 : 4 = 4 cm','24 : 4 = 6 cm'])+flow('Tổng diện tích hai hình chữ nhật bằng diện tích hình lớn trừ hình nhỏ.',['6 × 6 − 4 × 4 = 20 cm²'],'20 cm²')
S['T1-18']=flow('Liệt kê các cặp cạnh có tích bằng 30: (1; 30), (2; 15), (3; 10), (5; 6). Chu vi tương ứng là 62, 34, 26, 22. Cặp 5 và 6 cho chu vi nhỏ nhất.',['2 × (5 + 6) = 22'],'22')
S['T1-21']=flow('Trường hợp xấu nhất, lấy hết các lá không đỏ trước: 9 lá xanh và 10 lá vàng. Sau đó phải lấy thêm 4 lá đỏ.',['9 + 10 + 4 = 23'],'23 lá')
S['T1-22']=flow('Hàng chục có 4 cách chọn: 1, 2, 3, 4. Hàng đơn vị có 3 cách chọn: 0, 2, 4.',['4 × 3 = 12'],'12 số')
S['T1-23']=flow('Các số hai chữ số chia hết cho 3 là 12, 15, …, 99. Khoảng cách là 3.',['(99 − 12) : 3 + 1 = 30'],'30 số')
S['T6-2']=flow('Sau 4 năm, tuổi bố bằng tuổi mẹ sau 7 năm, nên bố hơn mẹ 3 tuổi. Tuổi mẹ hiện nay:',['(79 − 3) : 2 = 38'],'38 tuổi')
S['T6-3']=flow('Làm ngược từ kết quả cuối.',['60 × 10 = 600','600 + 79 = 679','679 : 7 = 97','97 − 4 = 93'],'93 tuổi')
S['T7-15']=flow('Gọi số ban đầu là N. Thêm chữ số 1 bên phải:',['10 × N + 1 − N = 856','9 × N = 855','N = 855 : 9','N = 95'],'95')
assert set(S)==set(EX),set(EX)-set(S)

# Mock answers: explicit expressions with prose kept intact, no formula scanning.
M={
1:flow('Nhóm 4 lá cờ có một lá Việt Nam. Có 10 nhóm trọn vẹn và một lá dư đầu nhóm, cũng là Việt Nam.',['41 = 10 × 4 + 1','10 + 1 = 11'],'11 lá — A'),
2:flow('Ngày mai là Chủ nhật nên hôm nay thứ Bảy. Sau 7 tuần vẫn là thứ Bảy; thêm một ngày là Chủ nhật.',['50 = 7 × 7 + 1'],'Chủ nhật — C'),
3:flow('Giả sử 42 con đều là gà. Số chân tính thiếu chia cho 2 là số ngựa.',['42 × 2 = 84','108 − 84 = 24','24 : 2 = 12'],'12 con — D'),
4:flow('Dãy hiệu là 2, 4, 6, 8, 10, 12, 14.',['23 + 10 = 33','33 + 12 = 45','45 + 14 = 59'],'59 — B'),
5:flow('Làm ngược từ 15 chiếc còn lại.',['15 + 25 = 40','40 × 2 = 80','80 + 29 = 109'],'109 chiếc — A'),
6:flow('Tính từng thương rồi cộng.',['150 : 3 + 150 : 5 + 150 : 10','= 50 + 30 + 15','= 95'],'95 — B'),
7:flow('Đếm số số hạng rồi tính tổng.',['(30 − 3) : 3 + 1 = 10','(3 + 30) × 10 : 2 = 165'],'165 — A'),
8:flow('Đặt thừa số chung 212.',['212 × 25 + 212 × 90 − 212 × 15','= 212 × (25 + 90 − 15)','= 21 200'],'21 200 — B'),
9:flow('Có 28 số, ghép thành 14 cặp, mỗi cặp có hiệu 2.',['(60 − 6) : 2 + 1 = 28','28 : 2 = 14','14 × 2 = 28'],'28 — A'),
10:flow('Đối chiếu hình phép cộng. Hàng đơn vị có nhớ nên C bằng 8. Hàng chục cho B bằng 3 hoặc 8; vì B khác C nên loại 8.',result='B = 3 — C'),
11:flow('Chọn hàng nghìn 9, trăm 8, chục 7. Hàng đơn vị 5 vừa chia hết cho 5 vừa không lặp chữ số.',result='9875 — C'),
12:flow('Tận cùng của tích các thừa số 4 lặp theo nhóm 4, 6. Có 2024 thừa số, là số chẵn.',result='6 — C'),
13:flow('Thay đúng vị trí trong định nghĩa phép toán.',['(3 × 2 − 4) × (6 : 3 + 8)','= 2 × 10','= 20'],'20 — A'),
14:flow('M có 9 phần, N có 1 phần. Tìm một phần rồi nhân 9.',['30 : (9 + 1) = 3','3 × 9 = 27'],'M = 27 — A'),
15:flow('Tổng chữ số là 8 cộng X. Điều kiện chia hết cho 3 cho X bằng 1, 4 hoặc 7. Điều kiện số chẵn giữ lại X bằng 4.',result='X = 4 — B'),
16:flow('Theo hình: có 2 đường trên, 2 đường dưới, 4 đường trái và 1 đường phải lá cờ.',['2 × 2 × 4 × 1 = 16'],'16 hình — B'),
17:flow('Hình vuông nhỏ có cạnh 3 cm. Hình chữ nhật dài 9 cm, rộng 3 cm.',['(9 − 3) : 2 = 3 cm','2 × (9 + 3) = 24 cm'],'24 cm — A'),
18:flow('Cặp cạnh nguyên là (1; 24), (2; 12), (3; 8), (4; 6). Chu vi lớn nhất ứng với cặp đầu.',['2 × (1 + 24) = 50'],'50 — C'),
19:flow('Hình lời giải nguồn đánh số 13 mặt phía trước. Hai mặt số 3 và 10 bị che bởi mặt số 2 và 9.',['13 − 2 = 11'],'11 mặt — C'),
20:flow('Cột buồm có diện tích 5 cm²; cánh buồm 4 cm²; thân thuyền 14 cm². Cộng đủ cả ba phần.',['5 + 4 + 14 = 23 cm²'],'23 cm² — C')+p('<b>Lưu ý từ bản gốc:</b> lời giải nguồn liệt kê hai phần 4 và 14 rồi kết luận 23, thiếu phần cột buồm 5 trong phép cộng. Hình nguồn vẫn đủ ba phần.'),
21:flow('Xấu nhất lấy hết hai màu có nhiều bút nhất: 8 xanh và 7 đen. Thêm một bút chắc chắn là đỏ.',['8 + 7 + 1 = 16'],'16 bút — A'),
22:flow('Liệt kê: 39, 48, 57, 66, 75, 84, 93. Có bảy số.',result='7 số — D'),
23:flow('Các bội của 5 có hai chữ số từ 10 đến 95.',['(95 − 10) : 5 + 1 = 18'],'18 số — B'),
24:flow('Số cách đến các bậc từ 0 đến 10 lần lượt: 1, 1, 2, 3, 5, 8, 13, 0, 13, 13, 26. Bậc 7 hỏng nên có 0 cách; mỗi bậc khác bằng tổng hai bậc trước.',result='26 cách — D'),
25:flow('Ghi 1 ở điểm xuất phát. Mỗi nút bằng tổng số cách từ những nút có đường đi tới nó. Đường không tồn tại không góp số cách. Đối chiếu hình đánh số ở PDF 70.',result='23 cách — B')}

for file in ROOT.glob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for article in soup.select('article.exercise'):
  k=article.get('id','')
  if k in EX:
   prompt=article.select_one('.prompt')
   if prompt:
    replacement=soup.new_tag('div',attrs={'class':'prompt'})
    label=soup.new_tag('span',attrs={'class':'prompt-label'});label.string='ĐỀ BÀI';replacement.append(label)
    question=Q.get(k,p(normalize(EX[k]['q'])))
    for child in list(BeautifulSoup(question,'html.parser').contents):replacement.append(child)
    prompt.replace_with(replacement)
   sol=article.select_one('details.solution')
   if sol:
    for child in list(sol.contents):
     if getattr(child,'name',None)!='summary':child.extract()
    box=soup.new_tag('div',attrs={'class':'solution-flow'})
    for child in list(BeautifulSoup(S[k],'html.parser').contents):box.append(child)
    sol.append(box)
  elif k.startswith('mock-'):
   for child in list(article.contents):
    if getattr(child,'name',None) not in ['h3','textarea'] and not (getattr(child,'name',None)=='p' and 'source' in child.get('class',[])):child.extract()
   box=soup.new_tag('div',attrs={'class':'solution-flow'})
   for child in list(BeautifulSoup(M[int(k[5:])],'html.parser').contents):box.append(child)
   article.find('textarea').insert_before(box)
 for text in list(soup.find_all(string=True)):
  if text.parent.name in ['script','style','title','a','mn','mtext'] or '1/4' not in str(text):continue
  bits=str(text).split('1/4')
  for i,bit in enumerate(bits):
   if bit:text.insert_before(bit)
   if i<len(bits)-1:
    inline=BeautifulSoup('<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mn>1</mn><mn>4</mn></mfrac></math>','html.parser').math
    text.insert_before(inline)
  text.extract()
 file.write_text(str(soup),encoding='utf-8')

with (ROOT/'style.css').open('a',encoding='utf-8') as f:f.write('''
/* A complete expression occupies one uninterrupted mathematical line. */
.math-display{background:transparent!important;border:0!important;border-radius:0;padding:14px 6px;margin:8px 0;min-height:0;text-align:left}.math-display math{margin:0 auto;display:math;font-size:1.25em}.solution-flow>p{margin:17px 0 6px;line-height:1.85}.solution-flow .math-display{margin:4px 0;padding:9px 6px}.answer-line{margin-top:23px!important;padding-top:12px;border-top:1px solid #c0d6c9;font-weight:700;color:#145339}.solution-flow .answer-line strong{background:none;border:0;padding:0;font-size:inherit;color:#145339}.prompt p{margin:8px 0 12px}.prompt .math-display{margin:0;padding:14px 5px}.subpart{margin:18px 0 24px;padding-bottom:12px;border-bottom:1px solid #e1e5ec}.subpart h4{margin:10px 0;font-size:19px;color:#213c5b}.solution-flow b{display:inline;background:none;border:0;padding:0;border-radius:0;font-size:inherit}.worked-example .math-display{border:0!important}.math-display{max-width:100%}@media(max-width:600px){.math-display{overflow-x:auto;padding:20px 4px}.math-display math{min-width:max-content;font-size:1.13em}}@media print{.math-display{overflow:visible;padding:8px 0}.math-display math{font-size:1.05em}}
''')
print('Replaced all61exercise prompts/solutions and25mock solutions with explicit prose/math records. No formula detection in final content.')
