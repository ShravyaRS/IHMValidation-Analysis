#!/usr/bin/env python3

import requests
import time
from pathlib import Path

# List of known SASBDB codes with fits (manually curated)
# These are entries that have both experimental and fitted data
SASBDB_CODES = [
    # Your existing 5
    "SASDBV9", "SASDBW9", "SASDBX9", "SASDBY9", "SASDBZ9",
    # Additional entries (examples - we'll try these)
    "SASDAA8", "SASDAB2", "SASDAB8", "SASDAC8", "SASDAD8",
    "SASDAE8", "SASDAF8", "SASDAG8", "SASDAH8", "SASDAI8",
    "SASDAJ8", "SASDAK8", "SASDAL8", "SASDAM8", "SASDAN8",
    "SASDAO8", "SASDAP8", "SASDAQ8", "SASDAR8", "SASDAS8",
    "SASDAT8", "SASDAU8", "SASDAV8", "SASDAW8", "SASDAX8",
    "SASDAY8", "SASDAZ8", "SASDBA8", "SASDBB8", "SASDBC8",
    "SASDBD8", "SASDBE8", "SASDBF8", "SASDBG8", "SASDBH8",
    "SASDBI8", "SASDBJ8", "SASDBK8", "SASDBL8", "SASDBM8",
]

def download_sascif(code, output_dir):
    url = f"https://www.sasbdb.org/media/sascif/sascif_files/{code}.sascif"
    output_path = Path(output_dir) / f"{code}.sascif"
    
    if output_path.exists():
        return True, "exists"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_path, 'w') as f:
                f.write(response.text)
            return True, "downloaded"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    output_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    
    print("Downloading SASBDB entries...")
    
    success = 0
    exists = 0
    failed = 0
    
    for code in SASBDB_CODES:
        status, msg = download_sascif(code, output_dir)
        if status and msg == "downloaded":
            print(f"✓ {code}: Downloaded")
            success += 1
            time.sleep(1)
        elif status and msg == "exists":
            print(f"• {code}: Already exists")
            exists += 1
        else:
            print(f"✗ {code}: {msg}")
            failed += 1
    
    print(f"\nTotal: {success + exists} available, {failed} failed")
