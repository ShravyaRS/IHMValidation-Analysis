#!/bin/bash
set -e

echo "=========================================="
echo "IHMValidation Analysis Setup"
echo "=========================================="

# Step 1: Check structure
echo -e "\n[1/9] Checking repository structure..."
cd ~/projects/IHMValidation-Analysis/IHMValidation
ls -la | head -20

# Check for dependencies file
echo -e "\n[2/9] Looking for dependencies..."
find . -maxdepth 2 -name "*.txt" | grep -i dep || echo "No dependencies.txt found"
find . -maxdepth 2 -name "requirements*.txt" || echo "No requirements.txt found"

# Check Python structure
echo -e "\n[3/9] Checking Python module structure..."
ls -la master/ 2>/dev/null || echo "No master/ directory"
ls -la master/pyext/src/ 2>/dev/null || echo "No master/pyext/src/"
ls -la master/pyext/src/validation/ 2>/dev/null || echo "No validation/ directory"

# Step 2: Create exploration script
echo -e "\n[4/9] Creating exploration script..."
cd ~/projects/IHMValidation-Analysis
mkdir -p scripts

cat > scripts/explore_structure.py << 'EOF'
#!/usr/bin/env python3
"""Explore IHMValidation structure"""
import os
import sys

print("IHMValidation Code Structure Analysis")
print("="*60)

ihm_base = os.path.expanduser('~/projects/IHMValidation-Analysis/IHMValidation')
print(f"\nBase directory: {ihm_base}")

# Find all Python files
print("\nSearching for Python modules...")
python_files = []
for root, dirs, files in os.walk(ihm_base):
    # Skip hidden and cache directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for file in files:
        if file.endswith('.py'):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ihm_base)
            python_files.append(rel_path)

print(f"\nFound {len(python_files)} Python files:")
for f in sorted(python_files)[:20]:  # Show first 20
    print(f"  - {f}")

if len(python_files) > 20:
    print(f"  ... and {len(python_files) - 20} more")

# Look for main entry points
print("\n" + "="*60)
print("Looking for entry points (files with __main__)...")
entry_points = []
for py_file in python_files:
    full_path = os.path.join(ihm_base, py_file)
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if '__name__' in content and '__main__' in content:
                entry_points.append(py_file)
    except:
        pass

if entry_points:
    print(f"\nFound {len(entry_points)} entry point(s):")
    for ep in entry_points:
        print(f"  - {ep}")
else:
    print("\nNo entry points found with __main__")

# Check for validation modules
print("\n" + "="*60)
print("Validation-related modules:")
validation_modules = [f for f in python_files if 'validation' in f.lower()]
for vm in validation_modules[:10]:
    print(f"  - {vm}")

# Look for README or documentation
print("\n" + "="*60)
print("Documentation files:")
for root, dirs, files in os.walk(ihm_base):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for file in files:
        if file.lower() in ['readme.md', 'readme.rst', 'readme.txt', 'readme']:
            print(f"  - {os.path.relpath(os.path.join(root, file), ihm_base)}")
            break

print("\n✓ Exploration complete")
EOF

chmod +x scripts/explore_structure.py

# Run exploration
echo -e "\n[5/9] Running structure exploration..."
python3 scripts/explore_structure.py

# Step 3: Download test data
echo -e "\n[6/9] Downloading test data..."
cd ~/projects/IHMValidation-Analysis
mkdir -p test-data
cd test-data

if [ ! -f PDBDEV_00000001.cif ]; then
    echo "Downloading PDBDEV_00000001.cif..."
    wget -q https://pdb-ihm.org/cif/PDBDEV_00000001.cif && echo "✓ Downloaded" || echo "✗ Failed"
fi

if [ ! -f PDBDEV_00000010.cif ]; then
    echo "Downloading PDBDEV_00000010.cif..."
    wget -q https://pdb-ihm.org/cif/PDBDEV_00000010.cif && echo "✓ Downloaded" || echo "✗ Failed"
fi

echo -e "\nTest data files:"
ls -lh *.cif 2>/dev/null || echo "No CIF files found"

# Step 4: Find validation scripts
echo -e "\n[7/9] Searching for validation scripts..."
cd ~/projects/IHMValidation-Analysis/IHMValidation
find . -name "validate*.py" -o -name "*validation*.py" | head -10

# Step 5: Check for web interface
echo -e "\n[8/9] Checking for web interface..."
find . -name "app.py" -o -name "server.py" -o -name "wsgi.py" | head -5

# Step 6: Create initial findings document
echo -e "\n[9/9] Creating findings document..."
cd ~/projects/IHMValidation-Analysis

cat > INITIAL_FINDINGS.md << 'FINDINGS'
# IHMValidation Initial Analysis Findings

## Date: $(date)

## Repository Structure

### What We Found
- Repository cloned successfully
- Total size: ~224 MB (large repository with data)
- Python version in use: 3.13.9

### Key Observations
1. **No standard Python package structure**
   - No `requirements.txt` in root
   - No `setup.py` in root
   - Non-standard installation process

2. **Code Organization**
   - See exploration output above for module structure
   - Validation logic likely in subdirectories

3. **Test Data**
   - Downloaded 2 sample structures from PDB-IHM
   - Files ready for testing

## Next Actions Required

### Immediate
1. Locate the actual validation entry point
2. Understand the installation method
3. Test basic validation functionality

### Short-term
1. Create wrapper scripts for ease of use
2. Document actual usage patterns
3. Run validations and collect metrics

### Medium-term
1. Identify bugs and limitations
2. Propose enhancements
3. Create reproducibility framework

## Questions to Answer
- [ ] Where is the main validation script?
- [ ] What are the actual dependencies?
- [ ] How is it meant to be installed?
- [ ] Is there a web interface or CLI only?
- [ ] What's in the test/ directory?

FINDINGS

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review the exploration output above"
echo "2. Check INITIAL_FINDINGS.md"
echo "3. Navigate to the IHMValidation directory and explore"
echo ""
echo "Useful commands:"
echo "  cd ~/projects/IHMValidation-Analysis/IHMValidation"
echo "  find . -name '*.py' | head -20"
echo "  ls -la master/"
echo "  cat README* 2>/dev/null"
echo ""

