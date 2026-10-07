"""Augment existing output without rerunning generators that replace precise MathML."""
from pathlib import Path
from bs4 import BeautifulSoup,Doctype
from html import escape as h
import ast,json,re
from collections import Counter

ROOT=Path('output/html')
records=json.loads((ROOT/'danh-muc-timo.json').read_text(encoding='utf-8'))
# Load only the pure MathML helpers; importing the original module rebuilds HTML.
tree=ast.parse(Path('tmp/analysis/math_layout.py').read_text(encoding='utf-8'))
pure=ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['row','math']],type_ignores=[])
ns={'re':re,'escape':h};exec(compile(pure,'math_helpers','exec'),ns);math=ns['math']

# Each entry: recognition, ordered method, formula(s), warning.
T={
'seq':('Dãy số có các số sau tăng hoặc giảm theo một quy luật, nhưng chưa chắc cách đều.',[
'Ghi từng hiệu: số sau trừ số trước. Nếu các hiệu bằng nhau, đây là dãy cách đều; nếu không, kiểm tra chính dãy hiệu.',
'Với dãy hiệu tăng đều, viết tiếp hiệu trước rồi mới cộng vào số cuối của dãy ban đầu. Viết từng số trung gian đến đúng vị trí đề hỏi.',
'Nếu phép cộng không phù hợp, kiểm tra nhân, chia hoặc hai dãy đan xen ở vị trí chẵn và lẻ. Thử lại quy luật trên mọi số đã cho.'],['Số số hạng = (số cuối − số đầu) : khoảng cách + 1'],'Không dùng công thức dãy cách đều khi khoảng cách đang thay đổi; không nhầm số tiếp theo với số ở vị trí thứ n.'),
'calendar':('Đề hỏi ngày trước/sau hôm nay, thứ trong tuần, tháng hoặc số ngày của một năm.',[
'Xác định mốc thực sự: nếu đề nói ngày mai là Chủ nhật thì hôm nay là thứ Bảy. Đánh dấu hướng tiến hoặc lùi.',
'Đổi chênh lệch về ngày rồi chia cho 7; bỏ tuần đủ và dịch theo số dư. Với tháng lặp lại hằng năm, dùng chu kì 12 tháng.',
'Nếu đi qua tháng/năm, dùng số ngày thực của từng tháng: 4, 6, 9, 11 có 30 ngày; tháng 2 có 28 hoặc 29; các tháng còn lại có 31. Năm chia hết cho 4 là nhuận, riêng năm tròn thế kỉ còn phải chia hết cho 400.'],['44 = 6 × 7 + 2'],'Số ngày đã trôi qua không tự động cộng thêm 1. Chỉ cộng 1 khi đếm cả hai ngày đầu và cuối; phân biệt trước và sau mốc.'),
'reverse':('Biết kết quả cuối sau một chuỗi thao tác; cần tìm số ban đầu.',[
'Viết các thao tác theo đúng thứ tự đề: cộng, trừ, nhân, chia hoặc lấy một phần.',
'Bắt đầu từ kết quả cuối. Đảo thứ tự thao tác, đồng thời đảo từng phép: cộng thành trừ, trừ thành cộng, nhân thành chia, chia thành nhân.',
'Thay số vừa tìm vào chuỗi thao tác xuôi. Mọi bước phải dẫn về kết quả cuối đã cho.'],['60 × 10 = 600','600 + 79 = 679','679 : 7 = 97','97 − 4 = 93'],'Phải đảo cả phép toán lẫn thứ tự. Ví dụ này lấy từ VL-6-3, không phải thao tác ngẫu nhiên.'),
'cycle':('Một nhóm hình, màu, chữ hoặc vị trí được lặp lại giống hệt nhau.',[
'Khoanh nhóm ngắn nhất lặp hoàn chỉnh và đánh số các vị trí trong nhóm từ 1 đến độ dài nhóm.',
'Chia vị trí cần tìm cho độ dài nhóm. Dư khác 0 thì lấy đúng vị trí đó; dư 0 thì lấy vị trí cuối nhóm.',
'Nếu hỏi số lần xuất hiện trong đoạn đầu của dãy, đếm trong các nhóm đủ rồi đếm thêm ở phần dư.'],['Vị trí = số nhóm đủ × độ dài nhóm + số dư'],'Dư 0 không phải vị trí 0. Dãy tăng dần không phải chu kì chỉ vì vài hình đầu giống nhau.'),
'assume':('Có hai loại vật/người với tổng số lượng và tổng chân, tiền hoặc điểm; mỗi loại đóng góp khác nhau.',[
'Giả sử tất cả đều thuộc loại có đóng góp nhỏ hơn. Tính tổng trong giả sử đó bằng số lượng nhân mức của loại nhỏ.',
'Lấy tổng thực trừ tổng giả sử. Mỗi lần đổi một vật từ loại nhỏ sang loại lớn, tổng tăng bằng chênh lệch hai mức.',
'Chia phần chênh tổng cho chênh mỗi vật để tìm số loại lớn. Lấy tổng số vật trừ kết quả để tìm loại nhỏ; kiểm tra cả hai tổng.'],['Số loại lớn = (tổng thực − tổng giả sử) : chênh lệch mỗi vật'],'Không chia cho mức của loại lớn; phải chia cho phần tăng khi thay một vật. Chỉ áp dụng trực tiếp khi có hai loại và đóng góp mỗi loại cố định.'),
'basic':('Một biểu thức có nhiều phép tính, ngoặc hoặc giá trị chữ được cho trước.',[
'Nếu có chữ, thay đúng giá trị vào toàn bộ biểu thức. Tính từ ngoặc trong ra ngoặc ngoài.',
'Thực hiện nhân và chia trước cộng và trừ. Các phép cùng mức tính từ trái sang phải; phép chia không có tính kết hợp tùy ý.',
'Ước lượng kết quả và tính lại bước dễ sai. Khi đặt tính, ghi các chữ số thẳng hàng; với chia, thử bằng thương nhân số chia rồi cộng số dư.'],['Số bị chia = số chia × thương + số dư'],'Số chia phải khác 0; số dư không âm và nhỏ hơn số chia. Không đổi thứ tự hai số trong phép trừ hoặc chia.'),
'sum':('Tính tổng một dãy cách đều có dấu ba chấm.',[
'Xác định số đầu, số cuối và khoảng cách. Kiểm tra số cuối thực sự thuộc dãy.',
'Đếm số số hạng, bao gồm cả hai đầu. Ghép số đầu với số cuối để thấy các cặp có cùng tổng.',
'Lấy tổng hai đầu nhân số số hạng rồi chia 2. Nếu số số hạng lẻ, vẫn dùng công thức; có thể tách số ở giữa để kiểm tra.'],['Số số hạng = (số cuối − số đầu) : khoảng cách + 1','Tổng = (số đầu + số cuối) × số số hạng : 2'],'Không áp dụng cho tổng có dấu trừ xen kẽ hay dãy nhân.'),
'factor':('Nhiều tích có một thừa số chung, hoặc các số có thể ghép thành số tròn.',[
'Tìm thừa số xuất hiện ở mọi số hạng. Số đứng riêng chính là số đó nhân 1.',
'Đưa thừa số chung ra ngoài ngoặc; giữ nguyên dấu cộng/trừ của các thừa số còn lại. Hoặc đổi thứ tự các số hạng cộng để ghép cặp thuận tiện.',
'Tính phần trong ngoặc, sau đó nhân. Kiểm tra không bỏ sót số hạng và không đổi dấu.'],['a × b + a × c = a × (b + c)','a × b − a × c = a × (b − c)'],'Chỉ đặt ra ngoài phần thực sự chung. Không ghép tùy ý qua một dấu chia hoặc ngoặc đang chứa phép trừ.'),
'pair':('Tổng dài có dấu cộng và trừ xen kẽ; các cặp hiệu giống nhau.',[
'Viết vài số đầu và cuối, xác định khoảng cách và đếm số hạng.',
'Ghép từng cặp theo dấu của đề. Tính giá trị một cặp, đếm số cặp; nếu thừa một số, giữ số ấy riêng.',
'Nhân giá trị cặp với số cặp, cộng phần dư. Thử trên đoạn ngắn để chắc việc ghép giữ nguyên biểu thức.'],['40 − 37 + 34 − 31 + … + 4 − 1 = 7 × 3 = 21'],'Dấu trừ phải đi với số bị trừ. Không biến tổng xen kẽ thành tổng tất cả số dương.'),
'crypt':('Một phép đặt tính thay chữ số bằng chữ; có điều kiện chữ khác nhau hoặc chữ đầu khác 0.',[
'Đặt phép tính thẳng hàng và bắt đầu ở hàng đơn vị. Xét chữ số kết quả cùng số nhớ hoặc số mượn.',
'Chuyển sang hàng chục, trăm; mỗi chữ đã xác định phải giữ nguyên giá trị tại tất cả vị trí. Dùng điều kiện khác nhau để loại khả năng.',
'Viết lại đầy đủ các số và tính phép toán gốc. Kiểm tra chữ số đầu không bằng 0 và không có hai chữ nhận cùng giá trị khi đề cấm.'],['a + b + số nhớ = chữ số kết quả + 10 × số nhớ mới'],'Chữ số chỉ từ 0 đến 9. Số nhớ là một phần của phép tính, không được bỏ qua hoặc tự mặc định có nhớ.'),
'div':('Tìm chữ số còn thiếu hoặc số lớn/nhỏ thỏa chia hết và điều kiện chữ số.',[
'Lọc theo chữ số tận cùng: chia hết cho 2 phải chẵn, cho 5 tận cùng 0 hoặc 5, cho 10 tận cùng 0.',
'Dùng tổng chữ số cho 3 và 9; hai chữ số cuối cho 4, ba chữ số cuối cho 8. Chia hết cho 6 cần cả 2 và 3; cho 12 cần cả 3 và 4; cho 45 cần cả 5 và 9.',
'Kết hợp mọi điều kiện rồi chọn lớn nhất/nhỏ nhất. Nếu cấm lặp chữ số, kiểm tra điều kiện đó trước khi chọn đáp án.'],[],'Một điều kiện đúng chưa đủ. Không dùng tổng chữ số để kiểm tra chia hết cho 4 hoặc 8.'),
'last':('Tích gồm rất nhiều thừa số giống nhau hoặc chỉ hỏi chữ số hàng đơn vị.',[
'Bỏ các hàng phía trước; nhân các chữ số hàng đơn vị và chỉ giữ hàng đơn vị sau mỗi bước.',
'Với thừa số lặp lại, lập chu kì: 9 cho 9, 1; 4 cho 4, 6; 3 cho 3, 9, 7, 1. Chia số thừa số cho độ dài chu kì.',
'Chọn vị trí theo số dư, dư 0 lấy cuối nhóm. Với nhiều nhóm tích, tìm tận cùng mỗi nhóm trước rồi kết hợp bằng phép toán của đề.'],[],'Đếm số thừa số, không đếm số dấu nhân. Không lấy số dư làm đáp án; số dư chỉ chỉ vị trí trong chu kì.'),
'op':('Đề tự định nghĩa một kí hiệu phép toán mới.',[
'Chép định nghĩa và đánh dấu số nào thay chữ thứ nhất, số nào thay chữ thứ hai.',
'Thay toàn bộ các vị trí theo định nghĩa; giữ ngoặc. Nếu phép toán lồng nhau, tìm kết quả bên trong trước rồi dùng nó như một số mới.',
'Thực hiện phép tính thông thường theo thứ tự. Nếu đổi chỗ hai đầu vào, phải tính lại vì phép toán mới chưa chắc giao hoán.'],['a ⊗ b = a × b + b × (a − 3) + 2','9 ⊗ 5 = 9 × 5 + 5 × (9 − 3) + 2 = 77'],'Kí hiệu mới không tự mang ý nghĩa cộng, nhân hoặc phép XOR. Ví dụ định nghĩa trên là của VL-1-13.'),
'ratio':('Đề cho tổng hoặc hiệu và quan hệ gấp một số lần; cần tìm mỗi lượng.',[
'Biểu diễn lượng bé bằng một số phần, lượng lớn bằng số phần tương ứng. Các phần phải có cùng giá trị.',
'Cho tổng thì cộng số phần; cho hiệu thì trừ số phần. Chia tổng/hiệu thực cho số phần tương ứng để tìm giá trị một phần.',
'Nhân một phần với số phần của từng lượng. Kiểm tra lại cả tổng/hiệu và quan hệ gấp.'],['Một phần = tổng : tổng số phần','Một phần = hiệu : hiệu số phần'],'Phải phân biệt tổng số phần với hiệu số phần. Không dùng công thức tổng–hiệu khi đề chỉ cho tỉ số.'),
'age':('Các tuổi ở hiện tại hoặc các năm khác nhau; đề cho tổng, hiệu hay quan hệ gấp.',[
'Vẽ mốc năm và đưa các tuổi cần so sánh về cùng thời điểm. Hai người cùng tăng một tuổi mỗi năm nên hiệu tuổi không đổi.',
'Nếu tổng tuổi được cho ở tương lai, trừ số năm tăng của từng người để đưa tổng về hiện tại. Tỉ số tuổi thường thay đổi theo thời gian.',
'Dùng tổng–hiệu hoặc tổng–tỉ tại đúng mốc. Thử bằng cách cộng/trừ số năm theo từng câu của đề.'],['Tuổi lớn = (tổng tuổi + hiệu tuổi) : 2','Tuổi bé = (tổng tuổi − hiệu tuổi) : 2'],'Không so trực tiếp tuổi hiện tại của người này với tuổi tương lai của người kia mà bỏ qua chênh lệch năm.'),
'grid':('Đếm hình chữ nhật trong một lưới; có thể phải chứa một ô/vùng được đánh dấu.',[
'Nếu đếm tất cả: mỗi hình chữ nhật được quyết định bởi hai đường ngang và hai đường dọc. Đếm số cặp đường ở mỗi chiều rồi nhân.',
'Nếu phải chứa ô/vùng: đếm riêng số lựa chọn biên trên, dưới, trái, phải bao quanh vùng. Nhân bốn số lựa chọn, kể cả biên sát vùng.',
'Nếu lưới thiếu đoạn hoặc đề loại hình vuông, kiểm tra hình tạo ra có đủ bốn cạnh và tách các trường hợp bị loại.'],['Số cặp trong n đường = n × (n − 1) : 2','Số hình chứa vùng = số biên trên × số biên dưới × số biên trái × số biên phải'],'Công thức chọn đường chỉ đúng với lưới có cạnh liên tục. Đếm đường kẻ, không nhầm với số ô.'),
'area':('Hình tô màu, hình gồm nhiều ô vuông hoặc lấy một hình lớn trừ hình nhỏ.',[
'Đưa kích thước về cùng đơn vị. Nếu có chu vi hình vuông, chia 4 để tìm cạnh rồi bình phương để tìm diện tích.',
'Tách phần cần tìm thành các phần không chồng nhau; hoặc lấy diện tích hình bao trừ những phần bị bỏ.',
'Nếu gồm ô vuông bằng nhau, tìm diện tích một ô rồi nhân số ô. Hai nửa ô chỉ ghép thành một ô khi chúng cùng diện tích.'],['Diện tích hình vuông = cạnh × cạnh','Diện tích hình chữ nhật = chiều dài × chiều rộng'],'Không cộng hai diện tích đang chồng nhau; không lấy chênh lệch chu vi làm chênh lệch diện tích.'),
'opt':('Tìm chu vi/diện tích lớn nhất hoặc nhỏ nhất với cạnh là số tự nhiên.',[
'Nếu biết diện tích, liệt kê các cặp số nguyên dương có tích bằng diện tích. Chỉ lấy mỗi cặp một lần, không cần đổi chỗ lặp lại.',
'Tính chu vi của từng cặp rồi so sánh. Nếu biết chu vi, tìm nửa chu vi và liệt kê các cặp cạnh có tổng bằng nửa chu vi; tính diện tích từng cặp.',
'Kiểm tra điều kiện cạnh nguyên và phân biệt đại lượng đề yêu cầu tối ưu. Với diện tích cố định, các cạnh càng gần nhau thường cho chu vi càng nhỏ.'],['Chu vi = 2 × (chiều dài + chiều rộng)','Nửa chu vi = chiều dài + chiều rộng'],'Phải liệt kê đủ các cặp hợp lệ; cạnh không được bằng 0. Kết luận gần nhau cần được kiểm tra bằng các cặp của bài.'),
'view':('Nhìn một khối ghép từ trước, trái, phải hoặc trên; hỏi số mặt nhìn thấy.',[
'Xác định hướng nhìn bằng mũi tên hoặc câu chữ. Mặt phía sau không được tính chỉ vì nhìn thấy trong hình phối cảnh.',
'Theo từng hàng/cột từ phía nhìn, đánh dấu mặt ngoài gần nhất. Mặt bị khối khác che hoàn toàn không nhìn thấy.',
'Đếm các mặt đánh dấu đúng một lần và đối chiếu sơ đồ nhìn thẳng. Nếu đề hỏi số ô hiện ra trong hình chiếu, các khối chồng lên nhau có thể cùng tạo một ô.'],[],'Không đếm mọi mặt của mọi khối. Phân biệt số khối, số mặt lộ ra và số ô trong hình chiếu.'),
'geo':('Biết chu vi hoặc cạnh của một phần và cần suy kích thước của hình ghép.',[
'Đánh dấu các cạnh bằng nhau theo kí hiệu hoặc vì cùng là cạnh một hình vuông. Không suy bằng nhau chỉ vì trông giống.',
'Viết chu vi bằng tổng các cạnh ngoài. Cạnh chung nằm bên trong không thuộc chu vi hình ghép.',
'Tìm cạnh còn thiếu bằng tổng hoặc hiệu các đoạn thẳng cùng đường. Sau đó tính đại lượng cần tìm và ghi đơn vị.'],['Cạnh hình vuông = chu vi : 4'],'Chu vi đi theo đường biên ngoài, không đi qua đường chia bên trong. Không đo kích thước bằng mắt trên ảnh.'),
'worst':('Có các từ chắc chắn, ít nhất phải lấy, đảm bảo có đủ một màu/loại.',[
'Xác định đúng yêu cầu: lấy được một màu cụ thể, đủ một số vật màu đó, hay có cùng màu bất kì.',
'Xây tình huống lấy nhiều nhất mà vẫn chưa đạt. Với một màu cụ thể, lấy hết các màu khác trước; với cùng màu bất kì, mỗi màu lấy tối đa ít hơn mức cần.',
'Thêm một vật để vượt ngưỡng chưa đạt, hoặc thêm đủ số vật của màu cụ thể. Kiểm tra ngưỡng trước vẫn có thể thất bại.'],['Mức chắc chắn = số lấy tối đa chưa đạt + 1'],'Không dùng xác suất trung bình. Phân biệt đủ 4 lá đỏ với 4 lá cùng màu bất kì; hai yêu cầu cho cách tính khác nhau.'),
'form':('Đếm số lập từ các chữ số với điều kiện chẵn/lẻ, tổng chữ số hoặc không lặp.',[
'Xác định số chữ số và điều kiện cho từng hàng. Chữ số đầu của số nhiều chữ số không bằng 0.',
'Nếu các hàng được chọn độc lập, nhân số lựa chọn. Nếu không được lặp, mỗi chữ số đã dùng phải loại khỏi các hàng sau.',
'Nếu điều kiện liên kết các hàng, chia trường hợp theo hàng bị ràng buộc hoặc liệt kê có thứ tự rồi cộng các nhóm không trùng.'],['Số cách = số lựa chọn hàng đầu × số lựa chọn hàng sau'],'Không nhân số lựa chọn như độc lập khi tổng chữ số hoặc điều kiện không lặp làm lựa chọn sau thay đổi.'),
'multiples':('Đếm các số trong một khoảng chia hết cho một số đã cho.',[
'Tìm bội đầu tiên không nhỏ hơn cận dưới và bội cuối cùng không lớn hơn cận trên. Kiểm tra đề có lấy hai cận hay không.',
'Các bội liên tiếp cách nhau đúng số chia. Dùng công thức đếm dãy cách đều với hai bội đã tìm.',
'Nếu đề có điều kiện thêm như hai chữ số, chẵn hoặc chữ số khác nhau, phải lọc tiếp; khi hai bội đầu/cuối không tồn tại thì có 0 số.'],['Số bội = (bội cuối − bội đầu) : số chia + 1'],'Không lấy trực tiếp cận dưới/cận trên nếu chúng không chia hết. Khoảng mở phải bỏ những cận bị loại.'),
'stairs':('Đi lên cầu thang bằng bước 1 hoặc 2 bậc, có thể có bậc hỏng.',[
'Ghi 1 cách tại bậc 0: chưa bước là một cách bắt đầu. Tại bậc 1 có 1 cách nếu không hỏng.',
'Với bậc không hỏng, cộng số cách ở hai bậc trước, vì bước cuối có thể dài 1 hoặc 2. Bậc hỏng phải ghi 0 ngay.',
'Tính lần lượt đến bậc cần hỏi. Nếu được bước dài khác, chỉ cộng từ những bậc thực sự có thể bước tới.'],['Cách đến bậc n = cách đến bậc trước + cách đến bậc cách hai'],'Một bậc hỏng không có nghĩa mọi bậc sau đều có 0 cách; có thể nhảy qua nó bằng bước 2.'),
'path':('Đếm đường đi trên sơ đồ hoặc lưới với các hướng được phép.',[
'Đọc hướng được phép và xác định các đoạn có thật. Ghi 1 ở điểm xuất phát.',
'Theo thứ tự từ xuất phát đến đích, tại mỗi nút cộng số cách ở tất cả nút có một bước hợp lệ đi tới nó.',
'Tại nút bị chặn ghi 0; không cộng từ đoạn bị xóa. Nếu đề cho phép quay lại hoặc cấm thăm lại, phải xét điều kiện riêng; không dùng phép cộng một lượt cho sơ đồ có vòng tùy ý.'],['Cách đến một nút = tổng cách từ các nút đi tới hợp lệ'],'Đường không được vẽ không tồn tại. Hai đường chỉ giao nhau chưa chắc là nút chuyển hướng nếu hình không cho phép.'),
'color':('Tô các ô hoặc vùng bằng một số màu; vùng kề nhau có thể phải khác màu.',[
'Đánh dấu những vùng thực sự kề nhau theo đề. Thường kề nhau là chung một cạnh, không chỉ chạm ở một điểm.',
'Tô theo một thứ tự thuận tiện; tại mỗi vùng loại các màu của những vùng kề đã tô. Nhân số lựa chọn nếu số lượng đó cố định cho từng bước.',
'Nếu vùng cuối kề cả vùng đầu hoặc nhiều vùng đã tô, chia trường hợp theo màu trước đó; không mặc định mỗi bước đều còn cùng số màu.'],[],'Đếm các cách tô khác nhau theo vị trí; chỉ coi cách xoay là một nếu đề nói rõ. Với hình khép kín, phải kiểm tra điều kiện ở đầu và cuối.'),
'solid':('Hỏi số đỉnh, cạnh hoặc mặt của lập phương, hình hộp, hình chóp.',[
'Phân biệt đỉnh là điểm, cạnh là đoạn nối hai đỉnh, mặt là vùng phẳng. Cạnh nét đứt vẫn là cạnh của khối.',
'Lập phương và hình hộp chữ nhật đều có 8 đỉnh, 12 cạnh, 6 mặt. Hình chóp có đáy n cạnh thì có n đỉnh ở đáy và 1 đỉnh chóp.',
'Với chóp: n cạnh đáy, n cạnh bên, n mặt bên và 1 mặt đáy. Nếu khối ghép, xem đề đếm khối riêng hay biên ngoài của cả hình.'],['Số đỉnh hình chóp = n + 1','Số cạnh hình chóp = 2 × n','Số mặt hình chóp = n + 1'],'Không nhầm cạnh của hình vẽ 2 chiều với toàn bộ cạnh khối; những cạnh bị khuất vẫn được tính khi hỏi khối có bao nhiêu cạnh.'),
'regions':('Hỏi số phần lớn nhất do một số đường thẳng cắt một vùng phẳng.',[
'Trước khi cắt, vùng có 1 phần. Đường đầu tiên có thể thêm 1 phần.',
'Để đường mới thêm nhiều phần nhất, nó phải cắt mọi đường trước ở các điểm khác nhau nằm trong vùng; các đường không song song và không có ba đường đồng quy.',
'Đường thứ n có tối đa n đoạn trong vùng nên thêm n phần. Cộng lần lượt số phần mới; nếu hình cho sẵn các đường không tối ưu, đếm đúng hình thay vì dùng mức lớn nhất.'],['Số phần lớn nhất = 1 + 1 + 2 + … + n'],'Công thức chỉ cho đường thẳng trong một vùng thích hợp và cấu hình cắt đạt tối đa; không áp dụng tự động cho đường gấp khúc hoặc đường trùng nhau.'),
'surface':('Khối ghép có các mặt cần sơn hoặc hỏi diện tích bề mặt.',[
'Đếm mặt của các khối nhỏ. Mỗi cặp khối ghép kín mất hai mặt ngoài, một mặt của mỗi khối.',
'Nếu chỉ sơn phần nhìn thấy hoặc không sơn đáy, trừ tiếp những mặt đề loại. Có thể đếm mặt lộ ra theo từng hướng để kiểm tra.',
'Nhân số mặt cần sơn với diện tích một mặt nếu các mặt đó bằng nhau. Nếu khác kích thước, cộng diện tích từng nhóm.'],['Số mặt ngoài = 6 × số khối lập phương − 2 × số cặp mặt ghép'],'Số cặp mặt ghép khác số khối. Công thức trên cho các khối lập phương nhỏ đồng kích thước ghép nguyên mặt; cần xét riêng các trường hợp khác.'),
'place':('Hàng/lớp, đọc số, giá trị chữ số hoặc thêm một chữ số bên trái/phải.',[
'Tách số từ phải sang trái thành lớp đơn vị, nghìn, triệu; mỗi lớp gồm hàng trăm, chục, đơn vị. Giá trị chữ số bằng chữ số nhân giá trị hàng.',
'Thêm d bên phải số N làm số mới bằng 10 lần N cộng d. Thêm bên trái thì xác định số chữ số của N rồi cộng d lần đơn vị hàng mới.',
'Viết quan hệ tăng thêm hoặc tổng hai số theo đề. Giải và viết lại thao tác thêm chữ số để kiểm tra số chữ số ban đầu.'],['Số mới bên phải = 10 × N + d','Số tăng bên phải = 9 × N + d'],'Không dùng công thức thêm bên phải cho thêm bên trái. Khi xác định số chữ số, phải thử lại miền giá trị của N.'),
'geosum':('Tổng của dãy nhân cùng một số, thay vì cộng cùng khoảng cách.',[
'Gọi toàn bộ tổng là S. Xác định công bội bằng cách chia hai số hạng liên tiếp.',
'Nhân S với công bội và viết thẳng hàng với tổng cũ. Lấy tổng mới trừ tổng cũ để các số hạng giữa triệt tiêu.',
'Từ phần còn lại suy S bằng một phép chia. Nếu chưa học lũy thừa, giữ các tích lặp đúng như đề; không ép con dùng kí hiệu mới.'],['3 × S − S = số hạng mới cuối − số hạng đầu'],'Đây là dãy nhân, không dùng tổng dãy cách đều. Công thức minh họa trên dành cho công bội 3; thay đúng công bội của bài.'),
'union':('Đếm số chia hết cho A hoặc B; một số có thể thuộc cả hai nhóm.',[
'Đếm nhóm chia hết cho A, rồi nhóm chia hết cho B trong đúng khoảng của đề.',
'Tìm nhóm chia hết đồng thời cho cả A và B; đó là các bội của bội chung nhỏ nhất. Đếm nhóm này bằng dãy cách đều.',
'Cộng hai nhóm rồi trừ nhóm bị đếm hai lần. Nếu đề yêu cầu chỉ một trong hai, phải trừ nhóm chung hai lần.'],['Số thuộc A hoặc B = số thuộc A + số thuộc B − số thuộc cả hai'],'Từ hoặc thông thường cho phép thuộc cả hai, trừ khi đề nói chỉ một. Với A và B có ước chung, không tự dùng tích A × B làm bội chung nhỏ nhất.'),
'divisors':('Hỏi có bao nhiêu số chia một số cho trước không dư, khác với đếm bội.',[
'Cách nền tảng: thử các ước nhỏ và ghi cặp thương tương ứng. Khi hai số trong cặp đã đổi thứ tự thì dừng.',
'Mỗi cặp gồm hai ước khác nhau đóng góp 2; nếu hai số bằng nhau thì chỉ đếm 1. Các ước bao gồm 1 và chính số đó, trừ khi đề loại.',
'Cách mở rộng: phân tích thành thừa số nguyên tố. Một thừa số xuất hiện a lần cho a + 1 lựa chọn số lần dùng; nhân các số lựa chọn của các nguyên tố.'],['Số ước = (a + 1) × (b + 1)'],'Công thức cuối dành cho một số có đúng hai thừa số nguyên tố với số lần xuất hiện a và b; với nhiều nguyên tố thêm thừa số tương ứng. Không tính đôi ước giữa của số chính phương.'),
'optimize':('Lập các số bằng chữ số cho trước để tổng hoặc hiệu đạt lớn/nhỏ nhất.',[
'Đánh dấu các vị trí hàng lớn: chữ số ở hàng nghìn ảnh hưởng hơn chữ số ở hàng trăm, chục, đơn vị.',
'Muốn tổng lớn, ưu tiên chữ số lớn vào vị trí có giá trị hàng lớn. Muốn hiệu lớn, ưu tiên làm số bị trừ lớn và số trừ nhỏ trong điều kiện dùng chữ số.',
'Nếu đề dùng chung một bộ chữ số cho hai số, không tối ưu hai số độc lập. Liệt kê các khả năng ở hàng đầu rồi so sánh các trường hợp còn tranh chấp.'],[],'Chữ số đầu không bằng 0. Khi tìm hiệu nhỏ nhất, thường cần hai số gần nhau; không chỉ chọn một số nhỏ nhất và một số lớn nhất.'),
'concat':('Viết liền các số tự nhiên rồi hỏi chữ số ở vị trí rất xa.',[
'Tách thành nhóm số có cùng số chữ số. Nhóm một chữ số từ 1 đến 9 có 9 chữ số; nhóm hai chữ số từ 10 đến 99 có 90 × 2 chữ số.',
'Trừ số chữ số của từng nhóm đủ để tìm nhóm chứa vị trí cần hỏi. Trong nhóm có k chữ số mỗi số, chia vị trí còn lại trừ 1 cho k.',
'Thương chỉ số lượng số đã đi qua; số đầu nhóm cộng thương là số chứa chữ số cần tìm. Số dư cộng 1 là vị trí chữ số trong số đó, tính từ trái.'],['180 = 90 × 2','Vị trí trong số = số dư + 1'],'Phải đọc dãy bắt đầu từ 0, 1 hay một số khác. Trừ 1 trước chia giúp xử lý đúng vị trí ở cuối một số.'),
'table':('Bảng ô có các tổng hàng/cột hoặc tổng của các ô liên tiếp bằng nhau.',[
'Chép dữ kiện lên sơ đồ; gọi ô chưa biết bằng chữ. Với hai tổng bằng nhau có phần chung, trừ phần chung để suy phần còn lại bằng nhau.',
'Ví dụ tổng ba ô liên tiếp luôn bằng nhau: so hai nhóm kế tiếp, hai ô ở giữa triệt tiêu nên ô thứ nhất bằng ô thứ tư; dãy lặp theo chu kì 3.',
'Điền các ô suy ra chắc chắn, rồi dùng một tổng có đủ dữ kiện để tìm ô cuối. Kiểm tra mọi tổng đề cho, không chỉ một hàng.'],['a + b + c = b + c + d','a = d'],'Không tự đoán mọi hàng/cột có cùng quy luật nếu đề chưa cho. Cần đủ dữ kiện để xác định duy nhất ô cần hỏi.'),
'average':('Biết trung bình cộng và cần tổng, số thiếu hoặc trung bình sau khi thêm/bớt.',[
'Đếm chính xác số lượng các số. Tổng bằng trung bình nhân số lượng.',
'Muốn tìm số thiếu, lấy tổng cần có trừ tổng các số đã biết. Muốn thêm/bớt, cập nhật cả tổng và số lượng.',
'Kiểm tra bằng cách cộng tất cả số rồi chia lại. Với hai nhóm có số lượng khác nhau, không lấy trung bình của hai trung bình một cách trực tiếp.'],['Trung bình cộng = tổng : số lượng','Tổng = trung bình cộng × số lượng'],'Mục này dùng cho vòng quốc gia và phiếu trung bình cộng có trong dữ liệu; chưa coi là nội dung giữa kì đã học.'),
'cuts':('Cắt một đoạn gỗ/dây thành các phần; hỏi số nhát cắt hoặc thời gian cắt.',[
'Xác định số đoạn cần tạo từ độ dài và điều kiện các phần bằng nhau.',
'Một vật ban đầu đã có một đoạn; mỗi nhát cắt riêng làm tăng số đoạn thêm 1. Vì vậy n đoạn cần n − 1 nhát.',
'Nhân số nhát với thời gian mỗi nhát nếu thời gian cố định. Nếu cắt nhiều vật hoặc được chồng/gấp, đọc và giải theo điều kiện riêng.'],['Số nhát cắt = số đoạn − 1'],'Không nhân thời gian với số đoạn. Công thức này không tự áp dụng khi được cắt chồng nhiều đoạn một lúc.'),
'consecutive':('Tổng của một số số chẵn/lẻ liên tiếp, mỗi số cách nhau 2.',[
'Đếm số lượng số cần tìm. Trung bình của dãy bằng tổng chia số lượng và cũng bằng trung bình hai đầu.',
'Nếu số lượng lẻ, trung bình là số chính giữa; đi về hai phía với khoảng cách 2. Nếu số lượng chẵn, trung bình nằm giữa hai số giữa.',
'Viết đủ dãy và kiểm tra tổng, tính chẵn/lẻ, khoảng cách và số lượng.'],['Trung bình hai đầu = tổng : số số hạng'],'Số trung bình không nhất thiết là một số hạng khi có số lượng chẵn. Phải giữ đúng dãy chẵn hoặc dãy lẻ đề yêu cầu.'),
'pyth':('Tam giác vuông trong bài quốc gia; biết hai cạnh để suy cạnh còn lại hoặc diện tích ghép.',[
'Xác định góc vuông bằng kí hiệu; cạnh đối diện góc vuông là cạnh huyền, luôn dài nhất.',
'Nếu đã học hệ thức tam giác vuông, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông. Suy bình phương cạnh thiếu bằng cộng hoặc trừ thích hợp.',
'Nếu con chưa học căn bậc hai, giữ bài này để sau hai kì thi. Có thể dùng cách cắt ghép khi lời giải nguồn cung cấp; không lấy hệ thức mới làm yêu cầu ôn giữa kì.'],['c × c = a × a + b × b'],'Chỉ đúng khi góc giữa a và b là góc vuông. Đây là phần mở rộng quốc gia, không thuộc nền tảng giữa kì hiện có.'),
'segments':('Có các điểm và hỏi số đoạn thẳng tạo được khi nối từng cặp.',[
'Mỗi đoạn được xác định bởi hai điểm phân biệt; chọn cặp điểm, không xét thứ tự đầu cuối.',
'Từ n điểm, cộng số đoạn mới khi thêm từng điểm: 1, 2, …, n − 1. Nếu chỉ nối một số điểm theo điều kiện, lọc cặp hợp lệ.',
'Nếu đề hỏi đường thẳng thay vì đoạn, các cặp trên cùng một đường có thể tạo đường trùng nhau; khi đó không dùng trực tiếp công thức đoạn.'],['Số đoạn nối n điểm = n × (n − 1) : 2'],'AB và BA là cùng một đoạn. Không nhầm số đoạn thẳng với số đường thẳng khi có nhiều điểm thẳng hàng.'),
'digitprod':('Tích các chữ số được cho; cần đếm các số có một số chữ số cố định.',[
'Phân tích tích thành các chữ số từ 1 đến 9. Nếu tích khác 0, không được có chữ số 0; chữ số 1 có thể xuất hiện mà không đổi tích.',
'Liệt kê các bộ chữ số không xét thứ tự, đủ số lượng chữ số của số cần lập. Không liệt kê lại cùng một bộ ở thứ tự khác.',
'Với từng bộ, đếm các cách sắp xếp khác nhau rồi lọc chẵn/lẻ hoặc điều kiện khác. Các chữ số trùng phải được coi như nhau.'],[],'Phân tích tích thành nguyên tố chưa phải là bộ chữ số hoàn chỉnh: 2 × 3 có thể gộp thành chữ số 6. Không bỏ qua chữ số 1.'),
'eliminate':('Hai tổ hợp vật có tổng khối lượng/giá tiền; có thể loại một loại bằng phép trừ.',[
'Viết mỗi tổ hợp bằng số lượng từng loại nhân khối lượng/giá một vật.',
'Nếu một loại có cùng số lượng ở hai tổ hợp, trừ trực tiếp. Nếu chưa bằng, nhân toàn bộ một hoặc cả hai tổ hợp để số lượng loại ấy bằng nhau.',
'Từ phần còn lại tìm loại thứ nhất; thay vào một tổ hợp để tìm loại thứ hai. Kiểm tra cả hai tổng gốc.'],[],'Khi nhân một tổ hợp, phải nhân mọi số lượng và cả tổng. Không chỉ nhân loại muốn khử.'),
'permutation':('Sắp xếp chữ/vật theo thứ tự; có thể yêu cầu một nhóm đứng cạnh nhau.',[
'Với các vật khác nhau, chọn vị trí thứ nhất rồi thứ hai; số lựa chọn giảm dần sau mỗi lần chọn.',
'Nếu một nhóm phải đứng cạnh nhau, gộp nhóm thành một khối để sắp với phần còn lại; sau đó xét các thứ tự bên trong nhóm.',
'Nếu có chữ giống nhau, nhiều thứ tự nhìn hoàn toàn giống nhau chỉ tính một. Liệt kê theo vị trí hoặc chia số hoán vị cho số cách đổi chỗ các chữ giống nhau khi đã hiểu quy tắc.'],['Số cách sắp n vật khác nhau = n × (n − 1) × … × 1'],'Mục mở rộng quốc gia. Không dùng công thức các vật khác nhau cho từ có chữ lặp; phải đọc đề có coi chiều ngược là khác hay không.'),
'productratio':('Biết tích hai số và quan hệ số lớn gấp k lần số bé.',[
'Gọi số bé là một phần; số lớn là k phần. Tích bằng k nhân bình phương giá trị một phần.',
'Chia tích cho k để tìm bình phương số bé. Tìm số dương có bình phương ấy bằng cách thử số phù hợp hoặc dùng kiến thức đã học.',
'Nhân số bé với k để tìm số lớn. Kiểm tra lại tích và tỉ số.'],['Số bé × số bé = tích : k'],'Không lấy tích chia tổng số phần; đó là cách của tổng–tỉ. Chỉ xét số dương khi đề nói độ dài hoặc số tự nhiên dương.'),
'remainder':('Cùng một số vật chia theo hai mức mỗi người, có dư hoặc thiếu.',[
'Ghi mức mỗi người ở từng cách chia và lượng dư/thiếu. Dư nghĩa tổng vật bằng lượng phát cộng dư; thiếu nghĩa tổng vật bằng lượng cần trừ thiếu.',
'So sánh hai cách: chênh mức mỗi người nhân số người bằng chênh lượng phát. Nếu một cách dư và một cách thiếu, chênh lượng phát là tổng dư và thiếu.',
'Chia chênh lượng phát cho chênh mức để tìm số người; thay lại để tìm tổng vật và kiểm tra cả hai cách.'],['Tổng vật = mức mỗi người × số người + số dư'],'Không luôn lấy hiệu hai số dư; khi một cách thiếu phải đổi đúng dấu. Đề chia có dư còn yêu cầu số dư nhỏ hơn số chia.'),
'pattern':('Dãy hình ngày càng thêm que, ô hoặc khối; hỏi hình thứ xa.',[
'Lập bảng: số thứ tự hình và số que/ô/khối. Đếm ít nhất các hình được cho thay vì đoán từ một hình.',
'So sánh lượng thêm mỗi bước. Tách phần cố định với phần lặp lại theo số thứ tự; nếu lượng thêm thay đổi, xem dãy hiệu.',
'Thử quy tắc trên toàn bộ hình đã có, sau đó tính hình cần tìm. Nếu ghép các ô chung cạnh, không tính lại cạnh chung.'],[],'Một mẫu phát triển không nhất thiết tăng đều. Công thức phải đúng cho mọi hình được vẽ trong đề.'),
'triangles':('Đếm tam giác vuông tạo bởi các đoạn đã vẽ.',[
'Chọn đỉnh góc vuông trước, xác định các cặp hướng vuông góc thực sự có trong hình.',
'Chọn một điểm trên mỗi hướng để tạo hai cạnh góc vuông. Chỉ giữ trường hợp cạnh nối hai điểm còn lại tồn tại hoặc được đề cho phép nối.',
'Đếm riêng theo đỉnh và kích thước; mỗi tam giác vuông chỉ có một góc vuông nên cách chia này tránh đếm trùng.'],[],'Không coi mọi cặp điểm là có cạnh nối. Không suy góc vuông chỉ vì hình nhìn gần vuông; dùng đường ngang/dọc hoặc kí hiệu.'),
'pigeon':('Chia vật vào các nhóm và cần bảo đảm một nhóm có ít nhất m vật.',[
'Giả sử chưa có nhóm nào đạt m; khi đó mỗi nhóm có tối đa m − 1 vật.',
'Nhân số nhóm với m − 1 để tìm tổng lớn nhất vẫn chưa đạt. Nếu tổng thực lớn hơn mức này, chắc chắn có ít nhất một nhóm đạt m.',
'Kiểm tra có đúng số nhóm và các vật đều được phân vào những nhóm đó. Ngưỡng đảm bảo là mức chưa đạt cộng 1.'],['Ngưỡng đảm bảo = số nhóm × (m − 1) + 1'],'Kết luận là tồn tại một nhóm, chưa chỉ ra nhóm cụ thể. Nếu nhóm có sức chứa hoặc điều kiện khác nhau, phải điều chỉnh mức chưa đạt.'),
'work':('Cùng công việc, số người hoặc máy thay đổi nên số ngày thay đổi.',[
'Xác nhận công việc giống nhau và năng suất mỗi người/máy không đổi. Tính tổng người-ngày hoặc máy-giờ cần cho công việc.',
'Chia tổng ấy cho số người/máy mới để tìm thời gian. Nếu đã làm một phần, trừ phần công đã hoàn thành trước.',
'Kiểm tra tăng số người thì thời gian giảm trong điều kiện lý tưởng của đề. Ghi rõ thời gian mỗi ngày nếu không làm số giờ như nhau.'],['Số người × số ngày = tổng lượng công'],'Chỉ dùng tỉ lệ nghịch khi năng suất như nhau và công việc có thể phân chia theo giả thiết. Đây là mở rộng quốc gia.')
}
assert set(T)=={r['category'] for r in records}

