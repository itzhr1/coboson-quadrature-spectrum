#!/usr/bin/env bash
# Reproduces the checks recorded in validation/: unit tests, generated manuscript blocks,
# and the independent cross-checks.  Run from the repository root.  Requires Python >= 3.11
# with numpy, scipy and sympy.  Does not rerun the archived scans (see README).
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
echo "== unit tests"
python -m unittest discover -s code -p tests.py -v 2>&1 | tee validation/tests.log
echo "== generated blocks (must print no differences)"
for f in coboson_paper_v10_14 undergrad_version_v10_14; do
  cp manuscript/$f.tex /tmp/$f.regen.tex
  python code/make_assets.py --manuscript /tmp/$f.regen.tex
  diff -q manuscript/$f.tex /tmp/$f.regen.tex && echo "$f: all generated blocks unchanged"
done
echo "== independent checks"
python code/independent/verify_cutoff_curves.py
python code/independent/verify_rank4_flat.py > /dev/null && echo "verify_rank4_flat.py ran"
python code/independent/verify_expansions.py > /dev/null && echo "verify_expansions.py ran"
python code/independent/verify_revision_numbers.py > /dev/null && echo "verify_revision_numbers.py ran"
python code/independent/independent_review_v5.py > /dev/null && echo "independent_review_v5.py ran (validation/independent_review_results.json)"
echo "== done"
