import csv
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

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/locator';ASSETS=ROOT/'assets/locator'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
c=module('locator_codebook',SAMPLE/'codebook.py');sys.modules['codebook']=c
a=module('locator_audit',SAMPLE/'audit.py')

class LocatorTests(unittest.TestCase):
    def test_lfsr_cycle_and_crt_map(self):
        state=1;seen=set();sequence=[]
        for _ in range(4095):
            self.assertNotIn(state,seen);seen.add(state);sequence.append(state&1)
            feedback=sum((state>>bit)&1 for bit in (0,1,4,6))%2;state=(state>>1)|(feedback<<11)
        self.assertEqual(state,1);grid=c.load(ASSETS/'pattern.csv')
        for y in range(65):
            for x in range(63):
                index=(2080*x+2016*y)%4095;self.assertEqual(index%63,x);self.assertEqual(index%65,y);self.assertEqual(grid[y][x],sequence[index])

    def test_certificate_and_independent_all_pair_distance(self):
        grid=c.load(ASSETS/'pattern.csv');report=a.audit(grid);self.assertEqual(report,json.loads((ASSETS/'certificate.json').read_text()))
        self.assertEqual(report['extended_rank_gf2'],12);self.assertEqual(report['window4_pair_distance'],1);self.assertEqual(report['certified_pair_distance'],7)
        codes=[code for _,_,code in c.book(grid)]
        # Exhaustively cross-check pair distance without relying on linearity argument.
        minimum=min((x^y).bit_count() for i,x in enumerate(codes) for y in codes[i+1:])
        self.assertEqual(minimum,7)

    def test_all_positions_exact_and_wrapped_crops(self):
        grid=c.load(ASSETS/'pattern.csv');entries=c.book(grid)
        self.assertEqual(len({c.signature(grid,x,y,4) for x,y,_ in entries}),4095)
        for x,y,code in entries[::137]+entries[-5:]:self.assertEqual(c.locate(entries,code)['position'],{'x':x,'y':y,'distance':0})
        crop='\n'.join(''.join(str(grid[(63+dy)%65][(61+dx)%63]) for dx in range(6)) for dy in range(6))+'\n'
        self.assertEqual(c.signature(grid,61,63),c.parse_patch(crop))

    def test_all_zero_to_three_flip_patterns_at_one_origin(self):
        entries=c.book(c.load(ASSETS/'pattern.csv'));original=next(code for x,y,code in entries if (x,y)==(9,12));count=0
        for size in range(4):
            for bits in itertools.combinations(range(36),size):
                observed=original
                for bit in bits:observed^=1<<bit
                self.assertEqual(c.locate(entries,observed)['position'],{'x':9,'y':12,'distance':size});count+=1
        self.assertEqual(count,7807)

    def test_beyond_guarantee_can_miscorrect(self):
        entries=c.book(c.load(ASSETS/'pattern.csv'));observed,target,bits=c.four_error_example(entries,9,12)
        self.assertEqual(sum(code.bit_count()==7 for _,_,code in entries),4) # each nonzero source has a nonzero distance-seven partner
        result=c.locate(entries,observed);self.assertTrue(result['accepted']);self.assertEqual(result['position'],{'x':11,'y':4,'distance':3})
        self.assertEqual(target,{'x':11,'y':4});self.assertEqual(len(bits),4)
        self.assertFalse(c.locate(entries,0)['accepted'])
        self.assertEqual(c.parse_patch((ASSETS/'four-flips-wrong.txt').read_text()),observed)

    def test_bad_input_rejection(self):
        for text in ('','000000\n'*5,'00000x\n'*6,'0'*36):
            with self.assertRaises(ValueError):c.parse_patch(text)
        for value in (-1,1<<36,True):
            with self.assertRaises(ValueError):c.locate([],value)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.csv';path.write_text('0,1\n')
            with self.assertRaises(ValueError):c.load(path)

    def test_standalone_decoder_and_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            for name in ('codebook.py','locate.py','audit.py'):shutil.copy(SAMPLE/name,tmp/name)
            for name in ('pattern.csv','three-flips.txt','zero-rejected.txt'):shutil.copy(ASSETS/name,tmp/name)
            result=subprocess.run([sys.executable,'-S',str(tmp/'locate.py'),str(tmp/'pattern.csv'),str(tmp/'three-flips.txt')],check=True,text=True,capture_output=True,cwd=tmp)
            self.assertEqual(json.loads(result.stdout)['position'],{'x':9,'y':12,'distance':3})
            result=subprocess.run([sys.executable,'-S',str(tmp/'audit.py'),str(tmp/'pattern.csv')],check=True,text=True,capture_output=True,cwd=tmp)
            self.assertEqual(json.loads(result.stdout)['certified_pair_distance'],7)
            result=subprocess.run([sys.executable,'-S',str(tmp/'locate.py'),str(tmp/'pattern.csv'),str(tmp/'zero-rejected.txt')],text=True,capture_output=True,cwd=tmp);self.assertEqual(result.returncode,2)

    def test_emitted_pattern_codebook_and_containers(self):
        grid=c.load(ASSETS/'pattern.csv')
        with Image.open(ASSETS/'pattern.png') as im:
            self.assertEqual(im.mode,'1');self.assertEqual(im.size,(504,520))
            for y in range(65):
                for x in range(63):self.assertEqual(bool(im.getpixel((x*8+4,y*8+4))),bool(grid[y][x]))
        with (ASSETS/'windows.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),4095)
        for row in rows:self.assertEqual(int(row['window6_hex'],16),c.signature(grid,int(row['x']),int(row['y'])))
        with zipfile.ZipFile(ASSETS/'bench.zip') as z:self.assertEqual(z.namelist(),['bench.html']);self.assertEqual(z.read('bench.html'),(ASSETS/'bench.html').read_bytes())
        with Image.open(ASSETS/'locate.gif') as im:self.assertEqual(im.n_frames,21);self.assertEqual(im.size,(1000,690))
        sources=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(sources),8)
        for record in sources:self.assertRegex(record['commit'],r'^[a-f0-9]{40}$');self.assertIn(record['commit'],record['url'])

    def test_byte_identical_regeneration(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            for path in ASSETS.iterdir():self.assertEqual(path.read_bytes(),(Path(tmp)/path.name).read_bytes(),path.name)

if __name__=='__main__':unittest.main()
