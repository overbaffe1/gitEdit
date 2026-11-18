// Optional isolated Chromium check of the actual distributed ZIP (sandbox disabled by helper).
// npm install --prefix /tmp/lens-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/lens-browser/node_modules node atlas/samples/lens/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');const {pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');const {PNG}=require('pngjs');
(async()=>{
  const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
  const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lens-live-'));
  try {
    const root=path.resolve(__dirname,'../../..');
    execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/lens/bench.zip'),temp]);
    const page=await browser.newPage({viewport:{width:1100,height:1000}}),errors=[],http=[];
    page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
    await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('на оси'));
    const pixels=id=>page.locator('#'+id).evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data));
    const initial={source:await pixels('source'),lensed:await pixels('lensed')};
    for(const [id,file] of [['source','bench-source.png'],['lensed','bench-ring.png']]){
      const expected=PNG.sync.read(fs.readFileSync(path.join(root,'assets/lens',file))).data;
      const actual=initial[id];let maximum=0;
      for(let i=0;i<actual.length;i++)maximum=Math.max(maximum,Math.abs(actual[i]-expected[i]));
      assert.ok(maximum<=1,`${id}: maximum Python/JS pixel difference ${maximum}`);
    }
    await page.locator('#offset').focus();await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#offset').inputValue(),'0.01');
    assert.notDeepEqual(await pixels('lensed'),initial.lensed);
    await page.locator('#offset').evaluate(e=>{e.value=.55;e.dispatchEvent(new Event('input'))});
    assert.notDeepEqual(await pixels('source'),initial.source);
    await page.locator('#radius').evaluate(e=>{e.value=0;e.dispatchEvent(new Event('input'))});
    assert.deepEqual(await pixels('source'),await pixels('lensed'));
    assert.match(await page.locator('#status').textContent(),/выключена/);
    await page.locator('#align').click();
    assert.deepEqual(await pixels('source'),initial.source);
    assert.deepEqual(await pixels('lensed'),initial.lensed);
    await page.setViewportSize({width:390,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
    console.log('PASS: extracted one-file ZIP; live JS vs Python pixels max error <=1, offset/keyboard/reset, zero-lens exact identity, mobile; no JS errors or HTTP');
  } finally {await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
