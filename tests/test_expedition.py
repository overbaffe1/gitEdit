"""The hyperlink game is a compiled finite-state machine, not a screenshot."""
from collections import deque
import csv
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'atlas/samples/expedition/generate.py'
ART=ROOT/'assets/wayfinder'
PAGES=ROOT/'atlas/wayfinder'
spec=importlib.util.spec_from_file_location('expedition',GEN)
gen=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


class ExpeditionTest(unittest.TestCase):
    def test_reachable_graph_exactly_matches_published_states(self):
        data=json.loads((ART/'states.json').read_text())
        states=gen.reachable()
        self.assertEqual(len(states),32)
        self.assertEqual({s['id'] for s in data['states']},{gen.state_id(s) for s in states})
        self.assertEqual({p.stem for p in PAGES.glob('r*.md')},{gen.state_id(s) for s in states})
        self.assertEqual(data['start'],'r00-i0')
        self.assertEqual(data['goal'],'r08-i3')
        for state in data['states']:
            expected=[{'label':label,'target':gen.state_id(target)} for label,target in gen.neighbors((state['room'],state['inventory']))]
            self.assertEqual(state['moves'],expected)
            self.assertEqual(state['won'],gen.won((state['room'],state['inventory'])))

    def test_every_state_can_reach_victory_without_reset(self):
        states=gen.reachable()
        for start in states:
            seen={start};queue=deque([start]);found=False
            while queue:
                state=queue.popleft()
                if gen.won(state):
                    found=True;break
                for _,target in gen.neighbors(state):
                    if target not in seen:
                        seen.add(target);queue.append(target)
            self.assertTrue(found,start)

    def test_pickups_are_monotonic_and_moves_use_real_doors(self):
        for room,mask in gen.reachable():
            self.assertEqual(gen.normalize(room,mask),(room,mask))
            if room==2:self.assertTrue(mask&2)
            if room==6:self.assertTrue(mask&1)
            for _,(target,inventory) in gen.neighbors((room,mask)):
                self.assertIn(tuple(sorted((room,target))),gen.EDGES)
                self.assertEqual(mask&inventory,mask)
                self.assertEqual(inventory,mask|gen.PICKUPS.get(target,0))
        self.assertFalse(gen.won((8,0)))
        self.assertFalse(gen.won((8,1)))
        self.assertFalse(gen.won((8,2)))
        self.assertEqual(gen.neighbors((8,3)),[])

    def test_complete_route_and_return_trip_preserve_inventory(self):
        route=[0,3,6,7,8,5,2,5,8]
        state=(0,0)
        for room in route[1:]:
            targets=[target for _,target in gen.neighbors(state) if target[0]==room]
            self.assertEqual(len(targets),1)
            state=targets[0]
        self.assertEqual(state,(8,3))
        self.assertIn('**Победа.**',(PAGES/'r08-i3.md').read_text())
        for mask in (0,1,2):
            path=PAGES/f'r08-i{mask}.md'
            if path.exists():
                self.assertNotIn('**Победа.**',path.read_text())
                self.assertIn('Не хватает:',path.read_text())

    def test_page_controls_exactly_match_graph_and_no_side_effect_urls(self):
        for state in gen.reachable():
            page=PAGES/f'{gen.state_id(state)}.md'
            source=page.read_text()
            self.assertIn(f'**Инвентарь: {gen.inventory_label(state[1])}.**',source)
            controls=re.findall(r'\[((?:Север|Юг|Запад|Восток): [^\]]+)\]\((r\d{2}-i\d\.md)\)',source)
            expected={(label+': '+gen.ROOMS[target[0]][0],gen.state_id(target)+'.md') for label,target in gen.neighbors(state)}
            self.assertEqual(set(controls),expected)
        for page in PAGES.glob('*.md'):
            source=page.read_text()
            self.assertNotRegex(source,r'<(?:script|iframe|form)\b|issues/new|workflow_dispatch')
            for href in re.findall(r'(?:href="|\]\()([^"\s)]+)',source):
                parts=urlsplit(href)
                self.assertFalse(parts.scheme or parts.netloc or parts.query or parts.fragment,href)
                resolved=(page.parent/parts.path).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT),href)
                self.assertTrue(resolved.is_file(),(page,href))

    def test_nine_original_self_contained_static_scenes(self):
        self.assertEqual(len(list(ART.glob('room*.svg'))),9)
        for file in ART.glob('room*.svg'):
            source=file.read_text()
            self.assertNotIn('@keyframes',source)
            root=ET.fromstring(source)
            ns={'s':'http://www.w3.org/2000/svg'}
            self.assertTrue(root.find('s:title',ns).text)
            self.assertTrue(root.find('s:desc',ns).text)
            for node in root.iter():
                self.assertNotIn(node.tag.rsplit('}',1)[-1],{'script','image','foreignObject','animate','animateMotion'})
                for key,value in node.attrib.items():
                    self.assertFalse(key.startswith('on'))
                    self.assertNotIn('http',value)
        readme=(ROOT/'README.md').read_text()
        self.assertIn('<a href="atlas/wayfinder/r00-i0.md"><img src="assets/wayfinder/room00.svg"',readme)

    def test_research_count_scope_and_pinned_source_evidence(self):
        folder=ROOT/'atlas/samples/expedition'
        rows=list(csv.DictReader(io.StringIO((folder/'survey.csv').read_text())))
        info=json.loads((folder/'sources.json').read_text())
        self.assertEqual(len(rows),102)
        self.assertEqual(len({r['repository'].lower() for r in rows}),102)
        self.assertEqual(info['unique_canonical_repositories'],102)
        self.assertEqual(info['lookup_attempts'],106)
        self.assertEqual(info['successful_readme_responses'],103)
        self.assertEqual(len(info['failed_lookups']),3)
        self.assertEqual(len(info['source_files']),9)
        self.assertEqual(len({r['repo'] for r in info['source_files']}),8)
        self.assertEqual(sum(r['review_level']=='source sample' for r in rows),8)
        for row in rows:
            self.assertRegex(row['readme_blob_sha'],r'^[a-f0-9]{40}$')
            self.assertGreater(int(row['readme_bytes']),0)
            self.assertTrue(row['url'].startswith('https://github.com/'))
        for row in info['source_files']:
            self.assertIn('/blob/'+row['commit']+'/',row['url'])

    def test_clean_reprint_does_not_touch_root_readme(self):
        before=(ROOT/'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)
            (dest/'README.md').write_text('untouched')
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual((dest/'README.md').read_text(),'untouched')
            for folder in (Path('assets/wayfinder'),Path('atlas/wayfinder')):
                self.assertEqual({p.name for p in (dest/folder).iterdir()},{p.name for p in (ROOT/folder).iterdir()})
                for file in (ROOT/folder).iterdir():
                    self.assertEqual(file.read_bytes(),(dest/folder/file.name).read_bytes(),file.name)
        self.assertEqual(before,(ROOT/'README.md').read_bytes())
