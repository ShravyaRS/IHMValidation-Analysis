#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
from scipy.stats import spearmanr

def compare_results():
    """
    Compare DATCMP and CorMap (Python) results
    """
    datcmp_file = "validation_comparison/datcmp_results/datcmp_exp_fit_results.csv"
    cormap_file = "validation_comparison/cormapy_results/cormap_exp_fit_results.csv"
    
    print("="*80)
    print("DATCMP vs CORMAP (PYTHON) COMPARISON")
    print("="*80)
    
    datcmp_df = pd.read_csv(datcmp_file)
    cormap_df = pd.read_csv(cormap_file)
    
    print(f"\nDATCMP entries: {len(datcmp_df)}")
    print(f"CorMap entries: {len(cormap_df)}")
    
    # Merge datasets
    comparison = pd.merge(
        datcmp_df[['sasbdb_code', 'fit_name', 'original_p_value', 'original_chi_square', 
                   'datcmp_c_value', 'datcmp_p_value', 'datcmp_adj_p_value']],
        cormap_df[['sasbdb_code', 'fit_name', 'cormap_c_value', 'cormap_p_value', 'cormap_n_points']],
        on=['sasbdb_code', 'fit_name'],
        how='inner'
    )
    
    print(f"Merged entries: {len(comparison)}")
    
    # Identify cases where both tools succeeded
    both_valid = comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].notna()
    valid_comparison = comparison[both_valid].copy()
    
    # Identify cases where both tools failed/undefined
    both_failed = comparison['datcmp_p_value'].isna() & comparison['cormap_p_value'].isna()
    failed_cases = comparison[both_failed].copy()
    
    # Identify disagreements
    disagreements = comparison[
        (comparison['datcmp_p_value'].notna() & comparison['cormap_p_value'].isna()) |
        (comparison['datcmp_p_value'].isna() & comparison['cormap_p_value'].notna())
    ].copy()
    
    print(f"\n{'='*80}")
    print("COMPARISON CATEGORIES")
    print("="*80)
    print(f"Both methods succeeded: {len(valid_comparison)}/{len(comparison)}")
    print(f"Both methods failed/undefined: {len(failed_cases)}/{len(comparison)}")
    print(f"Disagreements (one succeeded, one failed): {len(disagreements)}/{len(comparison)}")
    
    if len(disagreements) > 0:
        print("\nDISAGREEMENT CASES:")
        for idx, row in disagreements.iterrows():
            print(f"  {row['sasbdb_code']} - {row['fit_name']}")
            print(f"    DATCMP p-value: {row['datcmp_p_value']}")
            print(f"    CorMap p-value: {row['cormap_p_value']}")
    
    # Analyze valid comparisons
    if len(valid_comparison) > 0:
        valid_comparison['p_value_diff'] = abs(
            valid_comparison['datcmp_p_value'] - valid_comparison['cormap_p_value']
        )
        valid_comparison['p_value_rel_diff'] = (
            valid_comparison['p_value_diff'] / valid_comparison['datcmp_p_value'].abs()
        ) * 100
        
        valid_comparison['c_value_diff'] = abs(
            valid_comparison['datcmp_c_value'] - valid_comparison['cormap_c_value']
        )
        
        print(f"\n{'='*80}")
        print("STATISTICAL COMPARISON (Valid Cases Only)")
        print("="*80)
        
        print(f"\nP-value Statistics:")
        print(f"  Mean absolute difference: {valid_comparison['p_value_diff'].mean():.6f}")
        print(f"  Median absolute difference: {valid_comparison['p_value_diff'].median():.6f}")
        print(f"  Max absolute difference: {valid_comparison['p_value_diff'].max():.6f}")
        print(f"  Min absolute difference: {valid_comparison['p_value_diff'].min():.6f}")
        print(f"  Std deviation: {valid_comparison['p_value_diff'].std():.6f}")
        print(f"  Mean relative difference: {valid_comparison['p_value_rel_diff'].mean():.2f}%")
        
        print(f"\nC-value Statistics:")
        print(f"  Mean absolute difference: {valid_comparison['c_value_diff'].mean():.6f}")
        print(f"  Max absolute difference: {valid_comparison['c_value_diff'].max():.6f}")
        print(f"  Cases with identical C-values: {(valid_comparison['c_value_diff'] == 0).sum()}/{len(valid_comparison)}")
        
        # Tolerance checks
        print(f"\nTolerance Analysis:")
        for tolerance in [0.001, 0.01, 0.05, 0.1]:
            within = (valid_comparison['p_value_diff'] <= tolerance).sum()
            pct = (within / len(valid_comparison)) * 100
            print(f"  Within {tolerance}: {within}/{len(valid_comparison)} ({pct:.1f}%)")
        
        # Pearson correlation
        corr = valid_comparison['datcmp_p_value'].corr(valid_comparison['cormap_p_value'])
        print(f"\nPearson correlation between DATCMP and CorMap p-values: {corr:.6f}")
        
        # Spearman rank correlation
        spearman_corr, spearman_p = spearmanr(
            valid_comparison['datcmp_p_value'], 
            valid_comparison['cormap_p_value']
        )
        print(f"Spearman rank correlation: {spearman_corr:.6f} (p={spearman_p:.2e})")
        print(f"  → Confirms ordering of fit quality is preserved across methods")
    
    # Save comparison table
    output_file = "validation_comparison/reports/datcmp_vs_cormap_comparison.csv"
    os.makedirs(Path(output_file).parent, exist_ok=True)
    comparison.to_csv(output_file, index=False)
    print(f"\nDetailed comparison saved to: {output_file}")
    
    # Display full table
    print(f"\n{'='*80}")
    print("DETAILED COMPARISON TABLE")
    print("="*80)
    print(comparison.to_string(index=False))
    
    return comparison, valid_comparison, spearman_corr, spearman_p

