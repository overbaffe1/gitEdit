"""Unfold the gallery's octahedron at its real hinges. No 3D engine required.

python3 atlas/samples/night_shift/crystal.py
The cutting sheet is pure vector; the film export needs Pillow and DejaVu Sans.
"""
from collections import defaultdict
from math import atan2, cos, sin, sqrt, pi
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'assets/night-shift'
# Four upper faces form a fan; each one carries one lower face on its rim.
PARENT = (None, 0, 0, 2, 2, 4, 4, 6)
COLORS = ('#9edbca', '#e6b78f', '#76c6b7', '#f1c599', '#b7e7ce', '#df9979', '#8acdbe', '#f9cc9b')


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def unit(a): return mul(a, 1/sqrt(dot(a,a)))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def normal(face): return unit(cross(sub(face[1],face[0]),sub(face[2],face[0])))


class Net:
    def __init__(self, source=HERE.parent/'crystal.stl'):
        vertices = [tuple(map(float,line.split()[1:])) for line in source.read_text().splitlines() if line.lstrip().startswith('vertex ')]
        self.faces = [vertices[i:i+3] for i in range(0,len(vertices),3)]
        if len(self.faces) != len(PARENT):
            raise ValueError('This net is cut for the eight faces of crystal.stl')
        self.hinges = {}
        for i,parent in enumerate(PARENT):
            if parent is not None:
                a,b = sorted(set(self.faces[i]) & set(self.faces[parent]))
                axis = unit(sub(b,a)); old, new = normal(self.faces[i]), normal(self.faces[parent])
                self.hinges[i] = a,axis,atan2(dot(axis,cross(old,new)), dot(old,new))

    def pose(self, openness):
        def point(i, p):
            while i in self.hinges:
                a,axis,radians = self.hinges[i]; angle = openness*radians
                v = sub(p,a)
                # Rodrigues rotation about the actual shared edge; apply hinges from leaf to root.
                p = add(a,add(add(mul(v,cos(angle)),mul(cross(axis,v),sin(angle))),mul(axis,dot(axis,v)*(1-cos(angle)))))
                i = PARENT[i]
            return p
        return [[point(i,p) for p in face] for i,face in enumerate(self.faces)]

    def project(self, openness):
        c = unit(add(mul(unit((.85,.24,.52)),1-openness),mul(normal(self.faces[0]),openness)))
        right = unit(cross((0,0,1),c)); up = cross(c,right)
        angle = pi * openness / 2
        def view(p):
            x,y = dot(p,right),-dot(p,up)
            return (x*cos(angle)-y*sin(angle), x*sin(angle)+y*cos(angle), dot(p,c))
        return [[view(p) for p in face] for face in self.pose(openness)]


def fit(faces, box):
    pts = [p for face in faces for p in face]; x0,y0,x1,y1 = box
    xs,ys = [p[0] for p in pts],[p[1] for p in pts]
    scale = min((x1-x0)/(max(xs)-min(xs)),(y1-y0)/(max(ys)-min(ys)))
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    return [[((p[0]-cx)*scale+(x0+x1)/2, (p[1]-cy)*scale+(y0+y1)/2) for p in face] for face in faces]


def cutting_sheet(net):
    flat = fit(net.project(1), (17,31,280,177))  # viewBox units are millimetres
    edges = defaultdict(list)
    for i,face in enumerate(net.faces):
        for j in range(3): edges[tuple(sorted((face[j],face[(j+1)%3])))].append((i,j))
    fills, rules, labels = [], [], []
    fmt = lambda p: f'{p[0]:.2f},{p[1]:.2f}'
    def line(a,b,fold=False):
        dash = ' stroke-dasharray="1.8 1.15"' if fold else ''
        rules.append(f'<path d="M{fmt(a)}L{fmt(b)}"{dash}/>')
    def text(p, value, size):
        labels.append(f'<text x="{p[0]:.2f}" y="{p[1]+size*.34:.2f}" font-size="{size}">{value}</text>')
    for i,tri in enumerate(flat):
        fills.append(f'<polygon fill="{COLORS[i]}" points="{" ".join(map(fmt,tri))}"/>')
        text(tuple(sum(p[k] for p in tri)/3 for k in (0,1)), f'{i+1:02}', 5.2)
    seams = 0
    for adjacent in edges.values():
        (i,j),(k,l) = adjacent
        if PARENT[i] == k or PARENT[k] == i:
            line(flat[i][j],flat[i][(j+1)%3], True)
            continue
        tag = 'ABCDE'[seams]; seams += 1
        for side,(face,j) in enumerate(adjacent):
            a,b,c = flat[face][j],flat[face][(j+1)%3],flat[face][(j+2)%3]
            v = sub(b,a); u = unit(v); n = (-u[1],u[0]); mid = mul(add(a,b),.5)
            if dot(n,sub(c,mid))>0: n = mul(n,-1)
            text(sub(mid,mul(n,3.5)),tag,3.1)
            if side == 0:
                outer1,outer2 = add(add(a,mul(u,4.2)),mul(n,4.4)),add(sub(b,mul(u,4.2)),mul(n,4.4))
                fills.append(f'<polygon fill="#ede0c7" points="{" ".join(map(fmt,(a,outer1,outer2,b)))}"/>')
                line(a,outer1);line(outer1,outer2);line(outer2,b);line(a,b,True)
            else: line(a,b)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">Кристалл · выкройка А4</title><desc id="d">Восемь пронумерованных граней, семь сгибов между ними, пять клеевых клапанов. Совмести буквы от A до E.</desc>
