# Implementation Steps for Installability

## Current State
- IHMValidation code exists in: IHMValidation/ihm_validation/
- Main script: IHMValidation/ihm_validation/ihm_validator.py
- Works when called directly with full path
- No setup.py exists

## What You Need To Do

### 1. Create setup.py (DONE above)
Located at: IHMValidation/setup.py

### 2. Modify ihm_validator.py
The script currently has argparse at module level.
Need to wrap the main execution in a main() function:

Current structure (approximately):
```python
parser = argparse.ArgumentParser()
# ... argument definitions ...
args = parser.parse_args()
# ... main code ...
```

Needs to become:
```python
parser = argparse.ArgumentParser()
# ... argument definitions ...

def main():
    args = parser.parse_args()
    # ... main code ...
    
if __name__ == '__main__':
    main()
```

### 3. Test Locally (Outside Container)
```bash
cd IHMValidation
pip install -e .
ihm_validate --help
```

### 4. Update Singularity.def
Add to %post section:
```
cd /opt/IHMValidation
pip3 install -e .
```

### 5. Rebuild Container
```bash
sudo singularity build new_ihmvalidation.sif IHMValidation/singularity/Singularity.def
```

### 6. Test
```bash
singularity exec new_ihmvalidation.sif ihm_validate -f structure.cif
```

## This Is Real Work
This requires:
1. Understanding Python packaging
2. Modifying existing code carefully
3. Testing thoroughly
4. Ensuring backward compatibility

## Why Arthur Wants This
Currently users/scripts must know exact path to validator script.
After this work, they can just call `ihm_validate` like any other tool.
