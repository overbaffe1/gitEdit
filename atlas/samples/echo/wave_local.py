"""Reversible fixed-node lattice dynamics; no initial pulse, images or trajectory."""
import numpy as np

DT=.45


def laplacian(u,fixed):
    result=np.zeros_like(u)
    result[1:-1,1:-1]=u[:-2,1:-1]+u[2:,1:-1]+u[1:-1,:-2]+u[1:-1,2:]-4*u[1:-1,1:-1]
    result[fixed]=0
    return result


def step(u,v,fixed,dt=DT):
    # Velocity Verlet, speed=1 cell/unit time; fixed nodes are not dynamical degrees of freedom.
    half=v+.5*dt*laplacian(u,fixed)
    new_u=u+dt*half;new_u[fixed]=0
    new_v=half+.5*dt*laplacian(new_u,fixed);new_v[fixed]=0
    return new_u,new_v


def energy(u,v,fixed):
    return float(.5*np.sum(v*v)-.5*np.sum(u*laplacian(u,fixed)))


def modified_energy(u,v,fixed,dt=DT):
    # Exact quadratic invariant (up to roundoff) for the chosen linear Verlet map.
    force=laplacian(u,fixed)
    return energy(u,v,fixed)-dt*dt/8*float(np.sum(force*force))
