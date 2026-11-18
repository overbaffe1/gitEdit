#!/usr/bin/env python3
"""Own pixel-art lighthouse, ten encoded fragments and actual recovery trials."""
import argparse
import hashlib
import io
import itertools
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
import codec

ROOT=Path(__file__).resolve().parents[3]
PALETTE=['#102731','#20424d','#36717b','#7db3b6','#f5d19a','#c67e55','#faf0cf','#40525d']


def artwork():
    im=Image.new('RGB',(96,64),PALETTE[0]);d=ImageDraw.Draw(im)
    # Original small night coast; all coordinates defined here, no external artwork or font.
    d.polygon([(39,18),(91,5),(91,30)],fill=PALETTE[1])
    d.polygon([(39,18),(91,12),(91,24)],fill='#3d554f')
    d.ellipse((70,4,79,13),fill=PALETTE[4]);d.ellipse((67,3,76,12),fill=PALETTE[0])
    for x,y in [(8,7),(19,15),(49,5),(58,13),(84,6),(7,25),(54,27),(89,37)]:d.point((x,y),fill=PALETTE[3])
    d.rectangle((0,39,95,63),fill=PALETTE[1])
    for y in range(42,64,4):
        for x in range((y*7)%13,96,18):d.line((x,y,x+8,y),fill=PALETTE[2])
    d.polygon([(10,53),(16,44),(25,42),(29,37),(44,39),(48,46),(59,51),(61,55)],fill=PALETTE[7])
    d.polygon([(25,42),(29,22),(40,22),(44,43)],fill=PALETTE[6])
    d.polygon([(27,31),(42,32),(42,36),(26,35)],fill=PALETTE[5])
    d.rectangle((28,14,41,22),fill=PALETTE[4]);d.line((30,14,30,21),fill=PALETTE[0]);d.line((39,14,39,21),fill=PALETTE[0])
    d.polygon([(26,14),(34,8),(43,14)],fill=PALETTE[5]);d.line((34,8,34,5),fill=PALETTE[4])
    d.rectangle((32,38,36,43),fill=PALETTE[0]);d.rectangle((32,24,34,27),fill=PALETTE[2])
    for x,y,w in [(38,47,5),(41,51,9),(44,55,12),(47,59,16)]:d.line((x,y,x+w,y),fill=PALETTE[4])
    return im


def pack_zip(path,entries):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,payload in sorted(entries.items()):
            info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,payload)


