#!/usr/bin/env python3
"""
Deep analysis of validation failures
"""

import pandas as pd
from pathlib import Path
import subprocess
import re

def analyze_structure_content(struct_file):
    """Analyze structure file content to understand what data it contains"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {struct_file.name}")
    print(f"{'='*60}")
    
    with open(struct_file, 'r') as f:
        content = f.read()
    
    # Check for different data types
    data_types = {
        'SAS': '_ihm_sas_restraint' in content or 'ihm_sas' in content,
        'Cross-linking': '_ihm_cross_link' in content or 'ihm_cross_link' in content,
        '3DEM': '_ihm_3dem' in content or 'ihm_3dem' in content,
        'Starting models': '_ihm_starting_model' in content,
        'Datasets': '_ihm_dataset_list' in content,
        'Multi-state': '_ihm_multi_state' in content,
        'Ensemble': '_ihm_ensemble' in content,
    }
    
    print(f"\nData types present:")
    for dtype, present in data_types.items():
        status = "✓ YES" if present else "✗ NO"
        print(f"  {dtype:20s}: {status}")
    
    # Check for potential issues
    issues = []
    
    # Check for missing required fields
    if '_entry.id' not in content:
        issues.append("Missing entry ID")
    
    # Check for empty or None values in critical fields
    none_pattern = re.findall(r'\.\s+\.', content)
    if len(none_pattern) > 100:  # arbitrary threshold
        issues.append(f"Many empty fields detected ({len(none_pattern)})")
    
    # Check file structure
    lines = content.split('\n')
    comment_lines = [l for l in lines if l.strip().startswith('#')]
    data_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
    
    print(f"\nFile statistics:")
    print(f"  Total lines: {len(lines)}")
    print(f"  Data lines: {len(data_lines)}")
    print(f"  Comment lines: {len(comment_lines)}")
    print(f"  File size: {struct_file.stat().st_size / (1024*1024):.2f} MB")
    
    if issues:
        print(f"\n⚠ Potential issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    return data_types, issues

def compare_success_vs_failure():
    """Compare characteristics of successful vs failed structures"""
    
    df = pd.read_csv('analysis/data/validation_results.csv')
    
    print("\n" + "="*60)
    print("COMPARING SUCCESSFUL VS FAILED STRUCTURES")
    print("="*60)
    
    successful = df[df['validation_success'] == True]['structure'].tolist()
    failed = df[df['validation_success'] == False]['structure'].tolist()
    
    print("\nAnalyzing successful structures...")
    success_data = {}
    for struct in successful:
        struct_file = Path(f'test-data-extended/{struct}.cif')
        if struct_file.exists():
            data_types, issues = analyze_structure_content(struct_file)
            success_data[struct] = data_types
    
    print("\n" + "="*60)
    print("Analyzing failed structures...")
    failure_data = {}
    for struct in failed:
        struct_file = Path(f'test-data-extended/{struct}.cif')
        if struct_file.exists():
            data_types, issues = analyze_structure_content(struct_file)
            failure_data[struct] = data_types
    
    # Compare patterns
    print("\n" + "="*60)
    print("PATTERN ANALYSIS")
    print("="*60)
    
    # Check if SAS data correlates with failure
    print("\nSAS Data Correlation:")
    success_sas = sum(1 for s in success_data.values() if s.get('SAS', False))
    failure_sas = sum(1 for s in failure_data.values() if s.get('SAS', False))
    
    print(f"  Successful with SAS: {success_sas}/{len(success_data)}")
    print(f"  Failed with SAS: {failure_sas}/{len(failure_data)}")
    
    if failure_sas > success_sas:
        print("  ⚠ SAS data may be associated with failures!")
    
    # Check other patterns
    print("\nData Type Frequency:")
    for dtype in ['Cross-linking', '3DEM', 'Multi-state', 'Ensemble']:
        success_count = sum(1 for s in success_data.values() if s.get(dtype, False))
        failure_count = sum(1 for s in failure_data.values() if s.get(dtype, False))
        print(f"  {dtype}:")
        print(f"    Success: {success_count}/{len(success_data)}")
        print(f"    Failed:  {failure_count}/{len(failure_data)}")

if __name__ == '__main__':
    compare_success_vs_failure()
