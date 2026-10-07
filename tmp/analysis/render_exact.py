from pathlib import Path
import subprocess
root=Path.cwd()
args=[r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--allow-file-access-from-files','--user-data-dir='+str(root/'tmp/html-exact-profile'),'--window-size=1280,1900','--screenshot='+str(root/'tmp/analysis/html-exact.png'),(root/'tmp/analysis/exact-preview.html').as_uri()]
subprocess.run(args,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW,check=True)
print('Screenshot exists:',(root/'tmp/analysis/html-exact.png').exists())
