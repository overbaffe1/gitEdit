"""Synthetic task results, exact integer comparisons and common-weight rates."""
from fractions import Fraction

def parameter(x):
    if type(x)!=int or not 1<=x<=9:raise ValueError('integer composition 1..9 required')
    return x

def pair(f):return [f.numerator,f.denominator]
def construct(a=1,b=9):
    parameter(a);parameter(b)
    rows=[[9*a,10*a,8*b,10*b],[3*(10-a),10*(10-a),2*(10-b),10*(10-b)]]
    group_cross=[s*n2-s2*n for s,n,s2,n2 in rows];sa=sum(r[0] for r in rows);na=sum(r[1] for r in rows);sb=sum(r[2] for r in rows);nb=sum(r[3] for r in rows);cross=sa*nb-sb*na
    standard=[]
    for w in range(11):
        rates=[sum((Fraction(w if i==0 else 10-w,10)*Fraction(row[k],row[k+1]) for i,row in enumerate(rows)),Fraction()) for k in [0,2]]
        standard.append({'easy_tenths':w,'A':pair(rates[0]),'B':pair(rates[1])})
    return {'format':'simpson-two-strata-v1','rows':rows,'group_cross':group_cross,'total_cross':cross,'reversal':cross<0,'common_weights':standard}
