"""Finite Markdown UI: all states/transitions, portable snippets and no automation."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/switchboard';ART=ROOT/'assets/switchboard';PAGES=ROOT/'atlas/switchboard/states'
spec=importlib.util.spec_from_file_location('switchboard',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class SwitchboardTest(unittest.TestCase):
 def test_exact_cartesian_product(self):
  records=json.loads((ART/'states.json').read_text());self.assertEqual(len(records),12)
  self.assertEqual({r['id'] for r in records},{g.key(s) for s in g.states()})
  self.assertEqual({p.stem for p in PAGES.glob('*.md')},{r['id'] for r in records});self.assertEqual(len(list((ART/'snippets').glob('*.txt'))),12)
 def test_all_48_edges_change_one_parameter(self):
  records={g.key(s):s for s in g.states()};total=0
  for ident,state in records.items():
   nav=g.page(state).split('Состояние:',1)[0];edges=g.transitions(state);self.assertEqual(len(edges),4)
   for e in edges:
    total+=1;target=records[e['target']];self.assertEqual([k for k in state if state[k]!=target[k]],[e['axis']]);self.assertEqual(target[e['axis']],e['value']);self.assertIn(']('+e['target']+'.md)',nav)
  self.assertEqual(total,48)
 def test_graph_connected_from_every_start(self):
  graph={g.key(s):[e['target'] for e in g.transitions(s)] for s in g.states()}
  for start in graph:
   seen={start};todo=[start]
   while todo:
    for target in graph[todo.pop()]:
     if target not in seen:seen.add(target);todo.append(target)
   self.assertEqual(seen,set(graph))
 def test_switch_order_does_not_lose_choices(self):
  for start in g.states():
   for end in g.states():
    for order in itertools.permutations(g.OPTIONS):
     state=dict(start)
     for axis in order:
      if state[axis]!=end[axis]:
       edge=next(e for e in g.transitions(state) if e['axis']==axis and e['value']==end[axis]);state={s_id:g_value for s_id,g_value in zip(g.OPTIONS,edge['target'].split('-'))}
     self.assertEqual(state,end)
 def test_preview_export_match_except_portable_image_path(self):
  for s in g.states():
   page=(PAGES/(g.key(s)+'.md')).read_text();export=(ART/'snippets'/(g.key(s)+'.txt')).read_text();self.assertEqual(export,g.snippet(s))
   self.assertIn('```markdown\n'+export+'```',page);self.assertIn(g.snippet(s,'../../../assets/switchboard/'+g.image_name(s)),page)
   self.assertIn('assets/readme-card.svg',export);self.assertIn('два', (ROOT/'atlas/switchboard.md').read_text())
   self.assertEqual('### С чего начать' in export,s['detail']=='full')
 def test_all_page_links_and_preview_images_exist(self):
  for p in PAGES.glob('*.md'):
   text=p.read_text()
   for link in re.findall(r'\]\(([^)]+)\)',text):
    u=urlsplit(link);self.assertFalse(u.scheme or u.netloc or u.fragment);self.assertTrue((p.parent/u.path).is_file(),(p,link))
   preview=text.split('```markdown',1)[0];src=re.findall('src="([^"]+)"',preview);self.assertEqual(len(src),1);self.assertTrue((p.parent/src[0]).is_file())
 def test_svg_assets_safe_and_no_external_resources(self):
  self.assertEqual(len(list(ART.glob('*.svg'))),6)
  for p in ART.glob('*.svg'):
   root=ET.parse(p).getroot();self.assertEqual(root.attrib['role'],'img');self.assertIsNotNone(root.find('{*}title'));self.assertIsNotNone(root.find('{*}desc'))
   for e in root.iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate','a','style']);self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
 def test_manifest_research_and_honest_labels(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),31)
  for path,digest in m.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),6)
  for r in sources:self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url'])
  b=(SRC/'readme-block.md').read_text();self.assertIn('не скрытый движок',b);self.assertIn('два файла',b);self.assertIn('Actions не запускаются',b);self.assertNotRegex(b,r'<(?:script|iframe|form|input)\b')
 def test_entire_previous_readme_and_workflow_untouched(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch pinned history: '+ref)
  now=(ROOT/'README.md').read_bytes();b=(SRC/'readme-block.md').read_bytes();self.assertEqual(now.count(b),1)
  panel=(ROOT/'atlas/samples/exclusive_panel/readme-block.md').read_bytes();self.assertEqual(now.count(panel),1)
  old=subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT);self.assertEqual(now.replace(panel,b'',1).replace(b,b'',1),old)
  workflow='.github/workflows/native-lab.yml';self.assertEqual((ROOT/workflow).read_bytes(),subprocess.check_output(['git','show',ref+':'+workflow],cwd=ROOT))
 def test_regeneration_is_deterministic_and_read_only_readme(self):
  files=[*PAGES.glob('*.md'),*ART.glob('*.svg'),*(ART/'snippets').glob('*.txt'),ART/'states.json',ART/'manifest.json',SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
