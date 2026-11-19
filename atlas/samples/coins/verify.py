"""Independently simulate physical masses and prove every trace identifies one case."""
import argparse,json
from itertools import product
from pathlib import Path

def verify(c):
    if not isinstance(c,dict) or c.get('format')!='twelve-coins-v1':raise ValueError('unknown plan')
    rows=c.get('rows');cases=c.get('cases')
    if not isinstance(rows,list) or len(rows)!=3:raise ValueError('three weighings required')
    for row in rows:
        if not isinstance(row,list) or len(row)!=12 or any(type(x)!=int or x not in [-1,0,1] for x in row):raise ValueError('12 placements -1/0/1 required')
        if row.count(1)!=row.count(-1) or row.count(1)==0:raise ValueError('equal nonempty pans required')
    if not isinstance(cases,list) or len(cases)!=24:raise ValueError('24 cases required')
    seen={};identities=set()
    for case in cases:
        if not isinstance(case,dict) or type(case.get('coin'))!=int or not 1<=case['coin']<=12 or case.get('kind') not in ['heavy','light']:raise ValueError('bad case')
        identity=(case['coin'],case['kind'])
        if identity in identities:raise ValueError('duplicate case')
        identities.add(identity);outcomes=case.get('outcomes')
        if not isinstance(outcomes,list) or len(outcomes)!=3 or any(type(x)!=int or x not in [-1,0,1] for x in outcomes):raise ValueError('three integer outcomes required')
        # All real coins weigh 10, counterfeit 11 or 9. Same conclusions for any positive deviation.
        masses=[10]*12;masses[case['coin']-1]=11 if case['kind']=='heavy' else 9;actual=[]
        for row in rows:
            left=sum(m for m,p in zip(masses,row) if p==1);right=sum(m for m,p in zip(masses,row) if p==-1);actual.append((left>right)-(left<right))
        if actual!=outcomes:raise ValueError('outcome does not match physical mass sums')
        trace=tuple(actual)
        if trace in seen:raise ValueError('two counterfeit cases have the same outcome trace')
        seen[trace]=identity
    unused=[list(t) for t in product((-1,0,1),repeat=3) if t not in seen]
    return {'verified':True,'cases_checked':24,'mass_comparisons':72,'distinct_traces':len(seen),'pan_sizes':[[row.count(1),row.count(-1),row.count(0)] for row in rows],'unused_traces':unused,'two_weighings_outcomes':9,'hypotheses':24}

def thirteen_bound():
    return [{'coins_each_pan':k,'unbalanced_hypotheses':2*k,'balanced_hypotheses':2*(13-2*k),'remaining_outcomes_per_branch':9,'both_branches_fit':2*k<=9 and 2*(13-2*k)<=9} for k in range(7)]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);a=p.parse_args()
    try:r=verify(json.loads(a.plan.read_text()));r['thirteen_first_weighing']=thirteen_bound()
    except (ValueError,TypeError) as e:p.error(str(e))
    print(json.dumps(r,indent=2))
