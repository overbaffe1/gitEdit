"""Local structural checks. Browser behavior is opt-in check-browser.cjs."""
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/exclusive_panel';ART=ROOT/'assets/exclusive-panel'
spec=importlib.util.spec_from_file_location('exclusive_panel',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def live(text):return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M|re.S)
class Structure(HTMLParser):
 def __init__(self):super().__init__();self.panels=[];self.summaries=0;self.stack=[]
 def handle_starttag(self,tag,attrs):
  if tag=='details':self.panels.append(dict(attrs));self.stack.append(tag)
  if tag=='summary':self.summaries+=1
 def handle_endtag(self,tag):
  if tag=='details':
   if not self.stack:raise AssertionError('Unbalanced details')
   self.stack.pop()
class ExclusivePanelTest(unittest.TestCase):
 def test_exactly_three_grouped_panels_one_initially_open(self):
  p=Structure();p.feed(live(g.block()));self.assertEqual(len(p.panels),3);self.assertEqual(p.summaries,3);self.assertEqual(p.stack,[])
  self.assertEqual([x['name'] for x in p.panels],[g.GROUP]*3);self.assertEqual(['open' in x for x in p.panels],[True,False,False])
 def test_name_is_unique_to_this_live_readme_group(self):
  text=live((ROOT/'README.md').read_text());names=re.findall(r'<details[^>]*\bname="([^"]+)"',text);self.assertEqual(names,[g.GROUP]*3)
  self.assertEqual(text.count(g.START),1);self.assertEqual(text.count(g.END),1)
 def test_static_default_motion_is_opt_in_and_reduced_motion_exists(self):
  panels=live(g.block()).split('<details ')[1:];self.assertEqual(len(panels),3)
  self.assertIn('poster.png',panels[0]);self.assertNotIn('cube.gif',panels[0]);self.assertIn('prefers-reduced-motion: reduce',panels[1]);self.assertIn('cube.gif',panels[1]);self.assertIn('poster.png',panels[1]);self.assertNotIn(' open>',panels[1])
  self.assertIn('alt="',panels[0]);self.assertIn('alt="',panels[1])
 def test_all_local_links_and_media_exist(self):
  text=g.block()
  for value in re.findall(r'(?:src="|srcset="|\]\()([^"\s)]+)',text):
   self.assertNotIn('://',value);self.assertNotIn('#',value);self.assertTrue((ROOT/value).is_file(),value)
 def test_no_scripts_form_events_styles_or_external_services(self):
  text=live(g.block());self.assertNotRegex(text,r'<(?:script|iframe|video|input|form|style|canvas)\b');self.assertNotRegex(text,r'\bon\w+\s*=|\bstyle\s*=|\brole="tab');self.assertNotIn('https://',text)
  self.assertIn('Enter / Пробел',text);self.assertIn('закрыть и последнюю',g.panel());self.assertIn('старом браузере',text)
 def test_sources_pinned_and_manifest_matches(self):
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),6)
  for s in sources:self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
  manifest=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(manifest),4)
  for file,digest in manifest.items():self.assertEqual(hashlib.sha256((ROOT/file).read_bytes()).hexdigest(),digest)
 def test_portable_panel_is_same_as_displayed_panel(self):
  self.assertEqual((ART/'panel.txt').read_text(),g.panel());self.assertIn(g.panel(),(SRC/'readme-block.md').read_text());self.assertEqual((SRC/'readme-block.md').read_text(),g.block())
  self.assertIn('<details name="my-project-demo" open>',g.panel());self.assertNotIn('user-content-',g.panel())
 def test_full_previous_readme_and_workflows_preserved(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch base history '+ref)
  block=(SRC/'readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(block),1)
  quest=(ROOT/'atlas/samples/fragment_quest/readme-block.md').read_bytes();self.assertEqual(now.count(quest),1)
  self.assertEqual(now.replace(quest,b'',1).replace(block,b'',1),subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT))
  self.assertEqual(subprocess.check_output(['git','diff',ref,'--','.github/workflows'],cwd=ROOT),b'')
 def test_regeneration_does_not_edit_readme_or_existing_media(self):
  files=[SRC/'readme-block.md',ART/'manifest.json',ART/'panel.txt',ROOT/'README.md',ROOT/'assets/motion-formats/cube.gif',ROOT/'assets/motion-formats/poster.png'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT);self.assertEqual(before,{p:p.read_bytes() for p in files})
 def test_docs_boundaries_and_integration_script_present(self):
  doc=(ROOT/'atlas/exclusive-panel.md').read_text();self.assertIn('не radio-tabs',g.panel());self.assertIn('открыт локально',doc);self.assertIn('не физический iPhone',doc)
  script=(SRC/'check-browser.cjs').read_text();self.assertIn("['api', 'markdown', '--input', '-']",script);self.assertIn('keyboard.press',script);self.assertIn('independent-control',script);self.assertIn('img.currentSrc',script)
