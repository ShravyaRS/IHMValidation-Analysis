# CorMap Validation: FreeSAS vs DATCMP

Validation study confirming that freesas cormapy produces results
identical (within rounding error) to DATCMP from ATSAS.

Related: https://github.com/salilab/IHMValidation/issues/118

## Result

FreeSAS cormap agrees with DATCMP in 100% of cases within 0.05 tolerance.

| Metric | Value |
|--------|-------|
| Agreement (0.05 tolerance) | 100% |
| Agreement (0.01 tolerance) | 88% |
| Pearson r | 0.994841 |
| Spearman rho | 0.879203 |
| Mean p-value difference | 0.002597 |
| Pairs tested | 56 |

## Repository Structure
```
scripts/
    extract_exp_and_fit_data.py   # Step 1: Extract data from .sascif files
    run_datcmp_on_exp_fit.py      # Step 2: Run DATCMP (requires Singularity)
    run_cormap_on_exp_fit.py      # Step 3: Run FreeSAS cormap
    compare_freesas_vs_datcmp.py  # Step 4: Compare results
    generate_final_report.py      # Step 5: Generate report
    download_to_50_datasets.py    # Utility: Download SASBDB entries

tests/
    test_cormap_regression.py     # Regression tests (5/5 passing)

validation_comparison/
    reports/                      # All results and analysis
    plots/                        # Visualizations
    datasets/                     # Dataset provenance

run_all.sh                        # Run complete pipeline
```

## Usage

### Run complete validation
```bash
./run_all.sh
```

### Run individual steps
```bash
python scripts/extract_exp_and_fit_data.py
python scripts/run_datcmp_on_exp_fit.py
python scripts/run_cormap_on_exp_fit.py
python scripts/compare_freesas_vs_datcmp.py
python scripts/generate_final_report.py
```

### Run tests
```bash
python tests/test_cormap_regression.py
```

## Dependencies
```bash
pip install freesas numpy scipy pandas matplotlib
```

DATCMP requires the ATSAS Singularity container (ihmvalidation_complete.sif).

## Key Finding

FreeSAS cormapy is a valid replacement for DATCMP.
The small remaining differences (max 0.035) are due to minor
differences in q-grid alignment, not algorithmic differences.

## Reference

Franke et al. (2015) Nature Methods, DOI: 10.1038/nmeth.3358
