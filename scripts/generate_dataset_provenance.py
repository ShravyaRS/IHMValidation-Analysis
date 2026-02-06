#!/usr/bin/env python3
"""
Generate complete dataset provenance for reproducibility
"""

import json
from datetime import datetime
from pathlib import Path
import pandas as pd

def generate_provenance():
    # Load exp-fit pairs
    with open('validation_comparison/extracted_data/exp_fit_pairs.json', 'r') as f:
        pairs = json.load(f)
    
    # Load our SASBDB codes
    with open('validation_comparison/datasets_used.txt', 'r') as f:
        sasbdb_codes = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    provenance = []
    
    for pair in pairs:
        provenance.append({
            'pdb_ihm_id': 'N/A',  # Would need to query PDB-IHM
            'sasbdb_code': pair['sasbdb_code'],
            'fit_name': pair['fit_name'],
            'exp_file': pair['exp_file'],
            'fit_file': pair['fit_file'],
            'download_date': '2026-02-04',
            'source': 'https://www.sasbdb.org',
            'sascif_file': f"/root/projects/IHMValidation-Analysis/Validation/cache/{pair['sasbdb_code']}.sascif"
        })
    
    # Create DataFrame
    df = pd.DataFrame(provenance)
    
    # Save as CSV
    output_file = 'validation_comparison/datasets/used_entries.csv'
    Path(output_file).parent.mkdir(exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print("="*80)
    print("DATASET PROVENANCE GENERATED")
    print("="*80)
    print(f"\nTotal entries documented: {len(df)}")
    print(f"SASBDB codes: {df['sasbdb_code'].nunique()}")
    print(f"Download date: 2026-02-04")
    print(f"Source: https://www.sasbdb.org")
    print(f"\nSaved to: {output_file}")
    print("="*80)
    
    # Create metadata file
    metadata = {
        'validation_date': '2026-02-04',
        'total_pairs': len(df),
        'unique_sasbdb_codes': df['sasbdb_code'].nunique(),
        'source_database': 'SASBDB (https://www.sasbdb.org)',
        'file_format': '.sascif',
        'extraction_method': 'scripts/extract_exp_and_fit_data.py',
        'hardware': 'WSL Ubuntu 24.04, Intel i7, 16GB RAM',
        'python_version': '3.13.9',
        'numpy_version': '2.4.0',
        'scipy_version': '1.16.0'
    }
    
    with open('validation_comparison/datasets/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: validation_comparison/datasets/metadata.json")

if __name__ == "__main__":
    generate_provenance()
