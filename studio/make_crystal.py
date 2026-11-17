"""Build the theatre's GLB from the paper crystal STL. Python 3 + Pillow; no Blender."""
import io
import json
import math
import struct
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TAU = math.tau


def stone():
    """A UV plate of banded malachite with small copper inclusions, not vertex colours."""
    side = 320
    rgb = bytearray(); finish = bytearray()
    for j in range(side):
        for i in range(side):
            x, y = i / side, j / side
            u = x + .09*math.sin(8*y+1.3) + .023*math.cos(18*x-9*y)
            v = y + .046*math.cos(9*x-1.5) + .016*math.sin(21*y+3*x)
            d = math.hypot(1.04*(u-.13), .80*(v-.30)) + .045*math.sin(7*u+4*v)
            d += .011*math.sin(22*u+13*v)+.004*math.sin(47*u-33*v)
            band = .5 + .5*math.cos(47*d + 2*math.sin(11*v))
            grain = math.sin(540*d)*.052 + math.sin(i*41.2+j*3.7)*.012
            lace = (.5+.5*math.cos(155*d + 1.9*math.sin(9*u)))**7
            k = max(0,min(1,.10+.62*band**1.7+.21*lace+grain))
            a,b = (8,49,47),(105,195,145)
            c = [v+(w-v)*k for v,w in zip(a,b)]
            seam = abs(math.sin(11.2*d+2.2*u+.3*math.cos(19*v)))
            if seam < .038:
                c = [v+(w-v)*(1-seam/.038) for v,w in zip(c,(232,187,108))]
            rgb.extend(round(v) for v in c)
            finish.extend((255, round(78+72*band), 220 if seam < .038 else 35))
    # A separate plate for the *inside* of each leaf: engraved circular scales.
    gold=Image.new('RGB',(side,side),'#996232');draw=ImageDraw.Draw(gold)
    for i in range(side):
        k=.5+.5*math.sin(i*2.1); draw.line((0,i,side,i),fill=(round(149+12*k),round(99+10*k),round(55+6*k)))
    for x,y in [(160,135),(32,305),(290,305)]:
        for r in (5,9,36,40,45,74):draw.ellipse((x-r,y-r,x+r,y+r),outline='#59412b',width=2)
        for i in range(60):
            a=TAU*i/60; r=43 if i%5 else 49
            draw.line((x+39*math.cos(a),y+39*math.sin(a),x+r*math.cos(a),y+r*math.sin(a)), fill='#eaca83',width=2)
    plates=[]
    for im in (Image.frombytes('RGB',(side,side),bytes(rgb)),Image.frombytes('RGB',(side,side),bytes(finish)),gold):
        buf=io.BytesIO();im.save(buf,format='PNG',optimize=True);plates.append(buf.getvalue())
    return plates


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a): return mul(a, 1/math.hypot(*a))
def quat(axis,angle): return (*mul(unit(axis),math.sin(angle/2)), math.cos(angle/2))


class Model:
    def __init__(self):
        self.bin = bytearray()
        self.doc = {'asset': {'version':'2.0','generator':'gitEdit / Malachite No. 01'},
                    'scene':0,'scenes':[{'nodes':[0]}], 'nodes':[{'name':'Capsule','children':[]}],
                    'meshes':[], 'accessors':[], 'bufferViews':[]}

    def store(self, raw):
        self.bin.extend(b'\0'*(-len(self.bin)%4))
        views=self.doc['bufferViews']; views.append({'buffer':0,'byteOffset':len(self.bin),'byteLength':len(raw)})
        self.bin.extend(raw);return len(views)-1

    def floats(self, rows):
        size = len(rows[0]); typ={1:'SCALAR',2:'VEC2',3:'VEC3',4:'VEC4'}[size]
        raw = b''.join(struct.pack('<'+'f'*size,*r) for r in rows)
        acc=self.doc['accessors']; acc.append({'bufferView':self.store(raw),'componentType':5126,'type':typ,
                                               'count':len(rows),'min':list(map(min,zip(*rows))),'max':list(map(max,zip(*rows)))})
        return len(acc)-1

    def primitive(self, triangles, material, uv=None):
        pos=[]; normals=[]
        for a,b,c in triangles:
            pos.extend((a,b,c));normals.extend([unit(cross(sub(b,a),sub(c,a)))]*3)
        attrs={'POSITION':self.floats(pos),'NORMAL':self.floats(normals)}
        if uv: attrs['TEXCOORD_0']=self.floats(uv)
        return {'attributes':attrs,'material':material}

    def piece(self,name,primitives,**transform):
        nodes=self.doc['nodes'];meshes=self.doc['meshes']
        nodes[0]['children'].append(len(nodes));nodes.append({'mesh':len(meshes),'name':name,**transform})
        meshes.append({'primitives':primitives});return len(nodes)-1

    def save(self,path):
        self.doc['buffers']=[{'byteLength':len(self.bin)}]
        text=json.dumps(self.doc,separators=(',',':')).encode();text+=b' '*(-len(text)%4)
        self.bin.extend(b'\0'*(-len(self.bin)%4))
        payload=struct.pack('<I4s',len(text),b'JSON')+text+struct.pack('<I4s',len(self.bin),b'BIN\0')+self.bin
        path.write_bytes(struct.pack('<4sII',b'glTF',2,len(payload)+12)+payload)


