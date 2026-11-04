import numpy as np, sympy as sp
from numpy.linalg import eigh, norm
# --- (i) sympy check of expansion (11) ---
lam,r,b=sp.symbols('lambda r b',positive=True)
a=r*sp.sqrt(lam); be=b*sp.sqrt(lam)
g=1-2*sp.sin(a)**2*sp.sin(be)**2-sp.I/2*sp.sin(2*a)*sp.sin(2*be)
ser=sp.series(sp.log(g),lam,0,4).removeO()
ser=sp.expand(ser)
L=r**2+b**2
print("coeff lam  :",sp.simplify(ser.coeff(lam,1)), " expected -2 i r b")
print("coeff lam^2:",sp.simplify(ser.coeff(lam,2)), " expected i*4/3*r*b*L =",sp.expand(sp.I*sp.Rational(4,3)*r*b*L))
c3=sp.expand(ser.coeff(lam,3))
print("coeff lam^3 real:",sp.simplify(sp.re(c3))," expected -2r^2b^2L=",sp.expand(-2*r**2*b**2*L))
print("coeff lam^3 imag:",sp.simplify(sp.im(c3))," expected -(4rb(r^4+b^4)/15+20r^3b^3/9)=",sp.expand(-(sp.Rational(4,15)*r*b*(r**4+b**4)+sp.Rational(20,9)*r**3*b**3)))

# --- (ii) bin-edge atoms at perfect squares, convention sensitivity ---
def ladder(S,r=1.0,kappa=0.5,tie=+1.0):
    b=np.pi/(2*r); B=np.zeros((S+1,S+1))
    for n in range(1,S+1): B[n-1,n]=np.sqrt(n*(1-(n-1)/S))
    def binned(Q):
        w,V=eigh(Q); c=np.cos(w); s=np.where(np.abs(c)<1e-9,tie,np.sign(c))
        return ((V*s)@V.conj().T).real, w, c
    X,wx,cx=binned(-1j*r*(B.T-B)); Z,wz,cz=binned(-b*(B.T+B))
    K=(X@Z+Z@X)/2; kw,kV=eigh(K); sel=np.abs(kw)<=kappa+1e-9
    E=kV[:,sel]@kV[:,sel].T; J=(kV[:,sel]/np.sqrt(1-kw[sel]**2))@kV[:,sel].T
    Zt=(Z-K@X)@J; XE=E@X@E; Yt=1j*XE@Zt
    v=np.zeros(S+1); v[0]=1
    t=v@E@v; mx=v@XE@v; my=(v@Yt@v).real; mz=v@Zt@v
    eps=norm((X@Z+Z@X)@v)
    nat=int(np.sum(np.abs(cz)<1e-9))
    return eps,t,0.25*(t**2-mx**2-my**2-mz**2),nat
print("\nS  tie  eps     t      p        #Z-atoms-on-edge")
for S in (16,36,64,100):
    for tie in (+1,-1):
        e,t,p,nat=ladder(S,tie=tie); print("%3d  %+d  %.4f  %.4f  %.6f   %d"%(S,tie,e,t,p,nat))
print("\nlarge-S scan (non-square S), r=1, kappa=1/2")
for S in (300,500,700,1000,1500,2000,3000):
    e,t,p,nat=ladder(S); print("%5d eps=%.4f t=%.4f p=%.5f"%(S,e,t,p))
# kappa dependence at S=8 and S=32
print("\nkappa dependence")
for S in (8,32):
    for k in (0.2,0.35,0.5,0.7,0.9):
        e,t,p,nat=ladder(S,kappa=k); print("S=%d kappa=%.2f t=%.4f p=%.6f"%(S,k,t,p))
# balanced r at S=8
e,t,p,nat=ladder(8,r=np.sqrt(np.pi/2)); print("\nS=8 balanced r: eps=%.4f t=%.4f p=%.6f"%(e,t,p))
