"""Checks for the GitHub-safe screening, textured GLB and identical offline studio. No dependencies."""
import base64
import json
import re
import struct
import unittest
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.by_tag = defaultdict(list)

    def handle_starttag(self, tag, attrs):
        self.by_tag[tag].append(dict(attrs))


class CrystalViewTest(unittest.TestCase):
    def test_one_screening_at_shared_permalink(self):
        before, after = (ROOT/'README.md').read_text(encoding='utf-8').split('\n### Покрути кристалл\n')
        self.assertIn('href="#покрути-кристалл"', before)
        section = re.split(r'^#{1,3} ', after, maxsplit=1, flags=re.M)[0]
        tags = Tags(); tags.feed(section)
        for tag in ('details','iframe','model-viewer','script'):
            self.assertNotIn(tag, tags.by_tag)
        self.assertNotIn('```stl', section.lower())
        link, = tags.by_tag['a']
        player = link['href']
        self.assertRegex(player, r'^https://(?:rawcdn\.githack\.com/overbaffe1/gitEdit/[a-f0-9]{40}/docs/index\.html|overbaffe1\.github\.io/gitEdit/)$')
        self.assertIn(f']({player})', section)
        self.assertIn(player+'?scene=ship', section)
        self.assertEqual(len(tags.by_tag['img']), 1)
        data = (ROOT/tags.by_tag['img'][0]['src']).read_bytes()
        self.assertEqual((data[:6], struct.unpack_from('<HH',data,6)), (b'GIF89a',(704,400)))
        self.assertIn(b'NETSCAPE2.0',data)
        still, = tags.by_tag['source']
        self.assertEqual(still['media'], '(prefers-reduced-motion: reduce)')
        self.assertEqual((ROOT/still['srcset']).read_bytes()[:3], b'\xff\xd8\xff')

    def test_glb_bakes_actual_facets_material_and_loop(self):
        raw = (SITE/'malachite.glb').read_bytes()
        self.assertEqual(struct.unpack_from('<4sII',raw), (b'glTF',2,len(raw)))
        length, kind = struct.unpack_from('<I4s',raw,12); self.assertEqual(kind,b'JSON')
        doc=json.loads(raw[20:20+length]); binary=raw[28+length:]
        def view(i):
            v=doc['bufferViews'][i]; start=v.get('byteOffset',0)
            return binary[start:start+v['byteLength']]
        def rows(i):
            a=doc['accessors'][i]; self.assertEqual(a['componentType'],5126)
            n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
            return list(struct.iter_unpack('<'+'f'*n,view(a['bufferView'])))
        material=doc['materials'][0]['pbrMetallicRoughness']
        for slot in ('baseColorTexture','metallicRoughnessTexture'):
            image=doc['images'][doc['textures'][material[slot]['index']]['source']]
            self.assertTrue(view(image['bufferView']).startswith(b'\x89PNG\r\n\x1a\n'))
        verts=[]
        for line in (ROOT/'atlas/samples/crystal.stl').read_text().splitlines():
            if line.split()[:1]==['vertex']:
                x,y,z=map(float,line.split()[1:]);verts.append((x/18,(z-17)/18,-y/18))
        leaves=[(i,n) for i,n in enumerate(doc['nodes']) if n['name'].startswith('Leaf_')]
        self.assertEqual(len(leaves),8)
        clip,=doc['animations']; self.assertEqual(clip['name'],'Размыкание')
        for j,(i,node) in enumerate(leaves):
            face=doc['meshes'][node['mesh']]['primitives'][0];self.assertEqual(face['material'],0)
            self.assertEqual(len(rows(face['attributes']['TEXCOORD_0'])),3)
            for pt,src in zip(rows(face['attributes']['POSITION']),verts[3*j:3*j+3]):
                for p,c,s in zip(pt,node['translation'],src):self.assertAlmostEqual(c+p/(.99*.95),s,places=5)
            c,=[c for c in clip['channels'] if c['target']=={'node':i,'path':'translation'}]
            sampler=clip['samplers'][c['sampler']];keys=rows(sampler['output']);times=rows(sampler['input'])
            self.assertEqual((times[0],times[-1]),((0.,),(8.,)))
            self.assertEqual(keys[0],keys[-1]);self.assertNotEqual(keys[0],keys[len(keys)//2])

    def test_offline_studio_is_the_same_player(self):
        with ZipFile(ROOT/'assets/crystal-view.zip') as z:
            self.assertEqual(z.namelist(),['crystal.html']);html=z.read('crystal.html').decode()
        encoded=re.search(r'<script id="embedded-glb"[^>]*>([^<]+)</script>',html).group(1)
        self.assertEqual(base64.b64decode(encoded),(SITE/'malachite.glb').read_bytes())
        self.assertIn((SITE/'stage.js').read_text().replace('</script',r'<\/script'),html)
        self.assertIn((SITE/'studio.css').read_text(),html)
        self.assertNotIn('<script src=',html)
