from pathlib import Path
from html import escape as esc
from urllib.parse import quote
import fitz, json, shutil, re
from bs4 import BeautifulSoup

ROOT=Path.cwd(); OUT=ROOT/'output/html'; AS=OUT/'assets'; AS.mkdir(parents=True,exist_ok=True)
MID='[26 -27] ĐỀ CƯƠNG GIỮA KÌ 1 TOÁN 4.pdf'; TIMO='TIMOK4.pdf'
C1='4GE. CĐ1. Tính nhanh - Tìm thành phần chưa biết.pdf'; CS='[26-27]. Toán 4.CĐ2. Cấu tạo số.pdf'
THEORY={
'calc':('Biểu thức, tính nhanh và tìm x',C1,1,'''<p><b>Thứ tự tính:</b> trong ngoặc trước; nhân/chia trước cộng/trừ; các phép cùng mức làm từ trái sang phải. Thay chữ bằng số trước khi tính biểu thức chứa chữ.</p><p><b>Thừa số chung:</b> a×b+a×c=a×(b+c); a×b−a×c=a×(b−c). Một số đứng riêng là số đó nhân 1. Ví dụ bài 6a của lớp: 54×113+45×113+113=113×(54+45+1)=11 300.</p><p><b>Ghép cặp:</b> giữ nguyên dấu đi cùng số. Bài 8a: (2−4)+(6−8)+…+(18−20)+22=5×(−2)+22=12. Khi chưa học số âm, ghép (22−20)+(18−16)+…+(6−4)+2=12.</p><p><b>Tìm x:</b> coi cả cụm chứa x là một thành phần. Với x×2+375=5867: x×2=5867−375=5492; x=5492:2=2746. Thay lại để kiểm tra. Khi số bị trừ đã biết: 9035−x×5=760 ⇒ x×5=9035−760.</p><p><b>Dãy cách đều:</b> số số hạng=(cuối−đầu):khoảng cách+1; tổng=(đầu+cuối)×số số hạng:2. Chỉ áp dụng khi khoảng cách không đổi. Ví dụ 2,6,…,38 có 10 số, tổng 200.</p><p><b>Phép toán mới:</b> kí hiệu không phải phép nhân thông thường. Đọc định nghĩa, thay đúng a và b, rồi tính theo thứ tự. Không đổi chỗ a,b nếu đề không cho phép.</p>'''),
'number':('Cấu tạo số, hàng/lớp và làm tròn',CS,1,'''<p><b>Giá trị theo hàng:</b> abc=100a+10b+c. Mỗi lớp có ba hàng: đơn vị–chục–trăm; nghìn–chục nghìn–trăm nghìn; triệu–chục triệu–trăm triệu. Chữ số và giá trị của nó khác nhau: chữ số 5 ở hàng triệu có giá trị 5 000 000.</p><p><b>So sánh:</b> số có nhiều chữ số hơn lớn hơn; cùng số chữ số thì so từ trái sang phải. Số liền sau bằng số đã cho cộng 1. Số chẵn tận cùng 0,2,4,6,8; số lẻ tận cùng 1,3,5,7,9.</p><p><b>Làm tròn:</b> xác định hàng cần làm tròn; nhìn chữ số ngay bên phải. Nhỏ hơn 5 giữ nguyên; từ 5 trở lên tăng 1; các chữ số phía sau đổi thành 0. Ví dụ 751243 làm tròn trăm nghìn: chữ số chục nghìn là 5 ⇒ 800000.</p><p><b>Thêm chữ số:</b> thêm d bên phải số N được 10N+d. Nếu tăng K: 9N+d=K. Thêm chữ số 2 bên trái số có ba chữ số: số mới=2000+N, không phải 10N+2. Luôn kiểm tra số chữ số của N.</p><p><b>Số tròn chục trong khoảng:</b> liệt kê các bội 10 thỏa hai dấu bất đẳng thức; không lấy đầu mút nếu dấu là &lt;.</p>'''),
'div':('Chia hết, tận cùng, chu kì và quy luật','TN4. CĐ5. Dấu hiệu chia hết.pdf',1,'''<p><b>Chia hết:</b> cho 2 nếu tận cùng 0,2,4,6,8; cho 5 nếu tận cùng 0,5; cho 3 hoặc 9 nếu tổng chữ số chia hết cho 3 hoặc 9. Khi có nhiều điều kiện phải thỏa đồng thời. Ví dụ 2025A lẻ và chia hết 3: 9+A chia hết 3, A lẻ ⇒ A=3 hoặc 9; nhỏ nhất là 3.</p><p><b>Chữ số tận cùng của tích:</b> chỉ nhân chữ số hàng đơn vị, giữ lại chữ số hàng đơn vị sau mỗi phép nhân. 9 lặp chu kì 9,1; 4 lặp 4,6; 3 lặp 3,9,7,1. Chia số thừa số cho độ dài chu kì; dư 0 lấy phần tử cuối chu kì. 2025 thừa số 9 ⇒ tận cùng 9.</p><p><b>Chu kì:</b> tuần có 7 ngày. 44=6×7+2 nên lùi 44 ngày tương đương lùi 2 ngày. Với nhóm hình lặp, đếm số phần tử mỗi nhóm rồi xét thương và phần dư.</p><p><b>Dãy hiệu:</b> 3,4,8,15,25 có các hiệu 1,4,7,10; hiệu tăng 3 nên tiếp theo cộng 13 rồi 16 ⇒ 38,54. Không dùng công thức dãy cách đều cho dãy gốc này.</p>'''),
'geo':('Chu vi, diện tích và hình ghép',MID,1,'''<p><b>Hình vuông:</b> chu vi P=4×cạnh; cạnh=P:4; diện tích S=cạnh×cạnh. <b>Hình chữ nhật:</b> P=2×(dài+rộng); S=dài×rộng; rộng=S:dài. Chu vi ghi cm/m, diện tích ghi cm²/m².</p><p><b>Đổi diện tích:</b> m² → dm² → cm² → mm²: mỗi bước nhân 100; chiều ngược lại chia 100. 1m²=100dm²=10000cm²; 1cm²=100mm². 34dm²12cm²=3412cm². Không dùng hệ số 10 của độ dài.</p><p><b>Hình ghép:</b> đánh dấu cạnh bằng nhau; suy cạnh từ chu vi; chia hình thành hình chữ nhật/vuông hoặc lấy hình bao trừ phần bỏ đi. Không ước lượng chiều dài bằng mắt.</p><p><b>Diện tích cố định, cạnh nguyên:</b> liệt kê mọi cặp số tự nhiên có tích bằng diện tích, tính chu vi từng cặp rồi chọn lớn/nhỏ nhất. Với S=30: (1,30),(2,15),(3,10),(5,6); chu vi nhỏ nhất 22.</p><p><b>Từ khóa:</b> square=hình vuông; rectangle=hình chữ nhật; perimeter=chu vi; area=diện tích; identical=y hệt nhau; smallest=nhỏ nhất. Diện tích một ô có cạnh 2 là 4, không phải 2.</p>'''),
'word':('Bài nhiều bước, tiền và sơ đồ đoạn thẳng',MID,3,'''<p><b>Tiền:</b> thành tiền=số lượng×đơn giá; tổng tiền=cộng các khoản. Đơn giá=tổng tiền:số lượng. Giảm 1/4 hóa đơn nghĩa là trừ tổng:4, hoặc trả 3/4 tổng; không trừ 1/4 đồng.</p><p><b>Tổng–hiệu:</b> số lớn=(tổng+hiệu):2; số bé=(tổng−hiệu):2. Nếu lấy ở hai bao lượng khác nhau mà còn bằng nhau, hiệu ban đầu bằng chênh lệch lượng lấy đi. Vẽ đoạn thẳng trước khi tính.</p><p><b>Tổng–tỉ:</b> A gấp k lần B: B một phần, A k phần; tổng k+1 phần. Tổng–tỉ khác tổng–hiệu. Tuổi hai người cùng tăng một số năm nên hiệu tuổi không đổi.</p><p><b>Làm ngược:</b> đi từ kết quả cuối; đổi cộng thành trừ, nhân thành chia và ngược lại, theo thứ tự ngược. Với ((tuổi+4)×7−79):10=60: 60×10; cộng79; chia7; trừ4.</p><p><b>Bài sản lượng/số chuyến:</b> tìm chiều rộng → diện tích → lượng trên mỗi m² → tổng lượng → đổi đơn vị → số chuyến. Mỗi dòng ghi đơn vị và lời giải; kết thúc đáp số.</p>'''),
'units':('Góc, khối lượng, thời gian và thế kỉ',MID,1,'''<p><b>Góc:</b> nhọn nhỏ hơn 90°; vuông 90°; tù lớn hơn 90° nhưng nhỏ hơn 180°; bẹt 180°. Đếm theo từng đỉnh, mỗi cặp tia là một góc nhỏ hoặc bẹt. Đoạn có điểm ở giữa tạo hai tia đối nhau. Không chỉ đếm góc được đánh dấu.</p><p><b>Khối lượng:</b> 1 yến=10kg; 1tạ=10yến=100kg; 1tấn=10tạ=1000kg. Đổi hỗn hợp: 3tạ50kg=3×100+50=350kg. Đổi về tạ/yến chỉ sau khi cộng cùng đơn vị.</p><p><b>Thời gian:</b> 1giờ=60phút; 1phút=60giây; 1thế kỉ=100năm. 145giây=2phút25giây vì 145=2×60+25. 1/4giờ=60:4=15phút. Không đổi thời gian theo hệ số 100.</p><p><b>Năm thuộc thế kỉ:</b> thế kỉ I từ năm1 đến100; thế kỉ XIII từ1201 đến1300. Năm1226 thuộc XIII. Năm1900 thuộc XIX, năm1901 thuộc XX; không cộng1 nếu năm kết thúc bằng 00.</p>'''),
'count':('Đếm hình, đếm số, chắc chắn và đường đi',TIMO,5,'''<p><b>Đếm số:</b> hàng đầu không được 0; đọc kĩ có được lặp chữ số hay không. Hai chữ số đều nhỏ hơn5 và số chẵn: hàng chục 1,2,3,4 (4 cách); đơn vị 0,2,4 (3 cách) ⇒ 12 số.</p><p><b>Đếm bội:</b> số có hai chữ số chia hết3 là 12,15,…,99: (99−12):3+1=30 số. Phân biệt số lượng số với tổng các số.</p><p><b>Đếm hình chữ nhật chứa một ô:</b> chọn một đường trên, một đường dưới, một đường trái và một đường phải ô đó; nhân bốn số cách. Chỉ dùng khi các đường tạo đủ cạnh liên tục.</p><p><b>Chắc chắn:</b> nghĩ trường hợp bất lợi nhất. Muốn4 lá đỏ trong hộp 9xanh,6đỏ,10vàng: có thể lấy hết19 lá không đỏ trước, cần thêm4 ⇒ 23 lá. Muốn đủ ba màu: lấy hết hai màu nhiều nhất rồi thêm1.</p><p><b>Đường đi:</b> tại mỗi nút, ghi tổng số cách từ các nút có thể đi tới nó; điểm bắt đầu có1 cách; không cộng từ đường không tồn tại. Bậc thang bước1 hoặc2: F(n)=F(n−1)+F(n−2); bậc hỏng có0 cách. Quy ước F(0)=1.</p>''')}

