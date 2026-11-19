#!/usr/bin/env python3
"""Exact Wardrop equilibrium for one fixed directed Braess network; continuous flows."""
from fractions import Fraction as F

MODEL='braess-45-x100-directed-v1'


def equilibrium(demand,opened):
    if type(demand)!=int or not 1<=demand<=10000 or type(opened)!=bool:raise ValueError('integer demand 1..10000 and boolean opened required')
    q=F(demand)
    if not opened:x=y=q/2;z=F(0)
    elif q<=4500:x=y=F(0);z=q
    elif q<=9000:x=y=q-4500;z=9000-q
    else:x=y=q/2;z=F(0)
    flows={'SAT':x,'SBT':y};times={'SAT':(x+z)/100+45,'SBT':45+(y+z)/100}
    if opened:flows['SABT']=z;times['SABT']=(x+y+2*z)/100
    common=min(times.values())
    return {'model':MODEL,'demand':demand,'open':opened,'flows':{k:str(v) for k,v in flows.items()},'route_times':{k:str(v) for k,v in times.items()},'time':str(common)}
