"""Read-only GitHub Markdown API smoke test. Does NOT start a WebGL viewer."""
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[3]
class Rendered(HTMLParser):
 def __init__(self):super().__init__();self.payloads=[];self.containers=0;self.in_stl=False;self.raw=''
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='section' and d.get('data-type')=='stl':self.containers+=1
  if 'data-json' in d:
   try:self.payloads.append(json.loads(d['data-json']).get('data'))
   except (ValueError,AttributeError):pass
  if tag=='pre' and d.get('lang')=='stl':self.in_stl=True
 def handle_endtag(self,tag):
  if tag=='pre':self.in_stl=False
 def handle_data(self,data):
  if self.in_stl:self.raw+=data
if __name__=='__main__':
 request={'text':(ROOT/'atlas/dual-solid/README.md').read_text(),'mode':'gfm','context':'overbaffe1/gitEdit'}
 response=subprocess.check_output(['gh','api','markdown','--input','-'],input=json.dumps(request),text=True)
 parsed=Rendered();parsed.feed(response);model=(ROOT/'assets/dual-solid/ai-3d.stl').read_text()
 assert parsed.containers==1,parsed.containers
 assert model in parsed.payloads,'STL enrichment payload changed or missing'
 assert parsed.raw==model,'Raw fallback STL differs from file'
 print('PASS: one native STL enrichment container, exact 632-facet payload and raw fallback. WebGL/browser rendering not tested.')
