"""Run with: python -m unittest discover -s code -p tests.py -v"""
import unittest
import numpy as np
from numpy.linalg import norm
from scipy.linalg import expm,eigh
from nonflat import Binned,geometric,algebraic_profile,corrected_exact,corrected_lanczos,vacuum,deltaD,correction_bound,Fsign,raw_quantities
from flatscan import run,matrices
from make_assets import harmonic


def direct_operators(lam):
    n=2**len(lam);B=np.zeros((n,n))
    for k,l in enumerate(lam):
        mask=1<<(len(lam)-1-k)
        for j in range(n):
            if j&mask:B[j^mask,j]+=np.sqrt(l)
    return B


def spectral_bin(Q):
    w,U=eigh(Q);return (U*Fsign(w))@U.conj().T


class MathematicsTests(unittest.TestCase):
    def test_harmonic_product_against_direct_dicke_matrices(self):
        S=16
        B=np.diag(np.sqrt(np.arange(1,S+1)*(1-np.arange(S)/S)),1)
        Qr=-1j*(B.T-B);Qw=-np.pi/2*(B.T+B)
        def cos_matrix(Q,k):
            w,U=eigh(Q);return (U*np.cos(k*w))@U.conj().T
        for m,n in [(0,0),(3,0),(0,3),(3,3)]:
            X=cos_matrix(Qr,2*m+1);Z=cos_matrix(Qw,2*n+1)
            self.assertAlmostEqual(harmonic(S,m,n),norm((X@Z+Z@X)[:,0]),places=12)

    def test_complex_linear_transform_against_direct_quadratures(self):
        lam=np.array([.49,.01,.25,.25]);B=direct_operators(lam);X=spectral_bin(-1j*(B.T-B));Z=spectral_bin(-np.pi/2*(B.T+B));bn=Binned(lam)
        v=np.arange(16)+1j*np.arange(16)[::-1];v/=norm(v)
        np.testing.assert_allclose(bn.X(v),X@v,atol=3e-14);np.testing.assert_allclose(bn.Z(v),Z@v,atol=3e-14)
        np.testing.assert_allclose(bn.X(1j*v),1j*bn.X(v),atol=1e-14)

    def test_displacement_against_exponentials(self):
        for lam in [np.array([.49,.01,.25,.25]),geometric(5,.7)]:
            B=direct_operators(lam);U=expm(B.T-B);V=expm(-1j*np.pi/2*(B.T+B));v=vacuum(len(lam))
            self.assertAlmostEqual(deltaD(lam),norm((U@V+V@U)@v),places=12)

    def test_equal_moment_examples(self):
        a=np.array([.49,.01,.25,.25]);b=np.array([.442,.058,.394,.106])
        for p in [2,3]:self.assertAlmostEqual(sum(a**p),sum(b**p),places=14)
        for lam,e,p in [(a,1.,3/32),(b,2.5,23/128)]:
            eps,praw,*_=raw_quantities(Binned(lam));self.assertAlmostEqual(eps**2,e,places=13);self.assertAlmostEqual(praw,p,places=13)

    def test_eight_mode_and_zero_cutoff(self):
        a=run(8);self.assertAlmostEqual(a['p'],(959-49*np.sqrt(145))/29696,places=13)
        self.assertAlmostEqual(corrected_exact(Binned(np.ones(8)/8))['p'],a['p'],places=13)
        self.assertAlmostEqual(run(8,kappa=.05)['t'],0.,places=13)

    def test_edge_conventions_and_mass(self):
        plus,minus=run(16),run(16,tie=-1)
        self.assertEqual(plus['naz'],4);self.assertAlmostEqual(plus['edge_mass_z'],127/512,places=13)
        self.assertAlmostEqual(plus['p'],2.4047371424e-5,places=13);self.assertAlmostEqual(minus['p'],0.,places=13)
        self.assertGreater(run(16,r=1-1e-8)['p'],.005)

    def test_dense_lanczos_and_signed_targets(self):
        b=Binned(geometric(8,.7));a=corrected_exact(b,kappa=.6);c=corrected_lanczos(b,kappa=.6,m=128)
        for key in ['t','mx','mz','p']:self.assertAlmostEqual(a[key],c[key],places=11)
        self.assertAlmostEqual(a['near_target_weights']['-0.5'],.225,places=11)
        self.assertIn('0.5',a['near_target_weights']);self.assertLess(a['eigen_residual_inf'],1e-11)

    def test_pauli_projector_and_nested_cutoffs(self):
        X,Z,_,_=matrices(8);K=(X@Z+Z@X)/2;w,U=eigh(K);previous=None
        for k in [.05,.1,.2,.6,.9]:
            sel=abs(w)<=k;E=U[:,sel]@U[:,sel].T;J=(U[:,sel]/np.sqrt(1-w[sel]**2))@U[:,sel].T
            xe=E@X;zt=(Z-K@X)@J;yt=1j*xe@zt
            P=(np.kron(E,E)-np.kron(xe,xe)-np.kron(yt,yt)-np.kron(zt,zt))/4
            np.testing.assert_allclose(P@P,P,atol=3e-14)
            if previous is not None:np.testing.assert_allclose(previous@P,previous,atol=3e-14)
            previous=P

    def test_smooth_bounds_and_sign_margin(self):
        b=Binned(np.ones(8)/8);n=256;I=np.eye(n)
        X=np.column_stack([b.X(v) for v in I]);Z=np.column_stack([b.Z(v) for v in I]);v=vacuum(8)
        eta=.05;Xe=np.column_stack([b.smooth_X(v,eta) for v in I]);Ze=np.column_stack([b.smooth_Z(v,eta) for v in I])
        hx=1-np.tanh(np.sin(b.margin_x)/eta);hz=1-np.tanh(np.sin(b.margin_z)/eta)
        self.assertLessEqual(norm(Xe-X,2),hx+2e-13);self.assertLessEqual(norm(Ze-Z,2),hz+2e-13)
        self.assertLessEqual(abs(norm((Xe@Ze+Ze@Xe)@v)-norm((X@Z+Z@X)@v)),2*(hx+hz)+1e-12)
        # Both scales perturb within the calculated bin margin.
        bp=Binned(np.ones(8)/8,r=1.001);np.testing.assert_array_equal(b.xsign,bp.xsign);np.testing.assert_array_equal(b.zsign,bp.zsign)

    def test_mixedness_and_K_measure_not_sufficient(self):
        X=np.kron([[0,1],[1,0]],np.eye(2));Z=np.kron(np.diag([1,-1]),np.eye(2));Y=1j*X@Z
        np.testing.assert_allclose(X@Z+Z@X,0)
        product=np.array([1,1,0,0])/np.sqrt(2);entangled=np.array([1,0,0,1])/np.sqrt(2)
        for v,expected in [(product,0),(entangled,.25)]:
            rho=v.reshape(2,2)@v.reshape(2,2).T;p=(1-sum(abs(np.vdot(v,A@v))**2 for A in [X,Y,Z]))/4
            self.assertAlmostEqual(p,expected,places=14);self.assertAlmostEqual(p,(1-np.trace(rho@rho))/2,places=14)

    def test_field_correlation(self):
        for S in [2,3,8]:
            B=np.diag(np.sqrt(np.arange(1,S+1)*(1-np.arange(S)/S)),1)
            for beta in [.5,1.,2.]:
                v=expm(beta*B.T)[:,0];v/=norm(v);q=beta**2/(S+beta**2)
                I=S*q-(S-1)*q*q
                J=(S-1)/S*q*q*(S*(S-1)-2*(S-1)*(S-2)*q+(S-2)*(S-3)*q*q)
                self.assertAlmostEqual(norm(B@B@v)**2/norm(B@v)**4,J/I**2,places=12)

    def test_bound_values_and_no_qubit_model(self):
        self.assertAlmostEqual(correction_bound(.3),.303515398565,places=11);self.assertAlmostEqual(correction_bound(.8),.8944271909999,places=11)
        b=Binned(algebraic_profile(8,2.));self.assertTrue(np.all(b.xsign==1));self.assertAlmostEqual(corrected_exact(b,kappa=.6)['p'],0.,places=13)

    def test_reject_invalid_input(self):
        for a in [[.2,.3],[1.,0.],[-1.,2.]]:
            with self.assertRaises(ValueError):Binned(a)
        for k in [0,1,-.2]:
            with self.assertRaises(ValueError):correction_bound(k)




