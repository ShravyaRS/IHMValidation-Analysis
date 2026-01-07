#!/bin/bash

echo "Testing all 8 structures with ATSAS-fixed container"
echo ""

structures=(
    "PDBDEV_00000001"
    "PDBDEV_00000010"
    "PDBDEV_00000015"
    "PDBDEV_00000020"
    "PDBDEV_00000025"
    "PDBDEV_00000030"
    "PDBDEV_00000035"
    "PDBDEV_00000040"
)

for struct in "${structures[@]}"; do
    echo "============================================================"
    echo "Testing: $struct"
    echo "============================================================"
    
    singularity exec IHMValidation/ihmvalidation_fixed.sif \
        python3 /opt/IHMValidation/ihm_validation/ihm_validator.py \
        -f "test-data-extended/${struct}.cif" \
        --output-root "validation-outputs-fixed" \
        --output-prefix "${struct}" 2>&1 | tail -5
    
    # Check if PDF was generated
    if [ -f "validation-outputs-fixed/${struct}/${struct}_full_validation.pdf" ]; then
        echo "✓ SUCCESS - PDF generated"
    else
        echo "✗ FAILED - No PDF"
    fi
    echo ""
done

echo ""
echo "============================================================"
echo "FINAL RESULTS"
echo "============================================================"
ls -lh validation-outputs-fixed/*/PDBDEV*_full_validation.pdf 2>/dev/null | wc -l
echo "PDFs generated"
