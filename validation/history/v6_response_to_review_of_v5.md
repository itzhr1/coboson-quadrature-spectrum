# Response to the independent assessment of v5 (Codex/Astra, 30 October 2026)

Revision produced: **v6** — `coboson_paper_v6.tex` (25 pp.), `undergrad_version_v6.tex` (29 pp.), `coboson_paper_v6_bundle.zip`. Every claim of the assessment was checked against the archived data or by calculation before being acted on. Line numbers below refer to the v6 sources; "both" means the edit was made identically in both versions. No data file, figure block or table value changed; the generator reproduces all ten marked blocks of both files (`validation/validation.json`).

Legend: **A** accepted and applied · **A\*** accepted with a different wording than proposed · **D** disagreed, with reasons · **O** open (noted in the text as such).

---

## 1. Measurement statistics versus coherent preparation

| # | Review claim | Status | What was done / evidence |
|---|---|---|---|
| 1.1 | Binned homodyne *statistics* define the observables; singlet preparation needs coherent spectral filtering and heralded joint projections, which homodyne + classical binning does not implement. | **A** | Abstract (both, l. 34/35): "whose statistics define a pair of Pauli-like observables from which, with coherent spectral filtering and a heralded joint projection, a spin singlet is extracted". Sec. 4 opening (main l. 186 region): new sentence stating that the preparation protocols assume Lüders projections onto joint eigenspaces of $Z\otimes Z$, $X\otimes X$, "which ordinary homodyne detection followed by classical binning does not implement". Appendix A: the raw protocol is now described as "projective (Lüders) measurement of the two-party observable $Z\otimes Z$ followed by that of $X\otimes X$ … joint projections onto the $-1$ eigenspaces, not local binned measurements followed by classical post-selection". |
| 1.2 | A CHSH value of $2\sqrt2$ certifies state and observables on the support, up to local isometries, not the internal implementation. | **A** | Sec. 5.2 (both): "…a Pauli pair on its support, up to local isometries; a Bell test therefore verifies the output of an implementation of the filter and polar correction, though not the internal operations that produced it." |
| 1.3 | Add "whenever the preparation probability is nonzero" to the CHSH statements. | **A** | Added in Sec. 5.2 (the $2\sqrt2$ sentence), Sec. 6 ("prepares, whenever $p>0$, an exact singlet"), Table 1 caption ("at every rank with $p_{\rm corr}>0$") and Fig. 3 caption ("at every rank with $p>0$"). |

## 2. Numerical prose

