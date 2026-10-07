from pathlib import Path
from bs4 import BeautifulSoup
from html import escape

root=Path('output/html')
# These small examples are explicitly teacher-authored, not attributed to source worksheets.
lessons=[
('tinh','Tính nhanh: nhìn nhóm trước khi tính', 'Con có 7 túi, mỗi túi 3 viên bi, rồi thêm 7 túi, mỗi túi 2 viên. Có cần tính riêng hai lần không?',
 'Vẽ 7 nhóm; trong mỗi nhóm đặt 3 chấm xanh và 2 chấm đỏ. Mỗi nhóm có 5 chấm. Vì số nhóm bằng nhau nên ta gộp số bi trong mỗi nhóm.',
 '7 × 3 + 7 × 2 = 7 × (3 + 2) = 35. Số 7 là số nhóm; 3 + 2 là số bi của mỗi nhóm. Với 2024 × 14 + 2024 × 85 + 2024, số cuối chính là 2024 × 1. Có 14 + 85 + 1 = 100 nhóm, nên kết quả là 202 400.',
 '8 × 12 + 8 × 8; 25 × 19 + 25; 50 000 + 2 000 × 5.',
 '160; 500; 60 000. Câu cuối phải nhân trước cộng. Chỉ gộp khi các tích có cùng một thừa số.',
 'Nếu con bỏ số 2024 cuối, hỏi: “Một túi đứng riêng là mấy túi?” Nếu con nhân cả tổng ở câu cuối, yêu cầu khoanh phép nhân trước.',
 'Con chỉ ra số nhóm chung và giải thích được vì sao số đứng riêng tương ứng với 1 nhóm.', '06-10.html', 'TL7'),
('x','Tìm x: lần ngược đường đi', 'Một số được nhân 2, rồi cộng 375, được 5867. Muốn tìm số ban đầu, con tháo bước nào trước?',
 'Vẽ đường đi: [số ban đầu] → × 2 → [kết quả giữa] → + 375 → 5867. Đi ngược từ đích: trừ 375 rồi chia 2.',
 'x × 2 + 375 = 5867. Tích x × 2 là 5867 − 375 = 5492. Do đó x = 5492 : 2 = 2746. Thử lại: 2746 × 2 + 375 = 5867. Với 9035 − x × 5 = 760: phần bị bớt là 9035 − 760 = 8275, nên x = 8275 : 5 = 1655.',
 'x × 3 + 12 = 72; 100 − x × 4 = 20.',
 'x = 20 ở cả hai câu. Thử lại lần lượt được 72 và 20.',
 'Nếu con tính (760 − 9035) : 5, dùng 10 − □ = 3 để con nhận ra ô trống là 7; sau đó quay lại bài lớn. Không dùng lời nhắc “chuyển vế đổi dấu”.',
 'Con gọi tên được phần chưa biết, tìm đúng phần đó và thay lại để kiểm tra.', '06-10.html','TL6'),
('so','Cấu tạo số và làm tròn: mỗi chữ số có một chỗ', 'Trong 35 624 000, chữ số 5 là 5 đơn vị hay 5 triệu? Vì sao?',
 'Viết 35 | 624 | 000: lớp triệu | lớp nghìn | lớp đơn vị. Trong mỗi lớp, đọc từ trái sang phải: trăm, chục, đơn vị. Đặt chữ số vào bảng hàng để nhìn thấy những chỗ có số 0.',
 '3 triệu + 8 trăm nghìn + 3 chục + 6 đơn vị = 3 800 036. Không ghép các chữ số thành 3836 vì các hàng trống vẫn cần số 0. Làm tròn 751 243 đến trăm nghìn: số nằm giữa 700 000 và 800 000; mốc giữa là 750 000. Số đã cho vượt mốc giữa nên làm tròn thành 800 000. Sau khi hiểu mốc giữa, dùng chữ số chục nghìn: từ 5 trở lên thì tăng hàng trăm nghìn 1 đơn vị.',
 'Giá trị chữ số 2 trong 6 931 452; làm tròn 854 679 đến chục nghìn; số chẵn lớn nhất có 6 chữ số.',
 '2 đơn vị; 850 000 (so với mốc 855 000); 999 998.',
 'Nếu con viết 3836, đưa bảng hàng và hỏi vị trí hàng nghìn, hàng trăm. Nếu con làm tròn sai, viết hai số tròn kề nhau và mốc giữa trước khi nhắc quy tắc.',
 'Con phân biệt chữ số với giá trị chữ số; xác định được hàng làm tròn và hàng ngay bên phải.', '07-10.html','TN1'),
('chu-so','Thêm chữ số: thử số nhỏ để hiểu sự thay đổi', 'Viết thêm 2 bên phải 34 được bao nhiêu? Viết bên trái được bao nhiêu? Hai cách có giống nhau không?',
 'Bên phải: 34 → 342 = 340 + 2. Bên trái: 34 → 234 = 200 + 34. Làm tiếp với số 590 để thấy số chữ số của số cũ quyết định giá trị chữ số thêm bên trái.',
 'Đề cương TL8: tổng hai số là 3180; thêm 2 bên trái số bé được số lớn. Nếu số bé có 1 hoặc 2 chữ số, tổng lớn nhất lần lượt là 38 hoặc 398, đều chưa đủ. Nếu có 4 chữ số trở lên thì số lớn ít nhất 20 000, quá tổng. Vậy số bé có 3 chữ số; số lớn hơn số bé 2000. Bớt 2000 ở tổng, còn 1180 là hai lần số bé. Số bé = 1180 : 2 = 590; số lớn = 2590. Thử: 590 + 2590 = 3180.',
 'Thêm 4 bên phải 27; thêm 4 bên trái 27; hai số có tổng 568, số lớn nhận được bằng cách thêm 5 bên trái số bé có hai chữ số. Tìm hai số.',
 '274; 427; số bé 34, số lớn 534. Kiểm tra tổng 568 và thao tác thêm chữ số.',
 'Nếu con luôn nhân 10 khi thêm chữ số, cho con thực hiện cả hai thao tác trên thẻ số 27 và đọc số mới thành tiếng.',
 'Con phân biệt thêm trái/thêm phải và kiểm tra số tìm được có đúng số chữ số yêu cầu.', '07-10.html','TL8'),
('hinh','Chu vi và diện tích: đi quanh hay phủ kín?', 'Một sợi dây quấn quanh tấm bìa và giấy màu phủ mặt bìa đo hai điều gì khác nhau?',
 'Vẽ hình chữ nhật 4 hàng, mỗi hàng 6 ô vuông. Đếm 24 ô để hiểu diện tích; đi quanh bốn cạnh để thấy chu vi là 6 + 4 + 6 + 4 = 20. Mỗi ô cạnh 1 cm có diện tích 1 cm².',
 'TN14: hình vuông có chu vi 36 cm. Bốn cạnh bằng nhau nên mỗi cạnh là 36 : 4 = 9 cm. Diện tích là 9 × 9 = 81 cm². TN17: rộng 4 m, dài gấp 3 lần rộng, nên dài 4 × 3 = 12 m; diện tích 12 × 4 = 48 m². Với hình ghép, đánh dấu cạnh đã biết, tìm cạnh thiếu rồi chia thành hình chữ nhật; mỗi phần chỉ tính một lần.',
 'Hình chữ nhật dài 8 cm, rộng 3 cm: tìm chu vi và diện tích. Hình vuông chu vi 20 cm: tìm diện tích.',
 '22 cm và 24 cm²; hình vuông có cạnh 5 cm nên diện tích 25 cm².',
 'Nếu con lấy 36 × 36, hỏi 36 là một cạnh hay cả đường đi quanh. Nếu con cộng diện tích bị chồng, tô màu từng phần để nhận ra vùng tính hai lần.',
 'Con phân biệt hai đại lượng, tìm cạnh trước khi tính và ghi đúng cm hoặc cm².', '08-10.html','TN14'),
('loi-van','Bài lời văn: mỗi phép tính trả lời một câu hỏi', 'Hoa mua hai loại đồ. Muốn biết trả bao nhiêu tiền, con cần biết những khoản tiền nào?',
 'Lập bảng: vở | 5 quyển | 8000 đồng/quyển; bút | 2 hộp | 25 000 đồng/hộp. Viết tên đại lượng bên cạnh mỗi phép tính; dùng sơ đồ đoạn thẳng khi đề nói hơn, kém hoặc bằng nhau.',
 'TN16: tiền vở = 8000 × 5 = 40 000 đồng; tiền bút = 25 000 × 2 = 50 000 đồng; tổng = 90 000 đồng. TN18: 5 năm nữa cháu 10 tuổi, nên hiện nay cháu 10 − 5 = 5 tuổi; ông hiện nay 5 + 50 = 55 tuổi. Hiệu tuổi không đổi vì mỗi năm cả hai cùng tăng 1 tuổi. TL13: hai bao còn bằng nhau sau khi lấy 5 kg và 22 kg. Tổng còn lại = 147 − 5 − 22 = 120 kg; mỗi bao còn 60 kg. Ban đầu hai bao lần lượt 65 kg và 82 kg.',
 'Mua 3 vở giá 9000 đồng và 2 bút giá 6000 đồng. Hai bao tổng 50 kg, lấy lần lượt 4 kg và 6 kg thì còn bằng nhau. Tìm khối lượng ban đầu.',
 '39 000 đồng; hai bao còn 20 kg mỗi bao, ban đầu 24 kg và 26 kg.',
 'Nếu con chọn phép tính theo từ “nhiều hơn” mà không biết ai nhiều, hỏi con chỉ vào đối tượng trên sơ đồ. Nếu con dừng ở tổng còn lại, hỏi đề cần khối lượng trước hay sau khi lấy.',
 'Con nói được mỗi phép tính tìm gì và đối chiếu đáp số với mọi dữ kiện.', '09-10.html','TL13'),
('don-vi','Đổi đơn vị: hiểu một đơn vị chứa bao nhiêu', 'Một giờ có 60 phút. Vậy 2 giờ 15 phút có thể bằng 215 phút không?',
 'Vẽ hình vuông cạnh 1 dm = 10 cm, chia thành 10 hàng, mỗi hàng 10 ô vuông cạnh 1 cm. Có 100 ô nên 1 dm² = 100 cm². Viết riêng các quan hệ: 1 giờ = 60 phút; 1 tạ = 100 kg; 1 tấn = 10 tạ; 1 yến = 10 kg.',
 '3 phút 12 giây = 3 × 60 + 12 = 192 giây. 145 giây = 2 phút 25 giây vì 145 = 2 × 60 + 25. 34 dm² 12 cm² = 34 × 100 + 12 = 3412 cm². 3170 dm² = 31 m² 70 dm² vì 3170 = 31 × 100 + 70. Năm 1226 thuộc thế kỉ XIII vì nằm trong 1201–1300; năm 1200 vẫn thuộc thế kỉ XII.',
 '3 tạ 50 kg = … kg; 315 phút = … giờ … phút; 2 m² 8 dm² = … dm²; năm 2000 thuộc thế kỉ nào?',
 '350 kg; 5 giờ 15 phút; 208 dm²; thế kỉ XX.',
 'Nếu con đổi diện tích theo 10, quay lại hình 10 × 10 ô. Nếu con đổi thời gian theo 100, dùng mặt đồng hồ. Không dạy một mẹo thêm số 0 cho mọi loại đơn vị.',
 'Con nêu quan hệ giữa hai đơn vị trước khi đổi, kiểm tra phần dư nhỏ hơn 60 hoặc 100 tương ứng.', '10-10.html','TL5'),
('quy-luat','Quy luật và chu kì: tìm điều lặp lại', 'Dãy Đỏ – Xanh – Vàng lặp lại. Vị trí thứ 12 và thứ 14 có màu gì? Con có cần viết đủ 14 màu không?',
 'Đánh số từng nhóm: vị trí 1–3, 4–6, 7–9, 10–12. Mỗi nhóm kết thúc bằng Vàng. Vị trí 13 bắt đầu nhóm mới nên là Đỏ, vị trí 14 là Xanh.',
 '14 : 3 = 4 dư 2: bỏ 4 nhóm đủ, còn vị trí thứ 2 là Xanh. 12 : 3 = 4 dư 0: vị trí cuối nhóm là Vàng. Với dãy 2, 5, 8, 11, …, hiệu liên tiếp luôn là 3. Số thứ 6 = 2 + 5 × 3 = 17 vì từ số thứ 1 đến số thứ 6 chỉ có 5 bước.',
 'Màu thứ 20 và thứ 21 trong chu kì trên; số thứ 8 của dãy 4, 8, 12, 16, …; tổng 1 + 2 + 3 + 4 + 5 + 6.',
 'Xanh; Vàng; 32; tổng 21 bằng 3 cặp (1 + 6), (2 + 5), (3 + 4), mỗi cặp bằng 7.',
 'Nếu con chọn màu đầu khi dư 0, yêu cầu chỉ vị trí 3 và 6 trên dãy đã viết. Nếu con cộng 6 bước khi tìm số thứ 6, vẽ 6 điểm và đếm 5 khoảng.',
 'Con chỉ được một chu kì đầy đủ hoặc chứng minh hiệu không đổi trước khi áp dụng cách tính.', '10-10.html',None),
('dem','Đếm có thứ tự: tránh thiếu và trùng', 'Dùng 0, 1, 2 để viết số có hai chữ số khác nhau. Vì sao 01 không được tính?',
 'Lập bảng theo hàng chục: chục 1 → 10, 12; chục 2 → 20, 21. Hàng chục không được là 0; hàng đơn vị phải khác chữ số đã dùng.',
 'Có 4 số: 10, 12, 20, 21. Mỗi số thuộc đúng một dòng của bảng nên không trùng. Nếu được lặp chữ số, mỗi hàng chục có 3 cách chọn đơn vị, tổng 2 × 3 = 6 số. Trước khi nhân số cách chọn, phải đọc điều kiện có được lặp không. Với góc: cố định một đỉnh, chọn từng cặp tia tạo góc, dùng góc vuông làm mốc so sánh; quay hình không làm đổi loại góc.',
 'Dùng 0, 2, 5, viết các số có hai chữ số khác nhau. Có bao nhiêu số chẵn?',
 '20, 25, 50, 52: có 4 số, trong đó 3 số chẵn là 20, 50, 52.',
 'Nếu con sót số, không cho đáp số ngay: đưa hai dòng “chục 2” và “chục 5” để con tự điền. Nếu con đếm góc chỉ theo vùng nhỏ, nhắc xét cả góc tạo bởi hai tia ngoài.',
 'Con lập danh sách có thứ tự, giải thích điều kiện và kiểm tra không có trường hợp trùng.', '10-10.html',None),
]

