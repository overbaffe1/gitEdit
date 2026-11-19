"""Independent reflected-recursion and string-product checker; no model import."""
import argparse,json
from itertools import product
from pathlib import Path

def reflected(width):
    words=['']
    for _ in range(width):words=['0'+w for w in words]+['1'+w for w in reversed(words)]
    return words

def mixed_words(a,b):return {''.join(p) for p in product(*[(x,) if x==y else (x,y) for x,y in zip(a,b)])}
def strict_values(value,expected):
    if not isinstance(value,list) or any(type(x)!=int or not 0<=x<64 for x in value) or value!=expected:raise ValueError('incorrect sorted sampled positions')

def verify(c):
    if not isinstance(c,dict) or c.get('format')!='reflected-gray-six-v1':raise ValueError('unknown certificate')
    words=c.get('words');rows=c.get('transitions')
    if words!=reflected(6):raise ValueError('not the stated six-bit reflected Gray order')
    if not isinstance(rows,list) or len(rows)!=64:raise ValueError('64 cyclic transitions required')
    binary_changes=gray_changes=binary_samples=gray_samples=binary_nonendpoints=0;histogram={}
    for i,row in enumerate(rows):
        j=(i+1)%64
        if not isinstance(row,dict) or type(row.get('from'))!=int or type(row.get('to'))!=int or row['from']!=i or row['to']!=j:raise ValueError('incorrect cyclic transition identity')
        a,b=f'{i:06b}',f'{j:06b}';d=sum(x!=y for x,y in zip(a,b));gd=sum(x!=y for x,y in zip(words[i],words[j]))
        if gd!=1:raise ValueError('Gray edge must change exactly one bit')
        br=sorted(int(w,2) for w in mixed_words(a,b));gr=sorted(words.index(w) for w in mixed_words(words[i],words[j]));strict_values(row.get('binary_reads'),br);strict_values(row.get('gray_reads'),gr)
        if gr!=sorted([i,j]):raise ValueError('nonendpoint Gray reading')
        binary_changes+=d;gray_changes+=gd;binary_samples+=len(br);gray_samples+=len(gr);binary_nonendpoints+=sum(v not in [i,j] for v in br);histogram[str(d)]=histogram.get(str(d),0)+1
    return {'verified':True,'positions':64,'cyclic_transitions':64,'binary_bit_changes':binary_changes,'gray_bit_changes':gray_changes,'binary_mixed_readings':binary_samples,'gray_mixed_readings':gray_samples,'binary_nonendpoint_readings':binary_nonendpoints,'gray_nonendpoint_readings':0,'binary_change_histogram':histogram}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args()
    try:r=verify(json.loads(a.certificate.read_text()))
    except (ValueError,TypeError) as e:p.error(str(e))
    print(json.dumps(r,indent=2))