EX={}
def add(k,title,q,sol,page,source=MID,fig=False): EX[k]=dict(title=title,q=q,sol=sol,page=page,source=source,fig=fig)
add('TN1','Viết số','Số gồm 3 triệu, 8 trăm nghìn, 3 chục và 6 đơn vị là số nào?','3 000 000+800 000+30+6=<b>3 800 036</b>. Các hàng không nêu có chữ số 0.',1)
add('TN2','Giá trị chữ số','Chữ số 5 trong 35 624 000 có giá trị bao nhiêu?','5 ở hàng triệu, lớp triệu nên có giá trị <b>5 000 000</b>.',1)
add('TN3','Sắp xếp số','Viết từ bé đến lớn: 16 642; 16 624; 16 743; 16 742.','Cùng phần 16 nghìn, so ba chữ số cuối: <b>16 624 &lt; 16 642 &lt; 16 742 &lt; 16 743</b>.',1)
add('TN4','Số chẵn','Số chẵn lớn nhất có 6 chữ số là số nào?','Số lớn nhất có6 chữ số là999999 nhưng lẻ. Giảm1 được <b>999998</b>.',1)
add('TN5','Làm tròn','Làm tròn 190 101 994 đến hàng trăm nghìn.','Hàng trăm nghìn là1; bên phải là0&lt;5 nên giữ1, đổi năm chữ số phía sau thành0: <b>190 100 000</b>.',1)
add('TN6','Số liền sau','Số liền sau của 888 889 là số nào?','888889+1=<b>888890</b>.',1)
add('TN7','Đếm góc — hình trang 1','Đếm góc vuông, nhọn, tù, bẹt trong hình gốc. Xem hình dưới đây.','Đếm theo đỉnh: A,B,C,D mỗi đỉnh có1vuông và2nhọn. E có2vuông (AED,DEC),1nhọn (BEC),2tù (AEB,BED),1bẹt (AEC). M có1bẹt (DMC). Tổng: <b>6vuông,9nhọn,2tù,2bẹt</b>. Dùng dấu vuông ở E và hình chữ nhật ABCD; không đếm góc lõm lớn hơn180°.',1,fig=True)
add('TN8','Thế kỉ','Nhà Trần thành lập năm 1226. Năm đó thuộc thế kỉ nào?','1201≤1226≤1300 ⇒ <b>thế kỉ XIII</b>.',2)
add('TN9','Đếm góc — hình trang 2','Đếm góc tù, nhọn, vuông, bẹt trong hình gốc.','A có5nhọn,1vuông; B,C,D mỗi đỉnh1vuông. M có2nhọn (BMA,CMN),3tù (BMN,CMA,AMN),1bẹt (BMC). N có3nhọn (CNM,DNA,MNA),2tù (CNA,DNM),1bẹt (CND). Tổng <b>5tù,10nhọn,4vuông,2bẹt</b>. Đếm một lần mỗi cặp tia, không đảo tên để đếm lần nữa.',2,fig=True)
add('TN10','Một phần giờ','1/4 giờ bằng bao nhiêu phút?','60:4=<b>15phút</b>.',2)
add('TN11','Đổi giây','3phút12giây bằng bao nhiêu giây?','3×60+12=<b>192giây</b>.',2)
add('TN12','Biểu thức chứa chữ','Tính 12:(3−m) với m=2.','Thay m=2: 12:(3−2)=12:1=<b>12</b>.',2)
add('TN13','Thuộc dãy','1243 thuộc dãy nào: A.10,20,30,…; B.0,2,4,…; C.0,5,10,…; D.1,3,5,…?','1243 tận cùng3 nên là số lẻ. Chọn <b>D</b>; không phải số chẵn hoặc bội5/10.',2)
add('TN14','Hình vuông','Hình vuông chu vi36cm có diện tích bao nhiêu?','Cạnh:36:4=9cm. Diện tích:9×9=<b>81cm²</b>.',2)
add('TN15','Thứ tự tính','Tính 50 000+2 000×5.','Nhân trước:2000×5=10000; 50000+10000=<b>60000</b>.',2)
add('TN16','Mua hàng','Hoa mua5quyển vở, mỗi quyển8000đồng và2hộp bút chì, mỗi hộp25000đồng. Tổng tiền?','Tiền vở:5×8000=40000đồng. Tiền bút:2×25000=50000đồng. Tổng=<b>90000đồng</b>.',2)
add('TN17','Hình chữ nhật','Rộng4m, dài gấp3lần rộng. Tính diện tích.','Dài:4×3=12m. Diện tích:12×4=<b>48m²</b>.',2)
add('TN18','Tuổi','5năm nữa cháu có tuổi là số nhỏ nhất có hai chữ số. Ông hơn cháu50tuổi. Năm nay ông bao nhiêu tuổi?','Số nhỏ nhất có2chữ số là10. Cháu nay:10−5=5tuổi. Ông nay:5+50=<b>55tuổi</b>.',2)
add('TN19','Số tròn chục','Tìm số tròn chục x, biết47&lt;x&lt;92.','Các bội10 nằm trong khoảng là <b>50,60,70,80,90</b>.',2)
add('TN20','Thừa số chung','Tính 12345×17+12345×23+35×12345+12345×24+12345.','Đưa12345 ra chung:12345×(17+23+35+24+1)=12345×100=<b>1234500</b>. Đừng bỏ số1 từ số hạng cuối.',2)
add('TL1','Sắp xếp — đủ hai ý','a) Từ bé đến lớn:3771;4374;2312;4333;8951.<br>b) Từ lớn đến bé:2883;3182;4992;1475;2471.','a) <b>2312;3771;4333;4374;8951</b>.<br>b) <b>4992;3182;2883;2471;1475</b>. So hàng nghìn trước, khi bằng nhau mới xét hàng thấp hơn.',2)
add('TL2','Hàng/lớp và làm tròn','Cho132000000;751243;6931452;37214083.<br>a) Chữ số2 thuộc hàng/lớp nào?<br>b) Làm tròn từng số đến trăm nghìn.','a) Theo thứ tự: <b>triệu/lớp triệu; trăm/lớp đơn vị; đơn vị/lớp đơn vị; trăm nghìn/lớp nghìn</b>.<br>b) <b>132000000;800000;6900000;37200000</b>. Chữ số chục nghìn lần lượt0,5,3,1; chỉ số thứ hai tăng hàng trăm nghìn.',2)
add('TL3','Giá trị chữ số và làm tròn','Cho854679;1194476;19432370.<br>a) Giá trị chữ số9 trong mỗi số?<br>b) Làm tròn đến chục nghìn.','a) <b>9;90000;9000000</b>.<br>b) <b>850000;1190000;19430000</b>. Xét chữ số hàng nghìn lần lượt4,4,2, đều nhỏ5 nên giữ hàng chục nghìn.',3)
add('TL4','Khối lượng — đủ sáu ý','1yến=…kg;20tấn=…tạ;1000kg=…tạ;2yến8kg=…kg;3tạ50kg=…kg;3tạ=…kg.','Theo thứ tự: <b>10kg;200tạ;10tạ;28kg;350kg;300kg</b>.<br>20×10=200;1000:100=10;2×10+8=28;3×100+50=350.',3)
add('TL5','Thời gian và diện tích — đủ sáu ý','2thế kỉ25năm=…năm;145giây=…phút…giây;315phút=…giờ…phút;3phút28giây=…giây;34dm²12cm²=…cm²;3170dm²=…m²…dm².','Theo thứ tự: <b>225năm;2phút25giây;5giờ15phút;208giây;3412cm²;31m²70dm²</b>.<br>2×100+25;145=2×60+25;315=5×60+15;3×60+28;34×100+12;3170=31×100+70.',3)
add('TL6','Tìm x — đủ bốn ý','a)x×2+375=5867<br>b)1353+x:3=2343<br>c)x×4−725=8259<br>d)9035−x×5=760','a)x×2=5867−375=5492 ⇒ <b>x=2746</b>.<br>b)x:3=2343−1353=990 ⇒ <b>x=2970</b>.<br>c)x×4=8259+725=8984 ⇒ <b>x=2246</b>.<br>d)x×5=9035−760=8275 ⇒ <b>x=1655</b>.<br>Kiểm tra lần lượt:5492+375=5867;1353+990=2343;8984−725=8259;9035−8275=760.',3)
add('TL7','Tính hợp lý — đủ hai ý','a)2345+4257−345<br>b)2024×14+2024×85+2024','a)(2345−345)+4257=2000+4257=<b>6257</b>.<br>b)2024×(14+85+1)=2024×100=<b>202400</b>.',3)
add('TL8','Thêm chữ số và tổng hai số','Tổng hai số3180. Viết thêm chữ số2 bên trái số bé được số lớn. Tìm hai số.','Số bé phải có3chữ số: nếu1hoặc2chữ số, tổng quá nhỏ; nếu4chữ số, tổng ít nhất22000. Khi có3chữ số, số lớn hơn số bé2000. Số bé=(3180−2000):2=<b>590</b>; số lớn=590+2000=<b>2590</b>. Kiểm tra tổng3180, viết2trước590 được2590.',3)
add('TL9','So sánh đơn giá','Hôm qua bán5kg cam thu100000đồng; hôm nay bán4kg thu100000đồng. Giá hôm nay cao hơn bao nhiêu nghìn đồng/kg?','Hôm qua:100000:5=20000đồng/kg. Hôm nay:100000:4=25000đồng/kg. Chênh:25000−20000=5000đồng=<b>5nghìn đồng/kg</b>.',3)
add('TL10','Diện tích và thu hoạch','Đất dài210m, dài gấp3lần rộng. Cứ3m² thu9kg sắn. Thu được bao nhiêu tạ?','Rộng:210:3=70m. Diện tích:210×70=14700m². Mỗi m² thu9:3=3kg. Thu hoạch:14700×3=44100kg. Đổi:44100:100=<b>441tạ</b>.',3)
add('TL11','Ba thùng dầu','Thùng thứ nhất435lít, hơn thùng thứ hai15lít, ít hơn thùng thứ ba58lít. Tổng dầu?','Thùng2:435−15=420lít. Thùng3:435+58=493lít. Tổng:435+420+493=<b>1348lít</b>.',3)
add('TL12','Diện tích và số chuyến','Đất dài15m,rộng8m. Mỗi1m² cần2tấn cát; mỗi chuyến chở8tấn. Cần bao nhiêu chuyến?','Diện tích:15×8=120m². Cát:120×2=240tấn. Số chuyến:240:8=<b>30chuyến</b>.',3)
add('TL13','Tổng–hiệu hai bao','Hai bao tổng147kg. Lấy bao1 ra5kg, bao2 ra22kg thì còn bằng nhau. Tìm khối lượng mỗi bao.','Bao2 ban đầu nhiều hơn bao1:22−5=17kg. Bao1=(147−17):2=<b>65kg</b>. Bao2=65+17=<b>82kg</b>. Kiểm tra:65−5=82−22=60kg.',4)
add('TL14','Đổi yến','7bao khoai tây, mỗi bao30kg;5bao khoai lang, mỗi bao20kg. Tổng bao nhiêu yến?','Khoai tây:7×30=210kg; khoai lang:5×20=100kg. Tổng310kg;310:10=<b>31yến</b>.',4)
add('TL15','Hóa đơn và giảm giá','Lan mua4mũ,55000đồng/mũ và3áo choàng,80000đồng/áo.<br>a)Tổng tiền?<br>b)Giảm1/4hóa đơn, còn trả bao nhiêu?','a)4×55000+3×80000=220000+240000=<b>460000đồng</b>.<br>b)Giảm460000:4=115000đồng. Trả460000−115000=<b>345000đồng</b>.',4)
add('TT16','Diện tích hình vuông nhỏ nhất','Hình vuông ban đầu chu vi64cm, cắt thành3hình vuông và2hình chữ nhật; AB=BD,BC=CD,DE=EF. Tính diện tích hình vuông nhỏ nhất. Xem hình nguồn.','Cạnh hình lớn AD=64:4=16cm. AB=BD nên AB=BD=8cm. BC=CD nên BC=CD=4cm. Trong ba hình vuông, hình dưới bên phải rộng BD=8cm nên cao8cm; hai hình vuông trên bên phải có cạnh CD=4cm nên DE=EF=4cm. Hai phần bên trái và giữa là hình chữ nhật. Diện tích hình vuông nhỏ nhất=4×4=<b>16cm²</b>.',4,fig=True)
add('TT17','Diện tích hình chữ H','Tính diện tích hình chữ H theo hình có cao8cm;hai cột rộng2cm; khoảng giữa4cm; phần khuyết trên/dưới sâu3cm.','Hình bao dài2+4+2=8cm, cao8cm, diện tích64cm². Hai phần khuyết:2×(4×3)=24cm². Diện tích H=64−24=<b>40cm²</b>. Cách2: hai cột2×(2×8)=32; thanh giữa cao8−3−3=2,rộng4,diện tích8; tổng40.',4,fig=True)
add('TT18','Ghép tám hình chữ nhật','8hình chữ nhật y hệt nhau, mỗi hình chu vi36,ghép thành hình vuông như hình nguồn. Tính chu vi hình vuông.','Gọi cạnh ngắn b,cạnh dài a. Hai hình đứng bên ngoài chồng lên nhau nên cạnh hình lớn L=2a. Theo ngang qua phần trên: L=b+a+b=a+2b. Suy ra a=2b. Chu vi hình chữ nhật:2(a+b)=36 ⇒ a+b=18 ⇒3b=18 ⇒ b=6,a=12. L=24; chu vi hình vuông=<b>96</b> (đề không ghi đơn vị).',4,fig=True)