intro='''<section class="card"><h2>Bắt đầu bằng một bài con làm được</h2><p>Mỗi lần chỉ chọn một bài học bên dưới. Con lấy giấy, bút và vài vật nhỏ để minh họa. Đọc câu hỏi mở đầu, tự nói cách nghĩ rồi mới xem ví dụ. Ví dụ nhỏ do người soạn viết để giúp hiểu; bài có mã TN/TL là bài trong đề cương đã cung cấp.</p><p><b>Nhịp học 60 phút:</b> 5 phút nhớ lại → 10 phút khám phá và xem mẫu → 10 phút làm cùng người lớn → nghỉ 5 phút → 20 phút tự làm bài nguồn → 10 phút chữa và giải thích lại. Thời gian là khung điều chỉnh; nếu con chưa hiểu, giảm số câu.</p><p><b>Khi con bí:</b> hỏi “Đề cho biết gì? Con đang tìm gì?” → gợi ý dùng hình/bảng → cùng làm bước đầu. Sau đó che mẫu, để con tự làm lại. Ghi “cần gợi ý” nếu đã được hỗ trợ.</p></section>'''
parts=[]
for id,title,start,model,worked,practice,answer,repair,goal,day,source in lessons:
    link=f'<a href="toan-bo-de-cuong.html#{source}">Mở bài nguồn {source}</a>' if source else '<a href="danh-muc-timo.html">Chọn một câu vòng loại cùng dạng trong kho</a>'
    parts.append(f'''<section class="teach-lesson" id="{id}"><p class="eyebrow">Mục tiêu: {goal}</p><h2>{title}</h2><div class="teach-question"><h3>1. Con nghĩ thử</h3><p>{start}</p><p>Con nói hoặc vẽ cách nghĩ trước khi đọc tiếp.</p></div><h3>2. Nhìn để hiểu</h3><p>{model}</p><details open class="teach-model"><summary>3. Cùng cô/thầy làm mẫu</summary><p>{worked}</p></details><h3>4. Đến lượt con</h3><p>{practice}</p><div class="writing-space">Con viết phép tính, hình vẽ hoặc lời giải vào vở.</div><details class="solution"><summary>Đối chiếu sau khi con đã thử</summary><p>{answer}</p><p><b>Người lớn chữa theo lỗi:</b> {repair}</p></details><h3>5. Dùng vào bài thi</h3><p>{link} · <a href="{day}">Bài tập của buổi học</a>. Chọn một bài vừa sức để tự làm, sau đó mới thử bài khó hơn. Với bài hình ghép, dùng hình gốc; không đo độ dài bằng mắt.</p><p><b>Vé ra khỏi bài học:</b> che ví dụ, con giải thích lại một bước quan trọng và làm lại một câu. Nếu vẫn cần nhắc, hôm sau ôn lại câu đó trước khi sang dạng mới.</p></section>''')
