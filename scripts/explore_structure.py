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
