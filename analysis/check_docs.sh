#!/bin/bash

echo "Checking IHMValidation documentation and usage..."
echo ""

echo "1. Looking at the Python module structure:"
ls -la IHMValidation/ihm_validation/

echo ""
echo "2. Checking __init__.py for entry points:"
cat IHMValidation/ihm_validation/__init__.py | head -30

echo ""
echo "3. Looking for a main script or CLI:"
find IHMValidation/ihm_validation -name "*.py" -exec grep -l "if __name__" {} \;

echo ""
echo "4. Check if there's a setup.py that shows entry points:"
if [ -f "IHMValidation/setup.py" ]; then
    cat IHMValidation/setup.py | grep -A 10 "entry_points"
else
    echo "No setup.py found"
fi

echo ""
echo "5. Let's look at the online documentation:"
echo "Checking docs folder..."
find IHMValidation/docs -name "*.md" -o -name "*.rst" 2>/dev/null | head -5

echo ""
echo "6. Try to import and get help from the module:"
singularity exec IHMValidation/ihmvalidation.sif python3 << 'PYTHON'
import sys
sys.path.insert(0, '/app')
try:
    import ihm_validation
    print("Module imported successfully!")
    print("Available functions/classes:")
    print([x for x in dir(ihm_validation) if not x.startswith('_')])
except Exception as e:
    print(f"Import failed: {e}")
PYTHON

echo ""
echo "7. Check if there's a web server mode (from the templates folder):"
ls -la IHMValidation/templates/ 2>/dev/null