# Các bài TIMO/chuyên đề được dùng ngoài đề thi thử.
add('C1-6a','Bài lớp đã có ảnh chữa','54×113+45×113+113','113×(54+45+1)=113×100=<b>11300</b>.',2,C1)
add('C1-8a','Bài lớp đã có ảnh chữa','2−4+6−8+10−12+14−16+18−20+22','Ghép(22−20)+(18−16)+(14−12)+(10−8)+(6−4)+2=6×2=<b>12</b>.',2,C1)
add('CS4','Thêm chữ số bên phải','Tìm số có3chữ số; thêm2bên phải thì tăng4106.','Gọi số N:10N+2−N=4106 ⇒9N=4104 ⇒<b>N=456</b>. Kiểm tra4562−456=4106.',1,CS)
add('CS10','Thêm chữ số — bài nguồn cần kiểm tra','Tìm số có2chữ số; thêm5bên phải thì số mới hơn số cũ230.','10N+5−N=230 ⇒9N=225 ⇒<b>N=25</b>. Kiểm tra255−25=230.',2,CS)
add('T1-1','Logic: dãy hiệu','Tìm số thứ7 của3,4,8,15,25,…','Hiệu1,4,7,10 tăng3. Hai hiệu tiếp13,16. Số6=38,số7=<b>54</b>.',6,TIMO)
add('T1-2','Logic: lịch','Hôm nay thứ Sáu;44ngày trước là thứ mấy?','44=6×7+2; lùi2ngày từ thứ Sáu được <b>thứ Tư</b>.',6,TIMO)
add('T1-4','Logic: hình lặp','Nhóm tròn đặc,vuông,tròn rỗng lặp lại. Có bao nhiêu hình vuông trong50hình đầu?','50=16×3+2. Có16nhóm đủ, mỗi nhóm1vuông;2hình dư gồm tròn đặc và vuông. Tổng=<b>17</b>.',6,TIMO)
add('T1-7','Tổng dãy','Tính2+6+10+…+30+34+38.','Số số hạng=(38−2):4+1=10. Tổng=(2+38)×10:2=<b>200</b>.',7,TIMO)
add('T1-8','Thừa số chung','Tính45×15+45×17−45×12.','45×(15+17−12)=45×20=<b>900</b>.',7,TIMO)
add('T1-9','Ghép cặp','Tính40−37+34−31+…+10−7+4−1.','14số tạo7cặp,mỗi cặp3; tổng=<b>21</b>. Đếm số:(40−1):3+1=14.',7,TIMO)
add('T1-11','Chia hết','Số chẵn lớn nhất có3chữ số chia hết3?','998 không chia hết3;996 có tổng chữ số24 và chẵn. Đáp án <b>996</b>.',7,TIMO)
add('T1-12','Chữ số tận cùng','Tìm tận cùng của tích2025thừa số9.','9lặp tận cùng9,1;2025lẻ nên tận cùng <b>9</b>.',7,TIMO)
add('T1-13','Phép toán mới','a⊗b=a×b+b×(a−3)+2. Tính9⊗5.','9×5+5×(9−3)+2=45+30+2=<b>77</b>.',7,TIMO)
add('T1-14','Điều kiện chữ số','2025A là số lẻ có5chữ số chia hết3. A nhỏ nhất?','Tổng chữ số9+A chia hết3 ⇒A=0,3,6,9. Cần lẻ ⇒3hoặc9. Nhỏ nhất=<b>3</b>.',7,TIMO)
add('T1-15','Tổng–tỉ','Ashley và Bell tổng18dây buộc tóc; Ashley gấp đôi Bell. Bell có bao nhiêu?','Bell1phần,Ashley2phần;tổng3phần. Bell=18:3=<b>6</b>.',8,TIMO)
add('T1-17','Diện tích phần còn lại','Hình vuông chu vi16cm ghép với2hình chữ nhật thành hình vuông chu vi24cm. Tổng diện tích hai hình chữ nhật?','Cạnh vuông nhỏ4cm,lớn6cm. Diện tích còn lại6×6−4×4=<b>20cm²</b>.',8,TIMO)
add('T1-18','Chu vi nhỏ nhất','Hình chữ nhật diện tích30,cạnh tự nhiên. Chu vi nhỏ nhất?','Cặp cạnh:(1,30),(2,15),(3,10),(5,6). Chu vi62,34,26,22. Nhỏ nhất=<b>22</b>.',8,TIMO)
add('T1-21','Trường hợp xấu nhất','Hộp9lá xanh,6lá đỏ,10lá vàng. Lấy ít nhất bao nhiêu để chắc có4lá đỏ?','Xấu nhất lấy hết19lá không đỏ trước. Cần thêm4lá đỏ ⇒ <b>23lá</b>.22lá chỉ đảm bảo3lá đỏ.',9,TIMO)
add('T1-22','Đếm số','Có bao nhiêu số chẵn hai chữ số mà cả hai chữ số đều nhỏ5?','Chục1,2,3,4;đơn vị0,2,4. 4×3=<b>12số</b>:10,12,14,20,22,24,30,32,34,40,42,44.',9,TIMO)
add('T1-23','Đếm bội','Có bao nhiêu số hai chữ số chia hết3?','Từ12đến99,khoảng cách3. (99−12):3+1=<b>30số</b>.',10,TIMO)
add('T6-2','Tổng–hiệu tuổi','Bố+mẹ79tuổi. Tuổi bố4năm nữa bằng tuổi mẹ7năm nữa. Mẹ nay?','Bố+4=mẹ+7 ⇒bố hơn mẹ3tuổi. Mẹ=(79−3):2=<b>38tuổi</b>.',29,TIMO)
add('T6-3','Làm ngược','Tuổi bà cộng4,nhân7,trừ79,chia10 thì được60. Tuổi bà?','Ngược:60×10=600;600+79=679;679:7=97;97−4=<b>93tuổi</b>.',29,TIMO)
add('T7-15','Thêm chữ số','Thêm1bên phải số hai chữ số thì tăng856. Số ban đầu?','9N+1=856 ⇒9N=855 ⇒ <b>N=95</b>. Kiểm tra951−95=856.',35,TIMO)

