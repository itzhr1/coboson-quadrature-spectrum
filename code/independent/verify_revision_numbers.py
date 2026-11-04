"""Independent re-checks of the numbers added in the 26 Oct revision (Sec. 6 harmonic table, Table 1 large-S rows, Sec. 7 geometric class)."""
import numpy as np, json, math
from numpy.linalg import norm, eigh
from pathlib import Path
DATA = Path(__file__).resolve().parents[2]/'data'
from scipy.linalg import expm, eigh_tridiagonal

# ---- (1) harmonic-pair defects via matrix exponentials (independent of the eigendecomposition route)
def ladder(S, r=1.0):
    off = np.sqrt(np.arange(1, S+1)*(1-np.arange(0, S)/S))
    Bp = np.diag(off, 1)            # B^dag |N> ... as matrix acting on column vectors: Bp[N-1,N]? build B then transpose
    B = np.zeros((S+1, S+1));
    for n in range(1, S+1): B[n-1, n] = off[n-1]
    Qr = -1j*r*(B.T-B); Qw = -(np.pi/(2*r))*(B.T+B)
    return Qr, Qw
S = 256; Qr, Qw = ladder(S); v = np.zeros(S+1); v[0] = 1
def cosQ(Q, k):
    U = expm(1j*k*Q); return ((U+U.conj().T)/2)
print("harmonic table check S=256 via expm:")
for (m, n) in [(0, 0), (0, 2), (1, 1), (3, 0), (2, 3), (8, 0), (12, 0)]:
    A = cosQ(Qr, 2*m+1); Bm = cosQ(Qw, 2*n+1)
    print("  (m,n)=(%d,%d): %.3f" % (m, n, norm((A@Bm+Bm@A)@v)))
print("  table: (0,0) 0.019 (0,2) 0.995 (1,1) 0.858 (3,0) 0.965 (2,3) 0.734 (8,0) 0.470 (12,0) 1.348")

# ---- (2) Table 1 large-S rows and the local exponent, recomputed from scratch with the tridiagonal route
def flat(S, r=1.0, kappa=0.5):
    b = np.pi/(2*r); off = np.sqrt(np.arange(1, S+1)*(1-np.arange(0, S)/S))
    w, V = eigh_tridiagonal(np.zeros(S+1), off)
    Z = (V*np.sign(np.cos(b*w)))@V.T; ph = 1j**np.arange(S+1)
    X = ((ph[:, None]*((V*np.sign(np.cos(r*w)))@V.T))*ph.conj()[None, :]).real
    v = np.zeros(S+1); v[0] = 1; eps = norm((X@Z+Z@X)@v)
    K = (X@Z+Z@X)/2; kw, kV = eigh(K); sel = np.abs(kw) <= kappa+1e-9
    c = kV[0]; Ev = kV[:, sel]@c[sel]; Jv = kV[:, sel]@(c[sel]/np.sqrt(1-kw[sel]**2))
    t = Ev[0]; mx = Ev@(X@Ev); mz = (Z@Jv-K@(X@Jv))[0]
    a = r/np.sqrt(S); be = b/np.sqrt(S); g = (1-2*np.sin(a)**2*np.sin(be)**2-0.5j*np.sin(2*a)*np.sin(2*be))**S
    return eps, t, 0.25*(t**2-mx**2-mz**2), np.sqrt(mx**2+mz**2)/t, np.sqrt(2+2*g.real)
for S in (2050, 3956):
    eps, t, p, bl, dD = flat(S); print("S=%d eps=%.4f t=%.4f p=%.5f bloch=%.4f dD=%.4f" % (S, eps, t, p, bl, dD))
