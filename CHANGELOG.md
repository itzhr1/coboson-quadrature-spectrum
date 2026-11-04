# v10.12 (4 November 2026): review of v10.11, published reference for Sorella (batch 11)

Added `.zenodo.json` (Zenodo metadata for GitHub releases) and a README note on archiving.

Base: the Codex revision v10.11 (its four manuscript corrections from the v10.10 review were
re-derived and kept: narrowed continuous-variable-qubit claim, heralded-state reading of the Bell
values, finite-block versus direct-integral wording, collective-spin bin widths r*sqrt(S) and
pi*sqrt(S)/(2r); its reproduce.sh/tests.py fixes and author details are kept). Changes on top, both
versions: (1) Introduction, "Detector (B)" paragraph: the narrowed claim is kept, but the composite-field
motivation removed in v10.11 (polaritons, molecular condensates, spin ensembles; the 1e-3 vs 0.37 and
g2 = 0.99999 vs order-one contrasts) is restored, and the duplicated citations are dropped. (2) Sec. 5.1:
the retained-sector representation is written explicitly, ran E = C^2 (x) M with X = sx (x) I,
Zt = sz (x) I, K = I (x) C, Z = sx (x) C + sz (x) sqrt(I - C^2) (checked numerically at S = 8), and M is
identified with the complementary logical factor of the Introduction. (3) Conclusions: the closing
paragraph removed in v10.11 is restored; the third open problem names the confinement-model spectrum.
(4) Ref. Sorella2026 is now the published article, Phys. Lett. A 599, 132284 (2026), with the arXiv
number kept; Sec. 9 cites "arXiv version 1" for the values it corrects; acknowledgments reworded
(correction in preparation; LLM assistants named as Claude Fable 5.1 and OpenAI Codex). No equation,
number, table, figure block or data file changed. Validation history renamed to the v<tag>_<file>
convention and completed with the v10.10 test/figure/review records.

# v10.11 (4 November 2026): Minor corrections, shortening and author details

Both manuscript versions: add I. Roditi's author details and the LLM-assistance and
CNPq grant acknowledgment; retain the acknowledgment to S. P. Sorella. Narrow the
claim about continuous-variable qubit encodings, clarify the Bell-test preparation
sequence, distinguish finite Jordan blocks from infinite-dimensional direct
integrals, correct the two collective-spin bin widths, and state the leading
normalisation asymptotics as a logarithmic estimate. Shorten the introduction's
motivation and roadmap and remove repetition in the outlook and conclusion.
All numbered equations, numerical data, tables and figure blocks are unchanged.

Reproduction: use Bash with pipefail so a failing test cannot be hidden by tee;
move unittest.main after all test classes so direct execution includes Bell tests.
Update active filenames, citation metadata and package hashes for this revision.
Validation details are recorded in validation/revision_v10_11.json.

# v10.10 (3 November 2026): Conclusions, finite-mode evidence for Wannier-like spectra (batch 10)

Prose only, both versions. "dense finite-mode calculations give singlet probabilities up to 4% for
Schmidt numbers 2-9" mixed two sources: the dense examples (Table 2, S <= 12) reach Schmidt number
about 5 and 3.8%; the Schmidt number 9 (z = 0.8, 1/P_19 = 8.7) and the 4% come from the Lanczos rows
of Table 3. Now "finite-mode calculations (dense to Schmidt number about 5, Lanczos beyond) give
singlet probabilities up to 4% for Schmidt numbers between 2 and 9". Closes the section-by-section
re-verification (Secs. 3-10, Appendices A-E): every quoted value of Appendices A, B, D and E
reproduces exactly; four statements changed over the pass (v10.7 x2, v10.9, v10.10), no result.

# v10.9 (3 November 2026): Appendix C crossing density (batch 9)

One number, both versions. Appendix C: the density at which the Anderson state's field correlation
crosses 1 at S = 32 is q* = 0.524 (root of g2_A = 1), printed as 0.52 instead of 0.53; S = 8 (0.608 ->
0.61) was correct. Large-S check: g2_A = 1 - 2(1-2q)/(S(1-q)) + O(1/S^2), so q* -> 1/2 (0.508 at S = 100,
0.5008 at S = 1000). No other change.

