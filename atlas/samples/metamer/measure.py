#!/usr/bin/env python3
"""Compute XYZ, sRGB and a pair difference from the published spectral CSV only."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from model import evaluate


def load_csv(path):
    with Path(path).open(newline='') as f:rows=list(csv.DictReader(f))
    columns=['wavelength_nm','x_bar','y_bar','z_bar','D65','A','reflectance_a','reflectance_b']
    try:values=np.array([[float(row[key]) for key in columns] for row in rows])
    except (KeyError,ValueError,TypeError) as e:raise ValueError('invalid spectral columns') from e
    if values.shape!=(81,8) or not np.all(np.isfinite(values)):raise ValueError('81 finite rows required')
    if not np.array_equal(values[:,0],np.arange(380,781,5)):raise ValueError('380..780 nm at 5 nm required')
    if np.any(values[:,1:]<0) or np.any(values[:,6:]>1):raise ValueError('nonnegative data and reflectances on [0,1] required')
    standards={'wavelength_nm':values[:,0].tolist(),'cmf':values[:,1:4].tolist(),'D65':values[:,4].tolist(),'A':values[:,5].tolist()}
    return standards,[values[:,6].tolist(),values[:,7].tolist()]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('spectra',type=Path);p.add_argument('--mix',type=float,default=0);p.add_argument('--no-adapt',action='store_true');p.add_argument('--output',type=Path)
    args=p.parse_args()
    try:standards,pair=load_csv(args.spectra);result=evaluate(standards,pair,args.mix,not args.no_adapt)
    except ValueError as e:p.error(str(e))
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