<rect width="297" height="210" fill="#fffaf0"/><g fill="#203b41" font-family="sans-serif"><text x="10" y="11" font-family="monospace" font-size="3.8">НОЧНАЯ СМЕНА / 01</text><text x="10" y="22" font-size="8" font-weight="bold">Кристалл · раскрой</text><text x="286" y="15" text-anchor="end" font-size="4">А4 / 100 %</text></g>
<g>{''.join(fills)}</g><g fill="none" stroke="#254047" stroke-width=".36" stroke-linejoin="round">{''.join(rules)}</g>
<g font-family="monospace" font-weight="bold" text-anchor="middle" fill="#244149">{''.join(labels)}</g>
<g stroke="#254047" stroke-width=".6"><path d="M10 191h13"/><path d="M28 191h13" stroke-dasharray="1.8 1.15"/></g><text x="10" y="201" font-family="sans-serif" font-size="4.1">Контур — резать. Пунктир — сгибать. Склей одинаковые буквы.</text>
<path d="M254 194v4m0-2h30m0-2v4" stroke="#254047" fill="none" stroke-width=".6"/><text x="269" y="203" text-anchor="middle" font-family="monospace" font-size="4">30 мм</text></svg>\n'''


def film(net):
    from PIL import Image, ImageDraw, ImageFont
    W,H,S = 620,268,2
    paper,ink,line = '#eee4cc','#193945','#81918a'
    base = Image.new('RGB',(W*S,H*S),paper); d=ImageDraw.Draw(base)
    def pts(poly): return [(round(x*S),round(y*S)) for x,y in poly]
    def rect(d, box, fill): d.rectangle(tuple(round(v*S) for v in box),fill=fill)
    def write(d,x,y,value,size,color=ink,bold=False,mono=False):
        name=('DejaVuSansMono' if mono else 'DejaVuSans')+('-Bold' if bold else '')+'.ttf'
        d.text((x*S,y*S), value,font=ImageFont.truetype(name,size*S),fill=color,anchor='lt')
    for x in range(8,420,12):
        for y in range(48,H-13,12): rect(d,(x,y,x+.7,y+.7),'#b8b6a5')
    rect(d,(424,0,W,H),'#153744'); rect(d,(0,0,424,33),'#203e48')
    write(d,14,8,'01  /  СБОРОЧНЫЙ СТОЛ',14,'#f4e7c9',True,True)
    write(d,442,21,'ЛИСТ  01—А',14,'#a2cdbd',True,True)
    write(d,441,55,'8 граней',27,'#f4e7c9',True)
    write(d,442,94,'7 сгибов',18,'#e8c39a');write(d,442,122,'5 швов',18,'#e8c39a')
    rect(d,(442,177,601,178),'#6d8886');write(d,442,192,'ПОЛОЖЕНИЕ',12,'#b1cfc5',True,True)
    def frame(t):
        im=base.copy();d=ImageDraw.Draw(im);pro=net.project(t);flat=fit(pro,(22,45,400,249));pose=net.pose(t)
        for i in sorted(range(8),key=lambda i:sum(p[2] for p in pro[i])):
            tri=flat[i];n=normal(pose[i]); shade=.73+.27*abs(dot(n,unit((.24,.42,.87))))
            rgb=tuple(round(int(COLORS[i][j:j+2],16)*shade) for j in (1,3,5))
            d.polygon(pts(tri),fill=rgb)
            def between(a,b,k): return add(a,mul(sub(b,a),k))
            for k in (.62,.68,.73):
                a,b=between(tri[0],tri[1],k),between(tri[0],tri[2],k)
                d.line(pts((between(a,b,.13),between(a,b,.72))),fill=tuple((2*c+230)//3 for c in rgb),width=S)
            d.line(pts(tri+[tri[0]]),fill=ink,width=2*S,joint='curve')
        write(d,442,215,'ЛИСТ' if t>.88 else 'ОБЪЁМ' if t<.12 else 'СГИБ',22,'#f3cc9d',True,True)
        rect(d,(442,248,600,251),'#68837f');dotx=442+156*(1-t);rect(d,(dotx,245,dotx+4,254),'#f4dc9e')
        return im.resize((W,H),Image.Resampling.LANCZOS)
    steps=24
    forward=[frame(.5-.5*cos(pi*i/steps)) for i in range(steps+1)]
    # Calibrate the palette with flat, intermediate and closed poses; never dither moving edges.
    swatch=Image.new('RGB',(W,H*3));
    for j,i in enumerate((0,steps//2,steps)): swatch.paste(forward[i],(0,H*j))
    palette=swatch.quantize(colors=128); indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in forward]
    frames=indexed+indexed[-2:0:-1]; durations=[85]*len(frames);durations[0]=1100;durations[steps]=1450
    frames[0].save(OUT/'fold.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True,disposal=1)
    # The reduced-motion alternative shows both endpoints, not a frozen intermediate pose.
    still=Image.new('RGB',(W,H),paper)
    for i,t in enumerate((1.,0.)):
        rect_side=frame(t).crop((0,34,424,268))
        rect_side.thumbnail((W//2,195),Image.Resampling.LANCZOS)
        still.paste(rect_side,(i*(W//2),(H+41-rect_side.height)//2))
    d=ImageDraw.Draw(still);d.rectangle((0,0,W,41),fill=ink)
    font=ImageFont.truetype('DejaVuSansMono-Bold.ttf',16);d.text((14,10),'ЛИСТ  /  8 ГРАНЕЙ',font=font,fill=paper);d.text((326,10),'ОБЪЁМ  /  5 ШВОВ',font=font,fill=paper)
    still.save(OUT/'fold-still.png',optimize=True)


if __name__ == '__main__':
    n=Net(); (OUT/'crystal-net.svg').write_text(cutting_sheet(n),encoding='utf-8'); film(n)
