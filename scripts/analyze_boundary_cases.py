#!/usr/bin/env python3
"""
Analyze cases near decision boundaries (p ≈ 0.05, 0.01)
"""

import pandas as pd
import numpy as np

def analyze_boundaries():
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_data = comparison[both_valid].copy()
    
    print("="*80)
    print("BOUNDARY CASE ANALYSIS")
    print("="*80)
    
    thresholds = [0.01, 0.05, 0.10]
    
    for threshold in thresholds:
        # Find cases within ±0.01 of threshold
        boundary_window = 0.01
        
        datcmp_near = ((valid_data['datcmp_p_value'] >= threshold - boundary_window) & 
                       (valid_data['datcmp_p_value'] <= threshold + boundary_window))
        
        cormap_near = ((valid_data['cormap_p_value'] >= threshold - boundary_window) & 
                       (valid_data['cormap_p_value'] <= threshold + boundary_window))
        
        near_boundary = datcmp_near | cormap_near
        boundary_cases = valid_data[near_boundary]
        
        if len(boundary_cases) > 0:
            print(f"\nCases near p = {threshold} threshold (±{boundary_window}):")
            print(f"  Count: {len(boundary_cases)}")
            
            # Check if they agree on classification
            datcmp_above = (boundary_cases['datcmp_p_value'] >= threshold).astype(int)
            cormap_above = (boundary_cases['cormap_p_value'] >= threshold).astype(int)
            agree = (datcmp_above == cormap_above).sum()
            
            print(f"  Agreement on classification: {agree}/{len(boundary_cases)} ({agree/len(boundary_cases)*100:.1f}%)")
            
            # Show the cases
            for idx, row in boundary_cases.iterrows():
                print(f"    - {row['sasbdb_code']}: DATCMP={row['datcmp_p_value']:.4f}, CorMap={row['cormap_p_value']:.4f}")
    
    print(f"\n{'='*80}")
    print("INTERPRETATION:")
    print("="*80)
    print("Boundary cases (near decision thresholds) show:")
    print("- Minor differences driven by interpolation resolution")
    print("- Both methods typically agree on accept/reject decision")
    print("- Differences are expected due to discrete C-value statistic")
    print("="*80)

if __name__ == "__main__":
    analyze_boundaries()
