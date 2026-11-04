import numpy as np, itertools, math
from numpy.linalg import eigh, norm

def Fsign(q, tol=1e-11):
    c = np.cos(q)
    return np.where(c >= -tol, 1.0, -1.0)

def binned(Q):
    w, V = eigh(Q)
    return (V * Fsign(w)) @ V.conj().T, w

# ---------- Rank-4 nonflat, full 16-dim paired sector ----------
def rank4(lams, r=1.0):
    b = np.pi/(2*r)
    n = len(lams); dim = 2**n
    # local pair modes d_k: commuting hard-core bosons (2-level), basis bits
    def dk(k):
        d = np.zeros((dim,dim))
        for j in range(dim):
            if (j>>k)&1: d[j ^ (1<<k), j] = 1.0   # annihilate
        return d
    B = sum(np.sqrt(l)*dk(k) for k,l in enumerate(lams))
    Bd = B.T
    Qr = -1j*r*(Bd - B); Qw = -b*(Bd + B)
    X,_ = binned(Qr); Z,_ = binned(Qw)
    X = X.real if np.allclose(X.imag,0) else X
    v = np.zeros(dim); v[0]=1
    eps2 = norm((X@Z+Z@X)@v)**2
    # sequential state: Pi_X^- Pi_Z^- |00>
    Zv, Xv, XZv = Z@v, X@v, X@(Z@v)
    M = 0.25*(np.outer(v,v) - np.outer(Zv,Zv) - np.outer(Xv,Xv) + np.outer(XZv,XZv))
    pseq = np.trace(M.T@M).real
    Psi = M/np.sqrt(pseq)
    Bopt = 0.0
    for A in (X+Z, X-Z):
        H = Psi.T @ A.T @ Psi.conj()
        Bopt += np.abs(eigh((H+H.conj().T)/2)[0]).sum()
    # displacement defect direct vs product formula
    from scipy.linalg import expm
    U = expm(1j*Qr); V = expm(1j*Qw)
    dD2_direct = norm((U@V+V@U)@v)**2
    g = 1
    for l in lams:
        a, be = r*np.sqrt(l), b*np.sqrt(l)
        g *= 1 - 2*np.sin(a)**2*np.sin(be)**2 - 0.5j*np.sin(2*a)*np.sin(2*be)
    dD2_prod = 2 + 2*g.real
    return eps2, pseq, Bopt, dD2_direct, dD2_prod

for lab, lams in (("a",[0.49,0.01,0.25,0.25]),("b",[0.442,0.058,0.394,0.106])):
    print(lab, "P=%.6f M3=%.6f"%(sum(l**2 for l in lams), sum(l**3 for l in lams)), rank4(lams))
print("claimed: a eps2=1 pseq=3/32=%.5f B=%.5f ; b eps2=2.5 pseq=23/128=%.5f B=%.5f"%(3/32,1+3**.5,23/128,(2*31**.5+27*2**.5)/23))

# ---------- Flat spectrum, Dicke ladder ----------
def ladder(S, r=1.0, kappa=0.5):
    b = np.pi/(2*r)
    N = np.arange(S+1)
    B = np.zeros((S+1,S+1))
    for n in range(1,S+1): B[n-1,n] = np.sqrt(n*(1-(n-1)/S))
    Bd = B.T
    Qr = -1j*r*(Bd-B); Qw = -b*(Bd+B)
    X,_ = binned(Qr); Z,_ = binned(Qw)
    X = X.real; Z = Z.real
    K = (X@Z+Z@X)/2
    kw, kV = eigh(K)
    sel = np.abs(kw) <= kappa + 1e-9
    E = (kV[:,sel]) @ kV[:,sel].T
    J = (kV[:,sel] / np.sqrt(1-kw[sel]**2)) @ kV[:,sel].T
    Zt = (Z - K@X) @ J
    XE = E@X@E
    Yt = 1j*XE@Zt
    return dict(B=B,X=X,Z=Z,K=K,kw=kw,E=E,Zt=Zt,XE=XE,Yt=Yt,S=S)

def pcorr(L, v):
    t = v@L['E']@v
    mx = v@L['XE']@v; my = (v.conj()@L['Yt']@v).real; mz = v@L['Zt']@v
    return t, mx, my, mz, 0.25*(t**2-mx**2-my**2-mz**2)

def praw(L, v):
    X,Z = L['X'],L['Z']
    Zv,Xv,XZv = Z@v,X@v,X@(Z@v)
    M = 0.25*(np.outer(v,v)-np.outer(Zv,Zv)-np.outer(Xv,Xv)+np.outer(XZv,XZv))
    return np.trace(M.T@M)

def seeds(S, alpha=1.0, beta=1.0):
    FN = np.array([math.factorial(S)/(S**n*math.factorial(S-n)) for n in range(S+1)])
    fac = np.array([math.factorial(n) for n in range(S+1)],dtype=float)
    vac = np.zeros(S+1); vac[0]=1
    qg = alpha**np.arange(S+1)/np.sqrt(fac*FN); qg/=norm(qg)
    an = beta**np.arange(S+1)*np.sqrt(FN/fac); an/=norm(an)
    return vac,qg,an

