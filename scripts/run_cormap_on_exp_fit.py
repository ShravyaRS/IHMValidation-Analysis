#!/usr/bin/env python3
"""
Run CorMap validation using freesas (cormapy)
Uses pre-extracted exp/fit data files
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from freesas.cormap import gof


def run_cormap_freesas(pairs_file, output_file):
    """
    Run freesas cormap on all exp-fit pairs
    """
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)

    print("="*80)
    print("RUNNING CORMAP USING FREESAS")
    print("="*80)
    print(f"Total pairs: {len(pairs)}")

    results = []
    success = 0
    failed  = 0

    for i, pair in enumerate(pairs, 1):
        sasbdb_code = pair['sasbdb_code']
        fit_name    = pair['fit_name']
        exp_file    = pair['exp_file']
        fit_file    = pair['fit_file']

        print(f"[{i}/{len(pairs)}] {fit_name}...", end='', flush=True)

        try:
            # Load pre-extracted data
            exp_data = np.loadtxt(exp_file)
            fit_data = np.loadtxt(fit_file)

            # Run freesas cormap
            result = gof(exp_data, fit_data)

            print(f" N={result.n}, C={result.c}, p={result.P:.6f}")
            
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': result.P,
                'cormap_c_value': result.c,
                'n_points': result.n,
                'status': 'success'
            })
            success += 1

        except Exception as e:
            print(f" error: {str(e)[:40]}")
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': None,
                'cormap_c_value': None,
                'n_points': 0,
                'status': f'error'
            })
            failed += 1

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

    print(f"\n{'='*80}")
    print("SUMMARY")
    print("="*80)
    print(f"Total pairs:     {len(pairs)}")
    print(f"Successful:      {success}")
    print(f"Failed:          {failed}")
    print(f"Results saved:   {output_file}")
    print("="*80)

    return df


if __name__ == "__main__":
    pairs_file  = "validation_comparison/extracted_data/exp_fit_pairs.json"
    output_file = "validation_comparison/reports/cormap_freesas_results.csv"

    run_cormap_freesas(pairs_file, output_file)
