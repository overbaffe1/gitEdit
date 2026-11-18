"""Check objective drawing facts, not whether every viewer perceives an illusion."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'atlas/samples/perception/generate.py'
ART=ROOT/'assets/perception'
spec=importlib.util.spec_from_file_location('perception',GEN)
gen=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
NS={'s':'http://www.w3.org/2000/svg'}


def svg(name,proof=False):
    return ET.parse(ART/f'{name}{"-proof" if proof else ""}.svg').getroot()


def targets(name,kind,proof=False):
    return svg(name,proof).findall(f'.//*[@data-target="{kind}"]')


class PerceptionTest(unittest.TestCase):
    def test_equal_circles_and_reveal_does_not_resize_targets(self):
        for proof in (False,True):
            nodes=targets('ebbinghaus','equal-circle',proof)
            self.assertEqual(len(nodes),2)
            self.assertEqual([float(n.attrib['r']) for n in nodes],[28,28])
            self.assertEqual([float(n.attrib['cy']) for n in nodes],[285,285])
        a=[n.attrib for n in targets('ebbinghaus','equal-circle')]
        b=[n.attrib for n in targets('ebbinghaus','equal-circle',True)]
        self.assertEqual(a,b)

    def test_segments_and_verticals_are_really_straight(self):
        for proof in (False,True):
            nodes=targets('muller-lyer','equal-segment',proof)
            self.assertEqual(len(nodes),2)
            for n in nodes:
                self.assertEqual(float(n.attrib['x2'])-float(n.attrib['x1']),520)
                self.assertEqual(n.attrib['y1'],n.attrib['y2'])
                self.assertEqual((float(n.attrib['x1']),float(n.attrib['x2'])),(260,780))
            nodes=targets('hering','vertical-line',proof)
            self.assertEqual(len(nodes),2)
            for n in nodes:
                self.assertEqual(n.attrib['x1'],n.attrib['x2'])
                self.assertEqual((n.attrib['y1'],n.attrib['y2']),('130','440'))

    def test_wall_guides_are_parallel_and_within_mortar(self):
        nodes=targets('cafe-wall','horizontal-guide',True)
        self.assertEqual(len(nodes),7)
        for row,n in enumerate(nodes):
            y=float(n.attrib['y1'])
            self.assertEqual(y,float(n.attrib['y2']))
            self.assertEqual(y,128+row*42+40.5)
            self.assertTrue(128+row*42+39<y<128+(row+1)*42)

    def test_gray_is_the_same_color_not_opacity_trick(self):
        for proof in (False,True):
            nodes=targets('contrast','equal-gray',proof)
            self.assertEqual(len(nodes),2)
            for n in nodes:
                self.assertEqual(n.attrib['fill'],'#888888')
                self.assertNotIn('opacity',n.attrib)
                self.assertEqual((n.attrib['width'],n.attrib['height']),('90','100'))

    def test_kanizsa_has_no_visible_outline_and_matches_paper(self):
        for proof in (False,True):
            root=svg('kanizsa',proof)
            paper=root.find('s:rect',NS).attrib['fill']
            cutouts=targets('kanizsa','paper-cutout',proof)
            self.assertEqual(len(cutouts),1)
            self.assertEqual(cutouts[0].attrib['fill'],paper)
            self.assertNotIn('stroke',cutouts[0].attrib)
            self.assertEqual(len(targets('kanizsa','disk',proof)),3)
        proof_polygons=svg('kanizsa',True).findall('s:polygon',NS)
        self.assertEqual(len(proof_polygons),2)
        self.assertEqual(len(svg('kanizsa').findall('s:polygon',NS)),1)
        self.assertEqual(proof_polygons[1].attrib['fill'],'none')

    def test_self_contained_files_and_readme_links(self):
        expected={f'{name}{suffix}.svg' for name in gen.NAMES for suffix in ('','-proof')}
        self.assertEqual({p.name for p in ART.glob('*.svg')},expected)
        readme=(ROOT/'README.md').read_text()
        for name in gen.NAMES:
            pattern=rf'<a href="assets/perception/{name}-proof.svg"><img src="assets/perception/{name}.svg"[^>]+alt="[^"]{{30,}}"'
            self.assertRegex(readme,pattern)
        for file in ART.glob('*.svg'):
            source=file.read_text()
            self.assertNotIn('@keyframes',source)
            root=ET.fromstring(source)
            self.assertTrue(root.find('s:title',NS).text)
            self.assertTrue(root.find('s:desc',NS).text)
            ids={n.attrib['id'] for n in root.iter() if 'id' in n.attrib}
            for node in root.iter():
                self.assertNotIn(node.tag.rsplit('}',1)[-1],{'script','image','foreignObject','animate','animateMotion'})
                for attr,value in node.attrib.items():
                    self.assertFalse(attr.startswith('on'))
                    self.assertNotIn('http',value)
                    if value.startswith('url(#'):
                        self.assertIn(value[5:-1],ids)
        facts=json.loads((ART/'facts.json').read_text())
        self.assertEqual(facts['ebbinghaus']['target_radii'],[28,28])
        self.assertEqual(facts['contrast']['target_fill'],['#888888']*2)
        self.assertIn('](atlas/perception.md)',readme)

    def test_clean_reprint_preserves_readme(self):
        before=(ROOT/'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual({p.name for p in ART.iterdir()},{p.name for p in Path(tmp).iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)
        self.assertEqual(before,(ROOT/'README.md').read_bytes())