CSS='''*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#20313b;font:17px/1.7 system-ui,Arial,sans-serif}header{background:#153f4b;color:white;padding:35px max(20px,calc((100vw - 980px)/2))}header a{color:#c4f3ef}main{max-width:980px;margin:25px auto;padding:0 18px}h1{font-size:30px;line-height:1.3}h2{color:#145462;margin-top:32px}h3{line-height:1.4}p{margin:12px 0}a{color:#075f85}nav{display:flex;gap:14px;flex-wrap:wrap}.card,.exercise,.theory{background:white;border:1px solid #d8e1e5;border-radius:12px;padding:22px;margin:18px 0;break-inside:avoid}.source{font-size:14px;color:#506674}.note{background:#fff1d3;padding:15px;border-left:4px solid #bd7c12}.tag{background:#e1f2ef;padding:3px 10px;border-radius:20px;font-size:14px}table{width:100%;border-collapse:collapse;background:white}td,th{border:1px solid #d8e1e5;padding:10px;vertical-align:top;text-align:left}th{background:#e5f0f1}details{margin:16px 0;border-top:1px solid #d8e1e5;padding-top:12px}summary{cursor:pointer;color:#096c62;font-weight:650}img{max-width:100%;height:auto;border:1px solid #ddd}.figure{max-height:620px;object-fit:contain;display:block;margin:auto}textarea{width:100%;min-height:90px;border:1px solid #aebec5;border-radius:6px;font:inherit;padding:10px}.status{margin-top:12px;font-size:14px}select,button{font:inherit;padding:7px;border:1px solid #9db3bc;border-radius:6px;background:white;cursor:pointer}.toolbar{position:sticky;top:0;background:#f3f5f7;padding:10px;z-index:2}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px}.grid .card{margin:0}.write-lines{height:70px;background:repeating-linear-gradient(white,white 27px,#d7dfe3 28px)}.print-only{display:none}footer{padding:25px;text-align:center;font-size:14px;color:#506674}@media print{body{background:white;font-size:12pt}header{padding:10px;color:#20313b;background:white}header a,nav,.toolbar,button,.status,textarea,.no-print{display:none}main{max-width:none;margin:0;padding:0}h1{font-size:22pt}.card,.exercise,.theory{border-radius:0;padding:12px}.source{font-size:10pt}.print-only{display:block}.answers-hidden details.solution{display:none}.source-page{break-before:page}img{max-height:245mm}a{color:inherit;text-decoration:none}header h1{margin:0}}'''
JS='''document.querySelectorAll('[data-save]').forEach(el=>{const k='timo2026:'+location.pathname+':'+el.dataset.save;try{el.value=localStorage.getItem(k)||el.value}catch(e){}el.addEventListener('input',()=>{try{localStorage.setItem(k,el.value)}catch(e){}})});function showAnswers(v){document.querySelectorAll('details.solution').forEach(x=>x.open=v)}function printPack(answers){document.body.classList.toggle('answers-hidden',!answers);showAnswers(answers);window.print()}'''
(OUT/'style.css').write_text(CSS,encoding='utf-8');(OUT/'app.js').write_text(JS,encoding='utf-8')
def link(source,page):
 (OUT/'sources').mkdir(exist_ok=True)
 target=OUT/'sources'/source
 if not target.exists(): shutil.copy2(ROOT/'inputdata'/source,target)
 return 'sources/'+quote(source)+'#page='+str(page)
