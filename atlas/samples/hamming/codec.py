"""Interleaved even-parity Hamming(7,4); position 1 is the leftmost printed bit."""
def word(s,n):
    if not isinstance(s,str) or len(s)!=n or any(b not in '01' for b in s):raise ValueError(f'{n} binary characters required')
    return s

def encode(data):
    word(data,4);bits=[0]*8
    for i,b in zip([3,5,6,7],data):bits[i]=int(b)
    for p in [1,2,4]:bits[p]=sum(bits[i] for i in range(1,8) if i&p)%2
    return ''.join(map(str,bits[1:]))

def syndrome(received):
    word(received,7);s=0
    for i,b in enumerate(received,1):
        if b=='1':s^=i
    return s

def decode(received):
    s=syndrome(received);fixed=list(received)
    if s:fixed[s-1]='1' if fixed[s-1]=='0' else '0'
    fixed=''.join(fixed)
    return {'syndrome':s,'candidate':fixed,'candidate_data':''.join(fixed[i-1] for i in [3,5,6,7])}

def certificate(data,received):
    return {'format':'hamming74-v1','data':data,'sent':encode(data),'received':word(received,7),**decode(received)}