# v10.8 (3 November 2026): remaining non-physics vocabulary removed (batch 8)

Prose only. "trade-off" -> "sets ... against" (Sec. 7); "performs poorly under the conventional
diagnostics" -> "that the conventional diagnostics ... place far from bosonic" (Conclusions);
"readout" -> "measurement" (three places, Secs. 1-2); "at a computable loss of accepted weight" ->
"with the rejected weight computable from the spectrum" (Sec. 1); annotated version additionally
"costing" -> "requiring" (Background paragraph on numerical methods). Title unchanged. No number,
reference or generated block changed.

# v10.7 (3 November 2026): Sec. 6 scatter statement corrected (batch 7)

Prose only, both versions, from a re-verification of the archived flat scan. (1) "the scatter
between neighbouring ranks is about +-15% and does not diminish with S" was not supported by the data:
measured about the fitted power law (slope -0.146, S >= 64, + convention), the 5th-95th percentile
envelope of log eps_vac is [-0.14, +0.10] for 64 <= S <= 400 (neighbouring ranks differ by up to 43% near
S = 100), [-0.06, +0.06] for the sampled ranks 400-2000 and [-0.05, +0.01] for the log-spaced ranks to
8000; the text now states these three figures and that the envelope narrows slowly while the trend
stays shallow. (2) Fig. 2 caption: "scatters about its trend by up to +-15%". (3) "by two decades at
S = 1000" -> "a factor of about fifty" (0.0093 against 0.52). No number in tables or figures changed.

# v10.6 (3 November 2026): the moth-eaten effect named where it enters (batch 6)

Prose only, both versions. Sec. 2, after Eq. (ladder): F_N = prod_{k<N}(1 - k/S) decreases as
exp(-N(N-1)/2S) for N << S, reaches F_S = S!/S^S, and the ladder terminates at N = S (B^dagger|S> = 0):
the moth-eaten effect of Pogosov and Shiau-Combescot, contained in every flat-spectrum calculation
through the ladder coefficients. The later intensity sentence now reads "the saturation side of the
moth-eaten effect" (the references having moved to the first mention). No number, reference count or
generated block changed.

# v10.5 (3 November 2026): motivation -- why binned quadratures, and where they exist (batch 5)

Prose and three references, both versions. Introduction, two new paragraphs after the three
detectors: (i) sign-binned quadratures at Weyl area pi as the mechanism of every CV-to-qubit mapping
(modular variables, dichotomised-homodyne Bell tests, the GKP encoding), formulated for elementary
bosons; the relevant question for composite fields is whether their binned quadratures anticommute,
which the conventional criteria do not answer (Weyl defect 1e-3 with binned defect 0.37; g2 = 0.99999
with binned defect of order one), with the positive side (exact logical qubit at a computable loss of
accepted weight); (ii) where such measurements exist: spin ensembles (flat spectrum = collective
spin, Holstein-Primakoff setting, collective-spin measurements routine), exciton-polaritons (homodyne
on emission, coupling model needed), trapped dimers (no established implementation); the measurement
changes the pair number and presupposes a phase reference. Sec. 2: the flat case named as the
Holstein-Primakoff setting; the binned quadratures are sign functions of J_x, J_y with bins of width
sqrt(S) in m, twice the projection noise sqrt(S)/2 of |J,-J>. References added: Gottesman, Kitaev,
Preskill, PRA 64, 012310 (2001); Holstein and Primakoff, Phys. Rev. 58, 1098 (1940); Ma, Wang, Sun,
Nori, Phys. Rep. 509, 89 (2011). Bibliography 43 entries, renumbered. No number or generated block
changed.

# v10.4 (3 November 2026): s-lim defined; lambda^(a) as an instance of the mixedness criterion (batch 4)

Prose only, both versions. Sec. 4, Eq. (17): "with s-lim denoting the strong operator limit
(convergence on every vector)" at the notation's first use. Sec. 5.2, after "merely occupying
several blocks is insufficient": the rank-four spectrum lambda^(a) as a concrete instance -- K = -1/2
on the whole vacuum, t = 1 at kappa = 1/2, yet p = 0 (vacuum a product of qubit and multiplicity
states across four blocks of equal angle); values from the 16-dimensional construction. No number,
reference or generated block changed.

