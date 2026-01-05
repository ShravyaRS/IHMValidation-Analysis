#!/bin/bash

echo "Debugging validation failures..."
echo ""

# Test with a single structure to see detailed error
echo "Testing PDBDEV_00000001 with verbose output:"
singularity exec IHMValidation/ihmvalidation.sif ihm_validate test-data-extended/PDBDEV_00000001.cif -o analysis/debug_test 2>&1

echo ""
echo "Checking what validation commands are available:"
singularity exec IHMValidation/ihmvalidation.sif ls /usr/local/bin/ | grep -i val

echo ""
echo "Checking Python modules:"
singularity exec IHMValidation/ihmvalidation.sif python3 -c "import ihm_validation; print(ihm_validation.__file__)"

echo ""
echo "Trying alternative command format:"
singularity exec IHMValidation/ihmvalidation.sif python3 -m ihm_validation test-data-extended/PDBDEV_00000001.cif
