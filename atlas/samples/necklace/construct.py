"""Deterministic Euler traversal of the binary order-(n-1) overlap graph."""
def construct(n=5):
    if type(n)!=int or not 1<=n<=10:raise ValueError('integer order 1..10 required')
    mask=(1<<(n-1))-1;next_bit=[0]*(1<<(n-1));stack=[(0,None)];labels=[]
    while stack:
        node,_=stack[-1]
        if next_bit[node]<2:
            bit=next_bit[node];next_bit[node]+=1;stack.append((((node<<1)|bit)&mask,bit))
        else:
            _,bit=stack.pop()
            if bit is not None:labels.append(str(bit))
    return ''.join(reversed(labels))
