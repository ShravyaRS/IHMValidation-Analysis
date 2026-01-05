#!/bin/bash

echo "Getting usage information from multiple sources..."
echo ""

# Check if there's a CLI script
echo "1. Looking for command-line interface:"
find IHMValidation -type f -name "*.py" | xargs grep -l "argparse\|click\|sys.argv" | head -5

echo ""
echo "2. Check test files for usage examples:"
if [ -d "IHMValidation/tests" ]; then
    echo "Test files found, checking for usage patterns:"
    head -50 IHMValidation/tests/*.py 2>/dev/null | grep -A 3 "validate\|run"
fi

echo ""
echo "3. Let's check the actual documentation online:"
echo "Documentation URL: https://ihmvalidation.readthedocs.io/en/latest/"
echo ""

echo "4. Try running as a module with different flags:"
echo "Testing: python3 -m ihm_validation"
singularity exec IHMValidation/ihmvalidation.sif python3 -m ihm_validation 2>&1 | head -20

echo ""
echo "5. Check if it needs to be run through the web interface:"
find IHMValidation -name "*.py" | xargs grep -l "Flask\|app\.run\|web" | head -3
