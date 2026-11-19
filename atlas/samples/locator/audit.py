#!/usr/bin/env python3
"""Exhaustive uniqueness plus exact GF(2) minimum-distance certificate, from CSV only."""
import argparse
import json
from pathlib import Path
from codebook import load,book


def basis(values):
    pivots={}
    for value in values:
        while value:
            top=value.bit_length()-1
            if top in pivots:value^=pivots[top]
            else:pivots[top]=value;break
    return pivots


def audit(grid):
    codes4=[code for _,_,code in book(grid,4)];codes6=[code for _,_,code in book(grid)]
    rank=len(basis(codes6));extended=set(codes6)|{0}
    is_linear=len(extended)==1<<rank
    minimum=min(code.bit_count() for code in extended if code)
    # If 4095 distinct nonzero words exhaust a 12-dimensional subspace minus zero,
    # differences are nonzero words of that subspace. Two nonzero words attaining
    # the minimum difference exist because the space has >2 elements.
    certified=len(set(codes6))==4095 and 0 not in codes6 and rank==12 and is_linear
    return {'positions':4095,'window4_unique':len(set(codes4)),
            'window4_pair_distance':min(code.bit_count() for code in codes4) if len(set(codes4))==4095 and 0 not in codes4 and len(basis(codes4))==12 else None,
            'window6_unique':len(set(codes6)),
            'zero_in_window6':0 in codes6,'extended_rank_gf2':rank,'extended_code_size':len(extended),
            'extended_code_is_linear':is_linear,'minimum_nonzero_weight':minimum,
            'certified_pair_distance':minimum if certified else None,
            'guaranteed_correctable_flips':(minimum-1)//2 if certified else None,
            'gf2_basis_hex':[f'{value:09x}' for value in basis(codes6).values()],
            'minimum_weight_word_hex':f'{min((value for value in codes6 if value),key=int.bit_count):09x}',
            'method':'all windows from published CSV; GF(2) rank + cardinality establishes linear space after adding zero; minimum nonzero weight establishes pair distance'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('pattern',type=Path);args=parser.parse_args()
    try:print(json.dumps(audit(load(args.pattern)),indent=2))
    except ValueError as e:parser.error(str(e))
