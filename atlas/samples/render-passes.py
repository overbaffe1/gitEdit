"""Render aligned passes of crystal.stl and their GIF wipe.

Run with Python 3,
Pillow >= 10 and the DejaVu Sans fonts. --stamp prints the projection in text
cells for the README; no network or 3D engine needed.
"""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parents[1] / 'assets'
W, H, SS = 576, 276, 2


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def unit(a):
    return tuple(x/math.sqrt(dot(a, a)) for x in a)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def mesh():
    camera = unit((.28, -1, .22))
    right = unit(cross((0, 0, 1), camera))
    up = cross(camera, right)
    faces = []
    for line in (HERE / 'crystal.stl').read_text().splitlines():
        cols = line.split()
        if cols[:2] == ['facet', 'normal']:
            normal, tri = tuple(map(float, cols[2:])), []
        elif cols[:1] == ['vertex']:
            x, y, z = map(float, cols[1:]); p = (x, y, z-17)
            tri.append((W/2+6.4*dot(p, right), H/2-6.4*dot(p, up), dot(p, camera)))
        elif cols[:1] == ['endfacet']:
            faces.append((normal, tri))
    return sorted(faces, key=lambda f: sum(p[2] for p in f[1])), camera


def draw_pass(lit):
    paper, rule, ink = ('#152c2b', '#39514b', '#e4eddd') if lit else ('#f8f1df', '#d4cbb7', '#27454b')
    im = Image.new('RGB', (W*SS, H*SS), paper)
    d = ImageDraw.Draw(im)
    def pts(pp): return [(round(x*SS), round(y*SS)) for x, y in pp]
    def line(pp, col, w=1): d.line(pts(pp), fill=col, width=round(w*SS))
    def label(x,y,s,size=13,bold=False):
        font = ImageFont.truetype('DejaVuSansMono'+('-Bold' if bold else '')+'.ttf', size*SS)
        d.text((x*SS,y*SS),s,font=font,fill=ink,anchor='lt')
    if not lit:
        for x in range(0,W,16): line([(x,0),(x,H)],rule,.5)
        for y in range(0,H,16): line([(0,y),(W,y)],rule,.5)
    else:
        for radius in range(12,100,14):
            d.ellipse(pts([(W/2-radius,247-radius*.12),(W/2+radius,247+radius*.12)]),outline=rule,width=1)
    for x,y in [(16,18),(W-16,18),(16,H-18),(W-16,H-18)]:
        line([(x-4,y),(x+4,y)],ink); line([(x,y-4),(x,y+4)],ink)
    label(31,18,'GITEDIT / MESH',12,True)
    label(W-114,H-28, 'PASS 02' if lit else 'PASS 01')
    if lit: label(W-100,50,'СВЕТ',23,True)
    else: label(31,50,'СЕТКА',23,True)
    faces, camera = mesh(); light = unit((.65,-.40,.88))
    for normal, tri in faces:
        poly = [p[:2] for p in tri]; visible = dot(normal,camera)>0
        if lit and visible:
            k = max(0,dot(normal,light))**.8
            lo, hi = ((56,85,86),(251,190,126)) if normal[0]>.4 else ((33,77,81),(172,234,197))
            fill = tuple(round(a+(b-a)*k) for a,b in zip(lo,hi))
            # The same triangle mask clips both the gradient and the softbox reflection.
            mask = Image.new('1',im.size); ImageDraw.Draw(mask).polygon(pts(poly), fill=1)
            surface = Image.new('RGB',im.size,fill); paint = ImageDraw.Draw(surface)
            top, bottom = min(y for _,y in poly), max(y for _,y in poly)
            for y in range(math.floor(top*SS), math.ceil(bottom*SS)+1):
                t = (y/SS-top)/(bottom-top)
                rgb = tuple(min(255,round(c*(1.18-.42*t)+7)) for c in fill)
                paint.line((0,y,W*SS,y), fill=rgb)
            shine = ImageDraw.Draw(surface,'RGBA'); cy = 132+60*normal[0]
            for offset, width, opacity in [(0,12,46),(18,3,80)]:
                cy0 = cy+offset
                band = [(160,cy0+42),(410,cy0-44),(410,cy0-44+width),(160,cy0+42+width)]
                shine.polygon(pts(band),fill=(229,252,222,opacity))
            im.paste(surface,(0,0),mask); line(poly+[poly[0]],'#91b9a8' if normal[2]>0 else '#385654',1)
        elif not lit:
            line(poly+[poly[0]],ink if visible else '#a3ada0',2 if visible else 1)
    return im.resize((W,H),Image.Resampling.LANCZOS)


def stamp():
    faces, camera = mesh(); visible = [(n,t) for n,t in faces if dot(n,camera)>0]
    xs = [p[0] for _,tri in faces for p in tri]; ys = [p[1] for _,tri in faces for p in tri]
    for j in range(16):
        row = []
        for i in range(20):
            x = min(xs)+(max(xs)-min(xs))*(i+.5)/20; y = min(ys)+(max(ys)-min(ys))*(j+.5)/16
            ch = ' '
            for n,t in visible:
                sides = [(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0]) for a,b in zip(t,t[1:]+t[:1])]
                if min(sides)>=0 or max(sides)<=0:
                    ch = '░▒▓█'[round(3*max(0,dot(n,unit((.65,-.40,.88)))))]
            row.append(ch)
        print(''.join(row).rstrip())


def export():
    wire, light = draw_pass(False), draw_pass(True)
    wire.save(ASSETS/'crystal-wire.png', optimize=True); light.save(ASSETS/'crystal-light.png',optimize=True)

    def wipe(f):
        x = round(W*f); im = light.copy()
        if x: im.paste(wire.crop((0,0,x,H)), (0,0))
        if 0<x<W: ImageDraw.Draw(im).line((x,0,x,H),fill='#cd664d',width=2)
        return im
    # Start halfway across: the first frame is useful even when autoplay is off.
    poster = wipe(.5); poster.save(ASSETS/'crystal-wipe.png',optimize=True)
    palette_sheet = Image.new('RGB',(W,H*2)); palette_sheet.paste(wire); palette_sheet.paste(light,(0,H))
    palette = palette_sheet.quantize(colors=192)
    stops = range(32); amounts = [.5+.5*math.sin(i*math.tau/32) for i in stops]
    frames = [wipe(f).quantize(palette=palette,dither=Image.Dither.NONE) for f in amounts]
    frames[0].save(ASSETS/'crystal-wipe.gif',save_all=True,append_images=frames[1:],loop=0,disposal=1,
                   duration=[1000 if i in (0,8,24) else 90 for i in stops],optimize=True)


if __name__ == '__main__':
    stamp() if '--stamp' in sys.argv else export()