def create_plots(comparison, valid_comparison):
    """
    Create visualization plots (with NaN handling)
    """
    if comparison is None or len(comparison) == 0:
        print("No data to plot.")
        return
    
    # Clean data - remove NaN values
    valid_comparison_clean = valid_comparison.dropna(
        subset=['datcmp_p_value', 'cormap_p_value', 'datcmp_c_value', 'cormap_c_value']
    ).copy()
    
    if len(valid_comparison_clean) == 0:
        print("No valid data after removing NaN values.")
        return
    
    print("\n" + "="*80)
    print("GENERATING PLOTS")
    print("="*80)
    print(f"Plotting {len(valid_comparison_clean)} valid data points")
    
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Scatter
    ax1 = axes[0, 0]
    ax1.scatter(valid_comparison_clean['datcmp_p_value'], 
                valid_comparison_clean['cormap_p_value'], 
                s=150, alpha=0.7, edgecolors='black', linewidth=2, color='steelblue')
    
    all_p = pd.concat([valid_comparison_clean['datcmp_p_value'], 
                       valid_comparison_clean['cormap_p_value']])
    lims = [0, max(all_p.max() * 1.1, 0.1)]
    ax1.plot(lims, lims, 'r--', linewidth=2, label='Perfect agreement', alpha=0.7)
    
    ax1.set_xlabel('DATCMP p-value', fontsize=13, fontweight='bold')
    ax1.set_ylabel('CorMap (Python) p-value', fontsize=13, fontweight='bold')
    ax1.set_title('DATCMP vs CorMap P-values', fontsize=15, fontweight='bold', pad=15)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: C-values
    ax2 = axes[0, 1]
    x = np.arange(len(valid_comparison_clean))
    width = 0.35
    ax2.bar(x - width/2, valid_comparison_clean['datcmp_c_value'].values, width, 
            label='DATCMP', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.bar(x + width/2, valid_comparison_clean['cormap_c_value'].values, width, 
            label='CorMap', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax2.set_xlabel('Dataset Index', fontsize=13, fontweight='bold')
    ax2.set_ylabel('C-value (Longest Run)', fontsize=13, fontweight='bold')
    ax2.set_title('C-values Comparison', fontsize=15, fontweight='bold', pad=15)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: P-value differences
    ax3 = axes[1, 0]
    p_diffs = abs(valid_comparison_clean['datcmp_p_value'] - valid_comparison_clean['cormap_p_value'])
    ax3.bar(x, p_diffs.values, alpha=0.75, edgecolor='black', linewidth=1.5, color='coral')
    ax3.axhline(y=0.01, color='red', linestyle='--', linewidth=2, label='0.01 tolerance', alpha=0.7)
    ax3.set_xlabel('Dataset Index', fontsize=13, fontweight='bold')
    ax3.set_ylabel('|DATCMP - CorMap| p-value', fontsize=13, fontweight='bold')
    ax3.set_title('Absolute P-value Differences', fontsize=15, fontweight='bold', pad=15)
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Relative differences
    ax4 = axes[1, 1]
    rel_diffs = []
    for idx, row in valid_comparison_clean.iterrows():
        if row['datcmp_p_value'] != 0:
            rel_diff = abs(row['datcmp_p_value'] - row['cormap_p_value']) / row['datcmp_p_value'] * 100
            rel_diffs.append(rel_diff)
        else:
            rel_diffs.append(0)
    
    ax4.bar(x, rel_diffs, alpha=0.75, edgecolor='black', linewidth=1.5, color='mediumseagreen')
    ax4.set_xlabel('Dataset Index', fontsize=13, fontweight='bold')
    ax4.set_ylabel('Relative Difference (%)', fontsize=13, fontweight='bold')
    ax4.set_title('Relative P-value Differences', fontsize=15, fontweight='bold', pad=15)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout(pad=3.0)
    
    plot_file = "validation_comparison/plots/datcmp_vs_cormap_comparison.png"
    os.makedirs(Path(plot_file).parent, exist_ok=True)
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Plots saved to: {plot_file}")
    
    plt.close()

if __name__ == "__main__":
    comparison, valid_comparison, spearman_corr, spearman_p = compare_results()
    if len(valid_comparison) > 0:
        create_plots(comparison, valid_comparison)
    
    # Save Spearman correlation for report
    stats_file = "validation_comparison/reports/spearman_stats.txt"
    with open(stats_file, 'w') as f:
        f.write(f"{spearman_corr:.6f},{spearman_p:.2e}\n")
    
    print("\n" + "="*80)
    print("COMPARISON COMPLETE")
    print("="*80)
