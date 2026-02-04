# DATCMP vs Python CorMap Validation

## Objective
Verify if a pure Python implementation of the CorMap algorithm can replace DATCMP from the ATSAS suite for SAS validation in IHM workflows (GitHub Issue #118).

## Results Summary

- **Datasets:** 6 experimental-fitted SAS profile pairs from PDB-IHM (SASBDB)
- **Agreement:** 100% of valid cases within 0.05 tolerance
- **Correlation:** r = 0.999998 (essentially perfect)
- **Edge Cases:** Both methods correctly identified 1/6 as undefined
- **Performance:** Python implementation ~1000x faster

## Recommendation
✅ **YES** - Python CorMap is suitable to replace DATCMP for CorMap-based validation in IHM workflows.

## Files

### Reports
- `FINAL_VALIDATION_REPORT.txt` - Complete technical report
- `datcmp_vs_cormap_comparison.csv` - Detailed comparison data
- `SUMMARY_FOR_ARTHUR.txt` - Executive summary

### Plots
- `datcmp_vs_cormap_comparison.png` - Scatter plots and comparison charts

### Scripts
See `../scripts/` directory:
- `cormap_implementation.py` - Python CorMap algorithm
- `extract_exp_and_fit_data.py` - Extract data from .sascif files
- `run_datcmp_on_exp_fit.py` - Run DATCMP validation
- `run_cormap_on_exp_fit.py` - Run Python CorMap validation
- `compare_datcmp_cormap_final.py` - Statistical comparison
- `generate_final_report.py` - Generate validation report

## How to Reproduce
```bash
# 1. Extract experimental and fitted data
python scripts/extract_exp_and_fit_data.py

# 2. Run DATCMP validation
python scripts/run_datcmp_on_exp_fit.py

# 3. Run Python CorMap validation
python scripts/run_cormap_on_exp_fit.py

# 4. Compare results
python scripts/compare_datcmp_cormap_final.py

# 5. Generate report
python scripts/generate_final_report.py
```

## References
- Franke et al. (2015) Nature Methods, DOI: 10.1038/nmeth.3358
- GitHub Issue: https://github.com/salilab/IHMValidation/issues/118
