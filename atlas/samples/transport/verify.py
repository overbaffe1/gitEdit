#!/usr/bin/env python3
"""Check a primal/dual assignment certificate with exact integers; no solver imports."""
import argparse
import json
from pathlib import Path


def validate_problem(problem):
    if not isinstance(problem,dict) or problem.get('cost')!='squared_euclidean':raise ValueError('squared_euclidean problem required')
    source=problem.get('source');target=problem.get('target')
    if not isinstance(source,list) or not isinstance(target,list) or not 1<=len(source)<=128 or len(source)!=len(target):raise ValueError('1..128 points in equal-size arrays required')
    for point in source+target:
        if not isinstance(point,list) or len(point)!=2 or any(type(x)!=int or abs(x)>10000 for x in point):raise ValueError('bounded integer 2D coordinates required')
    return len(source)


def verify(problem,certificate):
    n=validate_problem(problem)
    if not isinstance(certificate,dict) or certificate.get('format')!='square-cost-assignment-v1':raise ValueError('unsupported certificate')
    assignment=certificate.get('assignment');u=certificate.get('u');v=certificate.get('v')
    for values in (assignment,u,v):
        if not isinstance(values,list) or len(values)!=n or any(type(x)!=int or abs(x)>10**12 for x in values):raise ValueError('integer certificate arrays of correct size required')
    if sorted(assignment)!=list(range(n)):raise ValueError('assignment must be a permutation')
    # Rebuild costs here: never import the optimizer or trust a claimed objective.
    costs=[[sum((a[k]-b[k])**2 for k in (0,1)) for b in problem['target']] for a in problem['source']]
    slacks=[[costs[i][j]-u[i]-v[j] for j in range(n)] for i in range(n)]
    feasible=all(value>=0 for row in slacks for value in row);tight=all(slacks[i][assignment[i]]==0 for i in range(n))
    primal=sum(costs[i][assignment[i]] for i in range(n));dual=sum(u)+sum(v)
    return {'particles':n,'bijection':True,'dual_feasible':feasible,'constraints_checked':n*n,
            'matched_edges_tight':tight,'primal_cost':primal,'dual_lower_bound':dual if feasible else None,
            'gap':primal-dual if feasible else None,'optimal_proved':feasible and tight and primal==dual}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('problem',type=Path);parser.add_argument('certificate',type=Path);args=parser.parse_args()
    try:result=verify(json.loads(args.problem.read_text()),json.loads(args.certificate.read_text()))
    except ValueError as e:parser.error(str(e))
    print(json.dumps(result,indent=2))
    if not result['optimal_proved']:raise SystemExit(2)