# v10.3 (3 November 2026): the rank-four counterexample made concrete (batch 3)

Prose only, both versions. Sec. 4, after the squared vacuum defects 1 and 5/2 of the two
rank-four spectra: one sentence saying where the difference comes from -- for lambda^(a) the two
drives cut the set of signed sums at the same places (F(r q_t) = F(b q_t) for every t, both -1
exactly at |q_t| = 1.6, 1.8), for lambda^(b) at different ones (F(r q_t) = -1 only at |q_t| = 1.86;
F(b q_t) = -1 at 1.21, 1.38, 1.86). Values recomputed from the 16-dimensional construction. No
number, reference or generated block changed.

# v10.2 (2 November 2026): two sentences in Sec. 3 (author's reading, batch 2)

Prose only, both versions. (1) After the characteristic function: the vacuum outcomes of Q_z are
the signed sums |z| sum_k eps_k sqrt(lambda_k) with fair signs, and a drive is the value of the
characteristic function at t = 1 -- the precise sense of "fundamental harmonic". (2) In the dilute
expansion: the first-order term summed over modes gives e^{-2irb} = -1, the elementary-boson value
of the group commutator, so the defect is built from the remaining orders and starts at P^2 and
M_3; the expansion of 2 - 2 Re e^X with X = iAP - (D + iE_3)M_3 + O(M_4) is named explicitly. No
number, reference or generated block changed.

# v10.1 (2 November 2026): "two vacua" defined at first use