def make():
    m=Model(); d=m.doc
    d.update(images=[{'bufferView':m.store(b),'mimeType':'image/png','name':name} for b,name in zip(stone(),['Veins','Polish','Engraving'])],
             textures=[{'source':i} for i in range(3)],extensionsUsed=['KHR_materials_clearcoat'])
    d['materials']=[{'name':'Polished malachite','pbrMetallicRoughness':{'baseColorTexture':{'index':0},'metallicRoughnessTexture':{'index':1},'metallicFactor':.75,'roughnessFactor':.89},
                     'extensions':{'KHR_materials_clearcoat':{'clearcoatFactor':.7,'clearcoatRoughnessFactor':.22}}},
                    {'name':'Brushed brass','pbrMetallicRoughness':{'baseColorFactor':[.79,.51,.19,1],'metallicFactor':.76,'roughnessFactor':.29}},
                    {'name':'Honey amber','pbrMetallicRoughness':{'baseColorFactor':[.96,.41,.065,1],'metallicFactor':.27,'roughnessFactor':.22},'emissiveFactor':[.13,.034,.002]}]
    d['materials'].append({'name':'Engraved liner','pbrMetallicRoughness':{'baseColorTexture':{'index':2},'metallicFactor':.55,'roughnessFactor':.38}})
    times=[(8*i/40,) for i in range(41)]; clock=m.floats(times)
    clip={'name':'Размыкание','samplers':[],'channels':[]};d['animations']=[clip]
    def track(node,path,values):
        clip['channels'].append({'sampler':len(clip['samplers']),'target':{'node':node,'path':path}})
        clip['samplers'].append({'input':clock,'output':m.floats(values),'interpolation':'LINEAR'})
    track(0,'rotation',[quat((0,1,0),.24+TAU*t/8) for t, in times])
    verts=[]
    for line in (ROOT/'atlas/samples/crystal.stl').read_text().splitlines():
        cols=line.split()
        if cols[:1]==['vertex']:
            x,y,z=map(float,cols[1:]);verts.append((x/18,(z-17)/18,-y/18))  # Z-up STL → Y-up glTF
    for i in range(0,len(verts),3):
        a,b,c=tri=verts[i:i+3]; center=mul(add(add(a,b),c),1/3);n=unit(cross(sub(b,a),sub(c,a)))
        edge=[mul(sub(p,center),.99) for p in tri]; inset=[mul(p,.95) for p in edge]; back=[sub(p,mul(n,.066)) for p in edge]
        rim=[]
        for k in range(3):
            j=(k+1)%3
            rim.extend([(edge[k],edge[j],inset[j]),(edge[k],inset[j],inset[k]),(edge[k],back[k],back[j]),(edge[k],back[j],edge[j])])
        dx=i%5*.073; uv=[(.45+dx,.96),(.01+dx,.055),(.84+dx,.12)]
        node=m.piece(f'Leaf_{i//3+1}',[m.primitive([inset],0,uv),m.primitive(rim,1),m.primitive([back[::-1]],3,[(.96,.96),(.04,.96),(.5,.03)])],translation=center)
        opens=[(.5-.5*math.cos(TAU*t/8))**1.1 for t, in times]
        track(node,'translation',[add(center,mul(n,.70*k)) for k in opens]);track(node,'rotation',[quat(sub(c,b),.57*k) for k in opens])
    # Two tilted brass hoops and an amber seed, revealed when the eight plates open.
    for j,(r,tube,axis) in enumerate([(.49,.023,(1,.25,.55)),(.39,.016,(.34,1,.76))]):
        def point(i,k):
            a=TAU*i/56; b=TAU*k/8;return ((r+tube*math.cos(b))*math.cos(a),tube*math.sin(b),(r+tube*math.cos(b))*math.sin(a))
        ts=[]
        for i in range(56):
            for k in range(8):
                a,b,c,e=point(i,k),point(i+1,k),point(i+1,k+1),point(i,k+1);ts.extend([(a,c,b),(a,e,c)])
        node=m.piece('Brass_orbit_'+str(j+1),[m.primitive(ts,1)]);track(node,'rotation',[quat(axis,.63+j+TAU*t/8) for t, in times])
    petals=[]
    for i in range(8):
        a,b=TAU*i/8,TAU*(i+1)/8;p=(.24*math.cos(a),0,.24*math.sin(a));q=(.24*math.cos(b),0,.24*math.sin(b))
        petals.extend([((0,.39,0),q,p),((0,-.31,0),p,q)])
    m.piece('Amber_seed',[m.primitive(petals,2)]); m.save(ROOT/'docs/malachite.glb')


if __name__=='__main__': make()
