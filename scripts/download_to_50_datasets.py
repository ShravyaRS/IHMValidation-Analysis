#!/usr/bin/env python3

import requests
import time
from pathlib import Path

# Extended list to reach 50+ entries with fits
ADDITIONAL_CODES = [
    # Series 9 continuation
    "SASDAP9", "SASDAQ9", "SASDAR9", "SASDAS9", "SASDAT9",
    "SASDAU9", "SASDAV9", "SASDAW9", "SASDAX9", "SASDAY9",
    "SASDAZ9", "SASDBA9", "SASDBB9", "SASDBC9", "SASDBD9",
    "SASDBE9", "SASDBF9", "SASDBG9", "SASDBH9", "SASDBI9",
    "SASDBJ9", "SASDBK9", "SASDBL9", "SASDBM9", "SASDBN9",
    
    # Series 7
    "SASDAA7", "SASDAB7", "SASDAC7", "SASDAD7", "SASDAE7",
    "SASDAF7", "SASDAG7", "SASDAH7", "SASDAI7", "SASDAJ7",
    "SASDAK7", "SASDAL7", "SASDAM7", "SASDAN7", "SASDAO7",
    "SASDAP7", "SASDAQ7", "SASDAR7", "SASDAS7", "SASDAT7",
    
    # Series 6
    "SASDAA6", "SASDAB6", "SASDAC6", "SASDAD6", "SASDAE6",
    "SASDAF6", "SASDAG6", "SASDAH6", "SASDAI6", "SASDAJ6",
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
            print(f" ✓ ({len(response.text)} bytes)")
            return True, "downloaded"
        else:
            print(f" ✗")
            return False, "no_fits"
    except Exception as e:
        print(f" ✗ ({str(e)[:30]})")
        return False, "failed"

if __name__ == "__main__":
    output_dir = "/root/projects/IHMValidation-Analysis/Validation/cache"
    
    # Count current entries
    current = len(list(Path(output_dir).glob("*.sascif")))
    target = 50
    needed = max(0, target - current)
    
    print("="*80)
    print("DOWNLOADING ADDITIONAL SASBDB ENTRIES")
    print("="*80)
    print(f"Current entries: {current}")
    print(f"Target: {target}")
    print(f"Need to download: {needed}")
    print()
    
    downloaded = 0
    exists = 0
    no_fits = 0
    failed = 0
    
    for code in ADDITIONAL_CODES:
        if current + downloaded >= target:
            print(f"\n✓ Reached target of {target} entries!")
            break
        
        success, status = download_sascif(code, output_dir)
        
        if status == "downloaded":
            downloaded += 1
            time.sleep(1)  # Be nice to server
        elif status == "exists_with_fits":
            exists += 1
        elif status in ["no_fits", "exists_no_fits"]:
            no_fits += 1
        else:
            failed += 1
    
    print(f"\n{'='*80}")
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"Downloaded with fits:  {downloaded}")
    print(f"Already had with fits: {exists}")
    print(f"Total entries now:     {current + downloaded}")
    print(f"No fit data:           {no_fits}")
    print(f"Failed:                {failed}")
    print("="*80)
