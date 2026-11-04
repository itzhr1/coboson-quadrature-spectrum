# Independent assessment of coboson paper v5

**Prepared for the authors and Claude — 30 October 2026**

Reviewed: `coboson_paper_v5.tex`, its supplied 23-page PDF, `undergrad_version_v5.tex`, all six calculation scripts, the supplied JSON datasets, and the validation and provenance records. Source locations below refer to the supplied v5 files, before any changes. No manuscript has been edited.

## Overall judgment

**There is a credible, mathematically coherent paper here, but I would make a focused scientific revision before submission.** I found no failure in the central finite-rank recovery construction or in the principal numerical examples I independently checked. The strongest material is the explicit comparison of smooth displacement diagnostics with discontinuous quadrature binning, the treatment of bin-edge atoms, the state-dependent efficiency of the recovered Pauli representation, and the controlled flat-spectrum oscillator limit.

The remaining work is more than copyediting. Some introductory and concluding claims outrun the precise results; the finite-mode numerical evidence is occasionally presented with unjustified precision; and the undergraduate additions introduce several actual errors. The fixed-purity convergence discussion can also be substantially strengthened by an elementary argument, given below.

My recommendation is to preserve the core calculations and proofs, correct the claims, clarify the measurement operations, and refresh the reproducibility package. I do not see a reason to restart the project or replace its central approach. This is a technical assessment, not a guarantee of acceptance or an exhaustive novelty search.

## What I verified

The review distinguishes rerunning the supplied implementation from checking results independently.

| Check | Outcome |
|---|---|
| Bundled regression suite | All 13 tests pass. |
| Generated manuscript assets | All **10** marked blocks reproduce exactly in **both** LaTeX versions. The records saying nine are stale. |
| Independent tensor-product quadrature calculations | All six rows of the dense nonflat table agree at both cutoffs; the largest probability difference from the archive is below `2e-15`. This implementation does not import the manuscript's operator code. |
| Independent flat calculations | Checked ranks 8, 16, 17, 32, 64 and 128, including corrected probabilities, raw probabilities and Bob-optimised CHSH values. |
| Two-party singlet construction | Direct coefficient-matrix norms agree with the one-party probability identity; checked stabilisers and the recovered Pauli relations. |
| Rank-four examples | Reproduced squared defects 1 and 5/2, raw probabilities 3/32 and 23/128, and CHSH values 2.73205080757 and 2.14431716999. |
| Displacement expansion | Symbolically verified the expansion of `log g` through the cubic power of the Schmidt weight, including the stated coefficients. |
| Oscillator overlap | Independent integration over Gaussian bin intervals agrees with the Fourier series: `p∞(1) = 0.0683497058886918`; balanced-scale value `0.0817088735327458`. |
| Anderson-state correction | Exact three-dimensional calculation at S=2, β=1 gives intensity 5/9, fourth-order moment 1/9 and field correlation 9/25. |
| Presentation | Inspected all 23 supplied PDF pages at overview scale and selected figure/equation pages in detail. The supplied main log has no overfull boxes or unresolved references. The undergraduate source compiles to 28 pages; its second-pass log likewise has no overfull boxes or unresolved references. |

The independent runtime was Python 3.12.14, NumPy 2.3.5, SciPy 1.17.1 and SymPy 1.14.0. I did **not** rerun the complete historical rank-8000 scan, the rank-19 nonflat scan, the rank-13/14 dense runs, or the 960-step Lanczos study. Those large-run values were inspected as archived evidence. Passing tests and selected independent calculations do not certify every large-run digit or every theorem.

## 1. Clarify what the preparation actually requires

**Priority: essential.** Main abstract; introduction, lines 41–49; Section 5.2; Appendix A; undergraduate “functions of an operator” box, line 212.

The paper already acknowledges joint entangling preparation, a phase reference where appropriate, and the fact that the polar-corrected observable depends on both quadratures. Those are important and should be retained. Nevertheless, the abstract's description of three “standard measurements,” followed by homodyne detection that “extracts a spin singlet from the vacuum,” can still suggest that ordinary homodyne recording and classical binning implement the preparation.

There are three different operations:

1. Measuring a quadrature and classically binning its outcome reproduces the **outcome probabilities** of the binned observable.
2. A coherent Lüders measurement of a degenerate binned observable preserves coherence within each bin. Resolving the underlying quadrature first generally does not.
3. The raw protocol requires the **joint** projectors `(I − Z⊗Z)/2` and `(I − X⊗X)/2`. Measuring the two local observables separately and retaining opposite outcomes is a different instrument: it loses the coherence between the `+−` and `−+` branches.