def clean_text(value):
 # Unicode letters only: × and ÷ must never count as letters.
 value=re.sub(r'([^\W\d_])(?=\d)',r'\1 ',value)
 value=re.sub(r'(\d)(?=[^\W\d_])',r'\1 ',value)
 value=re.sub(r'([:,;])(?=\S)',r'\1 ',value)
 value=re.sub(r'([²³])(?=\d)',r'\1 ',value)
 return value

def shell(title,body):
 return '<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><link rel="stylesheet" href="style.css"></head><body><header><nav><a href="index.html">Mục lục</a><a href="lo-trinh.html">Lộ trình</a><a href="ly-thuyet-day-du.html">Sổ tay lý thuyết</a><a href="danh-muc-timo.html">Kho TIMO</a><a href="theo-doi.html">Theo dõi giữa kì</a></nav><h1>'+title+'</h1></header><main>'+body+'</main></body></html>'

body='<p class="note"><b>Cách dùng:</b> mở đúng dạng của bài đang chọn, đọc phần nhận biết và cách làm, rồi thử bài nguồn trước khi mở lời giải. Sổ tay bổ sung lý thuyết cho toàn bộ 36 dạng vòng loại và 14 dạng chỉ xuất hiện ở quốc gia trong cách phân loại hiện tại. Không yêu cầu học tất cả trong một buổi. Phần nền tảng giữa kì ở đầu trang; phần quốc gia được tách để học sau hai kì thi.</p>'
body+='<nav class="theory-toc"><a href="#nen-tang">Nền tảng giữa kì</a><a href="#vong-loai">36 dạng vòng loại</a><a href="#quoc-gia">14 dạng riêng quốc gia</a><a href="bao-phu-ly-thuyet.html">Bảng đối chiếu bao phủ</a></nav>'
body+='<h2 id="nen-tang">A. Nền tảng và các điểm dễ thiếu khi ôn giữa kì</h2>'
# Keep carefully written existing theory, with source/example calculations intact.
existing={}
for file in sorted(ROOT.glob('*.html')):
 for section in BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser').select('section.theory'):
  title=section.h3.get_text(' ',strip=True)
  if title not in existing:existing[title]=str(section)
