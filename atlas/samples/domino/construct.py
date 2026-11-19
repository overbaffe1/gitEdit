#!/usr/bin/env python3
"""A single Hamiltonian cycle tiles every opposite-colour two-hole 8x8 board."""

def color(i):return (i//8+i%8)%2


def cycle():
    route=list(range(8))
    for row in range(1,8):
        for col in (range(7,0,-1) if row%2 else range(1,8)):route.append(row*8+col)
    route.extend(row*8 for row in range(7,0,-1))
    return route


def validate(holes):
    if not isinstance(holes,list) or len(holes)!=2 or any(type(i)!=int or not 0<=i<64 for i in holes) or holes[0]==holes[1]:raise ValueError('two distinct integer holes 0..63 required')
    return sorted(holes)


def paths(holes,route):
    holes=validate(holes);a,b=sorted(route.index(i) for i in holes)
    return [route[a+1:b],route[b+1:]+route[:a]]


def construct(holes):
    holes=validate(holes);parts=paths(holes,cycle());tileable=color(holes[0])!=color(holes[1]);dominoes=[]
    if tileable:
        for part in parts:dominoes.extend([part[i],part[i+1]] for i in range(0,len(part),2))
    counts=[32-sum(color(h)==c for h in holes) for c in [0,1]]
    return {'format':'two-holes-8x8-v1','holes':holes,'tileable':tileable,'remaining_colors':counts,'dominoes':dominoes}
