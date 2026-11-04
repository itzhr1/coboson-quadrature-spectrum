"""Bob-optimised CHSH value of the raw sequential state (Appendix A protocol) for the flat spectrum, vacuum initial state.
B_opt = ||H_+||_1 + ||H_-||_1 with H_pm = Psi^T (X pm Z)^T Psi^*, Psi the normalised coefficient matrix of
Pi_X^- Pi_Z^- |00>.  Both tie conventions at perfect squares."""
import argparse, json, time
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from flatscan import matrices

def bell_raw(S, r=1., tie=1.):
    X, Z, q, V = matrices(S, r, tie); v = np.zeros(S+1); v[0] = 1.
    z = Z@v; x = X@v; xz = X@z
    M = 0.25*(np.outer(v, v)-np.outer(z, z)-np.outer(x, x)+np.outer(xz, xz))
    p = float(np.trace(M.T@M)); Psi = M/np.sqrt(p)
    B = 0.
    for A in (X+Z, X-Z):
        H = Psi.T@A.T@Psi; H = (H+H.T)/2; B += float(np.abs(eigvalsh(H)).sum())
    return dict(S=int(S), tie=tie, praw=p, bell_raw=B)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ranks', type=int, nargs='*', default=None); ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    ranks = a.ranks or sorted(set(list(range(4, 401))+list(range(404, 2001, 4))+[int(round(x)) for x in np.geomspace(2050, 4096, 12)]))
    rows = []
    for S in ranks:
        t0 = time.time(); rows.append(bell_raw(S))
        if int(round(np.sqrt(S)))**2 == S: rows.append(bell_raw(S, tie=-1.))
        print(S, '%.4f' % rows[-1]['bell_raw'], '%.1fs' % (time.time()-t0), flush=True)
        if S % 100 == 0 or S > 2000: a.output.write_text(json.dumps(rows, indent=1))
    a.output.write_text(json.dumps(rows, indent=1))
