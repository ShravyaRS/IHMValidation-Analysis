#!/usr/bin/env python3
"""
Batch download all SASBDB entries from PDB-IHM
"""

import json
import requests
import time
from pathlib import Path

def download_sasbdb_batch():
    """Download all SASBDB entries"""
    
    # Load SASBDB codes
    with open('pdb_ihm_sas_entries.json', 'r') as f:
        data = json.load(f)
    
    codes = data['sasbdb_codes']
    total = len(codes)
    
    print("="*80)
    print(f"DOWNLOADING {total} SASBDB ENTRIES")
    print("="*80)
    
    output_dir = Path("/root/projects/IHMValidation-Analysis/Validation/cache")
    
    downloaded = 0
    exists = 0
    no_fits = 0
    failed = 0
    
    for i, code in enumerate(codes, 1):
        output_path = output_dir / f"{code}.sascif"
        
        # Skip if exists and has fits
        if output_path.exists():
            with open(output_path, 'r') as f:
                if '_FIT_' in f.read():
                    exists += 1
                    if i % 50 == 0:
                        print(f"[{i}/{total}] {code} - already exists with fits")
                    continue
        
        # Download
        url = f"https://www.sasbdb.org/media/sascif/sascif_files/{code}.sascif"
        
        try:
            print(f"[{i}/{total}] {code}...", end='', flush=True)
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                if '_FIT_' in content:
                    with open(output_path, 'w') as f:
                        f.write(content)
                    print(f" ✓ ({len(content)} bytes)")
                    downloaded += 1
                else:
                    print(f" ✗ (no fit data)")
                    no_fits += 1
            else:
                print(f" ✗ HTTP {response.status_code}")
                failed += 1
            
            # Rate limiting
            if downloaded % 10 == 0:
                time.sleep(2)
            else:
                time.sleep(0.5)
                
        except Exception as e:
            print(f" ✗ {str(e)[:30]}")
            failed += 1
    
    print(f"\n{'='*80}")
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"Downloaded with fits:  {downloaded}")
    print(f"Already had with fits: {exists}")
    print(f"Total with fits:       {downloaded + exists}")
    print(f"No fit data:           {no_fits}")
    print(f"Failed:                {failed}")
    print("="*80)

if __name__ == "__main__":
    download_sasbdb_batch()