Prose only (author's reading, batch 1). Introduction, detector (B): the bipartite setting is now
stated where the phrase first occurs -- two independent oscillators, one held by each of two
parties, Alice and Bob, with joint vacuum |0>_A|0>_B, "the two vacua referred to throughout", and
the singlet of the two Pauli pairs. Abstract: "from two vacua" -> "from the vacua of two independent
copies of the composite". Both versions. No number, reference or generated block changed.

# v10 (2 November 2026): footnotes for undefined terms

Prose only; no number, data file, reference or generated block changed (all ten blocks of both
manuscripts regenerate unchanged; 16/16 tests).

- Research version: six footnotes at the first use of terms that were not defined where they
  appeared -- the incomplete tensor product built on the vacuum (Proposition 2), coherent (Lueders)
  projections (Sec. 4), core and strong resolvent convergence (Sec. 9), the Fejer approximation
  (Sec. 4), "up to local isometries" (Sec. 5.2, pointing forward to extractability in Sec. 6), and
  Bernoulli convolutions with Pisot and Garsia numbers (Sec. 7) -- in addition to the v9 footnote on
  atoms. Three inline parentheticals: involutions (Sec. 1), Dicke states (Sec. 2), Ritz values
  (Sec. 7).
- Annotated version: the same footnotes where no Background paragraph covers the term (incomplete
  tensor product, Lueders projections, local isometries, Bernoulli/Pisot/Garsia; a one-line
  footnote on "core" pointing to the convergence paragraph); Fejer sums, Dicke states, involutions
  and Ritz values were already explained there.
- Pages: 26 (research), 31 (annotated). Repository references, CITATION.cff (10.0), validation
  records and SHA256SUMS updated; v9 records moved to validation/history/.
- Distributed PDFs (v10, later the same day): rebuilt with XeLaTeX and the Latin Modern OpenType
  fonts. The PDFs of v6-v10 as first delivered had been compiled on a TeX installation without
  the Latin Modern Type 1 fonts, so pdfTeX embedded bitmap Type 3 fonts without Unicode maps for
  the text face; text search and copy in viewers (e.g. Preview) were unreliable. Layout and page
  counts are unchanged; the sources are unchanged.

# v9 (2 November 2026): definition of "atom", SciPost-related references

Prose and bibliography only; no number, data file or generated block changed (all ten blocks of
both manuscripts regenerate unchanged; 16/16 tests).

- Introduction: footnote defining an atom of a measure and the spectral measure of a quadrature
  at the first use of "no atoms" (the annotated version's footnote also points to the Background
  paragraph of Sec. 7).
- Four references added, from a survey of SciPost Physics/Core papers adjacent to the three
  threads of the paper (the journal under consideration): Jimenez, Cuestas, Majtey, Cormick,
  SciPost Phys. Core 6, 012 (2023) [coboson formalism for strongly bound fermion pairs; cited for
  trapped dimers in Sec. 2]; Goodman, Mulkerin, Levinsen, Parish, SciPost Phys. 15, 116 (2023)
  [BCS-like description of polariton condensates at high density; Sec. 2]; Van Regemortel,
  Ravets, Imamoglu, Carusotto, Wouters, SciPost Phys. 5, 013 (2018) [correlations of microcavity
  emission shaped by detection optics; Sec. 2]; Dudal, De Fabritiis, Guimaraes, Peruzzo, Sorella,
  SciPost Phys. 15, 201 (2023) [Bell-CHSH with Weyl operators and squeezed states for bosonic
  fields; Sec. 1]. Bibliography now 40 entries, renumbered by first citation.
- Fig. 1(a): detector (A) label "sees the low harmonics of Q" -> "the fundamental harmonic of Q",
  consistent with the text since v6.
- Date lines v9. Pages: 26 (research; two references spill to the last page), 30 (annotated).
- Repository: file names, README, CI workflow, reproduce.sh, CITATION.cff (version 9.0) updated;
  validation records and SHA256SUMS regenerated; v8 records moved to validation/history/.

# v8 (30 October 2026): reassessment of v7 and repository layout

Base: the v7 sources. The v7 changes were re-verified before being kept: the rounded-down
fidelity bounds (0.67608985 -> 0.676, ..., 0.89698693 -> 0.896) against data/bell_raw_scan.json
and bell_raw_8000.json; the S = 13-19 spans (p_0.6: 0.36% and 1.56%; p_0.4: 2.7% and 3.5%;
t_0.4: 0.9% and 1.0% at z = 0.5 and 0.6) against data/legacy_nonflat_scan.json; the bounded
cutoff function g_kappa in Proposition 2 (continuous off +-kappa, hence strongly convergent under
the same hypothesis as the projector); C(0.4) = 0.4086, C(0.6) = 0.6325; the parameterisation
(sin t, 2 sin(t/2)) of the bound in Fig. 5(b). All 16 tests pass and all ten generated blocks of
both manuscripts reproduce. Data files are byte-identical to v5-v7.

## Manuscripts (both versions)
- Abstract shortened from 210 to 192 words with the v7 content kept (three probes, the Weyl
  expansion versus bin-edge sensitivity, filter and heralded projection, percent-level examples,
  g^(2) not controlling the binned algebra, strong convergence for flat spectra, generic-cutoff
  convergence for infinite spectra with positivity at the specific cutoffs open).
- Sec. 2, physical scales: v7's caution is kept (a numerical cutoff is not a coherence length or an
  inverse purity; assignment to a specific system needs a Schmidt decomposition) and one sentence
  of qualified orientation is restored (aggregate coherence lengths of a few to 10^2 sites; Schmidt
  number of a Wannier exciton from near 1 under strong confinement to of order 10 in a small dot
  and large in bulk, cf. the trapped-pair estimates of Ref. [Law 2005]).
- Conclusions: "lattice of signed sums ... which an elementary boson does not have" qualified to
  finite Schmidt rank; the drive described as the fundamental harmonic (not "low harmonics"), as
  elsewhere since v6; "entanglement between the resolved qubit and the unresolved pair structure"
  -> "and its complementary logical factor" (the v6 wording of Sec. 1 and 5.2, which this sentence
  had missed); "succeeds for all sufficiently large aggregates" -> "flat-spectrum ranks", consistent
  with the v7 physical-scales paragraph.
- Fig. 5: legend in one row (generator and standalone source); otherwise the v7 design.
- Date lines v8. Pages: 25 (research), 30 (annotated; the bibliography now spills to a last page).

## Repository layout (prepared for a public deposit; hosting to be decided)
- manuscript/ (sources, compiled PDFs, standalone Fig. 5), code/ (unchanged scripts, tests,
  independent/), data/ with data/README.md documenting every file and field, validation/ with
  the v8 records and history/ (v6 and v7 records, the two independent reviews and the responses).
