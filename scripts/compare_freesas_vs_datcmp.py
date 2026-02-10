#!/usr/bin/env python3
"""
Compare freesas cormap results against DATCMP
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load results
freesas = pd.read_csv("validation_comparison/reports/cormap_freesas_results.csv")
datcmp  = pd.read_csv("validation_comparison/reports/datcmp_vs_cormap_comparison.csv")

print("="*80)
print("FREESAS CORMAP vs DATCMP COMPARISON")
print("="*80)

# Merge on sasbdb_code and fit_name
merged = pd.merge(
    freesas[['sasbdb_code', 'fit_name', 'cormap_p_value', 'cormap_c_value', 'n_points', 'status']],
    datcmp[['sasbdb_code', 'fit_name', 'datcmp_p_value', 'datcmp_c_value']],
    on=['sasbdb_code', 'fit_name'],
    how='inner'
)

print(f"\nTotal pairs: {len(merged)}")

# Valid comparisons (both succeeded)
both_valid = merged['cormap_p_value'].notna() & merged['datcmp_p_value'].notna()
valid = merged[both_valid].copy()

print(f"Both succeeded: {len(valid)}")

# Calculate differences
valid['p_diff']   = abs(valid['cormap_p_value'] - valid['datcmp_p_value'])
valid['c_diff']   = abs(valid['cormap_c_value']  - valid['datcmp_c_value'])
valid['p_ratio']  = valid[['cormap_p_value', 'datcmp_p_value']].max(axis=1) / \
                    valid[['cormap_p_value', 'datcmp_p_value']].min(axis=1).replace(0, np.nan)

print(f"\n{'='*80}")
print("P-VALUE AGREEMENT")
print("="*80)

for tol in [0.001, 0.01, 0.05, 0.10]:
    within = (valid['p_diff'] <= tol).sum()
    pct    = within / len(valid) * 100
    print(f"Within {tol}: {within}/{len(valid)} ({pct:.1f}%)")

print(f"\n{'='*80}")
print("C-VALUE AGREEMENT")
print("="*80)

c_exact = (valid['c_diff'] == 0).sum()
print(f"Exact C match: {c_exact}/{len(valid)} ({c_exact/len(valid)*100:.1f}%)")

print(f"\n{'='*80}")
print("STATISTICAL SUMMARY")
print("="*80)
print(f"Mean p-value difference:   {valid['p_diff'].mean():.6f}")
print(f"Median p-value difference: {valid['p_diff'].median():.6f}")
print(f"Max p-value difference:    {valid['p_diff'].max():.6f}")
print(f"Mean C-value difference:   {valid['c_diff'].mean():.4f}")

# Pearson correlation
from scipy import stats
valid_nonzero = valid[valid['datcmp_p_value'] > 0]
if len(valid_nonzero) > 2:
    pearson_r, pearson_p = stats.pearsonr(
        valid_nonzero['datcmp_p_value'],
        valid_nonzero['cormap_p_value']
    )
    spearman_r, spearman_p = stats.spearmanr(
        valid['datcmp_p_value'],
        valid['cormap_p_value']
    )
    print(f"Pearson r:                 {pearson_r:.6f}")
    print(f"Spearman rho:              {spearman_r:.6f}")

print(f"\n{'='*80}")
print("PER-CASE RESULTS")
print("="*80)
print(f"\n{'SASBDB Code':<15} {'Fit':<12} {'DATCMP p':<12} {'FreeSAS p':<12} {'Diff':<10} {'C match'}")
print("-"*80)
for _, row in valid.iterrows():
    c_match = "YES" if row['c_diff'] == 0 else "NO"
    print(f"{row['sasbdb_code']:<15} {row['fit_name']:<12} "
          f"{row['datcmp_p_value']:<12.6f} {row['cormap_p_value']:<12.6f} "
          f"{row['p_diff']:<10.6f} {c_match}")

# Scatter plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

ax1 = axes[0]
ax1.scatter(valid['datcmp_p_value'], valid['cormap_p_value'],
            s=80, alpha=0.7, edgecolors='black', linewidth=1)
max_val = max(valid['datcmp_p_value'].max(), valid['cormap_p_value'].max())
ax1.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfect agreement')
ax1.set_xlabel('DATCMP p-value', fontsize=12)
ax1.set_ylabel('FreeSAS CorMap p-value', fontsize=12)
ax1.set_title('DATCMP vs FreeSAS CorMap', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[1]
diff = valid['cormap_p_value'] - valid['datcmp_p_value']
mean_p = (valid['cormap_p_value'] + valid['datcmp_p_value']) / 2
ax2.scatter(mean_p, diff, s=80, alpha=0.7, edgecolors='black', linewidth=1)
ax2.axhline(diff.mean(), color='red', linestyle='-', linewidth=2,
            label=f'Mean bias: {diff.mean():.6f}')
ax2.axhline(diff.mean() + 1.96*diff.std(), color='red', linestyle='--',
            linewidth=1.5, label=f'+1.96 SD: {diff.mean()+1.96*diff.std():.6f}')
ax2.axhline(diff.mean() - 1.96*diff.std(), color='red', linestyle='--',
            linewidth=1.5, label=f'-1.96 SD: {diff.mean()-1.96*diff.std():.6f}')
ax2.axhline(0, color='black', linestyle=':', linewidth=1, alpha=0.5)
ax2.set_xlabel('Mean of DATCMP and FreeSAS p-values', fontsize=12)
ax2.set_ylabel('Difference (FreeSAS - DATCMP)', fontsize=12)
ax2.set_title('Bland-Altman Plot: FreeSAS vs DATCMP', fontsize=14)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('validation_comparison/plots/freesas_vs_datcmp.png',
            dpi=300, bbox_inches='tight')
plt.close()

print(f"\n{'='*80}")
print("Plot saved: validation_comparison/plots/freesas_vs_datcmp.png")
print("="*80)

# Save merged results
valid.to_csv("validation_comparison/reports/freesas_vs_datcmp_comparison.csv", index=False)
print(f"Results saved: freesas_vs_datcmp_comparison.csv")
print("="*80)
