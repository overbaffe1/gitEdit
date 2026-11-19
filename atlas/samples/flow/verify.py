#!/usr/bin/env python3
"""Independent flow/cut verifier; optional exhaustive audit of all 64 s-t cuts. No solver imports."""
import argparse
import json
from pathlib import Path


def graph(a,b):
    if type(a)!=int or type(b)!=int or not 0<=a<=12 or not 0<=b<=12:raise ValueError('bounded integer valves required')
    # Rebuilt specification: node labels S,A,B,C,D,E,F,T = 0..7.
    endpoints=[(0,1),(0,2),(1,3),(1,4),(2,3),(2,4),(3,5),(3,6),(4,5),(4,6),(5,7),(6,7)]
    capacities=[a,5,6,4,3,5,5,4,3,4,b,6]
    return list(zip(endpoints,capacities))


def all_cuts(a,b):
    g=graph(a,b);out=[]
    for bits in range(64):
        inside={0}|{i+1 for i in range(6) if bits>>i&1};capacity=sum(c for (u,v),c in g if u in inside and v not in inside)
        out.append({'source_side':sorted(inside),'capacity':capacity})
    return out


def verify(certificate,exhaustive=False):
    if not isinstance(certificate,dict) or certificate.get('format')!='two-valves-8-v1':raise ValueError('unknown certificate')
    a=certificate.get('valve_a');b=certificate.get('valve_b');g=graph(a,b);flows=certificate.get('flows');cut=certificate.get('cut');value=certificate.get('value')
    if not isinstance(flows,list) or len(flows)!=12 or any(type(x)!=int for x in flows):raise ValueError('12 integer edge flows required')
    if type(value)!=int or not 0<=value<=24:raise ValueError('bounded integer value required')
    if not isinstance(cut,list) or any(type(x)!=int or not 0<=x<8 for x in cut) or len(set(cut))!=len(cut) or 0 not in cut or 7 in cut:raise ValueError('valid separating node set required')
    balance=[0]*8
    for ((u,v),capacity),flow in zip(g,flows):
        if not 0<=flow<=capacity:raise ValueError('edge capacity violation')
        balance[u]-=flow;balance[v]+=flow
    feasible=balance[0]==-value and balance[7]==value and all(balance[i]==0 for i in range(1,7))
    cut_capacity=sum(capacity for (u,v),capacity in g if u in cut and v not in cut)
    report={'feasible_flow':feasible,'flow_value':value,'cut_capacity':cut_capacity,'gap':cut_capacity-value,'maximum_proved':feasible and value==cut_capacity,'edges_checked':12,'internal_balances_checked':6}
    if exhaustive:
        cuts=all_cuts(a,b);minimum=min(x['capacity'] for x in cuts);report.update({'cuts_enumerated':64,'minimum_cut_capacity':minimum,'all_minimum_cuts':[x['source_side'] for x in cuts if x['capacity']==minimum]})
        report['exhaustive_agrees']=report['maximum_proved'] and value==minimum
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('certificate',type=Path);parser.add_argument('--all-cuts',action='store_true');args=parser.parse_args()
    try:result=verify(json.loads(args.certificate.read_text()),args.all_cuts)
    except ValueError as e:parser.error(str(e))
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['maximum_proved'] else 2)
