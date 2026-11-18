// Optional isolated Chromium test. Install separately:
// npm install --prefix /tmp/shards-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/shards-browser/node_modules node atlas/samples/shards/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core'),{PNG}=require('pngjs');
(async()=>{
 const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
 const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
 const root=path.resolve(__dirname,'../../..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'shards-live-'));
 try{
  execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/shards/bench.zip'),temp]);
  const page=await browser.newPage({acceptDownloads:true,viewport:{width:1100,height:1000}}),errors=[],http=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
  await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);await page.waitForFunction(()=>lastBytes!==null);
  const original=fs.readFileSync(path.join(root,'assets/shards/source.png'));
  const compareBytes=async()=>assert.deepEqual(Buffer.from(await page.evaluate(()=>Array.from(lastBytes))),original);
  await compareBytes();
  const actual=await page.locator('#view').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data));
  assert.deepEqual(Buffer.from(actual),PNG.sync.read(original).data);
  const trials=await page.evaluate(async()=>{let count=0;for(let a=0;a<5;a++)for(let b=a+1;b<6;b++)for(let c=b+1;c<7;c++)for(let d=c+1;d<8;d++)for(let e=d+1;e<9;e++)for(let f=e+1;f<10;f++){await choose([a,b,c,d,e,f]);if(!lastBytes||await sha(lastBytes)!==records[0].sha256)throw Error('subset failed');count++}return count});
  assert.equal(trials,210);await compareBytes();
  await page.locator('#five').click();await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('недостаточно'));
  assert.equal(await page.evaluate(()=>lastBytes),null);assert.equal(await page.locator('#download').isHidden(),true);
  await page.locator('#six').click();await page.waitForFunction(()=>lastBytes!==null);await compareBytes();
  await page.locator('#damage').click();await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('не совпала'));
  assert.equal(await page.evaluate(()=>lastBytes),null);assert.equal(await page.locator('#download').isHidden(),true);
  await page.locator('#reset').click();await page.waitForFunction(()=>lastBytes!==null);
  await page.locator('#shard-0').focus();await page.keyboard.press('Space');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('9/10: восстановлено'));await compareBytes();
  // Damaged shard can be excluded, but is not silently treated as an erasure.
  await page.locator('#damage').click();await page.waitForFunction(()=>lastBytes===null);
  await page.locator('#shard-1').uncheck();await page.waitForFunction(()=>lastBytes!==null);await compareBytes();
  // Race: no earlier successful async decode may re-show a stale image after five selected.
  await page.evaluate(async()=>{const prior=choose([2,3,4,5,6,7]);await choose([2,3,4,5,6]);await prior});
  assert.equal(await page.evaluate(()=>lastBytes),null);
  await page.locator('#reset').click();await page.waitForFunction(()=>lastBytes!==null);
  const waitDownload=page.waitForEvent('download');await page.locator('#download').click();const download=await waitDownload;
  assert.deepEqual(fs.readFileSync(await download.path()),original);
  await page.setViewportSize({width:390,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
  console.log('PASS extracted ZIP: all 210 subsets in real JS; exact bytes, PNG pixels and downloaded PNG; five-shard refusal, corrupt/remove/reset, keyboard, stale async guard, mobile; no HTTP or JS errors');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
