"""Encode one eight-second loop and its still from capture.mjs frames (Pillow)."""
import sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def export(directory):
    frames=[]
    for i in range(100):
        with Image.open(directory/f'frame-{i:03}.png') as im: frames.append(im.convert('RGB'))
    if any(f.size!=(704,400) for f in frames): raise ValueError('Expected full-size 704 × 400 plates')
    # Shared palette: no colour flashes on stationary labels between frames.
    sheet=Image.new('RGB',(176,100*25))
    for i,f in enumerate(frames[::4]):sheet.paste(f.resize((176,100)),(0,100*i))
    palette=sheet.quantize(colors=256)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(ROOT/'assets/crystal-theatre.gif',save_all=True,append_images=indexed[1:],duration=80,loop=0,disposal=1,optimize=True)
    frames[26].save(ROOT/'docs/poster.jpg',quality=91,optimize=True,subsampling=0)

if __name__=='__main__':export(Path(sys.argv[1]))
