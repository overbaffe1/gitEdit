#!/usr/bin/env python3
"""Replay invertible row operations; verify a complete/minimum press-set witness without solving."""
import argparse
import json
from pathlib import Path


def integer(x,limit=1<<25):
    if type(x)!=int or not 0<=x<limit:raise ValueError('bounded integers required')
    return x


def geometry():
    rows=[]
    for r in range(5):
        for c in range(5):
            value=0
            for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                rr,cc=r+dr,c+dc
                if 0<=rr<5 and 0<=cc<5:value|=1<<(rr*5+cc)
            rows.append(value)
    return rows


def check(cert,witness=None):
    if not isinstance(cert,dict) or cert.get('format')!='bounded-cross-5x5-gf2-v1':raise ValueError('unknown certificate')
    matrix=geometry();rows=matrix.copy();transform=[1<<i for i in range(25)];operations=cert.get('operations')
    if not isinstance(operations,list) or len(operations)>2000:raise ValueError('bounded operation list required')
    for op in operations:
        if not isinstance(op,list) or len(op)!=3 or op[0] not in ('swap','xor'):raise ValueError('unknown elementary operation')
        kind,i,j=op;integer(i,25);integer(j,25)
        if i==j:raise ValueError('self-operation forbidden')
        if kind=='swap':rows[i],rows[j]=rows[j],rows[i];transform[i],transform[j]=transform[j],transform[i]
        else:rows[i]^=rows[j];transform[i]^=transform[j]
    # JSON encoding also distinguishes bool from int in claimed matrix data.
    def same(a,b):return json.dumps(a)==json.dumps(b)
    if not same(cert.get('rref'),rows) or not same(cert.get('transform'),transform):raise ValueError('replayed matrices mismatch')
    pivots=[];zero_seen=False
    for i,row in enumerate(rows):
        if not row:zero_seen=True;continue
        if zero_seen:raise ValueError('nonzero row below zero row')
        pivot=(row&-row).bit_length()-1
        if pivots and pivot<=pivots[-1]:raise ValueError('pivots not increasing')
        if any(other>>pivot&1 for j,other in enumerate(rows) if j!=i):raise ValueError('pivot column not reduced')
        pivots.append(pivot)
    if not same(cert.get('pivots'),pivots):raise ValueError('pivot mismatch')
    kernel=[]
    for free in range(25):
        if free in pivots:continue
        x=1<<free
        for i,p in enumerate(pivots):
            if rows[i]>>free&1:x|=1<<p
        if any((row&x).bit_count()%2 for row in matrix):raise ValueError('not a null vector')
        kernel.append(x)
    checks=transform[len(pivots):]
    if not same(cert.get('kernel'),kernel) or not same(cert.get('checks'),checks):raise ValueError('nullspace/check mismatch')
    for check in checks:
        for column in range(25):
            if sum(((check>>r)&1)*((matrix[r]>>column)&1) for r in range(25))%2:raise ValueError('not a conserved parity')
    report={'rank':len(pivots),'nullity':25-len(pivots),'operations_replayed':len(operations),'solvable_boards':1<<len(pivots),'all_boards':1<<25,'press_sets_per_solvable_board':1<<len(kernel),'invariant_effects_checked':25*len(checks),'matrix_certificate_verified':True}
    if witness is not None:
        if not isinstance(witness,dict):raise ValueError('witness object required')
        board=integer(witness.get('board'));syndrome=[(board&x).bit_count()%2 for x in checks];solvable=not any(syndrome)
        if type(witness.get('solvable'))!=bool or witness['solvable']!=solvable or not same(witness.get('syndrome'),syndrome):raise ValueError('solvability witness mismatch')
        candidates=witness.get('candidates')
        if not isinstance(candidates,list):raise ValueError('candidate list required')
        if solvable:
            for x in candidates:integer(x)
            if len(candidates)!=1<<len(kernel) or len(set(candidates))!=len(candidates):raise ValueError('complete distinct solution set required')
            for x in candidates:
                effect=sum(((row&x).bit_count()%2)<<i for i,row in enumerate(matrix))
                if effect!=board:raise ValueError('press set does not clear board')
            chosen=min(candidates,key=lambda x:(x.bit_count(),x));integer(witness.get('chosen'));integer(witness.get('minimum'),26)
            if witness['chosen']!=chosen or witness['minimum']!=chosen.bit_count():raise ValueError('not minimum')
        elif candidates or witness.get('chosen') is not None or witness.get('minimum') is not None:raise ValueError('impossible board cannot have solution')
        report['board_witness_verified']=True;report['solvable']=solvable;report['minimum']=witness['minimum']
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);p.add_argument('witness',type=Path,nargs='?');a=p.parse_args()
    try:print(json.dumps(check(json.loads(a.certificate.read_text()),json.loads(a.witness.read_text()) if a.witness else None),indent=2))
    except (ValueError,KeyError,TypeError) as e:p.error(str(e))
