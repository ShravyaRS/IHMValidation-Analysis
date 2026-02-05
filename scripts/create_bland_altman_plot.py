#!/usr/bin/env python3
"""
Create Bland-Altman plot - gold standard for method comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from pathlib import Path

def bland_altman_plot(datcmp, cormap, output_file):
    """Create Bland-Altman plot"""
    
    # Remove NaN values
    valid = ~(np.isnan(datcmp) | np.isnan(cormap))
    datcmp = datcmp[valid]
    cormap = cormap[valid]
    
    if len(datcmp) == 0:
        print("No valid data for Bland-Altman plot")
        return
    
    # Calculate mean and difference
    mean = (datcmp + cormap) / 2
    diff = datcmp - cormap
    
    # Calculate statistics
    mean_diff = np.mean(diff)
    std_diff = np.std(diff)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scatter plot
    ax.scatter(mean, diff, s=100, alpha=0.6, edgecolors='black', linewidth=1.5)
    
    # Mean line
    ax.axhline(mean_diff, color='red', linestyle='-', linewidth=2, 
               label=f'Mean difference: {mean_diff:.6f}')
    
    # Limits of agreement (±1.96 SD)
    ax.axhline(mean_diff + 1.96*std_diff, color='red', linestyle='--', linewidth=2,
               label=f'+1.96 SD: {mean_diff + 1.96*std_diff:.6f}')
    ax.axhline(mean_diff - 1.96*std_diff, color='red', linestyle='--', linewidth=2,
               label=f'-1.96 SD: {mean_diff - 1.96*std_diff:.6f}')
    
    # Zero line
    ax.axhline(0, color='black', linestyle=':', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('Mean of DATCMP and CorMap p-values', fontsize=14, fontweight='bold')
    ax.set_ylabel('Difference (DATCMP - CorMap)', fontsize=14, fontweight='bold')
    ax.set_title('Bland-Altman Plot: DATCMP vs Python CorMap', fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Add statistics text
    textstr = f'n = {len(datcmp)}\nMean bias = {mean_diff:.6f}\nSD = {std_diff:.6f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return mean_diff, std_diff

if __name__ == "__main__":
    comparison = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")
    
    output_file = "validation_comparison/plots/bland_altman_plot.png"
    
    mean_bias, std_diff = bland_altman_plot(
        comparison['datcmp_p_value'].values,
        comparison['cormap_p_value'].values,
        output_file
    )
    
    print("="*80)
    print("BLAND-ALTMAN ANALYSIS")
    print("="*80)
    print(f"Mean bias: {mean_bias:.6f}")
    print(f"Standard deviation: {std_diff:.6f}")
    print(f"95% limits of agreement: [{mean_bias - 1.96*std_diff:.6f}, {mean_bias + 1.96*std_diff:.6f}]")
    print(f"\nPlot saved to: {output_file}")
    print("="*80)
