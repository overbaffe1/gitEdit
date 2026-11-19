// Optional Chromium check of distributed ZIP, isolated environment.
// npm install --prefix /tmp/locator-browser playwright-core @sparticuz/chromium
// NODE_PATH=/tmp/locator-browser/node_modules node atlas/samples/locator/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');
(async()=>{
 const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
 const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
 const root=path.resolve(__dirname,'../../..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'locator-live-'));
 try{
  execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/locator/bench.zip'),temp]);
  const page=await browser.newPage({viewport:{width:1200,height:1100}}),errors=[],http=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
  await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
  const expected=fs.readFileSync(path.join(root,'assets/locator/windows.csv'),'utf8').trim().split('\n').slice(1).map(line=>{const [x,y,four,six]=line.split(',');return {x:Number(x),y:Number(y),hex:six}});
  const actual=await page.evaluate(()=>entries.map(e=>({x:e.x,y:e.y,hex:e.code.toString(16).padStart(9,'0')})));assert.deepEqual(actual,expected);
  const cert=await page.evaluate(()=>audit());assert.deepEqual(cert,{unique4:4095,unique6:4095,rank:12,extended_size:4096,linear:true,minWeight:7});
  const count=await page.evaluate(()=>{let count=0;for(let i=0;i<entries.length;i+=137){const e=entries[i],observed=e.code^(1n<<35n)^(1n<<19n)^(1n<<2n),r=decode(observed);if(!r.accepted||r.position.x!==e.x||r.position.y!==e.y||r.position.distance!==3)throw Error('3-bit decode failed');count++}return count});assert.equal(count,30);
  assert.ok(await page.evaluate(()=>state.accepted&&state.position.x===9&&state.position.y===12));
  await page.locator('#three').click();assert.equal(await page.evaluate(()=>state.flips),3);assert.equal(await page.evaluate(()=>state.position.distance),3);
  await page.locator('#four').click();assert.deepEqual(await page.evaluate(()=>state.position),{x:11,y:4,distance:3});assert.match(await page.locator('#oracle').textContent(),/НЕВЕРНЫЙ/);
  await page.locator('#zero').click();assert.equal(await page.evaluate(()=>state.accepted),false);
  await page.locator('#reset').click();assert.equal(await page.evaluate(()=>state.flips),0);
  await page.locator('#patch button').first().focus();await page.keyboard.press('Space');assert.equal(await page.evaluate(()=>state.flips),1);assert.ok(await page.evaluate(()=>state.accepted));
  await page.locator('#x').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#x').inputValue(),'10');assert.equal(await page.evaluate(()=>state.flips),0);
  await page.locator('#wrap').click();assert.deepEqual(await page.evaluate(()=>state.position),{x:61,y:63,distance:0});
  const grid=fs.readFileSync(path.join(root,'assets/locator/pattern.csv'),'utf8').trim().split('\n').map(line=>line.split(',').map(Number));
  const samples=await page.locator('#map').evaluate(c=>{const ctx=c.getContext('2d');return [[4,4],[252,260],[500,516]].map(([x,y])=>Array.from(ctx.getImageData(x,y,1,1).data))});
  assert.deepEqual(samples,[[0,0],[31,32],[62,64]].map(([x,y])=>{const v=grid[y][x]*255;return [v,v,v,255]}));
  await page.locator('#map').click({position:{x:200,y:200}});assert.equal(await page.evaluate(()=>state.flips),0);assert.ok(await page.evaluate(()=>state.accepted&&state.position.x===state.truth.x&&state.position.y===state.truth.y));
  await page.setViewportSize({width:390,height:1000});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
  console.log('PASS extracted ZIP: all 4095 JS/Python signatures incl >32 bits; exact GF2 certificate; 30 3-flip decodes; accepted wrong 4-flip counterexample, refusal, keyboard/click/wrap/reset/mobile; canvas bits exact; no HTTP or JS errors');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
