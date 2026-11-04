"""Flat-spectrum calculations with analytic eigenvalue grid and explicit ties."""
import argparse,json
from pathlib import Path
import numpy as np
from numpy.linalg import norm
from scipy.linalg import eigh_tridiagonal,eigh
from nonflat import Fsign,edge_distance,deltaD,correction_bound


def matrices(S,r=1.,tie=1.):
    if not isinstance(S,(int,np.integer)) or S<1 or r<=0:raise ValueError('Positive integer rank and scale required')
    off=np.sqrt(np.arange(1,S+1)*(1-np.arange(S)/S))
    w,V=eigh_tridiagonal(np.zeros(S+1),off)
    grid=(2*np.arange(S+1)-S)/np.sqrt(S)  # ascending, matching eigensolver order
    b=np.pi/(2*r);sx=Fsign(r*grid,tie);sz=Fsign(b*grid,tie)
    phase=1j**np.arange(S+1)
    Z=(V*sz)@V.T;X=(phase[:,None]*((V*sx)@V.T)*phase.conj()[None,:]).real
    return X,Z,grid,V


def run(S,r=1.,kappa=.5,tie=1.,do_corr=True):
    X,Z,q,V=matrices(S,r,tie);b=np.pi/(2*r);v=np.zeros(S+1);v[0]=1.;x=X@v;z=Z@v;xz=X@z;zx=Z@x
    vecs=[v,z,x,xz];c=np.array([1,-1,-1,1])/4;G=np.array([[a@b for b in vecs] for a in vecs])
    tol=64*np.finfo(float).eps
    ex=edge_distance(r*q)<=tol*np.maximum(1.,abs(r*q));ez=edge_distance(b*q)<=tol*np.maximum(1.,abs(b*q))
    out=dict(S=int(S),r=float(r),tie=tie,dD=deltaD(np.ones(S)/S,r),eps=float(norm(xz+zx)),praw=float(c@(G**2)@c),
             naz=int(ez.sum()),nax=int(ex.sum()),edge_mass_z=float((V[0,ez]**2).sum()),edge_mass_x=float((V[0,ex]**2).sum()),
             margin_x=float(edge_distance(r*q).min()),margin_z=float(edge_distance(b*q).min()))
    if do_corr:
        correction_bound(kappa);ii=np.arange(0,S+1,2);Xe=X[np.ix_(ii,ii)];Ze=Z[np.ix_(ii,ii)];K=(Xe@Ze+Ze@Xe)/2
        w,U=eigh(K);sel=abs(w)<=kappa+128*np.finfo(float).eps;c=U[0]
        ev=U[:,sel]@c[sel];jv=U[:,sel]@(c[sel]/np.sqrt(1-w[sel]**2));zt=(Ze-K@Xe)@jv
        t=float(ev[0]);mx=float(ev@Xe@ev);mz=float(zt[0]);p=.25*(t*t-mx*mx-mz*mz)
        out.update(t=t,mx=mx,mz=mz,p=p,bloch=float(np.hypot(mx,mz)/t) if t>1e-14 else None,
                   cutoff_distance=float(np.min(abs(abs(w)-kappa))),method='dense_even_Dicke',numerical=True)
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ranks',type=int,nargs='+',default=[8,16,32,64,128,256]);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();rows=[]
    for S in a.ranks:
        rows.append(run(S))
        if int(np.sqrt(S))**2==S:rows.append(run(S,tie=-1))
    a.output.write_text(json.dumps(rows,indent=2)+'\n')
