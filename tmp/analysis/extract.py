from pathlib import Path
import fitz, zipfile, xml.etree.ElementTree as E
root=Path('inputdata'); out=Path('tmp/analysis')
for p in root.glob('*.pdf'):
 d=fitz.open(p)
 pages=[page.get_text() for page in d]
 (out/(p.stem+'.txt')).write_text('\n'.join(f'\n=== PDF PAGE {i+1} ===\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
 print(p.name, 'pages=',len(d),'text_chars=',sum(map(len,pages)))
p=next(root.glob('*.xlsx')); ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:
 strings=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  strings=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml'))]
 wb=E.fromstring(z.read('xl/workbook.xml'))
 rel={n.attrib['Id']:n.attrib['Target'] for n in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 result=[]
 for sheet in wb.find('m:sheets',ns):
  if not sheet.attrib['name'].startswith('BTVN'): continue
  target=rel[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
  path=target.lstrip('/') if target.startswith('/') else 'xl/'+target
  result.append('\n=== SHEET '+sheet.attrib['name']+' ===')
  for row in E.fromstring(z.read(path)).findall('.//m:sheetData/m:row',ns):
   cells=[]
   for c in row:
    v=c.find('m:v',ns); val=v.text if v is not None else ''
    if c.attrib.get('t')=='s': val=strings[int(val)] if val else ''
    if c.attrib.get('t')=='inlineStr': val=''.join(c.find('m:is',ns).itertext())
    if val: cells.append(c.attrib['r']+'='+val)
   if cells: result.append(' | '.join(cells))
 (out/'workbook.txt').write_text('\n'.join(result),encoding='utf-8')
 print('WORKBOOK',len(result),'rows')
