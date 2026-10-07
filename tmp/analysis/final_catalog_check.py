from pathlib import Path
import json,re
from collections import Counter
from bs4 import BeautifulSoup
root=Path('output/html')
records=json.loads((root/'danh-muc-timo.json').read_text(encoding='utf-8'))
assert len(records)==350 and len({r['id'] for r in records})==350
assert Counter(r['round'] for r in records)=={'VL':175,'QG':175}
assert all(v==25 for v in Counter((r['round'],r['exam']) for r in records).values())
for r in records:
 for key in ['question_images','solution_images']:
  assert r[key] and all((root/p).is_file() for p in r[key]),r['id']
for name in ['lo-trinh.html','danh-muc-timo.html']:
 p=root/name;soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for node in list(soup.find_all(string=True)):
  if node.parent.name in ['script','style']:continue
  s=str(node)
  s=re.sub(r'(\d)(?=[^\W\d_])',r'\1 ',s)
  s=re.sub(r'([^\W\d_])(?=\d)',r'\1 ',s)
  s=re.sub(r'([:,;])(?=[^\W\d_])',r'\1 ',s)
  node.replace_with(s)
 if name=='danh-muc-timo.html':
  item=soup.find(id='VL-2-20')
  note=soup.new_tag('p',attrs={'class':'note'})
  note.string='Lưu ý lời giải gốc: hình thuyền còn có 5 tam giác ở cột buồm. Tổng đúng là 5 + 4 + 14 = 23; xem phần chữa thi thử để đối chiếu.'
  item.find(class_='catalog-body').insert(0,note)
 p.write_text(str(soup),encoding='utf-8')
plan=Path('output/Phan-tich-va-ke-hoach-on-TIMO.md')
with plan.open('a',encoding='utf-8') as f:
 f.write('\n\n## Cập nhật: rà toàn bộ TIMO và lộ trình chọn bài\n\nĐã lập danh mục 350 câu của 14 đề: 175 câu vòng loại và 175 câu vòng quốc gia, đối chiếu trang đề và trang lời giải. Đây là kho chọn bài, không phải khối lượng phải làm hết.\n\n- [Lộ trình chọn bài cập nhật](html/lo-trinh.html): từng ngày đến thi TIMO Chủ nhật 11/10 và giữa kì 15/10; chọn bài đại diện, đổi bài khi cần, dừng khi đã nắm dạng.\n- [Danh mục toàn bộ TIMO](html/danh-muc-timo.html): lọc theo vòng, dạng và vai trò, xem ảnh nguyên bản đề/lời giải cùng số trang.\n- [Danh mục CSV](html/danh-muc-timo.csv): dùng để lọc trong Excel.\n\nLộ trình HTML này là bản cập nhật để chọn bài từ toàn bộ kho; tiếp tục dùng các trang theo ngày và ngân hàng đề cương để học lý thuyết và ôn đủ 38 bài giữa kì. Việc rà kho không đồng nghĩa đã giải lại độc lập cả 350 câu.\n')
print('PASS: 350 unique questions; 14 complete exams; every original question and solution crop exists.')
for rid in ['VL-1-7','VL-3-7','QG-6-19']:
 r=next(r for r in records if r['id']==rid);print(rid,r['question_images'])
