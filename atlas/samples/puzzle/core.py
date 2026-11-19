#!/usr/bin/env python3
"""Eight-puzzle, fixed goal 123456780; exact reverse BFS."""
from collections import deque
from math import factorial

GOAL=(1,2,3,4,5,6,7,8,0)
HARD=(8,6,7,2,5,4,3,0,1)
FACT=[factorial(i) for i in range(10)]
NEIGHBORS=tuple(tuple(j for j in range(9) if abs(i//3-j//3)+abs(i%3-j%3)==1) for i in range(9))


def validate(board):
    if not isinstance(board,(list,tuple)) or len(board)!=9 or any(type(x)!=int for x in board) or sorted(board)!=list(range(9)):raise ValueError('permutation of integer labels 0..8 required')
    return tuple(board)


def rank(board):
    return sum(sum(y<x for y in board[i+1:])*FACT[8-i] for i,x in enumerate(board))


def parity(board):
    values=[x for x in board if x];return sum(x>y for i,x in enumerate(values) for y in values[i+1:])%2


def neighbors(board):
    zero=board.index(0)
    for j in NEIGHBORS[zero]:
        copy=list(board);copy[zero],copy[j]=copy[j],copy[zero];yield tuple(copy)


def build():
    distance={GOAL:0};queue=deque([GOAL])
    while queue:
        board=queue.popleft();d=distance[board]
        for other in neighbors(board):
            if other not in distance:distance[other]=d+1;queue.append(other)
    table=bytearray([255])*FACT[9]
    for board,d in distance.items():table[rank(board)]=d
    return bytes(table)


def path(board,table):
    board=validate(board);d=table[rank(board)]
    if d==255:raise ValueError('unreachable: odd inversion parity')
    out=[board]
    while d:
        board=next(x for x in neighbors(board) if table[rank(x)]==d-1);out.append(board);d-=1
    return out
