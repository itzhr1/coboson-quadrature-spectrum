"""Independent spot checks written for the 30 October 2026 review of v5 (Codex/Astra); does not import the
package calculation modules.  Paths adapted to the repository layout; results written to validation/independent_review_results.json.
The numerical checks are unchanged from the v5 review."""
from pathlib import Path
import json, math, hashlib, re, sys
import numpy as np
import scipy
from scipy.linalg import eigh, expm
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]  # the package root (README.md, code/, data/)
DATA=ROOT/'data'
out={'runtime':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__}}
def bins(Q):
 w,V=eigh(Q)
 c=np.cos(w); c[np.abs(c)<1e-12]=0
 return (V*np.where(c>=0,1,-1))@V.conj().T

def operators(lam):
 S=len(lam); d=2**S; B=np.zeros((d,d))
 for k,l in enumerate(lam):
  for j in range(d):
   if j&(1<<k):B[j^(1<<k),j]=np.sqrt(l)
 return B

def stats(B,k=.5,full=True):
 X=bins(-1j*(B.T-B)); Z=bins(-np.pi/2*(B.T+B)); n=len(B);v=np.eye(n)[:,0]
 K=(X@Z+Z@X)/2;w,U=eigh(K);sel=abs(w)<k+1e-12
 E=U[:,sel]@U[:,sel].conj().T;J=(U[:,sel]/np.sqrt(1-w[sel]**2))@U[:,sel].conj().T
 x=E@X;z=(Z-K@X)@J;y=1j*x@z
 # Two-party coefficient matrix, using transpose (not conjugate transpose).
 vv=[E@v,x@v,y@v,z@v]
 M=sum(s*np.outer(a,a) for s,a in zip([1,-1,-1,-1],vv))/4
 p=np.linalg.norm(M)**2;t=float(E[0,0].real)
 means=np.array([a[0,0].real for a in [x,y,z]])
 res={'t':t,'p_direct':float(p),'p_identity':float((t*t-means@means)/4),'eps':float(np.linalg.norm((X@Z+Z@X)@v)),
      'pauli_residual':float(np.linalg.norm(x@z+z@x)), 'involution_residual':float(np.linalg.norm(z@z-E))}
 if p>1e-13:
  res['singlet_stabilizer_residual']=float(max(np.linalg.norm(a@M@a.T+M) for a in [x,y,z]))
 raw=(np.outer(v,v)-np.outer(Z@v,Z@v)-np.outer(X@v,X@v)+np.outer(X@Z@v,X@Z@v))/4
 pr=np.linalg.norm(raw)**2;psi=raw/np.sqrt(pr)
 res['praw']=float(pr);res['bell']=float(sum(np.abs(np.linalg.eigvalsh(psi.T@A.T@psi.conj())).sum() for A in [X+Z,X-Z]))
 U0=expm(B.T-B);V0=expm(-1j*np.pi/2*(B.T+B));res['deltaD_direct']=float(np.linalg.norm((U0@V0+V0@U0)@v))
 return res
out['rank4']=[stats(operators(np.array(lam))) for lam in [[.49,.01,.25,.25],[.442,.058,.394,.106]]]
out['flat']={}
for S in [8,16,17,32,64,128]:
 B=np.diag(np.sqrt(np.arange(1,S+1)*(1-np.arange(S)/S)),1)
 out['flat'][str(S)]=stats(B)
# Independent dense tensor-quadrature checks of all six nonflat table rows.
out['nonflat_table']=[]
for row in json.loads((DATA/'fresh_dense_nonflat.json').read_text()):
 S=row['S'];par=row['parameter'];lam=par**np.arange(S) if row['family']=='geometric' else (1+(np.arange(1,S+1)/par)**2)**-4
 lam=lam/lam.sum();B=operators(lam)
 X=bins(-1j*(B.T-B)); Z=bins(-np.pi/2*(B.T+B));ii=[j for j in range(2**S) if j.bit_count()%2==0]
 X=X[np.ix_(ii,ii)];Z=Z[np.ix_(ii,ii)];K=(X@Z+Z@X)/2;w,U=eigh(K)
 res={'family':row['family'],'parameter':par,'S':S,'results':{}}
 for k in [.4,.6]:
  sel=abs(w)<k;c=U[0].conj();ev=U[:,sel]@c[sel];jv=U[:,sel]@(c[sel]/np.sqrt(1-w[sel]**2));zt=(Z-K@X)@jv
  t=ev[0].real;mx=np.vdot(ev,X@ev).real;mz=zt[0].real;p=(t*t-mx*mx-mz*mz)/4
  res['results'][str(k)]={'p':float(p),'difference_from_archive':float(p-row['results'][str(k)]['p'])}
 out['nonflat_table'].append(res)