| # | Review claim | Verified? | Status | What was done |
|---|---|---|---|---|
| 2.1 | "numerically established to three digits" is too strong: over $S=13$–$19$, $p_{0.6}$ spans $4.4\times10^{-5}$ ($0.36\%$) at $z=0.5$ and $3.9\times10^{-4}$ ($1.56\%$) at $z=0.6$; $t_{0.4}$ spans $2.8\times10^{-3}$ and $5.3\times10^{-3}$. | Yes, from `legacy_nonflat_scan.json` (same numbers). | **A** | Sec. 7 (both): "$p_{0.6}$ varies by $4\times10^{-5}$ ($0.4\%$ of its value …) at $z=0.5$ and by $4\times10^{-4}$ ($1.6\%$) at $z=0.6$, $t_{0.6}$ by $6\times10^{-4}$ in both cases, and the $\kappa=0.4$ quantities by $1$–$3\%$. This is finite-window stability at the percent level, not a certified value of an infinite-mode limit." Table 3 caption: "the entries vary by $0.4$–$3\%$ over $13\le S\le19$". Conclusions: "stable at the percent level". |
| 2.2 | Fig. 4 caption: "stays finite", "infinite-mode composites" overstate. | — | **A** | Caption now: "remains at the percent level over the computed truncations" and "these are $19$-mode truncations of infinite-mode spectra … consistent with nonzero limits (Proposition 2 and the discussion below)". |
| 2.3 | "Schmidt number three" → 3.00 in a 19-mode truncation. | $\mathcal K_{19}=3.0000$ at $z=0.5$ (Table 3). | **A** | Introduction (both): "Schmidt number $3.00$ (a $19$-mode truncation of a geometric spectrum)". Abstract keeps "Schmidt number three" for brevity. |
| 2.4 | "for every $S\ge64$ the bound is at least $0.64$" is wrong with the $-$ convention at $S=64$ ($0.6313$); minimum of the $+$ convention is $0.6425$ at $S=71$. | Yes: `bell_raw_scan.json`, Kaniewski bound with $\mathcal B^*=(16+14\sqrt2)/17$. | **A** | Sec. 6 (both): "for every sampled rank $S\ge64$ with the $+1$ edge convention it is at least $0.64$ (the minimum, $0.642$, is at $S=71$; with the $-1$ convention the $S=64$ value is $0.631$)". |
| 2.5 | Define fidelity as extractability up to local isometries. | — | **A** | Sec. 6: "singlet extractability — the fidelity to a two-qubit singlet attainable by local isometries that may discard auxiliary degrees of freedom, not the overlap with a particular singlet vector in the original space". Undergraduate version: same content as a separate sentence. |
| 2.6 | "nothing is certified at $S=17$" → no improvement over the trivial $1/2$. | — | **A** | "the bound gives nothing beyond the trivial value $1/2$ (it is a bound, not evidence against entanglement)". |
| 2.7 | Table 2 caption wrong: $w=4$ has $p_{0.6}=0.598\%<1\%$; four of six exceed $1\%$. | Yes (`fresh_dense_nonflat.json`). | **A** | Caption: "at $\kappa=0.6$ four of the six yield a singlet with probability above $1\%$, the two most concentrated algebraic spectra ($w=3$, $\mathcal K=1.9$; $w=4$, $\mathcal K=2.6$) below it". |
| 2.8 | "$p_{\rm raw}$ is $5$–$13\%$ throughout" wrong: $2.6\%$ ($S=13$) to $13.5\%$ ($S=58$). | Yes (`bell_raw_scan.json`: min 0.0259 at 13, max 0.1352 at 58). | **A** | "lies between $2.6\%$ (at $S=13$) and $13.5\%$ (at $S=58$) over the ranks of Fig. 2(b), and above $6.9\%$ for $S\ge256$" (checked: min over $S\ge256$ is $0.0692$). |

## 3. Qualitative claims

