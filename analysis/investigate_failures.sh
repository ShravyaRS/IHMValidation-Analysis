#!/bin/bash

echo "=========================================="
echo "INVESTIGATING VALIDATION FAILURES"
echo "=========================================="
echo ""

failed_structures=(
    "PDBDEV_00000010"
    "PDBDEV_00000020"
    "PDBDEV_00000035"
    "PDBDEV_00000040"
)

for struct in "${failed_structures[@]}"; do
    echo "Analyzing $struct..."
    echo "Running with verbose output to see exact error:"
    
    singularity exec IHMValidation/ihmvalidation.sif python3 /opt/IHMValidation/ihm_validation/ihm_validator.py \
        -v \
        -f "test-data-extended/${struct}.cif" \
        --output-root "analysis/debug" \
        --output-prefix "${struct}_debug" \
        2>&1 | tail -50
    
    echo ""
    echo "---"
    echo ""
done
