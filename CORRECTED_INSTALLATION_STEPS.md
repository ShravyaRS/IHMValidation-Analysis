# CORRECTED: IHMValidation Installation & Analysis Steps

## Current Status
✓ Repository cloned to ~/projects/IHMValidation-Analysis/IHMValidation

## PHASE 1: CORRECT INSTALLATION

### Step 1: Check Repository Structure
```bash
cd ~/projects/IHMValidation-Analysis/IHMValidation
ls -la
# You should see: dependencies.txt (NOT requirements.txt)
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment (Python 3.8 recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies from correct file
pip install -r dependencies.txt

# If dependencies.txt doesn't exist, check for it
find . -name "*.txt" | grep -i dep
```

### Step 3: Set Up Environment File
```bash
# Create .env file for configuration
cd ~/projects/IHMValidation-Analysis/IHMValidation

cat > .env << 'ENVFILE'
# IHMValidation Environment Configuration
MOLPROBITY_PATH=/usr/bin/molprobity
ATSAS_PATH=/opt/atsas/bin
OUTPUT_DIR=./validation_output
ENVFILE

# Verify .env file created
ls -la .env
```

### Step 4: Install System Dependencies
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip

# Optional: Install Molprobity for atomic validation
sudo apt-get install -y molprobity

# Or build from source if needed
```

### Step 5: Explore the Codebase Structure
```bash
cd ~/projects/IHMValidation-Analysis/IHMValidation
tree -L 3 master/

# Expected structure:
# master/
# ├── pyext/
# │   └── src/
# │       └── validation/
# ├── test/
# └── ... other files
```

### Step 6: Test Import
```bash
# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/master/pyext/src"

# Test import
python3 << 'PYTEST'
import sys
sys.path.append('./master/pyext/src')

try:
    from validation import get_input_information
    print("✓ IHMValidation module imported successfully!")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("\nAvailable modules:")
    import os
    for root, dirs, files in os.walk('./master/pyext/src'):
        for file in files:
            if file.endswith('.py'):
                print(f"  - {os.path.join(root, file)}")
PYTEST
```

## PHASE 2: EXPLORE THE TOOL

### Step 7: Understand the Module Structure
```bash
cd ~/projects/IHMValidation-Analysis

cat > scripts/explore_structure.py << 'EOF'
#!/usr/bin/env python3
"""Explore IHMValidation structure"""
import os
import sys

ihm_path = os.path.expanduser('~/projects/IHMValidation-Analysis/IHMValidation/master/pyext/src')
sys.path.insert(0, ihm_path)

print("IHMValidation Code Structure")
print("="*60)

# Find all Python files
validation_dir = os.path.join(ihm_path, 'validation')
if os.path.exists(validation_dir):
    print(f"\nValidation modules found in: {validation_dir}\n")
    for file in sorted(os.listdir(validation_dir)):
        if file.endswith('.py'):
            print(f"  - {file}")
            filepath = os.path.join(validation_dir, file)
            # Count lines
            with open(filepath) as f:
                lines = len(f.readlines())
            print(f"    Lines: {lines}")
else:
    print(f"✗ Validation directory not found at: {validation_dir}")

# Try importing
print("\n" + "="*60)
print("Testing imports...\n")

try:
    from validation import get_input_information
    print("✓ get_input_information imported")
except Exception as e:
    print(f"✗ get_input_information: {e}")

try:
    from validation import sas
    print("✓ SAS module imported")
except Exception as e:
    print(f"✗ SAS module: {e}")

try:
    from validation import cx
    print("✓ CX module imported") 
except Exception as e:
    print(f"✗ CX module: {e}")
