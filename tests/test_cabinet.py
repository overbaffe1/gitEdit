"""Verify actual inputs and geometric encodings of the repository data room."""
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / 'atlas/samples/cabinet/generate.py'
ART = ROOT / 'assets/cabinet'
spec = importlib.util.spec_from_file_location('cabinet', GEN)
cabinet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cabinet)
NAMES = {'treemap','donut','pareto','compression','headers','spectrum'}
NS = {'s':'http://www.w3.org/2000/svg'}


class CabinetTest(unittest.TestCase):
    def test_measurements_match_all_original_files(self):
        data = json.loads((ART / 'measurements.json').read_text())
        self.assertIn('NOT whole repository',data['scope'])
        self.assertEqual(data['zlib_version'],zlib.ZLIB_RUNTIME_VERSION)
        rows = cabinet.collect()
        self.assertEqual(data['files'],rows)
        self.assertEqual(len(rows),12)
        self.assertEqual(len({r['format'] for r in rows}),12)
        self.assertEqual(data['total_bytes'],sum(r['bytes'] for r in rows))
        for r in rows:
            raw = (ROOT / r['path']).read_bytes()
            self.assertEqual(r['bytes'],len(raw))
            self.assertEqual(r['sha256'],hashlib.sha256(raw).hexdigest())
            self.assertEqual(r['first16_hex'],raw[:16].hex())
            self.assertEqual(r['zlib_bytes'],len(zlib.compress(raw,9)))
            self.assertEqual(sum(r['histogram16']),len(raw))
            expected = [0]*16
            for b in raw:
                expected[b//16]+=1
            self.assertEqual(r['histogram16'],expected)
            self.assertNotIn('/cabinet/',r['path'])

    def test_csv_is_an_exact_projection_of_json(self):
        data = json.loads((ART / 'measurements.json').read_text())
        rows = list(csv.DictReader(io.StringIO((ART / 'files.csv').read_text())))
        self.assertEqual(len(rows),12)
        for csv_row,json_row in zip(rows,data['files']):
            for key,value in csv_row.items():
                self.assertEqual(value,str(json_row[key]))

    def test_treemap_area_bounds_and_nonoverlap(self):
        rows = sorted(cabinet.collect(),key=lambda r:(-r['bytes'],r['id']))
        rects = cabinet.rectangles(rows,30,100,650,360)
        total = sum(r['bytes'] for r in rows)
        self.assertEqual({r['id'] for r,*_ in rects},{r['id'] for r in rows})
        for r,x,y,w,h in rects:
            self.assertGreater(w,0); self.assertGreater(h,0)
            self.assertGreaterEqual(x,30-1e-8); self.assertGreaterEqual(y,100-1e-8)
            self.assertLessEqual(x+w,680+1e-8); self.assertLessEqual(y+h,460+1e-8)
            self.assertAlmostEqual(w*h/(650*360),r['bytes']/total,places=12)
        for i,(_,x,y,w,h) in enumerate(rects):
            for _,u,v,a,b in rects[i+1:]:
                overlap_x = max(0,min(x+w,u+a)-max(x,u))
                overlap_y = max(0,min(y+h,v+b)-max(y,v))
                self.assertLess(overlap_x*overlap_y,1e-8)

    def test_ring_encodes_proportions(self):
        rows = sorted(cabinet.collect(),key=lambda r:(-r['bytes'],r['id']))
        circles = ET.parse(ART / 'donut.svg').getroot().findall('s:circle',NS)
        total = sum(r['bytes'] for r in rows)
        self.assertEqual(len(circles),12)
        for circle,row in zip(circles,rows):
            arc,gap = map(float,circle.attrib['stroke-dasharray'].split())
            self.assertAlmostEqual(arc/(arc+gap),row['bytes']/total,places=8)

    def test_clean_print_and_inputs_untouched(self):
        before = {p:(ROOT/p).read_bytes() for p in cabinet.SAMPLE}
        readme = (ROOT / 'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual({p.name for p in ART.iterdir()},{p.name for p in Path(tmp).iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(),(Path(tmp) / file.name).read_bytes(),file.name)
        for path,raw in before.items():
            self.assertEqual(raw,(ROOT/path).read_bytes())
        self.assertEqual(readme,(ROOT/'README.md').read_bytes())

    def test_static_self_contained_svg_and_links(self):
        self.assertEqual({p.stem for p in ART.glob('*.svg')},NAMES)
        readme = (ROOT/'README.md').read_text()
        for file in ART.glob('*.svg'):
            root = ET.parse(file).getroot()
            self.assertEqual(root.attrib['viewBox'],'0 0 1040 520')
            self.assertTrue(root.find('s:title',NS).text)
            self.assertTrue(root.find('s:desc',NS).text)
            for node in root.iter():
                self.assertNotIn(node.tag.rsplit('}',1)[-1],{'script','foreignObject','image','animate','animateMotion'})
                for attr,value in node.attrib.items():
                    self.assertFalse(attr.startswith('on'))
                    self.assertNotIn('http',value)
            self.assertRegex(readme,rf'<img src="assets/cabinet/{file.name}"[^>]+alt="[^"]{{30,}}"')
        self.assertIn('](atlas/cabinet.md)',readme)
        for name in ('files.csv','measurements.json'):
            self.assertIn(f'](assets/cabinet/{name})',readme)
