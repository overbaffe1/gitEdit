import base64
import copy
import csv
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/shards';ASSETS=ROOT/'assets/shards'
spec=importlib.util.spec_from_file_location('shards_codec',SAMPLE/'codec.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def records():return [json.loads(p.read_text()) for p in sorted((ASSETS/'fragments').glob('*.json'))]

class ShardsTests(unittest.TestCase):
    def test_field_arithmetic(self):
        self.assertEqual(c.multiply(128,2),29);self.assertEqual(c.multiply(7,11),49)
        for a in range(1,256):self.assertEqual(c.TABLE[a][c.power(a,254)],1)
        for a,b,d in [(12,45,67),(128,212,253),(255,0,18)]:
            self.assertEqual(c.multiply(a,b^d),c.multiply(a,b)^c.multiply(a,d))
        self.assertEqual(c.GENERATOR[:6],[[int(i==j) for j in range(6)] for i in range(6)])
        with self.assertRaises(ValueError):c.inverse([[1,1],[1,1]])

    def test_independent_lagrange_evaluation(self):
        # Alternate construction: interpolate through known data at x=1..6,
        # then evaluate at x=7..10, without codec.generator or matrix inversion.
        data=bytes([3,18,39,58,199,250]);encoded=c.encode(data)
        for x in range(7,11):
            expected=0
            for j in range(1,7):
                numerator=denominator=1
                for m in range(1,7):
                    if m!=j:numerator=c.multiply(numerator,x^m);denominator=c.multiply(denominator,j^m)
                expected^=c.multiply(data[j-1],c.multiply(numerator,c.power(denominator,254)))
            self.assertEqual(c.validate(encoded[x-1]),bytes([expected]))

    def test_all_210_six_subsets_exact(self):
        shards=records();original=(ASSETS/'source.png').read_bytes()
        for indices in itertools.combinations(range(10),6):self.assertEqual(c.decode([shards[i] for i in indices]),original,indices)
        rows=list(csv.DictReader((ASSETS/'recoveries.csv').open()));self.assertEqual(len(rows),210)
        self.assertTrue(all(row['sha256']==hashlib.sha256(original).hexdigest() and row['exact_match']=='true' for row in rows))
        self.assertEqual(c.decode(list(reversed(shards))),original)

    def test_padding_and_arbitrary_binary(self):
        for size in (1,2,5,6,7,255,256,511):
            payload=bytes((i*83+size)%256 for i in range(size));shards=c.encode(payload)
            self.assertEqual(c.decode([shards[i] for i in (1,3,6,7,8,9)]),payload)
        with self.assertRaises(ValueError):c.encode(b'')

    def test_reject_missing_duplicate_mixed_and_bad_metadata(self):
        shards=records()
        for selection in (shards[:5],[shards[0]]*6,shards+[shards[0]]):
            with self.assertRaises(ValueError):c.decode(selection)
        broken=copy.deepcopy(shards[:6]);broken[0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'mixed'):c.decode(broken)
        for key,value in [('size',0),('size',True),('index',10),('index',-1),('data','!'),('format','other'),('sha256','Z'*64)]:
            broken=copy.deepcopy(shards[:6]);broken[0][key]=value
            with self.assertRaises(ValueError):c.decode(broken)

    def test_corruption_and_not_authentication(self):
        shards=records();bad=copy.deepcopy(shards[:6]);block=bytearray(c.validate(bad[0]));block[4]^=1;bad[0]['data']=base64.b64encode(block).decode()
        with self.assertRaisesRegex(ValueError,'shard checksum'):c.decode(bad)
        bad[0]['block_sha256']=hashlib.sha256(block).hexdigest()
        with self.assertRaisesRegex(ValueError,'restored file checksum'):c.decode(bad)
        # Anyone who can replace blocks AND all hashes can provide another file.
        replacement=b'not the lighthouse';self.assertEqual(c.decode(c.encode(replacement)[:6]),replacement)

    def test_decoder_alone_without_art_or_libraries(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);shutil.copy(SAMPLE/'codec.py',tmp)
            files=[]
            for i in (1,4,7,8,9,10):
                name=f'fragment-{i:02}.json';shutil.copy(ASSETS/'fragments'/name,tmp/name);files.append(str(tmp/name))
            subprocess.run([sys.executable,'-I',str(tmp/'codec.py'),*files,'--output',str(tmp/'out.png')],check=True,cwd=tmp,capture_output=True)
            self.assertEqual((tmp/'out.png').read_bytes(),(ASSETS/'source.png').read_bytes())

    def test_containers_pins_and_no_source_in_html(self):
        with zipfile.ZipFile(ASSETS/'fragments.zip') as archive:
            self.assertEqual(len(archive.namelist()),10)
            for name in archive.namelist():self.assertEqual(archive.read(name),(ASSETS/'fragments'/name).read_bytes())
        with zipfile.ZipFile(ASSETS/'bench.zip') as archive:self.assertEqual(archive.namelist(),['bench.html']);self.assertEqual(archive.read('bench.html'),(ASSETS/'bench.html').read_bytes())
        html=(ASSETS/'bench.html').read_text();self.assertNotIn('data:image/png',html);self.assertNotIn('source.png',html);self.assertNotIn('<script src',html)
        self.assertNotIn(base64.b64encode((ASSETS/'source.png').read_bytes()).decode(),html)
        sources=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(sources),8)
        for source in sources:self.assertRegex(source['commit'],r'^[a-f0-9]{40}$');self.assertIn(source['commit'],source['url'])
        with Image.open(ASSETS/'recover.gif') as im:self.assertEqual(im.n_frames,11);self.assertEqual(im.size,(1000,580))

    def test_regenerate_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            for file in ASSETS.rglob('*'):
                if file.is_file():self.assertEqual(file.read_bytes(),(Path(tmp)/file.relative_to(ASSETS)).read_bytes(),str(file))

if __name__=='__main__':unittest.main()
