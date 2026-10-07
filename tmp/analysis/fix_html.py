from pathlib import Path
p=Path('tmp/analysis/build_html.py');s=p.read_text(encoding='utf-8')
start=s.index("'Cạnh hình lớn AD=64:4=16cm.");end=s.index("',4,fig=True)",start)
s=s[:start]+"'Cạnh hình lớn AD=64:4=16cm. AB=BD nên AB=BD=8cm. BC=CD nên BC=CD=4cm. Trong ba hình vuông, hình dưới bên phải rộng BD=8cm nên cao8cm; hai hình vuông trên bên phải có cạnh CD=4cm nên DE=EF=4cm. Hai phần bên trái và giữa là hình chữ nhật. Diện tích hình vuông nhỏ nhất=4×4=<b>16cm²</b>."+s[end:]
s=s.replace("'TT16':(380,280,565,420),'TT17':(380,420,565,530),'TT18':(375,535,565,650)","'TT16':(417,306,556,438),'TT17':(420,446,565,572),'TT18':(417,592,548,723)")
s=s.replace('import fitz, json','import fitz, json, shutil')
s=s.replace("def link(source,page):return '../../inputdata/'+quote(source)+'#page='+str(page)","def link(source,page):\n (OUT/'sources').mkdir(exist_ok=True)\n shutil.copy2(ROOT/'inputdata'/source,OUT/'sources'/source)\n return 'sources/'+quote(source)+'#page='+str(page)")
s=s.replace('Link PDF mở file trong thư mục inputdata; ảnh nguồn đã được kèm trong bộ HTML để xem khi sao chép cả thư mục html.','Link PDF mở bản sao nguồn kèm trong thư mục sources; ảnh nguồn cũng được kèm. Sao chép cả thư mục html để giữ đầy đủ hình và PDF.')
p.write_text(s,encoding='utf-8')
