from pathlib import Path
import subprocess
root=Path.cwd()
for name,width,height in [('lo-trinh',1280,1600),('lo-trinh',500,1500),('danh-muc-timo',1280,1400)]:
 args=[r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--allow-file-access-from-files','--user-data-dir='+str(root/'tmp/html-catalog-profile'),'--window-size='+str(width)+','+str(height),'--screenshot='+str(root/f'tmp/analysis/{name}-{width}.png'),(root/f'output/html/{name}.html').as_uri()]
 subprocess.run(args,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW,check=True)
 print(name,width,'rendered')
