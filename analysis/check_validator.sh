#!/bin/bash

echo "Checking ihm_validator.py - the main validation script..."
echo ""

echo "1. Looking at the beginning of ihm_validator.py:"
head -100 IHMValidation/ihm_validation/ihm_validator.py

echo ""
echo "2. Checking for main/argparse section:"
tail -100 IHMValidation/ihm_validation/ihm_validator.py

echo ""
echo "3. Let's try running it directly:"
singularity exec IHMValidation/ihmvalidation.sif python3 IHMValidation/ihm_validation/ihm_validator.py --help 2>&1

echo ""
echo "4. If that doesn't work, try with full path inside container:"
singularity exec IHMValidation/ihmvalidation.sif python3 /app/ihm_validation/ihm_validator.py --help 2>&1
