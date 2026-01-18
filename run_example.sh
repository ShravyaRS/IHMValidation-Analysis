#!/bin/bash
#
# Quick Demo: Run IHMValidation on example structure
#
# This script demonstrates the complete workflow in under 5 minutes
#

set -e

echo "============================================================"
echo "IHMValidation Quick Demo"
echo "============================================================"
echo ""

# Check if container exists
if [ ! -f "IHMValidation/ihmvalidation_complete.sif" ]; then
    echo "Container not found. Building now..."
    echo "This is a one-time setup (30-45 minutes)"
    echo ""
    read -p "Continue with build? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo bash install_complete.sh
    else
        echo "Please build container first with: sudo bash install_complete.sh"
        exit 1
    fi
fi

echo "Running validation on example structure..."
echo ""

# Use one of the test structures as example
EXAMPLE_STRUCTURE="test-data-extended/PDBDEV_00000001.cif"

if [ ! -f "$EXAMPLE_STRUCTURE" ]; then
    echo "Test data not found. Using minimal example..."
    EXAMPLE_STRUCTURE="example_data/minimal_structure.cif"
fi

# Run validation
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
    /opt/IHMValidation/ihm_validation/ihm_validator.py \
    -f "$EXAMPLE_STRUCTURE" \
    --output-root example_output \
    --output-prefix demo

echo ""
echo "============================================================"
echo "Demo Complete!"
echo "============================================================"
echo ""
echo "Output files generated in: example_output/demo/"
echo ""

# Check for PDF output
if [ -f "example_output/demo/demo_full_validation.pdf" ]; then
    echo "✓ Full validation report: example_output/demo/demo_full_validation.pdf"
fi

if [ -f "example_output/demo/demo_summary_validation.pdf" ]; then
    echo "✓ Summary report: example_output/demo/demo_summary_validation.pdf"
fi

echo ""
echo "To validate your own structure:"
echo "  singularity exec IHMValidation/ihmvalidation_complete.sif python3 \\"
echo "    /opt/IHMValidation/ihm_validation/ihm_validator.py \\"
echo "    -f your_structure.cif \\"
echo "    --output-root output_dir \\"
echo "    --output-prefix structure_name"
echo ""
