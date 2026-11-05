# The Liquidity Paradox: research paper

**Status: FINAL and FROZEN (2026-11-04).** Approved by the owner as the V1 research deliverable; see `FROZEN.md` and
`FROZEN.sha256`. No change without the owner's explicit authorisation. Not published, uploaded or distributed.

| File | Contents |
|---|---|
| `The_Liquidity_Paradox.pdf` | the paper |
| `The_Liquidity_Paradox.tex` | its LaTeX source |
| `references.bib` | bibliography (every entry checked against a publisher, DOI or index record) |
| `Reproducibility_Supplement.pdf`, `.tex` | specifications, outputs, version identifiers and pre-evaluation checks behind every result |
| `figures/make_figures.py` | draws every figure from frozen result files only |
| `figures/*.pdf` | the five figures |

## Sources

Every number comes from frozen artifacts: the discovery reports and their JSON/CSV outputs (`results/e00{1,2,3,4}/`), the
final protocol (`docs/experiments/FINAL_EVALUATION.md`, frozen at `dcb9b3a`) and the held-out results
(`results/closeout/`). The paper adds no new analysis of the held-out sessions.

## Build

```bash
python3 figures/make_figures.py
```

The figure script needs any Python with matplotlib; the project's pinned environment does not include it. Then, with
pdfLaTeX (TeX Live or TinyTeX with `lmodern`, `natbib`, `booktabs`, `float`):

```bash
pdflatex The_Liquidity_Paradox && bibtex The_Liquidity_Paradox && pdflatex The_Liquidity_Paradox && pdflatex The_Liquidity_Paradox
```

```bash
pdflatex Reproducibility_Supplement && pdflatex Reproducibility_Supplement
```
