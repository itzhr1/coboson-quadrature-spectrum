"""Independently verify every archived Figure 5 point using direct quadratures.
No production calculation modules are imported. Run from any directory.
"""
from pathlib import Path
import json, sys
import numpy as np
import scipy
from scipy.linalg import eigh
ROOT = Path(__file__).resolve().parents[2]

def bins(q):
    w, u = eigh(q)
    c = np.cos(w)
    c[np.abs(c) < 1e-12] = 0  # manuscript's positive bin-edge convention
    return (u * np.where(c >= 0, 1, -1)) @ u.conj().T

def quadratures(key):
    family, parameter = key.rsplit('_', 1)
    if family == 'flat':
        n = int(parameter)
        b = np.diag(np.sqrt(np.arange(1, n+1) * (1-np.arange(n)/n)), 1)
        indices = np.arange(0, n+1, 2)
    else:
        n = 8
        a = float(parameter)
        weights = a**np.arange(n) if family == 'geometric' else (1+(np.arange(1,n+1)/a)**2)**-4
        weights /= weights.sum()
        b = np.zeros((2**n, 2**n))
        for k, weight in enumerate(weights):
            for j in range(2**n):
                if j & (1 << k):
                    b[j ^ (1 << k), j] = np.sqrt(weight)
        indices = [j for j in range(2**n) if j.bit_count() % 2 == 0]
    x = bins(-1j*(b.T-b))[np.ix_(indices, indices)]
    z = bins(-np.pi/2*(b.T+b))[np.ix_(indices, indices)]
    return x, z

def main():
    curves = json.loads((ROOT/'data/cutoff_curves.json').read_text())
    result = {'runtime': {'python':sys.version.split()[0], 'numpy':np.__version__, 'scipy':scipy.__version__}, 'curves': {}}
    for key, rows in curves.items():
        x, z = quadratures(key)
        k = (x@z+z@x)/2
        w, u = eigh(k)
        discrepancies = []
        probabilities = []
        for row in rows:
            cutoff = row['kappa']
            keep = np.abs(w) <= cutoff
            e = u[:,keep] @ u[:,keep].conj().T
            g = (u[:,keep]/np.sqrt(1-w[keep]**2)) @ u[:,keep].conj().T
            xx, zz = e@x, (z-k@x)@g
            yy = 1j*xx@zz
            # Apply the two-party singlet projector directly to |0,0>.
            vecs = [a[:,0] for a in [e, xx, yy, zz]]
            state = sum(s*np.outer(v,v) for s,v in zip([1,-1,-1,-1], vecs))/4
            probability = float(np.linalg.norm(state)**2)
            probabilities.append(probability)
            discrepancies.append(abs(probability-row['p']))
            assert abs(e[0,0].real-row['t']) < 2e-10
            assert abs(np.sqrt(2*(1-np.sqrt(1-cutoff**2)))-row['bound']) < 1e-12
        assert max(discrepancies) < 2e-10, (key, max(discrepancies))
        assert min(np.diff(probabilities)) > -2e-12, key
        result['curves'][key] = {'points':len(rows), 'max_probability_discrepancy':max(discrepancies), 'monotone':True}
    result['passed'] = True
    (ROOT/'validation/figure5_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
