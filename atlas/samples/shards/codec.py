#!/usr/bin/env python3
"""Small educational systematic (10,6) Vandermonde erasure code over GF(256).
No artwork, original file, external libraries or network are needed by this decoder.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path

K=6
N=10
FORMAT='gitedit-shards-v1'


def multiply(a,b):
    result=0
    for _ in range(8):
        if b&1:result^=a
        a<<=1
        if a&256:a^=0x11d
        b>>=1
    return result


TABLE=tuple(bytes(multiply(a,b) for b in range(256)) for a in range(256))


def power(a,n):
    result=1
    while n:
        if n&1:result=TABLE[result][a]
        a=TABLE[a][a];n>>=1
    return result


def inverse(matrix):
    n=len(matrix)
    if not n or any(len(row)!=n for row in matrix):raise ValueError('square matrix required')
    work=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=next((i for i in range(col,n) if work[i][col]),None)
        if pivot is None:raise ValueError('singular matrix')
        work[col],work[pivot]=work[pivot],work[col]
        scale=power(work[col][col],254);work[col]=[TABLE[scale][v] for v in work[col]]
        for row in range(n):
            if row!=col:
                factor=work[row][col]
                work[row]=[a^TABLE[factor][b] for a,b in zip(work[row],work[col])]
    return [row[n:] for row in work]


def combine(matrix,rows):
    if not rows or len({len(row) for row in rows})!=1 or any(len(row)!=len(rows) for row in matrix):raise ValueError('matrix/data shape mismatch')
    result=[]
    for coefficients in matrix:
        out=bytearray(len(rows[0]))
        for coefficient,row in zip(coefficients,rows):
            products=TABLE[coefficient]
            for i,value in enumerate(row):out[i]^=products[value]
        result.append(bytes(out))
    return result


def generator():
    vandermonde=[[power(x,j) for j in range(K)] for x in range(1,N+1)]
    return [list(row) for row in combine(vandermonde,inverse(vandermonde[:K]))]


GENERATOR=generator()


def encode(payload):
    if not payload:raise ValueError('empty payload not supported')
    width=(len(payload)+K-1)//K;padded=payload+bytes(width*K-len(payload))
    rows=[padded[i*width:(i+1)*width] for i in range(K)]
    digest=hashlib.sha256(payload).hexdigest();encoded=combine(GENERATOR,rows)
    return [{'format':FORMAT,'k':K,'n':N,'index':i,'size':len(payload),'sha256':digest,
             'block_sha256':hashlib.sha256(block).hexdigest(),'data':base64.b64encode(block).decode()} for i,block in enumerate(encoded)]


def validate(record):
    if not isinstance(record,dict) or record.get('format')!=FORMAT or record.get('k')!=K or record.get('n')!=N:raise ValueError('unsupported shard format')
    for key,minimum,maximum in [('index',0,N-1),('size',1,10_000_000)]:
        value=record.get(key)
        if type(value)!=int or not minimum<=value<=maximum:raise ValueError('invalid '+key)
    for key in ('sha256','block_sha256'):
        value=record.get(key)
        if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):raise ValueError('invalid digest')
    try:block=base64.b64decode(record['data'],validate=True)
    except (KeyError,ValueError,TypeError) as e:raise ValueError('invalid base64 data') from e
    if len(block)!=(record['size']+K-1)//K:raise ValueError('incorrect block length')
    if hashlib.sha256(block).hexdigest()!=record['block_sha256']:raise ValueError('shard checksum mismatch; remove damaged shard')
    return block


def decode(records):
    if not K<=len(records)<=N:raise ValueError('need 6 to 10 distinct valid shards')
    rows=[validate(r) for r in records];indices=[r['index'] for r in records]
    if len(set(indices))!=len(indices):raise ValueError('duplicate shard index')
    if len({(r['size'],r['sha256']) for r in records})!=1:raise ValueError('mixed payloads')
    restored=b''.join(combine(inverse([GENERATOR[i] for i in indices[:K]]),rows[:K]))[:records[0]['size']]
    if hashlib.sha256(restored).hexdigest()!=records[0]['sha256']:raise ValueError('restored file checksum mismatch')
    return restored


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('shards',type=Path,nargs='+');parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try:payload=decode([json.loads(path.read_text()) for path in args.shards])
    except (ValueError,KeyError,OSError) as e:parser.error(str(e))
    args.output.write_bytes(payload)
    print(f'{len(payload)} bytes; SHA-256 {hashlib.sha256(payload).hexdigest()}')
