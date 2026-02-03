#!/usr/bin/env python3

import os
import subprocess
import pandas as pd
from pathlib import Path
import re
import time
import json

def run_datcmp(exp_file, fit_file, singularity_container):
    """
    Run DATCMP on experimental vs fitted data
    """
    cmd = [
        "singularity", "exec",
        singularity_container,
        "datcmp",
        str(exp_file),
        str(fit_file)
    ]
    
    print(f"Running: datcmp {exp_file.name} {fit_file.name}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        
        # Parse DATCMP output
        c_value = None
        p_value = None
        adj_p_value = None
        
        # Use regex to find the line with numeric values
        pattern = r'(\d+)\s+vs\.\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
        
        for line in output.split('\n'):
            match = re.search(pattern, line)
            if match:
                c_value = float(match.group(3))
                p_value = float(match.group(4))
                adj_p_value = float(match.group(5).rstrip('*'))
                break
        
        return {
            'p_value': p_value,
            'c_value': c_value,
            'adj_p_value': adj_p_value,
            'status': 'success',
            'output': output
        }
    
    except subprocess.TimeoutExpired:
        return {
            'p_value': None,
            'c_value': None,
            'adj_p_value': None,
            'status': 'timeout',
            'output': 'Process timed out'
        }
    except Exception as e:
        return {
            'p_value': None,
            'c_value': None,
            'adj_p_value': None,
            'status': 'error',
            'output': str(e)
        }

if __name__ == "__main__":
    # Load exp-fit pairs
    pairs_file = "validation_comparison/extracted_data/exp_fit_pairs.json"
    container = "ihmvalidation_complete.sif"
    output_csv = "validation_comparison/datcmp_results/datcmp_exp_fit_results.csv"
    
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)
    
    print("="*80)
    print("DATCMP VALIDATION: Experimental vs Fitted Data")
    print("="*80)
    print(f"Container: {container}")
    print(f"Found {len(pairs)} exp-fit pairs\n")
    
    results = []
    
    for i, pair in enumerate(pairs, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(pairs)}] {pair['sasbdb_code']} - {pair['fit_name']}")
        print(f"{'='*80}")
        print(f"Experimental: {Path(pair['exp_file']).name}")
        print(f"Fitted: {Path(pair['fit_file']).name}")
        print(f"Original p-value: {pair['original_p_value']}")
        print(f"Original chi-square: {pair['original_chi_square']}")
        
        exp_file = Path(pair['exp_file'])
        fit_file = Path(pair['fit_file'])
        
        start_time = time.time()
        result = run_datcmp(exp_file, fit_file, container)
        elapsed = time.time() - start_time
        
        results.append({
            'sasbdb_code': pair['sasbdb_code'],
            'fit_name': pair['fit_name'],
            'exp_file': exp_file.name,
            'fit_file': fit_file.name,
            'original_p_value': pair['original_p_value'],
            'original_chi_square': pair['original_chi_square'],
            'datcmp_c_value': result['c_value'],
            'datcmp_p_value': result['p_value'],
            'datcmp_adj_p_value': result['adj_p_value'],
            'status': result['status'],
            'runtime_seconds': elapsed
        })
        
        print(f"\nDATCMP Results:")
        print(f"  C-value: {result['c_value']}")
        print(f"  Pr(>C): {result['p_value']}")
        print(f"  Adj Pr(>C): {result['adj_p_value']}")
        print(f"  Status: {result['status']}")
        print(f"  Runtime: {elapsed:.2f}s")
        
        if pair['original_p_value'] is not None:
            diff = abs(result['p_value'] - pair['original_p_value']) if result['p_value'] else None
            print(f"  Difference from original: {diff}")
    
    df = pd.DataFrame(results)
    os.makedirs(Path(output_csv).parent, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"\n{'='*80}")
    print(f"DATCMP VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_csv}")
    print(f"\nResults Preview:")
    print(df.to_string())