print("  table: 2050: 0.4574 0.9350 0.05190 0.8732 0.0046 ; 3956: 0.4191 0.9422 0.05156 0.8762 0.0024")
rows = json.load(open(DATA/'legacy_flat_scan.json')); Sa = np.array([d['S'] for d in rows if d['tie'] > 0]); ea = np.array([d['eps'] for d in rows if d['tie'] > 0])
m = Sa >= 64; print("local exponent S>=64: %.3f (paper: -0.15)" % np.polyfit(np.log(Sa[m]), np.log(ea[m]), 1)[0])
pr = [d for d in rows if d['tie'] > 0 and 'p' in d]
print("exact zeros of p:", [d['S'] for d in pr if d['p'] < 1e-9], " near-zeros <1e-4:", [d['S'] for d in pr if 1e-9 <= d['p'] < 1e-4])
for lo, hi in ((32, 127), (128, 255), (1025, 4096)):
    sel = [d['p'] for d in pr if lo <= d['S'] <= hi]; print("  %d-%d: p in [%.4f, %.4f]" % (lo, hi, min(sel), max(sel)))

# ---- (3) geometric class, S=10, z=0.5: vacuum expectations by direct signed-sum enumeration; deltaD by expm in 2^S space
z = 0.5; S = 10; lam = (1-z)*z**np.arange(S); lam /= lam.sum(); sq = np.sqrt(lam)
signs = np.array([[1 if (t >> k) & 1 == 0 else -1 for k in range(S)] for t in range(2**S)])
q = signs@sq
X0 = np.mean(np.sign(np.cos(q))); Z0 = np.mean(np.sign(np.cos(np.pi/2*q)))
print("geometric z=0.5 S=10: <X>_0=%.4f <Z>_0=%.4f (paper table at S=19: 0.749, 0.293; scan at S=10: %s)" % (X0, Z0, "see json"))
sx = np.array([[0, 1], [1, 0]]); sy = np.array([[0, -1j], [1j, 0]])
def local(op, k):
    M = np.array([[1.0]])
    for j in range(S): M = np.kron(M, op if j == k else np.eye(2))
    return M
Qr = sum(-sq[k]*local(sy, k) for k in range(S)); Qw = sum(-(np.pi/2)*sq[k]*local(sx, k) for k in range(S))
U = expm(1j*Qr); Vv = expm(1j*Qw); v = np.zeros(2**S); v[0] = 1
dD_direct = norm((U@Vv+Vv@U)@v)
g = np.prod(1-2*np.sin(sq)**2*np.sin(np.pi/2*sq)**2-0.5j*np.sin(2*sq)*np.sin(np.pi*sq)); dD_prod = np.sqrt(2+2*g.real)
print("  deltaD direct=%.4f product=%.4f (table S=19: 1.266)" % (dD_direct, dD_prod))
# X, Z, K dense from definitions, exact filter, compare with scan json at S=10
wr, Vr = eigh(Qr); ww, Vw = eigh(Qw)
X = (Vr*np.sign(np.cos(wr)))@Vr.conj().T; Zm = (Vw*np.sign(np.cos(ww)))@Vw.conj().T
X = X.real; Zm = Zm.real; K = (X@Zm+Zm@X)/2; kw, kV = eigh(K); c = kV[0]
print("  eps_vac=%.4f" % norm((X@Zm+Zm@X)@v), " weight at K=+-1: %.3f, at -1/2: %.3f" % (np.sum(c[np.abs(np.abs(kw)-1) < 1e-8]**2), np.sum(c[np.abs(kw+0.5) < 1e-8]**2)))
for kap in (0.4, 0.6):
    sel = np.abs(kw) <= kap+1e-9; Ev = kV[:, sel]@c[sel]; Jv = kV[:, sel]@(c[sel]/np.sqrt(1-kw[sel]**2))
    t = Ev[0]; mx = Ev@(X@Ev); mz = (Zm@Jv-K@(X@Jv))[0]
    print("  kappa=%.1f t=%.4f p=%.5f" % (kap, t, 0.25*(t**2-mx**2-mz**2)))
d = [d for d in json.load(open(DATA/'legacy_nonflat_scan.json')) if d['z'] == 0.5 and d['S'] == 10][0]
print("  scan json S=10: eps=%.4f X0=%.4f Z0=%.4f w1=%.3f wh=%.3f t.4=%.4f p.4=%.5f t.6=%.4f p.6=%.5f" % (d['eps'], d['X0'], d['Z0'], d['w_at_1'], d['w_at_half'], d['t_0.4'], d['p_0.4'], d['t_0.6'], d['p_0.6']))
