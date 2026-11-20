// Read-only opt-in check: GitHub Markdown API HTML, local Chromium, no site deployment.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');const root=path.resolve(__dirname,'../../..');
const localRequire=require('node:module').createRequire(path.join(root,'.local/resize-scan/package.json'));
const {chromium:pw}=localRequire('playwright-core');const {default:cr,inflate,setupLambdaEnvironment}=localRequire('@sparticuz/chromium');
(async()=>{
 const text=fs.readFileSync(path.join(__dirname,'readme-block.md'),'utf8');
 const html=execFileSync('gh',['api','markdown','--input','-'],{input:JSON.stringify({text,mode:'gfm',context:'overbaffe1/gitEdit'}),encoding:'utf8',cwd:root});
 if(process.env.RESIZE_SCAN_BUNDLED_LIBS==='1'){
  await inflate(path.join(root,'.local/resize-scan/node_modules/@sparticuz/chromium/bin/al2023.tar.br'));
  setupLambdaEnvironment(path.join(require('node:os').tmpdir(),'al2023/lib'));
 }
 const browser=await pw.launch({executablePath:await cr.executablePath(),headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-zygote']});const results=[];
 try{
  for(const deviceScaleFactor of [1,2]){
   const context=await browser.newContext({viewport:{width:390,height:900},deviceScaleFactor});const page=await context.newPage();let documents=0;const unexpected=[];
   await page.route('**/*',route=>{
    const u=new URL(route.request().url());if(u.hostname!=='fixture.test'){unexpected.push(u.hostname);return route.abort();}
    if(u.pathname==='/README'){documents++;return route.fulfill({contentType:'text/html; charset=utf-8',body:'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'});}
    const file=path.resolve(root,'.'+u.pathname);if(!file.startsWith(root+path.sep)||!fs.existsSync(file))return route.fulfill({status:404,body:''});
    return route.fulfill({contentType:'image/svg+xml',body:fs.readFileSync(file)});
   });
   await page.goto('http://fixture.test/README');const picture=page.locator('picture');assert.equal(await picture.count(),1);assert.equal(await picture.locator('source').count(),12);assert.equal(await page.locator('script,input,iframe').count(),0);
   const widths=[390,...Array.from({length:12},(_,i)=>599+80*i).flatMap(w=>[w,w+1]),1600];
   const seen=new Set();
   for(const width of [...widths,...widths.toReversed()]){
    await page.setViewportSize({width,height:900});const expected=Math.min(12,Math.max(0,Math.floor((width-520)/80)));const file='slice-'+String(expected).padStart(2,'0')+'.svg';
    await page.waitForFunction(file=>document.querySelector('picture img').currentSrc.endsWith('/'+file),file,{timeout:5000});
    await picture.locator('img').evaluate(img=>img.decode());seen.add(file);
   }
   assert.equal(seen.size,13);assert.equal(documents,1);assert.deepEqual(unexpected,[]);assert.equal(page.url(),'http://fixture.test/README');
   results.push({deviceScaleFactor,resizeChecks:widths.length*2,frames:seen.size,documentLoads:documents,currentSrcAndDecode:'pass'});await context.close();
  }
  console.log(JSON.stringify({browser:browser.version(),method:'GitHub Markdown API with repository context, rendered locally; production github.com CSS/JS not tested',results},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
