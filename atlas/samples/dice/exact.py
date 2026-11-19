#!/usr/bin/env python3
"""Exact distributions of sums of independent fair six-sided labelled dice."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

DICE={'A':[0,0,4,4,4,4],'B':[3,3,3,3,3,3],'C':[2,2,2,2,6,6],'D':[1,1,1,5,5,5]}


def validate(dice):
    if not isinstance(dice,dict) or set(dice)!=set('ABCD'):raise ValueError('exactly dice A, B, C, D required')
    for faces in dice.values():
        if not isinstance(faces,list) or len(faces)!=6 or any(type(x)!=int or abs(x)>100 for x in faces):raise ValueError('six integer labels in [-100,100] per die required')


def distribution(faces,rolls):
    if type(rolls)!=int or not 1<=rolls<=4:raise ValueError('1..4 independent rolls required')
    counts=Counter({0:1})
    for _ in range(rolls):
        out=Counter()
        for total,multiplicity in counts.items():
            for face in faces:out[total+face]+=multiplicity
        counts=out
    return counts


def compare(first,second):
    wins=sum(a*b for x,a in first.items() for y,b in second.items() if x>y)
    ties=sum(a*second.get(x,0) for x,a in first.items());total=sum(first.values())*sum(second.values())
    return {'wins':wins,'ties':ties,'losses':total-wins-ties,'total':total,'probability':str(Fraction(wins,total))}


def audit(dice):
    validate(dice);report={'model':'independent fair faces; compare sums; ties do not win','dice':dice,'modes':{}}
    for rolls in [1,2]:
        distributions={name:distribution(faces,rolls) for name,faces in dice.items()}
        pairs={a+b:compare(distributions[a],distributions[b]) for a in 'ABCD' for b in 'ABCD'}
        response={b:max((a for a in 'ABCD' if a!=b),key=lambda a:Fraction(pairs[a+b]['wins'],pairs[a+b]['total'])) for b in 'ABCD'}
        report['modes'][str(rolls)]={'distributions':{a:{str(x):count for x,count in sorted(d.items())} for a,d in distributions.items()},'pairs':pairs,'best_response':response}
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('dice',type=Path,nargs='?');args=parser.parse_args()
    try:print(json.dumps(audit(json.loads(args.dice.read_text()) if args.dice else DICE),indent=2))
    except ValueError as error:parser.error(str(error))
