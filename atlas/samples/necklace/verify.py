"""Independent exhaustive cyclic-window checker. No constructor imports."""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

def verify(c):
    if not isinstance(c,dict) or c.get('format')!='binary-necklace-v1':raise ValueError('unknown certificate')
    n=c.get('order');s=c.get('bits')
    if type(n)!=int or not 1<=n<=10:raise ValueError('integer order 1..10 required')
    if not isinstance(s,str) or len(s)!=2**n or any(x not in '01' for x in s):raise ValueError('exactly 2^n binary symbols required')
    windows=[''.join(s[(i+j)%len(s)] for j in range(n)) for i in range(len(s))];counts=Counter(windows);expected={''.join(x) for x in product('01',repeat=n)}
    if set(counts)!=expected or any(v!=1 for v in counts.values()):raise ValueError('missing or repeated cyclic word')
    return {'verified':True,'order':n,'cyclic_length':len(s),'distinct_words':len(counts),'linear_length_required':2**n+n-1,'positions':{word:windows.index(word) for word in sorted(expected)}}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args()
    try:result=verify(json.loads(a.certificate.read_text()))
    except (ValueError,TypeError) as e:p.error(str(e))
    print(json.dumps(result,indent=2))
