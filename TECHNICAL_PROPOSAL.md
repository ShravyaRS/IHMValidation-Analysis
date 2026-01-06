# Technical Proposal: IHMValidation Installability

## Problem Statement
IHMValidation currently requires users to call scripts with full paths:
```
python3 /opt/IHMValidation/ihm_validation/ihm_validator.py -f file.cif
```

This is not standard Python package behavior.

## Proposed Solution

### 1. Add setup.py
Create standard Python package configuration with:
- Package metadata
- Dependency specifications  
- Console script entry points

### 2. Refactor ihm_validator.py
Wrap main execution logic in a main() function that can be called as entry point.

### 3. Container Integration
Update container build to install package in editable mode, supporting dev mounts.

## Expected Outcome

After implementation:
```bash
# Standard installation
pip install ihm-validation

# Clean command-line usage
ihm_validate -f structure.cif

# Dev workflow with mounted directory
singularity exec -B /local/dev:/opt/IHMValidation container.sif ihm_validate -f file.cif
```

## Benefits
1. Standard Python package behavior
2. Easier scripting and automation
3. Better development workflow
4. Cleaner user experience
5. Proper dependency management

## Implementation Risk
Low - maintains backward compatibility while adding new capability.

## Testing Plan
1. Local installation test
2. Entry point functionality test
3. Container installation test
4. Dev mount workflow test
5. Validation functionality test (ensure nothing breaks)

## Timeline
3 weeks part-time after exams
