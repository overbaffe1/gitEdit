"""Native one-document hypertext quest. Runtime checks are opt-in JS fixture."""
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/fragment_quest';ART=ROOT/'assets/fragment-quest';PLAY=ROOT/'atlas/fragment-quest/README.md'
spec=importlib.util.spec_from_file_location('fragment_quest',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.details=[];self.ids=[];self.depth=0;self.target_depths=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='details':self.details.append(a);self.depth+=1
  if 'id' in a:self.ids.append(a['id']);self.target_depths.append(self.depth)
 def handle_endtag(self,t):
  if t=='details':self.depth-=1
class FragmentQuestTest(unittest.TestCase):
 def setUp(self):self.graph=json.loads((ART/'graph.json').read_text());self.text=PLAY.read_text()
 def test_seven_scenes_fourteen_nonself_choices(self):
  self.assertEqual(len(self.graph),7);self.assertEqual(len({r['id'] for r in self.graph}),7)
  edges=[(r['id'],e['target']) for r in self.graph for e in r['transitions']];self.assertEqual(len(edges),14);self.assertEqual(len(set(edges)),14)
  ids={r['id'] for r in self.graph}
  for a,b in edges:self.assertIn(b,ids);self.assertNotEqual(a,b)
 def test_all_scenes_reachable_and_can_return_to_start(self):
  graph={r['id']:[e['target'] for e in r['transitions']] for r in self.graph}
  for start in graph:
   seen={start};todo=[start]
   while todo:
    for target in graph[todo.pop()]:
     if target not in seen:seen.add(target);todo.append(target)
   self.assertEqual(seen,set(graph))
 def test_target_inside_closed_section_not_on_summary(self):
  p=Parser();p.feed(self.text);self.assertEqual(p.depth,0);self.assertEqual(len(p.details),7);self.assertEqual(p.target_depths,[1]*7)
  self.assertEqual([r['name'] for r in p.details],[g.GROUP]*7);self.assertEqual(['open' in r for r in p.details],[True]+[False]*6)
  self.assertEqual(set(p.ids),{g.PREFIX+s[0] for s in g.SCENES});self.assertEqual(len(p.ids),len(set(p.ids)))
 def test_every_fragment_targets_the_intended_sanitized_id(self):
  links=re.findall(r'\]\(#([^\s)]+)\)',self.text);self.assertEqual(len(links),14)
  ids={r['target_id'] for r in self.graph};self.assertTrue(set(links)<=ids)
  for r in self.graph:
   self.assertEqual(r['target_id'],'user-content-'+g.PREFIX+r['id'])
   for edge in r['transitions']:
    target=next(x for x in self.graph if x['id']==edge['target']);self.assertIn('['+edge['label']+'](#'+target['target_id']+') → '+target['title'],self.text)
 def test_local_file_links_and_root_entry_exist(self):
  for href in re.findall(r'\]\(([^)]+)\)',self.text):
   if not href.startswith('#'):self.assertTrue((PLAY.parent/href).is_file(),href)
  block=g.block();self.assertIn('atlas/fragment-quest/README.md',block)
  for href in re.findall(r'\]\(([^)]+)\)',block):self.assertTrue((ROOT/href).is_file(),href)
 def test_no_javascript_backend_forms_or_external_media(self):
  self.assertNotRegex(self.text,r'<(?:script|iframe|video|audio|canvas|input|form|img|picture)\b');self.assertNotRegex(self.text,r'\bon\w+\s*=|\bstyle\s*=');self.assertNotIn('https://',self.text);self.assertNotIn('issues/new',self.text)
  self.assertIn('вручную',self.text);self.assertIn('не production',self.text);self.assertIn('не проверяет память',self.text)
 def test_sources_hashes_and_copy_match(self):
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),8)
  for s in sources:self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
  manifest=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(manifest),4)
  for name,digest in manifest.items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
  self.assertEqual(self.text,(ART/'play.txt').read_text());self.assertEqual(self.text,g.play());self.assertEqual((SRC/'readme-block.md').read_text(),g.block())
 def test_entire_old_readme_and_workflows_unchanged(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch base history '+ref)
  block=(SRC/'readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(block),1)
  self.assertEqual(now.replace(block,b'',1),subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT));self.assertEqual(subprocess.check_output(['git','diff',ref,'--','.github/workflows'],cwd=ROOT),b'')
 def test_generator_deterministic_readme_not_edited(self):
  files=[PLAY,ART/'graph.json',ART/'play.txt',ART/'manifest.json',SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT);self.assertEqual(before,{p:p.read_bytes() for p in files})
 def test_integration_checks_repository_context_and_real_clicks(self):
  script=(SRC/'check-browser.cjs').read_text();self.assertIn("'overbaffe1/gitEdit'",script);self.assertIn('.click()',script);self.assertIn("keyboard.press('Enter')",script);self.assertIn('documents,1',script);self.assertIn('videoProbe',script)
  doc=(ROOT/'atlas/fragment-quest.md').read_text();self.assertIn('ложноположительный',doc);self.assertIn('не универсален',doc);self.assertIn('не запускает production',doc)
