#!/usr/bin/env python3
"""
Extract experimental and fitted SAS profiles from SASBDB .sascif files

Pipeline Step 1 of 4
Input:  .sascif files in cache directory
Output: exp_fit_pairs.json (metadata for all pairs)

Extraction logic:
- Uses FIT block directly (contains both exp and fit on same q-grid)
- Filters only points where q > 0 (removes q=0 padding point)
- Matches experimental errors from scan block by nearest q-value
"""

import numpy as np
import json
from pathlib import Path

CACHE_DIR   = "/root/projects/IHMValidation-Analysis/Validation/cache"
OUTPUT_DIR  = "validation_comparison/extracted_data"
OUTPUT_JSON = f"{OUTPUT_DIR}/exp_fit_pairs.json"

def parse_sascif(sascif_file):
    """
    Parse a .sascif file and return all fit blocks found.

    Returns list of dicts:
        fit_id    : int
        exp_data  : np.array (q, I_exp, sigma)
        fit_data  : np.array (q, I_fit, sigma)
        n_points  : int
    """
    with open(sascif_file, 'r') as f:
        lines = f.readlines()

    # Extract experimental scan block (has 5 columns, last is scan_id)
    # Format: point_id  q  I  sigma  scan_id
    exp_block = []
    for line in lines:
        parts = line.split()
        if len(parts) == 5 and parts[-1].isdigit():
            try:
                q     = float(parts[1])
                I     = float(parts[2])
                sigma = float(parts[3])
                if q > 0 and sigma > 0:
                    exp_block.append([q, I, sigma])
            except:
                pass

    if not exp_block:
        return []

    exp_array = np.array(exp_block)

    # Find all fit IDs in the file
    fit_ids = set()
    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            try:
                fit_id = int(parts[0])
                q      = float(parts[2])
                I_exp  = float(parts[3])
                I_fit  = float(parts[4])
                if fit_id > 100:  # fit IDs are typically large numbers
                    fit_ids.add(fit_id)
            except:
                pass

    results = []

    for fit_id in sorted(fit_ids):
        # Extract fit block
        # Format: fit_id  point_id  q  I_exp  I_fit
        fit_rows = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 5 and parts[0] == str(fit_id):
                try:
                    q     = float(parts[2])
                    I_exp = float(parts[3])
                    I_fit = float(parts[4])
                    # Filter: q > 0 only (removes q=0 padding)
                    if q > 0:
                        fit_rows.append([q, I_exp, I_fit])
                except:
                    pass

        if len(fit_rows) < 3:
            continue

        fit_array = np.array(fit_rows)

        # Match sigma from experimental block by nearest q-value
        matched_exp = []
        matched_fit = []

        for row in fit_rows:
            q_target = row[0]
            I_exp    = row[1]
            I_fit    = row[2]

            idx   = np.argmin(np.abs(exp_array[:, 0] - q_target))
            sigma = exp_array[idx, 2]

            if sigma > 0:
                matched_exp.append([q_target, I_exp,  sigma])
                matched_fit.append([q_target, I_fit, sigma])

        if len(matched_exp) < 3:
            continue

        results.append({
            'fit_id':   fit_id,
            'exp_data': np.array(matched_exp),
            'fit_data': np.array(matched_fit),
            'n_points': len(matched_exp)
        })

    return results


def run_extraction():
    """Extract all exp-fit pairs from cache directory"""

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    sascif_files = sorted(Path(CACHE_DIR).glob("*.sascif"))

    print("="*80)
    print("EXTRACTING EXP-FIT PAIRS FROM SASCIF FILES")
    print("="*80)
    print(f"Cache directory: {CACHE_DIR}")
    print(f"Files found: {len(sascif_files)}")

    pairs    = []
    success  = 0
    no_fits  = 0

    for sascif_file in sascif_files:
        sasbdb_code = sascif_file.stem
        fits = parse_sascif(sascif_file)

        if not fits:
            no_fits += 1
            continue

        for fit in fits:
            fit_name = f"{sasbdb_code}_FIT_{fit['fit_id']}"

            # Save data files
            exp_file = f"{OUTPUT_DIR}/{fit_name}_exp.dat"
            fit_file = f"{OUTPUT_DIR}/{fit_name}_fit.dat"

            np.savetxt(exp_file, fit['exp_data'], fmt='%.6e',
                       header='q I sigma')
            np.savetxt(fit_file, fit['fit_data'], fmt='%.6e',
                       header='q I_fit sigma')

            pairs.append({
                'sasbdb_code': sasbdb_code,
                'fit_name':    fit_name,
                'fit_id':      fit['fit_id'],
                'n_points':    fit['n_points'],
                'exp_file':    exp_file,
                'fit_file':    fit_file
            })
            success += 1

        print(f"  {sasbdb_code}: {len(fits)} fit(s) extracted")

    # Save metadata
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(pairs, f, indent=2)

    print(f"\n{'='*80}")
    print("SUMMARY")
    print("="*80)
    print(f"Files processed:    {len(sascif_files)}")
    print(f"Pairs extracted:    {success}")
    print(f"No fit data:        {no_fits}")
    print(f"Metadata saved:     {OUTPUT_JSON}")
    print("="*80)

    return pairs


if __name__ == "__main__":
    run_extraction()
