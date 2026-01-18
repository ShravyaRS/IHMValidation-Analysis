
#!/bin/bash
#
# Run Test Suite
#
# Tests validation functionality and scientific correctness
#

set -e

echo "============================================================"
echo "IHMValidation Test Suite"
echo "============================================================"
echo ""

# Check if container exists
if [ ! -f "IHMValidation/ihmvalidation_complete.sif" ]; then
    echo "ERROR: Container not found"
    echo "Build container first with: bash install.sh"
    exit 1
fi

echo "Running tests..."
echo ""

# Run unit tests
echo "1. Unit Tests"
echo "   Testing individual components..."
python3 -m pytest tests/unit_tests/ -v

echo ""
echo "2. Integration Tests"
echo "   Testing complete workflow..."
python3 -m pytest tests/integration_tests/ -v

echo ""
echo "3. Scientific Validation Tests"
echo "   Testing biophysical correctness..."
python3 tests/scientific_controls/test_scientific_validation.py

echo ""
echo "============================================================"
echo "✓ All Tests Passed"
echo "============================================================"
echo ""
echo "Test coverage:"
echo "  - Container integrity"
echo "  - Dependency accessibility (ATSAS, Python)"
echo "  - Validation logic (valid/invalid detection)"
echo "  - Complete workflow (end-to-end)"
echo "  - Scientific correctness (discriminates quality)"
echo ""
