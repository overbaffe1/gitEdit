// Research probes, NOT a README feature or Ctrl+F/visual-overlay conformance test.
// npm install --prefix .local/find-probe --no-audit --no-fund playwright-core@1.65.1 @sparticuz/chromium@153.0.0
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');const root=path.resolve(__dirname,'../../..');
const localRequire=require('node:module').createRequire(path.join(root,'.local/find-probe/package.json'));
const {chromium:pw}=localRequire('playwright-core');const {default:cr,inflate,setupLambdaEnvironment}=localRequire('@sparticuz/chromium');
(async()=>{
 const text='<p>VisibleProbe512</p>\n<details name="native-find-probe"><summary>First</summary><p>4317 hidden panel</p></details>\n<details name="native-find-probe"><summary>Second</summary><p>8264 another panel</p></details>\n<p><img src="assets/veil/sheet-a.png" width="256" alt="A"> <img src="assets/veil/sheet-b.png" width="256" alt="B"></p>';
 const html=execFileSync('gh',['api','markdown','--input','-'],{cwd:root,encoding:'utf8',input:JSON.stringify({text,mode:'gfm',context:'overbaffe1/gitEdit'})});
 if(process.env.NATIVE_PROBES_BUNDLED_LIBS==='1'){
  await inflate(path.join(root,'.local/find-probe/node_modules/@sparticuz/chromium/bin/al2023.tar.br'));
  setupLambdaEnvironment(path.join(require('node:os').tmpdir(),'al2023/lib'));
 }
 const browser=await pw.launch({executablePath:await cr.executablePath(),headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-zygote']});
 try{
  const page=await browser.newPage({viewport:{width:900,height:600}});let documents=0;
  await page.route('**/*',route=>{
   const u=new URL(route.request().url());if(u.hostname!=='fixture.test')return route.abort();
   if(u.pathname==='/readme'){documents++;return route.fulfill({contentType:'text/html; charset=utf-8',body:'<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>'});}
   if(!['/assets/veil/sheet-a.png','/assets/veil/sheet-b.png'].includes(u.pathname))return route.fulfill({status:404,body:''});
   return route.fulfill({contentType:'image/png',body:fs.readFileSync(path.join(root,u.pathname))});
  });
  await page.goto('http://fixture.test/readme');assert.equal(await page.locator('details').count(),2);assert.equal(await page.locator('img').count(),2);
  assert.ok((await page.locator('body').innerText()).includes('VisibleProbe512'),'The visible control must be present in rendered text');
  await page.bringToFront();
  const visibleSearch=await page.evaluate(()=>window.find('VisibleProbe512'));
  // A false visible control makes any conclusion about hidden search inconclusive.
  await page.evaluate(()=>window.getSelection().removeAllRanges());
  const hiddenSearch=await page.evaluate(()=>window.find('4317'));const afterSearch=await page.locator('details').evaluateAll(ns=>ns.map(n=>n.open));
  // Do not freeze hiddenSearch=false as a universal browser rule; report observations.
  await page.evaluate(()=>{
   window.getSelection().removeAllRanges();window.nativeProbeDrags=[];
   document.addEventListener('dragstart',e=>window.nativeProbeDrags.push({tag:e.target.tagName,types:[...e.dataTransfer.types]}));
  });
  for(const image of await page.locator('img').all())await image.evaluate(img=>img.decode());
  const a=await page.locator('img').nth(0).boundingBox(),b=await page.locator('img').nth(1).boundingBox();
  await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:20});
  const drags=await page.evaluate(()=>window.nativeProbeDrags);assert.ok(drags.some(e=>e.tag==='IMG'),'A native image drag must actually start');
  if(process.env.NATIVE_PROBES_SCREENSHOT==='1')await page.screenshot({path:path.join(root,'.local/find-probe/drag-page.png')});
  await page.keyboard.press('Escape');await page.mouse.up();assert.equal(page.url(),'http://fixture.test/readme');assert.equal(documents,1);
  console.log(JSON.stringify({browser:browser.version(),method:'GitHub Markdown API with repository context, local headless Chromium only',search:{visibleBaseline:visibleSearch,hiddenResult:hiddenSearch,detailsOpen:afterSearch,ctrlFUiTested:false,interpretation:visibleSearch?'Observed window.find result only; not a Ctrl+F UI verdict':'INCONCLUSIVE: visible window.find baseline did not match'},drag:{events:drags,cancelledWithoutDrop:true,visualOverlay:'NOT VERIFIED: dragstart and page pixels do not prove OS/browser drag-feedback compositing'},readmeFeatureAdded:false},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
