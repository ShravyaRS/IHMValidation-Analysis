#!/usr/bin/env python3
"""
Calculate bootstrap confidence intervals for agreement percentages
"""

import pandas as pd
import numpy as np
from scipy import stats

def bootstrap_ci(data, n_bootstrap=10000, alpha=0.05):
    """
    Calculate bootstrap confidence interval
    """
    bootstrap_means = []
    n = len(data)
    
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        bootstrap_means.append(np.mean(sample))
    
    lower = np.percentile(bootstrap_means, (alpha/2) * 100)
    upper = np.percentile(bootstrap_means, (1 - alpha/2) * 100)
    mean = np.mean(data)
    
    return mean, lower, upper

def calculate_agreement_ci():
    """
    Calculate confidence intervals for agreement percentages
    """
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    # Get valid comparisons
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_data = comparison[both_valid].copy()
    
    if len(valid_data) == 0:
        print("No valid data")
        return
    
    valid_data['p_diff'] = abs(valid_data['datcmp_p_value'] - valid_data['cormap_p_value'])
    
    print("="*80)
    print("CONFIDENCE INTERVALS (95% Bootstrap)")
    print("="*80)
    print(f"Sample size: {len(valid_data)}")
    print()
    
    results = []
    
    for tolerance in [0.001, 0.01, 0.05, 0.1]:
        # Binary indicator: within tolerance or not
        within = (valid_data['p_diff'] <= tolerance).astype(int).values
        
        # Bootstrap
        mean_pct, lower_pct, upper_pct = bootstrap_ci(within * 100, n_bootstrap=10000)
        margin = (upper_pct - lower_pct) / 2
        
        print(f"Within {tolerance} tolerance:")
        print(f"  Agreement: {mean_pct:.1f}% ± {margin:.1f}% (95% CI: [{lower_pct:.1f}%, {upper_pct:.1f}%])")
        
        results.append({
            'tolerance': tolerance,
            'agreement_pct': mean_pct,
            'ci_lower': lower_pct,
            'ci_upper': upper_pct,
            'margin': margin
        })
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv("validation_comparison/reports/confidence_intervals.csv", index=False)
    
    print(f"\n{'='*80}")
    print("Results saved to: confidence_intervals.csv")
    print("="*80)

if __name__ == "__main__":
    np.random.seed(42)  # Reproducibility
    calculate_agreement_ci()
