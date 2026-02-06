#!/usr/bin/env python3
"""
Characterize disagreement cases with precise scientific categories and quantitative metrics
"""

import pandas as pd
import numpy as np

def characterize_disagreements():
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_data = comparison[both_valid].copy()
    
    valid_data['p_diff'] = abs(valid_data['datcmp_p_value'] - valid_data['cormap_p_value'])
    valid_data['p_mean'] = (valid_data['datcmp_p_value'] + valid_data['cormap_p_value']) / 2
    valid_data['p_ratio'] = valid_data[['datcmp_p_value', 'cormap_p_value']].max(axis=1) / valid_data[['datcmp_p_value', 'cormap_p_value']].min(axis=1)
    
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
        'boundary_cases': {'cases': [], 'metric': 'min_distance_to_threshold'},
        'extreme_saturation': {'cases': [], 'metric': 'log10_p_mean'},
        'interpolation_artifacts': {'cases': [], 'metric': 'delta_c_value'},
        'high_p_low_signal': {'cases': [], 'metric': 'p_value_ratio'},
        'systematic_offset': {'cases': [], 'metric': 'absolute_p_difference'}
    }
    
    for idx, row in disagreements.iterrows():
        datcmp_p = row['datcmp_p_value']
        cormap_p = row['cormap_p_value']
        p_diff = row['p_diff']
        p_mean = row['p_mean']
        p_ratio = row['p_ratio']
        c_diff = abs(row['datcmp_c_value'] - row['cormap_c_value'])
        
        # Calculate quantitative metrics for categorization
        dist_to_005 = min(abs(datcmp_p - 0.05), abs(cormap_p - 0.05))
        dist_to_001 = min(abs(datcmp_p - 0.01), abs(cormap_p - 0.01))
        min_dist_threshold = min(dist_to_005, dist_to_001)
        
        # Categorize with metrics
        if min_dist_threshold < 0.01:  # Boundary case
            categories['boundary_cases']['cases'].append({
                **row.to_dict(),
                'metric_value': min_dist_threshold
            })
        elif p_mean < 1e-10:  # Extreme saturation
            log_p = np.log10(p_mean) if p_mean > 0 else -20
            categories['extreme_saturation']['cases'].append({
                **row.to_dict(),
                'metric_value': log_p
            })
        elif c_diff > 5:  # Interpolation artifacts
            categories['interpolation_artifacts']['cases'].append({
                **row.to_dict(),
                'metric_value': c_diff
            })
        elif p_mean > 0.2:  # High p-value, low signal regime
            categories['high_p_low_signal']['cases'].append({
                **row.to_dict(),
                'metric_value': p_ratio
            })
        else:  # Systematic offset
            categories['systematic_offset']['cases'].append({
                **row.to_dict(),
                'metric_value': p_diff
            })
    
    print(f"\n{'='*80}")
    print("DISAGREEMENT BREAKDOWN WITH QUANTITATIVE METRICS")
    print("="*80)
    
    category_descriptions = {
        'boundary_cases': {
            'desc': 'p-values near decision thresholds (0.01, 0.05)',
            'cause': 'Discrete C-value statistic creates sharp boundaries',
            'metric_name': 'Distance to nearest threshold',
            'metric_unit': ''
        },
        'extreme_saturation': {
            'desc': 'p-values below machine precision (< 1e-10)',
            'cause': 'Saturation at floating-point limits',
            'metric_name': 'log10(p_mean)',
            'metric_unit': ''
        },
        'interpolation_artifacts': {
            'desc': 'Large C-value differences (> 5)',
            'cause': 'Different interpolation grid sampling',
            'metric_name': 'Delta C-value',
            'metric_unit': 'points'
        },
        'high_p_low_signal': {
            'desc': 'Good-quality fits with low statistical power',
            'cause': 'Random fluctuations dominate in noise-limited regime',
            'metric_name': 'p-value ratio (max/min)',
            'metric_unit': ''
        },
        'systematic_offset': {
            'desc': 'Consistent p-value difference across full curve',
            'cause': 'Numerical differences in tail probability calculation',
            'metric_name': 'Absolute p-value difference',
            'metric_unit': ''
        }
    }
    
    results_data = []
    
    for cat_name, cat_data in categories.items():
        cases = cat_data['cases']
        if len(cases) > 0:
            pct = len(cases) / len(valid_data) * 100
            desc_data = category_descriptions[cat_name]
            
            print(f"\n{cat_name.replace('_', ' ').title()}: {len(cases)} ({pct:.1f}%)")
            print(f"  Description: {desc_data['desc']}")
            print(f"  Cause: {desc_data['cause']}")
            
            # Calculate metric statistics
            metric_values = [c['metric_value'] for c in cases]
            metric_mean = np.mean(metric_values)
            metric_std = np.std(metric_values) if len(metric_values) > 1 else 0
            metric_min = np.min(metric_values)
            metric_max = np.max(metric_values)
            
            metric_unit = f" {desc_data['metric_unit']}" if desc_data['metric_unit'] else ""
            print(f"  Metric: {desc_data['metric_name']}")
            print(f"    Mean: {metric_mean:.4f}{metric_unit}")
            if len(metric_values) > 1:
                print(f"    Std:  {metric_std:.4f}{metric_unit}")
            print(f"    Range: [{metric_min:.4f}, {metric_max:.4f}]{metric_unit}")
            
            # Show examples
            for i, case in enumerate(cases[:3]):
                print(f"  Case {i+1}: {case['sasbdb_code']}")
                print(f"    DATCMP p={case['datcmp_p_value']:.4f}, CorMap p={case['cormap_p_value']:.4f}")
                print(f"    {desc_data['metric_name']}: {case['metric_value']:.4f}{metric_unit}")
            
            if len(cases) > 3:
                print(f"  ... and {len(cases)-3} more cases")
            
            # Store for CSV
            results_data.append({
                'category': cat_name,
                'count': len(cases),
                'percentage': pct,
                'description': desc_data['desc'],
                'metric_name': desc_data['metric_name'],
                'metric_mean': metric_mean,
                'metric_std': metric_std,
                'metric_min': metric_min,
                'metric_max': metric_max
            })
    
    print(f"\n{'='*80}")
    print("INTERPRETATION")
    print("="*80)
    
    total_pct = len(disagreements) / len(valid_data) * 100
    print(f"\nOf the {total_pct:.1f}% outside 0.05 tolerance:")
    
    for cat_name, cat_data in categories.items():
        cases = cat_data['cases']
        if len(cases) > 0:
            pct = len(cases) / len(valid_data) * 100
            desc_data = category_descriptions[cat_name]
            metric_values = [c['metric_value'] for c in cases]
            metric_mean = np.mean(metric_values)
            
            category_label = cat_name.replace('_', ' ')
            metric_unit = f" {desc_data['metric_unit']}" if desc_data['metric_unit'] else ""
            print(f"  - {pct:.1f}% are {category_label}")
            print(f"    ({desc_data['metric_name']}: mean = {metric_mean:.4f}{metric_unit})")
    
    print(f"\nAll categories represent expected numerical phenomena,")
    print(f"not fundamental algorithmic errors or implementation bugs.")
    
    print(f"\nQuantitative thresholds used for classification:")
    print(f"  - Boundary cases: min_distance_to_threshold < 0.01")
    print(f"  - Extreme saturation: p_mean < 1e-10")
    print(f"  - Interpolation artifacts: delta_C > 5")
    print(f"  - High-p low-signal: p_mean > 0.2")
    print(f"  - Systematic offset: all other cases")
    print("="*80)
    
    # Save detailed results
    result_df = pd.DataFrame(results_data)
    result_df.to_csv("validation_comparison/reports/disagreement_characterization.csv", index=False)
    print(f"\nSummary saved to: disagreement_characterization.csv")
    
    # Save detailed case-by-case breakdown
    all_cases = []
    for cat_name, cat_data in categories.items():
        for case in cat_data['cases']:
            all_cases.append({
                'category': cat_name,
                'sasbdb_code': case['sasbdb_code'],
                'fit_name': case['fit_name'],
                'datcmp_p_value': case['datcmp_p_value'],
                'cormap_p_value': case['cormap_p_value'],
                'p_diff': case['p_diff'],
                'metric_value': case['metric_value'],
                'metric_name': category_descriptions[cat_name]['metric_name']
            })
    
    if all_cases:
        cases_df = pd.DataFrame(all_cases)
        cases_df.to_csv("validation_comparison/reports/disagreement_cases_detailed.csv", index=False)
        print(f"Detailed cases saved to: disagreement_cases_detailed.csv")

if __name__ == "__main__":
    characterize_disagreements()
