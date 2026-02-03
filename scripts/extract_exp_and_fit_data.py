#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import re

def extract_sas_data_from_sascif(sascif_path, output_dir):
    """
    Extract experimental and fitted SAS data from .sascif file
    Returns paths to experimental and fitted .dat files
    """
    print(f"\n{'='*80}")
    print(f"Processing: {sascif_path}")
    print(f"{'='*80}")
    
    with open(sascif_path, 'r') as f:
        content = f.read()
    
    basename = Path(sascif_path).stem
    
    # Extract experimental data from _sas_scan_intensity
    exp_data = []
    in_exp_section = False
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '_sas_scan_intensity.scan_id' in line:
            in_exp_section = True
            continue
        
        if in_exp_section:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            if stripped.startswith('_') or stripped.startswith('loop_') or stripped.startswith('data_'):
                break
            
            parts = stripped.split()
            if len(parts) >= 5:
                try:
                    q = float(parts[1])
                    intensity = float(parts[2])
                    error = float(parts[3])
                    exp_data.append(f"{q:15.8e} {intensity:15.8e} {error:15.8e}")
                except (ValueError, IndexError):
                    continue
    
    # Extract fitted data and p-value from _sas_model_fitting
    fit_blocks = {}
    current_fit_id = None
    
    for i, line in enumerate(lines):
        # Find fit blocks
        if line.startswith('data_') and '_FIT_' in line:
            current_fit_id = line.strip().replace('data_', '')
            fit_blocks[current_fit_id] = {
                'p_value': None,
                'chi_square': None,
                'data': []
            }
        
        # Extract p-value and chi-square
        if current_fit_id and '_sas_model_fitting_details.p_value' in line:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    p_val = float(parts[1]) if parts[1] != '.' else None
                    fit_blocks[current_fit_id]['p_value'] = p_val
                except ValueError:
                    pass
        
        if current_fit_id and '_sas_model_fitting_details.chi_square' in line:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    chi_sq = float(parts[1]) if parts[1] != '.' else None
                    fit_blocks[current_fit_id]['chi_square'] = chi_sq
                except ValueError:
                    pass
    
    # Extract fitted intensity data
    in_fit_section = False
    current_fit_data_id = None
    
    for i, line in enumerate(lines):
        if '_sas_model_fitting.fit' in line:
            in_fit_section = True
            continue
        
        if in_fit_section:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            if stripped.startswith('_') or stripped.startswith('loop_') or stripped.startswith('data_'):
                in_fit_section = False
                current_fit_data_id = None
                continue
            
            parts = stripped.split()
            if len(parts) >= 4:
                try:
                    fit_id = int(parts[0])
                    q = float(parts[2])
                    i_exp = float(parts[3])
                    i_fit = float(parts[4])
                    
                    # Find which fit block this belongs to
                    for fit_name, fit_info in fit_blocks.items():
                        if str(fit_id) in fit_name:
                            # Use fitted intensity with same error as experimental
                            # (or estimate error as 1% of fitted intensity)
                            error = i_fit * 0.01
                            fit_info['data'].append(f"{q:15.8e} {i_fit:15.8e} {error:15.8e}")
                            break
                except (ValueError, IndexError):
                    continue
    
    # Save experimental data
    exp_file = Path(output_dir) / f"{basename}_exp.dat"
    if exp_data:
        with open(exp_file, 'w') as f:
            f.write("# q I(q) error - Experimental data\n")
            f.write('\n'.join(exp_data))
        print(f"✓ Experimental data: {len(exp_data)} points → {exp_file.name}")
    else:
        print(f"✗ No experimental data found")
        exp_file = None
    
    # Save fitted data (use first fit with valid data)
    fit_files = []
    for fit_name, fit_info in fit_blocks.items():
        if fit_info['data']:
            fit_file = Path(output_dir) / f"{basename}_fit_{fit_name.split('_')[-1]}.dat"
            with open(fit_file, 'w') as f:
                f.write(f"# q I(q) error - Fitted data from {fit_name}\n")
                f.write(f"# Original p-value: {fit_info['p_value']}\n")
                f.write(f"# Original chi-square: {fit_info['chi_square']}\n")
                f.write('\n'.join(fit_info['data']))
            
            fit_files.append({
                'file': fit_file,
                'fit_name': fit_name,
                'p_value': fit_info['p_value'],
                'chi_square': fit_info['chi_square'],
                'n_points': len(fit_info['data'])
            })
            print(f"✓ Fitted data {fit_name}: {len(fit_info['data'])} points → {fit_file.name}")
            print(f"  Original p-value: {fit_info['p_value']}")
            print(f"  Original chi-square: {fit_info['chi_square']}")
    
    if not fit_files:
        print(f"✗ No fitted data found")
    
    return exp_file, fit_files

if __name__ == "__main__":
    input_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    output_dir = "validation_comparison/extracted_data"
    
    os.makedirs(output_dir, exist_ok=True)
    
    sascif_files = sorted(Path(input_dir).glob("SASD*.sascif"))
    
    print("="*80)
    print(f"SAS DATA EXTRACTION (Experimental + Fitted)")
    print("="*80)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Found {len(sascif_files)} .sascif files")
    
    all_pairs = []
    
    for sascif_file in sascif_files:
        exp_file, fit_files = extract_sas_data_from_sascif(sascif_file, output_dir)
        
        if exp_file and fit_files:
            for fit_info in fit_files:
                all_pairs.append({
                    'sasbdb_code': sascif_file.stem,
                    'exp_file': exp_file,
                    'fit_file': fit_info['file'],
                    'fit_name': fit_info['fit_name'],
                    'original_p_value': fit_info['p_value'],
                    'original_chi_square': fit_info['chi_square']
                })
    
    print(f"\n{'='*80}")
    print(f"Extraction Summary:")
    print(f"  Total SASBDB entries: {len(sascif_files)}")
    print(f"  Total exp-fit pairs: {len(all_pairs)}")
    print(f"{'='*80}")
    
    # Save pairs info
    import json
    pairs_file = Path(output_dir) / "exp_fit_pairs.json"
    with open(pairs_file, 'w') as f:
        json.dump([{
            'sasbdb_code': p['sasbdb_code'],
            'exp_file': str(p['exp_file']),
            'fit_file': str(p['fit_file']),
            'fit_name': p['fit_name'],
            'original_p_value': p['original_p_value'],
            'original_chi_square': p['original_chi_square']
        } for p in all_pairs], f, indent=2)
    
    print(f"\nPairs info saved to: {pairs_file}")
