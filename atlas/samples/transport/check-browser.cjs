// npm install --prefix /tmp/transport-browser playwright-core @sparticuz/chromium
// NODE_PATH=/tmp/transport-browser/node_modules node atlas/samples/transport/check-browser.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const {chromium:playwright}=require('playwright-core');
(async()=>{const chromium=(await import(pathToFileURL(require.resolve('@sparticuz/chromium')).href)).default;
const browser=await playwright.launch({executablePath:process.env.CHROMIUM_PATH||await chromium.executablePath(),args:chromium.args,headless:true});const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'transport-'));try{
execFileSync('python3',['-m','zipfile','-e',path.resolve(__dirname,'../../../assets/transport/bench.zip'),tmp]);
const page=await browser.newPage({viewport:{width:1100,height:1000}}),errors=[],requests=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
await page.goto(pathToFileURL(path.join(tmp,'transport.html')).href);assert.equal(await page.evaluate(()=>audit()),true);
assert.equal(JSON.parse(await page.locator('#result').textContent()).primal,47854);
await page.locator('#tamper').click();assert.equal(JSON.parse(await page.locator('#result').textContent()).optimal_proved,false);
await page.reload();await page.locator('#time').fill('50');await page.locator('#time').dispatchEvent('input');
const pixels=await page.locator('canvas').evaluate(c=>Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data).filter((x,i)=>i%4===3&&x>0).length);assert.ok(pixels>10000);
await page.locator('#lines').uncheck();await page.locator('#play').click();await page.waitForFunction(()=>Number(document.getElementById('time').value)>52);await page.locator('#play').click();await page.locator('#reset').click();assert.equal(await page.locator('#time').inputValue(),'0');
await page.setViewportSize({width:390,height:1000});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
await page.locator('#check').focus();await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>audit()),true);assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);console.log('PASS extracted file:// ZIP: certificate, tamper rejection, canvas, slider, animation, reset, keyboard, mobile, zero network/errors');
}finally{await browser.close();fs.rmSync(tmp,{recursive:true,force:true})}})().catch(e=>{console.error(e);process.exitCode=1});
