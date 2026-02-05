#!/bin/bash

echo "================================================================================"
echo "  DATCMP vs Python CorMap Validation Pipeline"
echo "  Complete Reproducible Workflow"
echo "================================================================================"
echo ""

# Check if container exists
if [ ! -f "ihmvalidation_complete.sif" ]; then
    echo "ERROR: ihmvalidation_complete.sif not found!"
    echo "Please ensure the Singularity container is in the current directory."
    exit 1
fi

# Step 1: Extract data
echo "[1/9] Extracting experimental and fitted data from SASBDB entries..."
python scripts/extract_exp_and_fit_data.py || exit 1

# Step 2: Run DATCMP
echo ""
echo "[2/9] Running DATCMP validation (via Singularity container)..."
python scripts/run_datcmp_on_exp_fit.py || exit 1

# Step 3: Run Python CorMap
echo ""
echo "[3/9] Running Python CorMap validation..."
python scripts/run_cormap_on_exp_fit.py || exit 1

# Step 4: Compare results
echo ""
echo "[4/9] Comparing DATCMP vs Python CorMap..."
python scripts/compare_datcmp_cormap_final.py || exit 1

# Step 5: Classify cases
echo ""
echo "[5/9] Classifying edge cases and quality levels..."
python scripts/classify_edge_cases.py || exit 1

# Step 6: Stratify by quality
echo ""
echo "[6/9] Stratifying agreement by data quality..."
python scripts/stratify_by_quality.py || exit 1

# Step 7: Create Bland-Altman plot
echo ""
echo "[7/9] Creating Bland-Altman plot..."
python scripts/create_bland_altman_plot.py || exit 1

# Step 8: Analyze disagreement cases
echo ""
echo "[8/9] Analyzing disagreement case studies..."
python scripts/analyze_disagreement_cases.py || exit 1

# Step 9: Generate final report
echo ""
echo "[9/9] Generating comprehensive final report..."
python scripts/generate_final_report.py || exit 1

echo ""
echo "================================================================================"
echo "  ✓ VALIDATION COMPLETE!"
echo "================================================================================"
echo ""
echo "Results available in:"
echo "  - validation_comparison/reports/FINAL_VALIDATION_REPORT.txt"
echo "  - validation_comparison/plots/"
echo "  - validation_comparison/case_studies/"
echo ""
echo "================================================================================"
