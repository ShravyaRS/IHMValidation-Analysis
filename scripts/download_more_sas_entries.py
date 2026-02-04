#!/usr/bin/env python3

import requests
import time
from pathlib import Path
import json

def get_sasbdb_entries(limit=50):
    """
    Get list of SASBDB entries from the database
    """
    # SASBDB REST API endpoint
    url = "https://www.sasbdb.org/rest-api/entry/list/"
    
    print(f"Fetching SASBDB entry list...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            entries = [item['code'] for item in data if 'code' in item]
            print(f"Found {len(entries)} total entries in SASBDB")
            return entries[:limit]
        else:
            print(f"Error: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching entry list: {e}")
        return []

def download_sascif(code, output_dir):
    """
    Download .sascif file for a given SASBDB code
    """
    url = f"https://www.sasbdb.org/media/sascif/sascif_files/{code}.sascif"
    output_path = Path(output_dir) / f"{code}.sascif"
    
    # Skip if already exists
    if output_path.exists():
        print(f"  {code}: Already exists")
        return True
    
    try:
        print(f"  {code}: Downloading...", end='')
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with open(output_path, 'w') as f:
                f.write(response.text)
            print(f" ✓ ({len(response.text)} bytes)")
            return True
        else:
            print(f" ✗ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f" ✗ Error: {e}")
        return False

if __name__ == "__main__":
    output_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    target_count = 50
    
    print("="*80)
    print("DOWNLOADING ADDITIONAL SASBDB ENTRIES")
    print("="*80)
    print(f"Target: {target_count} entries")
    print(f"Output: {output_dir}\n")
    
    # Get list of entries
    entries = get_sasbdb_entries(limit=100)  # Get more than needed
    
    if not entries:
        print("ERROR: Could not fetch entry list")
        exit(1)
    
    # Download entries
    successful = 0
    failed = 0
    
    for i, code in enumerate(entries, 1):
        if successful >= target_count:
            break
        
        if download_sascif(code, output_dir):
            successful += 1
            time.sleep(0.5)  # Be nice to the server
        else:
            failed += 1
        
        if i % 10 == 0:
            print(f"\nProgress: {successful} successful, {failed} failed\n")
    
    print(f"\n{'='*80}")
    print(f"DOWNLOAD COMPLETE")
    print(f"{'='*80}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {successful + failed}")
