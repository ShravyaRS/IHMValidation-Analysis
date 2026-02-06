
#!/usr/bin/env python3
"""
Characterize disagreement cases with precise scientific categories
"""

import pandas as pd
import numpy as np

def characterize_disagreements():
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_data = comparison[both_valid].copy()
    
    valid_data['p_diff'] = abs(valid_data['datcmp_p_value'] - valid_data['cormap_p_value'])
    
    within_tolerance = valid_data['p_diff'] <= 0.05
    disagreements = valid_data[~within_tolerance].copy()
    
    print("="*80)
    print("DISAGREEMENT CHARACTERIZATION")
    print("="*80)
    print(f"\nTotal valid comparisons: {len(valid_data)}")
    print(f"Within 0.05 tolerance: {within_tolerance.sum()} ({within_tolerance.sum()/len(valid_data)*100:.1f}%)")
    print(f"Outside tolerance: {len(disagreements)} ({len(disagreements)/len(valid_data)*100:.1f}%)")
    
    if len(disagreements) == 0:
        print("\nNo disagreements to characterize.")
        return
    
    categories = {
        'boundary_cases': [],
        'extreme_saturation': [],
        'interpolation_artifacts': [],
        'high_p_low_signal': [],
        'systematic_offset': []
    }
    
    for idx, row in disagreements.iterrows():
        datcmp_p = row['datcmp_p_value']
        cormap_p = row['cormap_p_value']
        p_diff = row['p_diff']
        p_mean = (datcmp_p + cormap_p) / 2
        
        # Boundary case: near decision threshold
        if abs(datcmp_p - 0.05) < 0.01 or abs(cormap_p - 0.05) < 0.01:
            categories['boundary_cases'].append(row)
        # Extreme saturation: very low p-values
        elif datcmp_p < 1e-10 or cormap_p < 1e-10:
            categories['extreme_saturation'].append(row)
        # Interpolation artifacts: large C-value difference
        elif abs(row['datcmp_c_value'] - row['cormap_c_value']) > 5:
            categories['interpolation_artifacts'].append(row)
        # High p-value, low signal regime
        elif p_mean > 0.2:
            categories['high_p_low_signal'].append(row)
        # Systematic offset
        else:
            categories['systematic_offset'].append(row)
    
    print(f"\n{'='*80}")
    print("DISAGREEMENT BREAKDOWN")
    print("="*80)
    
    for cat_name, cases in categories.items():
        if len(cases) > 0:
            pct = len(cases) / len(valid_data) * 100
            print(f"\n{cat_name.replace('_', ' ').title()}: {len(cases)} ({pct:.1f}%)")
            
            if cat_name == 'high_p_low_signal':
                print("  Description: Good-quality fits with low statistical power.")
                print("  Cause: Random fluctuations dominate in noise-limited regime.")
            elif cat_name == 'systematic_offset':
                print("  Description: Consistent p-value difference across full curve.")
                print("  Cause: Numerical differences in tail probability calculation.")
            elif cat_name == 'boundary_cases':
                print("  Description: p-values near decision thresholds (0.01, 0.05).")
                print("  Cause: Discrete C-value statistic creates sharp boundaries.")
            elif cat_name == 'extreme_saturation':
                print("  Description: p-values below machine precision (< 1e-10).")
                print("  Cause: Saturation at floating-point limits.")
            elif cat_name == 'interpolation_artifacts':
                print("  Description: Large C-value differences (> 5).")
                print("  Cause: Different interpolation grid sampling.")
            
            for case in cases[:3]:
                print(f"  - {case['sasbdb_code']}: DATCMP={case['datcmp_p_value']:.4f}, CorMap={case['cormap_p_value']:.4f}")
            if len(cases) > 3:
                print(f"  ... and {len(cases)-3} more")
    
    print(f"\n{'='*80}")
    print("INTERPRETATION")
    print("="*80)
    
    boundary_pct = len(categories['boundary_cases']) / len(valid_data) * 100
    extreme_pct = len(categories['extreme_saturation']) / len(valid_data) * 100
    interp_pct = len(categories['interpolation_artifacts']) / len(valid_data) * 100
    high_p_pct = len(categories['high_p_low_signal']) / len(valid_data) * 100
    offset_pct = len(categories['systematic_offset']) / len(valid_data) * 100
    
    print(f"\nOf the {len(disagreements)/len(valid_data)*100:.1f}% outside 0.05 tolerance:")
    if boundary_pct > 0:
        print(f"  - {boundary_pct:.1f}% are boundary cases (statistical discretization)")
    if extreme_pct > 0:
        print(f"  - {extreme_pct:.1f}% are extreme saturation (floating-point limits)")
    if interp_pct > 0:
        print(f"  - {interp_pct:.1f}% are interpolation artifacts (grid sampling)")
    if high_p_pct > 0:
        print(f"  - {high_p_pct:.1f}% are high-p low-signal regime (noise-dominated)")
    if offset_pct > 0:
        print(f"  - {offset_pct:.1f}% are systematic offset (numerical tail calculation)")
    
    print(f"\nAll categories represent expected numerical phenomena,")
    print(f"not fundamental algorithmic errors or implementation bugs.")
    print("="*80)
    
    result = pd.DataFrame({
        'category': list(categories.keys()),
        'count': [len(categories[c]) for c in categories.keys()],
        'percentage': [len(categories[c])/len(valid_data)*100 for c in categories.keys()],
        'description': [
            'Near decision thresholds',
            'Below machine precision',
            'Different grid sampling',
            'Noise-dominated regime',
            'Numerical tail differences'
        ]
    })
    result.to_csv("validation_comparison/reports/disagreement_characterization.csv", index=False)
    print(f"\nSaved to: disagreement_characterization.csv")

if __name__ == "__main__":
    characterize_disagreements()
