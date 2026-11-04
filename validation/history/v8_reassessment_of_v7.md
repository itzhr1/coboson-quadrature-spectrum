# Reassessment of v7 and changes made in v8

30 October 2026. Base: the v7 bundle (`coboson_paper_v7_bundle.zip`). Output: `coboson_paper_v8_repo.zip` (repository-ready tree), `coboson_paper_v8.pdf` (25 pp.), `undergrad_version_v8.pdf` (30 pp.).

## 1. What v7 changed, and whether it holds

Every v7 change was re-derived from the data or by calculation before being kept.

| v7 change | Check | Verdict |
|---|---|---|
| Certified fidelity bounds rounded **down** to three decimals (0.676, 0.625, 0.748, 0.830, 0.822, 0.874, 0.896) and the trivial baseline $\max\{1/2,\cdot\}$ written into Eq. (selftest). | Recomputed from `bell_raw_scan.json` / `bell_raw_8000.json` with $\mathcal B^*=(16+14\sqrt2)/17$: 0.67608985, 0.62543192, 0.74825869, 0.83031839, 0.82242054, 0.87499685, 0.89698693. v6's "0.68 at $S=8$" was indeed a lower bound rounded upward. | Correct; kept. |
| "$\kappa=0.4$ quantities vary by approximately 1–3.5%"; Table 3 caption restricted to preparation probabilities. | Spans over $S=13$–$19$ from `legacy_nonflat_scan.json`: $p_{0.6}$ 0.36% / 1.56%, $p_{0.4}$ 2.7% / 3.5%, $t_{0.4}$ 0.9% / 1.0%, $t_{0.6}$ 0.09% / 0.08% ($z=0.5$ / $0.6$). | Correct; kept. |
| Proposition 2: explicit hypotheses (normalised infinite sequence, $\lambda_k>0$, $\sum\sqrt{\lambda_k}<\infty$, fixed $r$, $b$) and the bounded cutoff function $g_\kappa(k)=\mathbf 1_{[-\kappa,\kappa]}(k)/\sqrt{1-k^2}$. | $g_\kappa$ is bounded, Borel and continuous except at $\pm\kappa$, so $g_\kappa(K_S)\to g_\kappa(K_\infty)$ strongly under exactly the hypothesis already needed for the projector. The restated $\widetilde Z_S=(Z_S-K_SX_S)g_\kappa(K_S)$ is the v6 definition. | Correct; a clearer proof, same theorem. Kept. |
| Introduction and conclusions aligned with Proposition 2 ("all but countably many cutoffs"; the specific cutoffs, positivity and a rate open); "summable Schmidt amplitudes", not weights. | Consistent with Sec. 7. | Kept. |
| Fig. 5 split into aligned panels: (a) probabilities on a 0–5% scale, (b) the bound $C(\kappa)$ with guides at 0.4 and 0.6. | $C(0.4)=\sqrt{2(1-\sqrt{0.84})}=0.4086$, $C(0.6)=0.6325$; the curve is drawn as $(\sin t,\,2\sin(t/2))$, which is $C(\kappa)$ exactly; the 50 stored points pass the independent check (`verify_cutoff_curves.py`, max discrepancy $4\times10^{-15}$); the generator reproduces the block in both files. | The split is an improvement: the old dual axis mixed a model probability with a universal bound and wasted half the plot. Kept; the legend is set in one row (cosmetic). |
| Fig. 2 caption: $\Delta=2\hat N/S$ "tends to zero at fixed pair number". | $\Delta=2\sum\lambda_kn_k=2\hat N/S$ for the flat spectrum. | Correct; kept. |
| $g^{(2)}$ wording (Sec. 8): "consistent with a coherent field, but does not by itself characterize a coherent state". | — | Kept. |
| Physical-scales paragraph stripped of all numerical assignments. | Defensible, but it removed the orientation the earlier passes had added on purpose. | **Partly reversed**: v7's caveats stay (a cutoff $S$ is not a coherence length or an inverse purity; a specific system needs its Schmidt decomposition) and one sentence of qualified orientation is restored (aggregate coherence lengths of a few to $10^2$ sites; Schmidt number of a Wannier exciton from near 1 under strong confinement to of order 10 in a small dot and large in bulk, cf. the trapped-pair estimates of Law 2005). |
| New abstract (210 words). | Content is right, but longer than the ≤200 words asked for earlier. | **Shortened to 192 words**, same content. |
| Sec. 5.2: "whenever $p>0$" removed from the CHSH sentence. | The sentence describes the singlet state itself; the condition remains in Sec. 6 and the captions. | Kept. |

## 2. Residual issues found in v7 and fixed in v8 (both versions)

- Conclusions still said the singlet comes from entanglement "between the resolved qubit and the **unresolved pair structure**" — the reading corrected in Sec. 1 and 5.2 since v6. Now "its complementary logical factor".
- Conclusions: "a classical drive responds to the **low harmonics**" → "is the fundamental harmonic", as elsewhere.
- Conclusions: "the protocol succeeds for all sufficiently large **aggregates**" → "flat-spectrum ranks", consistent with the v7 physical-scales paragraph; "the lattice of signed sums, which an elementary boson does not have" qualified to finite Schmidt rank.

No number, data file or table changed. Pages: 25 and 30 (the annotated version's bibliography now spills onto a last page).

## 3. Repository preparation

The package is now a self-contained tree that can be pushed as-is (`git init` has deliberately not been run):

```
README.md  LICENSE  CITATION.cff  CHANGELOG.md  .gitignore  requirements.txt  reproduce.sh  SHA256SUMS
.github/workflows/tests.yml   (tests + generator check + Fig. 5 check on Python 3.11–3.13)
manuscript/   sources, PDFs, standalone Fig. 5 (tex + pdf)
code/         scripts, tests.py (16), independent/ (5 scripts + stored results)
data/         14 JSON files + data/README.md documenting every file and field
validation/   v8 records (tests.log, validation.json, provenance.json with hashes of sources, code and data,
              figure5_checks.json, independent_review_results.json) and history/ (v6, v7 records,
              the two independent reviews and the responses)
```

`./reproduce.sh` was run from the root: 16/16 tests, all ten blocks of both manuscripts regenerate unchanged, the Fig. 5 check passes, and the rerun independent review agrees with the v7 record to $10^{-9}$. Data files are byte-identical to v5–v7.

## 4. Decisions left to the authors

1. Author and affiliation lines (both manuscripts, `CITATION.cff` — currently one name).
2. Licence: MIT for code and data is a default; the manuscript sources are marked all-rights-reserved pending publication.
3. Whether to keep `validation/history/` (the review documents mention the assistants by name) in the public repository, or only in the private record.
4. Hosting (GitHub/Zenodo): once a DOI exists, add it to `CITATION.cff` and Appendix E.
