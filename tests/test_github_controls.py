"""Native GitHub entry points: structural checks only, no issue submission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import parse_qs,urlsplit
import yaml
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/github_controls';ART=ROOT/'assets/github-controls';FORM=ROOT/'.github/ISSUE_TEMPLATE/native-playground.yml'
spec=importlib.util.spec_from_file_location('github_controls',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class GitHubControlsTest(unittest.TestCase):
 def require_history(self,ref):
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
   self.skipTest(f'Historical object unavailable in shallow clone: {ref}; fetch the pinned commit with --depth=2')
 def setUp(self):self.form=yaml.safe_load(FORM.read_text())
 def test_five_documented_field_types_and_ids(self):
  f=self.form;self.assertTrue(f['name']);self.assertTrue(f['description']);self.assertLessEqual(len(f['description']),200)
  self.assertEqual(set(f),{'name','description','title','body'})
  fields=f['body'];self.assertEqual({x['type'] for x in fields},{'markdown','input','dropdown','textarea','checkboxes'})
  ids=[x['id'] for x in fields if x['type']!='markdown'];self.assertEqual(len(ids),len(set(ids)))
  for x in fields:
   self.assertIsInstance(x['attributes'],dict)
   if x['type']=='markdown':self.assertTrue(x['attributes']['value'])
   else:self.assertRegex(x['id'],r'^[a-z][a-z0-9_-]*$');self.assertTrue(x['attributes']['label'])
 def test_choices_and_required_fields(self):
  fields={x['id']:x for x in self.form['body'] if 'id' in x}
  self.assertEqual({k for k,v in fields.items() if v.get('validations',{}).get('required')},{'callsign','surface'})
  self.assertIs(fields['mechanisms']['attributes']['multiple'],True)
  for name in ['surface','mechanisms']:
   options=fields[name]['attributes']['options'];self.assertGreater(len(options),1);self.assertEqual(len(options),len(set(options)));self.assertTrue(all(isinstance(o,str) for o in options))
  ack=fields['publish_ack']['attributes']['options'];self.assertEqual(len(ack),1);self.assertIs(ack[0]['required'],True)
  self.assertFalse(any(o.get('required',False) for o in fields['switches']['attributes']['options']))
 def test_no_execution_or_implicit_issue_automation(self):
  fields={x['id']:x for x in self.form['body'] if 'id' in x}
  self.assertEqual(fields['specimen']['attributes']['render'],'json')
  json.loads(fields['specimen']['attributes']['value'])
  self.assertNotIn('render',fields['observation']['attributes'])
  s=FORM.read_text();self.assertNotRegex(s,r'<(?:script|iframe|form)\b');self.assertIn('ничего отправлять не нужно',s);self.assertIn('публичную запись',s);self.assertIn('до отправки',s)
  self.assertFalse(set(self.form)&{'assignees','labels','projects'})
 def test_links_are_form_opening_and_canonical_prefill(self):
  form,prefilled,diff=g.links()
  for url in [form,prefilled]:
   u=urlsplit(url);self.assertEqual(u.netloc,'github.com');self.assertEqual(u.path,'/overbaffe1/gitEdit/issues/new');q=parse_qs(u.query);self.assertEqual(q['template'],['native-playground.yml']);self.assertFalse(set(q)-{'template','callsign'})
  self.assertEqual(parse_qs(urlsplit(prefilled).query)['callsign'],['Лунный архивариус'])
  self.assertTrue(any(x.get('id')=='callsign' for x in self.form['body']))
  self.assertRegex(diff,r'/commit/[a-f0-9]{40}$')
 def test_real_short_document_history(self):
  sha=json.loads((SRC/'config.json').read_text())['rich_diff_commit'];self.assertRegex(sha,r'^[a-f0-9]{40}$')
  self.require_history(sha+'^')
  def get(ref):return subprocess.check_output(['git','show',ref+':assets/github-controls/revision.md'],cwd=ROOT)
  old,new=get(sha+'^'),get(sha);self.assertNotEqual(old,new);self.assertEqual(new,(ART/'revision.md').read_bytes())
  for s in ['статичная картинка','| Формат | PNG |']:self.assertIn(s,old.decode())
  for s in ['нативная интерактивная карта','| Формат | GeoJSON |','3. Изменить масштаб.']:self.assertIn(s,new.decode())
  changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',sha],cwd=ROOT,text=True).splitlines();self.assertEqual(changed,['assets/github-controls/revision.md'])
 def test_original_readme_and_old_form_untouched(self):
  base=json.loads((SRC/'config.json').read_text())['base_commit'];b=(SRC/'readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(b),1)
  self.require_history(base)
  old=subprocess.check_output(['git','show',base+':README.md'],cwd=ROOT)
  legacy=now
  for name in ('browser_desk','actions_lab','switchboard','exclusive_panel','fragment_quest','dual_solid','resize_scan'):
   addition=(ROOT/f'atlas/samples/{name}/readme-block.md').read_bytes()
   self.assertEqual(legacy.count(addition),1);legacy=legacy.replace(addition,b'',1)
  self.assertEqual(legacy.replace(b,b'',1),old)
  for path in ['.github/ISSUE_TEMPLATE/config.yml','.github/ISSUE_TEMPLATE/readme-block.yml']:
   self.assertEqual((ROOT/path).read_bytes(),subprocess.check_output(['git','show',base+':'+path],cwd=ROOT))
 def test_entry_points_and_boundaries_in_readme(self):
  b=(SRC/'readme-block.md').read_text();self.assertLess((ROOT/'README.md').read_text().index(b),(ROOT/'README.md').read_text().index('<!-- native-lab:start -->'))
  for url in g.links():self.assertIn(url,b)
  self.assertIn('не отправка',b);self.assertIn('публичную запись',b);self.assertNotRegex(b,r'<(?:iframe|script|input|form)\b')
  doc=(ROOT/'atlas/github-controls.md').read_text();self.assertIn('не проверялись',doc);self.assertIn('не валидация JSON',doc)
 def test_manifest_and_primary_research(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),3)
  for path,digest in m.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),4)
  for s in sources:self.assertEqual(s['repo'],'github/docs');self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
 def test_mechanics_are_native_pages_not_fake_inline_widgets(self):
  data=json.loads((ART/'mechanics.json').read_text());self.assertEqual({x['id'] for x in data},{'issue-form','prefill','rich-diff'})
  self.assertEqual([x['entry'] for x in data],list(g.links()))
  for x in data:self.assertIs(x['mutates_on_open'],False);self.assertTrue(x['context'])
 def test_regeneration_changes_neither_form_nor_readme(self):
  files=[*ART.iterdir(),FORM,ROOT/'README.md',SRC/'readme-block.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
