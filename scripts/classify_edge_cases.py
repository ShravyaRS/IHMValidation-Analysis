#!/usr/bin/env python3

import pandas as pd
import numpy as np
from pathlib import Path

def classify_case(row):
    """Classify validation case by type and quality"""
    datcmp_valid = pd.notna(row['datcmp_p_value'])
    cormap_valid = pd.notna(row['cormap_p_value'])
    
    if not datcmp_valid and not cormap_valid:
        # Both undefined - determine reason
        n_points = row.get('cormap_n_points', 0)
        if n_points == 0:
            return "insufficient_overlap"
        else:
            return "zero_error_case"
    elif datcmp_valid and cormap_valid:
        # Both succeeded - classify by fit quality
        p_avg = (row['datcmp_p_value'] + row['cormap_p_value']) / 2
        if p_avg >= 0.05:
            return "good_quality_fit"
        elif p_avg >= 0.01:
            return "moderate_quality_fit"
        else:
            return "poor_quality_fit"
    else:
        # Disagreement (one succeeded, one failed)
        return "disagreement"

if __name__ == "__main__":
    comparison_file = "validation_comparison/reports/datcmp_vs_cormap_comparison.csv"
    output_file = "validation_comparison/reports/datcmp_vs_cormap_classified.csv"
    
    print("="*80)
    print("CLASSIFYING VALIDATION CASES")
    print("="*80)
    
    # Load comparison data
    comparison = pd.read_csv(comparison_file)
    
    # Apply classification
    comparison['classification'] = comparison.apply(classify_case, axis=1)
    
    # Save enhanced version
    comparison.to_csv(output_file, index=False)
    
    # Print summary
    print("\nClassification Summary:")
    print("-"*80)
    class_counts = comparison['classification'].value_counts()
    for class_name, count in class_counts.items():
        pct = (count / len(comparison)) * 100
        print(f"  {class_name:25s}: {count:3d}/{len(comparison)} ({pct:5.1f}%)")
    
    print("\n" + "="*80)
    print(f"Classified data saved to: {output_file}")
    print("="*80)
    
    # Detailed breakdown
    print("\nDetailed Breakdown by Category:")
    print("-"*80)
    
    for class_name in class_counts.index:
        print(f"\n{class_name.upper().replace('_', ' ')}:")
        subset = comparison[comparison['classification'] == class_name]
        for idx, row in subset.iterrows():
            print(f"  - {row['sasbdb_code']} ({row['fit_name']})")
