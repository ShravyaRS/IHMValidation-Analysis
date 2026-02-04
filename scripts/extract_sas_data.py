#!/usr/bin/env python3

import os
import sys
import re
from pathlib import Path

def extract_sas_from_sascif(sascif_path, output_dir):
    """
    Extract SAS data from .sascif file and save as .dat format
    """
    print(f"Processing: {sascif_path}")
    
    try:
        with open(sascif_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    # Find the data loop section
    in_data_section = False
    data_lines = []
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Look for data section markers
        if 'loop_' in line.lower():
            # Check next few lines for intensity data
            for j in range(i, min(i+20, len(lines))):
                if '_sas' in lines[j].lower() and 'intensity' in lines[j].lower():
                    in_data_section = True
                    break
        
        if in_data_section:
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Stop if we hit another loop or section
            if stripped.startswith('_') or stripped.startswith('loop_'):
                if data_lines:
                    break
                continue
            
            # Try to parse data line
            parts = stripped.split()
            if len(parts) >= 3:
                try:
                    q = float(parts[0])
                    intensity = float(parts[1])
                    error = float(parts[2])
                    data_lines.append(f"{q:15.8e} {intensity:15.8e} {error:15.8e}")
                except ValueError:
                    continue
    
    if not data_lines:
        print(f"Warning: No data extracted from {sascif_path.name}")
        return None
    
    # Save as .dat file
    basename = Path(sascif_path).stem
    output_path = Path(output_dir) / f"{basename}.dat"
    
    with open(output_path, 'w') as f:
        f.write("# q I(q) error\n")
        f.write('\n'.join(data_lines))
    
    print(f"Extracted {len(data_lines)} data points -> {output_path.name}")
    return output_path

if __name__ == "__main__":
    # CORRECTED PATHS
    input_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    output_dir = "validation_comparison/extracted_data"
    
    os.makedirs(output_dir, exist_ok=True)
    
    sascif_files = sorted(Path(input_dir).glob("SASD*.sascif"))
    
    print("="*80)
    print(f"SAS DATA EXTRACTION")
    print("="*80)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Found {len(sascif_files)} .sascif files\n")
    
    successful = 0
    failed = 0
    
    for sascif_file in sascif_files:
        output_path = extract_sas_from_sascif(sascif_file, output_dir)
        if output_path:
            successful += 1
        else:
            failed += 1
        print()
    
    print("="*80)
    print(f"Extraction Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(sascif_files)}")
    print("="*80)