# Symbolic local group-commutator log through weight^3.
u,r,b=sp.symbols('u r b',real=True)
g=1-2*sp.sin(r*u)**2*sp.sin(b*u)**2-sp.I*sp.sin(2*r*u)*sp.sin(2*b*u)/2
coeff=sp.series(sp.log(sp.series(g,u,0,8).removeO()),u,0,8).removeO().expand()
A=sp.Rational(4,3)*r*b*(r*r+b*b);D=2*r*r*b*b*(r*r+b*b);E=4*r*b*(r**4+b**4)/15+20*r**3*b**3/9
out['logg_series_verified']=sp.simplify(coeff-(-2*sp.I*r*b*u**2+sp.I*A*u**4-(D+sp.I*E)*u**6))==0
# Independently integrate the oscillator Gaussian over alternating bins.
from scipy.special import ndtr
from scipy.integrate import quad
def f_integral(s):
 return sum((-1.)**j*(ndtr((j+.5)*np.pi/s)-ndtr((j-.5)*np.pi/s)) for j in range(-80,81))
def f_series(s):
 return 4/np.pi*sum((-1.)**m/(2*m+1)*np.exp(-(2*m+1)**2*s*s/2) for m in range(500))
out['oscillator']={}
for r0 in [1.,np.sqrt(np.pi/2)]:
 x,z=f_integral(r0),f_integral(np.pi/(2*r0));out['oscillator'][str(r0)]={'x':x,'z':z,'p':(1-x*x-z*z)/4,'series_difference':max(abs(x-f_series(r0)),abs(z-f_series(np.pi/(2*r0))))}
# Exact eight-mode probability and field correlation counterexample.
out['p8_exact']=str((sp.Integer(959)-49*sp.sqrt(145))/29696)
out['p8_value']=float((sp.Integer(959)-49*sp.sqrt(145))/29696)
B=sp.Matrix([[0,1,0],[0,0,1],[0,0,0]]);v=sp.Matrix([sp.Rational(2,3),sp.Rational(2,3),sp.Rational(1,3)])
I=(B*v).dot(B*v);J=(B*B*v).dot(B*B*v)
out['S2_anderson']={'I':str(I),'J':str(J),'g2':str(J/I**2)}
# Scan coverage and prose numerical assertions.
bell=json.loads((DATA/'bell_raw_scan.json').read_text());flat=json.loads((DATA/'legacy_flat_scan.json').read_text());nf=json.loads((DATA/'legacy_nonflat_scan.json').read_text())
th=(16+14*np.sqrt(2))/17
b64=[d for d in bell if d['S']>=64]
minrow=min(b64,key=lambda d:d['bell_raw'])
out['bell_scan']={'rows':len(bell),'distinct_ranks':len({d['S'] for d in bell}),'max_rank':max(d['S'] for d in bell),'minimum_ge64':minrow,'fidelity_bound_min_ge64':.5+.5*(minrow['bell_raw']-th)/(2*np.sqrt(2)-th),'missing_401_420':[s for s in range(401,421) if s not in {d['S'] for d in bell}]}
out['nonflat_stability']={}
for z0 in [.5,.6]:
 rows=[d for d in nf if d['z']==z0 and 13<=d['S']<=19]
 out['nonflat_stability'][str(z0)]={key:{'min':min(d[key] for d in rows),'max':max(d[key] for d in rows),'span':max(d[key] for d in rows)-min(d[key] for d in rows)} for key in ['p_0.4','p_0.6','t_0.4','t_0.6']}
out['manuscript_sha256']=hashlib.sha256((ROOT/'manuscript/coboson_paper_v10_14.tex').read_bytes()).hexdigest()
(ROOT/'validation/independent_review_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
