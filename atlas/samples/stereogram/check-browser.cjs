// Optional, isolated sandbox only (Chromium sandbox disabled by helper).
// npm install --prefix /tmp/stereo-browser playwright-core @sparticuz/chromium
// NODE_PATH=/tmp/stereo-browser/node_modules node atlas/samples/stereogram/check-browser.cjs
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {execFileSync}=require('node:child_process');
const {pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');
(async()=>{
  const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
  const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'stereo-bench-'));
  try {
    const root=path.resolve(__dirname,'../../..');
    // Test the distributed archive, not a development-only web server.
    execFileSync('python3',['-m','zipfile','-e',path.join(root,'assets/stereogram/bench.zip'),temp]);
    const page=await browser.newPage({viewport:{width:1100,height:1000}});
    const errors=[],network=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
    await page.goto(pathToFileURL(path.join(temp,'bench.html')).href);
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('Строка 240'));
    const initial=await page.locator('canvas').screenshot();
    await page.locator('#pair').focus();await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#pair').inputValue(),'1');
    assert.notDeepEqual(await page.locator('canvas').screenshot(),initial);
    await page.locator('#mode').click();
    assert.match(await page.locator('#status').textContent(),/Исходная карта/);
    assert.equal(await page.locator('#pair').isDisabled(),true);
    const reveal=await page.locator('canvas').screenshot();
    assert.notDeepEqual(reveal,initial);
    await page.locator('#mode').click();
    assert.equal(await page.locator('#pair').isDisabled(),false);
    await page.locator('#pair').evaluate(e=>{e.value=e.max;e.dispatchEvent(new Event('input'))});
    const facts=JSON.parse(fs.readFileSync(path.join(root,'assets/stereogram/facts.json'),'utf8'));
    const last=facts.sample_row_edges.at(-1);
    assert.match(await page.locator('#status').textContent(),new RegExp('пиксели '+last[1]+' и '+last[2]));
    await page.locator('#reset').click();
    assert.equal(await page.locator('#pair').inputValue(),'0');
    assert.deepEqual(await page.locator('canvas').screenshot(),initial);
    // Narrow viewport: controls remain usable, no forced horizontal page overflow.
    await page.setViewportSize({width:390,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.locator('#mode').click();
    assert.match(await page.locator('#status').textContent(),/Исходная карта/);
    assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
    console.log('PASS: extracted ZIP loads offline; images, keyboard/range, reveal/reset, mobile width; no JS errors or HTTP requests');
  } finally {await browser.close();fs.rmSync(temp,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
