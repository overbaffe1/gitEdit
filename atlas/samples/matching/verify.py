#!/usr/bin/env python3
"""Independent stability checker and exhaustive stable-set verifier. No solver imports."""
import argparse
from itertools import permutations
import json
from math import factorial
from pathlib import Path


def validate(problem):
    if not isinstance(problem,dict) or set(problem)!={'A','B'}:raise ValueError('A/B preference matrices required')
    n=len(problem['A']) if isinstance(problem['A'],list) else 0
    if not 1<=n<=8 or not isinstance(problem['B'],list) or len(problem['B'])!=n:raise ValueError('two equal sides, 1..8')
    for row in problem['A']+problem['B']:
        if not isinstance(row,list) or len(row)!=n or any(type(x)!=int for x in row) or set(row)!=set(range(n)):raise ValueError('strict complete lists required')
    return n


def blocking(problem,assignment):
    n=validate(problem)
    if not isinstance(assignment,list) or len(assignment)!=n or any(type(x)!=int for x in assignment) or sorted(assignment)!=list(range(n)):raise ValueError('assignment must be a full permutation')
    inverse=[assignment.index(b) for b in range(n)];out=[]
    for a in range(n):
        for b in range(n):
            if problem['A'][a].index(b)<problem['A'][a].index(assignment[a]) and problem['B'][b].index(a)<problem['B'][b].index(inverse[b]):out.append([a,b])
    return out


def enumerate_stable(problem):
    n=validate(problem);a=problem['A'];b=problem['B'];stable=[]
    # Independent brute-force search; comparisons use the published ordered lists.
    for assignment in permutations(range(n)):
        inverse=[assignment.index(j) for j in range(n)];ok=True
        for i in range(n):
            for j in a[i]:
                if j==assignment[i]:break
                if b[j].index(i)<b[j].index(inverse[j]):ok=False;break
            if not ok:break
        if ok:stable.append(list(assignment))
    return stable


def audit(problem,first,second,claimed_stable=None):
    n=validate(problem)
    if blocking(problem,first) or blocking(problem,second):raise ValueError('endpoint has a blocking pair')
    stable=enumerate_stable(problem)
    if claimed_stable is not None and json.dumps(claimed_stable)!=json.dumps(stable):raise ValueError('incomplete or incorrect stable set')
    a_optimal=all(problem['A'][i].index(first[i])<=problem['A'][i].index(m[i]) for m in stable for i in range(n))
    b_optimal=all(problem['B'][j].index(second.index(j))<=problem['B'][j].index(m.index(j)) for m in stable for j in range(n))
    return {'assignments_checked':factorial(n),'stable_count':len(stable),'changed_pairs':sum(x!=y for x,y in zip(first,second)),'A_proposer_optimal':a_optimal,'B_proposer_optimal':b_optimal,'A_rank_sum_when_A_proposes':sum(problem['A'][i].index(first[i])+1 for i in range(n)),'A_rank_sum_when_B_proposes':sum(problem['A'][i].index(second[i])+1 for i in range(n)),'B_rank_sum_when_A_proposes':sum(problem['B'][j].index(first.index(j))+1 for j in range(n)),'B_rank_sum_when_B_proposes':sum(problem['B'][j].index(second.index(j))+1 for j in range(n))}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('problem',type=Path);parser.add_argument('certificate',type=Path);args=parser.parse_args()
    try:
        p=json.loads(args.problem.read_text());c=json.loads(args.certificate.read_text())
        if not isinstance(c['all_stable'],list):raise ValueError('complete stable list required')
        result=audit(p,c['A_assignment'],c['B_assignment'],c['all_stable'])
    except (ValueError,KeyError,TypeError) as error:parser.error(str(error))
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['A_proposer_optimal'] and result['B_proposer_optimal'] else 2)
