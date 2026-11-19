"""Independent truth-table checker; does not import codec or use syndrome to choose a candidate."""
import argparse,json
from itertools import product
from pathlib import Path
GROUPS=[[1,3,5,7],[2,3,6,7],[4,5,6,7]]
def binary(s,n):
    if not isinstance(s,str) or len(s)!=n or any(b not in '01' for b in s):raise ValueError('invalid binary string')
    return s

def checks(s):return [sum(int(s[i-1]) for i in group)%2 for group in GROUPS]
def codebook():return [''.join(p) for p in product('01',repeat=7) if checks(''.join(p))==[0,0,0]]
def distance(a,b):return sum(x!=y for x,y in zip(a,b))
def verify(c):
    if not isinstance(c,dict) or c.get('format')!='hamming74-v1':raise ValueError('unknown certificate')
    data=binary(c.get('data'),4);sent=binary(c.get('sent'),7);received=binary(c.get('received'),7);candidate=binary(c.get('candidate'),7);decoded=binary(c.get('candidate_data'),4)
    if checks(sent)!=[0,0,0] or ''.join(sent[i-1] for i in [3,5,6,7])!=data:raise ValueError('sent word not the stated encoding')
    parity=checks(received);s=parity[0]+2*parity[1]+4*parity[2]
    if type(c.get('syndrome'))!=int or c['syndrome']!=s:raise ValueError('incorrect syndrome')
    nearest=[w for w in codebook() if distance(w,received)<=1]
    if nearest!=[candidate] or ''.join(candidate[i-1] for i in [3,5,6,7])!=decoded:raise ValueError('incorrect nearest codeword/data')
    errors=distance(sent,received)
    return {'verified':True,'parity_checks':parity,'syndrome':s,'true_errors_known_to_demo':errors,'candidate_equals_sent':candidate==sent,'within_one_error_guarantee':errors<=1}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args()
    try:r=verify(json.loads(a.certificate.read_text()))
    except (ValueError,TypeError) as e:p.error(str(e))
    print(json.dumps(r,indent=2))
