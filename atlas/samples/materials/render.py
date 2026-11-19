"""Small deterministic orthographic triangle renderer; artistic lighting, not a physical BRDF."""
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

def unit(a):return a/np.maximum(np.linalg.norm(a,axis=-1,keepdims=True),1e-12)
def mesh(nu=160,nv=28):
    t=np.arange(nu)*2*np.pi/nu
    center=np.stack(((2+np.cos(3*t))*np.cos(2*t),(2+np.cos(3*t))*np.sin(2*t),np.sin(3*t)),axis=1)
    tangent=unit(np.roll(center,-1,axis=0)-np.roll(center,1,axis=0));n=unit(np.cross(tangent,[0,0,1]));b=unit(np.cross(tangent,n));v=np.arange(nv)*2*np.pi/nv
    points=center[:,None,:]+.36*(np.cos(v)[None,:,None]*n[:,None,:]+np.sin(v)[None,:,None]*b[:,None,:])
    normals=unit(np.cross(np.roll(points,-1,axis=0)-np.roll(points,1,axis=0),np.roll(points,-1,axis=1)-np.roll(points,1,axis=1)))
    faces=[]
    for i in range(nu):
        for j in range(nv):
            a=i*nv+j;c=((i+1)%nu)*nv+(j+1)%nv;d=i*nv+(j+1)%nv;e=((i+1)%nu)*nv+j;faces.extend([[a,e,c],[a,c,d]])
    if np.mean(np.sum(normals*(points-center[:,None,:]),axis=-1))<0:normals=-normals;faces=[f[::-1] for f in faces]
    return points.reshape(-1,3),normals.reshape(-1,3),np.array(faces,dtype=np.int32)

def buffers(vertices,normals,faces,width=1100,height=1000):
    eye=unit(np.array([5.,-7.,5.2]));right=unit(np.cross([0,0,1],eye));up=unit(np.cross(eye,right));rotation=np.stack([right,up,eye],axis=1);v=vertices@rotation;n=normals@rotation
    scale=min(width/(np.ptp(v[:,0])+1.0),height/(np.ptp(v[:,1])+1.1));xy=np.stack((width/2+(v[:,0]-(v[:,0].max()+v[:,0].min())/2)*scale,height/2-(v[:,1]-(v[:,1].max()+v[:,1].min())/2)*scale),axis=1)
    depth=np.full((height,width),-np.inf);normal=np.zeros((height,width,3))
    for face in faces:
        p=xy[face];x0=max(0,int(np.floor(p[:,0].min())));x1=min(width-1,int(np.ceil(p[:,0].max())));y0=max(0,int(np.floor(p[:,1].min())));y1=min(height-1,int(np.ceil(p[:,1].max())))
        if x0>x1 or y0>y1:continue
        ax,ay=p[0];bx,by=p[1];cx,cy=p[2];den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-9:continue
        yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5;w0=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den;w1=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den;w2=1-w0-w1;zz=w0*v[face[0],2]+w1*v[face[1],2]+w2*v[face[2],2];old=depth[y0:y1+1,x0:x1+1];inside=(w0>=-1e-8)&(w1>=-1e-8)&(w2>=-1e-8)&(zz>old)
        if np.any(inside):
            old[inside]=zz[inside];value=w0[...,None]*n[face[0]]+w1[...,None]*n[face[1]]+w2[...,None]*n[face[2]];normal[y0:y1+1,x0:x1+1][inside]=value[inside]
    return depth,unit(normal),xy,v[:,2]

def shading(depth,normal,style):
    mask=np.isfinite(depth);n=normal;h,w=depth.shape;light=unit(np.array([-.45,.65,1.]));diffuse=np.maximum(0,n@light);rim=np.clip(1-n[:,:,2],0,1)
    # Local depth contrast is only an illustrative screen-space crevice cue.
    ao=np.zeros_like(depth);base=np.where(mask,depth,-100)
    for dy,dx in [(0,18),(0,-18),(18,0),(-18,0),(13,13),(-13,-13)]:
        other=np.roll(base,(dy,dx),(0,1));ao+=(other-base>.2)&mask
    ao=1-.3*ao/6
    if style=='matte':
        basecolor=np.array([.34,.43,.79]);intensity=.29+.70*diffuse;rgb=basecolor[None,None,:]*intensity[:,:,None];spec=np.maximum(0,n@unit(light+[0,0,1]))**34;rgb+=spec[:,:,None]*.13
    elif style=='metal':
        # A stylized studio environment evaluated along reflected view rays, no texture map.
        r=2*n[:,:,2,None]*n-np.array([0,0,1]);level=.12+.5*(r[:,:,1]+1)/2;rgb=np.repeat(level[:,:,None],3,axis=2)*np.array([.83,.89,.96]);stripe=np.exp(-((r[:,:,0]+.38)/.11)**4)*np.exp(-((r[:,:,1]-.1)/.95)**4);rgb+=stripe[:,:,None]*np.array([.85,.85,.78]);edge=np.exp(-((r[:,:,0]-.62)/.06)**2)*np.exp(-((r[:,:,1]-.15)/.95)**4);rgb+=edge[:,:,None]*np.array([.9,.72,.46]);rgb+=rim[:,:,None]*.15;rgb=np.clip(rgb,0,1)
    else:
        rgb=np.broadcast_to(np.array([.76,.83,.83]),(h,w,3)).copy();rgb*= (.7+.3*diffuse[:,:,None])
    rgb*=ao[:,:,None];rgb=np.clip(rgb,0,1);rgb=np.power(rgb,1/1.5);rgba=np.zeros((h,w,4),dtype=np.uint8);rgba[:,:,:3]=np.round(rgb*255).astype('uint8');rgba[:,:,3]=mask.astype('uint8')*255;return Image.fromarray(rgba)

def wire_overlay(image,xy,z,depth,nu=160,nv=28):
    arr=np.array(image);h,w=depth.shape;edges=[]
    for j in range(0,nv,3):edges.extend((i*nv+j,((i+1)%nu)*nv+j) for i in range(nu))
    for i in range(0,nu,5):edges.extend((i*nv+j,i*nv+(j+1)%nv) for j in range(nv))
    for a,b in edges:
        steps=max(2,int(np.linalg.norm(xy[a]-xy[b])*1.5));t=np.linspace(0,1,steps);p=xy[a,None,:]*(1-t[:,None])+xy[b,None,:]*t[:,None];zz=z[a]*(1-t)+z[b]*t;xx=p[:,0].astype(int);yy=p[:,1].astype(int);inside=(xx>=0)&(xx<w)&(yy>=0)&(yy<h);xx=xx[inside];yy=yy[inside];zz=zz[inside];visible=np.isfinite(depth[yy,xx])&(abs(depth[yy,xx]-zz)<.07);arr[yy[visible],xx[visible],:3]=[28,65,76]
    return Image.fromarray(arr)

def ground(width,height):
    im=Image.new('RGBA',(width,height),(0,0,0,0));d=ImageDraw.Draw(im);d.ellipse((width*.19,height*.84,width*.82,height*.94),fill=(35,42,51,60));return im.filter(ImageFilter.GaussianBlur(24))