def g2(L,v):
    B=L['B']; I=norm(B@v)**2; Jv=norm(B@B@v)**2
    return Jv/I**2 if I>0 else float('nan')

L8 = ladder(8)
print("\nS=8 K spectrum:", np.round(L8['kw'],6))
print("claimed: -1, 1/8 x2, -3/32 x2 (even) ; -1,1,-3/4,-3/4 (odd); -3/32=%.6f"%(-3/32))
even = [0,2,4,6,8]
print("X even block:\n", np.round(L8['X'][np.ix_(even,even)],6))
print("claimed X[0,0]=55/64=%.6f X[0,1]=5sqrt7/32=%.6f X[0,2]=-sqrt70/64=%.6f"%(55/64,5*7**.5/32,-70**.5/64))
print("Z even block:\n", np.round(L8['Z'][np.ix_(even,even)],6))
print("claimed Z[0,0]=27/64=%.6f Z[0,1]=-9sqrt7/32=%.6f Z[2,2]=-23/32=%.6f"%(27/64,-9*7**.5/32,-23/32))
print("X bins:", Fsign(eigh(-1j*(L8['B'].T-L8['B']))[0]))
print("Z bins:", Fsign(eigh(-np.pi/2*(L8['B'].T+L8['B']))[0]))
for S in (8,32):
    L = ladder(S)
    for name,v in zip(("vac","quasiGlauber","Anderson"), seeds(S)):
        t,mx,my,mz,p = pcorr(L,v)
        eps = norm((L['X']@L['Z']+L['Z']@L['X'])@v)
        print("S=%d %-13s t=%.6f g2=%.9f eps=%.6f p=%.12f  (mx=%.6f my=%.6f mz=%.6f) praw=%.6f"%(S,name,t,g2(L,v),eps,p,mx,my,mz,praw(L,v)))
print("claimed p8(vac)=(959-49sqrt145)/29696=%.13f t=225/232=%.6f mx=1539/1856=%.6f mz=%.6f"%((959-49*145**.5)/29696,225/232,1539/1856,7*1015**.5/1856+7**.5/8))
print("claimed p8(G1)=%.12f p8(A1)=%.12f"%((536363635311-37848641985*145**.5)/293607926091776,(361243454159-29996554273*145**.5)/103543549572096))
# singlet stabilizers check S=8
E,XE,Zt,Yt = L8['E'],L8['XE'],L8['Zt'],L8['Yt']
print("E^2=E:",np.allclose(E@E,E)," Zt^2=E:",np.allclose(Zt@Zt,E)," {XE,Zt}=0:",np.allclose(XE@Zt+Zt@XE,0)," Yt herm:",np.allclose(Yt,Yt.conj().T))

# ---------- displacement defect flat S=8 ----------
from scipy.linalg import expm
for S in (8,32,128):
    L=ladder(S); B=L['B']; v=np.zeros(S+1); v[0]=1
    Qr=-1j*(B.T-B); Qw=-np.pi/2*(B.T+B)
    dD=norm((expm(1j*Qr)@expm(1j*Qw)+expm(1j*Qw)@expm(1j*Qr))@v)
    a=1/np.sqrt(S); be=np.pi/2/np.sqrt(S)
    g=(1-2*np.sin(a)**2*np.sin(be)**2-0.5j*np.sin(2*a)*np.sin(2*be))**S
    Lsc=1+np.pi**2/4
    print("S=%d deltaD direct=%.6f product=%.6f leading pi*sqrt(L+4L^2/9)/S=%.6f"%(S,dD,np.sqrt(2+2*g.real),np.pi*np.sqrt(Lsc+4*Lsc**2/9)/S))

# ---------- oscillator limit ----------
def f(s): return 4/np.pi*sum((-1)**k/(2*k+1)*np.exp(-(2*k+1)**2*s**2/2) for k in range(40))
r=1; print("\nf(1)=%.6f f(pi/2)=%.6f p_inf(1)=%.13f"%(f(1),f(np.pi/2),(1-f(1)**2-f(np.pi/2)**2)/4))
rb=np.sqrt(np.pi/2); print("balanced r: f=%.6f p=%.6f"%(f(rb),(1-2*f(rb)**2)/4))
print("Sorella's claim <X>=<Z>=0.878 -> (1-2*0.878^2)/4 = %.4f"%((1-2*0.878**2)/4))

# ---------- Fig 1 scan ----------
print("\nS   eps_vac   t      p_corr    p_raw")
for S in (4,8,12,16,24,32,48,64,96,128,192,256):
    L=ladder(S); v=np.zeros(S+1); v[0]=1
    t,mx,my,mz,p=pcorr(L,v)
    print("%3d  %.4f  %.4f  %.5f  %.5f"%(S,norm((L['X']@L['Z']+L['Z']@L['X'])@v),t,p,praw(L,v)))
