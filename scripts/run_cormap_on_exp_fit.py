#!/usr/bin/env python3

import os
import sys
import pandas as pd
from pathlib import Path
import numpy as np
import time
import json

# Import our CorMap implementation
sys.path.insert(0, str(Path(__file__).parent))
from cormap_implementation import cormap_pairwise

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

if __name__ == "__main__":
    # Load exp-fit pairs
    pairs_file = "validation_comparison/extracted_data/exp_fit_pairs.json"
    output_csv = "validation_comparison/cormapy_results/cormap_exp_fit_results.csv"
    
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)
    
    print("="*80)
    print("CORMAP (Python) VALIDATION: Experimental vs Fitted Data")
    print("="*80)
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
        
        try:
            # Load data
            exp_q, exp_I, exp_err = load_dat_file(exp_file)
            fit_q, fit_I, fit_err = load_dat_file(fit_file)
            
            print(f"  Experimental: {len(exp_q)} points, q range: [{exp_q.min():.4f}, {exp_q.max():.4f}]")
            print(f"  Fitted: {len(fit_q)} points, q range: [{fit_q.min():.4f}, {fit_q.max():.4f}]")
            
            start_time = time.time()
            result = cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)
            elapsed = time.time() - start_time
            
            results.append({
                'sasbdb_code': pair['sasbdb_code'],
                'fit_name': pair['fit_name'],
                'exp_file': exp_file.name,
                'fit_file': fit_file.name,
                'original_p_value': pair['original_p_value'],
                'original_chi_square': pair['original_chi_square'],
                'cormap_c_value': result['c_value'],
                'cormap_p_value': result['p_value'],
                'cormap_n_points': result['n_points'],
                'status': result['status'],
                'runtime_seconds': elapsed
            })
            
            print(f"\nCorMap Results:")
            print(f"  C-value (longest run): {result['c_value']}")
            print(f"  P-value: {result['p_value']}")
            print(f"  N points: {result['n_points']}")
            print(f"  Status: {result['status']}")
            print(f"  Runtime: {elapsed:.2f}s")
            
            if pair['original_p_value'] is not None and result['p_value'] is not None:
                diff = abs(result['p_value'] - pair['original_p_value'])
                rel_diff = (diff / pair['original_p_value']) * 100 if pair['original_p_value'] != 0 else 0
                print(f"  Difference from original: {diff:.6f} ({rel_diff:.2f}%)")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'sasbdb_code': pair['sasbdb_code'],
                'fit_name': pair['fit_name'],
                'exp_file': exp_file.name,
                'fit_file': fit_file.name,
                'original_p_value': pair['original_p_value'],
                'original_chi_square': pair['original_chi_square'],
                'cormap_c_value': None,
                'cormap_p_value': None,
                'cormap_n_points': 0,
                'status': f'error: {str(e)}',
                'runtime_seconds': 0
            })
    
    df = pd.DataFrame(results)
    os.makedirs(Path(output_csv).parent, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"\n{'='*80}")
    print(f"CORMAP VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_csv}")
    print(f"\nResults Preview:")
    print(df.to_string())
