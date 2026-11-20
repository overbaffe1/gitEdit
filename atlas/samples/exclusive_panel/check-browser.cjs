// Explicit integration check: GitHub Markdown API output + local Chromium.
// npm install --prefix .local/readme-browser --no-audit --no-fund playwright-core @sparticuz/chromium
// node atlas/samples/exclusive_panel/check-browser.cjs
// No issue/PR mutation, dispatch, upload, application JS or remote asset fetch.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../../..');
const modules = path.join(root, '.local/readme-browser/node_modules');
const {chromium: playwright} = require(path.join(modules, 'playwright-core'));
const localRequire = require('node:module').createRequire(path.join(root, '.local/readme-browser/package.json'));
const chromium = localRequire('@sparticuz/chromium').default;
const source = fs.readFileSync(path.join(__dirname, 'readme-block.md'), 'utf8');
const rendered = execFileSync('gh', ['api', 'markdown', '--input', '-'], {
  cwd: root, input: JSON.stringify({text: source, mode: 'gfm', context: 'overbaffe1/gitEdit'}), encoding: 'utf8',
});
(async () => {
 if (process.env.EXCLUSIVE_PANEL_BUNDLED_LIBS === '1') {
  // Optional local Linux fixture support, not an AWS service or cloud launch.
  const {inflate, setupLambdaEnvironment} = localRequire('@sparticuz/chromium');
  await inflate(path.join(modules, '@sparticuz/chromium/bin/al2023.tar.br'));
  setupLambdaEnvironment(path.join(require('node:os').tmpdir(), 'al2023/lib'));
 }
 const browser = await playwright.launch({executablePath: await chromium.executablePath(), args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--no-zygote'], headless: true});
 const results = [];
 try {
  for (const [width, reducedMotion] of [[1280, 'no-preference'], [390, 'reduce']]) {
   const context = await browser.newContext({viewport: {width, height: 900}, reducedMotion});
   const page = await context.newPage();
   const unexpected = [];
   await page.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.hostname !== 'fixture.test') {unexpected.push(url.hostname); return route.abort();}
    if (url.pathname === '/README') return route.fulfill({contentType: 'text/html', body: '<!doctype html><html lang="ru"><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + rendered + '<details name="independent-control" open><summary>Независимая группа</summary>Контроль</details></body></html>'});
    const file = path.resolve(root, '.' + url.pathname);
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return route.fulfill({status: 404, body: ''});
    return route.fulfill({body: fs.readFileSync(file), contentType: file.endsWith('.png') ? 'image/png' : 'image/gif'});
   });
   await page.goto('http://fixture.test/README');
   const group = page.locator('details[name="user-content-gitedit-motion-desk-v1"]');
   assert.equal(await group.count(), 3, 'GitHub must preserve one shared prefixed name on all live panels');
   const state = () => group.evaluateAll(nodes => nodes.map(n => n.open));
   assert.deepEqual(await state(), [true, false, false]);
   const original = page.url();
   await group.nth(1).locator('summary').click();
   assert.deepEqual(await state(), [false, true, false]);
   assert.equal(await group.nth(0).locator('img').isVisible(), false);
   const image = group.nth(1).locator('img');
   await image.evaluate(img => img.decode());
   const selected = await image.evaluate(img => img.currentSrc);
   assert.ok(selected.endsWith(reducedMotion === 'reduce' ? '/poster.png' : '/cube.gif'), selected);
   await group.nth(2).locator('summary').click();
   assert.deepEqual(await state(), [false, false, true]);
   assert.equal(await image.isVisible(), false);
   assert.equal(await group.nth(2).locator('pre').isVisible(), true);
   await group.nth(2).locator('summary').click();
   assert.deepEqual(await state(), [false, false, false], 'All panels may close');
   await group.nth(0).locator('summary').focus();
   await page.keyboard.press('Enter');
   assert.deepEqual(await state(), [true, false, false]);
   // GitHub may wrap the first image in a focusable link, so Tab can visit it first.
   for (let steps = 0; steps < 12; steps++) {
    await page.keyboard.press('Tab');
    if (await group.nth(1).locator('summary').evaluate(el => el === document.activeElement)) break;
   }
   assert.equal(await group.nth(1).locator('summary').evaluate(el => el === document.activeElement), true);
   await page.keyboard.press('Space');
   assert.deepEqual(await state(), [false, true, false]);
   assert.equal(await page.locator('details[name="independent-control"]').evaluate(el => el.open), true);
   assert.equal(page.url(), original, 'No page navigation');
   assert.deepEqual(unexpected, [], 'No external service needed for panel interaction');
   results.push({width, reducedMotion, initial: [true, false, false], pointer: 'pass', keyboardEnterTabSpace: 'pass', allMayClose: 'pass', independentGroup: 'pass', noNavigation: 'pass', selectedImage: path.basename(selected)});
   await context.close();
  }
  const report = {browser: browser.version(), method: 'GitHub Markdown API HTML rendered locally; not an authenticated github.com UI test', results};
  console.log(JSON.stringify(report, null, 2));
 } finally {await browser.close();}
})().catch(error => {console.error(error); process.exitCode = 1;});
