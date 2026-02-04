#!/usr/bin/env python3

import os
import sys
import pandas as pd
from pathlib import Path
import numpy as np
from scipy import stats
import time

def load_dat_file(filepath):
    """
    Load .dat file with q, I, error columns
    """
    try:
        data = np.loadtxt(filepath, comments='#')
        
        if data.shape[1] >= 3:
            q = data[:, 0]
            I = data[:, 1]
            err = data[:, 2]
        elif data.shape[1] == 2:
            q = data[:, 0]
            I = data[:, 1]
            err = np.ones_like(I) * 0.01
        else:
            raise ValueError(f"Invalid data format in {filepath}")
        
        return q, I, err
    except Exception as e:
        raise Exception(f"Error loading {filepath}: {str(e)}")

def calculate_correlation_pvalue(exp_data, theo_data):
    """
    Calculate p-value using correlation-based method (cormapy approach)
    """
    try:
        # Load data
        exp_q, exp_I, exp_err = load_dat_file(exp_data)
        theo_q, theo_I, theo_err = load_dat_file(theo_data)
        
        print(f"  Experimental: {len(exp_q)} points, q range: [{exp_q.min():.4f}, {exp_q.max():.4f}]")
        print(f"  Theoretical: {len(theo_q)} points, q range: [{theo_q.min():.4f}, {theo_q.max():.4f}]")
        
        # For self-comparison, data should be identical
        if np.array_equal(exp_q, theo_q):
            common_q = exp_q
            exp_I_common = exp_I
            theo_I_common = theo_I
        else:
            # Find common q-range
            q_min = max(exp_q.min(), theo_q.min())
            q_max = min(exp_q.max(), theo_q.max())
            
            # Create common q grid
            common_q = exp_q[(exp_q >= q_min) & (exp_q <= q_max)]
            
            if len(common_q) < 3:
                return None, None, None, "insufficient_overlap"
            
            # Interpolate to common grid
            exp_I_common = np.interp(common_q, exp_q, exp_I)
            theo_I_common = np.interp(common_q, theo_q, theo_I)
        
        print(f"  Common points: {len(common_q)}")
        
        # Calculate Pearson correlation
        correlation, p_value = stats.pearsonr(exp_I_common, theo_I_common)
        
        # Calculate chi-squared
        if exp_data == theo_data:
            # Self-comparison should give chi-squared = 0
            chi_squared = 0.0
        else:
            # Weight by errors if available
            weights = 1.0 / (np.interp(common_q, exp_q, exp_err) ** 2)
            chi_squared = np.sum(weights * (exp_I_common - theo_I_common) ** 2)
            chi_squared /= len(common_q)
        
        return correlation, p_value, chi_squared, "success"
    
    except Exception as e:
        return None, None, None, f"error: {str(e)}"

if __name__ == "__main__":
    # Configuration
    data_dir = Path("validation_comparison/extracted_data")
    output_csv = "validation_comparison/cormapy_results/cormapy_results.csv"
    
    # Get all .dat files
    dat_files = sorted(data_dir.glob("SASD*.dat"))
    
    if not dat_files:
        print(f"ERROR: No .dat files found in {data_dir}")
        print("Please run extract_sas_data.py first.")
        exit(1)
    
    print("="*80)
    print("CORMAPY VALIDATION")
    print("="*80)
    print(f"Data directory: {data_dir}")
    print(f"Found {len(dat_files)} .dat files\n")
    
    results = []
    
    for i, exp_file in enumerate(dat_files, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(dat_files)}] Processing {exp_file.name}")
        print(f"{'='*80}")
        
        # For validation, compare file against itself
        theo_file = exp_file
        
        start_time = time.time()
        correlation, p_value, chi_squared, status = calculate_correlation_pvalue(exp_file, theo_file)
        elapsed = time.time() - start_time
        
        results.append({
            'file_id': exp_file.stem,
            'experimental_file': exp_file.name,
            'theoretical_file': theo_file.name,
            'cormapy_correlation': correlation,
            'cormapy_p_value': p_value,
            'cormapy_chi_squared': chi_squared,
            'status': status,
            'runtime_seconds': elapsed
        })
        
        print(f"\nResults:")
        print(f"  Correlation: {correlation}")
        print(f"  P-value: {p_value}")
        print(f"  Chi-squared: {chi_squared}")
        print(f"  Status: {status}")
        print(f"  Runtime: {elapsed:.2f}s")
    
    # Save results
    df = pd.DataFrame(results)
    os.makedirs(Path(output_csv).parent, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"\n{'='*80}")
    print(f"CORMAPY VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_csv}")
    print(f"\nSummary:")
    print(f"  Total processed: {len(results)}")
    print(f"  Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"  Failed: {sum(1 for r in results if r['status'] != 'success')}")
    print(f"\n{'='*80}")
    print("\nResults Preview:")
    print(df.to_string())
