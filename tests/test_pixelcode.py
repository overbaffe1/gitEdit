"""The artifact must be executable pixels, not a pre-recorded story about code."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SAMPLE=ROOT/'atlas/samples/pixelcode'
ART=ROOT/'assets/pixelcode'
spec=importlib.util.spec_from_file_location('pixelcode_runner',SAMPLE/'runner.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)


class Pixelcode(unittest.TestCase):
    def test_raw_png_executes_without_generator_or_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            image=Path(tmp)/'only-input.png';image.write_bytes((ART/'program.png').read_bytes())
            result=subprocess.run([sys.executable,str(SAMPLE/'runner.py'),str(image)],capture_output=True,check=True)
            self.assertEqual(result.stdout,b'GIT')
            self.assertEqual(result.stderr,b'')
        data=(ART/'program.png').read_bytes();offset=8;chunks=[]
        while offset<len(data):
            length=struct.unpack('>I',data[offset:offset+4])[0]
            chunks.append(data[offset+4:offset+8]);offset+=12+length
        self.assertEqual(offset,len(data))
        self.assertEqual(set(chunks),{b'IHDR',b'IDAT',b'IEND'})
        with Image.open(ART/'program.png') as image:self.assertEqual(image.size,(22,14))

    def test_exported_trace_and_arithmetic_match_real_execution(self):
        actual=runner.run(runner.load(ART/'program.png'))
        self.assertEqual(actual,json.loads((ART/'trace.json').read_text()))
        self.assertTrue(actual['halted']);self.assertEqual(actual['stack'],[])
        trace=actual['trace'];self.assertEqual(len(trace),21)
        output_events=[row for row in trace if row['operation']=='outchar']
        self.assertEqual([row['stack_before'] for row in output_events],[[71],[73],[84]])
        self.assertEqual([row['output'] for row in output_events],['G','GI','GIT'])
        pushes=[row['stack_after'][-1] for row in trace if row['operation']=='push']
        self.assertEqual(pushes,[7,10,1,8,9,1,7,12,1])
        rows=list(csv.DictReader(io.StringIO((ART/'trace.csv').read_text())))
        self.assertEqual(len(rows),21)
        for row,event in zip(rows,trace):
            self.assertEqual(row['operation'],event['operation'])
            self.assertEqual(row['stdout'],event['output'])
            self.assertEqual(int(row['source_area']),event['area'])
        # Without a generator import, changing just one source pixel changes arithmetic/output.
        grid=runner.load(ART/'program.png');grid[6][0]=(0,0,0)
        changed=runner.run(grid)
        self.assertTrue(changed['halted']);self.assertEqual(changed['output'],'=IT')

    def test_halt_is_eight_geometric_blockages_not_step_budget(self):
        grid=runner.load(ART/'program.png');result=runner.run(grid)
        last=result['trace'][-1]
        self.assertEqual(last['operation'],'halt')
        self.assertEqual(last['area'],25)
        self.assertEqual(len(last['attempts']),8)
        self.assertEqual(len({(a['dp'],a['cc']) for a in last['attempts']}),8)
        block=runner.component(grid,tuple(last['source']))
        for dp in range(4):
            for cc in range(2):
                x,y=runner.exit_point(block,dp,cc);dx,dy=runner.DIRECTIONS[dp]
                self.assertEqual(grid[y+dy][x+dx],(0,0,0))
        limited=runner.run(grid,max_steps=3)
        self.assertFalse(limited['halted']);self.assertEqual(len(limited['trace']),3)
        result=subprocess.run([sys.executable,str(SAMPLE/'runner.py'),str(ART/'program.png'),'--max-steps','3'],capture_output=True)
        self.assertEqual(result.returncode,2)

    def test_exit_selection_and_four_neighbor_components(self):
        square={(x,y) for x in range(3) for y in range(3)}
        expected=[[(2,0),(2,2)],[(2,2),(0,2)],[(0,2),(0,0)],[(0,0),(2,0)]]
        for dp in range(4):
            for cc in range(2):self.assertEqual(runner.exit_point(square,dp,cc),expected[dp][cc])
        red=tuple(bytes.fromhex('ff0000'));black=(0,0,0)
        self.assertEqual(runner.component([[red,black],[black,red]],(0,0)),{(0,0)})
        stack=[];self.assertEqual(runner.execute('pop',1,stack,0),(0,''))
        self.assertEqual(runner.execute('multiply',1,stack,0),(0,''))
        stack=[-1];self.assertEqual(runner.execute('pointer',1,stack,0),(3,''));self.assertEqual(stack,[])

    def test_scale_24_preserves_codels_and_loader_rejects_bad_inputs(self):
        self.assertEqual(runner.load(ART/'program.png'),runner.load(ART/'program-24x.png',24))
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'bad.png'
            for color in ('white','#123456'):
                Image.new('RGB',(2,2),color).save(dest)
                with self.assertRaises(ValueError):runner.load(dest)
            Image.new('RGBA',(2,2),(255,0,0,0)).save(dest)
            with self.assertRaises(ValueError):runner.load(dest)
            with self.assertRaises(ValueError):runner.load(ART/'program.png',3)
            Image.new('RGB',(2,2),'red').save(dest)
            image=Image.open(dest);image.putpixel((1,1),(255,255,0));image.save(dest);image.close()
            with self.assertRaises(ValueError):runner.load(dest,2)
        with self.assertRaises(ValueError):runner.execute('roll',1,[],0)
        # A valid Piet command outside this runner's subset is not silently ignored.
        red=tuple(bytes.fromhex('ff0000'));yellow=tuple(bytes.fromhex('c0c000'))
        with self.assertRaises(ValueError):runner.run([[red,yellow]])

    def test_preview_uses_trace_and_reduced_motion_still(self):
        with Image.open(ART/'execution.gif') as gif:
            self.assertEqual(gif.n_frames,21)
            gif.seek(20);self.assertEqual(gif.info['duration'],2200)
        with Image.open(ART/'poster.png') as poster:self.assertEqual(poster.size,(1000,620))
        text=(ROOT/'README.md').read_text()
        section=text.split('## Пиксельный код',1)[1].split('\n## ',1)[0]
        self.assertIn('srcset="assets/pixelcode/poster.png"',section)
        self.assertIn('prefers-reduced-motion: reduce',section)
        self.assertIn('href="assets/pixelcode/program-24x.png"',section)
        self.assertNotIn('<script',section)

    def test_sources_pinned_with_honest_scope(self):
        rows=json.loads((SAMPLE/'sources.json').read_text())
        self.assertEqual(len(rows),8)
        self.assertEqual(sum('source_file' in row for row in rows),3)
        self.assertEqual(sum(len(row.get('additional_source_files',[])) for row in rows),1)
        for row in rows:
            self.assertRegex(row['commit'],r'^[0-9a-f]{40}$')
            self.assertIn('/blob/'+row['commit']+'/',row['url'])
            if 'source_file' in row:self.assertIn('/blob/'+row['commit']+'/',row['source_url'])
            for extra in row.get('additional_source_files',[]):self.assertIn('/blob/'+row['commit']+'/',extra['url'])
        helper=(SAMPLE/'check-external.cjs').read_text()
        self.assertIn('--allow-download',helper)
        self.assertIn('Piet.colorvec2color',helper)

    def test_reprint_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for source in ART.iterdir():self.assertEqual(source.read_bytes(),(Path(tmp)/source.name).read_bytes(),source.name)
