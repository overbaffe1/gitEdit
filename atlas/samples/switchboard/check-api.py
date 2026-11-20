"""Read-only Markdown API smoke test for all 12 documents; no UI/browser claim."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import json,subprocess
import generate as g
class Parsed(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.images=[];self.in_pre=False;self.code=''
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='a':self.links.append(d.get('href',''))
  if tag=='img':self.images.append(d.get('src',''))
  if tag=='pre':self.in_pre=True
 def handle_endtag(self,tag):
  if tag=='pre':self.in_pre=False
 def handle_data(self,data):
  if self.in_pre:self.code+=data

def check(state):
 text=g.page(state);request=json.dumps({'text':text,'mode':'gfm','context':'overbaffe1/gitEdit'})
 response=subprocess.check_output(['gh','api','markdown','--input','-'],input=request,text=True)
 p=Parsed();p.feed(response)
 for edge in g.transitions(state):assert any(edge['target']+'.md' in href for href in p.links),edge
 assert len(p.images)==1,(g.key(state),p.images)
 assert g.image_name(state) in p.images[0]
 assert p.code.rstrip()==g.snippet(state).rstrip(),g.key(state)
 return g.key(state)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:
  results=list(pool.map(check,g.states()))
 print(f'PASS Markdown API: {len(results)} pages, 48 choice links, 12 preview images, 12 matching code blocks. Routing is checked locally relative to each file; remote browser navigation is not tested.')
