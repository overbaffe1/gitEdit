#!/usr/bin/env python3
"""Independent local-certificate check of the ENTIRE eight-puzzle distance table. No BFS/solver import."""
import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path


def check(table):
    if not isinstance(table,(bytes,bytearray)) or len(table)!=362880:raise ValueError('exactly 9! raw bytes required')
    # Lexicographic enumeration defines table order independently of core.rank.
    boards=list(permutations(range(9)));values=dict(zip(boards,table));goal=(1,2,3,4,5,6,7,8,0)
    if values[goal]!=0:raise ValueError('goal must be zero')
    edges=0;reachable=0;histogram=Counter()
    for board,d in values.items():
        labels=[x for x in board if x];odd=sum(x>y for i,x in enumerate(labels) for y in labels[i+1:])%2
        if (d==255)!=bool(odd):raise ValueError('parity/sentinel mismatch')
        if d==255:continue
        if not 0<=d<=31 or (d==0 and board!=goal):raise ValueError('bad distance or extra zero')
        reachable+=1;histogram[d]+=1;zero=board.index(0);descent=d==0
        row,column=divmod(zero,3)
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            r,c=row+dr,column+dc
            if not (0<=r<3 and 0<=c<3):continue
            j=r*3+c;copy=list(board);copy[zero],copy[j]=copy[j],copy[zero];other=values[tuple(copy)];edges+=1
            if other==255 or abs(d-other)>1:raise ValueError('edge violates unit Lipschitz bound')
            if other==d-1:descent=True
        if not descent:raise ValueError('no descending neighbor')
    return {'states':362880,'reachable':reachable,'unreachable':362880-reachable,'directed_edges_checked':edges,'maximum_distance':max(histogram),'histogram':{str(k):v for k,v in sorted(histogram.items())},'exact_distances_proved':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('table',type=Path);args=parser.parse_args()
    try:print(json.dumps(check(args.table.read_bytes()),indent=2))
    except ValueError as error:parser.error(str(error))
