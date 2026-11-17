// Optional local recipe: npm install --no-save --package-lock=false d3-hierarchy@3
// Run from a gitEdit checkout: node atlas/samples/repo-fingerprint.mjs [commit]
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { hierarchy, pack } from 'd3-hierarchy';

const revision = execFileSync('git', ['rev-parse', '--verify', '--end-of-options', (process.argv[2] ?? '11ea344') + '^{commit}'], {encoding:'utf8'}).trim();
const entries = execFileSync('git', ['ls-tree', '-rlz', revision], {encoding:'utf8'}).split('\0').filter(Boolean);
const groups = new Map();
for (const entry of entries) {
  const [head, name] = entry.split(/\t(.*)/s);
  const size = Number(head.trim().split(/\s+/).at(-1));
  if (!Number.isFinite(size)) continue; // not a blob (e.g. a submodule)
  const folder = name.includes('/') ? name.split('/')[0] : '/';
  if (!groups.has(folder)) groups.set(folder, []);
  groups.get(folder).push({name, size});
}
const tree = hierarchy({children: [...groups].map(([name,children])=>({name,children}))})
  .sum(d => d.size ?? 0).sort((a,b) => b.value-a.value || String(a.data.name).localeCompare(String(b.data.name),'en'));
pack().size([300,300]).padding(3)(tree);
const colors = ['#f4ac7f','#95d8b3','#bbb5ea','#f0d88f'];
const ink = '#f7f0df', muted = '#bfc9c5';
const esc = v => String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const fmt = n => n.toFixed(2); const kib = n => (n/1024).toFixed(1).replace('.',',');
const label = (x,y,v,size=14,c=ink,bold=false) => `<text x="${x}" y="${y}" fill="${c}" font-size="${size}" font-weight="${bold?700:400}">${esc(v)}</text>`;
const buckets = tree.children;
const packed = buckets.map((group,i) => {
  const c = colors[i%colors.length];
  const outer = `<circle cx="${fmt(group.x)}" cy="${fmt(group.y)}" r="${fmt(group.r)}" fill="#243438" stroke="${c}" stroke-width="1.4"/>`;
  return outer + group.children.map(n=>{
    const file = n.data.name.split('/').pop(); const suffix=file==='README.md'?'MD':file.split('.').pop().toUpperCase();
    const text = n.r>17 && suffix.length<=4 ? `<text x="${fmt(n.x)}" y="${fmt(n.y+4)}" text-anchor="middle" fill="#142729" font-size="${Math.min(14,Math.floor(n.r/1.8))}" font-weight="700">${esc(suffix)}</text>`:'';
    return `<g><title>${esc(n.data.name)} · ${n.value} B</title><circle cx="${fmt(n.x)}" cy="${fmt(n.y)}" r="${fmt(n.r)}" fill="${c}"/>${text}</g>`;
  }).join('\n');
}).join('\n');

function render(compact) {
  const w=compact?344:650, x=compact?20:334, top=compact?391:92;
  const h=top+93+buckets.length*29;
  const spec = `${tree.leaves().length} файлов · ${kib(tree.value)} КиБ`;
  const rows=buckets.map((g,i)=>{
    const y=top+57+i*29;
    return `<circle cx="${x+5}" cy="${y-4}" r="5" fill="${colors[i%colors.length]}"/>`+
      label(x+20,y,g.data.name==='/'?'корень':g.data.name+'/',16)+label(x+169,y,`${kib(g.value)} КиБ`,15,muted);
  }).join('\n');
  const dy=compact?53:Math.round((h-300)/2);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">Отпечаток gitEdit</title><desc id="d">${spec}. Каждый цветной круг — файл, площадь пропорциональна числу байтов. Контуры группируют файлы по каталогу.</desc>
<rect x="1" y="1" width="${w-2}" height="${h-2}" rx="13" fill="#18282c" stroke="#697a73"/>
<g font-family="system-ui, sans-serif">
${label(20,29,'АРХИВ   /   '+revision.slice(0,7),13,muted,true)}
<g transform="translate(${compact?22:14} ${dy})">${packed}</g>
${label(x,top,'Отпечаток',33,ink,true)}${label(x,top+26,spec,16,muted)}
${rows}
<path d="M${x} ${h-45}h${compact?299:278}" stroke="#657872"/>
${label(x,h-21,'1 круг = 1 файл',14,muted)}</g></svg>\n`;
}
for (const slim of [false,true]) writeFileSync(`assets/repo-fingerprint${slim?'-compact':''}.svg`,render(slim));
console.log(revision, tree.leaves().length, 'files,', tree.value, 'bytes');
