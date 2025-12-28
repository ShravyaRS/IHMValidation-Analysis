#!/usr/bin/env python3
"""Analyze the validator code structure"""
import sys
import re

validator_file = 'IHMValidation/ihm_validation/ihm_validator.py'

print("IHM Validator Code Analysis")
print("="*60)

with open(validator_file) as f:
    content = f.read()
    lines = content.split('\n')

# Count lines
print(f"\nTotal lines: {len(lines)}")

# Find imports
print("\nImported modules:")
imports = [line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
for imp in imports[:15]:
    print(f"  {imp.strip()}")
if len(imports) > 15:
    print(f"  ... and {len(imports)-15} more")

# Find functions
print("\nDefined functions:")
functions = re.findall(r'^def (\w+)\(', content, re.MULTILINE)
for func in functions:
    print(f"  - {func}()")

# Find classes
print("\nDefined classes:")
classes = re.findall(r'^class (\w+)', content, re.MULTILINE)
for cls in classes:
    print(f"  - {cls}")

# Check for validation types
print("\nValidation types mentioned:")
for validation_type in ['sas', 'cx', 'em', 'molprobity', 'excluded', 'precision']:
    count = content.lower().count(validation_type)
    if count > 0:
        print(f"  - {validation_type}: {count} occurrences")

print("\n" + "="*60)
