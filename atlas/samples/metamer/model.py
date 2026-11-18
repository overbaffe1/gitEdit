"""Sampled spectral colour model, independently implemented; standard tables credited separately."""
import json
from pathlib import Path
import numpy as np

BRADFORD=np.array([[.8951,.2664,-.1614],[-.7502,1.7135,.0367],[.0389,-.0685,1.0296]])
D65_WHITE=np.array([.95047,1.,1.08883])
XYZ_TO_RGB=np.array([[3.2404542,-1.5371385,-.4985314],[-.969266,1.8760108,.041556],[.0556434,-.2040259,1.0572252]])


def load():return json.loads(Path(__file__).with_name('standards.json').read_text())


def operator(standards,illuminant):
    wavelengths=np.array(standards['wavelength_nm']);cmf=np.array(standards['cmf']);light=np.asarray(illuminant)
    if light.shape!=wavelengths.shape or not np.all(np.isfinite(light)) or np.any(light<0):raise ValueError('finite nonnegative spectrum on standard wavelength grid required')
    weights=np.full(len(light),float(wavelengths[1]-wavelengths[0]));weights[[0,-1]]*=.5
    denominator=np.sum(cmf[:,1]*light*weights)
    if denominator<=0:raise ValueError('illuminant must have positive photopic power')
    return (cmf*(light*weights)[:,None]/denominator).T


def adaptation(white):
    return np.linalg.solve(BRADFORD,np.diag((BRADFORD@D65_WHITE)/(BRADFORD@white))@BRADFORD)


def lab(xyz):
    ratio=np.asarray(xyz)/D65_WHITE;delta=6/29
    f=np.where(ratio>delta**3,np.cbrt(ratio),ratio/(3*delta**2)+4/29)
    return np.array([116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])])


def srgb(linear):
    # Clipping is display-only, gamut is separately reported from the unmodified values.
    value=np.clip(linear,0,1)
    return np.where(value<=.0031308,12.92*value,1.055*value**(1/2.4)-.055)


def evaluate(standards,reflectances,mix,adapt=True):
    if not 0<=mix<=1:raise ValueError('mix must lie on [0,1]')
    # Normalize each endpoint to equal photopic Y before mixing, not equal arbitrary table units.
    cmf=np.array(standards['cmf']);weights=np.full(len(cmf),5.);weights[[0,-1]]*=.5
    lights=[np.array(standards[key]) for key in ('D65','A')]
    lights=[light/np.sum(light*cmf[:,1]*weights) for light in lights]
    light=(1-mix)*lights[0]+mix*lights[1]
    op=operator(standards,light);white=op@np.ones(len(light));cat=adaptation(white) if adapt else np.eye(3)
    xyz=[op@np.asarray(r) for r in reflectances];view=[cat@v for v in xyz];linear=[XYZ_TO_RGB@v for v in view]
    return {'xyz':[v.tolist() for v in xyz],'adapted_xyz':[v.tolist() for v in view],
            'linear_rgb':[v.tolist() for v in linear],'rgb8':[np.floor(srgb(v)*255+.5).astype(int).tolist() for v in linear],
            'delta_e76':float(np.linalg.norm(lab(view[0])-lab(view[1]))),'gamut_clipped':any(np.any(v<0) or np.any(v>1) for v in linear),
            'white':white.tolist(),'adaptation':cat.tolist(),'illuminant':light.tolist()}


def design(standards):
    wl=np.array(standards['wavelength_nm']);centers=np.arange(400,761,30)
    basis=np.exp(-.5*((wl[:,None]-centers[None,:])/24)**2)
    constraint=operator(standards,standards['D65'])@basis
    projector=np.eye(len(centers))-constraint.T@np.linalg.solve(constraint@constraint.T,constraint)
    rng=np.random.default_rng(20261118);best=None
    for _ in range(768):
        coeff=projector@rng.normal(size=len(centers));direction=basis@coeff;direction*=.46/np.max(np.abs(direction))
        pair=[.5+direction,.5-direction];result=evaluate(standards,pair,1)
        if not result['gamut_clipped'] and (best is None or result['delta_e76']>best[0]):best=(result['delta_e76'],pair)
    if best is None:raise RuntimeError('no in-gamut pair found')
    return [r.tolist() for r in best[1]]