for i,(title,section) in enumerate(existing.items(),1):
 sp=BeautifulSoup(section,'html.parser');sp.section['id']='nen-'+str(i);body+=str(sp)

extras=[
('unknown','Tìm thành phần chưa biết — đủ các phép toán',
'Trước hết gọi cả cụm chứa x là một thành phần. Tìm giá trị cụm đó bằng phép toán ngoài cùng, rồi mới tìm x ở phép toán bên trong. Với mỗi phép toán phải phân biệt vị trí của x; không chỉ học một quy tắc “chuyển vế”.',[
'Số hạng chưa biết = tổng − số hạng đã biết','Số bị trừ = hiệu + số trừ','Số trừ = số bị trừ − hiệu','Thừa số chưa biết = tích : thừa số đã biết','Số bị chia = thương × số chia','Số chia = số bị chia : thương'],
'Bước cuối luôn thay x vào biểu thức ban đầu. Trong phép chia này xét chia hết và số chia khác 0; khi tìm số chia từ thương, thương phải khác 0.', 'toan-bo-de-cuong.html#TL6','Đề cương giữa kì TL6, bốn ý a–d; Chuyên đề 1, bài tìm x ở trang PDF 3.'),
('column','Đặt tính: cộng, trừ, nhân và chia',
'Cộng/trừ phải đặt hàng đơn vị thẳng hàng đơn vị, rồi làm từ phải sang trái. Ghi số nhớ khi tổng một hàng từ 10 trở lên; ghi việc mượn ở phép trừ, đặc biệt khi mượn qua nhiều chữ số 0. Nhân với số có nhiều chữ số phải đặt tích riêng theo đúng hàng trước khi cộng.',[
'Số bị chia = số chia × thương + số dư'],
'Với chia, thực hiện chia–nhân–trừ–hạ lần lượt từ trái sang phải. Khi một lượt chia cho thương 0 mà vẫn còn chữ số hạ xuống, phải viết 0 ở thương. Số dư cuối phải nhỏ hơn số chia. Ước lượng để phát hiện thương hoặc tích sai một hàng.', 'toan-bo-de-cuong.html#TN15','Đề cương giữa kì TN15, TL7; Chuyên đề 1 trang PDF 1–2. Dữ liệu không có một bài đặt tính độc lập cho mọi trường hợp nên không ghi nhầm thành bài lớp đã làm.'),
('read','Đọc, viết số; số liền trước; chẵn/lẻ và số tròn chục',
'Tách số thành các lớp ba chữ số từ phải sang trái. Đọc từng lớp từ trái sang phải, kèm tên lớp triệu/nghìn; lớp bằng 000 có thể bỏ khi đọc nhưng phải giữ vị trí khi viết. Viết số theo giá trị từng hàng, thêm 0 ở hàng không có.',[
'Số liền sau = số đã cho + 1','Số liền trước = số đã cho − 1'],
'Chẵn: tận cùng 0, 2, 4, 6, 8; lẻ: 1, 3, 5, 7, 9. Số tròn chục tận cùng 0. Với điều kiện 47 < x < 92, liệt kê 50, 60, 70, 80, 90; không lấy hai cận. Số tự nhiên 0 không có số liền trước trong tập số tự nhiên.', 'toan-bo-de-cuong.html#TN19','Đề cương giữa kì TN1, TN4, TN6, TN13, TN19; Cấu tạo số trang PDF 1–2.'),
('units','Đổi đơn vị: chọn đúng hệ số và kiểm tra đơn vị kết quả',
'Đổi tất cả về cùng đơn vị trước khi cộng, trừ hoặc so sánh. Đơn vị hỗn hợp đổi từng phần rồi cộng; đổi ngược lấy thương làm phần đơn vị lớn, dư làm phần đơn vị nhỏ. Chú ý ba hệ số khác nhau: độ dài theo 10, diện tích theo 100 và giờ/phút/giây theo 60.',[
'1 m = 10 dm = 100 cm = 1 000 mm','1 tấn = 10 tạ = 100 yến = 1 000 kg','1 m² = 100 dm² = 10 000 cm²'],
'Tiền dùng cùng đơn vị đồng trước khi tính; 1 nghìn đồng bằng 1 000 đồng. Không đổi 1 m² thành 100 cm². Với sản lượng theo diện tích, phải tính lượng trên một đơn vị diện tích rồi nhân diện tích thật.', 'toan-bo-de-cuong.html#TL5','Đề cương giữa kì TL4–5, TL9–10, TL14–15.'),
('angles','Đếm góc trên hình có nhiều tia — quy trình đầy đủ',
'Khoanh từng đỉnh. Liệt kê các tia khác nhau xuất phát từ đỉnh đó; hai điểm trên cùng một hướng xác định cùng một tia. Mỗi cặp tia khác nhau cho một góc nhỏ hoặc góc bẹt trong cách đếm của đề. Đếm theo từng cặp rồi phân loại, tránh đảo tên để đếm hai lần.',[],
'Góc nhọn nhỏ hơn góc vuông; góc tù lớn hơn góc vuông và nhỏ hơn góc bẹt. Hai tia đối nhau tạo góc bẹt. Trên hình không ghi số đo, dùng kí hiệu vuông và quan hệ ngang/dọc; ảnh phải xem đủ các đoạn. Sau cùng cộng số lượng từng loại từ các đỉnh.', 'toan-bo-de-cuong.html#TN7','Đề cương giữa kì TN7 và TN9, trang PDF 1; có ảnh đề gốc và lời giải phân loại theo đỉnh.')]
for key,title,words,formulas,warning,link,source in extras:
 body+=f'<section class="theory" id="school-{key}"><h3>{title}</h3><div class="rule"><p>{words}</p>'+''.join(math(x) for x in formulas)+f'<p class="theory-warning"><b>Kiểm tra và tránh sai:</b> {warning}</p><p class="source">Nguồn đối chiếu: {source}</p><p><a href="{link}">Mở bài nguồn và lời giải từng bước</a></p></div></section>'

