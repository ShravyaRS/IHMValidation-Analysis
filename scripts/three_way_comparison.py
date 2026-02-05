#!/usr/bin/env python3
"""
Three-way comparison: DATCMP vs CorMap (main) vs CorMap (alternative)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import time

# Import both implementations
import sys
sys.path.insert(0, str(Path(__file__).parent))
from cormap_implementation import cormap_pairwise
from cormap_alternative_implementation import cormap_alternative

def load_dat_file(filepath):
    data = np.loadtxt(filepath, comments='#')
    if data.shape[1] >= 3:
        return data[:, 0], data[:, 1], data[:, 2]
    elif data.shape[1] == 2:
        return data[:, 0], data[:, 1], np.ones_like(data[:, 0]) * 0.01
    raise ValueError(f"Invalid format: {filepath}")

if __name__ == "__main__":
    pairs_file = "validation_comparison/extracted_data/exp_fit_pairs.json"
    
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)
    
    print("="*80)
    print("THREE-WAY COMPARISON: DATCMP vs CorMap (Main) vs CorMap (Alt)")
    print("="*80)
    print(f"Analyzing {len(pairs)} pairs\n")
    
    results = []
    
    for i, pair in enumerate(pairs[:10], 1):  # Test on first 10
        print(f"[{i}/10] {pair['sasbdb_code']} - {pair['fit_name']}")
        
        exp_file = Path(pair['exp_file'])
        fit_file = Path(pair['fit_file'])
        
        try:
            exp_q, exp_I, exp_err = load_dat_file(exp_file)
            fit_q, fit_I, fit_err = load_dat_file(fit_file)
            
            # Main implementation
            result_main = cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)
            
            # Alternative implementation
            p_alt, c_alt, n_alt = cormap_alternative(exp_q, exp_I, exp_err, fit_q, fit_I)
            
            results.append({
                'sasbdb_code': pair['sasbdb_code'],
                'fit_name': pair['fit_name'],
                'cormap_main_p': result_main['p_value'],
                'cormap_main_c': result_main['c_value'],
                'cormap_alt_p': p_alt,
                'cormap_alt_c': c_alt,
                'n_points': n_alt
            })
            
            print(f"  Main:  p={result_main['p_value']:.6e}, C={result_main['c_value']}")
            print(f"  Alt:   p={p_alt:.6e}, C={c_alt}")
            
            if result_main['p_value'] and p_alt:
                diff = abs(result_main['p_value'] - p_alt)
                print(f"  Diff:  {diff:.6e}")
            print()
            
        except Exception as e:
            print(f"  Error: {e}\n")
    
    df = pd.DataFrame(results)
    output_file = "validation_comparison/reports/three_way_comparison.csv"
    df.to_csv(output_file, index=False)
    
    print("="*80)
    print(f"Results saved to: {output_file}")
    print("="*80)
    
    if len(df) > 0:
        both_valid = df['cormap_main_p'].notna() & df['cormap_alt_p'].notna()
        if both_valid.sum() > 0:
            df_valid = df[both_valid]
            diff = abs(df_valid['cormap_main_p'] - df_valid['cormap_alt_p'])
            print(f"\nMain vs Alternative CorMap:")
            print(f"  Mean difference: {diff.mean():.6e}")
            print(f"  Max difference:  {diff.max():.6e}")
            print(f"  Correlation:     {df_valid['cormap_main_p'].corr(df_valid['cormap_alt_p']):.6f}")
