"""Reproduce new revision data; the historical large scans are not rerun.
Run from any directory: python code/revision_checks.py [--extended]
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
from pathlib import Path
import argparse,json,sys,time
import numpy as np
from scipy.linalg import eigh
from nonflat import Binned,geometric,algebraic_profile,corrected_exact,corrected_lanczos,correction_bound,raw_quantities,deltaD,vacuum
from flatscan import run,matrices
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'


def cutoff_curve(X,Z):
    K=(X@Z+Z@X)/2;w,U=eigh(K);c=U[0];vals=np.sort(abs(w[abs(w)<1-1e-10]));knots=[]
    for x in vals:
        if not knots or x-knots[-1]>1e-9:knots.append(float(x))
    kap=[.001]+[x+1e-10 for x in knots if x>.001]+[.999]
    rows=[]
    for k in kap:
        sel=abs(w)<=k;ev=U[:,sel]@c[sel];jv=U[:,sel]@(c[sel]/np.sqrt(1-w[sel]**2));zt=(Z-K@X)@jv
        t=ev[0];mx=ev@X@ev;mz=zt[0];rows.append(dict(kappa=k,t=float(t),p=float((t*t-mx*mx-mz*mz)/4),bound=correction_bound(k)))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--extended',action='store_true');args=ap.parse_args();DATA.mkdir(exist_ok=True)
    rows=[run(S,r=r) for S in [8,16,64] for r in [1-1e-8,1.,1+1e-8]]
    (DATA/'scale_sensitivity.json').write_text(json.dumps(rows,indent=2)+'\n')
    fresh=[run(S,tie=tie) for S in [8,16,32,64,128,256,1024] for tie in ([1,-1] if int(np.sqrt(S))**2==S else [1])]
    (DATA/'fresh_flat_checks.json').write_text(json.dumps(fresh,indent=2)+'\n')
    dense=[]
    for S,family,param in [(8,'geometric',.7),(10,'geometric',.5),(10,'geometric',.7),(10,'algebraic',3.),(10,'algebraic',4.),(10,'algebraic',6.)]:
        lam=geometric(S,param) if family=='geometric' else algebraic_profile(S,param);B=Binned(lam);eps,pr,x,z=raw_quantities(B)
        ans=corrected_exact(B,kappas=[.4,.6]);dense.append(dict(S=S,family=family,parameter=param,P=float(sum(lam**2)),eps=eps,dD=deltaD(lam),praw=pr,X0=x,Z0=z,results=ans))
    (DATA/'fresh_dense_nonflat.json').write_text(json.dumps(dense,indent=2)+'\n')
    curves={}
    for S in [8,64]:
        X,Z,_,_=matrices(S);idx=np.arange(0,S+1,2);curves['flat_'+str(S)]=cutoff_curve(X[np.ix_(idx,idx)],Z[np.ix_(idx,idx)])
    for family,param in [('geometric',.5),('geometric',.7),('algebraic',6.)]:
        lam=geometric(8,param) if family=='geometric' else algebraic_profile(8,param);B=Binned(lam);idx=np.array([j for j in range(256) if j.bit_count()%2==0]);I=np.eye(256)
        X=np.column_stack([B.X(I[k])[idx] for k in idx]);Z=np.column_stack([B.Z(I[k])[idx] for k in idx]);curves[family+'_'+str(param)]=cutoff_curve(X,Z)
    (DATA/'cutoff_curves.json').write_text(json.dumps(curves,indent=2)+'\n')
    smooth=[]
    for S in [8,16]:
        B=Binned(np.ones(S)/S);v=vacuum(S);hard=raw_quantities(B)[0]
        for eta in [.02,.05,.1,.2]:
            x=B.smooth_X(v,eta);z=B.smooth_Z(v,eta);eps=float(np.linalg.norm(B.smooth_X(z,eta)+B.smooth_Z(x,eta)))
            hx=1-np.tanh(np.sin(B.margin_x)/eta);hz=1-np.tanh(np.sin(B.margin_z)/eta)
            smooth.append(dict(S=S,eta=eta,hard_defect=hard,soft_defect=eps,gamma_x=B.margin_x,gamma_z=B.margin_z,hx=float(hx),hz=float(hz),defect_difference_bound=float(2*(hx+hz))))
    (DATA/'smooth_binning.json').write_text(json.dumps(smooth,indent=2)+'\n')
    if args.extended:
        rows=[];B=Binned(geometric(16,.8))
        for m in [240,480,960]:
            start=time.time();res=corrected_lanczos(B,m=m,kappas=[.4,.6])
            for d in res.values():d.pop('ritz')
            rows.append(dict(S=16,z=.8,requested_steps=m,results=res,seconds=time.time()-start))
        (DATA/'lanczos_sensitivity.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('Wrote revision data to',DATA)

if __name__=='__main__':main()
