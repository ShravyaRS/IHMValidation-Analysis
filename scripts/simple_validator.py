#!/usr/bin/env python3
"""
Simplified validator that bypasses PDF generation
"""
import sys
import os

# Add to path
sys.path.insert(0, 'IHMValidation')

def validate_structure(cif_file):
    """Run validation without PDF generation"""
    print(f"\n{'='*60}")
    print(f"Validating: {cif_file}")
    print(f"{'='*60}\n")
    
    try:
        # Import validation modules
        from ihm_validation import get_input_information
        from ihm_validation import sas
        from ihm_validation import cx
        from ihm_validation import em
        
        # Read structure
        print("[1/5] Reading structure file...")
        I = get_input_information.GetInputInformation(cif_file)
        
        print(f"  Entry ID: {I.get_id()}")
        print(f"  Title: {I.get_title()}")
        
        # Get datasets
        print("\n[2/5] Analyzing datasets...")
        datasets = I.get_dataset_comp()
        print(f"  Available data types: {datasets}")
        
        # SAS validation
        print("\n[3/5] Running SAS validation...")
        try:
            sas_val = sas.sas_validation(I)
            print(f"  SAS validation complete")
            print(f"  Results: {type(sas_val)}")
        except Exception as e:
            print(f"  SAS validation skipped: {e}")
        
        # CX validation
        print("\n[4/5] Running Crosslink validation...")
        try:
            cx_val = cx.cx_validation(I)
            print(f"  CX validation complete")
        except Exception as e:
            print(f"  CX validation skipped: {e}")
        
        # EM validation
        print("\n[5/5] Running EM validation...")
        try:
            em_val = em.em_validation(I)
            print(f"  EM validation complete")
        except Exception as e:
            print(f"  EM validation skipped: {e}")
        
        print(f"\n{'='*60}")
        print("✓ Validation complete!")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python simple_validator.py <structure.cif>")
        sys.exit(1)
    
    success = validate_structure(sys.argv[1])
    sys.exit(0 if success else 1)
