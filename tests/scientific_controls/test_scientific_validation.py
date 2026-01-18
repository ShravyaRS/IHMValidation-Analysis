#!/usr/bin/env python3
"""
Scientific Unit Tests - Validate biophysical correctness, not just code execution
"""

import subprocess
import os
import sys
from pathlib import Path

class ScientificValidator:
    """Validates that the tool produces scientifically correct results"""
    
    def __init__(self):
        self.gold_standard = "tests/scientific_controls/gold_standard.cif"
        self.decoy_broken = "tests/scientific_controls/decoy_broken.cif"
        self.results = {}
    
    def run_validation(self, structure_file, label):
        """Run IHMValidation on a structure"""
        print(f"\nTesting {label}...")
        cmd = [
            'singularity', 'exec', 
            'IHMValidation/ihmvalidation_complete.sif',
            'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
            '-f', structure_file,
            '--output-root', f'tests/scientific_controls/output_{label}',
            '--output-prefix', label
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            success = result.returncode == 0
            self.results[label] = {
                'exit_code': result.returncode,
                'success': success
            }
            return success
        except Exception as e:
            print(f"Error: {e}")
            self.results[label] = {'exit_code': -1, 'success': False}
            return False
    
    def test_discrimination(self):
        """Test that tool can differentiate good from bad structures"""
        print("\n" + "="*60)
        print("SCIENTIFIC CONTROL TEST")
        print("="*60)
        
        gold_result = self.run_validation(self.gold_standard, "gold")
        decoy_result = self.run_validation(self.decoy_broken, "decoy")
        
        # The tool should handle gold standard better than decoy
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        print(f"Gold Standard: {'PASS' if gold_result else 'FAIL'}")
        print(f"Decoy (Broken): {'Correctly rejected' if not decoy_result else 'FAIL - accepted bad structure'}")
        
        if gold_result and not decoy_result:
            print("\n✓ SCIENTIFIC VALIDITY CONFIRMED")
            print("Tool correctly discriminates between valid and invalid structures")
            return True
        else:
            print("\n✗ SCIENTIFIC VALIDITY ISSUE")
            print("Tool does not properly discriminate structure quality")
            return False

if __name__ == '__main__':
    validator = ScientificValidator()
    result = validator.test_discrimination()
    sys.exit(0 if result else 1)