| # | Review claim | Status | What was done |
|---|---|---|---|
| 3.1 | "commutator a third away from unity" is wrong: on the one-pair state $\langle\Delta\rangle=2P=2/3$; the quantity that is $1/3$ below unity is $F_2/F_1=1-P$. | **A** (verified: $\langle1|\Delta|1\rangle=2\sum\lambda_k^2=2P$) | Introduction and closing paragraph (both): "normalisation ratio $F_2/F_1=1-P$ a third below unity". Fig. 2 caption: "commutator deviation $\Delta$". |
| 3.2 | "no finite set of moments determines them" — only purity and the third moment were shown. | **A** | "the purity and the third moment do not determine them" (Introduction, both). |
| 3.3 | "drive is a low-order function / sees first few moments" — the drive is a smooth fundamental-harmonic probe with a controlled dilute expansion. | **A** | Introduction, abstract, Sec. 3 closing sentence and Fig. 1 caption rewritten in those terms ("a smooth probe — the fundamental harmonic of the quadrature — … real-analytic … dilute expansion controlled by the first Schmidt moments"; Fig. 1: "the characteristic function at one frequency, a smooth functional dominated in the dilute regime by the first moments"). |
| 3.4 | "lattice with $2^S$ points … Cantor-like": $2^S$ signed sums with multiplicity, $S+1$ distinct values for the flat spectrum; support an interval for $\sqrt z\ge1/2$. | **A\*** | Introduction: "$2^S$ values counted with multiplicity … for a flat spectrum reduce to $S+1$ equally spaced points … for a localised spectrum with infinitely many modes fill an interval or a Cantor set, depending on how fast the weights decrease, with a spectral measure that has no atoms". Sec. 4: "counted with multiplicity". The word "lattice" is kept for the flat case and in figure labels, where it is accurate. |
| 3.5 | Keep the explicit criterion $\sum_k\sqrt{\lambda_k}<\pi/2$; do not suggest purity alone decides. | **A** | Introduction: "vanishes identically when the spectrum is so concentrated that $\sum_k\sqrt{\lambda_k}<\pi/2$ at $r=1$, for then one binned quadrature is the identity"; Conclusions: "an explicit condition on the amplitudes, which near-unit purity alone does not imply". |
| 3.6 | The multiplicity factor $\mathcal M$ is an observable-defined logical subsystem, not a constituent subsystem; the oscillator has the same structure; no pre-existing Alice–Bob entanglement is implied. | **A** | Sec. 5.2 paragraph rewritten: "$\mathcal M$ is a logical subsystem defined by the two observables — the label of the Jordan block — not a spatial or constituent subsystem; … the same structure exists for the elementary oscillator, whose vacuum has a reduced-qubit Bloch length $0.85$. What is specific to the composite is how the block weights, and with them $t$ and $p$, depend on the Schmidt spectrum." Second introductory conclusion reworded in the same way. (Bloch length $0.85$: for the oscillator $X$ and $Z$ anticommute exactly, so $t=1$ and $|\vec m|=\sqrt{f(1)^2+f(\pi/2)^2}=\sqrt{0.7675^2+0.3708^2}=0.852$ from the Sec. 9 constants.) |
| 3.7 | Physical scales are heuristics; no claim that polariton light directly measures the quadrature spectrum. | **A** | Sec. 2: "These are order-of-magnitude assignments: finite Schmidt rank, inverse purity, coherence length and sample size are related but not interchangeable … Whether the quadrature spectrum of a given composite is accessible to homodyne detection … depends on a coupling model between the composite field and the detected field that we do not supply." |

## 4. Infinite-mode limit

| # | Review claim | Status | What was done |
|---|---|---|---|
| 4.1 | Replace the Bernoulli-convolution absolute-continuity argument by a nonatomicity lemma plus strong convergence for all vectors and all but countably many cutoffs. | **A** (argument checked step by step; one detail corrected, see 4.2) | Sec. 7 (both): **Lemma 2** (law of $\sum a_k\varepsilon_k$ with summable $a_k$ has no atoms; proof by a subsequence with $b_{j+1}<b_j/4$, injectivity of the sign-to-sum map, convolution) and **Proposition 2** (vacuum incomplete tensor product $\cong L^2(\{\pm1\}^{\mathbb N},\mu)$ via the local $\sigma_x$ basis; $Q_w^{(\infty)}$ is multiplication by $-bq(\varepsilon)$; every vector's spectral measure is absolutely continuous w.r.t. the vacuum's; uniform convergence $\sup|q_S-q|\le(\sum a_k)|(\sum_{j\le S}\lambda_j)^{-1/2}-1|+\sum_{k>S}a_k$; dominated convergence gives $Z_S\to Z_\infty$ strongly; $X_S$ by the unitary of 4.2; products give $K_S$; spectral projector and polar factor converge when $\pm\kappa$ are not eigenvalues of $K_\infty$; countably many exceptions). The Bernoulli references are kept in one parenthetical sentence. Conclusions and the open-questions paragraph updated. Undergraduate version: a new Background paragraph (spectral measures, atoms, coin-toss sums) precedes the lemma and says explicitly that only nonatomicity is used. |
| 4.2 | (Detail of 4.1.) The $Q_r$ case. | **A\*** | The review's sketch uses a diagonal unitary; the exact identity is $Q_r=(r/b)\,i^{\hat N}Q_w\,i^{-\hat N}$ (sign $+$; checked numerically on three modes to machine precision and stated with its derivation, $i^{\hat N}(B^\dagger+B)i^{-\hat N}=i(B^\dagger-B)$). |
| 4.3 | Retain the unresolved specific-cutoff and positivity questions. | **O** | Stated after Proposition 2: no proof that $0.4$, $0.6$ are not eigenvalues of $|K_\infty|$ for the spectra of Table 3, no proof of positivity, no rate; existence and positivity of the Table 3 limits remain a conjecture. Listed in `validation.json` under limitations. |

