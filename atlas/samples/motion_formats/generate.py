#!/usr/bin/env python3
"""One original 32-frame loop in GIF, APNG and lossless animated WebP.

Requires Pillow with WebP animation support. Does not modify README.
"""
import argparse
import csv
import io
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, __version__ as PILLOW_VERSION, features

ROOT=Path(__file__).resolve().parents[3]
SIZE=(256,192)
COUNT=32
DURATION=80
MATTE=(244,239,226,255)


def rotate(p,t):
    x,y,z=p
    x,z=x*math.cos(t)+z*math.sin(t),-x*math.sin(t)+z*math.cos(t)
    a=.35+.16*math.sin(t)
    return x,y*math.cos(a)-z*math.sin(a),y*math.sin(a)+z*math.cos(a)


def project(p):
    x,y,z=p
    scale=47/(1+z*.13)
    return (128+x*scale,89+y*scale)


def frame(index):
    """Shaded rotating cube and translucent orbital trail, all authored geometry."""
    t=math.tau*index/COUNT
    scale=3
    image=Image.new('RGBA',(SIZE[0]*scale,SIZE[1]*scale),(0,0,0,0))
    draw=ImageDraw.Draw(image)
    def polygon(points,fill,outline=None,width=1):
        pts=[(round(x*scale),round(y*scale)) for x,y in points]
        draw.polygon(pts,fill=fill)
        if outline:
            draw.line(pts+[pts[0]],fill=outline,width=width*scale,joint='curve')
    # Soft shadow is a set of concentric, partially transparent ellipses.
    for i in range(10,0,-1):
        rx=37+i*2;ry=5+i*.5
        draw.ellipse(((128-rx)*scale,(159-ry)*scale,(128+rx)*scale,(159+ry)*scale),fill=(25,61,85,3+(10-i)*2))
    vertices=[rotate((x,y,z),t) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
    faces=[((0,1,2,3),(35,100,139,255)),((4,7,6,5),(70,177,184,255)),
           ((0,4,5,1),(102,211,200,255)),((3,2,6,7),(28,75,115,255)),
           ((0,3,7,4),(45,129,160,255)),((1,5,6,2),(92,189,198,255))]
    # Painter ordering: larger positive z is farther away in this projection.
    for ids,color in sorted(faces,key=lambda item:sum(vertices[i][2] for i in item[0]),reverse=True):
        polygon([project(vertices[i]) for i in ids],color,(221,252,241,255))
    # Semi-transparent orange trail follows a screen-space ellipse.
    for i in range(12):
        a=t-i*.09
        x=128+92*math.cos(a);y=98+46*math.sin(a)
        radius=2.5+(11-i)*.22
        draw.ellipse(((x-radius)*scale,(y-radius)*scale,(x+radius)*scale,(y+radius)*scale),fill=(235,128,72,25+(11-i)*18))
    image=image.resize(SIZE,Image.Resampling.LANCZOS)
    # Canonical RGB under fully transparent pixels; keeps lossless comparisons meaningful.
    pixels=list(image.get_flattened_data())
    image.putdata([p if p[3] else (0,0,0,0) for p in pixels])
    return image


def flatten(image):
    return Image.alpha_composite(Image.new('RGBA',SIZE,MATTE),image).convert('RGB')


def generate(output):
    if not features.check('webp'):
        raise RuntimeError('Pillow needs WebP codec support')
    output.mkdir(parents=True,exist_ok=True)
    frames=[frame(i) for i in range(COUNT)]
    frames[0].save(output/'poster.png')
    flatten(frames[0]).save(output/'poster-matte.png')
    frames[0].save(output/'cube-apng.png',save_all=True,append_images=frames[1:],duration=DURATION,loop=0,disposal=0,blend=0)
    frames[0].save(output/'cube.webp',save_all=True,append_images=frames[1:],duration=DURATION,loop=0,lossless=True,quality=100,method=6,background=(0,0,0,0))
    # A single shared 256-color palette avoids palette changes between frames.
    matte=[flatten(image) for image in frames]
    contact=Image.new('RGB',(SIZE[0]*8,SIZE[1]*4))
    for i,image in enumerate(matte):
        contact.paste(image,((i%8)*SIZE[0],(i//8)*SIZE[1]))
    palette=contact.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    indexed=[image.quantize(palette=palette,dither=Image.Dither.NONE) for image in matte]
    indexed[0].save(output/'cube.gif',save_all=True,append_images=indexed[1:],duration=DURATION,loop=0,optimize=False,disposal=1)
    # Eight evenly spaced samples make a usable static storyboard, not a sprite player.
    strip=Image.new('RGB',(SIZE[0]*4,SIZE[1]*2),MATTE[:3])
    for j,i in enumerate(range(0,COUNT,4)):
        strip.paste(matte[i],((j%4)*SIZE[0],(j//4)*SIZE[1]))
    strip.save(output/'storyboard.png')
    rows=[]
    for name in ('cube.gif','cube-apng.png','cube.webp'):
        with Image.open(output/name) as image:
            rows.append({'file':name,'bytes':(output/name).stat().st_size,'frames':image.n_frames,
                         'duration_ms':COUNT*DURATION,'alpha':'no (matte)' if name.endswith('.gif') else 'yes'})
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    (output/'formats.csv').write_text(stream.getvalue(),encoding='utf-8')
    info={'scope':'One authored loop, not a universal compression benchmark','size':list(SIZE),
          'frames':COUNT,'frame_ms':DURATION,'loop_ms':COUNT*DURATION,'pillow':PILLOW_VERSION,
          'webp_codec':features.version('webp'),'zlib_codec':features.version('zlib'),'files':rows}
    (output/'formats.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/motion-formats')
    generate(parser.parse_args().output)
