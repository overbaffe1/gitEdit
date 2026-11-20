// Opt-in integration check: real GitHub API HTML, local browser, no GitHub mutations.
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'../../..');
const localRequire=require('node:module').createRequire(path.join(root,'.local/anchor-probe/package.json'));
const {chromium:pw}=localRequire('playwright-core');
const {default:cr,inflate,setupLambdaEnvironment}=localRequire('@sparticuz/chromium');
function api(text,context){const request={text,mode:'gfm'};if(context)request.context=context;return execFileSync('gh',['api','markdown','--input','-'],{input:JSON.stringify(request),encoding:'utf8',cwd:root});}
(async()=>{
 const html=api(fs.readFileSync(path.join(root,'atlas/fragment-quest/README.md'),'utf8'),'overbaffe1/gitEdit');
 const graph=JSON.parse(fs.readFileSync(path.join(root,'assets/fragment-quest/graph.json'),'utf8'));
 if(process.env.FRAGMENT_QUEST_BUNDLED_LIBS==='1'){
  await inflate(path.join(root,'.local/anchor-probe/node_modules/@sparticuz/chromium/bin/al2023.tar.br'));
  setupLambdaEnvironment(path.join(require('node:os').tmpdir(),'al2023/lib'));
 }
 const browser=await pw.launch({executablePath:await cr.executablePath(),headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-zygote']});
 const results=[];
 try{
  for(const width of [1280,390]){
   const context=await browser.newContext({viewport:{width,height:900}});const page=await context.newPage();
   let documents=0;const external=[];const base='http://fixture.test/play';
   await page.route('**/*',route=>{
    const url=new URL(route.request().url());
    if(url.hostname!=='fixture.test'){external.push(url.hostname);return route.abort();}
    documents++;return route.fulfill({contentType:'text/html; charset=utf-8',body:'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'});
   });
   await page.goto(base);const group=page.locator('details[name="user-content-gitedit-fragment-quest-v1"]');assert.equal(await group.count(),7);
   const opens=()=>group.evaluateAll(ns=>ns.map(n=>n.open));
   async function selected(id){const idx=graph.findIndex(s=>s.id===id);await page.waitForFunction(({idx})=>Array.from(document.querySelectorAll('details[name="user-content-gitedit-fragment-quest-v1"]')).every((n,i)=>n.open===(i===idx)),{idx},{timeout:5000});assert.equal(await page.locator('#user-content-fq-scene-'+id).isVisible(),true);}
   assert.deepEqual(await opens(),[true,false,false,false,false,false,false]);
   let edges=0;
   for(const state of graph){
    for(const edge of state.transitions){
     await page.goto(base+'#'+state.target_id);await selected(state.id);
     const source=group.nth(graph.indexOf(state));
     const target=graph.find(s=>s.id===edge.target);
     await source.locator('a[href="#'+target.target_id+'"]').click();
     await selected(edge.target);assert.equal(new URL(page.url()).hash,'#'+target.target_id);edges++;
    }
   }
   assert.equal(documents,1,'All choices stay in the original document');assert.deepEqual(external,[]);
   await page.goto(base+'#user-content-fq-scene-dock');await selected('dock');
   const link=group.nth(0).locator('a[href="#user-content-fq-scene-radio"]');await link.focus();await page.keyboard.press('Enter');await selected('radio');
   // A direct URL into a closed scene must reveal it after a fresh document load.
   await page.goto(base+'?fresh=1#user-content-fq-scene-rescue');await selected('rescue');
   // Close everything manually; summary is a usable fallback when a fragment does not re-trigger.
   await group.nth(6).locator('summary').click();assert.ok((await opens()).every(x=>!x));
   await group.nth(0).locator('summary').focus();await page.keyboard.press('Space');await selected('dock');
   results.push({width,edges,oneDocumentForChoices:true,keyboardLink:true,directDeepLink:true,manualFallback:true});await context.close();
  }
  const video='<video controls src="x.mp4"></video>';
  const noContext=api(video),repoContext=api(video,'overbaffe1/gitEdit');
  assert.equal(repoContext.includes('<video'),false,'Do not claim raw video works in repository context');
  console.log(JSON.stringify({browser:browser.version(),method:'GitHub Markdown API HTML rendered locally, not production github.com UI',results,videoProbe:{withoutContextKeepsVideo:noContext.includes('<video'),repositoryContextKeepsVideo:repoContext.includes('<video')}},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
