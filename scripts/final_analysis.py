#!/usr/bin/env python3
"""
Comprehensive analysis of IHMValidation results
"""
import os
import json
import glob
from pathlib import Path

print("\n" + "="*60)
print("IHMValidation Comprehensive Analysis")
print("="*60)

# Analyze validation outputs
output_dirs = [
    'validation-outputs/final1',
    'validation-outputs/run1', 
    'validation-outputs/test1',
    'validation-outputs/test2'
]

findings = {
    'outputs_found': [],
    'json_files': [],
    'html_files': [],
    'pdf_files': [],
    'errors': []
}

for out_dir in output_dirs:
    if os.path.exists(out_dir):
        findings['outputs_found'].append(out_dir)
        
        # Find all files
        for root, dirs, files in os.walk(out_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if f.endswith('.json'):
                    findings['json_files'].append(filepath)
                elif f.endswith('.html'):
                    findings['html_files'].append(filepath)
                elif f.endswith('.pdf'):
                    findings['pdf_files'].append(filepath)

print(f"\n✓ Found {len(findings['outputs_found'])} output directories")
print(f"  - JSON files: {len(findings['json_files'])}")
print(f"  - HTML files: {len(findings['html_files'])}")
print(f"  - PDF files: {len(findings['pdf_files'])}")

# Parse JSON if available
if findings['json_files']:
    print(f"\n{'='*60}")
    print("Validation Results from JSON:")
    print(f"{'='*60}")
    
    for json_file in findings['json_files']:
        print(f"\n📄 {json_file}:")
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            # Pretty print key metrics
            if isinstance(data, dict):
                for key, value in list(data.items())[:10]:
                    if isinstance(value, (str, int, float, bool)):
                        print(f"  {key}: {value}")
                    elif isinstance(value, dict):
                        print(f"  {key}: {len(value)} items")
                    elif isinstance(value, list):
                        print(f"  {key}: {len(value)} items")
        except Exception as e:
            print(f"  ✗ Could not parse: {e}")

# Check log files for key information
print(f"\n{'='*60}")
print("Analyzing Log Files:")
print(f"{'='*60}")

log_files = glob.glob('reports/*.log')
for log_file in log_files:
    print(f"\n📋 {log_file}:")
    
    with open(log_file) as f:
        content = f.read()
    
    # Look for key indicators
    if 'Error' in content or 'error' in content:
        errors = [line for line in content.split('\n') if 'error' in line.lower()]
        print(f"  ⚠ Errors found: {len(errors)}")
        for err in errors[:3]:
            print(f"    - {err[:100]}")
    
    if 'Success' in content or 'complete' in content.lower():
        print(f"  ✓ Contains success indicators")
    
    # Count validation mentions
    sas_count = content.lower().count('sas')
    cx_count = content.lower().count('crosslink') + content.lower().count('cx')
    em_count = content.lower().count('em ') + content.lower().count('electron microscopy')
    
    print(f"  Validation mentions: SAS({sas_count}), CX({cx_count}), EM({em_count})")

# Save comprehensive findings
findings_file = 'reports/COMPREHENSIVE_FINDINGS.json'
with open(findings_file, 'w') as f:
    json.dump(findings, f, indent=2)

print(f"\n{'='*60}")
print(f"✓ Analysis complete!")
print(f"  Results saved to: {findings_file}")
print(f"{'='*60}\n")
