#!/usr/bin/env python3
"""Exact integer graph invariants from a CSV adjacency matrix. No named-graph generator or eigen solver."""
import argparse
import csv
import itertools
import json
from pathlib import Path


def load(path):
    with Path(path).open(newline='') as f:rows=list(csv.reader(f))
    n=len(rows)-1
    if not 1<=n<=32 or rows[0]!=['vertex']+[str(i) for i in range(n)]:raise ValueError('expected vertex,0,... header and 1..32 vertices')
    if any(len(row)!=n+1 or row[0]!=str(i) or any(value not in ('0','1') for value in row[1:]) for i,row in enumerate(rows[1:])):raise ValueError('invalid indexed binary adjacency rows')
    matrix=[[int(value) for value in row[1:]] for row in rows[1:]]
    if any(matrix[i][i] or matrix[i][j]!=matrix[j][i] for i in range(n) for j in range(n)):raise ValueError('simple undirected graph required')
    return matrix


def matmul(a,b):
    columns=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in columns] for row in a]


def characteristic(matrix):
    n=len(matrix);power=[[int(i==j) for j in range(n)] for i in range(n)];traces=[];coefficients=[1]
    for k in range(1,n+1):
        power=matmul(power,matrix);traces.append(sum(power[i][i] for i in range(n)))
        numerator=-sum(coefficients[k-i]*traces[i-1] for i in range(1,k+1))
        if numerator%k:raise ArithmeticError('Newton identity did not divide exactly')
        coefficients.append(numerator//k)
    return coefficients


def cliques4(matrix):
    return [list(vertices) for vertices in itertools.combinations(range(len(matrix)),4) if all(matrix[a][b] for a,b in itertools.combinations(vertices,2))]


def certify(matrix):
    n=len(matrix);degrees=list(map(sum,matrix));seen={0};pending=[0]
    while pending:
        i=pending.pop()
        for j in range(n):
            if matrix[i][j] and j not in seen:seen.add(j);pending.append(j)
    squared=matmul(matrix,matrix);laplacian=[[degrees[i]*int(i==j)-matrix[i][j] for j in range(n)] for i in range(n)];cliques=cliques4(matrix)
    return {'vertices':n,'edges':sum(degrees)//2,'degrees':degrees,'connected':len(seen)==n,
            'adjacency_characteristic_descending':characteristic(matrix),'laplacian_characteristic_descending':characteristic(laplacian),
            'A_squared_equals_4I_plus_2J':n==16 and all(squared[i][j]==4*int(i==j)+2 for i in range(n) for j in range(n)),
            'four_clique_count':len(cliques),'four_cliques_zero_based':cliques}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('adjacency',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
    try:report=certify(load(args.adjacency))
    except ValueError as e:p.error(str(e))
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