- README.md rewritten as a repository front page (layout, reproduction commands, status of the
  results, decisions before release); CITATION.cff (author list to be completed); .gitignore;
  reproduce.sh (tests, regeneration, independent checks); GitHub Actions workflow running the
  tests, the generator check and the Fig. 5 verification on Python 3.11-3.13; requirements.txt
  with lower bounds. The independent review script's paths point at the new layout.
- LICENSE (MIT, code and data) retained as the default to be confirmed.

# v7 (30 October 2026): recheck and Figure 5 redesign

- Rechecked the v6 response and the new nonatomicity/strong-convergence proof.
- Clarified the theorem hypotheses, bounded cutoff function, and generic-cutoff scope throughout.
- Rounded certified fidelity lower bounds down and included the trivial 1/2 baseline.
- Updated the abstract and physical-scales discussion; narrowed residual overclaims and scan wording.
- Replaced Figure 5's dual axes with aligned probability/bound panels, a 0–5% probability scale, distinct line patterns, and guides at cutoffs 0.4 and 0.6.
- Updated both manuscripts together; only one of the ten generated blocks changes. All data files are byte-identical to v6. The generator no longer overwrites harmonic_checks.json.
- Added an independent direct-matrix check of all 50 Figure 5 points. All 16 regression tests and the independent numerical review pass.
- Compiled and visually inspected the research (25 pages) and undergraduate (29 pages) PDFs; supplied a standalone vector Figure 5 PDF/source.
- Refreshed validation and checksums; retained v6 records under validation/history/.
- Full rationale: validation/history/v7_recheck_of_v6.md. Historical entries below describe their original versions and may contain claims superseded in later revisions.

# v3 (26 October 2026, evening): editing pass on v2

Scope: prose only, plus one generator fix and two new dense data files. No figure block or
table value changed, except the formatting of Table 4 (fixed decimals instead of 2 significant
figures) and its regenerated form. `make_assets.py` was patched accordingly and rerun; it
reproduces every block of the edited manuscript unchanged.

## Content changes
- Abstract shortened to 172 words.
- Introduction: explicit list of the new results (i)-(v); open items stated once.
- Repeated disclaimers removed throughout (one methods statement remains in Appendix E).
- Sec. 7: numerical stability in S stated for z <= 0.6; the S-drift at z = 0.7, kappa = 0.4 is
  diagnosed as mode truncation, not Krylov error, by new dense even-sector runs at S = 13 and 14
  (data/dense_z07_S13.json, data/dense_z07_S14.json; they reproduce the archived Lanczos values
  to four digits and show the -1/2 atom with weight 0.081 and 0.074).
- Sec. 7: new paragraph on the infinite-mode limit: the vacuum spectral measure of the limiting
  quadrature is the Bernoulli convolution with parameter sqrt(z); absolutely continuous for
  z = 1/2 (Garsia) and for a.e. z in (1/4,1) (Solomyak; Shmerkin), hence no limiting mass at the
  bin edges and norm convergence of X|0>, Z|0>. Filter-boundary mass and other spectral measures
  remain open; existence of the infinite-mode probabilities is stated as a conjecture.
- Sec. 8: pointer to the Acknowledgments; new Acknowledgments section recording Sorella's
  confirmation of the corrected values (replaces the private-communication citation removed in v2).
- Conclusions rewritten: positive results first, then what is not shown.
- Small fixes: s-lim typo in Eq. (18); Fig. 1 caption (triangles = minus convention only);
  Sec. 3 wording; "cost" wording in Sec. 5; Appendix D text and caption; Appendix E rewritten.
- Bibliography: Erdos 1939, Garsia 1962, Solomyak 1995, Shmerkin 2014 added.

## Not changed
- All numerical data, figures, Tables 1-3, 5, 6 and the appendices A-C.
- The decision (v2) not to claim an asymptotic rate for the hard-bin convergence.

# v4 (26 October 2026, late evening): physical motivation pass on v3

Prose and one new figure only; no number, data file or generated block changed (the generator
reproduces every block of v4 unchanged).

- New Fig. 1: (a) the three detectors applied to one composite field and what each resolves of
  the quadrature spectrum; (b) the quadrature lattice of a Frenkel-like coboson with S = 16
  (vacuum weights on the stems) against the bins of the sign function and the oscillator
  distribution, showing the four lattice points exactly on bin edges (25% of the vacuum weight).
