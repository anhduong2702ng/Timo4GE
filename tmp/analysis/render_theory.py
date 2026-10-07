from pathlib import Path
import subprocess
root=Path.cwd()
for name,width,height in [('theory-preview',1280,2100),('theory-preview',500,1800)]:
 args=[r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--allow-file-access-from-files','--user-data-dir='+str(root/'tmp/html-theory-profile'),'--window-size='+str(width)+','+str(height),'--screenshot='+str(root/f'tmp/analysis/{name}-{width}.png'),(root/f'tmp/analysis/{name}.html').as_uri()]
 subprocess.run(args,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW,check=True)
 print(name,width,'rendered')
