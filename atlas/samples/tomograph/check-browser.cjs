// Optional isolated Chromium check of the actual distributed ZIP (sandbox disabled by helper).
// npm install --prefix /tmp/lens-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/lens-browser/node_modules node atlas/samples/tomograph/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');const {pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');const {PNG}=require('pngjs');
(async()=>{
  const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
  const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'tomo-live-'));
  try {
    const root=path.resolve(__dirname,'../../..');
    execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/tomograph/bench.zip'),temp]);
    const page=await browser.newPage({viewport:{width:1100,height:1000}}),errors=[],http=[];
    page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
    await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('120'));
    const pixels=()=>page.locator('#view').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data));
    const initial=await pixels();
    const expected=PNG.sync.read(fs.readFileSync(path.join(root,'assets/tomograph/bench-reference.png'))).data;
    let maximum=0;for(let i=0;i<initial.length;i++)maximum=Math.max(maximum,Math.abs(initial[i]-expected[i]));
    assert.ok(maximum<=1,`Python/JS maximum pixel difference ${maximum}`);
    await page.locator('#views').focus();await page.keyboard.press('ArrowUp');
    assert.equal(await page.locator('#views').inputValue(),'60');
    assert.notDeepEqual(await pixels(),initial);
    await page.locator('#filter').uncheck();assert.notDeepEqual(await pixels(),initial);
    assert.match(await page.locator('#status').textContent(),/без фильтра/);
    await page.locator('#reset').click();assert.deepEqual(await pixels(),initial);
    await page.setViewportSize({width:390,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
    console.log('PASS: extracted one-file ZIP; JS FFT+FBP vs Python max pixel error <=1; keyboard/views/filter/reset/mobile; no JS errors or HTTP');
  } finally {await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
