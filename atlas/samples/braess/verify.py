#!/usr/bin/env python3
"""Independent Wardrop certificate verifier: rebuild link loads and route costs, no equilibrium solver."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re


def rational(text):
    if not isinstance(text,str) or not re.fullmatch(r'-?\d{1,10}(?:/[1-9]\d{0,6})?',text):raise ValueError('bounded rational strings required')
    return Fraction(text)


def verify(c):
    if not isinstance(c,dict) or c.get('model')!='braess-45-x100-directed-v1':raise ValueError('unknown network')
    q=c.get('demand');opened=c.get('open')
    if type(q)!=int or not 1<=q<=10000 or type(opened)!=bool:raise ValueError('bad demand or topology flag')
    paths={'SAT':['SA','AT'],'SBT':['SB','BT']}
    edges={'SA':(Fraction(1,100),0),'AT':(0,45),'SB':(0,45),'BT':(Fraction(1,100),0)}
    if opened:paths['SABT']=['SA','AB','BT'];edges['AB']=(0,0)
    if not isinstance(c.get('flows'),dict) or set(c['flows'])!=set(paths) or not isinstance(c.get('route_times'),dict) or set(c['route_times'])!=set(paths):raise ValueError('exact available-route keys required')
    flows={p:rational(value) for p,value in c['flows'].items()}
    if any(x<0 for x in flows.values()) or sum(flows.values())!=q:raise ValueError('nonnegative conserved demand required')
    loads={e:sum(flows[p] for p in paths if e in paths[p]) for e in edges}
    link_times={e:a*loads[e]+b for e,(a,b) in edges.items()}
    times={p:sum(link_times[e] for e in route) for p,route in paths.items()};minimum=min(times.values())
    wardrop=all(flows[p]==0 or times[p]==minimum for p in paths)
    claimed=all(rational(c['route_times'][p])==times[p] for p in paths) and rational(c.get('time'))==minimum
    return {'equilibrium_verified':wardrop and claimed,'demand_conserved':True,'wardrop':wardrop,'claimed_costs_match':claimed,'link_loads':{e:str(x) for e,x in loads.items()},'route_times':{p:str(x) for p,x in times.items()},'minimum_time':str(minimum),'mean_used_time':str(sum(flows[p]*times[p] for p in paths)/q)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('certificate',type=Path);args=parser.parse_args()
    try:result=verify(json.loads(args.certificate.read_text()))
    except ValueError as error:parser.error(str(error))
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['equilibrium_verified'] else 2)
