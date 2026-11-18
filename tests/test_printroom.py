"""Same original field, six encodings; validate the algorithms and shipped results."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT/'atlas/samples/printroom/generate.py'
ART = ROOT/'assets/printroom'
spec = importlib.util.spec_from_file_location('printroom',GEN)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
NAMES = {'indigo','halftone','bayer','ascii','hatch','isolines'}
NS = {'s':'http://www.w3.org/2000/svg'}


def read_pgm():
    lines = (ART/'source.pgm').read_text().splitlines()
    tokens = ' '.join(line for line in lines if not line.startswith('#')).split()
    assert tokens[:4] == ['P2','128','80','255']
    numbers = list(map(int,tokens[4:]))
    assert len(numbers) == 128*80
    return [numbers[i:i+128] for i in range(0,len(numbers),128)]


class PrintroomTest(unittest.TestCase):
    def test_original_distance_field(self):
        # Rotations preserve distance to the origin; the origin is in the hole.
        self.assertAlmostEqual(gen.sdf((0,0,0)),.58)
        # Evaluate points on the central circle using inverse rotations of sdf().
        import math
        for t in (0,.7,1.8,3.2):
            x,y,z=.88*math.cos(t),.88*math.sin(t),0
            # Invert the y rotation, then x rotation.
            x,z=x*math.cos(.3)-z*math.sin(.3),x*math.sin(.3)+z*math.cos(.3)
            y,z=y*math.cos(.65)+z*math.sin(.65),-y*math.sin(.65)+z*math.cos(.65)
            self.assertAlmostEqual(gen.sdf((x,y,z)),-.30)

    def test_render_matches_pgm_with_nonempty_hole(self):
        image = read_pgm()
        self.assertEqual(gen.render(),image)
        self.assertTrue(all(0<=v<=255 for row in image for v in row))
        hits = sum(v<255 for row in image for v in row)
        self.assertGreater(hits,1500)
        self.assertLess(hits,6000)
        self.assertEqual(image[40][64],255)
        self.assertEqual(image[0][0],255)
        self.assertLess(min(v for row in image for v in row),60)

    def test_bayer_thresholds_and_endpoints(self):
        self.assertEqual(sorted(v for row in gen.BAYER for v in row),list(range(16)))
        for gray in (0,64,128,192,255):
            result = gen.dither([[gray]*4 for _ in range(4)])
            self.assertTrue(all(type(v) is bool for row in result for v in row))
            expected = sum(gray/255 < (v+.5)/16 for row in gen.BAYER for v in row)
            self.assertEqual(sum(sum(row) for row in result),expected)
        self.assertEqual(sum(map(sum,gen.dither([[0]*4 for _ in range(4)]))),16)
        self.assertEqual(sum(map(sum,gen.dither([[255]*4 for _ in range(4)]))),0)

    def test_ascii_is_actual_portable_text(self):
        value = (ART/'torus.txt').read_text()
        self.assertTrue(value.isascii())
        self.assertEqual(gen.ascii_art(read_pgm()),value)
        rows = value.splitlines()
        self.assertEqual(len(rows),20)
        self.assertTrue(all(len(row)==64 for row in rows))
        self.assertTrue(set(value)-{'\n'} <= set(gen.RAMP))
        readme = (ROOT/'README.md').read_text()
        # Markdown trims unused right margins, but keeps every visible symbol.
        trimmed = '\n'.join(row.rstrip() for row in rows)+'\n'
        self.assertIn('```text\n'+trimmed+'```',readme)
        self.assertEqual(gen.ascii_art([[255]*128 for _ in range(80)]),(' '*64+'\n')*20)

    def test_rle_preserves_pixels_and_rows(self):
        source = [[1,1,1,2,2],[3,4,4,4,5]]
        result = [[None]*5 for _ in range(2)]
        for x,y,width,value in gen.rle(source):
            self.assertGreater(width,0)
            for i in range(x,x+width):
                self.assertIsNone(result[y][i])
                result[y][i]=value
        self.assertEqual(source,result)

    def test_contours_interpolate_and_handle_saddles(self):
        segments = gen.contours([[0,100],[0,100]],25)
        self.assertEqual(len(segments),1)
        self.assertEqual({tuple(p) for p in segments[0]},{(.25,0),(.25,1)})
        self.assertEqual(gen.contours([[50,50],[50,50]],25),[])
        self.assertEqual(len(gen.contours([[0,100],[100,0]],50)),2)

    def test_self_contained_statics_and_readme_wiring(self):
        self.assertEqual({p.stem for p in ART.glob('*.svg')},NAMES)
        readme = (ROOT/'README.md').read_text()
        for file in ART.glob('*.svg'):
            svg = ET.parse(file).getroot()
            self.assertEqual(svg.attrib['viewBox'],'0 0 1040 560')
            self.assertTrue(svg.find('s:title',NS).text)
            self.assertTrue(svg.find('s:desc',NS).text)
            for node in svg.iter():
                self.assertNotIn(node.tag.rsplit('}',1)[-1],{'script','image','foreignObject','animate','animateMotion'})
                for attr,value in node.attrib.items():
                    self.assertFalse(attr.startswith('on'))
                    self.assertNotIn('http',value)
            self.assertRegex(readme,rf'<img src="assets/printroom/{file.name}"[^>]+alt="[^"]{{30,}}"')
        self.assertIn('](atlas/printroom.md)',readme)
        self.assertIn('](assets/printroom/torus.txt)',readme)

    def test_clean_reprint_does_not_edit_readme(self):
        before = (ROOT/'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual({p.name for p in ART.iterdir()},{p.name for p in Path(tmp).iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)
        self.assertEqual(before,(ROOT/'README.md').read_bytes())
