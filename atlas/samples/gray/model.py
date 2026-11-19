"""Six-bit reflected Gray code and exhaustive old/new transition samples."""
from itertools import product

def gray(i):return i^(i>>1)
def decode(g):
    if type(g)!=int or not 0<=g<64:raise ValueError('six-bit integer required')
    n=0
    while g:n^=g;g>>=1
    return n

def mixtures(a,b):
    changes=[i for i in range(6) if (a^b)&(1<<i)];values=[]
    for choices in product((0,1),repeat=len(changes)):
        x=a
        for bit,new in zip(changes,choices):
            if new:x=(x&~(1<<bit))|(b&(1<<bit))
        values.append(x)
    return sorted(values)

def construct():
    words=[f'{gray(i):06b}' for i in range(64)];transitions=[]
    for i in range(64):
        j=(i+1)%64;transitions.append({'from':i,'to':j,'binary_reads':mixtures(i,j),'gray_reads':sorted(decode(g) for g in mixtures(gray(i),gray(j)))})
    return {'format':'reflected-gray-six-v1','words':words,'transitions':transitions}
