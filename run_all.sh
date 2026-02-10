#!/bin/bash
# CorMap Validation Pipeline
# Compares freesas cormap (cormapy) against DATCMP
# Usage: ./run_all.sh

set -e

echo "================================================================="
echo "CorMap Validation Pipeline"
echo "FreeSAS cormap vs DATCMP"
echo "================================================================="

# Check dependencies
python -c "from freesas.cormap import gof" 2>/dev/null || {
    echo "ERROR: freesas not installed. Run: pip install freesas"
    exit 1
}

if [ ! -f "ihmvalidation_complete.sif" ]; then
    echo "ERROR: ihmvalidation_complete.sif not found (needed for DATCMP)"
    exit 1
fi

echo ""
echo "Step 1/4: Extracting experimental and fitted data from SASBDB..."
python scripts/extract_exp_and_fit_data.py

echo ""
echo "Step 2/4: Running DATCMP..."
python scripts/run_datcmp_on_exp_fit.py

echo ""
echo "Step 3/4: Running FreeSAS CorMap..."
python scripts/run_cormap_on_exp_fit.py

echo ""
echo "Step 4/4: Comparing results and generating report..."
python scripts/compare_freesas_vs_datcmp.py
python scripts/generate_final_report.py

echo ""
echo "================================================================="
echo "COMPLETE"
echo "Results: validation_comparison/reports/FINAL_VALIDATION_REPORT.txt"
echo "================================================================="
