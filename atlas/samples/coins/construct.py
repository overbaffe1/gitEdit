"""Find a balanced nonadaptive three-weighing plan for twelve coins."""
from itertools import product

def construct():
    # Each nonzero vector is paired with its negative. Choose one orientation per class.
    classes=[v for v in product((-1,0,1),repeat=3) if next((x for x in v if x),0)==1]
    for omitted in range(len(classes)):
        chosen=classes[:omitted]+classes[omitted+1:]
        for signs in product((-1,1),repeat=12):
            columns=[[s*x for x in v] for s,v in zip(signs,chosen)]
            if all(sum(v[i] for v in columns)==0 for i in range(3)):
                rows=[[v[i] for v in columns] for i in range(3)]
                return {'format':'twelve-coins-v1','rows':rows,'cases':[{'coin':j+1,'kind':kind,'outcomes':[sign*v for v in column]} for j,column in enumerate(columns) for kind,sign in [('heavy',1),('light',-1)]]}
    raise RuntimeError('no balanced plan found')

if __name__=='__main__':
    import json
    print(json.dumps(construct(),indent=2))
