// Optional: npm install --prefix /tmp/threadmoon-browser playwright-core @sparticuz/chromium
// NODE_PATH=/tmp/threadmoon-browser/node_modules node atlas/samples/threadmoon/check-browser.cjs
// Run only in an isolated sandbox: Chromium sandbox is disabled by this helper.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium:playwright} = require('playwright-core');
(async()=>{
  const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
  const executablePath=process.env.CHROMIUM_PATH || await chromium.executablePath();
  const browser=await playwright.launch({executablePath,args:chromium.args,headless:true});
  try {
    const page=await browser.newPage();
    const errors=[],network=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
    const root=path.resolve(__dirname,'../../..');
    await page.goto(pathToFileURL(path.join(root,'assets/threadmoon/counter.html')).href);
    assert.equal(await page.locator('#prev').isDisabled(),true);
    const initial=await page.locator('canvas').evaluate(c=>c.toDataURL());
    await page.locator('#next').click();
    const facts=JSON.parse(fs.readFileSync(path.join(root,'assets/threadmoon/facts.json'),'utf8'));
    assert.match(await page.locator('#status').textContent(),new RegExp('000 → '+String(facts.route[1]).padStart(3,'0')));
    assert.notEqual(await page.locator('canvas').evaluate(c=>c.toDataURL()),initial);
    await page.locator('#step').evaluate(e=>{e.value=e.max;e.dispatchEvent(new Event('input'))});
    assert.match(await page.locator('#status').textContent(),/маршрут закончен/);
    assert.equal(await page.locator('#next').isDisabled(),true);
    await page.locator('#prev').click();
    assert.equal(await page.locator('#step').inputValue(),'458');
    await page.locator('#reset').click();
    assert.equal(await page.locator('#step').inputValue(),'0');
    assert.equal(await page.locator('canvas').evaluate(c=>c.toDataURL()),initial);
    // Standard range keyboard interaction, no custom arrow-key interceptor.
    await page.locator('#step').focus();await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#step').inputValue(),'1');
    assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
    console.log('PASS: next/back/reset/slider/keyboard/canvas, no JS errors or HTTP requests');
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