groups={cat:[r for r in records if r['category']==cat] for cat in T}
prelim=[cat for cat in T if any(r['round']=='VL' for r in groups[cat])]
national=[cat for cat in T if cat not in prelim]
for heading,anchor,cats in [('B. Lý thuyết cho 36 dạng vòng loại','vong-loai',prelim),('C. 14 dạng chỉ có ở vòng quốc gia — học sau hai kì thi','quoc-gia',national)]:
 body+=f'<h2 id="{anchor}">{heading}</h2><div class="theory-toc">'+''.join(f'<a href="#type-{cat}">{h(groups[cat][0]["category_name"])}</a>' for cat in cats)+'</div>'
 for cat in cats:
  recognition,steps,formulas,warning=T[cat]
  candidates=groups[cat]
  r=next((r for r in candidates if r['selection']=='Bài đại diện'),next((r for r in candidates if r['round']=='VL' and r['exam']!=2),candidates[0]))
  if cat=='reverse':r=next(r for r in records if r['id']=='VL-6-3')
  title=r['category_name'];role='Vòng loại' if cat in prelim else 'Mở rộng quốc gia'
  body+=f'<section class="theory" id="type-{cat}" data-category="{cat}"><h3>{h(title)}</h3><p class="tag">{role}</p><div class="rule"><h4>Nhận biết</h4><p>{recognition}</p><h4>Cách làm từng bước</h4><ol>'+''.join(f'<li>{step}</li>' for step in steps)+'</ol>'
  if formulas:body+='<h4>Công thức / phép tính cần nhớ</h4>'+''.join(math(e) for e in formulas)
  body+=f'<p class="theory-warning"><b>Dễ sai:</b> {warning}</p><p><b>Liên hệ tài liệu lớp:</b> {h(clean_text(r["connection"]))}</p><div class="worked-example"><h4>Ví dụ có trong tài liệu: {r["id"]}</h4><p class="source">{r["label"]} · TIMOK4.pdf · đề trang PDF {r["page"]} (trang in {r["printed_page"]}); lời giải trang PDF {r["solution_page"]} (trang in {r["solution_page"]-1}).</p><p>Đọc đề bên dưới. Tự xác định dữ kiện và áp dụng các bước trên; sau đó đối chiếu lời giải gốc. Ảnh giữ nguyên biểu thức và hình vẽ.</p>'
  body+=''.join(f'<img loading="lazy" class="source-crop" src="{x}" alt="Đề gốc {r["id"]}">' for x in r['question_images'])
  body+='<details class="solution"><summary>Mở lời giải ví dụ từ tài liệu</summary>'+''.join(f'<img loading="lazy" class="source-crop" src="{x}" alt="Lời giải gốc {r["id"]}">' for x in r['solution_images'])+'</details>'
  body+=f'<p><a href="danh-muc-timo.html#{r["id"]}">Chọn bài khác cùng dạng và đối chiếu PDF</a></p></div></div></section>'
