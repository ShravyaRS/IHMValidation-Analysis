#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
import os

def generate_report():
    """
    Generate professional report for Arthur
    """
    # Load comparison data
    comparison_file = "validation_comparison/reports/comparison_table.csv"
    
    if not Path(comparison_file).exists():
        print(f"ERROR: {comparison_file} not found. Run compare_datcmp_cormapy.py first.")
        return
    
    comparison = pd.read_csv(comparison_file)
    
    report = []
    report.append("="*80)
    report.append("DATCMP vs CORMAPY VALIDATION REPORT")
    report.append("="*80)
    report.append(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Author: IHM Validation Analysis Team")
    report.append(f"Project: IHMValidation-Analysis")
    report.append(f"Location: ~/projects/IHMValidation-Analysis/IHMValidation")
    
    report.append(f"\n{'='*80}")
    report.append("EXECUTIVE SUMMARY")
    report.append("="*80)
    
    # Calculate key metrics
    n_datasets = len(comparison)
    mean_diff = comparison['p_value_diff'].mean()
    median_diff = comparison['p_value_diff'].median()
    max_diff = comparison['p_value_diff'].max()
    min_diff = comparison['p_value_diff'].min()
    std_diff = comparison['p_value_diff'].std()
    
    report.append(f"\nObjective:")
    report.append(f"  Verify if cormapy can replace DATCMP for SAS validation")
    report.append(f"\nDatasets Analyzed: {n_datasets}")
    report.append(f"Source: PDB-Dev SASBDB entries")
    report.append(f"Data Location: Validation/cache/")
    
    report.append(f"\n{'='*80}")
    report.append("STATISTICAL RESULTS")
    report.append("="*80)
    report.append(f"\nP-value Comparison:")
    report.append(f"  Mean Absolute Difference:     {mean_diff:.8f}")
    report.append(f"  Median Absolute Difference:   {median_diff:.8f}")
    report.append(f"  Maximum Difference:           {max_diff:.8f}")
    report.append(f"  Minimum Difference:           {min_diff:.8f}")
    report.append(f"  Standard Deviation:           {std_diff:.8f}")
    
    report.append(f"\nAgreement Analysis:")
    
    # Tolerance checks
    tolerances = [0.001, 0.01, 0.05, 0.1]
    for tolerance in tolerances:
        within = (comparison['p_value_diff'] <= tolerance).sum()
        pct = (within / n_datasets) * 100
        report.append(f"  Within {tolerance:6.3f} tolerance: {within:2d}/{n_datasets} ({pct:5.1f}%)")
    
    # Correlation analysis
    from scipy import stats as sp_stats
    if 'cormapy_correlation' in comparison.columns:
        mean_corr = comparison['cormapy_correlation'].mean()
        report.append(f"\nCorrelation Metrics:")
        report.append(f"  Mean Correlation Coefficient: {mean_corr:.6f}")
    
    # Recommendation logic
    report.append(f"\n{'='*80}")
    report.append("RECOMMENDATION")
    report.append("="*80)
    
    # Determine tolerance for recommendation
    tolerance_95 = (comparison['p_value_diff'] <= 0.01).sum() / n_datasets * 100
    tolerance_90 = (comparison['p_value_diff'] <= 0.05).sum() / n_datasets * 100
    
    if tolerance_95 >= 95:
        recommendation = "YES - Cormapy can replace DATCMP"
        justification = f"Cormapy shows excellent agreement with DATCMP ({tolerance_95:.1f}% within 0.01 tolerance). The statistical differences are minimal and within acceptable limits for scientific validation."
    elif tolerance_90 >= 90:
        recommendation = "CONDITIONAL YES - Cormapy can replace DATCMP with minor caveats"
        justification = f"Cormapy shows good agreement with DATCMP ({tolerance_90:.1f}% within 0.05 tolerance). Minor discrepancies exist but are acceptable for most validation purposes. Additional verification recommended for critical cases."
    elif tolerance_90 >= 75:
        recommendation = "PARTIAL - Cormapy can supplement DATCMP"
        justification = f"Cormapy shows moderate agreement with DATCMP ({tolerance_90:.1f}% within 0.05 tolerance). Recommend using cormapy for preliminary screening with DATCMP verification for final validation."
    else:
        recommendation = "NO - Further investigation required"
        justification = f"Cormapy shows limited agreement with DATCMP ({tolerance_90:.1f}% within 0.05 tolerance). Significant refinement and additional validation needed before replacement can be considered."
    
    report.append(f"\n{recommendation}")
    report.append(f"\nJustification:")
    report.append(f"  {justification}")
    
    # Technical notes
    report.append(f"\n{'='*80}")
    report.append("TECHNICAL NOTES")
    report.append("="*80)
    report.append(f"\nMethodology:")
    report.append(f"  1. Extracted SAS data from {n_datasets} .sascif files")
    report.append(f"  2. Ran DATCMP using Singularity container (ATSAS suite)")
    report.append(f"  3. Ran cormapy using Pearson correlation method")
    report.append(f"  4. Compared p-values from both methods")
    report.append(f"\nLimitations:")
    report.append(f"  - Self-comparison test (experimental vs experimental)")
    report.append(f"  - Limited dataset size (n={n_datasets})")
    report.append(f"  - Additional validation with theoretical data recommended")
    
    # Detailed table
    report.append(f"\n{'='*80}")
    report.append("DETAILED COMPARISON TABLE")
    report.append("="*80)
    report.append("\n" + comparison.to_string(index=False))
    
    # Next steps
    report.append(f"\n{'='*80}")
    report.append("RECOMMENDED NEXT STEPS")
    report.append("="*80)
    report.append(f"\n1. Expand validation to more PDB-Dev entries (target: 50-100 datasets)")
    report.append(f"2. Test with experimental vs theoretical data comparisons")
    report.append(f"3. Validate across different q-ranges and data qualities")
    report.append(f"4. Benchmark computational performance (DATCMP vs cormapy)")
    report.append(f"5. Conduct peer review of methodology and results")
    
    # Save report
    report_text = "\n".join(report)
    
    # Save as text file
    report_file = "validation_comparison/reports/VALIDATION_REPORT.txt"
    os.makedirs(Path(report_file).parent, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(report_text)
    
    # Save as markdown
    md_file = "validation_comparison/reports/VALIDATION_REPORT.md"
    with open(md_file, 'w') as f:
        f.write("```\n")
        f.write(report_text)
        f.write("\n```\n")
    
    # Print to console
    print(report_text)
    
    print(f"\n{'='*80}")
    print(f"REPORT FILES GENERATED")
    print(f"{'='*80}")
    print(f"  Text Report:  {report_file}")
    print(f"  Markdown:     {md_file}")
    print(f"  Comparison:   validation_comparison/reports/comparison_table.csv")
    print(f"  Plots:        validation_comparison/plots/comparison_plots.png")
    print(f"{'='*80}")

if __name__ == "__main__":
    generate_report()
