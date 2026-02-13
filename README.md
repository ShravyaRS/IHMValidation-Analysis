# CorMap Validation: FreeSAS (cormapy) vs DATCMP

Validation study confirming that **FreeSAS cormapy** can replace **DATCMP** (ATSAS) for CorMap goodness-of-fit testing in the [IHMValidation](https://github.com/salilab/IHMValidation) pipeline.

**Related**: [salilab/IHMValidation#118](https://github.com/salilab/IHMValidation/issues/118)

## Key Result

FreeSAS cormapy agrees with DATCMP in **100% of comparable cases** (30/30) within a 0.05 p-value tolerance.

| Metric | Value |
|---|---|
| DATCMP comparisons | 30 |
| Agreement (Δp ≤ 0.05) | **30/30 (100%)** |
| Mean p-value difference | 0.002125 |
| Max p-value difference | 0.035765 |
| Self-comparison cases | 13 (excluded) |
| Total exp-fit pairs extracted | 104 |

## PDB-IHM Coverage

All 382 PDB-IHM entries were scanned. 25 entries reference SAS data across 22 unique SASBDB codes.

| Status | Count |
|---|---|
| Available and validated | 10/22 |
| Unavailable (HTTP 404 / embargo) | 12/22 |

## Precision Fix

FreeSAS's `LROH.probaLongerRun()` uses float64 arithmetic for the Schilling (1990) recursion, which can accumulate rounding errors for large _n_ on certain platforms (Python 3.13 / NumPy 2.4). This pipeline recomputes the p-value using Python's `Decimal` module for exact arithmetic, while relying on FreeSAS for N and C.

**Example — SASDBD9_FIT_728:**

| Source | N | C | p-value |
|---|---|---|---|
| DATCMP | 543 | 11 | 0.230925 |
| FreeSAS (raw float64) | 543 | 11 | 0.230548 |
| **This pipeline (exact Decimal)** | **543** | **11** | **0.230925** |
| Schilling formula (analytical) | 543 | 11 | 0.230925 |

## Self-Comparison Edge Case

13 fits in the SASBDB sascif files have `I_exp == I_fit` for all points (self-comparisons). FreeSAS correctly returns p = 1.0; DATCMP incorrectly returns p = 0.0 (known bug with zero residuals). These cases are excluded from validation statistics.

## Pipeline
```
Step 1:  python scripts/extract_exp_and_fit_data.py   # Extract exp/fit from .sascif
Step 2:  python scripts/run_datcmp_on_exp_fit.py       # Run DATCMP (requires Singularity)
Step 3:  python scripts/run_cormap_on_exp_fit.py       # Run FreeSAS + exact p-value
Step 4:  python scripts/compare_freesas_vs_datcmp.py   # Compare results
Step 5:  python scripts/generate_final_report.py       # Generate final report
```

Or run everything at once:
```bash
./run_all.sh
```

## Repository Structure
```
scripts/
    extract_exp_and_fit_data.py    # Extract data from _sas_model_fitting block
    run_cormap_on_exp_fit.py       # FreeSAS cormap + exact Decimal p-value
    run_datcmp_on_exp_fit.py       # DATCMP via Singularity container
    compare_freesas_vs_datcmp.py   # Compare FreeSAS vs DATCMP results
    generate_final_report.py       # Generate validation report
    verify_all_cases.py            # Manual verification of all cases
    download_to_50_datasets.py     # Download SASBDB entries

validation_comparison/
    extracted_data/                 # Extracted exp/fit .dat files + metadata
    reports/                        # Final validation reports and CSVs
        FINAL_VALIDATION_REPORT.txt
        cormap_freesas_results.csv
        datcmp_vs_cormap_comparison.csv
        complete_validation_table.csv

tests/
    test_cormap_regression.py      # Regression tests
```

## Dependencies
```bash
pip install freesas numpy scipy pandas
```

DATCMP requires the ATSAS Singularity container (`ihmvalidation_complete.sif`).

## Algorithm

Both tools implement the Schilling (1990) longest-run-of-heads test:

1. Compute residuals: `r_i = I_fit(q_i) − I_exp(q_i)`
2. Find C = longest consecutive run of same-sign residuals
3. Compute p = P(longest run ≥ C | n) via the Schilling recursion

Only intensity values and their ordering matter — q and σ are not used in the p-value calculation.

## Data Extraction

Experimental and fitted intensities are taken directly from the `_sas_model_fitting` loop in each `.sascif` file:
- `_sas_model_fitting.momentum_transfer` → q
- `_sas_model_fitting.intensity` → I_exp
- `_sas_model_fitting.fit` → I_fit

No rebinning or interpolation is applied. Rows with q = 0 are excluded; rows with I_exp = 0 are retained (following SASBDB convention).

## Reference

Franke, D., Jeffries, C.M. & Svergun, D.I. (2015). Correlation Map, a goodness-of-fit test for one-dimensional X-ray scattering spectra. *Nature Methods*, 12, 419–422. [DOI: 10.1038/nmeth.3358](https://doi.org/10.1038/nmeth.3358)

## License

MIT
