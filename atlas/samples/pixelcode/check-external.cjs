// Optional independent verification, explicit network opt-in. No downloaded code is vendored.
// npm install --prefix /tmp/piet-tools pngjs
// NODE_PATH=/tmp/piet-tools/node_modules node atlas/samples/pixelcode/check-external.cjs --allow-download
// Requires authenticated gh and node. Downloads and executes pinned third-party JS in a temp dir.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');
if(!process.argv.includes('--allow-download'))throw Error('This helper downloads and executes pinned third-party code. Pass --allow-download to opt in.');
const root=path.resolve(__dirname,'../../..');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'sources.json'),'utf8')).find(r=>r.repo==='Bubbler-4/piet');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'piet-independent-'));
try {
  fs.writeFileSync(path.join(temp,'package.json'),'{"type":"module"}');
  for(const name of ['piet.js','piet-run.js']){
    const response=JSON.parse(execFileSync('gh',['api',`repos/${source.repo}/contents/src/${name}?ref=${source.commit}`],{encoding:'utf8'}));
    fs.writeFileSync(path.join(temp,name),Buffer.from(response.content,'base64'));
  }
  const check=`import fs from 'node:fs';
import {createRequire} from 'node:module';
import Piet from './piet.js';import PietRun from './piet-run.js';
const require=createRequire(import.meta.url),{PNG}=require(${JSON.stringify(require.resolve('pngjs'))});
const image=PNG.sync.read(fs.readFileSync(${JSON.stringify(path.join(root,'assets/pixelcode/program.png'))}));
const grid=[];for(let y=0;y<image.height;y++){const row=[];for(let x=0;x<image.width;x++){const i=(y*image.width+x)*4;const color=Array.from(image.data.subarray(i,i+4));const value=Piet.colorvec2color[color];if(value===undefined)throw Error('unknown color');row.push(value)}grid.push(row)}
const run=new PietRun(grid,'');let calls=0;while(!run.finished&&calls<200){run.step();calls++}
if(!run.finished||run.output!=='GIT'||run.stack.length)throw Error('independent result mismatch');
console.log(JSON.stringify({repo:${JSON.stringify(source.repo)},commit:${JSON.stringify(source.commit)},png_decoder:'pngjs',stdout:run.output,finished:run.finished,step_calls:calls,stack:run.stack.map(String)}));`;
  fs.writeFileSync(path.join(temp,'check.mjs'),check);
  process.stdout.write(execFileSync(process.execPath,[path.join(temp,'check.mjs')],{encoding:'utf8',timeout:15000}));
} finally {fs.rmSync(temp,{recursive:true,force:true})}
