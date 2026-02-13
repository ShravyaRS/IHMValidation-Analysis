#!/usr/bin/env python3
"""
Run CorMap validation using freesas (cormapy)
Uses pre-extracted exp/fit data files

FIX: Uses exact Decimal arithmetic for p-value computation
     to avoid floating-point precision loss in FreeSAS's LROH.probaLongerRun()
     on certain platforms (Python 3.13 / NumPy 2.4).
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from decimal import Decimal, getcontext
from freesas.cormap import gof

getcontext().prec = 100


def cormap_pvalue_exact(n, c_longest):
    """
    Compute CorMap p-value with exact arithmetic using Schilling (1990) recursion.
    Replaces FreeSAS LROH.probaLongerRun() which has float64 precision issues.
    """
    k = c_longest - 1
    if k > n:
        return 0.0
    if k <= 0:
        return 1.0
    f = [Decimal(0)] * (n + 1)
    for i in range(min(k, n + 1)):
        f[i] = Decimal(2) ** i
    for i in range(k, n + 1):
        f[i] = sum(f[i - j] for j in range(1, k + 1))
    p = Decimal(1) - f[n] / Decimal(2) ** n
    return float(p)


def run_cormap_freesas(pairs_file, output_file):
    with open(pairs_file, 'r') as f:
        pairs = json.load(f)
    print("=" * 80)
    print("RUNNING CORMAP USING FREESAS (with exact p-value fix)")
    print("=" * 80)
    print(f"Total pairs: {len(pairs)}")
    results = []
    success = 0
    failed = 0
    for i, pair in enumerate(pairs, 1):
        sasbdb_code = pair['sasbdb_code']
        fit_name = pair['fit_name']
        exp_file = pair['exp_file']
        fit_file = pair['fit_file']
        print(f"[{i}/{len(pairs)}] {fit_name}...", end='', flush=True)
        try:
            exp_data = np.loadtxt(exp_file)
            fit_data = np.loadtxt(fit_file)
            result = gof(exp_data, fit_data)
            p_exact = cormap_pvalue_exact(result.n, result.c)
            print(f" N={result.n}, C={result.c}, p={p_exact:.6f} (freesas={result.P:.6f})")
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': p_exact,
                'cormap_c_value': result.c,
                'n_points': result.n,
                'freesas_p_raw': result.P,
                'status': 'success'
            })
            success += 1
        except Exception as e:
            print(f" error: {str(e)[:60]}")
            results.append({
                'sasbdb_code': sasbdb_code,
                'fit_name': fit_name,
                'cormap_p_value': None,
                'cormap_c_value': None,
                'n_points': 0,
                'freesas_p_raw': None,
                'status': 'error'
            })
            failed += 1
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)
    print(f"Total pairs:     {len(pairs)}")
    print(f"Successful:      {success}")
    print(f"Failed:          {failed}")
    print(f"Results saved:   {output_file}")
    print("=" * 80)
    return df


if __name__ == "__main__":
    pairs_file = "validation_comparison/extracted_data/exp_fit_pairs.json"
    output_file = "validation_comparison/reports/cormap_freesas_results.csv"
    run_cormap_freesas(pairs_file, output_file)