- Abstract and introduction rewritten around the physical framing: three detectors (classical
  drive, intensity correlation, binned homodyne) on one composite; the discrete quadrature
  spectrum as the single mechanism; the two unexpected conclusions (Schmidt-number-3 composite
  yields a singlet; the singlet comes from entanglement between the resolved qubit and the
  unresolved pair structure; a composite too close to one pair yields none).
- Sec. 2: new paragraph "Physical scales" placing Frenkel aggregates, Wannier excitons in dots
  and bulk, and cold-atom dimers on the Schmidt-number axis of the paper.
- Section titles and openings reframed by detector; Sec. 6 and 7 open with the physical question
  they answer; Sec. 5.2 gives the physical reading of the multiplicity space.
- Figure and table captions rewritten to say what the reader should see and why.
- Robustness table and Lanczos table moved to Appendix E (main text now has four tables).
- Reference added: Deng, Haug, Yamamoto, Rev. Mod. Phys. 82, 1489 (2010).

# v4b (26 October 2026): figure and reference pass

- Fig. 2(b): legend now "raw sequential (not a singlet)" / "corrected: exact singlet"; the
  perfect-square triangles are removed from panel (b) (they remain in (a)); caption explains
  why the raw curve lies above the oscillator value.
- Fig. 3 right panel: the omitted-weight plot z^S is replaced by the S = 19 values of delta_D,
  eps, t_0.6, the vacuum weight at K = +-1, 10 p_0.6 and p_raw versus purity (data from
  legacy_nonflat_scan.json); caption marks the z = 0.8, 0.9 points as unconverged in S.
  make_assets.py updated accordingly; it reproduces every block.
- References added (23 -> 35): Combescot et al. Phys. Rep. 2008; Combescot & Shiau 2015;
  Pogosov & Combescot 2010; Chudzicki, Oke, Wootters 2010; Tichy, Bouvrie, Molmer PRL 2012;
  Kasprzak et al. 2006; Combescot, Combescot, Dubin 2017; Gilchrist, Deuar, Reid 1998;
  Munro 1999; Wenger et al. 2003; Garcia-Patron et al. 2004; Banaszek & Wodkiewicz 1999;
  Chen et al. 2002; Aharonov, Pendleton, Petersen 1969; Vernaz-Gris et al. 2014;
  Ketterer et al. 2016; Halmos 1969; Supic & Bowles 2020. Cited in the introduction
  (coboson formalism; entanglement and bosonicity; exciton/polariton coherence; dichotomised
  homodyne Bell tests; modular variables), in Sec. 2 (moth-eaten effect) and Sec. 5
  (two-subspace theorem; self-testing).

# v4c (29 October 2026): Bell value of the raw protocol; detector relabelling

- Detectors relabelled so that the labels follow the text order: (A) classical drive,
  (B) binned homodyne, (C) intensity correlations (previously B and C were interchanged).
  Fig. 1(a) boxes reordered accordingly.
- New code/bell_raw.py and data/bell_raw_scan.json, data/bell_raw_8000.json: Bob-optimised
  CHSH value of the raw sequential state (Appendix A protocol) for every rank of the flat scan
  up to 4096, both tie conventions at perfect squares, plus S = 8000.
- Table 1: new column B_raw. New Fig. 3: B_raw versus S with the 2 sqrt 2 and local-bound lines.
- Sec. 5.2: the CHSH value 2 sqrt 2 of the corrected protocol is stated as a tautology of the
  recovered algebra; the Bell value is informative only for the uncorrected protocol.
- Sec. 6: new paragraph "The raw protocol in Bell units" comparing the two protocols.
- Introduction and conclusions: the Bell disclaimers reduced to one clause each.
- make_assets.py extended (flat_table column, bell_figure block); it reproduces every block.
- Same changes applied to undergrad_version.tex.
- (v4c, later) Sec. 5.2: the CHSH value 2 sqrt 2 identified as the self-testing certificate an
  experiment would use (Kaniewski 2016; Supic & Bowles 2020). Sec. 6: Kaniewski's bound
  F >= 1/2 + (1/2)(B - B*)/(2 sqrt 2 - B*), B* = (16+14 sqrt 2)/17, applied to the raw state:
  certified singlet fidelity 0.68 (S=8), 0.63 (32), 0.75 (128), 0.83 (512), 0.82 (1024),
  0.88 (3956), 0.90 (8000); nothing certified at S=17; at least 0.64 for all S >= 64.
