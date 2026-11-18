#!/usr/bin/env python3
"""Own virtual metamer pair and reproducible spectral exhibit. No real pigments claimed."""
import argparse
import csv
import json
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import model

ROOT=Path(__file__).resolve().parents[3]
SAMPLE=Path(__file__).resolve().parent


def graph(draw,rect,values,colors,maximum=1):
    x,y,w,h=rect;draw.rectangle((x,y,x+w,y+h),fill='#10232e',outline='#4c6b77')
    for fraction in (.25,.5,.75):draw.line((x,y+h*fraction,x+w,y+h*fraction),fill='#294451')
    for curve,color in zip(values,colors):
        points=[(x+i*w/(len(curve)-1),y+h*(1-value/maximum)) for i,value in enumerate(curve)]
        draw.line(points,fill=color,width=3)


def plate(standards,pair,mix):
    image=Image.new('RGB',(1000,680),'#152934');d=ImageDraw.Draw(image);large=ImageFont.load_default(size=22);small=ImageFont.load_default(size=15)
    d.text((26,20),'SAME COLOUR / DIFFERENT SPECTRA',font=large,fill='#efd09a')
    d.text((26,54),'VIRTUAL REFLECTANCES / CIE 1931 2 DEG / BRADFORD -> D65 / sRGB PREVIEW',font=small,fill='#bed0cc')
    day=model.evaluate(standards,pair,0);current=model.evaluate(standards,pair,mix)
    for x,result,label in [(26,day,'D65 / MATCHING XYZ'),(526,current,f'MIX: {round(mix*100):3}% A / CHANGING LIGHT')]:
        d.text((x,102),label,font=small,fill='#efd09a')
        for i,rgb in enumerate(result['rgb8']):
            d.rectangle((x+i*227,138,x+i*227+210,298),fill=tuple(rgb))
            d.text((x+i*227,313),f'{"AB"[i]} / '+','.join(map(str,rgb)),font=small,fill='#bed0cc')
        d.text((x,349),f'Delta E76 = {result["delta_e76"]:.5f}',font=small,fill='#efd09a')
    d.text((26,398),'REFLECTANCE / 0..1 / THE TWO MATERIALS NEVER CHANGE',font=small,fill='#efd09a')
    graph(d,(26,430,600,165),pair,['#efd09a','#53bac3'])
    light=np.array(current['illuminant']);light/=light.max()
    graph(d,(670,430,300,165),[light],['#bed0cc'])
    d.text((670,405),'CURRENT LAMP / OWN MAX=1',font=small,fill='#bed0cc')
    d.text((26,606),'380 nm                         A: AMBER / B: CYAN                          780 nm',font=small,fill='#bed0cc')
    d.text((26,642),'MODEL ONLY: SCREEN DOES NOT REPRODUCE THESE SPECTRA. NO PHYSICAL INKS OR PRINT TEST.',font=small,fill='#bed0cc')
    return image


def generate(output):
    output.mkdir(parents=True,exist_ok=True);standards=model.load();pair=model.design(standards)
    # Publish with enough precision, then compute every exhibit from the rounded CSV alone.
    with (output/'spectra.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['wavelength_nm','x_bar','y_bar','z_bar','D65','A','reflectance_a','reflectance_b'])
        for i,wavelength in enumerate(standards['wavelength_nm']):writer.writerow([wavelength,*standards['cmf'][i],standards['D65'][i],standards['A'][i],f'{pair[0][i]:.15f}',f'{pair[1][i]:.15f}'])
    with (output/'spectra.csv').open() as f:rows=list(csv.DictReader(f))
    pair=[[float(row[key]) for row in rows] for key in ('reflectance_a','reflectance_b')]
    with (output/'measurements.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['mix_A','adapt','delta_e76','A_R','A_G','A_B','B_R','B_G','B_B','gamut_clipped'])
        for adapt in (True,False):
            for mix in np.linspace(0,1,101):
                result=model.evaluate(standards,pair,float(mix),adapt);writer.writerow([f'{mix:.2f}',adapt,f'{result["delta_e76"]:.12f}',*result['rgb8'][0],*result['rgb8'][1],result['gamut_clipped']])
    plate(standards,pair,1).save(output/'poster.png');plate(standards,pair,0).save(output/'daylight.png')
    fractions=list(np.linspace(0,1,21))+list(np.linspace(.95,.05,19))
    frames=[plate(standards,pair,float(mix)) for mix in fractions]
    sheet=Image.new('RGB',(1000,1360));sheet.paste(frames[0],(0,0));sheet.paste(frames[20],(0,680))
    palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    durations=[100]*len(frames);durations[0]=1500;durations[20]=1500
    indexed[0].save(output/'illuminants.gif',save_all=True,append_images=indexed[1:],loop=0,duration=durations,disposal=2,optimize=False)
    cmf=np.array(standards['cmf']);weights=np.full(len(cmf),5.);weights[[0,-1]]*=.5
    lights=[np.array(standards[key]) for key in ('D65','A')];lights=[light/np.sum(light*cmf[:,1]*weights) for light in lights]
    config={'cmf':standards['cmf'],'day':lights[0].tolist(),'lamp':lights[1].tolist(),'reflectances':pair,
            'bradford':model.BRADFORD.tolist(),'inverse_bradford':np.linalg.inv(model.BRADFORD).tolist(),
            'white':model.D65_WHITE.tolist(),'xyz_to_rgb':model.XYZ_TO_RGB.tolist()}
    live=(SAMPLE/'bench-template.html').read_text().replace('__CONFIG__',json.dumps(config,separators=(',',':'))).encode()
    license=(SAMPLE/'COLOUR-LICENSE.txt').read_bytes();(output/'bench.html').write_bytes(live);(output/'COLOUR-LICENSE.txt').write_bytes(license)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in [('bench.html',live),('COLOUR-LICENSE.txt',license)]:
            info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,data)
    facts={'model':'CIE 1931 2 degree, sampled 380..780 nm, 5 nm trapezoidal integration',
           'pair':'own smooth Gaussian-basis nullspace search; not measured pigments or globally optimal pair',
           'data_source_commit':standards['source_commit'],'data_license':'COLOUR-LICENSE.txt',
           'reflectance_min':min(min(r) for r in pair),'reflectance_max':max(max(r) for r in pair),
           'daylight':model.evaluate(standards,pair,0),'illuminant_A':model.evaluate(standards,pair,1),
           'adapted_path_in_gamut':all(not model.evaluate(standards,pair,float(t))['gamut_clipped'] for t in np.linspace(0,1,101)),
           'frames':len(frames),'limits':'synthetic reflectances; standard observer only; no measured display, pigment, printer or real observation'}
    # Store compact facts: the table already contains the lamp spectrum.
    for key in ('daylight','illuminant_A'):facts[key].pop('illuminant')
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps(facts,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'assets/metamer');generate(parser.parse_args().output)
