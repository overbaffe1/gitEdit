// Optional Chromium validation of the extracted ZIP (isolated environment).
// npm install --prefix /tmp/twins-browser playwright-core @sparticuz/chromium
// NODE_PATH=/tmp/twins-browser/node_modules node atlas/samples/twins/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');
(async()=>{
 const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
 const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
 const root=path.resolve(__dirname,'../../..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'twins-live-'));
 try{
  execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/twins/bench.zip'),temp]);
  const expected=JSON.parse(execFileSync(process.env.PYTHON||path.join(root,'.venv/bin/python'),['-c',`import sys,json;sys.path.insert(0,sys.argv[1]);import certify,heat;from pathlib import Path;p=Path(sys.argv[2]);a=certify.load(p/'rook.csv');b=certify.load(p/'shrikhande.csv');c=[row[:] for row in b];c[0][1]=c[1][0]=0;print(json.dumps([{'graph':i,'time':t,'kernel':heat.kernel(m,t).tolist()} for i,m in enumerate((a,b,c)) for t in (0,.03,.25,1,2)]))`,path.join(root,'atlas/samples/twins'),path.join(root,'assets/twins')],{encoding:'utf8'}));
  const page=await browser.newPage({viewport:{width:1100,height:1100}}),errors=[],http=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
  await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
  for(const trial of expected){
   const actual=await page.evaluate(({graph,time})=>{const a=original[graph===0?0:1].map(r=>r.slice());if(graph===2)a[0][1]=a[1][0]=0;return kernel(a,time)},trial);
   for(let i=0;i<16;i++)for(let j=0;j<16;j++)assert.ok(Math.abs(actual[i][j]-trial.kernel[i][j])<5e-15,'heat kernel differs');
  }
  const reports=await page.evaluate(()=>verify());assert.deepEqual(reports.map(r=>[r.edges,r.identity,r.cliques.length]),[[48,true,8],[48,true,0]]);
  assert.ok(await page.evaluate(()=>Math.abs(state.traces[0]-state.traces[1])<1e-12));
  const pixel=await page.locator('#rook').evaluate(c=>{const p=cfg.positions[0][0];return Array.from(c.getContext('2d').getImageData(Math.round(p[0]),Math.round(p[1])+8,1,1).data)});
  const sourceHeat=expected.find(r=>r.graph===0&&r.time===.25).kernel[0][0],cold=[29,66,82],hot=[245,209,154];
  assert.deepEqual(pixel,[...cold.map((v,i)=>Math.floor(v+(hot[i]-v)*Math.sqrt(sourceHeat)+.5)),255]);
  await page.locator('#time').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#time').inputValue(),'26');
  await page.locator('#source').selectOption({value:'7'});assert.equal(await page.evaluate(()=>state.source),7);
  await page.locator('#clique').click();assert.equal(await page.evaluate(()=>highlight),true);
  await page.locator('#break').click();assert.ok(await page.evaluate(()=>Math.abs(state.traces[0]-state.traces[1])>.1));
  assert.equal(await page.locator('#break').isDisabled(),true);assert.equal((await page.evaluate(()=>verify()))[1].identity,false);
  await page.locator('#reset').click();assert.equal(await page.evaluate(()=>state.broken),false);assert.equal(await page.locator('#time').inputValue(),'25');assert.equal(await page.locator('#source').inputValue(),'0');
  await page.setViewportSize({width:390,height:1000});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
  console.log('PASS extracted ZIP: 15 full JS/Python kernel matrices within 5e-15; integer A² and all K4 counts; canvas heat colour exact; keyboard/source/clique/delete/reset/mobile; no JS errors or HTTP');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
