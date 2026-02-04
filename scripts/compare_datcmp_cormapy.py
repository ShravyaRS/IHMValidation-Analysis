#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

def compare_results():
    """
    Compare DATCMP and cormapy results
    """
    datcmp_file = "validation_comparison/datcmp_results/datcmp_results.csv"
    cormapy_file = "validation_comparison/cormapy_results/cormapy_results.csv"
    
    print(f"Loading DATCMP results from: {datcmp_file}")
    print(f"Loading Cormapy results from: {cormapy_file}")
    
    if not Path(datcmp_file).exists():
        print(f"ERROR: {datcmp_file} not found.")
        return None
    
    if not Path(cormapy_file).exists():
        print(f"ERROR: {cormapy_file} not found.")
        return None
    
    datcmp_df = pd.read_csv(datcmp_file)
    cormapy_df = pd.read_csv(cormapy_file)
    
    print(f"\nDATCMP entries: {len(datcmp_df)}")
    print(f"Cormapy entries: {len(cormapy_df)}")
    
    # Merge datasets
    comparison = pd.merge(
        datcmp_df[['file_id', 'datcmp_c_value', 'datcmp_p_value', 'datcmp_adj_p_value']],
        cormapy_df[['file_id', 'cormapy_correlation', 'cormapy_p_value', 'cormapy_chi_squared']],
        on='file_id',
        how='inner'
    )
    
    print(f"\nMerged entries: {len(comparison)}")
    
    if len(comparison) == 0:
        print("ERROR: No data after merge!")
        return None
    
    # Calculate differences
    comparison['p_value_diff'] = abs(comparison['datcmp_p_value'] - comparison['cormapy_p_value'])
    
    # Avoid division by zero
    comparison['p_value_rel_diff'] = 0.0
    mask = comparison['datcmp_p_value'] != 0
    if mask.any():
        comparison.loc[mask, 'p_value_rel_diff'] = (
            comparison.loc[mask, 'p_value_diff'] / comparison.loc[mask, 'datcmp_p_value'].abs()
        ) * 100
    
    # Print summary
    print("\n" + "="*80)
    print("COMPARISON SUMMARY: DATCMP vs Cormapy")
    print("="*80)
    print(f"\nDatasets compared: {len(comparison)}")
    
    print(f"\nDATCMP P-values:")
    print(f"  Min: {comparison['datcmp_p_value'].min():.6f}")
    print(f"  Max: {comparison['datcmp_p_value'].max():.6f}")
    print(f"  Mean: {comparison['datcmp_p_value'].mean():.6f}")
    
    print(f"\nCormapy P-values:")
    print(f"  Min: {comparison['cormapy_p_value'].min():.6f}")
    print(f"  Max: {comparison['cormapy_p_value'].max():.6f}")
    print(f"  Mean: {comparison['cormapy_p_value'].mean():.6f}")
    
    print(f"\nCormapy Correlations:")
    print(f"  Min: {comparison['cormapy_correlation'].min():.6f}")
    print(f"  Max: {comparison['cormapy_correlation'].max():.6f}")
    print(f"  Mean: {comparison['cormapy_correlation'].mean():.6f}")
    
    print(f"\nP-value Differences:")
    print(f"  Mean abs diff: {comparison['p_value_diff'].mean():.6f}")
    print(f"  Max abs diff: {comparison['p_value_diff'].max():.6f}")
    print(f"  Std dev: {comparison['p_value_diff'].std():.6f}")
    
    # Tolerance checks
    for tolerance in [0.001, 0.01, 0.05, 0.1]:
        within = (comparison['p_value_diff'] <= tolerance).sum()
        pct = (within / len(comparison)) * 100
        print(f"  Within {tolerance}: {within}/{len(comparison)} ({pct:.1f}%)")
    
    # Save comparison table
    output_file = "validation_comparison/reports/comparison_table.csv"
    os.makedirs(Path(output_file).parent, exist_ok=True)
    comparison.to_csv(output_file, index=False)
    print(f"\nSaved to: {output_file}")
    
    # Display full table
    print("\n" + "="*80)
    print("DETAILED COMPARISON TABLE")
    print("="*80)
    print(comparison.to_string(index=False))
    
    return comparison

def create_plots(comparison):
    """
    Create visualization plots
    """
    if comparison is None or len(comparison) == 0:
        print("No data to plot")
        return
    
    print("\nCreating plots...")
    
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Scatter DATCMP vs Cormapy p-values
    ax1 = axes[0, 0]
    ax1.scatter(comparison['datcmp_p_value'], comparison['cormapy_p_value'], 
                s=120, alpha=0.7, edgecolors='black', linewidth=1.5)
    
    all_p = pd.concat([comparison['datcmp_p_value'], comparison['cormapy_p_value']])
    lims = [all_p.min() - 0.01, all_p.max() + 0.01]
    ax1.plot(lims, lims, 'r--', linewidth=2, label='Perfect agreement')
    
    ax1.set_xlabel('DATCMP p-value', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cormapy p-value', fontsize=12, fontweight='bold')
    ax1.set_title('DATCMP vs Cormapy P-values', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Correlation values
    ax2 = axes[0, 1]
    x = np.arange(len(comparison))
    ax2.bar(x, comparison['cormapy_correlation'], alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Dataset Index', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Correlation', fontsize=12, fontweight='bold')
    ax2.set_title('Cormapy Correlation Coefficients', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: P-value differences
    ax3 = axes[1, 0]
    ax3.bar(x, comparison['p_value_diff'], alpha=0.7, edgecolor='black', color='coral')
    ax3.set_xlabel('Dataset Index', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Absolute Difference', fontsize=12, fontweight='bold')
    ax3.set_title('P-value Differences (|DATCMP - Cormapy|)', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Side-by-side comparison
    ax4 = axes[1, 1]
    width = 0.35
    ax4.bar(x - width/2, comparison['datcmp_p_value'], width, label='DATCMP', alpha=0.8, edgecolor='black')
    ax4.bar(x + width/2, comparison['cormapy_p_value'], width, label='Cormapy', alpha=0.8, edgecolor='black')
    ax4.set_xlabel('Dataset Index', fontsize=12, fontweight='bold')
    ax4.set_ylabel('P-value', fontsize=12, fontweight='bold')
    ax4.set_title('P-values by Dataset', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    plot_file = "validation_comparison/plots/comparison_plots.png"
    os.makedirs(Path(plot_file).parent, exist_ok=True)
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Plots saved to: {plot_file}")
    
    plt.close()

if __name__ == "__main__":
    print("="*80)
    print("DATCMP vs CORMAPY COMPARISON")
    print("="*80)
    
    comparison = compare_results()
    
    if comparison is not None:
        create_plots(comparison)
        print("\n" + "="*80)
        print("COMPARISON COMPLETE")
        print("="*80)
    else:
        print("\nComparison failed!")
