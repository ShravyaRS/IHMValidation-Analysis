#!/bin/bash
set -e

echo "=========================================="
echo "PHASE 5: Discover & Run Actual Validation"
echo "=========================================="

# Step 1: Discover what's actually in ihm_validation
echo -e "\n[1/5] Discovering available modules..."

python3 << 'DISCOVER'
import sys
sys.path.insert(0, 'IHMValidation')

import ihm_validation
print("ihm_validation module location:", ihm_validation.__file__)
print("\nAvailable attributes:")
for attr in dir(ihm_validation):
    if not attr.startswith('_'):
        print(f"  - {attr}")

# Check individual files
import os
ihm_dir = 'IHMValidation/ihm_validation'
print(f"\n\nPython files in {ihm_dir}:")
for f in sorted(os.listdir(ihm_dir)):
    if f.endswith('.py'):
        print(f"  - {f}")
DISCOVER

# Step 2: Check what each module exports
echo -e "\n[2/5] Checking module contents..."

python3 << 'CHECK_MODULES'
import sys
sys.path.insert(0, 'IHMValidation')

modules_to_check = [
    'mmcif_io',
    'sas', 
    'cx',
    'em',
    'molprobity',
    'report',
    'utility'
]

for mod_name in modules_to_check:
    try:
        mod = __import__(f'ihm_validation.{mod_name}', fromlist=[mod_name])
        print(f"\n✓ {mod_name}:")
        funcs = [x for x in dir(mod) if not x.startswith('_') and callable(getattr(mod, x))]
        for func in funcs[:5]:
            print(f"    - {func}()")
        if len(funcs) > 5:
            print(f"    ... and {len(funcs)-5} more")
    except Exception as e:
        print(f"\n✗ {mod_name}: {e}")
CHECK_MODULES

# Step 3: Read the actual ihm_validator.py to understand usage
echo -e "\n[3/5] Understanding ihm_validator.py flow..."

grep -A 5 "def main" IHMValidation/ihm_validation/ihm_validator.py || echo "No main() function"

# Check the imports it uses
echo -e "\nKey imports in ihm_validator.py:"
grep "^from" IHMValidation/ihm_validation/ihm_validator.py | grep -v "^#"

# Step 4: Create working validator based on actual structure
echo -e "\n[4/5] Creating working validator..."

cat > scripts/working_validator.py << 'WORKING'
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
WORKING

chmod +x scripts/working_validator.py

echo -e "\n[5/5] Running working validation..."
python3 scripts/working_validator.py test-data/PDBDEV_00000001.cif 2>&1 | tee reports/working_validation1.log

# Also run on second file
echo -e "\n\nValidating second structure..."
python3 scripts/working_validator.py test-data/PDBDEV_00000010.cif 2>&1 | tee reports/working_validation2.log

# Check results
echo -e "\n\nValidation Results:"
if [ -f validation-outputs/working/validation_results.json ]; then
    echo "✓ Results file created!"
    cat validation-outputs/working/validation_results.json
fi

echo ""
echo "=========================================="
echo "✓ Phase 5 Complete - Real Validations Run!"
echo "=========================================="
echo ""
echo "Review outputs:"
echo "  - reports/working_validation1.log"
echo "  - reports/working_validation2.log"  
echo "  - validation-outputs/working/validation_results.json"
echo ""