## 5. Undergraduate version

| # | Review claim | Verified? | Status | What was done |
|---|---|---|---|---|
| 5.1 | Weyl background: $D(z)D(w)=e^{(zw^*-z^*w)/2}D(z+w)$, hence $D(z)D(w)=e^{zw^*-z^*w}D(w)D(z)$; phase $e^{+2irb}=-1$. | Yes (BCH). | **A** | Both formulas and the sign corrected (l. 153). |
| 5.2 | $Q_r=-ir(a^\dagger-a)=-r\sqrt2\,\hat p$, not $+$; vacuum variances $1/2$, rescaled $r^2$, $b^2$. | Yes. | **A** | Displacement background rewritten with $\hat x,\hat p$ defined explicitly, the sign, and the variances (l. 112). |
| 5.3 | "nested commutators … none of which vanish on the vacuum" is false: $[B,[B,B^\dagger]]=-2\sum\lambda_k^{3/2}d_k$ annihilates the vacuum. | Yes. | **A** | Sec. 2 (undergraduate): the sentence now says the BCH series of two rotations brings in $[\Delta,B^\dagger]=2\sum\lambda_k^{3/2}d_k^\dagger$ etc., "which do not vanish on the vacuum ($[\Delta,B^\dagger]\ket0\neq0$) and are not numbers. (Individual nested commutators such as $[B,[B,B^\dagger]]$ do annihilate the vacuum; it is the full series that fails to collapse to a phase.)" The research version's weaker sentence was adjusted to the same statement. |
| 5.4 | Functions-of-an-operator box: same statistics, not the same post-measurement state. | — | **A** | Box now distinguishes the two procedures and says Sec. 5 uses the projective measurement of $F(Q)$. |
| 5.5 | Jordan box: $XK=(Z+XZX)/2=KX$ (the printed line was garbled); degenerate $K$-eigenspaces contain many blocks. | — | **A** | Both corrected (l. 301). |
| 5.6 | Temper "$g^{(2)}=1$ is the standard test of a coherent field". | — | **A** | "a standard signature of a coherent field — a necessary condition, satisfied also by some states that are not coherent, as Sec. 8 exploits". |
| 5.7 | Label "annotated advanced-undergraduate version" and give a reading route. | — | **A** | Paragraph "About this version (annotated advanced-undergraduate version)" with a suggested first-reading route; `\date{Annotated version v6}`. |

## 6. Package