(ROOT/'ly-thuyet-day-du.html').write_text(shell('Sổ tay lý thuyết — giữa kì và toàn bộ dạng TIMO',body),encoding='utf-8')

# Coverage refers to conceptual categories, never claims every question has been independently solved.
body='<p class="note"><b>Kết quả rà:</b> bản cũ có 7 nhóm lý thuyết nền tảng, nhưng nhiều dạng mới chỉ có gợi ý một câu. Bản bổ sung giữ các nhóm nền tảng, thêm 5 mục kĩ năng giữa kì và viết riêng 50 mục TIMO, gồm 36 dạng vòng loại và 14 dạng riêng quốc gia. Bao phủ ở đây là bao phủ cách làm theo phân loại; không có nghĩa đã giải lại độc lập cả 350 câu hoặc con phải học cả 50 mục trước Chủ nhật.</p><h2>1. Đối chiếu đề cương giữa kì</h2><div class="coverage-table"><table><thead><tr><th>Bài nguồn</th><th>Lý thuyết dùng để làm</th><th>Đối chiếu</th></tr></thead><tbody>'
midrows=[('TN1–6; TL1–3, TL8','Giá trị hàng/lớp, so sánh, làm tròn, thêm chữ số','place'),('TN7, TN9','Nhận biết và đếm góc theo đỉnh','school-angles'),('TN8; TN10–11; TL4–5','Thế kỉ, thời gian, khối lượng, diện tích và đổi đơn vị','school-units'),('TN12, TN15, TN20; TL6–7','Thứ tự phép tính, tìm x, tính nhanh','school-unknown'),('TN13, TN19','Chẵn/lẻ, tròn chục, cận của khoảng','school-read'),('TN14, TN17; TL10, TL12; TT16–18','Chu vi, diện tích, suy cạnh và hình ghép','geo'),('TN16; TL9, TL14–15','Đơn giá, tiền, nhiều bước và giảm một phần tư','school-units'),('TN18; TL11, TL13','Tuổi, hơn/kém và tổng–hiệu','age')]
for source,topic,anchor in midrows:
 anchor=anchor if anchor.startswith('school-') else 'type-'+anchor
 body+=f'<tr><td>{source}</td><td>{topic}</td><td><a href="ly-thuyet-day-du.html#{anchor}">Mở lý thuyết</a></td></tr>'
