#!/usr/bin/env python3
"""
Run CorMap validation using freesas (cormapy)
Replaces custom p-value implementation with freesas.cormap.gof
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from freesas.cormap import gof

def extract_exp_fit_from_sascif(sascif_file, fit_id):
    """
    Extract experimental and fitted data from .sascif file
    Uses FIT block q-grid directly to avoid interpolation artifacts
    """
    with open(sascif_file, 'r') as f:
        lines = f.readlines()

    # Extract fit block
    fit_block = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == str(fit_id):
            try:
                q     = float(parts[2])
                I_exp = float(parts[3])
                I_fit = float(parts[4])
                fit_block.append([q, I_exp, I_fit])
            except:
                pass

    if not fit_block:
        return None, None

    # Filter out padding points (I_exp = 0)
    valid_rows = [[q, I_exp, I_fit]
                  for q, I_exp, I_fit in fit_block
                  if I_exp != 0.0]

    if not valid_rows:
        return None, None

    valid_data = np.array(valid_rows)

    # Get experimental errors from scan block
    # Find scan_id associated with this entry
    exp_block = []
    for line in lines:
        parts = line.split()
        if len(parts) == 5 and parts[-1].isdigit():
            try:
                q     = float(parts[1])
                I     = float(parts[2])
                sigma = float(parts[3])
                if sigma > 0:
                    exp_block.append([q, I, sigma])
            except:
                pass

    if not exp_block:
        return None, None

    exp_array = np.array(exp_block)

    # Match q-values to get sigma
    matched_exp = []
    matched_fit = []

    for row in valid_rows:
        q_target = row[0]
        I_exp    = row[1]
        I_fit    = row[2]

        idx   = np.argmin(np.abs(exp_array[:, 0] - q_target))
        sigma = exp_array[idx, 2]

        if sigma > 0:
            matched_exp.append([q_target, I_exp, sigma])
            matched_fit.append([q_target, I_fit, sigma])

    if len(matched_exp) < 3:
        return None, None

    return np.array(matched_exp), np.array(matched_fit)


def run_cormap_freesas(pairs_file, cache_dir, output_file):
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
        sascif_file = Path(cache_dir) / f"{sasbdb_code}.sascif"

        # Extract fit_id from fit_name (e.g. SASDBD9_FIT_728 -> 728)
        try:
            fit_id = int(fit_name.split('_FIT_')[1])
        except:
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': None,
                'cormap_c_value': None,
                'n_points': 0,
                'status': 'parse_error'
            })
            failed += 1
            continue

        print(f"[{i}/{len(pairs)}] {sasbdb_code} FIT_{fit_id}...", end='', flush=True)

        # Extract data
        exp_data, fit_data = extract_exp_fit_from_sascif(sascif_file, fit_id)

        if exp_data is None or fit_data is None:
            print(" insufficient_data")
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': None,
                'cormap_c_value': None,
                'n_points': 0,
                'status': 'insufficient_data'
            })
            failed += 1
            continue

        # Run freesas cormap
        try:
            result = gof(exp_data, fit_data)

            print(f" C={result.c}, p={result.P:.6f}")
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
    cache_dir   = "/root/projects/IHMValidation-Analysis/Validation/cache"
    output_file = "validation_comparison/reports/cormap_freesas_results.csv"

    run_cormap_freesas(pairs_file, cache_dir, output_file)
