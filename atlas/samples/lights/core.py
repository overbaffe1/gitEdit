#!/usr/bin/env python3
"""Fixed bounded 5x5 Lights Out over GF(2), bit i = row-major cell i."""
N=25;LIMIT=1<<N

def mask(value):
    if type(value)!=int or not 0<=value<LIMIT:raise ValueError('25-bit unsigned integer required')
    return value


def moves():
    return [sum(1<<j for j in range(N) if abs(i//5-j//5)+abs(i%5-j%5)<=1) for i in range(N)]


def apply(presses):
    mask(presses);out=0
    for i,effect in enumerate(moves()):
        if presses>>i&1:out^=effect
    return out


def certificate():
    rows=moves();transform=[1<<i for i in range(N)];operations=[];pivots=[];r=0
    for c in range(N):
        pivot=next((i for i in range(r,N) if rows[i]>>c&1),None)
        if pivot is None:continue
        if pivot!=r:
            rows[r],rows[pivot]=rows[pivot],rows[r];transform[r],transform[pivot]=transform[pivot],transform[r];operations.append(['swap',r,pivot])
        for i in range(N):
            if i!=r and rows[i]>>c&1:rows[i]^=rows[r];transform[i]^=transform[r];operations.append(['xor',i,r])
        pivots.append(c);r+=1
    kernel=[]
    for free in range(N):
        if free in pivots:continue
        vector=1<<free
        for i,c in enumerate(pivots):
            if rows[i]>>free&1:vector|=1<<c
        kernel.append(vector)
    return {'format':'bounded-cross-5x5-gf2-v1','operations':operations,'rref':rows,'transform':transform,'pivots':pivots,'kernel':kernel,'checks':transform[r:]}


def solve(board,cert):
    mask(board);syndrome=[(board&check).bit_count()%2 for check in cert['checks']]
    if any(syndrome):return {'board':board,'solvable':False,'syndrome':syndrome,'candidates':[],'chosen':None,'minimum':None}
    rhs=[(board&row).bit_count()%2 for row in cert['transform']];first=sum(rhs[i]<<p for i,p in enumerate(cert['pivots']));candidates=[first]
    for null in cert['kernel']:candidates += [x^null for x in candidates]
    candidates.sort(key=lambda x:(x.bit_count(),x));chosen=candidates[0]
    return {'board':board,'solvable':True,'syndrome':syndrome,'candidates':candidates,'chosen':chosen,'minimum':chosen.bit_count()}
