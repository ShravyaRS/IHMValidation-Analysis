
#!/bin/bash
#
# phase6_working_solution.sh - Development Phase 6
#
# Purpose: Incremental development and testing script
# Part of systematic debugging process (Phase 1-8)
# This script represents intermediate development state
#

set -e

echo "=========================================="
echo "PHASE 6: Final Working Solution"
echo "=========================================="

# Step 1: Install ALL missing dependencies
echo -e "\n[1/5] Installing ALL dependencies..."
pip install bokeh jinja2 plotly pytz pdfkit ihm matplotlib numpy scipy || echo "Some deps may have failed"

# Step 2: Check how the original script is supposed to run
echo -e "\n[2/5] Checking original usage..."
cd ~/projects/IHMValidation-Analysis/IHMValidation

# Look at the actual imports in ihm_validator.py
echo "Imports in ihm_validator.py:"
head -40 ihm_validation/ihm_validator.py | grep -E "^import|^from"

# Step 3: Run from the correct directory
echo -e "\n[3/5] Running validator from correct directory..."
cd ~/projects/IHMValidation-Analysis/IHMValidation/ihm_validation

# Run it with proper Python path
PYTHONPATH="$(pwd):$PYTHONPATH" python3 ihm_validator.py \
    ../../test-data/PDBDEV_00000001.cif \
    --output ../../validation-outputs/final1/ 2>&1 | tee ../../reports/final_run1.log || echo "Exit code: $?"

# Step 4: Check output
echo -e "\n[4/5] Checking outputs..."
cd ~/projects/IHMValidation-Analysis

if [ -d validation-outputs/final1 ]; then
    echo "✓ Output directory created!"
    echo -e "\nGenerated files:"
    find validation-outputs/final1 -type f -exec ls -lh {} \;
    
    echo -e "\nChecking for JSON output:"
    find validation-outputs/final1 -name "*.json" -exec cat {} \;
    
    echo -e "\nChecking for HTML output:"
    find validation-outputs/final1 -name "*.html" | head -5
else
    echo "⚠ No output directory"
    echo -e "\nLast 30 lines of log:"
    tail -30 reports/final_run1.log
fi

# Step 5: Create comprehensive analysis script
echo -e "\n[5/5] Creating comprehensive analysis..."

cat > scripts/final_analysis.py << 'ANALYSIS'
#!/usr/bin/env python3
"""
Comprehensive analysis of IHMValidation results
"""
import os
import json
import glob
from pathlib import Path

print("\n" + "="*60)
print("IHMValidation Comprehensive Analysis")
print("="*60)

# Analyze validation outputs
output_dirs = [
    'validation-outputs/final1',
    'validation-outputs/run1', 
    'validation-outputs/test1',
    'validation-outputs/test2'
]

findings = {
    'outputs_found': [],
    'json_files': [],
    'html_files': [],
    'pdf_files': [],
    'errors': []
}

for out_dir in output_dirs:
    if os.path.exists(out_dir):
        findings['outputs_found'].append(out_dir)
        
        # Find all files
        for root, dirs, files in os.walk(out_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if f.endswith('.json'):
                    findings['json_files'].append(filepath)
                elif f.endswith('.html'):
                    findings['html_files'].append(filepath)
                elif f.endswith('.pdf'):
                    findings['pdf_files'].append(filepath)

print(f"\n✓ Found {len(findings['outputs_found'])} output directories")
print(f"  - JSON files: {len(findings['json_files'])}")
print(f"  - HTML files: {len(findings['html_files'])}")
print(f"  - PDF files: {len(findings['pdf_files'])}")

# Parse JSON if available
if findings['json_files']:
    print(f"\n{'='*60}")
    print("Validation Results from JSON:")
    print(f"{'='*60}")
    
    for json_file in findings['json_files']:
        print(f"\n📄 {json_file}:")
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            # Pretty print key metrics
            if isinstance(data, dict):
                for key, value in list(data.items())[:10]:
                    if isinstance(value, (str, int, float, bool)):
                        print(f"  {key}: {value}")
                    elif isinstance(value, dict):
                        print(f"  {key}: {len(value)} items")
                    elif isinstance(value, list):
                        print(f"  {key}: {len(value)} items")
        except Exception as e:
            print(f"  ✗ Could not parse: {e}")

# Check log files for key information
print(f"\n{'='*60}")
print("Analyzing Log Files:")
print(f"{'='*60}")

log_files = glob.glob('reports/*.log')
for log_file in log_files:
    print(f"\n📋 {log_file}:")
    
    with open(log_file) as f:
        content = f.read()
    
    # Look for key indicators
    if 'Error' in content or 'error' in content:
        errors = [line for line in content.split('\n') if 'error' in line.lower()]
        print(f"  ⚠ Errors found: {len(errors)}")
        for err in errors[:3]:
            print(f"    - {err[:100]}")
    
    if 'Success' in content or 'complete' in content.lower():
        print(f"  ✓ Contains success indicators")
    
    # Count validation mentions
    sas_count = content.lower().count('sas')
    cx_count = content.lower().count('crosslink') + content.lower().count('cx')
    em_count = content.lower().count('em ') + content.lower().count('electron microscopy')
    
    print(f"  Validation mentions: SAS({sas_count}), CX({cx_count}), EM({em_count})")

# Save comprehensive findings
findings_file = 'reports/COMPREHENSIVE_FINDINGS.json'
with open(findings_file, 'w') as f:
    json.dump(findings, f, indent=2)

print(f"\n{'='*60}")
print(f"✓ Analysis complete!")
print(f"  Results saved to: {findings_file}")
print(f"{'='*60}\n")
ANALYSIS

chmod +x scripts/final_analysis.py
python3 scripts/final_analysis.py

echo ""
echo "=========================================="
echo "✓ Phase 6 Complete!"
echo "=========================================="
echo ""
echo "KEY FILES TO REVIEW:"
echo "  1. reports/final_run1.log - Main validation log"
echo "  2. validation-outputs/final1/ - Generated outputs"
echo "  3. reports/COMPREHENSIVE_FINDINGS.json - Analysis summary"
echo ""
echo "ACHIEVEMENT STATUS:"
echo "  Goal #1 (New Insights): Check validation outputs"
echo "  Goal #2 (Bugs Found): Documented in logs"
echo "  Goal #3 (Documentation): Issues identified"
echo "  Next: Goals #4, #5, #6"
echo ""

