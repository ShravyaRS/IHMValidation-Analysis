#!/usr/bin/env python3

import os
import sys
import pandas as pd
from pathlib import Path
import numpy as np
from scipy import stats
import time
import json

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

def calculate_correlation_pvalue(exp_file, fit_file):
    """
    Calculate p-value using correlation-based method (cormapy approach)
    """
    try:
        # Load data
        exp_q, exp_I, exp_err = load_dat_file(exp_file)
        fit_q, fit_I, fit_err = load_dat_file(fit_file)
        
        print(f"  Experimental: {len(exp_q)} points, q range: [{exp_q.min():.4f}, {exp_q.max():.4f}]")
        print(f"  Fitted: {len(fit_q)} points, q range: [{fit_q.min():.4f}, {fit_q.max():.4f}]")
        
        # Find common q-range
        q_min = max(exp_q.min(), fit_q.min())
        q_max = min(exp_q.max(), fit_q.max())
        
        # Filter to common range
        exp_mask = (exp_q >= q_min) & (exp_q <= q_max)
        fit_mask = (fit_q >= q_min) & (fit_q <= q_max)
        
        exp_q_common = exp_q[exp_mask]
        exp_I_common = exp_I[exp_mask]
        
        fit_q_common = fit_q[fit_mask]
        fit_I_common = fit_I[fit_mask]
        
        print(f"  Common q-range: [{q_min:.4f}, {q_max:.4f}]")
        print(f"  Experimental points in range: {len(exp_q_common)}")
        print(f"  Fitted points in range: {len(fit_q_common)}")
        
        # Check if we have enough overlap
        if len(exp_q_common) < 3 or len(fit_q_common) < 3:
            return None, None, None, "insufficient_overlap"
        
        # Interpolate fitted data to experimental q points
        fit_I_interp = np.interp(exp_q_common, fit_q_common, fit_I_common)
        
        print(f"  Interpolated to {len(exp_q_common)} common points")
        
        # Calculate Pearson correlation
        correlation, p_value = stats.pearsonr(exp_I_common, fit_I_interp)
        
        # Calculate chi-squared
        if len(exp_q_common) > 0:
            residuals = exp_I_common - fit_I_interp
            # Use experimental errors for weighting
            exp_err_common = exp_err[exp_mask]
            weights = 1.0 / (exp_err_common ** 2)
            chi_squared = np.sum(weights * (residuals ** 2)) / len(exp_q_common)
        else:
            chi_squared = None
        
        return correlation, p_value, chi_squared, "success"
    
    except Exception as e:
        return None, None, None, f"error: {str(e)}"

if __name__ == "__main__":
    # Load exp-fit pairs
    pairs_file = "validation_comparison/extracted_data/exp_fit_pairs.json"
    output_csv = "validation_comparison/cormapy_results/cormapy_exp_fit_results.csv"
    
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)
    
    print("="*80)
    print("CORMAPY VALIDATION: Experimental vs Fitted Data")
    print("="*80)
    print(f"Found {len(pairs)} exp-fit pairs\n")
    
    results = []
    
    for i, pair in enumerate(pairs, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(pairs)}] {pair['sasbdb_code']} - {pair['fit_name']}")
        print(f"{'='*80}")
        
        exp_file = Path(pair['exp_file'])
        fit_file = Path(pair['fit_file'])
        
        start_time = time.time()
        correlation, p_value, chi_squared, status = calculate_correlation_pvalue(exp_file, fit_file)
        elapsed = time.time() - start_time
        
        results.append({
            'sasbdb_code': pair['sasbdb_code'],
            'fit_name': pair['fit_name'],
            'exp_file': exp_file.name,
            'fit_file': fit_file.name,
            'original_p_value': pair['original_p_value'],
            'original_chi_square': pair['original_chi_square'],
            'cormapy_correlation': correlation,
            'cormapy_p_value': p_value,
            'cormapy_chi_squared': chi_squared,
            'status': status,
            'runtime_seconds': elapsed
        })
        
        print(f"\nCormapy Results:")
        print(f"  Correlation: {correlation}")
        print(f"  P-value: {p_value}")
        print(f"  Chi-squared: {chi_squared}")
        print(f"  Status: {status}")
        print(f"  Runtime: {elapsed:.2f}s")
        
        if pair['original_p_value'] is not None and p_value is not None:
            diff = abs(p_value - pair['original_p_value'])
            print(f"  Difference from original: {diff:.6f}")
    
    df = pd.DataFrame(results)
    os.makedirs(Path(output_csv).parent, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"\n{'='*80}")
    print(f"CORMAPY VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_csv}")
    print(f"\nResults Preview:")
    print(df.to_string())
