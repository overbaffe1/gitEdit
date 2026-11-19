#!/usr/bin/env python3
"""Integer primal-dual shortest-augmenting-path assignment, O(n^3), no external optimizer."""
import argparse
import json
from pathlib import Path


def costs(source,target):return [[(a[0]-b[0])**2+(a[1]-b[1])**2 for b in target] for a in source]


def hungarian(cost):
    n=len(cost)
    if not n or any(len(row)!=n or any(type(x)!=int or not 0<=x<=10**9 for x in row) for row in cost):raise ValueError('nonempty square nonnegative integer cost matrix required')
    u=[0]*(n+1);v=[0]*(n+1);owner=[0]*(n+1)
    for row in range(1,n+1):
        owner[0]=row;column=0;distance=[10**18]*(n+1);predecessor=[0]*(n+1);visited=[False]*(n+1)
        while True:
            visited[column]=True;active=owner[column];delta=10**18;next_column=0
            for candidate in range(1,n+1):
                if not visited[candidate]:
                    reduced=cost[active-1][candidate-1]-u[active]-v[candidate]
                    if reduced<distance[candidate]:distance[candidate]=reduced;predecessor[candidate]=column
                    if distance[candidate]<delta:delta=distance[candidate];next_column=candidate
            for candidate in range(n+1):
                if visited[candidate]:u[owner[candidate]]+=delta;v[candidate]-=delta
                else:distance[candidate]-=delta
            column=next_column
            if owner[column]==0:break
        while column:
            previous=predecessor[column];owner[column]=owner[previous];column=previous
    assignment=[0]*n
    for column in range(1,n+1):assignment[owner[column]-1]=column-1
    return {'format':'square-cost-assignment-v1','assignment':assignment,'u':u[1:],'v':v[1:]}


def greedy(cost):
    available=set(range(len(cost)));assignment=[]
    for row in cost:
        chosen=min(available,key=lambda j:(row[j],j));assignment.append(chosen);available.remove(chosen)
    return assignment


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('problem',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    from verify import validate_problem
    try:problem=json.loads(args.problem.read_text());validate_problem(problem);solution=hungarian(costs(problem['source'],problem['target']))
    except ValueError as e:parser.error(str(e))
    args.output.write_text(json.dumps(solution,indent=2)+'\n')
