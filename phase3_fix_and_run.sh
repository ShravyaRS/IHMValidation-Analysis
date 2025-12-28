#!/bin/bash
set -e

echo "=========================================="
echo "PHASE 3: Fix Dependencies & Run Analysis"
echo "=========================================="

# Step 1: Install missing dependencies
echo -e "\n[1/6] Installing missing dependencies..."
cd ~/projects/IHMValidation-Analysis/IHMValidation

# Check for dependency information in README or docs
echo "Checking for dependency requirements..."
grep -r "requirements" . --include="*.md" --include="*.txt" --include="*.rst" | head -10

# Install common dependencies for this type of tool
pip install pdfkit ihm python-ihm matplotlib numpy scipy plotly || echo "Some installations may have failed"

# Install wkhtmltopdf (required by pdfkit)
echo -e "\nInstalling wkhtmltopdf..."
sudo apt-get update
sudo apt-get install -y wkhtmltopdf || echo "wkhtmltopdf installation failed (optional)"

# Step 2: Try validation again
echo -e "\n[2/6] Running validation (attempt 2)..."
cd ~/projects/IHMValidation-Analysis

python3 IHMValidation/ihm_validation/ihm_validator.py \
    test-data/PDBDEV_00000001.cif \
    --output validation-outputs/test1/ 2>&1 | tee reports/validation_run1.log

if [ $? -eq 0 ]; then
    echo "✓ Validation successful!"
else
    echo "⚠ Validation had errors - check reports/validation_run1.log"
fi

# Step 3: Check what was generated
echo -e "\n[3/6] Checking output files..."
if [ -d validation-outputs/test1 ]; then
    echo "Output directory contents:"
    ls -lh validation-outputs/test1/
    tree validation-outputs/test1/ 2>/dev/null || find validation-outputs/test1/ -type f
else
    echo "⚠ No output directory created"
fi

# Step 4: Run on second test file
echo -e "\n[4/6] Running validation on second test file..."
python3 IHMValidation/ihm_validation/ihm_validator.py \
    test-data/PDBDEV_00000010.cif \
    --output validation-outputs/test2/ 2>&1 | tee reports/validation_run2.log

# Step 5: Analyze the validation code
echo -e "\n[5/6] Analyzing validation code structure..."
cd ~/projects/IHMValidation-Analysis

cat > scripts/analyze_validator.py << 'ANALYZER'
#!/usr/bin/env python3
"""Analyze the validator code structure"""
import sys
import re

validator_file = 'IHMValidation/ihm_validation/ihm_validator.py'

print("IHM Validator Code Analysis")
print("="*60)

with open(validator_file) as f:
    content = f.read()
    lines = content.split('\n')

# Count lines
print(f"\nTotal lines: {len(lines)}")

# Find imports
print("\nImported modules:")
imports = [line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
for imp in imports[:15]:
    print(f"  {imp.strip()}")
if len(imports) > 15:
    print(f"  ... and {len(imports)-15} more")

# Find functions
print("\nDefined functions:")
functions = re.findall(r'^def (\w+)\(', content, re.MULTILINE)
for func in functions:
    print(f"  - {func}()")

# Find classes
print("\nDefined classes:")
classes = re.findall(r'^class (\w+)', content, re.MULTILINE)
for cls in classes:
    print(f"  - {cls}")

# Check for validation types
print("\nValidation types mentioned:")
for validation_type in ['sas', 'cx', 'em', 'molprobity', 'excluded', 'precision']:
    count = content.lower().count(validation_type)
    if count > 0:
        print(f"  - {validation_type}: {count} occurrences")

print("\n" + "="*60)
ANALYZER

python3 scripts/analyze_validator.py

# Step 6: Document findings
echo -e "\n[6/6] Creating detailed findings report..."

cat > reports/DETAILED_FINDINGS.md << 'FINDINGS'
# IHMValidation Detailed Findings Report

## Date: $(date +%Y-%m-%d)

## Installation Analysis

### Dependencies Issues Found
1. **Missing setup.py/pyproject.toml**
   - Impact: Cannot install via `pip install`
   - Workaround: Direct Python path usage
   - Recommendation: Create proper setup.py

2. **Missing pdfkit dependency**
   - Found: ModuleNotFoundError on first run
   - Fixed: Manual installation required
   - Impact: PDF report generation fails without it

3. **System Dependencies**
   - wkhtmltopdf required for PDF generation
   - Not documented in README (potential issue #1)

### Package Structure
- **Main module**: `ihm_validation/`
- **Entry point**: `ihm_validator.py`
- **Validation modules**: sas.py, cx.py, em.py, molprobity.py, etc.
- **Web interface**: templates/ and static/ directories suggest web server capability

## Validation Runs

### Test File 1: PDBDEV_00000001.cif
- Status: [Check validation_run1.log]
- Output location: validation-outputs/test1/
- Files generated: [List from ls output]

### Test File 2: PDBDEV_00000010.cif
- Status: [Check validation_run2.log]
- Output location: validation-outputs/test2/
- Files generated: [List from ls output]

## Code Quality Observations

### From ihm_validator.py
- Entry point script
- Command-line argument parsing
- Multiple validation type support
- PDF/HTML report generation

### Modular Structure
✓ Good: Separate modules for each validation type
✓ Good: Clear separation of concerns
⚠ Note: Requires proper documentation

## Issues Identified (Goal #2)

### Issue #1: Missing Installation Documentation
**Severity**: High
**Description**: No setup.py or installation guide for dependencies
**Impact**: Users cannot easily install the tool
**Recommendation**: Create setup.py with proper dependencies listed

### Issue #2: pdfkit Not Listed as Dependency
**Severity**: Medium
**Description**: Runtime dependency not documented
**Impact**: Tool crashes on first run
**Reproduction**: Run validator without pdfkit installed

### Issue #3: No Command-Line Tool Installed
**Severity**: Low
**Description**: No `ihm_validate` command after installation
**Impact**: Must use full path to Python script
**Recommendation**: Add console_scripts entry point in setup.py

## New Insights Generated (Goal #1)

### Performance Metrics
[To be filled from validation logs]

### Validation Coverage
- SAS: [Status]
- CX-MS: [Status]
- EM: [Status]
- Molprobity: [Status]

## Next Steps

1. **Immediate**:
   - Extract metrics from validation output
   - Analyze validation reports
   - Document output format

2. **Short-term**:
   - Create setup.py (Enhancement proposal)
   - Run more test cases
   - Benchmark performance

3. **Documentation**:
   - User guide improvements
   - API documentation
   - Installation troubleshooting

FINDINGS

echo ""
echo "=========================================="
echo "✓ Phase 3 Complete!"
echo "=========================================="
echo ""
echo "Review the following:"
echo "  1. reports/validation_run1.log - First validation attempt"
echo "  2. reports/validation_run2.log - Second validation attempt"  
echo "  3. validation-outputs/test1/ - Output files"
echo "  4. validation-outputs/test2/ - Output files"
echo "  5. reports/DETAILED_FINDINGS.md - Comprehensive analysis"
echo ""
echo "Next: Examine validation outputs to extract metrics"
echo ""

