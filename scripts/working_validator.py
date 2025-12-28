#!/usr/bin/env python3
"""
Working validator based on actual IHMValidation structure
"""
import sys
import os
import json

# Add to path
sys.path.insert(0, 'IHMValidation')

def validate_structure(cif_file, output_dir='validation-outputs/working/'):
    """Run validation using actual modules"""
    
    print(f"\n{'='*60}")
    print(f"Validating: {cif_file}")
    print(f"{'='*60}\n")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Import based on actual structure
        from ihm_validation import mmcif_io
        from ihm_validation import sas
        from ihm_validation import cx  
        from ihm_validation import em
        from ihm_validation import utility
        
        print("[1/6] Reading mmCIF file...")
        # Use mmcif_io to read the file
        mmcif_data = mmcif_io.GetInputInformation(cif_file)
        
        entry_id = mmcif_data.get_id()
        print(f"  ✓ Entry ID: {entry_id}")
        
        print("\n[2/6] Getting dataset composition...")
        datasets = mmcif_data.get_dataset_comp()
        print(f"  Available datasets: {datasets}")
        
        results = {
            'entry_id': entry_id,
            'input_file': cif_file,
            'datasets': datasets,
            'validations': {}
        }
        
        print("\n[3/6] Running SAS validation...")
        try:
            sas_result = sas.sas_validation(mmcif_data)
            results['validations']['sas'] = str(type(sas_result))
            print(f"  ✓ SAS validation completed")
            
            # Try to extract metrics
            if hasattr(sas_result, '__dict__'):
                sas_dict = vars(sas_result)
                print(f"    SAS attributes: {list(sas_dict.keys())[:5]}")
        except Exception as e:
            results['validations']['sas'] = f"Error: {str(e)}"
            print(f"  ⚠ SAS validation: {e}")
        
        print("\n[4/6] Running Crosslink validation...")
        try:
            cx_result = cx.cx_validation(mmcif_data)
            results['validations']['cx'] = str(type(cx_result))
            print(f"  ✓ CX validation completed")
            
            if hasattr(cx_result, '__dict__'):
                cx_dict = vars(cx_result)
                print(f"    CX attributes: {list(cx_dict.keys())[:5]}")
        except Exception as e:
            results['validations']['cx'] = f"Error: {str(e)}"
            print(f"  ⚠ CX validation: {e}")
        
        print("\n[5/6] Running EM validation...")
        try:
            em_result = em.em_validation(mmcif_data)
            results['validations']['em'] = str(type(em_result))
            print(f"  ✓ EM validation completed")
            
            if hasattr(em_result, '__dict__'):
                em_dict = vars(em_result)
                print(f"    EM attributes: {list(em_dict.keys())[:5]}")
        except Exception as e:
            results['validations']['em'] = f"Error: {str(e)}"
            print(f"  ⚠ EM validation: {e}")
        
        print("\n[6/6] Saving results...")
        results_file = os.path.join(output_dir, 'validation_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"  ✓ Results saved to: {results_file}")
        
        print(f"\n{'='*60}")
        print("✓ Validation complete!")
        print(f"{'='*60}\n")
        
        return results
        
    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python working_validator.py <structure.cif>")
        sys.exit(1)
    
    result = validate_structure(sys.argv[1])
    sys.exit(0 if result else 1)
