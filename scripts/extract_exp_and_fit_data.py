#!/usr/bin/env python3
"""
Extract experimental and fitted data from SASBDB .sascif files
Following professor's specification: use _sas_model_fitting block exactly as-is
Filter: q > 0 only (keep I_exp=0 rows)
Sigma: uniform (=1) since not present in _sas_model_fitting block
"""

import os
import json
import numpy as np
from pathlib import Path

CACHE_DIR = "/root/projects/IHMValidation-Analysis/Validation/cache"
OUTPUT_DIR = "validation_comparison/extracted_data"

def extract_fit_pair(sascif_file, fit_id):
    """
    Extract exp-fit pair from _sas_model_fitting block
    
    Columns in _sas_model_fitting:
      0: id (fit_id)
      1: ordinal
      2: momentum_transfer (q)
      3: intensity (I_exp on fit grid)
      4: fit (I_fit)
    
    Filter: q > 0 only (as per professor's approach)
    Sigma: uniform (=1) - not present in _sas_model_fitting
    """
    with open(sascif_file) as f:
        lines = f.readlines()
    
    fit_block = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == str(fit_id):
            try:
                q     = float(parts[2])  # momentum_transfer
                I_exp = float(parts[3])  # intensity (experimental)
                I_fit = float(parts[4])  # fit (model)
                if q > 0:  # Only filter on q > 0
                    fit_block.append([q, I_exp, I_fit])
            except:
                pass
    
    if len(fit_block) < 3:
        return None, None
    
    # Create arrays with uniform sigma=1
    exp_data = []
    fit_data = []
    
    for row in fit_block:
        q_val, I_exp, I_fit = row
        exp_data.append([q_val, I_exp, 1.0])  # sigma=1
        fit_data.append([q_val, I_fit, 1.0])  # sigma=1
    
    return np.array(exp_data), np.array(fit_data)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("="*80)
    print("EXTRACTING EXP-FIT PAIRS FROM SASCIF FILES")
    print("="*80)
    print(f"Cache directory: {CACHE_DIR}")
    print(f"Using _sas_model_fitting block (professor's specification)")
    print(f"Columns: [id, ordinal, q, I_exp, I_fit]")
    print(f"Filter: q > 0 only (keep I_exp=0 rows)")
    print(f"Sigma: uniform (=1)")
    print()
    
    sascif_files = sorted(Path(CACHE_DIR).glob("*.sascif"))
    print(f"Files found: {len(sascif_files)}")
    
    pairs_metadata = []
    total_extracted = 0
    no_fit_data = 0
    
    for sascif_file in sascif_files:
        sasbdb_code = sascif_file.stem
        
        # Find all fit IDs
        with open(sascif_file) as f:
            lines = f.readlines()
        
        fit_ids = set()
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                try:
                    fid = int(parts[0])
                    float(parts[2])
                    float(parts[3])
                    float(parts[4])
                    if fid > 50:
                        fit_ids.add(fid)
                except:
                    pass
        
        if not fit_ids:
            no_fit_data += 1
            continue
        
        fits_extracted = 0
        for fit_id in sorted(fit_ids):
            exp_pair, fit_pair = extract_fit_pair(sascif_file, fit_id)
            
            if exp_pair is None:
                continue
            
            # Save files
            fit_name = f"{sasbdb_code}_FIT_{fit_id}"
            exp_file = f"{OUTPUT_DIR}/{fit_name}_exp.dat"
            fit_file = f"{OUTPUT_DIR}/{fit_name}_fit.dat"
            
            np.savetxt(exp_file, exp_pair, fmt='%.6e')
            np.savetxt(fit_file, fit_pair, fmt='%.6e')
            
            pairs_metadata.append({
                'sasbdb_code': sasbdb_code,
                'fit_id': fit_id,
                'fit_name': fit_name,
                'exp_file': exp_file,
                'fit_file': fit_file,
                'n_points': len(exp_pair)
            })
            
            fits_extracted += 1
            total_extracted += 1
        
        if fits_extracted > 0:
            print(f"  {sasbdb_code}: {fits_extracted} fit(s) extracted")
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files processed: {len(sascif_files)}")
    print(f"Pairs extracted: {total_extracted}")
    print(f"No fit data:     {no_fit_data}")
    
    # Save metadata
    with open(f"{OUTPUT_DIR}/exp_fit_pairs.json", 'w') as f:
        json.dump(pairs_metadata, f, indent=2)
    
    print(f"Metadata saved:  {OUTPUT_DIR}/exp_fit_pairs.json")
    print("="*80)


if __name__ == "__main__":
    main()