nav='<nav><a href="index.html">Buổi học</a><a href="bai-hoc-toan-4.html">Học cách làm</a><a href="toan-bo-de-cuong.html">Bài nguồn</a><a href="theo-doi.html">Theo dõi</a></nav>'
toc='<div class="lesson-links">'+''.join(f'<a href="#{x[0]}">{x[1]}</a>' for x in lessons)+'</div>'
page=f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Học Toán cùng con — lớp 4</title><link rel="stylesheet" href="style.css"></head><body><header>{nav}<h1>Hiểu cách làm, rồi tự giải được</h1><p>Bài học Toán lớp 4 · Ôn TIMO 11/10 và giữa kì 15/10/2026</p></header><main>{intro}{toc}{"".join(parts)}</main><script src="app.js"></script></body></html>'
(root/'bai-hoc-toan-4.html').write_text(page,encoding='utf-8')
mapping={'06':['tinh','x'],'07':['so','chu-so'],'08':['hinh','don-vi'],'09':['loi-van'],'10':['don-vi','dem','quy-luat'],'11':['quy-luat'],'12':['so','don-vi','dem'],'13':['x','loi-van','hinh'],'14':['so','x','hinh'],'15':['don-vi']}
for day,ids in mapping.items():
    file=root/f'{day}-10.html'; soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    links=' · '.join(f'<a href="bai-hoc-toan-4.html#{id}">{next(x[1] for x in lessons if x[0]==id)}</a>' for id in ids)
    msg='Ngày thi: chỉ xem một câu quen thuộc nếu con muốn; không học thêm bài mới.' if day in ('11','15') else 'Học một mục còn chưa chắc trước. Người lớn làm mẫu một câu, cùng con một câu, rồi để con tự làm. Danh sách bài phía dưới dùng để chọn và rà soát; hết giờ thì ghi phần còn lại.'
    block=BeautifulSoup(f'<section class="card teaching-start"><h2>Bắt đầu buổi học</h2><p>{links}</p><p>{msg}</p><p>Cuối buổi, hỏi: “Hôm nay con hiểu thêm điều gì? Con kiểm tra đáp án bằng cách nào?”</p></section>','html.parser')
    soup.main.insert(0,block)
    # Dense reference theory remains accessible, but does not precede guided instruction in full.
    for theory in list(soup.select('section.theory')):
        details=soup.new_tag('details',attrs={'class':'reference-theory'})
        summary=soup.new_tag('summary'); summary.string='Tra cứu thêm kiến thức của buổi này'
        theory.wrap(details);details.insert(0,summary)
    file.write_text(str(soup),encoding='utf-8')