def cite(source,page):return f'<p class="source">Nguồn: <a href="{link(source,page)}">{esc(source)} · trang PDF {page}'+(f' · trang in {page-1}' if source==TIMO else '')+'</a></p>'
docs={}
def render(source,page):
 key=(source,page)
 if key not in docs:
  name=('mid' if source==MID else 'timo' if source==TIMO else 'class'+str(len(docs)))+f'-{page}.png'
  d=fitz.open(ROOT/'inputdata'/source); d[page-1].get_pixmap(matrix=fitz.Matrix(1.65,1.65)).save(AS/name); docs[key]=name
 return 'assets/'+docs[key]
def figure(k):
 e=EX[k]; page=e['page'];d=fitz.open(ROOT/'inputdata'/MID)
 clips={'TN7':(310,665,460,754),'TN9':(275,52,427,148),'TT16':(417,306,556,438),'TT17':(420,446,565,572),'TT18':(417,592,548,723)}
 path=AS/(k+'.png');d[page-1].get_pixmap(matrix=fitz.Matrix(2.3,2.3),clip=fitz.Rect(*clips[k])).save(path)
 return f'<a href="{render(MID,page)}"><img class="figure" src="assets/{k}.png" alt="Hình nguồn {k}; bấm để xem nguyên trang"></a>'
def exercise(k,repeat=False):
 e=EX[k]
 if re.fullmatch(r'T\d+-\d+',k):
  de,cau=k[1:].split('-'); label=f'Vòng loại · Đề {de} · Câu {cau}'
 elif k.startswith('TN'): label='Giữa kì · Trắc nghiệm · Câu '+k[2:]
 elif k.startswith('TL'): label='Giữa kì · Tự luận · Bài '+k[2:]
 elif k.startswith('TT'): label='Giữa kì · Thử thách · Bài '+k[2:]
 else: label='Bài chuyên đề '+k
 return f'''<article class="exercise" id="{k}"><span class="tag">{label}{' · ôn lại' if repeat else ''}</span><h3>{e['title']}</h3>{cite(e['source'],e['page'])}<p>{e['q']}</p>{figure(k) if e['fig'] else ''}<textarea aria-label="Bài làm {k}" data-save="work-{k}" placeholder="Con làm vào vở hoặc ghi lời giải ở đây…"></textarea><div class="write-lines print-only"></div><details class="solution"><summary>Xem lời giải từng bước</summary><p>{e['sol']}</p></details><div class="status">Kết quả: <select aria-label="Kết quả {k}" data-save="status-{k}"><option>Chưa làm</option><option>Tự làm đúng</option><option>Cần gợi ý</option><option>Sai — cần làm lại</option></select></div></article>'''
