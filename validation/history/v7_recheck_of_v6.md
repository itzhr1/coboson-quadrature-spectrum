# Recheck of v6 and changes made in v7

30 October 2026. Prepared for the authors and for handoff to Claude.

## Assessment

V6 substantially resolves the scientific and interpretive concerns in the earlier assessment. In particular, it separates binned measurement statistics from the coherent operations needed for heralded preparation, defines the self-testing fidelity as extractability, qualifies the finite-rank evidence, and supplies a useful new infinite-mode convergence argument. I found no new failure of the central finite-mode construction or of that convergence argument in this recheck. This is a focused analytical and numerical review, not a guarantee of publication acceptance or an exhaustive new literature review.

A v7 is warranted for a small set of precision corrections, clearer presentation of the new result, and Figure 5. Both the research and annotated undergraduate versions have been revised together. The research PDF remains 25 pages; the undergraduate PDF remains 29 pages. All archived data files are unchanged byte for byte. Of the ten generated tables/figures, only the Figure 5 block changes.

## Scientific and numerical corrections

1. **The new infinite-mode result is sound under its stated condition on the amplitudes.** The rapidly decreasing subsequence argument establishes nonatomicity. The product-space representation then transfers the absence of bin-edge atoms to every vector, and uniform convergence of the truncated quadratures gives strong convergence of their binnings. The final step requires that the filter boundaries are not eigenvalues of the limiting anticommutator. V7 makes the infinite normalised spectrum, positive amplitudes, and fixed scales explicit, and writes the bounded cutoff function used in the polar correction. This clarifies the proof without claiming a stronger theorem.

2. **The introduction still contradicted the new proposition.** V6 said that the infinite-mode limit at fixed purity was unproved, without distinguishing generic cutoffs from the particular cutoffs in the tables. V7 consistently states convergence at all but countably many cutoffs. Convergence at the specific cutoffs 0.4 and 0.6, positive limiting probabilities there, and a rate remain open. The conclusion now says “summable Schmidt amplitudes”; summability of the normalised weights alone is automatic and is not the theorem's hypothesis.

3. **Certified lower bounds must not be rounded upward.** V6's “at least 0.68” at S=8 exceeded the calculated analytic guarantee 0.67608985. Similar rounding affected several other examples. V7 rounds the displayed guarantees down to three decimals: 0.676, 0.625, 0.748, 0.830, 0.822, 0.874, and 0.896 at ranks 8, 32, 128, 512, 1024, 3956, and 8000. The last two deliberately read 0.874 and 0.896, since the underlying values are 0.87499685 and 0.89698693. The formula now explicitly includes the trivial 1/2 baseline. The Figure 3 caption refers to the exact formula rather than repeating rounded coefficients as a certified inequality. These are floating-point evaluations of the analytical guarantee, not interval-arithmetic certificates.

4. **A few residual claims were broader than the evidence.** V7 qualifies finite-spectrum discreteness and the fixed-pair-number limit of the commutator deviation; identifies the oscillator Bloch length 0.85 with r=1; marks scan-range claims as applying to sampled ranks; replaces “fail every bosonicity criterion” with the actual two order-one defects; and states that near-unit intensity correlation is consistent with, but does not establish, a coherent state. The Table 3 caption now identifies preparation probabilities rather than all table entries as varying by approximately 0.4–3.5%.

5. **Physical interpretation and abstract.** The physical-scales paragraph no longer assigns a numerical truncation rank directly to a real quantum dot or aggregate without a microscopic Schmidt decomposition. The abstract now includes the generic-cutoff convergence result, distinguishes finite examples from limiting claims, and keeps the coherent preparation requirement explicit. The original scientific scope and conclusions are retained.

## Figure 5

The concern about Figure 5 was justified. The v6 dual-axis arrangement mixed probabilities with a universal operator bound, while its 0–10% probability scale left approximately half the plotting area unused. It made the cutoff trade-off unnecessarily difficult to read.

V7 uses two vertically aligned panels with the same cutoff axis:

- Panel (a) shows the five unchanged probability step functions on a 0–5% scale. Colour and line pattern both distinguish the curves.
- Panel (b) shows the universal correction bound. Guides at 0.4 and 0.6 connect the plot to the nonflat tables and label the corresponding bounds, approximately 0.409 and 0.632.
- The caption distinguishes a bound from a model's actual correction, explains the jump locations through the spectrum of the anticommutator, and identifies the open endpoint as the limiting bound sqrt(2). The filter remains restricted to cutoff below 1.

No smoothing, interpolation of the probability jumps, or change of data was used. The stored jump locations retain the original tiny numerical displacement above each threshold. The change is implemented in `code/make_assets.py`, so regeneration preserves the new design in both manuscripts. A standalone vector PDF and its LaTeX source are supplied in `figures/`.

## Verification performed

- All 16 bundled assertion-based regression tests pass.
- A new independent direct-quadrature script checks all 50 stored Figure 5 points, including accepted weights, direct two-party singlet probabilities, correction bounds, and monotonicity. The largest probability discrepancy is 2.3e-15.
- The earlier independent review calculation was rerun: all six dense nonflat table rows agree to within 1.9e-15 in the probabilities; the symbolic displacement expansion passes; the rank-four and selected flat-rank calculations, eight-mode identity, Anderson field correlation, and oscillator constants were rechecked. The largest selected flat-rank Pauli and involution residuals are below 4e-13.
- Both manuscripts reproduce all ten generated blocks, and the blocks agree between versions. The other nine blocks are unchanged from v6.
- All 14 JSON files under `data/` match the supplied v6 files byte for byte. The asset generator now computes the harmonic table in memory without overwriting archived data as a side effect.
- Both PDFs compile with no unresolved references, missing citations, duplicate labels, or overfull boxes. Rendered pages were inspected, including the new figure and its placement. Routine LaTeX float-placement notices remain.

The complete historical scans and the expensive 960-step Lanczos calculation were not rerun. Their provenance and the v6 validation records are retained. Numerical agreement does not replace the analytical proofs or establish the conjectured infinite-mode positivity.

## Remaining author decisions before submission

Insert the authors and affiliations, which are still placeholders. Confirm the existing code/data licence and the intended journal's formatting and data-deposit requirements. V7 preserves the supplied licence and acknowledgments; no statement about correspondence or permissions was independently verified. The mathematical open questions above are now explicit limits of the paper, not hidden claims that the edits purport to settle.

## Handoff to Claude

Please use the v7 sources as the new base. Preserve the distinction between measurement statistics and coherent heralded preparation; the summability condition is on the Schmidt amplitudes, not merely the weights. Keep the lower-bound rounding conservative, and preserve the two-panel Figure 5 through the generator. Any later scientific edit should be made in both versions, followed by regeneration and recompilation. `validation/validation.json`, the independent check outputs, and `SHA256SUMS` record the verification accompanying this revision.
