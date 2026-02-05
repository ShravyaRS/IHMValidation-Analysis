# Quick Start Guide: DATCMP vs Python CorMap Validation

## Installation

### Prerequisites
- Python 3.8+
- Singularity/Apptainer (for DATCMP)
- Git

### Clone Repository
```bash
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis/IHMValidation
```

### Install Python Dependencies
```bash
pip install numpy scipy pandas matplotlib seaborn
```

## Running the Complete Validation

### Option 1: One-Command (Recommended)
```bash
./run_all.sh
```

This runs the entire pipeline:
1. Data extraction (5 min)
2. DATCMP validation (10 min)
3. Python CorMap validation (1 min)
4. Statistical comparison (1 min)
5. Classification & analysis (1 min)
6. Report generation (1 min)

**Total time**: ~20 minutes

### Option 2: Step-by-Step

#### Step 1: Extract Data
```bash
python scripts/extract_exp_and_fit_data.py
```

#### Step 2: Run DATCMP
```bash
python scripts/run_datcmp_on_exp_fit.py
```

#### Step 3: Run Python CorMap
```bash
python scripts/run_cormap_on_exp_fit.py
```

#### Step 4: Compare Results
```bash
python scripts/compare_datcmp_cormap_final.py
```

#### Step 5: Generate Report
```bash
python scripts/generate_final_report.py
```

## View Results

### Main Report
```bash
cat validation_comparison/reports/FINAL_VALIDATION_REPORT.txt
```

### Plots
```bash
ls validation_comparison/plots/
# - datcmp_vs_cormap_comparison.png
# - bland_altman_plot.png
```

### Classification
```bash
cat validation_comparison/reports/datcmp_vs_cormap_classified.csv
```

## Running Tests

### Regression Tests
```bash
python tests/test_cormap_regression.py
```

Should output:
```
RESULTS: 5 passed, 0 failed
```

## Key Results

Expected outputs:
- **Agreement**: 84% within 0.05 tolerance
- **Correlation**: r = 0.999998 (Pearson), ρ = 0.927 (Spearman)
- **Dataset**: 56 experimental-fitted pairs
- **Performance**: ~1000x faster than DATCMP

## Troubleshooting

### Issue: Singularity container not found
```bash
# Ensure ihmvalidation_complete.sif is in project root
ls -lh ihmvalidation_complete.sif
```

### Issue: Missing SASBDB data
```bash
# Download additional entries
python scripts/download_to_50_datasets.py
```

### Issue: Import errors
```bash
# Install missing packages
pip install numpy scipy pandas matplotlib seaborn
```

## Understanding Output

### P-values
- **p > 0.05**: Good agreement (accept fit)
- **0.01 < p < 0.05**: Moderate agreement
- **p < 0.01**: Poor agreement (reject fit)

### C-values
- **C ≈ log₂(N)**: Expected for random residuals
- **C >> log₂(N)**: Systematic deviations
- **C ≈ N**: Complete failure

### Classifications
- **good_quality_fit**: Both methods agree, p > 0.05
- **moderate_quality_fit**: Both agree, 0.01 < p < 0.05
- **poor_quality_fit**: Both agree, p < 0.01
- **insufficient_overlap**: Both return undefined
- **disagreement**: DATCMP fails, Python succeeds

## Next Steps

### Expand Dataset
```bash
python scripts/download_to_50_datasets.py
./run_all.sh
```

### Run Case Studies
```bash
python scripts/analyze_disagreement_cases.py
# Generates detailed plots in validation_comparison/case_studies/
```

### Calculate Confidence Intervals
```bash
python scripts/calculate_confidence_intervals.py
```

## Support

- **Documentation**: See `validation_comparison/reports/`
- **Issues**: https://github.com/ShravyaRS/IHMValidation-Analysis/issues
- **Paper**: Franke et al. (2015) Nature Methods, DOI: 10.1038/nmeth.3358

## Citation

If you use this validation in your work, please cite:
```
IHM Validation Analysis (2026)
GitHub: https://github.com/ShravyaRS/IHMValidation-Analysis
```