body+='</tbody></table></div><p>Toàn bộ 20 câu trắc nghiệm, 15 bài tự luận và 3 bài thử thách được đối chiếu trong bảng trên. Các ý nhỏ tiếp tục theo dõi ở <a href="theo-doi.html">bảng từng ý của đề cương</a>. Mục giảm tiền một phần tư và tổng–hiệu nằm trong nhóm “Bài nhiều bước, tiền và sơ đồ đoạn thẳng” ở phần nền tảng của sổ tay.</p><h2>2. Đối chiếu tất cả dạng TIMO</h2><div class="coverage-table"><table><thead><tr><th>Dạng</th><th>Vòng loại</th><th>Quốc gia</th><th>Lý thuyết</th></tr></thead><tbody>'
for cat in prelim+national:
 counts=Counter(r['round'] for r in groups[cat])
 body+=f'<tr><td>{h(groups[cat][0]["category_name"])}</td><td>{counts["VL"]}</td><td>{counts["QG"]}</td><td><a href="ly-thuyet-day-du.html#type-{cat}">Nhận biết · cách làm · ví dụ nguồn</a></td></tr>'
body+='</tbody></table></div><p class="note">Tất cả 350 câu có liên kết tới một mục lý thuyết tương ứng. Các dạng ghép nhiều kĩ năng vẫn cần đọc điều kiện từng bài; việc phân loại không thay thế cho kiểm tra lời giải. Chưa có bằng chứng học sinh đã làm mọi bài trong phiếu lớp; chỉ dùng tài liệu và nhật kí để nối nội dung.</p>'
(ROOT/'bao-phu-ly-thuyet.html').write_text(shell('Đối chiếu bao phủ lý thuyết',body),encoding='utf-8')