For example, if `P±` are local sign projectors, the desired first update is

`(P+⊗P− + P−⊗P+) ρ (P+⊗P− + P−⊗P+)`.

Local measurements with classical outcome selection instead produce the sum of the two separate branch updates, without their cross terms. They cannot generate entanglement from the initial product vacuum.

**Suggested statement:** “Binned quadrature statistics define the local observables. Singlet preparation additionally assumes coherent spectral filtering and heralded joint projective operations; ordinary homodyne detection followed by classical binning does not implement these state updates.”

The Bell discussion should also distinguish certification of the **output state and observables on its support**, up to local isometries, from certification that a device physically executed the particular filter and polar correction. A maximal CHSH score cannot identify that internal implementation. Joint entangling preparation is compatible with a subsequent legitimate Bell test; what is not demonstrated is nonlocality of the initial product vacuum or entanglement generation by local homodyne processing alone.

## 2. Bring the numerical prose into agreement with the data

**Priority: essential.** The numerical tables themselves checked well; several surrounding sentences do not.

### Fixed-purity precision and existence

Section 7, line 544, calls the limits “numerically established to three digits.” Table 3's caption, line 560, says the z≤0.6 rows are stable to the displayed digits. These formulations are stronger than the scan supports.

For S=13 through 19, the archived data give:

| Quantity | Minimum | Maximum | Span |
|---|---:|---:|---:|
| z=0.5, p₀.₆ | 0.0121467552 | 0.0121909292 | 0.0000441740 |
| z=0.6, p₀.₆ | 0.0249588951 | 0.0253506152 | 0.0003917202 |
| z=0.5, t₀.₄ | 0.3015694617 | 0.3043966488 | 0.0028271871 |
| z=0.6, t₀.₄ | 0.5306761594 | 0.5359627288 | 0.0052865695 |

These spans do not establish three significant digits of an infinite-mode limit, particularly for z=0.6. Nor is the last computed value a certified approximation to that limit. Use the actual finite-window variation, separately from the fixed-rank Lanczos sensitivity.

Figure 4's caption, line 482, also says the singlet probability “stays finite” and describes the plotted examples as “infinite-mode composites” with specified probabilities. That conflicts with the explicit conjectural status later in the section. Replace it with a statement about finite truncations and evidence consistent with a nonzero limit. The introductory Schmidt-number-three example should likewise say **approximately three in a finite truncation**, unless an exactly specified finite spectrum or an infinite-limit proof is supplied.

### Bell-fidelity scan and tie convention

Section 6, line 408, states that the fidelity bound is at least 0.64 “for every S≥64.” The scan is not exhaustive above 400 and does not cover all arbitrarily large ranks. For the default positive-edge convention, the smallest archived bound in the sampled range S≥64 is approximately **0.64247853 at S=71**. Thus the supported statement is “at least 0.64 for every sampled rank S≥64 under the positive-edge convention.”

If both conventions are included, the assertion fails even within the supplied table: at **S=64, negative-edge convention**, `B = 2.29560986829`, giving a bound of **0.63132150**.

