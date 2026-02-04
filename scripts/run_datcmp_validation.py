#!/usr/bin/env python3

import os
import subprocess
import pandas as pd
from pathlib import Path
import re
import time

def run_datcmp(exp_file, theo_file, singularity_container):
    """
    Run DATCMP on experimental and theoretical data
    """
    cmd = [
        "singularity", "exec",
        singularity_container,
        "datcmp",
        str(exp_file),
        str(theo_file)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        
        print(f"DATCMP output:\n{output}\n")
        
        # Parse DATCMP output using regex
        # Looking for pattern like: "1 vs.    2                                 380.000000     0.000000     0.000000*"
        c_value = None
        p_value = None
        adj_p_value = None
        
        # Use regex to find the line with "vs." followed by three numbers
        pattern = r'(\d+)\s+vs\.\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
        
        for line in output.split('\n'):
            match = re.search(pattern, line)
            if match:
                # Groups: 1=first_num, 2=second_num, 3=C_value, 4=Pr(>C), 5=adj_Pr(>C)
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
            'output': 'Process timed out after 120 seconds'
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
    # Configuration
    data_dir = Path("validation_comparison/extracted_data")
    container = "ihmvalidation_complete.sif"
    output_csv = "validation_comparison/datcmp_results/datcmp_results.csv"
    
    if not Path(container).exists():
        print(f"ERROR: Container not found at {container}")
        exit(1)
    
    dat_files = sorted(data_dir.glob("SASD*.dat"))
    
    if not dat_files:
        print(f"ERROR: No .dat files found in {data_dir}")
        exit(1)
    
    print("="*80)
    print("DATCMP VALIDATION")
    print("="*80)
    print(f"Container: {container}")
    print(f"Data directory: {data_dir}")
    print(f"Found {len(dat_files)} .dat files\n")
    
    results = []
    
    for i, exp_file in enumerate(dat_files, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(dat_files)}] Processing {exp_file.name}")
        print(f"{'='*80}")
        
        theo_file = exp_file
        
        start_time = time.time()
        result = run_datcmp(exp_file, theo_file, container)
        elapsed = time.time() - start_time
        
        results.append({
            'file_id': exp_file.stem,
            'experimental_file': exp_file.name,
            'theoretical_file': theo_file.name,
            'datcmp_c_value': result['c_value'],
            'datcmp_p_value': result['p_value'],
            'datcmp_adj_p_value': result['adj_p_value'],
            'status': result['status'],
            'runtime_seconds': elapsed
        })
        
        print(f"\nParsed Results:")
        print(f"  C-value: {result['c_value']}")
        print(f"  Pr(>C): {result['p_value']}")
        print(f"  Adj Pr(>C): {result['adj_p_value']}")
        print(f"  Status: {result['status']}")
        print(f"  Runtime: {elapsed:.2f}s")
    
    df = pd.DataFrame(results)
    os.makedirs(Path(output_csv).parent, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"\n{'='*80}")
    print(f"DATCMP VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_csv}")
    print(f"\nSummary:")
    print(f"  Total processed: {len(results)}")
    print(f"  Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"  Failed: {sum(1 for r in results if r['status'] != 'success')}")
    print(f"\n{'='*80}")
    print("\nResults Preview:")
    print(df.to_string())
