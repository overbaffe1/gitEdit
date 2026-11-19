#!/usr/bin/env python3
"""Deferred acceptance with strict complete preference lists, equal sides, n<=8."""
from collections import deque


def validate(problem):
    if not isinstance(problem,dict) or set(problem)!={'A','B'}:raise ValueError('exactly A and B required')
    a,b=problem['A'],problem['B']
    if not isinstance(a,list) or not isinstance(b,list) or not 1<=len(a)<=8 or len(a)!=len(b):raise ValueError('equal sides of size 1..8 required')
    n=len(a)
    if any(not isinstance(row,list) or len(row)!=n or any(type(x)!=int for x in row) or sorted(row)!=list(range(n)) for row in a+b):raise ValueError('each preference row must be a permutation 0..n-1')
    return n


def deferred(problem,proposing='A'):
    n=validate(problem)
    if proposing not in ('A','B'):raise ValueError('proposing must be A or B')
    receiving='B' if proposing=='A' else 'A';preferences=problem[proposing];ranks=[[row.index(i) for i in range(n)] for row in problem[receiving]]
    pending=deque(range(n));next_choice=[0]*n;held=[-1]*n;events=[]
    while pending:
        p=pending.popleft();r=preferences[p][next_choice[p]];next_choice[p]+=1;previous=held[r]
        accepted=previous==-1 or ranks[r][p]<ranks[r][previous]
        if accepted:
            held[r]=p
            if previous!=-1:pending.append(previous)
        else:pending.append(p)
        assignment=[-1]*n
        for receiver,proposer in enumerate(held):
            if proposer!=-1:
                if proposing=='A':assignment[proposer]=receiver
                else:assignment[receiver]=proposer
        events.append({'proposer':p,'receiver':r,'accepted':accepted,'displaced':previous if accepted else -1,'assignment':assignment})
    return {'proposing':proposing,'assignment':events[-1]['assignment'],'events':events}
