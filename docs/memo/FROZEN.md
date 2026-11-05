# Research manuscript — FINAL and FROZEN (2026-11-04)

The owner approved *The Liquidity Paradox* research manuscript, its LaTeX source, bibliography, figures and
reproducibility supplement as the final V1 research deliverables on 2026-11-04. They are frozen.

- **Approved content commit:** `7e35572dab9f5a4de0c65b02cbfdf2fa4419236d`. Every file listed in `FROZEN.sha256` is
  byte-identical to that commit.
- **Freezing commit:** carries the local tag `memo-v1-final` (local only; nothing is pushed).
- **Verification**, from the repository root:

  ```bash
  shasum -a 256 -c docs/memo/FROZEN.sha256
  ```

  No guard test was added: a new file under `tests/` would change the code tree that the held-out evaluation's freeze
  record pins (`results/closeout_freeze/freeze_record.json`). The hash list above is the check.

## Frozen files

| File | Role |
|---|---|
| `The_Liquidity_Paradox.pdf`, `The_Liquidity_Paradox.tex` | the paper (26 pages) |
| `references.bib` | bibliography (61 references) |
| `Reproducibility_Supplement.pdf`, `Reproducibility_Supplement.tex` | specifications, outputs, version identifiers and pre-evaluation checks |
| `figures/fig1_design.pdf` … `figures/fig5_holdout.pdf`, `figures/make_figures.py` | the five figures and the script that draws them from frozen results |

## Rules while frozen
- No scientific, editorial or formatting change to any frozen file without the owner's explicit authorisation, recorded
  in `docs/DECISIONS.md`.
- No publication, distribution, upload or push without the owner's approval.
- The underlying research results, frozen protocols and reproducibility artifacts are unchanged by this freeze; the paper
  restates them and adds no new analysis of the held-out sessions.
- Any later analysis of the held-out sessions is post hoc and exploratory, and is never cited as confirmation.
- Website and other derived material must reproduce the paper's labels and qualifications as frozen
  (`docs/experiments/FINAL_EVALUATION.md`, section 8).
