#!/usr/bin/env python3
"""Continue a complete wave checkpoint; no initial condition or frame history required."""
import argparse
from pathlib import Path
import numpy as np
from wave_local import step


def resume(path,mode='reverse',steps=240):
    if mode not in ('reverse','zero','keep') or steps<0:raise ValueError('invalid mode or step count')
    with np.load(path,allow_pickle=False) as data:
        u=data['u'].copy();v=data['v'].copy();fixed=data['fixed'].copy()
    if u.ndim!=2 or min(u.shape)<3 or u.shape!=v.shape or u.shape!=fixed.shape:raise ValueError('matching 2D fields required')
    if fixed.dtype!=np.bool_ or not np.isfinite(u).all() or not np.isfinite(v).all():raise ValueError('finite fields and bool mask required')
    if not (fixed[0].all() and fixed[-1].all() and fixed[:,0].all() and fixed[:,-1].all()):raise ValueError('outer boundary must be fixed')
    if np.any(u[fixed]!=0) or np.any(v[fixed]!=0):raise ValueError('fixed nodes must be zero')
    if mode=='reverse':v=-v
    if mode=='zero':v[:]=0
    for _ in range(steps):u,v=step(u,v,fixed)
    return u,v


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('checkpoint',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mode',choices=('reverse','zero','keep'),default='reverse');p.add_argument('--steps',type=int,default=240)
    args=p.parse_args()
    try:u,v=resume(args.checkpoint,args.mode,args.steps)
    except ValueError as e:p.error(str(e))
    np.savez(args.output,u=u,v=v)
