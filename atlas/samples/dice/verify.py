#!/usr/bin/env python3
"""Independent exhaustive face-index verifier. No imports from exact.py."""
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def verify(dice,report):
    if not isinstance(dice,dict) or set(dice)!=set('ABCD'):raise ValueError('four dice required')
    if any(not isinstance(f,list) or len(f)!=6 or any(type(x)!=int or abs(x)>100 for x in f) for f in dice.values()):raise ValueError('six bounded integer labels required')
    # Check JSON types too: Python equality alone considers True equal to 1.
    if not isinstance(report,dict) or json.dumps(report.get('dice'),sort_keys=True)!=json.dumps(dice,sort_keys=True):return False
    try:
        for rolls in [1,2]:
            mode=report['modes'][str(rolls)]
            sums={a:[sum(dice[a][i] for i in indices) for indices in product(range(6),repeat=rolls)] for a in 'ABCD'}
            expected_distributions={a:{str(x):sums[a].count(x) for x in sorted(set(sums[a]))} for a in 'ABCD'}
            if json.dumps(mode['distributions'],sort_keys=True)!=json.dumps(expected_distributions,sort_keys=True):return False
            for a in 'ABCD':
                for b in 'ABCD':
                    outcomes=[(x>y)-(x<y) for x in sums[a] for y in sums[b]]
                    w=outcomes.count(1);t=outcomes.count(0);l=outcomes.count(-1);n=len(outcomes)
                    expected={'wins':w,'ties':t,'losses':l,'total':n,'probability':str(Fraction(w,n))}
                    if json.dumps(mode['pairs'][a+b],sort_keys=True)!=json.dumps(expected,sort_keys=True):return False
            for b in 'ABCD':
                best=max((a for a in 'ABCD' if a!=b),key=lambda a:mode['pairs'][a+b]['wins'])
                if mode['best_response'][b]!=best:return False
    except (KeyError,TypeError,ValueError):return False
    return True


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('dice',type=Path);parser.add_argument('report',type=Path);args=parser.parse_args()
    try:ok=verify(json.loads(args.dice.read_text()),json.loads(args.report.read_text()))
    except ValueError as error:parser.error(str(error))
    print('VERIFIED: 16 ordered pairs, 36 and 1296 equally likely outcomes per pair' if ok else 'REJECTED')
    raise SystemExit(0 if ok else 2)
