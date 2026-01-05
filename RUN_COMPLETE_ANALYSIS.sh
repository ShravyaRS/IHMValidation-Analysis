#!/bin/bash

echo "============================================================"
echo "HIGH-QUALITY METRIC ANALYSIS PIPELINE"
echo "============================================================"
echo ""

echo "Step 1: Downloading additional structures..."
bash analysis/download_structures.sh

echo ""
echo "Step 2: Extracting metrics from all structures..."
python3 analysis/extract_metrics.py

echo ""
echo "Step 3: Creating visualizations..."
python3 analysis/visualize_metrics.py

echo ""
echo "Step 4: Generating research report..."
python3 analysis/generate_report.py

echo ""
echo "============================================================"
echo "ANALYSIS COMPLETE"
echo "============================================================"
echo ""
echo "Output locations:"
echo "  Data:    analysis/data/"
echo "  Figures: analysis/figures/"
echo "  Report:  analysis/reports/METRIC_ANALYSIS_REPORT.html"
echo ""
echo "Open the HTML report in your browser!"