Define the fidelity as extracted two-qubit singlet fidelity, or singlet extractability, with local channels/isometries and discarded auxiliary systems. It is not necessarily the literal overlap with a preferred singlet vector in the original full Hilbert space. The numerical formula is consistent with [Kaniewski's definition and bound](https://arxiv.org/pdf/1604.08176); the qualification needs to remain visible. At S=17, “nothing is certified” should mean no fidelity improvement over the trivial 1/2 baseline from this particular bound, not absence of entanglement evidence.

### Two simple numerical corrections

- **Table 2 caption, line 510:** “all but” the w=3 example exceed 1% is false. The w=4 example has `p₀.₆ = 0.00598153`, i.e. **0.598%**. At κ=0.6, four of the six examples exceed 1%; both w=3 and w=4 are below it.
- **Raw success range, line 403:** “5–13% throughout” is false. For the positive-edge points plotted in Figure 2(b), the archived extrema are **2.609590% at S=13** and **13.452408% at S=58**. Even the highlighted S=8 and S=17 values are below 5%. Use approximately 2.6–13.5% over the plotted scan, or describe a clearly specified subrange.
- **CHSH saturation in captions, lines 381 and 426:** add “whenever the preparation probability is nonzero.” At ranks/cutoffs with p=0 there is no normalized corrected output state on which to report a CHSH value.

These are easy fixes, but referees will notice contradictions between prose and tables.

## 3. Tighten the main physical and mathematical claims

**Priority: essential claim corrections; no need to change the central results.**

- **“Commutator a third away from unity” — introduction line 45 and conclusion line 658.** The commutator is an operator and needs a state or norm. On the vacuum, its deviation is exactly zero. On the normalized one-pair state `B†|0⟩`, `⟨Δ⟩ = 2P`, so at P=1/3 the expectation of the commutator is 1/3 and its deviation from unity is **2/3**, not 1/3. The normalization ratio `F₂/F₁ = 1−P` has a deviation of 1/3; do not conflate these diagnostics. “Fails every conventional test of bosonic behaviour” is also unsupported: the paper shows failure of particular tests, and g² is undefined on the vacuum.
- **“No finite set of moments determines them” — introduction line 43.** This conflicts with the correct Newton-identity qualification in Section 4, line 201. The examples establish nondetermination by **purity and the third moment**. They do not establish the universal statement. Replace it with the result actually proved.
- **“A drive is a low-order function” / “sees only its first few moments.”** The displacement is an exponential, not a low-degree polynomial. The exact product formula depends on the full spectrum; its leading dilute expansion is controlled by the moments displayed in Section 3. Say “a smooth fundamental-harmonic probe, with a controlled dilute moment expansion.” The contrast with a discontinuous square wave then remains precise.
- **“A lattice with 2^S points,” and localized spectra as a “Cantor-like set” — introduction line 43.** There are 2^S signed sums **counted with multiplicity**; a flat spectrum has only S+1 distinct eigenvalues. General nonflat signed sums are not a uniformly spaced lattice. In the geometric infinite limit the support is an interval when √z≥1/2, including all z=0.5–0.9 examples. A singular measure can also have interval support. Distinguish finite signed-sum spectra, equally spaced flat spectra, support, and spectral measure.
- **The no-qubit statement needs its actual hypothesis.** At r=1, `Σ√λk < π/2` is a valid sufficient criterion for `X=I`, hence p=0. Near-unit purity alone does not imply this ℓ¹ condition uniformly over unbounded ranks: a small total tail can contain many modes with a large sum of square roots. Retain the explicit criterion instead of suggesting a general purity-only threshold.
- **“The commutator ... vanishes” — Figure 2 caption, line 344.** It is the commutator **deviation** that vanishes on the appropriate fixed vectors; the bosonic commutator approaches the identity.

The multiplicity factor should be described as an **observable-defined logical subsystem**, not automatically a spatial or microscopic constituent subsystem. Its entanglement with the recovered qubit is a valid statement in that factorization. It does not mean that the original site-product vacuum contains pre-existing Alice–Bob entanglement, nor that the mechanism is unique to composites: the oscillator also has multiplicity. The paper's useful contribution is calculating how this representation and its efficiency depend on the composite spectrum.

The “Physical scales” paragraph should either cite quantitative, system-specific sources or present its estimates as heuristics. Finite Schmidt rank, inverse purity, coherence length, and sample size are not interchangeable. In particular, mapping S≤20 directly to dots/aggregates, or asserting that emitted polariton light directly measures the model's composite quadrature lattice, needs a measurement/coupling model beyond what is supplied. The later statement that this is not an experimental proposal is appropriate but does not substantiate these earlier mappings.

## 4. Strengthen Section 7: atomlessness is enough

**Priority: substantive mathematical improvement.** Main Section 7, line 568, and the corresponding conclusion. This is an opportunity to improve the theorem, rather than a reason to reject the finite-rank results.

The current argument invokes difficult absolute-continuity results for Bernoulli convolutions to exclude mass at bin edges for selected parameters. **Absolute continuity is unnecessary: atomlessness suffices.** In this model there is also a direct route from the vacuum representation to all vectors, so the “other spectral measures” obstacle can be removed.

Here is a self-contained argument for the authors to check and incorporate if desired. It applies to both supplied infinite families, not just almost every geometric parameter.

### Proposed lemma and proof

Let `ak = √λk > 0`, with infinitely many nonzero terms and `Σ ak < ∞`. Let `εk` be independent fair signs. The distribution of `q = Σ ak εk` is nonatomic.

Choose an infinite subsequence `bk` with `b(k+1) < bk/4`. Then `Σj>k bj < bk/3`. Two different sign sequences on this subsequence cannot give the same sum: at the first differing term, its contribution dominates the remaining tail. A specified sum therefore corresponds to at most one infinite fair-sign sequence and has probability zero. This subsequence sum is independent of the complementary sum. Convolving a nonatomic distribution with any probability distribution remains nonatomic, proving the assertion.

Now identify the vacuum incomplete tensor product with `L²({−1,+1}^N, μ)`, where μ is fair product measure: finite occupied-mode basis vectors become Walsh characters and the vacuum becomes the constant function 1. In the σx basis, the limiting quadrature is multiplication by `−b Σ ak εk`. Every vector's quadrature spectral measure therefore has the form

`νψ(A) = ∫ 1{−b q(ε) ∈ A} |ψ(ε)|² dμ(ε)`.

A zero-mass spectral set for the vacuum has zero mass for **every** vector. The other quadrature is obtained by a fixed diagonal phase unitary on the finite-occupation basis, so the same conclusion holds there.

The normalized finite truncations converge uniformly as multiplication functions because the coefficients are summable and the normalization tends to one. Away from the countable bin-edge set, their bin signs eventually agree with the limit. Dominated convergence then gives strong convergence of **both** binned operators on the full Hilbert space. Consequently their products and `K_S = {X_S,Z_S}/2` converge strongly too.

For any fixed `0<κ<1` satisfying

`1{−κ,+κ}(K∞) = 0`,

bounded functional calculus gives convergence of the filter, the cut-off polar factor and the two-party singlet projector. Thus the preparation probability converges at that cutoff.

Because the Hilbert space is separable, the limiting K has at most countably many eigenvalues. For a fixed spectrum and scale, this yields convergence for **all but at most countably many cutoffs**.

### What this still does not prove

It does not establish that the particular κ=0.4 and 0.6 avoid limiting atoms, nor that their limiting probabilities are strictly positive, nor any convergence rate or certified error bar. Those remain distinct questions. An authors' revision could retain those open problems while replacing the unnecessarily restricted bin-edge discussion with this stronger result. No claim of novelty for the underlying nonatomicity argument is intended here.

## 5. Correct the undergraduate additions before distribution

**Priority: essential for the pedagogical version.** The inserted explanations are useful, but they need their own accuracy pass; inheriting correct research equations has not prevented errors in the connecting text.

| Location in `undergrad_version_v5.tex` | Problem and correction |
|---|---|
| Line 153, Weyl-relation background | The formula has the BCH half-phase but multiplies the reversed product. Correct forms are `D(z)D(w)=exp[(zw*−z*w)/2]D(z+w)` and `D(z)D(w)=exp[zw*−z*w]D(w)D(z)`. With the manuscript's z=r, w=−ib convention, the latter phase is `exp(+2irb)`. It still equals −1 at 2rb=π. |
| Line 112, displacement/quadrature background | With `[x,p]=i` and `x=(a+a†)/√2`, the defined `Qr=−ir(a†−a)` equals **−r√2 p**, not +r√2 p. The sign is irrelevant to the even binning function, but the teaching equation must be consistent. |
| Same line | The oscillator vacuum has `Var(x)=Var(p)=1/2` in this normalization, not 1. The rescaled quadratures have variances r² and b², as used correctly in the main calculation. |
| Line 109, nested commutators | “None ... vanish on the vacuum” is false for the displayed examples. In fact `[B,[B,B†]]=−2Σ λk^(3/2) dk` annihilates the vacuum, and the next nested commutator with B is zero. Use a creation-containing example such as `[Δ,B†]|0⟩≠0` to explain why the vacuum commutator alone does not fix finite displacements. |
| Line 212, functions of an operator | Measuring Q and applying F gives the same **outcome statistics** as F(Q); generally not the same postmeasurement state. Add this distinction explicitly because the paper studies sequential preparation. |
| Line 301, Jordan-lemma background | The intermediate multiplication for XK is incorrect. Write `XK=(Z+XZX)/2=KX`. Explain that a degenerate K eigenspace may contain many two-dimensional blocks; it is not necessarily itself two dimensional. |

Also temper “g²=1 is the standard test of a coherent field”: it is a second-order consistency test, not a characterization of a coherent state. For example, phase averaging a coherent state preserves its number statistics and g² while removing a definite coherent amplitude.

For its intended audience, I would label this an **annotated advanced-undergraduate version**. A short reading route would help: finite paired model → eight-mode example → recovery identity → numerical figures, with the functional-analysis limit and Bernoulli discussion optional on first reading. It currently preserves the full research argument with background boxes; that is valuable, but not the same as a substantially simpler pedagogical derivation.

## 6. Refresh the reproducibility and submission package

**Priority: essential packaging correction; modest work.**

The supplied code is readable and the separation between fresh dense data and historical scans is helpful. The documentation needs to describe the delivered revision:

- `README.md` still calls the package revision v2 and says no PDF was exported, although v5 includes one.
- `validation/validation.json` and `provenance.json` describe v2: 18 pages, 12 bibliography entries and nine generated blocks, versus the supplied v5's **23 pages, 36 bibliography entries and ten blocks**. The recorded current-manuscript hash is not the v5 hash.
- The README mentions `SHA256SUMS`, which is absent from the supplied folder. Add a manifest covering the actual release.
- Document `bell_raw.py`, both Bell datasets, and the rank-13/14 dense checks, with the exact commands and environments that produced them. Preserve the distinction between archived data and freshly rerun data.
- Add regression coverage for the Bell addition. The existing 13-test suite does not test `bell_raw.py`. The two exact rank-four CHSH values and selected flat cases offer meaningful benchmarks.
- Appendix E's statement that “every number quoted in the text was reproduced by an independent implementation” needs an identifiable script/log or a narrower statement. The package currently demonstrates representative independent cross-checks, not an auditable reproduction of every prose statistic.
- Replace author/affiliation placeholders, choose the submission format, and prepare a durable code/data deposit with a citation and an explicit license as appropriate.

An optional efficiency improvement: the raw coefficient matrix is a sum of four outer products and has rank at most four. Bob's trace-norm optimization can therefore be reduced to that small support after an orthonormal basis is formed. This would avoid much of `bell_raw.py`'s dense high-rank matrix work. It is an optimization opportunity, not evidence that the current values are wrong.

## 7. Position the contribution without overselling it

The paper is strongest as a theoretical study of **observable-dependent bosonic behaviour and recovery efficiency in a specified paired-mode model**. The generic Jordan/Halmos reduction, the singlet projector, the two-copy purity identity and maximal CHSH saturation should remain clearly identified as established tools. The novel content to foreground is their quantitative dependence on the specified coboson quadratures, the discontinuity/edge mechanism, explicit counterexamples to low-moment determination, and the convergence analysis.

The oscillator and Anderson-state corrections are worth retaining in a careful factual tone. I independently reproduced the corrected oscillator values; the quoted inconsistent numbers are present in [Sorella v1, Section 5.1](https://arxiv.org/html/2610.23264v1). I also verified the S=2 field-correlation counterexample algebraically and checked that [the accessible Shiau–Combescot preprint, equations (50)–(53)](https://arxiv.org/pdf/1609.08119) contains the state and amplitude-independent expression being discussed. Publisher metadata confirms the [2017 PRA article](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.95.013838); I did not retrieve the full publisher PDF. The private correspondence in the acknowledgment is for the authors to substantiate.

Do not let the corrections to other papers dominate the contribution. Nor should the final paragraph claim that compositeness itself is a newly established entanglement resource: the protocol uses joint entangling operations and has an elementary-oscillator counterpart. A more defensible conclusion is that **poor performance under conventional bosonic diagnostics does not preclude a useful recovered logical qubit, at a calculable preparation cost**.

## Suggested revision request to Claude

Please revise v5 using this assessment as a list of claims to check, not as an instruction to accept every criticism automatically. Preserve the verified core equations and datasets. First correct the numerical prose and undergraduate equations, clarify the distinction between binned measurement statistics and coherent joint preparation, and qualify the commutator, moment and physical-realization claims. Then independently check the proposed nonatomicity/strong-convergence argument and incorporate it if valid, while retaining the unresolved specific-cutoff and positivity questions. Update both versions together and regenerate the v5 validation/provenance records. Return a point-by-point response that distinguishes accepted corrections, justified disagreements and open questions, with source locations and verification evidence.

**Assessment:** suitable to continue toward publication after a focused revision; not ready to submit unchanged. The checked core survives this review. The main need is to make the claims as precise as the calculations.
