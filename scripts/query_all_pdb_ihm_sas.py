#!/usr/bin/env python3
"""
Query PDB-IHM for all SAS entries using REST API
"""

import requests
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path

def scrape_pdb_ihm_sas():
    """
    Scrape PDB-IHM website for SAS entries
    """
    print("="*80)
    print("QUERYING PDB-IHM FOR SAS ENTRIES")
    print("="*80)
    
    # Try REST API first
    api_url = "https://pdb-ihm.org/api/search"
    
    # Search parameters
    params = {
        'input_data_type': 'SAS data',
        'format': 'json'
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"API Success: {len(data)} entries found")
            return parse_api_response(data)
    except Exception as e:
        print(f"API failed: {e}")
    
    # Fallback: Parse the HTML page
    print("\nTrying HTML scraping...")
    
    # URL with SAS filter applied
    url = "https://pdb-ihm.org/?input_data_type=SAS+data"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all entry IDs (8ZZX pattern)
        entries = []
        entry_pattern = re.compile(r'8[A-Z0-9]{3}')
        
        # Look for entry links
        for link in soup.find_all('a', href=True):
            href = link['href']
            match = entry_pattern.search(href)
            if match:
                entry_id = match.group()
                if entry_id not in entries:
                    entries.append(entry_id)
        
        print(f"\nFound {len(entries)} PDB-IHM entries")
        
        if len(entries) == 0:
            print("\nManual list from screenshot:")
            # From your screenshot
            manual_entries = ['8ZZ4', '8ZZ9', '8ZZA']  # Add more as visible
            return get_sasbdb_codes(manual_entries)
        
        return get_sasbdb_codes(entries)
        
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def get_sasbdb_codes(pdb_ihm_entries):
    """
    Get SASBDB codes for each PDB-IHM entry
    """
    print(f"\nQuerying SASBDB codes for {len(pdb_ihm_entries)} entries...")
    
    sasbdb_codes = []
    entry_mapping = {}
    
    for entry_id in pdb_ihm_entries:
        try:
            # Query PDB-IHM entry page
            url = f"https://pdb-ihm.org/{entry_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Look for SASBDB codes (SASD*** pattern)
                sasbdb_pattern = re.compile(r'SASD[A-Z0-9]{3,4}')
                matches = sasbdb_pattern.findall(response.text)
                
                for code in set(matches):
                    if code not in sasbdb_codes:
                        sasbdb_codes.append(code)
                        entry_mapping[code] = entry_id
                        print(f"  {entry_id} → {code}")
            
        except Exception as e:
            print(f"  {entry_id} - Error: {e}")
            continue
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print("="*80)
    print(f"PDB-IHM entries processed: {len(pdb_ihm_entries)}")
    print(f"SASBDB codes found: {len(sasbdb_codes)}")
    
    # Save results
    output = {
        'pdb_ihm_entries': pdb_ihm_entries,
        'sasbdb_codes': sasbdb_codes,
        'entry_mapping': entry_mapping
    }
    
    with open('pdb_ihm_sas_complete.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: pdb_ihm_sas_complete.json")
    print("="*80)
    
    return sasbdb_codes

if __name__ == "__main__":
    codes = scrape_pdb_ihm_sas()
    
    if codes:
        print(f"\n✓ Found {len(codes)} SASBDB codes")
        print(f"\nNext step:")
        print(f"  python scripts/batch_download_sasbdb.py")
    else:
        print(f"\n✗ No SASBDB codes found")
        print(f"\nFallback: Use manual list from PDB-IHM website")
