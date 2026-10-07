import {spawn} from 'node:child_process';
import {writeFileSync,mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const dir=resolve('tmp/analysis/qa');mkdirSync(dir,{recursive:true});
const bin=process.env.LOCALAPPDATA+'/ms-playwright/chromium-1243/chrome-win64/chrome.exe';
const child=spawn(bin,['--headless=new','--no-sandbox','--disable-gpu','--remote-debugging-port=9337','--remote-allow-origins=*','--allow-file-access-from-files','--user-data-dir='+resolve('tmp/qa-chromium-profile'),'about:blank'],{windowsHide:true,stdio:'ignore'});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
let ws;
try{
 let targets;
 for(let i=0;i<30;i++){try{targets=await(await fetch('http://127.0.0.1:9337/json')).json();break}catch{await pause(300)}}
 if(!targets)throw Error('Chromium could not start');
 ws=new WebSocket(targets.find(x=>x.type==='page').webSocketDebuggerUrl);
 await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 let seq=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}};
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 const evaluate=async expression=>(await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true})).result.value;
 await call('Page.enable');
 const report=[];
 for(const width of [1280,390]){
  await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:width<600});
  for(const name of ['index','bai-hoc-toan-4','07-10','timo-vl-1','timo-qg-7','timo-day-du']){
   await call('Page.navigate',{url:pathToFileURL(resolve('output/html/'+name+'.html')).href});
   await pause(600);
   await evaluate(`Promise.all([document.fonts.ready,...Array.from(document.images).filter(i=>i.loading!=='lazy').map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r}))])`);
   const check=await evaluate(`(()=>{const visible=e=>{const r=e.getBoundingClientRect();return r.width&&r.height};return {title:document.title,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,overflow:Array.from(document.querySelectorAll('main *')).filter(e=>visible(e)&&e.getBoundingClientRect().right>innerWidth+2&&getComputedStyle(e).position!=='absolute').slice(0,8).map(e=>e.tagName+'.'+e.className),hiddenTheory:document.querySelectorAll('details.reference-theory,details.reading-help,details.teach-model').length,theoryPanels:document.querySelectorAll('.visible-theory').length}})()`);
   const shot=await call('Page.captureScreenshot',{format:'png'});writeFileSync(dir+'/'+name+'-'+width+'.png',Buffer.from(shot.data,'base64'));
   if(name==='bai-hoc-toan-4'){
    await evaluate(`document.getElementById('hinh').scrollIntoView()`);await pause(200);
    const shot=await call('Page.captureScreenshot',{format:'png'});writeFileSync(dir+'/diagram-'+width+'.png',Buffer.from(shot.data,'base64'));
   }
   if(name==='timo-vl-1'){
    const interaction=await evaluate(`(()=>{const d=document.querySelector('.original-solution');const closed=!d.open;d.open=true;const opened=d.open;showAnswers(false);const hidden=!d.open;const e=document.querySelector('textarea');e.value='QA temporary';e.dispatchEvent(new Event('input'));const k='timo2026:'+location.pathname+':'+e.dataset.save;const saved=localStorage.getItem(k)==='QA temporary';localStorage.removeItem(k);e.value='';return {closed,opened,hidden,saved}})()`);check.interaction=interaction;
    await call('Emulation.setEmulatedMedia',{media:'print'});
    check.printTheory=await evaluate(`getComputedStyle(document.querySelector('.visible-theory')).display`);
    await call('Emulation.setEmulatedMedia',{media:'screen'});
   }
   report.push({page:name,viewport:width,...check});
  }
 }
 writeFileSync(dir+'/visual-results.json',JSON.stringify(report,null,2));
 const failures=report.filter(x=>x.scrollWidth>x.width+2||x.hiddenTheory||x.interaction&&Object.values(x.interaction).some(v=>!v)||x.printTheory==='none');
 console.log(JSON.stringify({screenshots:14,pages:6,viewports:[1280,390],failures,report:dir+'/visual-results.json'},null,2));
 if(failures.length)process.exitCode=1;
}finally{ws?.close();child.kill()}
