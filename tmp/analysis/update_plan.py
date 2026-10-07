from pathlib import Path
p=Path('output/Phan-tich-va-ke-hoach-on-TIMO.md')
s=p.read_text(encoding='utf-8')
start=s.index('Ngày lập:'); end=s.index('## 1.')
s=s[:start]+'''Ngày lập: thứ Ba 06/10/2026. Cập nhật theo xác nhận mới nhất: **TIMO Chủ nhật 11/10; giữa kì Toán thứ Năm 15/10**. Ngày thường ôn khoảng 60 phút; thứ Bảy 10/10 có cả ngày để bố trí các phiên học.

Đây là bản phân tích và kế hoạch trước khi biên soạn bộ ôn chi tiết. Hai yêu cầu bắt buộc: luyện đủ năm nhóm TIMO và bao phủ toàn bộ đề cương giữa kì hiện có. Thứ Bảy dành khoảng 3 giờ học thực tế, chia thành bốn phiên và nghỉ dài giữa phiên; có cả ngày không có nghĩa học liên tục cả ngày. Sau TIMO tiếp tục ôn giữa kì đến 14/10, tạm giữ mức một giờ/ngày như ngày thường. Chưa có kết quả làm bài cá nhân để kết luận con mạnh/yếu ở đâu.

“Bao phủ đầy đủ” nghĩa là mọi câu và mọi ý của đề cương đều có lý thuyết, bài nguồn, đáp án/lời giải và buổi ôn cụ thể; không đồng nghĩa cam kết con đã thành thạo. Bài đã làm đúng có thể kiểm tra nhanh bằng cách giải thích; bài sai phải tự làm lại.

'''+s[end:]
start=s.index('## 4.'); end=s.index('## 6.')
s=s[:start]+'''## 4. Lịch ôn hai kỳ thi đã chốt

Ngày thường: 55 phút học + 5 phút nghỉ trong tổng một giờ, trừ thi thử 60 phút liên tục theo tài liệu. Hết giờ thì đánh dấu phần chưa xong vào buổi củng cố 12–14/10; không tự phát sinh bài bắt buộc ngoài lịch.

TN = trắc nghiệm giữa kì; TL = tự luận giữa kì; TT = thử thách giữa kì. Các mã này đều trỏ đến file [26 -27] ĐỀ CƯƠNG GIỮA KÌ 1 TOÁN 4.pdf. Trang cụ thể nằm trong bảng bao phủ bên dưới.

| Ngày | Phân bổ | Bài bắt buộc và liên hệ TIMO |
|---|---|---|
| T3 06/10 — 60 phút | 10 phút lý thuyết; 20 phút bài lớp; nghỉ 5 phút; 15 phút TIMO; 10 phút chữa | TN12,15,20; TL6a–d,7a–b. Dùng CĐ1 bài 6a,8a làm ví dụ đã chữa, không giao thêm. TIMO đề 1 câu 7,8,9,13 (PDF 7): tổng dãy, thừa số chung, ghép cặp, phép toán mới |
| T4 07/10 — 60 phút | 10 phút lý thuyết; 25 phút bài lớp; nghỉ 5 phút; 10 phút TIMO; 10 phút chữa | TN1–6,13,19; TL1a–b,2a–b,3a–b,8. TIMO đề 7 câu 15 (PDF 35) và đề 1 câu 11,14 (PDF 7): thêm chữ số và chia hết. Nhóm TL2–3 có nhiều số: ưu tiên làm đủ ý; nếu đã đúng, con nêu hàng/lớp và cách làm tròn |
| T5 08/10 — 60 phút | 10 phút lý thuyết; 25 phút bài lớp; nghỉ 5 phút; 10 phút TIMO; 10 phút chữa | TN14,17; TL5 chỉ hai ý diện tích; TT16,17,18. TIMO đề 1 câu 17,18 (PDF 8); đề 7 câu 20 (PDF 36) dùng đối chiếu TT18, giải một lần. Câu chưa tự giải được giữ để chữa thứ Bảy |
| T6 09/10 — 60 phút | 10 phút lý thuyết; 25 phút bài lớp; nghỉ 5 phút; 10 phút TIMO; 10 phút chữa | TN16,18; TL9,11,13,15a–b. TIMO đề 6 câu 2,3 (PDF 29) hoặc đề 1 câu 15 (PDF 8): sơ đồ tổng–hiệu, làm ngược, phần bằng nhau. Chọn hai câu phù hợp, không bắt làm cả ba |
| T7 10/10 — phiên sáng 1, 45 phút | 10 phút lý thuyết; 25 phút bài lớp; 10 phút chữa | TN7,8,9,10,11; TL4 đủ sáu phép đổi; TL5 bốn ý thời gian/thế kỉ; TL14. Ôn góc, thời gian, thế kỉ, khối lượng — các phần cần cho giữa kì dù liên hệ TIMO ít |
| T7 — phiên sáng 2, 40 phút | Sau nghỉ tối thiểu 30 phút: 10 phút lý thuyết; 20 phút bài lớp; 10 phút chữa | TL10,12: diện tích → sản lượng/khối lượng → đổi đơn vị/số chuyến. Hoàn thành phần tồn đọng trong đề cương, ưu tiên bài nền tảng trước |
| T7 — phiên chiều, 60 phút | Sau ăn trưa và nghỉ: thi thử liên tục | **TIMO vòng loại đề 2, PDF 11–15**, giữ chưa dùng trước buổi này. Bao gồm đủ logic, số học, lý thuyết số, hình học, tổ hợp. Không chữa trong thời gian làm đề |
| T7 — phiên cuối, 35 phút | Sau nghỉ tối thiểu 30 phút: 20 phút chữa; 10 phút giải lại; 5 phút nhắc chiến thuật | Lời giải đề 2: PDF 66–70. Chọn tối đa ba lỗi đáng sửa; nhắc chu kì, chữ số tận cùng, đếm số/đếm hình, trường hợp xấu nhất hoặc đường đi theo lỗi thực tế. Dừng học vào cuối chiều, tối nghỉ |
| CN 11/10 — thi TIMO | Khởi động 10 phút nếu thuận tiện | Xem công thức và 1–2 câu đã làm đúng. Sau thi nghỉ; không bố trí ôn giữa kì bắt buộc |
| T2 12/10 — 60 phút | 10 phút lý thuyết; 30 phút giải lại; nghỉ 5 phút; 15 phút chữa | Củng cố toàn bộ TN1–13,19; TL1–5,8,14. Kiểm tra nhanh câu đúng, tự làm lại câu sai và mọi ý chưa hoàn thành; chú trọng góc, làm tròn, thời gian, đổi diện tích/khối lượng |
| T3 13/10 — 60 phút | 10 phút lý thuyết; 30 phút giải lại; nghỉ 5 phút; 15 phút chữa | Củng cố TN14–18,20; TL6–7,9–13,15; TT16–18. Ôn trình bày bài lời văn, tìm x, đơn vị đáp số. Ưu tiên phần chưa xong/sai; mỗi dạng đã đúng chỉ kiểm tra nhanh |
| T4 14/10 — 60 phút | 35 phút kiểm tra tổng hợp giữa kì; nghỉ 5 phút; 15 phút chữa; 5 phút xem phiếu lỗi | Phiếu tổng hợp mới có ít nhất một câu mỗi nhóm trong bảng bao phủ, không tự nhận là đề thi chính thức. Chữa lỗi cuối, xem lại câu nguồn chưa chắc. Không mở chuyên đề mới |
| T5 15/10 — thi giữa kì | Khởi động nhẹ 5–10 phút nếu thuận tiện | Xem bảng đơn vị, quy tắc làm tròn, công thức hình học và phiếu lỗi |

Thứ Bảy có tổng **180 phút học thực tế**, chia 45 + 40 + 60 + 35 phút. Khung giờ cụ thể phụ thuộc sinh hoạt gia đình; không cần học hết ngày. Nếu con mệt, cắt câu TIMO bổ sung và phần chữa dài trước, chuyển phần giữa kì chưa xong sang 12–13/10.

Thời lượng thi thử 60 phút theo TIMOK4.pdf, PDF 3. Dùng thời lượng/cách ghi đáp án theo thông báo BTC nếu khác. Không dùng kết quả đề đã luyện làm thước đo của một đề mới.

## 5. Bảng bao phủ đầy đủ đề cương giữa kì

Trang đều là trang PDF, tính từ 1. Bảng này bao phủ **20 câu trắc nghiệm + 15 bài tự luận + 3 bài thử thách**, gồm tất cả ý nhỏ. Lịch phân buổi không chứng minh con đã hoàn thành; khi triển khai phải ghi trạng thái từng câu/ý.

| Nhóm kiến thức và lý thuyết phải có | Câu/bài nguồn và trang | Ôn lần đầu | Kiểm tra lại |
|---|---|---|---|
| Đọc/viết số, hàng/lớp, giá trị chữ số; so sánh, sắp xếp; số liền sau | TN1,2,3,6 PDF1; TL1a,b và TL2a PDF2; TL3a PDF3 | 07/10 | 12/10 |
| Làm tròn đến chục nghìn/trăm nghìn | TN5 PDF1; TL2b PDF2; TL3b PDF3 | 07/10 | 12/10 |
| Chẵn/lẻ, dãy tự nhiên, số tròn chục và bất đẳng thức | TN4 PDF1; TN13,19 PDF2 | 07/10 | 12/10 |
| Nhận biết và đếm góc nhọn, vuông, tù, bẹt theo hình | TN7 PDF1; TN9 PDF2 | 10/10 | 12/10 |
| Thế kỉ, đổi giờ–phút–giây, đơn vị hỗn hợp | TN8,10,11 PDF2; bốn ý đầu TL5 PDF3 | 10/10 | 12/10 |
| Yến–tạ–tấn–kg; đổi khối lượng, đơn vị hỗn hợp | TL4 đủ sáu ý PDF3; TL14 PDF4 | 10/10 | 12/10 |
| Đổi đơn vị diện tích: hai đơn vị kề nhau gấp/kém 100 lần | Hai ý cuối TL5 PDF3 | 08/10 | 12/10 |
| Biểu thức chứa chữ; thứ tự phép tính; đặt thừa số chung, tính thuận tiện | TN12,15,20 PDF2; TL7a,b PDF3 | 06/10 | 13/10 |
| Tìm x, phép toán ngược và kiểm tra bằng thay lại | TL6a,b,c,d PDF3 | 06/10 | 13/10 |
| Cấu tạo số kết hợp tổng–hiệu: thêm chữ số bên trái | TL8 PDF3 | 07/10 | 12/10 |
| Tiền, đơn giá, nhiều bước, giảm một phần hóa đơn | TN16 PDF2; TL9 PDF3; TL15a,b PDF4 | 09/10 | 13/10 |
| Tuổi, quan hệ hơn/kém, suy ngược, tổng–hiệu ẩn | TN18 PDF2; TL11 PDF3; TL13 PDF4 | 09/10 | 13/10 |
| Chu vi/diện tích hình vuông, hình chữ nhật; chiều dài gấp chiều rộng | TN14,17 PDF2 | 08/10 | 13/10 |
| Diện tích kết hợp năng suất/khối lượng/số chuyến | TL10,12 PDF3 | 10/10 | 13/10 |
| Hình ghép, chia hình; diện tích phần còn lại; suy cạnh từ chu vi; đọc thuật ngữ Anh–Việt | TT16,17,18 PDF4 | 08/10 | 13/10 |

### Theo dõi từng câu/ý khi thực hiện

Mỗi câu/ý có các cột: mã nguồn — ngày ôn — tự làm đúng/cần gợi ý/sai/chưa làm — loại lỗi — ngày giải lại — kết quả lần hai. Không bỏ TT16–18 vì phụ huynh yêu cầu toàn bộ đề cương. Bài khó có thể được hướng dẫn trước, nhưng trạng thái “cần gợi ý” giữ nguyên cho đến khi con tự làm lại.

Đến cuối 13/10 phải kiểm tra không còn câu/ý nguồn nào “chưa làm”. Nếu vẫn còn, ngày 14/10 ưu tiên hoàn tất phần đó trước phiếu kiểm tra mới. Nếu thời gian không đủ, ghi rõ phần chưa hoàn thành; không báo đạt bao phủ chỉ vì có trong tài liệu.

Phần “Nội dung ôn tập” đầu trang 1 và các hình không trích xuất đầy đủ thành chữ: khi soạn bộ chi tiết cần nhìn trang gốc, đọc khung nội dung và đối chiếu với bảng này. “Bao phủ toàn bộ” hiện giới hạn ở đề cương được cung cấp, chưa khẳng định bao phủ một phạm vi thi mới do giáo viên bổ sung sau 06/10.

'''+s[end:]
s=s.replace('Chọn khoảng 10–15 câu TIMO để kiểm tra ngắn, luyện và chữa ngoài đề thi thử; trong đó một số là câu làm lại. Số cuối cùng phụ thuộc kết quả kiểm tra và tốc độ làm thực tế.','Chọn khoảng 15–20 câu TIMO luyện/chữa ngoài một đề thi thử đầy đủ, phù hợp lỗi thực tế. Đồng thời soạn đủ 20 câu TN, 15 bài TL và 3 bài TT của giữa kì, không cắt các phần ít liên quan TIMO.')
s=s.replace('Xuất bộ dễ đọc/in gồm lịch từng ngày, phiếu lý thuyết–bài tập, lời giải cho phụ huynh và bảng theo dõi lỗi.','Xuất bộ dễ đọc/in gồm lịch đến 15/10, phiếu lý thuyết–bài tập, lời giải cho phụ huynh, bảng theo dõi từng câu/ý giữa kì và phiếu kiểm tra tổng hợp ngày 14/10.')
start=s.index('## 8.')
s=s[:start]+'''## 8. Thông tin đã chốt và giới hạn còn lại

Đã xác nhận TIMO Chủ nhật 11/10, giữa kì 15/10, ngày thường khoảng một giờ, thứ Bảy có cả ngày. Lịch 12–14/10 tạm giữ một giờ/ngày. Giờ thi, ngôn ngữ thi và lỗi cá nhân chưa có; có thể thực hiện bằng tài liệu song ngữ hiện có và ghi lỗi trong các buổi luyện.

Phiếu Topic 3/4/5, VBT và PCT được nhắc trong Excel chưa có đủ đầu vào. Bộ ôn sẽ bao phủ toàn bộ đề cương giữa kì hiện có và các cụm kiến thức được xác nhận trong nhật kí; không tự dựng bài rồi ghi là bài lớp. Nếu giáo viên bổ sung phạm vi thi, cập nhật bảng bao phủ và thay bài trong khung thời gian đã chốt.
'''
p.write_text(s,encoding='utf-8')
print('Updated Sunday TIMO / 15 October midterm plan; complete source coverage table added.')
