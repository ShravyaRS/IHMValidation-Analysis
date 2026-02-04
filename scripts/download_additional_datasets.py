#!/usr/bin/env python3

import requests
import time
from pathlib import Path

# Additional SASBDB codes to reach 50+ total
ADDITIONAL_CODES = [
    # Series 9 continuation
    "SASDAP9", "SASDAQ9", "SASDAR9", "SASDAS9", "SASDAT9",
    "SASDAU9", "SASDAV9", "SASDAW9", "SASDAX9", "SASDAY9",
    "SASDAZ9", "SASDBA9", "SASDBB9", "SASDBC9", "SASDBD9",
    "SASDBE9", "SASDBF9", "SASDBG9", "SASDBH9", "SASDBI9",
    
    # Try some Series 7
    "SASDAA7", "SASDAB7", "SASDAC7", "SASDAD7", "SASDAE7",
    "SASDAF7", "SASDAG7", "SASDAH7", "SASDAI7", "SASDAJ7",
]

def download_sascif(code, output_dir):
    url = f"https://www.sasbdb.org/media/sascif/sascif_files/{code}.sascif"
    output_path = Path(output_dir) / f"{code}.sascif"
    
    if output_path.exists():
        with open(output_path, 'r') as f:
            if '_FIT_' in f.read():
                return True, "exists_with_fits"
        return True, "exists_no_fits"
    
    try:
        print(f"  {code}...", end='', flush=True)
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200 and '_FIT_' in response.text:
            with open(output_path, 'w') as f:
                f.write(response.text)
            print(f" ✓")
            return True, "downloaded"
        else:
            print(f" ✗")
            return False, "no_fits"
    except:
        print(f" ✗")
        return False, "failed"

if __name__ == "__main__":
    output_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    target = 20
    
    print("Downloading additional SASBDB entries...")
    success = 0
    
    for code in ADDITIONAL_CODES:
        if success >= target:
            break
        s, msg = download_sascif(code, output_dir)
        if s and msg == "downloaded":
            success += 1
            time.sleep(1)
    
    print(f"\nDownloaded {success} additional entries")