| # | Review claim | Status | What was done |
|---|---|---|---|
| 6.1 | README still says v2 / no PDF exported. | **A** | README rewritten for v6: both sources, PDFs distributed, packages, commands. |
| 6.2 | `validation.json` / `provenance.json` describe v2 (18 pp., 12 refs, 9 blocks, stale hash). | **A** | Both rewritten: 25/29 pages, 36 references, 10 blocks in both files, SHA-256 of both sources and PDFs, of the v5 archive and of the review inputs; tests 16/16; runtime versions. |
| 6.3 | `SHA256SUMS` missing. | **A** | Added at the package root (34 files; `sha256sum -c` passes). |
| 6.4 | Document `bell_raw.py`, both Bell datasets, the $S=13/14$ dense runs, with commands and environments. | **A** | README table rows; `provenance.json` → `data_origin_notes` (rank list, conventions, environment, dates). Archived data are marked as byte-identical to v5 (verified by `cmp` against the v5 archive). |
| 6.5 | Add regression tests for `bell_raw`. | **A** | `code/tests.py`: `BellRawTests` — rank-four values $1+\sqrt3=2.73205080757$ and $2.14431716999$ against the review's implementation; five flat rows ($S=8$; $16\pm$; $17$; $64-$) against `bell_raw_scan.json` to $10^{-10}$; Tsirelson value $2\sqrt2$ of the corrected protocol at $S=8$, $\kappa=1/2$ with $p=0.012424631790112$. 16 tests pass (`validation/tests.log`). |
| 6.6 | Appendix E's "every number reproduced" needs an identifiable script or a narrower statement. | **A** | Narrowed (both): tabulated values, rank-four and eight-mode quantities, oscillator constants, harmonic-pair defects and Bell values at selected ranks are reproduced by `code/independent/` (four scripts: the three 26–29 October check scripts and the reviewer's `independent_review_v5.py`, paths adapted, rerun on the v6 package with every numerical entry identical to the reviewer's results file); window minima/maxima/medians are read from the archived scans. |
| 6.7 | Author/affiliation placeholders, submission format, deposit, licence. | **O / partly A** | `LICENSE` (MIT, code and data) added as a default **to be confirmed by the authors**; the author line remains "Authors and affiliations to be added" and the deposit/DOI is for the authors. |
| 6.8 | Optional: rank-4 reduction in `bell_raw.py`. | **D** (not needed) | Not implemented: the archived values are already reproduced by two independent dense implementations; the optimisation would change no number. |

## 7. Positioning

| # | Review claim | Status | What was done |
|---|---|---|---|
| 7.1 | Foreground the quantitative dependence on the specified coboson quadratures; keep the Jordan/Halmos reduction, singlet projector, purity identity and CHSH saturation identified as established tools. | **A** (already largely in v5) | Sec. 5.1 already states "We claim no novelty for this algebraic step, which is the standard tool of self-testing"; the introduction's list (i)–(v) names the composite-specific results. Unchanged except for the wording fixes above. |
| 7.2 | The final paragraph must not claim compositeness is a newly established entanglement resource; the protocol uses joint entangling operations and has an oscillator counterpart. | **A** | Closing paragraph (both) rewritten: "A composite boson that performs poorly under the conventional diagnostics … still yields … an exact Pauli algebra and an exact singlet at the percent level, by a construction with an elementary-oscillator counterpart and with every loss computable from the Schmidt spectrum … Seen by the right detector, compositeness is not a defect that must be removed before a composite can serve as a qubit resource; it is a structure whose consequences for that use can be computed, and used." The phrases "fails every conventional test" and "the structure that the resource is made of" are gone. |
| 7.3 | Corrections to other papers should not dominate; acknowledgment correspondence is for the authors to substantiate. | **A / O** | Unchanged (Sec. 8 and the Acknowledgments are already factual and brief); the correspondence is the authors' to confirm. |

---

## Verification summary

- Both sources compile with `latexmk -pdf`: 0 overfull boxes, 0 undefined references, 0 multiply defined labels; bibliographies (36 entries) renumbered by first citation with no missing or uncited keys (the undergraduate order changed because the Bernoulli references now first appear in the new Background paragraph).
- `make_assets.py` reproduces all ten generated blocks of both files unchanged.
- `python -m unittest discover -s code -p tests.py`: 16 passed.
- `code/independent/independent_review_v5.py` rerun on the v6 package: all numerical entries identical to the reviewer's results file (relative tolerance $10^{-9}$).
- Data files byte-identical to v5 (`cmp` against the v5 archive); `SHA256SUMS` verifies.
- New analytical content (Lemma 2, Proposition 2) checked line by line; the conjugation identity $Q_r=(r/b)\,i^{\hat N}Q_w i^{-\hat N}$ checked numerically.
