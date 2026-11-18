// Optional isolated Chromium check of the actual distributed ZIP.
// npm install --prefix /tmp/metamer-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/metamer-browser/node_modules node atlas/samples/metamer/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');
(async()=>{
 const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
 const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
 const root=path.resolve(__dirname,'../../..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'metamer-live-'));
 try{
  execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/metamer/bench.zip'),temp]);
  const expected=JSON.parse(execFileSync(process.env.PYTHON||path.join(root,'.venv/bin/python'),['-c',`import sys,json;sys.path.insert(0,sys.argv[1]);import model,measure;s,p=measure.load_csv(sys.argv[2]);print(json.dumps([{'mix':t,'adapt':a,'result':model.evaluate(s,p,t,a)} for t in (0,.01,.25,.5,.75,1) for a in (True,False)]))`,path.join(root,'atlas/samples/metamer'),path.join(root,'assets/metamer/spectra.csv')],{encoding:'utf8'}));
  const page=await browser.newPage({viewport:{width:1100,height:1000}}),errors=[],http=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
  await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
  for(const trial of expected){
   const actual=await page.evaluate(({mix,adapt})=>evaluate(mix,adapt),trial),wanted=trial.result;
   for(const key of ['xyz','adapted_xyz','linear_rgb'])for(let i=0;i<2;i++)for(let j=0;j<3;j++)assert.ok(Math.abs(actual[key][i][j]-wanted[key][i][j])<1e-10,`${key} mismatch`);
   assert.ok(Math.abs(actual.delta_e76-wanted.delta_e76)<1e-9);assert.deepEqual(actual.rgb8,wanted.rgb8);assert.equal(actual.gamut_clipped,wanted.gamut_clipped);
  }
  const graph=()=>page.locator('#curves').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data));
  const originalGraph=await graph();assert.ok(await page.evaluate(()=>result.delta_e76<1e-10));
  await page.locator('#mix').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#mix').inputValue(),'1');
  await page.locator('#lamp').click();assert.ok(await page.evaluate(()=>result.delta_e76>40));
  const samples=await page.locator('#swatches').evaluate(c=>{const ctx=c.getContext('2d');return [Array.from(ctx.getImageData(150,100,1,1).data),Array.from(ctx.getImageData(480,100,1,1).data)]});
  const desired=expected.find(t=>t.mix===1&&t.adapt).result.rgb8;assert.deepEqual(samples,desired.map(rgb=>[...rgb,255]));
  await page.locator('#adapt').uncheck();assert.equal(await page.locator('#adapt').isChecked(),false);assert.match(await page.locator('#status').textContent(),/без адаптации/);
  await page.locator('#day').click();assert.equal(await page.locator('#adapt').isChecked(),true);assert.equal(await page.locator('#mix').inputValue(),'0');assert.ok(await page.evaluate(()=>result.delta_e76<1e-10));
  assert.deepEqual(await graph(),originalGraph);
  await page.setViewportSize({width:390,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
  console.log('PASS extracted ZIP: JS/Python XYZ, adapted XYZ, linear RGB, RGB8 and deltaE on 12 cases; canvas exact RGB; keyboard/lamp/adapt/reset/mobile, invariant reflectances; no JS errors or HTTP');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