def theory(k):
 title,src,p,body=THEORY[k]
 return f'<section class="theory"><h3>{title}</h3>{cite(src,p)}{body}</section>'
def write(name,title,body,sub='Ôn TIMO 11/10 • Giữa kì 15/10 • Lớp 4'):
 soup=BeautifulSoup(body,'html.parser')
 for node in list(soup.find_all(string=True)):
  if node.parent.name=='a' and node.parent.get('href','').startswith('sources/'): continue
  txt=str(node)
  txt=re.sub(r'(?<=\d)(?=[A-Za-zÀ-ỹ])',' ',txt)
  txt=re.sub(r'(?<=[,;:→])(?=[A-Za-zÀ-ỹ0-9])',' ',txt)
  node.replace_with(txt)
 body=str(soup)
 (OUT/name).write_text(f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"></head><body><header><nav><a href="index.html">Mục lục</a><a href="toan-bo-de-cuong.html">Toàn bộ đề cương</a><a href="theo-doi.html">Theo dõi</a><a href="nguon.html">Nguồn</a></nav><h1>{title}</h1><p>{sub}</p></header><main><div class="toolbar"><button onclick="printPack(false)">In bài tập</button> <button onclick="printPack(true)">In kèm lời giải</button> <button onclick="showAnswers(true)">Mở lời giải</button> <button onclick="showAnswers(false)">Ẩn lời giải</button></div>{body}</main><footer>Trang PDF tính từ 1. Bài nguồn được giữ nguyên dữ kiện; lời giải biên soạn cho bộ ôn. Ghi chú/bài làm lưu trong trình duyệt này nếu trình duyệt cho phép.</footer><script src="app.js"></script></body></html>''',encoding='utf-8')

DAYS=[
('06-10.html','06/10 — Nền tảng tính nhanh và tìm x',['calc'],['TN12','TN15','TN20','TL6','TL7','T1-7','T1-8','T1-9','T1-13'],'10phút lý thuyết →20phút bài lớp →nghỉ5phút →15phút TIMO →10phút chữa.'),
('07-10.html','07/10 — Cấu tạo số, làm tròn và chia hết',['number','div'],['TN1','TN2','TN3','TN4','TN5','TN6','TN13','TN19','TL1','TL2','TL3','TL8','T7-15','T1-11','T1-14'],'10phút lý thuyết →25phút bài lớp →nghỉ5phút →10phút TIMO →10phút chữa. Nếu TL2–3 đã làm đúng ở lớp, kiểm tra miệng cách làm rồi chỉ viết lại ý sai.'),
('08-10.html','08/10 — Diện tích và hình ghép',['geo'],['TN14','TN17','TL5','TT16','TT17','TT18','T1-17','T1-18'],'10phút lý thuyết →25phút bài lớp →nghỉ5phút →10phút TIMO →10phút chữa. TL5 hôm nay chỉ làm hai ý diện tích; bốn ý thời gian làm thứ Bảy. TT18 đồng thời là TIMO đề7 câu20, PDF36.'),
('09-10.html','09/10 — Bài lời văn, tiền và tuổi',['word'],['TN16','TN18','TL9','TL11','TL13','TL15','T6-2','T6-3','T1-15'],'10phút lý thuyết →25phút bài lớp →nghỉ5phút →10phút TIMO →10phút chữa. Chọn hai trong ba câu TIMO; câu còn lại là bài dự phòng.'),
('10-10.html','10/10 — Bốn phiên học và thi thử',['units','word','div','count'],['TN7','TN8','TN9','TN10','TN11','TL4','TL5','TL14','TL10','TL12'],'Phiên1 sáng45phút: góc,thời gian,khối lượng. Nghỉ≥30phút. Phiên2 sáng40phút: TL10,12 và phần chưa xong. Sau nghỉ trưa, phiên3 thi thử60phút. Nghỉ≥30phút. Phiên4 chữa35phút. Tổng180phút học; tối nghỉ.'),
('11-10.html','11/10 — Thi TIMO: khởi động nhẹ',['calc','div'],['T1-8','T1-12'],'Chỉ5phút nhắc công thức +5phút một hoặc hai câu quen thuộc nếu thuận tiện. Không đọc toàn bộ phần lý thuyết trước giờ thi; sau thi nghỉ.'),
('12-10.html','12/10 — Củng cố số, góc và đổi đơn vị',['number','units','geo'],['TN1','TN2','TN3','TN4','TN5','TN6','TN7','TN8','TN9','TN10','TN11','TN12','TN13','TN19','TL1','TL2','TL3','TL4','TL5','TL8','TL14'],'10phút nhắc lý thuyết →30phút làm lại bài sai/chưa làm →nghỉ5phút →15phút chữa. Đây là danh sách rà soát; bài đúng chỉ kiểm tra nhanh, không bắt chép lại tất cả.'),
('13-10.html','13/10 — Củng cố tìm x, lời văn và hình ghép',['calc','word','geo'],['TN14','TN15','TN16','TN17','TN18','TN20','TL6','TL7','TL9','TL10','TL11','TL12','TL13','TL15','TT16','TT17','TT18'],'10phút nhắc lý thuyết →30phút làm lại bài sai/chưa làm →nghỉ5phút →15phút chữa. Đánh dấu đủ từng ý; ưu tiên hoàn tất đề cương trước kiểm tra ngày14/10.'),
('14-10.html','14/10 — Kiểm tra tổng hợp giữa kì',['number','calc','units','geo','word'],['TN2','TN5','TN13','TN9','TN8','TN10','TL4','TL5','TN12','TN20','TL6','TL8','TL15','TL13','TN14','TL12','TT17'],'35phút kiểm tra →nghỉ5phút →15phút chữa →5phút xem lỗi. Các câu đều trích từ tài liệu đã có, không phải đề mới hoặc đề chính thức. Chỉ làm TL4:3tạ50kg; TL5:145giây và3170dm²; TL6:ý d; TL15:ý b. Nếu còn bài chưa làm, hoàn tất chúng trước.'),
('15-10.html','15/10 — Thi giữa kì: khởi động nhẹ',['units','calc'],['TN11','TN15'],'5–10phút: nhắc đơn vị và thứ tự phép tính, làm một hoặc hai câu quen thuộc nếu thuận tiện. Không dùng hết một giờ trong ngày thi.')]

for name,title,ths,ks,timing in DAYS:
 body=f'<p class="note"><b>Khung buổi học:</b> {timing}</p>'
 if name=='06-10.html':body+='<p class="note">Hôm nay đã07/10. Nếu chưa học phần này: tối07/10 lấy10phút đầu ôn TN12,15 và ví dụ thừa số chung; thay hai câu TIMO bằng T1-8. Các ý TL6–7 còn lại làm phiên sáng2 thứ Bảy hoặc buổi13/10. Không cộng thêm giờ vào tối ngày thường.</p>'
 body+='<h2>1. Kiến thức cần nhớ</h2>'+''.join(theory(k) for k in ths)
 if name=='10-10.html':body+='<p class="note">Phần chu kì/tận cùng và đếm là tài liệu chữa sau thi thử. Trước thi thử chỉ đọc lý thuyết nếu con đã học dạng đó; không mở đề2 hoặc đáp án trước phiên chiều.</p>'
 body+='<h2>2. Bài luyện tập từ tài liệu</h2><p>Làm vào vở, nêu cách làm trước khi mở lời giải. Ghi kết quả từng bài để buổi sau chọn đúng bài cần chữa.</p>'+''.join(exercise(k,name in ['12-10.html','13-10.html']) for k in ks)
 if name=='10-10.html':body+='<h2>3. Thi thử và chữa</h2><p><a href="thi-thu-timo.html">Mở đề TIMO vòng loại số2 — 25câu</a></p><p><a href="chua-timo.html">Chỉ mở trang chữa sau khi kết thúc60phút</a></p>'
 if name=='14-10.html':body+='<p class="note">Đây là phiếu kiểm tra dùng lại câu nguồn nên điểm phản ánh mức nhớ/củng cố; không dùng để dự đoán chắc chắn điểm thi. Lý thuyết đọc sau khi kết thúc35phút. Mỗi thẻ có một mã nguồn, nhưng thẻ nhiều ý chỉ làm các ý đã ghi trong khung buổi học.</p>'
 body+='<h2>3. Chốt buổi</h2><p>Con nói lại một quy tắc, chọn một lỗi cần tránh và tự giải lại câu sai không nhìn lời giải. Với bài cần gợi ý, giữ trạng thái đó đến khi tự làm được.</p><textarea data-save="daily-error" aria-label="Lỗi cuối buổi" placeholder="Bài nào sai? Vì sao? Ngày nào làm lại?"></textarea>'
 write(name,title,body)

midkeys=[f'TN{i}' for i in range(1,21)]+[f'TL{i}' for i in range(1,16)]+[f'TT{i}' for i in range(16,19)]
write('toan-bo-de-cuong.html','Đề cương giữa kì — đủ 38 câu/bài', '<p class="note">Bao gồm mọi ý của20câu trắc nghiệm,15bài tự luận,3bài thử thách. Đây là ngân hàng đối chiếu, không giao làm hết trong một buổi.</p>'+''.join(exercise(k) for k in midkeys))

mockanswers=['A','C','D','B','A','B','A','B','A','C','C','C','A','A','B','B','A','C','C','C','A','D','B','D','B']
mocksol=[
'Nhóm4lá cờ có1lá Việt Nam.41=10×4+1; lá dư đầu tiên là Việt Nam.10+1=11lá.',
'Ngày mai Chủ nhật ⇒hôm nay thứ Bảy.50=7×7+1; tiến1ngày ⇒Chủ nhật.',
'Giả sử42con đều là gà:84chân.Thiếu108−84=24chân;mỗi ngựa hơn gà2chân.24:2=12ngựa.',
'Các hiệu2,4,6,8,10,12,14. Số thứ6=33,thứ7=45,thứ8=59.',
'Làm ngược:trước ngày3 có15+25=40chiếc;trước ngày2 có40×2=80;ban đầu80+29=109.',
'150:3+150:5+150:10=50+30+15=95.',
'Có(30−3):3+1=10số;tổng(3+30)×10:2=165.',
'212×(25+90−15)=212×100=21200.',
'28số ghép14cặp,mỗi cặp2 ⇒28.',
'Theo hình phép cộng:2C tận cùng6 và có nhớ ⇒C=8.2B+1=7 hoặc17 ⇒B=3hoặc8. B khác C nên B=3; khi đó A=2.',
'Chọn nghìn9,trăm8,chục7 để lớn nhất;đơn vị5thỏa chia hết5 và không trùng ⇒9875.',
'Tận cùng tích4 lặp4,6.2024chẵn ⇒6.',
'(3×2−4)×(6:3+8)=2×10=20.',
'M9phần,N1phần;tổng10phần,mỗi phần30:10=3;M=27.',
'Tổng chữ số8+X chia hết3 ⇒X=1,4,7;chẵn ⇒X=4.',
'Có2đường trên,2đường dưới,4đường trái,1đường phải lá cờ.2×2×4×1=16hình.',
'Vuông nhỏ cạnh3vì3×3=9. Hình chữ nhật dài9,rộng(9−3):2=3. Chu vi2×(9+3)=24cm.',
'Cặp cạnh(1,24),(2,12),(3,8),(4,6) cho chu vi50,28,22,20. Lớn nhất50.',
'Nguồn lời giải đánh số13mặt phía trước; hai mặt3và10 bị che bởi2và9. Nhìn thẳng phía trước còn13−2=11mặt. Đối chiếu hình đánh số bên dưới.',
'Tách thuyền: cột buồm rộng1,cao5 ⇒5cm²; cánh buồm tam giác đáy2,cao4 ⇒4cm² (ghép hai tam giác thành chữ nhật2×4 rồi lấy nửa); thân thuyền hình thang đáy9và5,cao2 ⇒14cm² (cắt ghép thành chữ nhật7×2). Tổng5+4+14=23cm². Lời giải nguồn bỏ cột buồm trong câu cộng hai phần; kết quả23vẫn đúng.',
'Bất lợi nhất lấy hết8xanh+7đen=15chiếc mà chưa có đỏ. Lấy thêm1chắc chắn đỏ ⇒16chiếc để đủ ba màu.',
'Liệt kê39,48,57,66,75,84,93 ⇒7số. Không có hai chữ số0và12.',
'10,15,…,95 có(95−10):5+1=18số.',
'Số cách từ bậc0đến10:1,1,2,3,5,8,13,0,13,13,26. Bậc7hỏng gán0,không xóa bậc khỏi hệ thống. Đáp án26.',
'Ghi1tại điểm xuất phát; mỗi nút bằng tổng số cách từ nút bên trái và dưới có đường nối tới. Đường thiếu không góp số cách. Tính lần lượt theo hình đánh số trong trang lời giải PDF70 ⇒23cách.'
]
body='<p class="note">Thi thử thứ Bảy10/10:60phút. Không đọc lý thuyết hoặc mở lời giải trong thời gian làm. Dùng thời lượng BTC nếu thông báo khác. Các trang bên dưới giữ nguyên25câu và mọi hình nguồn.</p><h2>Đề gốc — đủ 5 trang</h2>'
for page in range(11,16):body+=f'<section class="source-page">{cite(TIMO,page)}<img src="{render(TIMO,page)}" alt="Đề vòng loại2 trang PDF{page}"></section>'
body+='<h2>Phiếu trả lời</h2><table><tr><th>Câu</th><th>Đáp án của con</th></tr>'
for i in range(1,26):body+=f'<tr><td>{i}</td><td><select data-save="mock-{i}" aria-label="Đáp án câu{i}"><option value="">Chưa chọn</option>'+''.join(f'<option>{x}</option>' for x in 'ABCD')+'</select></td></tr>'
body+='</table><p><a href="chua-timo.html">Kết thúc thi thử rồi mới mở lời giải</a></p>'
write('thi-thu-timo.html','Thi thử TIMO — vòng loại đề số 2',body)
body='<p class="note">Chỉ mở sau thi thử. Đáp án đối chiếu lời giải PDF66–70; riêng câu20 được bổ sung phép cộng cột buồm5cm². Chọn tối đa3lỗi để chữa trong phiên35phút.</p><h2>Lý thuyết để chữa</h2>'+''.join(theory(k) for k in ['calc','div','geo','word','count'])+'<h2>Đáp án và lời giải25câu</h2>'
for i,sol in enumerate(mocksol,1):
 pp=66 if i<=5 else 67 if i<=12 else 68 if i<=18 else 69 if i<=23 else 70
 qp=11 if i<=5 else 12 if i<=13 else 13 if i<=18 else 14 if i<=22 else 15
 body+=f'<article class="exercise" id="mock-{i}"><h3>Câu{i} — đáp án {mockanswers[i-1]}</h3>{cite(TIMO,qp)}<p class="source">Lời giải nguồn: trang PDF{pp}, trang in{pp-1}.</p><p>{sol}</p><textarea aria-label="Lỗi câu{i}" data-save="error-{i}" placeholder="Con sai ở bước nào? Giải lại vào vở."></textarea></article>'
body+='<h2>Hình và lời giải gốc để đối chiếu</h2>'
for p in range(66,71):body+=f'<details><summary>Lời giải nguồn PDF{p}</summary><img src="{render(TIMO,p)}" alt="Trang lời giải PDF{p}"></details>'
write('chua-timo.html','Chữa thi thử TIMO — 25 câu',body)

first={}
for name,title,ths,ks,timing in DAYS:
 for k in ks:first.setdefault(k,(name,title[:5]))
body='<p>Mỗi bài có ngày ôn đầu và mọi ý cần đánh dấu. Trạng thái ở trang này lưu riêng trong trình duyệt; phụ huynh nhập sau khi kiểm tra vở, không tự coi đã hoàn thành vì bài xuất hiện trong lịch.</p><table><tr><th>Mã / nguồn</th><th>Ngày đầu</th><th>Ý phải kiểm tra</th><th>Kết quả</th></tr>'
parts={'TL1':['a','b'],'TL2':['a—4số','b—4số'],'TL3':['a—3số','b—3số'],'TL4':['1yến','20tấn','1000kg','2yến8kg','3tạ50kg','3tạ'],'TL5':['thế kỉ','145giây','315phút','3phút28giây','34dm²12cm²','3170dm²'],'TL6':['a','b','c','d'],'TL7':['a','b'],'TL15':['a','b']}
for k in midkeys:
 name,date=first[k];opts=parts.get(k,['toàn bài'])
 for j,part in enumerate(opts):body+=f'<tr><td><a href="toan-bo-de-cuong.html#{k}">{k}</a> · PDF{EX[k]["page"]}</td><td><a href="{name}#{k}">{date}</a></td><td>{part}</td><td><select data-save="cover-{k}-{j}" aria-label="Theo dõi{k} {part}"><option>Chưa làm</option><option>Đúng độc lập</option><option>Cần gợi ý</option><option>Sai, làm lại</option><option>Đã sửa và làm lại đúng</option></select></td></tr>'
body+='</table><p class="note">TL2,TL3 kiểm tra đủ từng số trong từng ý. Trước14/10 rà soát mọi hàng “Chưa làm”. Nếu chưa xong, dùng buổi14/10 để hoàn thành trước phiếu kiểm tra.</p>'
write('theo-doi.html','Theo dõi bao phủ đề cương giữa kì',body)

body='<p>Trang PDF tính từ1. TIMOK4 có một trang bìa nên trang in=trang PDF−1. Link PDF mở bản sao nguồn kèm trong thư mục sources; ảnh nguồn cũng được kèm. Sao chép cả thư mục html để giữ đầy đủ hình và PDF.</p><h2>Tài liệu chính</h2>'
for src in [MID,TIMO,C1,CS,'TN4. CĐ 2. DÃY SỐ.pdf','TN4. CĐ5. Dấu hiệu chia hết.pdf','4GE. CĐ2. Dạng toán liên quan đến chữ số tận cùng.pdf','TN4. CĐ4. TỔNG HIỆU.pdf']:
 body+=cite(src,1)
body+='<h2>Căn cứ lý thuyết bổ sung</h2><p>Chu kì/tận cùng: phiếu Chữ số tận cùng PDF1; quy luật/dãy: phiếu Dãy số PDF1–2; tổng–hiệu: phiếu Tổng hiệu PDF1; đếm/đường đi: TIMO khung chương trình PDF5 và lời giải vòng loại đề2 PDF68–70. Các giải thích và bước giải trong HTML là biên soạn lại từ dữ kiện nguồn.</p><h2>Ảnh lời giải trên lớp</h2><p>Thư mục “Bài6,Bài8 Chuyên đề Tính nhanh +Tìm X” gồm10ảnh. Có bài6a–i và8a–d đã chữa; đây không phải bằng chứng con tự làm đúng.</p><h2>Đề cương gốc</h2>'
for p in range(1,5):body+=f'<details><summary>Giữa kì PDF{p}</summary><img src="{render(MID,p)}" alt="Đề cương gốc trang{p}"></details>'
write('nguon.html','Nguồn và cách đối chiếu',body)

body='''<p class="note"><b>Hai mốc:</b> TIMO Chủ nhật11/10/2026; giữa kì thứ Năm15/10/2026. Ngày thường60phút; thứ Bảy4phiên tổng180phút. Hôm nay07/10: nếu chưa học06/10, xem hướng dẫn bù trong buổi nền tảng, không dồn thêm giờ tối.</p><h2>Mở từng ngày</h2><div class="grid">'''
for name,title,ths,ks,timing in DAYS:body+=f'<article class="card"><h3><a href="{name}">{title}</a></h3><p>{timing}</p></article>'
body+='</div><h2>Cách dùng</h2><ol><li>Mở buổi học; đọc phần lý thuyết đúng cụm, không đọc tất cả ngân hàng.</li><li>Con làm vào vở hoặc ô bài làm; phụ huynh chỉ mở lời giải sau khi con thử.</li><li>Đánh dấu đúng/cần gợi ý/sai; cập nhật bảng theo dõi từng ý.</li><li>Ngày rà soát chỉ làm lại bài sai/chưa làm. Các buổi có nhiều thẻ là danh sách bao phủ, không yêu cầu chép lại mọi bài đúng.</li><li>In bài tập ẩn lời giải; in kèm lời giải dành cho phụ huynh. Không cần mạng.</li></ol><p><a href="thi-thu-timo.html">Đề thi thử TIMO2</a> · <a href="chua-timo.html">Lời giải thi thử</a> · <a href="toan-bo-de-cuong.html">Đủ38câu/bài giữa kì</a> · <a href="theo-doi.html">Theo dõi từng ý</a></p><p>Không có kết quả cá nhân ban đầu; lịch chọn lỗi theo bài làm thực tế. Phạm vi giữa kì theo đề cương đã cung cấp; tài liệu trường bổ sung cần cập nhật tiếp.</p>'
write('index.html','Bộ ôn TIMO và giữa kì — lớp 4',body)
(OUT/'manifest.json').write_text(json.dumps({'days':len(DAYS),'midterm_exercises':len(midkeys),'exercises':len(EX),'mock_questions':25,'sources':list({e['source'] for e in EX.values()})},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(list(OUT.glob("*.html")))} HTML files; {len(midkeys)} midterm exercises; {len(EX)} exercises total; 25-question mock.')
