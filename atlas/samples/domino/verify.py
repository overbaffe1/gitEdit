#!/usr/bin/env python3
"""Check tilings or colour-impossibility witnesses and an optional Hamiltonian-cycle certificate. No constructor import."""
import argparse
import json
from pathlib import Path


def cell(x):
    if type(x)!=int or not 0<=x<64:raise ValueError('integer cell 0..63 required')
    return x


def adjacent(a,b):return abs(a//8-b//8)+abs(a%8-b%8)==1


def check_cycle(route):
    if not isinstance(route,list) or len(route)!=64:raise ValueError('64-cell cycle required')
    for i in route:cell(i)
    if set(route)!=set(range(64)) or any(not adjacent(route[i],route[(i+1)%64]) for i in range(64)):raise ValueError('not a Hamiltonian cycle on this board')
    return {'cycle_verified':True,'cells_visited_once':64,'adjacent_edges_including_closure':64}


def verify(c):
    if not isinstance(c,dict) or c.get('format')!='two-holes-8x8-v1':raise ValueError('unknown certificate')
    holes=c.get('holes');dominoes=c.get('dominoes');claimed=c.get('tileable')
    if not isinstance(holes,list) or len(holes)!=2:raise ValueError('two holes required')
    for i in holes:cell(i)
    if holes[0]==holes[1] or type(claimed)!=bool or not isinstance(dominoes,list):raise ValueError('distinct holes, boolean claim, domino list required')
    remaining=[i for i in range(64) if i not in holes];counts=[sum((i//8+i%8)%2==colour for i in remaining) for colour in [0,1]]
    if json.dumps(c.get('remaining_colors'))!=json.dumps(counts):raise ValueError('colour-count mismatch')
    if claimed:
        if len(dominoes)!=31:raise ValueError('31 dominoes required')
        covered=[]
        for pair in dominoes:
            if not isinstance(pair,list) or len(pair)!=2:raise ValueError('two-cell domino required')
            a,b=map(cell,pair)
            if not adjacent(a,b):raise ValueError('domino cells not side-adjacent')
            covered.extend(pair)
        if sorted(covered)!=remaining:raise ValueError('overlap, hole covered, or uncovered cell')
        return {'certificate_verified':True,'tileable':True,'dominoes':31,'cells_covered_once':62,'remaining_colors':counts}
    if dominoes or counts[0]==counts[1]:raise ValueError('colour inequality required to certify impossibility')
    return {'certificate_verified':True,'tileable':False,'dominoes':0,'cells_covered_once':0,'remaining_colors':counts,'colour_obstruction':abs(counts[0]-counts[1])}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);p.add_argument('--cycle',type=Path);a=p.parse_args()
    try:
        result=verify(json.loads(a.certificate.read_text()))
        if a.cycle:result.update(check_cycle(json.loads(a.cycle.read_text())))
    except (ValueError,TypeError,KeyError) as e:p.error(str(e))
    print(json.dumps(result,indent=2))