def swatch(record):
    block=codec.validate(record);width=16;height=(len(block)+width-1)//width
    im=Image.new('RGB',(width,height),PALETTE[0]);pixels=im.load()
    for i,b in enumerate(block):pixels[i%width,i//width]=(30+b//3,57+b//2,70+b//2)
    return im.resize((64,64),Image.Resampling.NEAREST)


def plate(records,indices):
    im=Image.new('RGB',(1000,580),PALETTE[0]);d=ImageDraw.Draw(im);large=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16)
    d.text((26,18),'THE LIGHTHOUSE / ANY SIX FRAGMENTS BRING IT BACK',font=large,fill=PALETTE[4])
    d.text((26,54),'SYSTEMATIC (10,6) ERASURE CODE / EXACT FILE BYTES, NOT IMAGE INPAINTING',font=small,fill=PALETTE[3])
    for i,record in enumerate(records):
        x=26+(i%5)*93;y=140+(i//5)*150
        if i in indices:im.paste(swatch(record),(x,y))
        else:
            d.rectangle((x,y,x+63,y+63),outline=PALETTE[2]);d.line((x,y,x+63,y+63),fill=PALETTE[5],width=2);d.line((x+63,y,x,y+63),fill=PALETTE[5],width=2)
        d.text((x,y+72),f'{i+1:02} '+('DATA' if i<6 else 'PAR'),font=small,fill=PALETTE[3] if i in indices else PALETTE[5])
    d.text((26,104),'ENCODED BYTES / NOT PIECES OF THE PICTURE',font=small,fill=PALETTE[4])
    if len(indices)>=6:
        recovered=codec.decode([records[i] for i in indices]);picture=Image.open(io.BytesIO(recovered)).convert('RGB')
        im.paste(picture.resize((432,288),Image.Resampling.NEAREST),(542,140))
        d.text((542,104),'RECOVERED PNG / SHA-256 MATCH',font=small,fill=PALETTE[4])
        d.text((542,450),f'{len(indices)}/10 AVAILABLE: EXACT RECOVERY',font=small,fill=PALETTE[4])
    else:
        d.rectangle((542,140,973,427),outline=PALETTE[2])
        d.text((565,245),'NOT ENOUGH INDEPENDENT BLOCKS',font=small,fill=PALETTE[5])
        d.text((542,450),f'{len(indices)}/10 AVAILABLE: REFUSE TO GUESS',font=small,fill=PALETTE[5])
    d.text((26,518),'LOSE FOUR: OK. LOSE FIVE: NO GUARANTEE FOR AN ARBITRARY FILE.',font=small,fill=PALETTE[3])
    d.text((26,549),'REDUNDANCY IS NOT ENCRYPTION / CHECKSUMS ARE NOT SIGNATURES.',font=small,fill=PALETTE[3])
    return im


def generate(output):
    output.mkdir(parents=True,exist_ok=True);(output/'fragments').mkdir(exist_ok=True)
    artwork().save(output/'source.png');payload=(output/'source.png').read_bytes();records=codec.encode(payload)
    files={}
    for i,r in enumerate(records):
        data=(json.dumps(r,indent=2)+'\n').encode();name=f'fragment-{i+1:02}.json';(output/'fragments'/name).write_bytes(data);files[name]=data
    pack_zip(output/'fragments.zip',files)
    links=['# Десять фрагментов маяка', '', 'Нужны любые шесть **различных целых** фрагментов. Номера в JSON начинаются с нуля; здесь — с единицы.', '']
    for i in range(10):
        name=f'fragment-{i+1:02}.json'
        links.append(f'- [{i+1:02} / '+('data' if i<6 else 'parity')+f'](fragments/{name})')
    links+=['', '[Все фрагменты ZIP](fragments.zip) · [Описание формата и декодер](../../atlas/shards.md)', '']
    (output/'fragments.md').write_text('\n'.join(links))
    # Reload published fragments; neither the figure nor decoder reads source.png again.
    records=[json.loads((output/'fragments'/f'fragment-{i+1:02}.json').read_text()) for i in range(10)]
    digest=hashlib.sha256(payload).hexdigest();lines=['indices_1based,sha256,exact_match']
    for indices in itertools.combinations(range(10),6):
        recovered=codec.decode([records[i] for i in indices]);assert recovered==payload
        lines.append('"'+' '.join(str(i+1) for i in indices)+'",'+hashlib.sha256(recovered).hexdigest()+',true')
    (output/'recoveries.csv').write_text('\n'.join(lines)+'\n')
    selections=[list(range(i,10)) for i in range(6)]+[[0,3,6,7,8,9],[1,2,4,5,7,8],[0,2,4,6,8],[0,2,4,6,8,9],list(range(10))]
    frames=[plate(records,indices) for indices in selections]
    frames[6].save(output/'poster.png');plate(records,[0,2,4,6,8]).save(output/'insufficient.png')
    sample=Image.new('RGB',(1000,580*2));sample.paste(frames[0],(0,0));sample.paste(frames[5],(0,580))
    palette=sample.quantize(colors=192,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(output/'recover.gif',save_all=True,append_images=indexed[1:],loop=0,duration=[850]*len(frames),disposal=2,optimize=False)
    live=(Path(__file__).with_name('bench-template.html').read_text().replace('__RECORDS__',json.dumps(records,separators=(',',':')))).encode()
    (output/'bench.html').write_bytes(live);pack_zip(output/'bench.zip',{'bench.html':live})
    facts={'code':'systematic (10,6) Vandermonde over GF(256), polynomial 0x11d, evaluation points 1..10',
           'original_bytes':len(payload),'sha256':digest,'block_bytes':len(codec.validate(records[0])),
           'raw_coded_bytes':sum(len(codec.validate(r)) for r in records),'fragment_json_bytes':sum(len(v) for v in files.values()),
           'all_six_subsets_tested':210,'all_exact':True,'frames':len(frames),'animation_indices_1based':[[i+1 for i in s] for s in selections],
           'limits':'known erasures only; no unknown-error correction, encryption, signatures or cross-library wire compatibility'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps(facts,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'assets/shards');generate(parser.parse_args().output)
