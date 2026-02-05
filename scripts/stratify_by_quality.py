#!/usr/bin/env python3
"""
Stratify agreement by data quality
"""

import pandas as pd
import numpy as np

def stratify_by_quality():
    classified = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_classified.csv")
    
    # Filter only cases where both succeeded
    both_valid = classified['datcmp_p_value'].notna() & classified['cormap_p_value'].notna()
    valid_data = classified[both_valid].copy()
    
    if len(valid_data) == 0:
        print("No valid data for stratification")
        return
    
    # Calculate difference
    valid_data['p_diff'] = abs(valid_data['datcmp_p_value'] - valid_data['cormap_p_value'])
    
    # Stratify
    quality_groups = {
        'good_quality_fit': valid_data[valid_data['classification'] == 'good_quality_fit'],
        'moderate_quality_fit': valid_data[valid_data['classification'] == 'moderate_quality_fit'],
        'poor_quality_fit': valid_data[valid_data['classification'] == 'poor_quality_fit']
    }
    
    print("="*80)
    print("AGREEMENT STRATIFIED BY DATA QUALITY")
    print("="*80)
    print(f"\n{'Quality':<20} {'N':<5} {'Agreement (0.05)':<20} {'Agreement (0.10)':<20}")
    print("-"*80)
    
    results = []
    
    for quality, group in quality_groups.items():
        if len(group) > 0:
            within_005 = (group['p_diff'] <= 0.05).sum()
            within_010 = (group['p_diff'] <= 0.10).sum()
            pct_005 = (within_005 / len(group)) * 100
            pct_010 = (within_010 / len(group)) * 100
            
            quality_label = quality.replace('_', ' ').title()
            print(f"{quality_label:<20} {len(group):<5} {within_005}/{len(group)} ({pct_005:.1f}%){'':<8} {within_010}/{len(group)} ({pct_010:.1f}%)")
            
            results.append({
                'quality': quality_label,
                'n': len(group),
                'agreement_0.05': f"{pct_005:.1f}%",
                'agreement_0.10': f"{pct_010:.1f}%",
                'mean_diff': group['p_diff'].mean()
            })
    
    # Save
    df_results = pd.DataFrame(results)
    df_results.to_csv("validation_comparison/reports/quality_stratified_agreement.csv", index=False)
    
    print("\n" + "="*80)
    print("Stratified results saved to: quality_stratified_agreement.csv")
    print("="*80)

if __name__ == "__main__":
    stratify_by_quality()
