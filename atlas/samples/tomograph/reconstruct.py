#!/usr/bin/env python3
"""Parallel-beam filtered backprojection from a self-describing CSV, no phantom input."""
import argparse
import csv
import math
from pathlib import Path
import numpy as np
from PIL import Image


def load(path):
    with Path(path).open(newline='') as f:
        reader=csv.reader(f)
        try:header=next(reader)
        except StopIteration:raise ValueError('empty measurement table') from None
        if len(header)<3 or header[0]!='detector_s' or any(not h.startswith('angle_') for h in header[1:]):raise ValueError('expected detector_s and angle_* columns')
        angles=np.array([float(h.removeprefix('angle_'))*math.pi/180 for h in header[1:]])
        data=np.array([[float(v) for v in row] for row in reader])
    if data.ndim!=2 or data.shape[1]!=len(header) or data.shape[0]<4:raise ValueError('invalid projection table')
    s=data[:,0];projections=data[:,1:].T
    if not np.all(np.isfinite(data)) or not np.all(np.isfinite(angles)):raise ValueError('finite values required')
    if not np.allclose(np.diff(s),s[1]-s[0],rtol=1e-5,atol=1e-8) or s[1]<=s[0]:raise ValueError('uniform increasing detector coordinates required')
    expected=np.arange(len(angles))*math.pi/len(angles)
    if not np.allclose(angles,expected,atol=1e-8):raise ValueError('uniform angles on [0,180) required')
    return s,angles,projections


def ramp_filter(projections,spacing):
    if spacing<=0:raise ValueError('positive detector spacing required')
    width=projections.shape[1];padded=1<<(2*width-1).bit_length()
    frequencies=np.fft.rfftfreq(padded,d=spacing)
    spectrum=np.fft.rfft(projections,n=padded,axis=1)
    return np.fft.irfft(spectrum*np.abs(frequencies)[None,:],n=padded,axis=1)[:,:width]


def selected(total,views):
    if not 1<=views<=total or total%views:raise ValueError('views must be a positive divisor of available angle count (uniform quadrature)')
    return np.floor(np.arange(views)*total/views).astype(int)


def backproject(s,angles,data,size=192,span=math.pi):
    axis=np.linspace(-1,1,size);x,y=np.meshgrid(axis,axis)
    result=np.zeros_like(x)
    for angle,row in zip(angles,data):
        coordinate=x*math.cos(angle)+y*math.sin(angle)
        result+=np.interp(coordinate,s,row,left=0,right=0)
    return result*(span/len(angles))


def reconstruct(s,angles,data,views=None,filtered=True,size=192):
    indices=selected(len(angles),len(angles) if views is None else views)
    processed=ramp_filter(data,s[1]-s[0]) if filtered else data
    return backproject(s,angles[indices],processed[indices],size)


def display(array,filtered=True):
    # Explicit display-only scales. Raw numeric results are not clipped in the solver.
    scale=1.5 if filtered else 4.5
    return Image.fromarray(np.uint8(np.floor(np.clip(array/scale,0,1)*255+.5)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('measurements',type=Path)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--views',type=int)
    p.add_argument('--plain',action='store_true',help='unfiltered backprojection; display scale differs explicitly')
    args=p.parse_args()
    try:s,angles,data=load(args.measurements);image=reconstruct(s,angles,data,args.views,not args.plain)
    except ValueError as e:p.error(str(e))
    display(image,not args.plain).save(args.output)
