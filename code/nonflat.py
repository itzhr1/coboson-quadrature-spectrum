"""Periodic quadratures for a normalized finite Schmidt spectrum.

Complex-linear fast Hadamard implementation; dense and Lanczos vacuum filters.
Lanczos output is an approximation, not a certified spectral enclosure. Near-cutoff
Ritz counts and near-target weights are diagnostics, not proofs of exact atoms.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from numpy.linalg import norm
from scipy.linalg import eigh, eigh_tridiagonal


def validate_spectrum(lam):
    lam = np.asarray(lam, dtype=float)
    if lam.ndim != 1 or not len(lam) or not np.all(np.isfinite(lam)) or np.any(lam <= 0):
        raise ValueError('Schmidt weights must be finite and positive')
    if not np.isclose(lam.sum(), 1., atol=2e-13, rtol=0):
        raise ValueError('Schmidt weights must sum to one; normalize explicitly')
    return lam


def fwht(v):
    a = np.array(v, copy=True, dtype=np.result_type(v, float))
    n = len(a)
    if a.ndim != 1 or n == 0 or n & (n-1):
        raise ValueError('Expected a power-of-two vector')
    h = 1
    while h < n:
        q = a.reshape(-1, 2*h)
        x, y = q[:, :h].copy(), q[:, h:].copy()
        q[:, :h], q[:, h:] = x+y, x-y
        h *= 2
    return a/np.sqrt(n)


def signed_sums(sq, S=None):
    sq = np.asarray(sq)
    if S is not None and len(sq) != S:
        raise ValueError('Rank mismatch')
    q = np.array([0.])
    for a in sq:
        q = np.stack((q+a, q-a), axis=1).reshape(-1)
    return q


def edge_distance(q):
    return np.abs(np.remainder(np.asarray(q), np.pi)-np.pi/2)


def Fsign(q, tie=1., tolerance=None):
    if tie not in (-1, 1):
        raise ValueError('tie must be +1 or -1')
    q = np.asarray(q)
    tol = 64*np.finfo(float).eps*np.maximum(1., np.abs(q)) if tolerance is None else tolerance
    return np.where(edge_distance(q) <= tol, tie, np.where(np.cos(q) >= 0, 1., -1.))


def correction_bound(kappa):
    if not 0 < kappa < 1:
        raise ValueError('Require 0 < kappa < 1')
    return float(np.sqrt(2*(1-np.sqrt(1-kappa*kappa))))


def deltaD(lam, r=1.):
    lam = validate_spectrum(lam)
    if not np.isfinite(r) or r <= 0:
        raise ValueError('r must be finite and positive')
    a = r*np.sqrt(lam); b = np.pi/(2*r)*np.sqrt(lam)
    u, v = np.sin(a)**2, np.sin(b)**2
    ell = np.clip(4*u*v*(u+v-2*u*v), 0., 1.)
    g = 1-2*u*v-.5j*np.sin(2*a)*np.sin(2*b)
    if np.any(ell == 1.):
        return float(np.sqrt(2.))
    logmag = .5*np.log1p(-ell).sum()
    phase = np.angle(g).sum()
    value = -2*np.expm1(logmag)+4*np.exp(logmag)*np.cos(phase/2)**2
    return float(np.sqrt(max(0., value)))


class Binned:
    def __init__(self, lam, r=1., tie=1.):
        self.lam = validate_spectrum(lam); self.S = len(self.lam)
        if not np.isfinite(r) or r <= 0:
            raise ValueError('r must be finite and positive')
        self.r, self.b = float(r), np.pi/(2*r)
        self.q = signed_sums(np.sqrt(self.lam))
        self.zsign, self.xsign = Fsign(self.b*self.q, tie), Fsign(r*self.q, tie)
        # F is even, hence H F H has no matrix elements between number parities.
        # Replacing i**N by this real phase is therefore exact on both blocks.
        self.phase = np.array([(-1.)**(j.bit_count()//2) for j in range(2**self.S)])
        self.margin_x = float(edge_distance(r*self.q).min())
        self.margin_z = float(edge_distance(self.b*self.q).min())

    def Z(self, v):
        return fwht(self.zsign*fwht(v))

    def X(self, v):
        return self.phase*fwht(self.xsign*fwht(self.phase*np.asarray(v)))

    def K(self, v):
        return .5*(self.X(self.Z(v))+self.Z(self.X(v)))

    def smooth_X(self, v, eta):
        if eta <= 0:
            raise ValueError('eta must be positive')
        return self.phase*fwht(np.tanh(np.cos(self.r*self.q)/eta)*fwht(self.phase*np.asarray(v)))

    def smooth_Z(self, v, eta):
        if eta <= 0:
            raise ValueError('eta must be positive')
        return fwht(np.tanh(np.cos(self.b*self.q)/eta)*fwht(v))


def vacuum(S):
    v = np.zeros(2**S); v[0] = 1.
    return v


def raw_quantities(Bn):
    v = vacuum(Bn.S); x, z = Bn.X(v), Bn.Z(v); xz, zx = Bn.X(z), Bn.Z(x)
    vectors = [v,z,x,xz]; signs = np.array([1,-1,-1,1])/4
    G = np.array([[np.vdot(a,b) for b in vectors] for a in vectors])
    # For v tensor v, each two-party inner product is G_ij squared, not |G_ij|^2.
    p = float(np.real(signs @ (G**2) @ signs))
    return float(norm(xz+zx)), p, float(np.real(x[0])), float(np.real(z[0]))


def _selected(w, kappa):
    correction_bound(kappa)
    gap = np.abs(np.abs(w)-kappa)
    tol = 128*np.finfo(float).eps
    # Inclusive convention only within the recorded roundoff band.
    return np.abs(w) <= kappa+tol, dict(cutoff_near_count=int(np.sum(gap<=tol)),
                                      cutoff_distance=float(gap.min()))


def _filter_result(Bn, Ev, Jv):
    t = float(Ev[0]); xe = Bn.X(Ev)
    zt = Bn.Z(Jv)-Bn.K(Bn.X(Jv))
    mx, mz = float(np.vdot(Ev,xe).real), float(zt[0])
    p = .25*(t*t-mx*mx-mz*mz)  # vacuum is real: exact m_y = 0
    return dict(t=t, mx=mx, mz=mz, p=p,
                projector_vector_consistency=float(abs(np.vdot(Ev,Ev).real-t)),
                mx_consistency=float(abs(mx-xe[0])),
                pauli_cross_diagnostic=float(abs(np.vdot(xe,zt))),
                probability_formula_status='model identity evaluated on numerical filter; not a certified error bound')


def corrected_exact(Bn, kappa=.5, kappas=None):
    """Dense floating-point diagonalization in the invariant vacuum parity sector."""
    n = 2**Bn.S
    inds = np.array([j for j in range(n) if j.bit_count()%2 == 0]); K = np.empty((len(inds),len(inds)))
    for j,k in enumerate(inds):
        e = np.zeros(n); e[k] = 1.; K[:,j] = Bn.K(e)[inds]
    w,U = eigh((K+K.T)/2)
    residual = float(norm(K@U-U*w, ord=np.inf)); c = U[0]
    def one(k):
        sel, diag = _selected(w,k)
        ev = U[:,sel]@c[sel]; jv = U[:,sel]@(c[sel]/np.sqrt(1-w[sel]**2))
        Ev,Jv = np.zeros(n),np.zeros(n);Ev[inds]=ev;Jv[inds]=jv
        ans=_filter_result(Bn,Ev,Jv)
        ans.update(diag, method='dense_even_sector',dimension=len(inds),eigen_residual_inf=residual,
                   near_target_weights={str(a):float(np.sum(c[np.abs(w-a)<1e-9]**2)) for a in [-1.,-.5,.5,1.]},
                   target_weight_status='finite numerical neighborhoods; no exact-rational or infinite-spectrum certification')
        return ans
    return one(kappa) if kappas is None else {k:one(k) for k in kappas}


def lanczos(Bn, v0, m, reorth=True):
    if m < 1:
        raise ValueError('m must be positive')
    n=len(v0);m=min(m,n);Q=np.zeros((m,n));q=np.array(v0,dtype=float);q/=norm(q);Q[0]=q
    al=[];be=[];qm=np.zeros(n);bp=0.;terminal=0.
    for j in range(m):
        w=Bn.K(q)-bp*qm;a=float(q@w);w-=a*q
        if reorth:
            for _ in range(2):w-=Q[:j+1].T@(Q[:j+1]@w)
        terminal=float(norm(w));al.append(a)
        if terminal<1e-13 or j==m-1:break
        be.append(terminal);qm=q;q=w/terminal;Q[j+1]=q;bp=terminal
    return Q[:len(al)],np.array(al),np.array(be),terminal


def corrected_lanczos(Bn,kappa=.5,m=240,kappas=None):
    Q,al,be,beta=lanczos(Bn,vacuum(Bn.S),m)
    if len(al)==1:w=al;U=np.ones((1,1))
    else:w,U=eigh_tridiagonal(al,be)
    c=U[0];ritz_residual=beta*np.abs(U[-1])
    def one(k):
        sel,diag=_selected(w,k);f=np.zeros_like(w);f[sel]=1/np.sqrt(1-w[sel]**2)
        Ev=Q.T@(U@(sel*c));Jv=Q.T@(U@(f*c));ans=_filter_result(Bn,Ev,Jv)
        ans.update(diag,method='lanczos',requested_steps=m,steps=len(al),terminal_beta=beta,
                   max_ritz_residual=float(ritz_residual.max()),
                   near_target_weights={str(a):float(np.sum(c[np.abs(w-a)<1e-7]**2)) for a in [-1.,-.5,.5,1.]},
                   target_weight_status='approximate Ritz neighborhoods, not certified atoms',
                   ritz=[dict(value=float(a),weight=float(b*b),residual=float(e)) for a,b,e in zip(w,c,ritz_residual) if b*b>1e-10])
        return ans
    return one(kappa) if kappas is None else {k:one(k) for k in kappas}


def geometric(S,z):
    if S<1 or not 0<z<1:raise ValueError('Require S >= 1 and 0 < z < 1')
    a=(1-z)*z**np.arange(S);return a/a.sum()


def algebraic_profile(S,width):
    """Model sequence, NOT a 3D exciton Schmidt discretization."""
    if S<1 or width<=0:raise ValueError('Require positive rank and width')
    a=(1+(np.arange(1,S+1)/width)**2)**-4;return a/a.sum()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rank',type=int,default=10);parser.add_argument('--z',type=float,default=.5)
    parser.add_argument('--steps',type=int,nargs='+',default=[120,240,480]);parser.add_argument('--cutoffs',type=float,nargs='+',default=[.4,.6])
    parser.add_argument('--dense',action='store_true');parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();B= Binned(geometric(args.rank,args.z));rows=[]
    if args.dense:rows.append(corrected_exact(B,kappas=args.cutoffs))
    else:
        for m in args.steps:rows.append(corrected_lanczos(B,m=m,kappas=args.cutoffs))
    args.output.write_text(json.dumps(dict(S=args.rank,z=args.z,omitted_weight=args.z**args.rank,
                                         status='finite-mode numerical estimates; compare steps and modes separately',results=rows),indent=2)+'\n')