soup=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
for note in list(soup.main.select('p.note')): note.decompose()
soup.header.h1.string='Học Toán cùng con — lớp 4'
soup.main.insert(0,BeautifulSoup('<section class="card"><h2>Con cần hiểu gì hôm nay?</h2><p><a href="bai-hoc-toan-4.html"><b>Mở bài học có hướng dẫn</b></a>: nghĩ thử → nhìn hình/bảng → xem mẫu → tự làm → giải thích lại.</p><p>TIMO: Chủ nhật 11/10/2026. Giữa kì: thứ Năm 15/10/2026. Mở buổi học theo ngày bên dưới; mỗi buổi chọn ít bài và chữa kỹ. Kho 350 câu và sổ tay là tài liệu tra cứu khi cần.</p></section>','html.parser'))
(root/'index.html').write_text(str(soup),encoding='utf-8')
with (root/'style.css').open('a',encoding='utf-8') as f:
    f.write('''\n/* Guided grade-four lessons */
.teach-lesson{background:white;padding:32px;border:1px solid #ccdce7;border-radius:16px;margin:28px 0;scroll-margin-top:20px;max-width:820px}.teach-lesson h2{margin-top:8px}.eyebrow{font-size:16px;color:#406554}.teach-question{background:#fff3d9;padding:20px;border-radius:12px}.teach-model{background:#edf6f2;padding:20px;margin:20px 0}.teach-model summary,.reference-theory>summary{font-weight:700;cursor:pointer}.writing-space{border:1px dashed #9daebb;padding:24px;color:#627482}.lesson-links{display:flex;flex-wrap:wrap;gap:12px}.lesson-links a{background:white;border:1px solid #ccdce7;border-radius:8px;padding:10px}.reference-theory{margin:20px 0;padding:14px;background:#f0f4f8}.teach-lesson p{max-width:68ch}@media(max-width:600px){.teach-lesson{padding:18px}.teach-question,.teach-model{padding:14px}}@media print{.teach-lesson{border-radius:0;padding:12px;break-inside:auto}.lesson-links,.writing-space{display:none}.teach-lesson h3{break-after:avoid}}
''')
plan=Path('output/Phan-tich-va-ke-hoach-on-TIMO.md')
old=plan.read_text(encoding='utf-8')
archive=Path('output/Phan-tich-va-ke-hoach-on-TIMO-ban-truoc.md')
if not archive.exists():archive.write_text(old,encoding='utf-8')
appendix=old[old.index('## 1. Dữ liệu'):old.index('## 6. Kế hoạch')]
new='''# Thiết kế lại bộ ôn Toán lớp 4: hiểu — làm — tự kiểm tra

Cập nhật 07/10/2026. TIMO 11/10; giữa kì Toán 15/10. Ngày thường khoảng 60 phút; thứ Bảy chia các phiên có nghỉ.

**Bắt đầu tại [Học Toán cùng con](html/index.html)** và [9 bài học có hướng dẫn](html/bai-hoc-toan-4.html). Các trang theo ngày đã đặt hướng dẫn học ở đầu; phần lý thuyết dài được thu gọn để tra cứu.

## 1. Đích đến của việc học

Con hiểu ý nghĩa phép tính, chọn được cách làm, trình bày được lý do và kiểm tra kết quả. Làm đúng nhờ nhìn đáp án chưa được tính là tự làm được. Chưa có bài làm cá nhân để kết luận con yếu ở dạng nào.

Mỗi bài học có ba mức: làm cùng người lớn; tự làm câu tương tự; vận dụng vào bài nguồn. Chỉ tăng độ khó khi con giải thích được cách làm ở mức trước. Bài hình ghép khó vẫn được giữ trong ngân hàng, nhưng cần đọc hình và hướng dẫn theo từng bước.

## 2. Một tiết ôn thực sự diễn ra thế nào?

| Thời gian | Hoạt động | Người lớn quan sát |
|---|---|---|
| 5 phút | Con nhớ lại một câu hôm trước, chưa xem mẫu | Con còn nhớ cách nghĩ hay chỉ đáp số? |
| 10 phút | Khám phá bằng đồ vật, hình hoặc bảng; xem một ví dụ | Con hiểu đại lượng và lý do của phép tính? |
| 10 phút | Cùng làm một câu; con tự thực hiện bước cuối | Cần hỗ trợ ở bước nào? |
| 5 phút | Nghỉ | Dừng đúng giờ |
| 20 phút | Tự làm 2–4 câu/ý nguồn tùy độ khó | Có đọc đúng điều kiện, đơn vị và hình? |
| 10 phút | Chữa một lỗi chính; che mẫu, làm lại | Đã tự sửa được chưa? |

Số câu là điểm bắt đầu để điều chỉnh, không là định mức bắt buộc. Nếu con còn vướng kiến thức nền, dùng phần vận dụng để củng cố nền. Cuối buổi hỏi con giải thích một bước; đầu buổi sau kiểm tra lại không nhìn mẫu.

## 3. Chín bài học được viết lại

| Bài học | Điều con cần hiểu | Minh họa trước công thức |
|---|---|---|
| Tính nhanh | Gộp các nhóm có cùng số lượng | Túi bi; số đứng riêng tương ứng một nhóm |
| Tìm x | Tháo thao tác theo thứ tự ngược | Đường đi của số; tìm phần bị bớt |
| Cấu tạo số, làm tròn | Chữ số có giá trị theo vị trí | Bảng hàng; hai mốc tròn và mốc giữa |
| Thêm chữ số | Thêm trái và thêm phải làm số đổi khác nhau | Thẻ số; kiểm tra số chữ số |
| Chu vi, diện tích | Đường bao khác phần mặt được phủ | Đi quanh hình; đếm ô vuông |
| Lời văn | Mỗi phép tính tìm một đại lượng | Bảng giá; đoạn thẳng; phần còn lại |
| Đơn vị | Quan hệ đơn vị quyết định phép đổi | Hình 10 × 10 ô; giờ/phút; kg/tạ |
| Quy luật, chu kì | Đếm bước hoặc nhóm lặp, hiểu số dư | Các nhóm màu; điểm và khoảng |
| Đếm | Liệt kê có thứ tự và tuân thủ điều kiện | Bảng theo hàng chục; xét cặp tia |

Ví dụ nhỏ và câu tự thử trong bài học do người soạn biên soạn, ghi rõ để phân biệt với bài nguồn. Các bài TN/TL dẫn về ngân hàng đề cương. Đáp án câu tự thử được đặt sau phần làm bài; có hướng dẫn chữa theo lỗi cụ thể.

## 4. Chữa bài để con học được

Không nói ngay đáp án. Hỏi con đọc lại yêu cầu, chỉ dữ kiện, vẽ hoặc lập bảng. Nếu vẫn bí, chỉ làm cùng bước đầu. Sau khi chữa, con che mẫu và tự giải lại. Phản hồi cụ thể: “Con đã tìm đúng chiều dài; cần ghi m² ở diện tích”, thay vì chỉ ghi “sai” hoặc “cẩn thận”.

Ghi bốn trạng thái: tự làm đúng và giải thích được; đúng nhưng chưa giải thích được; cần gợi ý; chưa làm. Với bài sai, ghi lỗi đọc đề, hiểu kiến thức, chọn cách làm, tính toán hoặc đơn vị; chọn một lỗi chính để sửa trước.

## 5. Lịch học và phạm vi

07/10: cấu tạo số, làm tròn, thêm chữ số. 08/10: chu vi, diện tích và đổi diện tích. 09/10: lời văn, tiền, tuổi. 10/10: đơn vị, góc, quy luật/đếm và thi thử; có nghỉ giữa các phiên. 11/10: thi TIMO, nghỉ sau thi. 12–13/10: hoàn tất các ý đề cương và làm lại lỗi. 14/10: kiểm tra bằng câu nguồn đã có, dùng để xem mức nhớ lại và khả năng tự trình bày. 15/10: thi giữa kì.

Nếu chưa học buổi 06/10, dùng một phần buổi hiện tại để học tính nhanh/tìm x; chuyển bài giữa kì còn lại sang 12–13/10. Không dồn thành hai giờ học trong một tối. Các bài quy luật và đếm có thể dùng một câu ngắn ở cuối buổi 07 hoặc 09 khi con đã xong bài chính; nếu chưa xong, học ở phiên thứ Bảy. Không đưa câu đề TIMO 2 vào luyện trước khi thi thử.

Giữ toàn bộ 38 câu/bài giữa kì và từng ý nhỏ trong ngân hàng. Danh sách nguồn bên dưới là bảng rà soát; số lượng câu liệt kê trong lịch cũ không phải khối lượng phải hoàn thành trong một tiết. Đến 13/10 rà lại từng ý. Nếu còn thiếu, 14/10 ưu tiên hoàn tất trước phiếu kiểm tra; ghi trung thực phần chưa hoàn thành.

## Phụ lục: căn cứ, bài nguồn và bảng rà soát

Phần dưới giữ thông tin đối chiếu từ bản trước. Lịch phân bổ nguồn là chỉ mục để chọn bài; khi dạy dùng nhịp tiết học và tiêu chí chuyển mức ở trên.

'''
plan.write_text(new+appendix,encoding='utf-8')
print('Redesigned: 9 guided lessons, 10 daily entry points, homepage and planning document.')
