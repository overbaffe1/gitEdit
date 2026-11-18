// Optional isolated Chromium check of the distributed ZIP; no-sandbox only in isolated test environment.
// npm install --prefix /tmp/echo-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/echo-browser/node_modules node atlas/samples/echo/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core'),{PNG}=require('pngjs');
(async()=>{
 const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
 const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'echo-live-')),root=path.resolve(__dirname,'../../..');
 try{
  execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/echo/bench.zip'),temp]);
  const page=await browser.newPage({viewport:{width:1100,height:1000}}),errors=[],http=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
  await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
  const pixels=()=>page.locator('#view').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data));
  const compare=async file=>{const actual=await pixels(),expected=PNG.sync.read(fs.readFileSync(path.join(root,'assets/echo',file))).data;let max=0;for(let i=0;i<actual.length;i++)max=Math.max(max,Math.abs(actual[i]-expected[i]));assert.ok(max<=1,`${file}: pixel max diff ${max}`)};
  await compare('source.png');await page.locator('#end').click();await compare('turn.png');
  await page.locator('#end').click();await compare('reverse.png');assert.ok(await page.evaluate(()=>error()<1e-12));
  assert.equal(await page.locator('#step').isDisabled(),true);
  await page.locator('#reset').click();await compare('source.png');
  await page.locator('#mode').focus();await page.keyboard.press('ArrowDown');assert.equal(await page.locator('#mode').inputValue(),'zero');
  await page.locator('#end').click();await page.locator('#end').click();await compare('zero.png');assert.ok(await page.evaluate(()=>error()>.6));
  assert.equal(await page.locator('#mode').isDisabled(),true);
  await page.locator('#reset').click();await page.locator('#mode').selectOption('keep');
  await page.locator('#step').click();assert.match(await page.locator('#status').textContent(),/Шаг 12/);
  await page.locator('#end').click();await page.locator('#end').click();await compare('keep.png');
  await page.setViewportSize({width:390,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
  console.log('PASS extracted ZIP: JS/Python source, turn and all 3 final fields max RGB difference <=1; return error <1e-12; keyboard/step/reset/locks/mobile; no JS errors or HTTP');
 }finally{await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
