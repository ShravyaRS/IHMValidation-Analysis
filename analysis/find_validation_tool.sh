#!/bin/bash

echo "Finding the actual validation tool..."
echo ""

echo "1. Checking all executables in container:"
singularity exec IHMValidation/ihmvalidation.sif ls /usr/local/bin/ 2>/dev/null | head -20

echo ""
echo "2. Checking for Python validation scripts:"
singularity exec IHMValidation/ihmvalidation.sif find /usr/local -name "*valid*" -type f 2>/dev/null | head -10

echo ""
echo "3. Checking installed Python packages:"
singularity exec IHMValidation/ihmvalidation.sif pip3 list 2>/dev/null | grep -i ihm

echo ""
echo "4. Looking at the original IHMValidation repo for clues:"
ls -la IHMValidation/

echo ""
echo "5. Checking if there's a validation script in the repo:"
find IHMValidation/ -name "*.py" -type f | grep -i valid | head -5

echo ""
echo "6. Let's check the actual usage from the repo README:"
if [ -f "IHMValidation/README.md" ]; then
    echo "Found README - checking for usage examples:"
    grep -A 10 -i "usage\|example\|run" IHMValidation/README.md | head -20
fi