class BellRawTests(unittest.TestCase):
    """Bob-optimised CHSH value of the raw sequential state (code/bell_raw.py).  Reference values: the
    independent implementation of the 30 October 2026 review (rank-4, 2.73205080757 = 1+sqrt 3 and
    2.14431716999) and the archived scan data/bell_raw_scan.json (flat ranks)."""

    @staticmethod
    def bell_from_operators(X, Z):
        from scipy.linalg import eigvalsh
        n = X.shape[0]; v = np.zeros(n); v[0] = 1.
        z = Z@v; x = X@v; xz = X@z
        M = .25*(np.outer(v, v)-np.outer(z, z)-np.outer(x, x)+np.outer(xz, xz))
        p = float(np.trace(M.T@M)); Psi = M/np.sqrt(p); B = 0.
        for A in (X+Z, X-Z):
            H = Psi.T@A.T@Psi; H = (H+H.T)/2; B += float(np.abs(eigvalsh(H)).sum())
        return p, B

    def test_rank4_examples_against_independent_values(self):
        for lam, praw_ref, bell_ref in [([.49,.01,.25,.25], 3/32, 1+np.sqrt(3)),
                                        ([.442,.058,.394,.106], 0.1796875, 2.144317169988418)]:
            B = direct_operators(np.array(lam)); X = spectral_bin(-1j*(B.T-B)).real; Z = spectral_bin(-np.pi/2*(B.T+B)).real
            p, bell = self.bell_from_operators(X, Z)
            self.assertAlmostEqual(p, praw_ref, places=12); self.assertAlmostEqual(bell, bell_ref, places=10)

    def test_flat_ranks_against_archived_scan(self):
        from bell_raw import bell_raw
        for S, tie, praw_ref, bell_ref in [(8, 1., 0.0484732389450073, 2.360309460483011),
                                           (16, 1., 0.0513156486325029, 2.378562718802744),
                                           (16, -1., 0.09236869043780165, 2.4171508355777),
                                           (17, 1., 0.04472949627363933, 2.0876518809139695),
                                           (64, -1., 0.12090279326933334, 2.295609868289806)]:
            row = bell_raw(S, tie=tie)
            self.assertAlmostEqual(row['praw'], praw_ref, places=12); self.assertAlmostEqual(row['bell_raw'], bell_ref, places=10)

    def test_corrected_protocol_is_tsirelson_when_p_positive(self):
        # Flat S=8, kappa=1/2: the corrected observables X_E, Z~ anticommute on the retained sector, the
        # singlet projector P_- = (E E - X X - Y Y - Z~ Z~)/4 with Y = i X Z~ has positive vacuum weight, and
        # the Bob-optimised CHSH value of the prepared state is 2 sqrt 2.
        from scipy.linalg import eigvalsh
        X, Z, q, V = matrices(8, 1., 1.); K = .5*(X@Z+Z@X); w, U = eigh(K); sel = np.abs(w) <= .5
        Us = U[:, sel]; E = Us@Us.T; XE = E@X@E; Zt = (Z-K@X)@(Us*(1-w[sel]**2)**-.5)@Us.T
        np.testing.assert_allclose(XE@Zt+Zt@XE, 0, atol=1e-12)
        XZ = XE@Zt   # Y = i XZ, so Y (x) Y = -(XZ) (x) (XZ)
        Pm = .25*(np.kron(E, E)-np.kron(XE, XE)-np.kron(Zt, Zt)+np.kron(XZ, XZ))
        v = np.zeros(9); v[0] = 1.; vv = np.kron(v, v); psi = Pm@vv; p = float(vv@psi)
        self.assertAlmostEqual(p, 0.012424631790112, places=12)
        Psi = (psi/np.sqrt(p)).reshape(9, 9); B = 0.
        for A in (XE+Zt, XE-Zt):
            H = Psi.T@A.T@Psi; H = (H+H.T)/2; B += float(np.abs(eigvalsh(H)).sum())
        self.assertAlmostEqual(B, 2*np.sqrt(2), places=10)


if __name__ == '__main__':
    unittest.main(verbosity=2)
