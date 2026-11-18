// Optional isolated Chromium test of the distributed ZIP (sandbox disabled by helper).
// npm install --prefix /tmp/veil-browser playwright-core @sparticuz/chromium pngjs
// NODE_PATH=/tmp/veil-browser/node_modules node atlas/samples/veil/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');const {pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');const {PNG}=require('pngjs');
(async()=>{
  const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
  const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'veil-bench-'));
  try {
    const root=path.resolve(__dirname,'../../..');
    execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/veil/bench.zip'),temp]);
    const page=await browser.newPage({viewport:{width:1000,height:1000}}),errors=[],http=[];
    page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))http.push(r.url())});
    await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('сдвиг 9'));
    await page.locator('#align').click();
    assert.match(await page.locator('#status').textContent(),/точное совмещение/);
    const actual=await page.locator('canvas').evaluate(c=>Array.from(c.getContext('2d').getImageData(16,16,256,192).data));
    const expected=PNG.sync.read(fs.readFileSync(path.join(root,'assets/veil/stack.png')));
    assert.deepEqual(Buffer.from(actual),expected.data);
    for(const [mode,file] of [['a','sheet-a.png'],['b','sheet-b.png']]){
      await page.locator('#mode').selectOption(mode);
      assert.equal(await page.locator('#shift').isDisabled(),true);
      const rgba=PNG.sync.read(fs.readFileSync(path.join(root,'assets/veil',file))).data;
      const white=Buffer.alloc(rgba.length,255);
      for(let i=0;i<rgba.length;i+=4){const val=255-rgba[i+3];white[i]=val;white[i+1]=val;white[i+2]=val}
      const pixels=await page.locator('canvas').evaluate(c=>Array.from(c.getContext('2d').getImageData(16,16,256,192).data));
      assert.deepEqual(Buffer.from(pixels),white);
    }
    await page.locator('#align').click();await page.locator('#shift').focus();await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#shift').inputValue(),'1');
    const shifted=await page.locator('canvas').evaluate(c=>Array.from(c.getContext('2d').getImageData(16,16,256,192).data));
    assert.notDeepEqual(Buffer.from(shifted),expected.data);
    await page.setViewportSize({width:390,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.locator('#align').click();assert.equal(await page.locator('#shift').inputValue(),'0');
    assert.deepEqual(errors,[]);assert.deepEqual(http,[]);
    console.log('PASS: extracted ZIP; browser pixels match stack and each standalone sheet exactly; align/range/keyboard/mobile; no JS errors or HTTP');
  } finally {await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
