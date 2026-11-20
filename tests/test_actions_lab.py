"""Manual Actions lab: local payload + structural workflow checks, no dispatch."""
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import yaml
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/actions_lab';ART=ROOT/'assets/actions-lab';WF=ROOT/'.github/workflows/native-lab.yml'
spec=importlib.util.spec_from_file_location('actions_payload',SRC/'run.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class ActionsLabTest(unittest.TestCase):
 def test_dispatch_only_and_typed_inputs(self):
  d=yaml.safe_load(WF.read_text());self.assertEqual(set(d['on']),{'workflow_dispatch'})
  inputs=d['on']['workflow_dispatch']['inputs'];self.assertEqual(set(inputs),{'motif','count','palette','include_csv'})
  self.assertEqual([inputs[k]['type'] for k in inputs],['choice','number','choice','boolean'])
  defaults=g.parse_inputs({});self.assertEqual(defaults,{'motif':'orbit','count':24,'palette':'night','include_csv':True})
  self.assertEqual(inputs['count']['default'],defaults['count']);self.assertEqual(inputs['motif']['options'],['orbit','spiral'])
 def test_read_only_permissions_pins_and_env_boundaries(self):
  d=yaml.safe_load(WF.read_text());self.assertEqual(d['permissions'],{'contents':'read'});self.assertEqual(len(d['jobs']),1)
  job=d['jobs']['experiment'];self.assertEqual(job['timeout-minutes'],5);self.assertEqual(job['runs-on'],'ubuntu-24.04');steps=job['steps']
  self.assertIs(steps[0]['with']['persist-credentials'],False)
  self.assertEqual(steps[0]['uses'],'actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683')
  self.assertEqual(steps[2]['uses'],'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02');self.assertEqual(steps[2]['with']['retention-days'],3);self.assertEqual(steps[2]['with']['if-no-files-found'],'error')
  for step in steps:self.assertNotIn('${{ inputs.',step.get('run',''));self.assertNotIn('secrets',str(step))
  self.assertEqual(steps[1]['run'],'python3 atlas/samples/actions_lab/run.py')
  self.assertEqual(steps[3]['env']['ARTIFACT_URL'],'${{ steps.artifact.outputs.artifact-url }}')
 def test_invalid_inputs_rejected_before_writes(self):
  cases=[('LAB_COUNT',s) for s in ['0','11','97','24.0','1e2','-24','24; echo hi','${{ secrets.X }}']]+[('LAB_MOTIF','$(id)'),('LAB_PALETTE','../night'),('LAB_INCLUDE_CSV','yes')]
  with tempfile.TemporaryDirectory() as tmp:
   for key,value in cases:
    out=Path(tmp)/'not-created'
    with self.assertRaises(ValueError):g.execute({key:value,'LAB_OUTPUT':str(out)})
    self.assertFalse(out.exists())
 def test_variant_outputs_are_deterministic_and_consistent(self):
  for motif in ['orbit','spiral']:
   for count in [12,24,96]:
    for palette in ['night','paper']:
     for flag in ['true','false']:
      params=g.parse_inputs({'LAB_MOTIF':motif,'LAB_COUNT':str(count),'LAB_PALETTE':palette,'LAB_INCLUDE_CSV':flag});files=g.build(params);self.assertEqual(files,g.build(params))
      root=ET.fromstring(files['drawing.svg']);self.assertEqual(len(root.findall('{*}circle')),count);self.assertEqual(root.attrib['role'],'img')
      self.assertEqual('coordinates.csv' in files,flag=='true')
      result=json.loads(files['result.json']);self.assertEqual(result['points'],count);self.assertEqual(result['parameters'],params)
      for name,digest in result['sha256'].items():self.assertEqual(hashlib.sha256(files[name]).hexdigest(),digest)
      for e in root.iter():self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate']);self.assertFalse(any(k.endswith('href') for k in e.attrib))
 def test_csv_coordinates_match_svg_and_bounds(self):
  files=g.build(g.parse_inputs({}));rows=list(csv.DictReader(io.StringIO(files['coordinates.csv'].decode())));points=ET.fromstring(files['drawing.svg']).findall('{*}circle');self.assertEqual(len(rows),len(points))
  for row,point in zip(rows,points):self.assertEqual(row['x'],point.attrib['cx']);self.assertEqual(row['y'],point.attrib['cy']);self.assertTrue(0<float(row['x'])<640 and 0<float(row['y'])<520)
 def test_summary_append_and_no_stale_file_mix(self):
  with tempfile.TemporaryDirectory() as tmp:
   output=Path(tmp)/'result';summary=Path(tmp)/'summary';summary.write_text('previous step\n')
   g.execute({'LAB_OUTPUT':str(output),'GITHUB_STEP_SUMMARY':str(summary),'LAB_INCLUDE_CSV':'false'})
   self.assertTrue(summary.read_text().startswith('previous step\n# Native lab:'))
   self.assertFalse((output/'coordinates.csv').exists());self.assertEqual(len(list(output.iterdir())),3)
   before={p.name:p.read_bytes() for p in output.iterdir()}
   with self.assertRaises(ValueError):g.execute({'LAB_OUTPUT':str(output)})
   self.assertEqual(before,{p.name:p.read_bytes() for p in output.iterdir()})
 def test_local_example_manifest_and_sources(self):
  self.assertEqual({p.name:p.read_bytes() for p in (ART/'example').iterdir()},g.build(g.parse_inputs({})))
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),6)
  for path,digest in m.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
  records=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(records),5)
  for r in records:self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url'])
 def test_entire_previous_readme_preserved(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch pinned commit in shallow clone: '+ref)
  old=subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT);b=(SRC/'readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(b),1)
  later=(ROOT/'atlas/samples/switchboard/readme-block.md').read_bytes();self.assertEqual(now.count(later),1)
  panel=(ROOT/'atlas/samples/exclusive_panel/readme-block.md').read_bytes();self.assertEqual(now.count(panel),1)
  quest=(ROOT/'atlas/samples/fragment_quest/readme-block.md').read_bytes();self.assertEqual(now.count(quest),1)
  self.assertEqual(now.replace(quest,b'',1).replace(panel,b'',1).replace(later,b'',1).replace(b,b'',1),old)
 def test_no_fake_success_or_inline_runner_claim(self):
  b=(SRC/'readme-block.md').read_text();doc=(ROOT/'atlas/actions-lab.md').read_text();self.assertIn('не запускался',b);self.assertIn('квоты',b);self.assertIn('права записи',b);self.assertIn('не исполняется внутри README',b)
  self.assertNotIn('/actions/runs/',b);self.assertNotIn('badge.svg',b);self.assertNotRegex(b,r'<(?:iframe|script|input|form)\b')
  self.assertIn('не проверялись',doc);self.assertIn('не общий лимит расходов',doc)
 def test_regeneration_never_dispatches_or_edits_readme_workflow(self):
  paths=[*sorted((ART/'example').iterdir()),ART/'manifest.json',ROOT/'README.md',WF,SRC/'readme-block.md'];before={p:p.read_bytes() for p in paths}
  subprocess.run([sys.executable,str(SRC/'generate.py')],cwd=ROOT,check=True)
  self.assertEqual(before,{p:p.read_bytes() for p in paths})
