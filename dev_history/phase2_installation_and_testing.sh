
#!/bin/bash
#
# phase2_installation_and_testing.sh - Development Phase 2
#
# Purpose: Incremental development and testing script
# Part of systematic debugging process (Phase 1-8)
# This script represents intermediate development state
#

set -e

echo "=========================================="
echo "PHASE 2: Installation & Testing"
echo "=========================================="

# Step 1: Check README for installation instructions
echo -e "\n[1/8] Reading installation instructions..."
cd ~/projects/IHMValidation-Analysis/IHMValidation
cat README.md | head -50

# Step 2: Look for setup.py or pyproject.toml
echo -e "\n[2/8] Checking for installation files..."
ls -la setup.py 2>/dev/null && echo "✓ Found setup.py" || echo "✗ No setup.py"
ls -la pyproject.toml 2>/dev/null && echo "✓ Found pyproject.toml" || echo "✗ No pyproject.toml"
ls -la setup.cfg 2>/dev/null && echo "✓ Found setup.cfg" || echo "✗ No setup.cfg"

# Step 3: Check the main validator script
echo -e "\n[3/8] Examining main validator (ihm_validator.py)..."
head -50 ihm_validation/ihm_validator.py

# Step 4: Try to install the package
echo -e "\n[4/8] Attempting installation..."
cd ~/projects/IHMValidation-Analysis/IHMValidation

# Try pip install in development mode
pip install -e . 2>&1 | tee ../reports/installation.log || echo "Installation via pip failed"

# Step 5: Test import
echo -e "\n[5/8] Testing import..."
python3 << 'PYTEST'
import sys
try:
    import ihm_validation
    print("✓ ihm_validation imported successfully!")
    print(f"  Location: {ihm_validation.__file__}")
    
    # Check what's available
    print("\n  Available modules:")
    for attr in dir(ihm_validation):
        if not attr.startswith('_'):
            print(f"    - {attr}")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)
PYTEST

# Step 6: Check entry point
echo -e "\n[6/8] Checking command-line tools..."
which ihm_validate 2>/dev/null && echo "✓ ihm_validate command available" || echo "⚠ No ihm_validate command"

# Try running the validator directly
echo -e "\n[7/8] Testing validation on sample file..."
cd ~/projects/IHMValidation-Analysis

python3 IHMValidation/ihm_validation/ihm_validator.py \
    --help 2>&1 | head -30 || echo "Could not run validator"

# Step 7: Run actual validation test
echo -e "\n[8/8] Running validation on test file..."
python3 IHMValidation/ihm_validation/ihm_validator.py \
    test-data/PDBDEV_00000001.cif \
    --output validation-outputs/test1/ 2>&1 | tee reports/first_validation.log

echo ""
echo "=========================================="
echo "✓ Phase 2 Complete!"
echo "=========================================="
echo ""
echo "Check the following for results:"
echo "  - reports/installation.log"
echo "  - reports/first_validation.log"
echo "  - validation-outputs/test1/"
echo ""

