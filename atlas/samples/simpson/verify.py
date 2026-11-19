"""Independent count-table certificate checker; no model imports or fixed percentages."""
import argparse,json,math
from pathlib import Path

def integer(x,lo,hi):
    if type(x)!=int or not lo<=x<=hi:raise ValueError('bounded integer required')
    return x

def rational(n,d):
    g=math.gcd(n,d);return [n//g,d//g]

def verify(c):
    if not isinstance(c,dict) or c.get('format')!='simpson-two-strata-v1':raise ValueError('unknown certificate')
    rows=c.get('rows')
    if not isinstance(rows,list) or len(rows)!=2:raise ValueError('two strata required')
    for row in rows:
        if not isinstance(row,list) or len(row)!=4:raise ValueError('A successes,total; B successes,total required')
        for k in [0,2]:integer(row[k+1],1,1000000);integer(row[k],0,row[k+1])
    group_cross=[r[0]*r[3]-r[2]*r[1] for r in rows]
    if any(x<=0 for x in group_cross):raise ValueError('A must strictly outperform B in both strata')
    claimed=c.get('group_cross')
    if not isinstance(claimed,list) or len(claimed)!=2 or any(type(x)!=int for x in claimed) or claimed!=group_cross:raise ValueError('incorrect group cross products')
    sa,na,sb,nb=[sum(row[k] for row in rows) for k in range(4)];cross=sa*nb-sb*na
    if type(c.get('total_cross'))!=int or c['total_cross']!=cross or type(c.get('reversal'))!=bool or c['reversal']!=(cross<0):raise ValueError('incorrect aggregate claim')
    standard=c.get('common_weights')
    if not isinstance(standard,list) or len(standard)!=11:raise ValueError('eleven common-weight certificates required')
    for w,entry in enumerate(standard):
        if not isinstance(entry,dict) or type(entry.get('easy_tenths'))!=int or entry['easy_tenths']!=w:raise ValueError('incorrect weight')
        for name,k in [('A',0),('B',2)]:
            x,n=rows[0][k:k+2];y,m=rows[1][k:k+2];expected=rational(w*x*m+(10-w)*y*n,10*n*m);claim=entry.get(name)
            if not isinstance(claim,list) or len(claim)!=2 or any(type(i)!=int for i in claim) or claim!=expected:raise ValueError('incorrect common-weight fraction')
        if entry['A'][0]*entry['B'][1]<=entry['B'][0]*entry['A'][1]:raise ValueError('common weights did not preserve order')
    return {'verified':True,'group_cross':group_cross,'total_cross':cross,'reversal':cross<0,'aggregate_A':[sa,na],'aggregate_B':[sb,nb],'common_weights_checked':11}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args()
    try:r=verify(json.loads(a.certificate.read_text()))
    except (ValueError,TypeError) as e:p.error(str(e))
    print(json.dumps(r,indent=2))
