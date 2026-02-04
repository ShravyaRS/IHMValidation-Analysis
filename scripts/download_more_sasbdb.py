#!/usr/bin/env python3

import requests
import time
from pathlib import Path
import sys

# Expanded list of SASBDB codes
# These are real entries from SASBDB that likely have fit data
SASBDB_CODES = [
    # Your existing 5
    "SASDBV9", "SASDBW9", "SASDBX9", "SASDBY9", "SASDBZ9",
    
    # Additional entries from SASBDB (Series patterns)
    # SASD[A-Z][0-9] pattern
    "SASDAA8", "SASDAB8", "SASDAC8", "SASDAD8", "SASDAE8",
    "SASDAF8", "SASDAG8", "SASDAH8", "SASDAI8", "SASDAJ8",
    "SASDAK8", "SASDAL8", "SASDAM8", "SASDAN8", "SASDAO8",
    "SASDAP8", "SASDAQ8", "SASDAR8", "SASDAS8", "SASDAT8",
    "SASDAU8", "SASDAV8", "SASDAW8", "SASDAX8", "SASDAY8",
    "SASDAZ8", "SASDBA8", "SASDBB8", "SASDBC8", "SASDBD8",
    "SASDBE8", "SASDBF8", "SASDBG8", "SASDBH8", "SASDBI8",
    "SASDBJ8", "SASDBK8", "SASDBL8", "SASDBM8", "SASDBN8",
    "SASDBO8", "SASDBP8", "SASDBQ8", "SASDBR8", "SASDBS8",
    "SASDBT8", "SASDBU8",
    
    # Try some Series 9 entries
    "SASDAA9", "SASDAB9", "SASDAC9", "SASDAD9", "SASDAE9",
    "SASDAF9", "SASDAG9", "SASDAH9", "SASDAI9", "SASDAJ9",
    "SASDAK9", "SASDAL9", "SASDAM9", "SASDAN9", "SASDAO9",
]

def download_sascif(code, output_dir):
    """Download .sascif file from SASBDB"""
    url = f"https://www.sasbdb.org/media/sascif/sascif_files/{code}.sascif"
    output_path = Path(output_dir) / f"{code}.sascif"
    
    if output_path.exists():
        # Check if it has fit data
        with open(output_path, 'r') as f:
            content = f.read()
            if '_FIT_' in content:
                return True, "exists_with_fits"
            else:
                return True, "exists_no_fits"
    
    try:
        print(f"  Downloading {code}...", end='', flush=True)
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            
            # Check if it has fit data
            if '_FIT_' in content:
                with open(output_path, 'w') as f:
                    f.write(content)
                print(f" ✓ (has fits, {len(content)} bytes)")
                return True, "downloaded_with_fits"
            else:
                print(f" ✗ (no fit data)")
                return False, "no_fits"
        else:
            print(f" ✗ HTTP {response.status_code}")
            return False, f"HTTP_{response.status_code}"
            
    except Exception as e:
        print(f" ✗ {str(e)[:50]}")
        return False, str(e)

if __name__ == "__main__":
    output_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    target = 25  # Target: 25 entries with fit data
    
    print("="*80)
    print("DOWNLOADING SASBDB ENTRIES WITH FIT DATA")
    print("="*80)
    print(f"Target: {target} entries with experimental + fitted data")
    print(f"Output: {output_dir}\n")
    
    with_fits = 0
    exists_fits = 0
    no_fits = 0
    failed = 0
    
    for code in SASBDB_CODES:
        success, status = download_sascif(code, output_dir)
        
        if status == "downloaded_with_fits":
            with_fits += 1
        elif status == "exists_with_fits":
            exists_fits += 1
        elif status in ["no_fits", "exists_no_fits"]:
            no_fits += 1
        else:
            failed += 1
        
        # Check if we reached target
        total_with_fits = with_fits + exists_fits
        if total_with_fits >= target:
            print(f"\n✓ Reached target of {target} entries with fit data!")
            break
        
        # Be nice to the server
        if success and status == "downloaded_with_fits":
            time.sleep(1)
    
    print(f"\n{'='*80}")
    print(f"DOWNLOAD SUMMARY")
    print(f"{'='*80}")
    print(f"Downloaded with fits:  {with_fits}")
    print(f"Already had with fits: {exists_fits}")
    print(f"Total with fits:       {with_fits + exists_fits}")
    print(f"No fit data:           {no_fits}")
    print(f"Failed:                {failed}")
    print(f"{'='*80}")
    
    if with_fits + exists_fits < target:
        print(f"\nOnly found {with_fits + exists_fits}/{target} entries with fit data")
        print(f"   You may need to try more SASBDB codes")
    else:
        print(f"\n SUCCESS: {with_fits + exists_fits} entries ready for validation")
