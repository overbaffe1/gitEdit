"""Heat kernel by uniformization, not a table of precomputed spectral values."""
import math
import numpy as np


def kernel(adjacency,time):
    a=np.asarray(adjacency,dtype=float)
    if not 0<=time<=2 or a.ndim!=2 or a.shape[0]!=a.shape[1] or not np.all(np.isfinite(a)) or np.any(a<0) or not np.array_equal(a,a.T) or np.any(np.diag(a)!=0):raise ValueError('symmetric nonnegative loopless matrix and time on [0,2] required')
    degrees=a.sum(axis=1);rate=float(degrees.max());identity=np.eye(len(a))
    if rate==0:return identity
    if rate>6:raise ValueError('demonstration supports maximum weighted degree 6')
    transition=identity-(np.diag(degrees)-a)/rate
    power=identity.copy();weight=math.exp(-rate*time);result=weight*power
    for k in range(1,97):
        power=power@transition;weight*=rate*time/k;result+=weight*power
    return result


def exact_regular_kernel(adjacency,time):
    # Independent closed form for the certified (16,6,2,2) pair only.
    a=np.asarray(adjacency,dtype=float);identity=np.eye(16);constant=np.ones((16,16))/16
    plus=(a+2*identity-8*constant)/4;minus=identity-constant-plus
    return constant+math.exp(-4*time)*plus+math.exp(-8*time)*minus
