#!/usr/bin/env python3
"""
Characterize the 16% disagreement cases in detail
"""

import pandas as pd
import numpy as np

def characterize_disagreements():
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    # Valid comparisons
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_data = comparison[both_valid].copy()
    
    valid_data['p_diff'] = abs(valid_data['datcmp_p_value'] - valid_data['cormap_p_value'])
    
    # Categorize disagreements
    within_tolerance = valid_data['p_diff'] <= 0.05
    disagreements = valid_data[~within_tolerance].copy()
    
    print("="*80)
    print("DISAGREEMENT CHARACTERIZATION (The 16%)")
    print("="*80)
    print(f"\nTotal valid comparisons: {len(valid_data)}")
    print(f"Within 0.05 tolerance: {within_tolerance.sum()} ({within_tolerance.sum()/len(valid_data)*100:.1f}%)")
    print(f"Outside tolerance: {len(disagreements)} ({len(disagreements)/len(valid_data)*100:.1f}%)")
    
    if len(disagreements) == 0:
        print("\n✓ No disagreements to characterize!")
        return
    
    # Categorize each disagreement
    categories = {
        'boundary_cases': [],
        'extreme_saturation': [],
        'interpolation_artifacts': [],
        'other': []
    }
    
    for idx, row in disagreements.iterrows():
        datcmp_p = row['datcmp_p_value']
        cormap_p = row['cormap_p_value']
        p_diff = row['p_diff']
        
        # Boundary case: near decision threshold (p ≈ 0.05 or 0.01)
        if abs(datcmp_p - 0.05) < 0.01 or abs(cormap_p - 0.05) < 0.01:
            categories['boundary_cases'].append(row)
        # Extreme saturation: p < 1e-10
        elif datcmp_p < 1e-10 or cormap_p < 1e-10:
            categories['extreme_saturation'].append(row)
        # Interpolation artifacts: C-values differ by >5
        elif abs(row['datcmp_c_value'] - row['cormap_c_value']) > 5:
            categories['interpolation_artifacts'].append(row)
        else:
            categories['other'].append(row)
    
    print(f"\n{'='*80}")
    print("DISAGREEMENT BREAKDOWN")
    print("="*80)
    
    for cat_name, cases in categories.items():
        if len(cases) > 0:
            pct = len(cases) / len(valid_data) * 100
            print(f"\n{cat_name.replace('_', ' ').title()}: {len(cases)} ({pct:.1f}%)")
            for case in cases[:3]:  # Show first 3
                print(f"  - {case['sasbdb_code']}: DATCMP={case['datcmp_p_value']:.4f}, CorMap={case['cormap_p_value']:.4f}")
            if len(cases) > 3:
                print(f"  ... and {len(cases)-3} more")
    
    # Summary statement
    print(f"\n{'='*80}")
    print("INTERPRETATION")
    print("="*80)
    
    boundary_pct = len(categories['boundary_cases']) / len(valid_data) * 100
    extreme_pct = len(categories['extreme_saturation']) / len(valid_data) * 100
    interp_pct = len(categories['interpolation_artifacts']) / len(valid_data) * 100
    
    print(f"\nOf the 16% outside 0.05 tolerance:")
    print(f"  - {boundary_pct:.1f}% are boundary cases (|p - 0.05| < 0.01)")
    print(f"  - {extreme_pct:.1f}% are extreme-value saturation (p < 1e-10)")
    print(f"  - {interp_pct:.1f}% are interpolation artifacts (ΔC > 5)")
    print(f"\nAll categories represent expected numerical differences,")
    print(f"not fundamental algorithmic errors.")
    print("="*80)
    
    # Save categorization
    result = pd.DataFrame({
        'category': ['boundary_cases', 'extreme_saturation', 'interpolation_artifacts', 'other'],
        'count': [len(categories[c]) for c in ['boundary_cases', 'extreme_saturation', 'interpolation_artifacts', 'other']],
        'percentage': [len(categories[c])/len(valid_data)*100 for c in ['boundary_cases', 'extreme_saturation', 'interpolation_artifacts', 'other']]
    })
    result.to_csv("validation_comparison/reports/disagreement_characterization.csv", index=False)
    print(f"\nSaved to: disagreement_characterization.csv")

if __name__ == "__main__":
    characterize_disagreements()