# Add relevant supplements to each study session, with a reminder not to study all modules.
daily={
'06-10.html':['basic','factor','sum','pair','place','div','last'],
'07-10.html':['seq','cycle','calendar','div','last','crypt','op','table'],
'08-10.html':['area','geo','opt','grid','view','surface'],
'09-10.html':['reverse','assume','ratio','age','worst'],
'10-10.html':['form','multiples','stairs','path','view','solid','table'],
'11-10.html':['basic','calendar'],
'12-10.html':['place','basic','factor'],
'13-10.html':['age','ratio','geo','area','reverse'],
'14-10.html':['basic','place','geo','area','age'],
'15-10.html':['basic','geo']}
for file in list(ROOT.glob('*.html')):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 nav=soup.find('nav')
 if nav and not nav.find('a',href='ly-thuyet-day-du.html'):
  a=soup.new_tag('a',href='ly-thuyet-day-du.html');a.string='Sổ tay lý thuyết';nav.append(a)
 if file.name in daily:
  old=soup.find(id='theory-supplement')
  if old:old.decompose()
  block='<section class="theory" id="theory-supplement"><h3>Lý thuyết bổ sung cho buổi này</h3><p>Chỉ mở mục tương ứng bài đang chọn hoặc lỗi vừa mắc. Không học hết danh sách trong một buổi.</p><ul>'+''.join(f'<li><a href="ly-thuyet-day-du.html#type-{cat}">{h(groups[cat][0]["category_name"])}</a> — nhận biết, từng bước, lưu ý và ví dụ nguyên bản.</li>' for cat in daily[file.name])+'</ul><p><a href="ly-thuyet-day-du.html#nen-tang">Nền tảng giữa kì và 5 mục kĩ năng cần kiểm tra</a></p></section>'
  target=soup.select_one('article.exercise')
  frag=BeautifulSoup(block,'html.parser').section
  if target:target.insert_before(frag)
  else:soup.main.append(frag)
 for item in soup.select('.catalog-item'):
  cat=item.get('data-category')
  if cat:
   p=soup.new_tag('p',attrs={'class':'theory-link'});a=soup.new_tag('a',href='ly-thuyet-day-du.html#type-'+cat);a.string='Đọc lý thuyết đầy đủ và ví dụ đúng dạng';p.append(a);item.select_one('.catalog-body').insert(0,p)
 if file.name in ['index.html','lo-trinh.html']:
  p=soup.new_tag('p',attrs={'class':'note','id':'theory-update'})
  p.append(BeautifulSoup('<b>Đã bổ sung lý thuyết:</b> <a href="ly-thuyet-day-du.html">Sổ tay giữa kì và 50 dạng TIMO</a> · <a href="bao-phu-ly-thuyet.html">Bảng đối chiếu bao phủ</a>. Mỗi bài trong kho đã có liên kết đến cách làm đầy đủ.','html.parser'))
  soup.main.insert(1,p)
 # Fix prose everywhere, including attributes visible to users. Never split or edit MathML.
 for node in list(soup.find_all(string=True)):
  if isinstance(node,Doctype):continue
  if node.parent==soup and str(node).strip()=='html':node.extract();continue
  if node.find_parent(['math','script','style','code','pre']):continue
  node.replace_with(clean_text(str(node)))
 for el in soup.find_all(True):
  for attr in ['alt','title','placeholder','aria-label']:
   if isinstance(el.get(attr),str):el[attr]=clean_text(el[attr])
 file.write_text(str(soup),encoding='utf-8')

