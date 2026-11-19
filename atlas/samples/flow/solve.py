#!/usr/bin/env python3
"""Integer Edmonds-Karp on one fixed 8-node DAG; two valve capacities 0..12."""
from collections import deque

LABELS='SABCDEFT'

def edges(a,b):
    if type(a)!=int or type(b)!=int or not 0<=a<=12 or not 0<=b<=12:raise ValueError('integer valve capacities 0..12 required')
    return [(0,1,a),(0,2,5),(1,3,6),(1,4,4),(2,3,3),(2,4,5),(3,5,5),(3,6,4),(4,5,3),(4,6,4),(5,7,b),(6,7,6)]


def solve(a,b):
    graph=edges(a,b);residual=[[0]*8 for _ in range(8)]
    for u,v,capacity in graph:residual[u][v]=capacity
    value=0;augmentations=[]
    while True:
        parent=[-1]*8;parent[0]=0;queue=deque([0])
        while queue and parent[7]<0:
            u=queue.popleft()
            for v in range(8):
                if parent[v]<0 and residual[u][v]>0:parent[v]=u;queue.append(v)
        if parent[7]<0:break
        route=[7]
        while route[-1]!=0:route.append(parent[route[-1]])
        route.reverse();delta=min(residual[u][v] for u,v in zip(route,route[1:]));value+=delta
        for u,v in zip(route,route[1:]):residual[u][v]-=delta;residual[v][u]+=delta
        augmentations.append({'path':route,'delta':delta})
    reachable={0};queue=deque([0])
    while queue:
        u=queue.popleft()
        for v in range(8):
            if residual[u][v]>0 and v not in reachable:reachable.add(v);queue.append(v)
    return {'format':'two-valves-8-v1','valve_a':a,'valve_b':b,'flows':[cap-residual[u][v] for u,v,cap in graph],'value':value,'cut':sorted(reachable),'augmentations':augmentations}
