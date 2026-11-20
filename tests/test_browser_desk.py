"""AST-backed entry points to native GitHub browsing; no remote UI claims."""
import ast
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'assets/browser-desk';SRC=ROOT/'atlas/samples/browser_desk'
spec=importlib.util.spec_from_file_location('browser_desk',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class BrowserDeskTest(unittest.TestCase):
 def require_history(self,ref):
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch pinned history in shallow clone: '+ref)
 def test_three_real_functions_and_ast_ranges(self):
  records=g.collect();self.assertEqual(len(records),3)
  for r in records:
   p=ROOT/r['path'];data=p.read_bytes();tree=ast.parse(data);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==r['symbol'])
   self.assertEqual((r['start'],r['end']),(fn.lineno,fn.end_lineno));self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
   self.assertTrue(data.decode().splitlines()[r['start']-1].startswith('def '+r['symbol']+'('))
 def test_pinned_content_matches_working_sources(self):
  for r in g.collect():
   self.require_history(r['commit']);data=subprocess.check_output(['git','show',r['commit']+':'+r['path']],cwd=ROOT)
   self.assertEqual(data,(ROOT/r['path']).read_bytes())
 def test_link_context_and_ranges(self):
  for r in g.collect():
   u=urlsplit(r['source']);self.assertEqual(u.netloc,'github.com');self.assertIn('/blob/main/',u.path);self.assertFalse(u.fragment)
   p=urlsplit(r['permalink']);self.assertIn('/blob/'+r['commit']+'/',p.path);self.assertEqual(p.fragment,f'L{r["start"]}-L{r["end"]}')
   self.assertEqual(r['blame'],f'https://github.com/overbaffe1/gitEdit/blame/{r["commit"]}/{r["path"]}')
 def test_direct_calls_are_only_local_syntax(self):
  for r in g.collect():
   tree=ast.parse((ROOT/r['path']).read_text());expected=sorted(n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==r['symbol'])
   self.assertEqual(r['direct_calls_in_same_file'],expected);self.assertTrue(expected)
 def test_csv_json_manifest(self):
  records=json.loads((ART/'tour.json').read_text());self.assertEqual(records,g.collect())
  with (ART/'tour.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),3)
  for row,r in zip(rows,records):self.assertEqual(row['symbol'],r['symbol']);self.assertEqual(int(row['start']),r['start']);self.assertEqual(row['permalink'],r['permalink'])
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(set(m),{'tour.csv','tour.json'})
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
 def test_full_previous_readme_preserved(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit'];self.require_history(ref);old=subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT)
  now=(ROOT/'README.md').read_bytes();b=(SRC/'readme-block.md').read_bytes();self.assertEqual(now.count(b),1);self.assertEqual(now.replace(b,b'',1),old)
  self.assertLess(now.index(b),now.index(b'<!-- github-controls:start -->'))
 def test_primary_sources_and_honest_boundaries(self):
  records=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(records),6)
  for r in records:self.assertEqual(r['repo'],'github/docs');self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url'])
  b=(SRC/'readme-block.md').read_text();self.assertIn('https://github.dev/overbaffe1/gitEdit',b);self.assertIn('Нужен вход',b);self.assertIn('не Codespaces',b);self.assertIn('Commit & Push не нажимай',b);self.assertNotRegex(b,r'<(?:script|iframe|input|form)\b')
  doc=(ROOT/'atlas/browser-desk.md').read_text();self.assertIn('**Не проверялись:**',doc);self.assertIn('local storage',doc)
 def test_deterministic_generation_without_readme_or_source_edits(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md',*(ROOT/p for p,_,_ in g.TARGETS)];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],cwd=ROOT,check=True)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