with (ROOT/'style.css').open('a',encoding='utf-8') as f:
 f.write('\n/* Theory supplement: clear prose, formulas and source examples. */\n.theory-toc{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0 30px}.theory-toc a{padding:8px 12px;background:#eaf1fc;border-radius:6px;font-size:15px}.theory-warning{border-left:4px solid #d89125;background:#fff5e1;padding:14px 18px;margin-top:22px!important}.theory ol{padding-left:28px}.theory ol li{padding-left:8px;margin:16px 0;line-height:1.85}.theory .source-crop{padding:12px;box-sizing:border-box}.theory-link a{font-weight:700}.coverage-table{overflow-x:auto;margin:24px 0}.coverage-table table{border-collapse:collapse;width:100%;background:white}.coverage-table th,.coverage-table td{padding:15px;text-align:left;border:1px solid #d6e1ee;line-height:1.7}.coverage-table th{background:#e8f0fb}.theory{scroll-margin-top:20px}@media(max-width:600px){.theory .rule{padding:18px 14px}.theory h3{font-size:23px}.coverage-table th,.coverage-table td{padding:10px;min-width:100px}}\n')
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
manifest.update(theory_timo_categories=50,theory_preliminary_categories=36,theory_national_only_categories=14,theory_midterm_extra_skills=5)
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Completed theory for 50 categories (36 preliminary,14 national-only); retained',len(existing),'school theory groups; added 5 school skills. Fixed prose spacing across all HTML without touching MathML.')