- (30 Oct) Title changed to "Discrete quadrature spectrum of composite bosons: Weyl relation,
  intensity correlations, and binned homodyne detection". Author names removed from the running
  text in favour of reference numbers (Sorella, Law, Kaniewski); established eponyms kept with
  their references (Jordan/Halmos, Tsirelson, Anderson state now cited to Anderson 1958).

# v5 (30 October 2026)
v5 is the state of the manuscript after the 26-30 October passes listed above (v3, v4, v4b, v4c
and the 30 October title/name pass), renamed: coboson_paper_v5.tex, undergrad_version_v5.tex.
Generated blocks of both files are reproduced by `python code/make_assets.py --manuscript <file>`.
Note: the undergraduate version previously carried the generated blocks without markers, so the
Bell column of Table 1 had not reached it; in v5 all nine blocks are marked and identical to
those of coboson_paper_v5.tex, and the generator reproduces both files.
- (30 Oct, later) Final paragraph of the conclusions replaced: the list of caveats ("What the
  results do not show") is removed -- its items are stated where the objects are introduced --
  and replaced by "Open questions and outlook": the four open problems with what is known about
  each, and a closing paragraph stating the positive content of the work. Same in both versions.

# v6 (30 October 2026): revision after the independent review of v5

Input: the independent assessment of v5 with its check script and results (30 October;
validation/history/v5_assessment.md). Every numerical claim of the review was checked against the archived data before being
acted on; the proposed nonatomicity/strong-convergence argument was checked step by step and
incorporated. Both versions edited together; the generator reproduces all ten blocks of both.
No data file, figure block or table value changed. 16 tests pass (3 new). Pages: 25 / 29.

## Accepted and applied (research and undergraduate versions)
- Measurement vs preparation: abstract, Sec. 4 and Appendix A now state that binned homodyne
  statistics define the local observables, while the preparation protocols assume coherent
  spectral filtering and Lüders projections onto joint eigenspaces of Z(x)Z, X(x)X, which homodyne
  detection followed by classical binning does not implement. Sec. 5.2: a CHSH value of 2 sqrt 2
  certifies state and observables on the support up to local isometries, not the internal
  operations; "whenever p > 0" added to the three places that state the corrected value.
- Numerical prose: "established to three digits" replaced by the actual spans over S = 13-19
  (p_0.6: 0.4% of its value at z = 0.5, 1.6% at z = 0.6; kappa = 0.4 quantities 1-3%); Fig. 4
  caption no longer says "stays finite" / "infinite-mode composites" (now: finite truncations
  consistent with a nonzero limit); Table 3 caption likewise; "Schmidt number three" ->
  "3.00 (19-mode truncation)"; fidelity bound "for every S >= 64" -> "every sampled rank S >= 64,
  + convention (minimum 0.642 at S = 71; 0.631 at S = 64 with the - convention)"; fidelity defined
  as extractability up to local isometries; S = 17: "no improvement over the trivial 1/2";
  Table 2 caption corrected (four of six above 1%; w = 3 and w = 4 below); p_raw range corrected
  to 2.6% (S = 13) - 13.5% (S = 58), above 7% for S >= 256.
- Claims: "commutator a third away from unity" -> "normalisation ratio F_2/F_1 = 1 - P a third
  below unity" (the commutator deviation on the one-pair state is 2P = 2/3); "no finite set of
  moments determines them" -> "the purity and the third moment do not determine them"; the drive
  is described as a smooth fundamental-harmonic probe with a dilute moment expansion, not as a
  "low-order function that sees the first few moments" (Sec. 1, Sec. 3 closing sentence, Fig. 1
  caption, abstract); "lattice with 2^S points ... Cantor-like" -> 2^S signed sums with
  multiplicity, S+1 distinct values for the flat spectrum, interval or Cantor support for
  infinitely many modes, nonatomic spectral measure; the explicit criterion sum sqrt(lambda_k) <
  pi/2 is kept and stated not to follow from purity alone; Fig. 2 caption "commutator
  deviation"; the multiplicity factor M is described as the observable-defined logical factor,
  shared by the oscillator (Bloch length 0.85), with the Schmidt dependence of the block weights
  as the composite-specific content (Sec. 1 second conclusion, Sec. 5.2); physical scales
  qualified as order-of-magnitude assignments and the polariton readout as requiring a coupling
  model (Sec. 2).
- Sec. 7, infinite-mode limit: the Bernoulli-convolution paragraph is replaced by Lemma 2
  (nonatomicity of the law of sum a_k eps_k for summable a_k) and Proposition 2 (strong convergence
  of X_S, Z_S, K_S on the vacuum incomplete tensor product, identified with L^2 of the fair
  product measure on sign sequences; convergence of filter, corrected observables, singlet
  projector and vacuum probability for every cutoff that is not an eigenvalue of |K_infty|, i.e.
  all but countably many). The Q_r case uses Q_r = (r/b) i^N Q_w i^-N (checked numerically on
  three modes). What remains open is stated: the cutoffs 0.4, 0.6 are not shown to be
  non-exceptional, positivity of the limits, and a rate. The Bernoulli references are retained
  in one sentence. Conclusions updated accordingly.
- Conclusions, closing paragraph: no claim that compositeness is "the structure the resource is
  made of" or that the composite "fails every conventional test"; the defensible statement
  (poor performance under conventional diagnostics does not preclude an exact recovered logical
  qubit with calculable losses, by a construction with an oscillator counterpart) replaces it.
- Appendix E: the reproduction statement is narrowed to the identified scripts
  (`code/independent/`) and the prose statistics read from the archived scans.

## Accepted and applied (undergraduate version only)
- Weyl background: D(z)D(w) = e^{(zw*-z*w)/2} D(z+w), hence D(z)D(w) = e^{zw*-z*w} D(w)D(z);
  phase e^{+2irb} = -1 at 2rb = pi.  Displacement background: Q_r = -ir(a^+ - a) = -r sqrt2 p
  (sign), vacuum variances 1/2 for x, p and r^2, b^2 for Q_r, Q_w.  Sec. 2: the false statement
  that no nested commutator vanishes on the vacuum replaced ([B,[B,B^+]] does; [Delta,B^+]|0> does
  not; the BCH series does not collapse to a phase).  Functions-of-an-operator background: same
  outcome statistics, different post-measurement state.  Jordan background: XK = (Z + XZX)/2 = KX
  written out; degenerate K-eigenspaces contain many two-dimensional blocks.  g^(2) background:
  "standard test" -> "standard signature ... a necessary condition".  Title note "annotated
  advanced-undergraduate version" and a reading route added.  New Background paragraph on
  spectral measures, atoms and coin-toss sums before Lemma 2 (only nonatomicity is used).

## Package
- README rewritten for v6 (both sources, PDFs distributed, bell_raw.py, Bell datasets, dense
  S = 13/14 runs, independent scripts, narrow reproduction claim, licence); LICENSE (MIT, code
  and data) added -- to be confirmed by the authors.
- code/tests.py: three Bell tests (rank-four values 1 + sqrt 3 and 2.14431716999 against the
  review's implementation; five flat rows against data/bell_raw_scan.json; Tsirelson value of
  the corrected protocol at S = 8, kappa = 1/2).
- code/independent/: verify_rank4_flat.py, verify_expansions.py, verify_revision_numbers.py,
  independent_review_v5.py (+ results; rerun on this package: all values identical).
- validation/validation.json, provenance.json rewritten for v6 (pages, references, blocks,
  hashes, test count); SHA256SUMS added.

## Considered and not applied, or applied differently
- "Lattice" is kept as a word for the flat-spectrum quadrature spectrum (S+1 equally spaced
  points) and in figure labels; the general case is called "discrete spectrum" or "signed sums".
- The review's "optional efficiency improvement" for bell_raw.py (rank-4 support) is not
  implemented; the archived values are reproduced by two independent dense implementations.
- Author/affiliation line and submission format: left for the authors.
