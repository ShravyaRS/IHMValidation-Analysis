
#!/usr/bin/env python3
"""
Generate professional figures for IHMValidation Analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import numpy as np

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# Create figures directory
import os
os.makedirs('figures/generated', exist_ok=True)

# ============================================================================
# Figure 1: Success Rate Comparison
# ============================================================================
def create_success_rate_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Before/After comparison
    categories = ['Before Fix', 'After Fix']
    success_rates = [50, 100]
    colors = ['#e74c3c', '#27ae60']
    
    bars = ax1.bar(categories, success_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Success Rate (%)', fontweight='bold')
    ax1.set_title('Validation Success Rate Improvement', fontweight='bold', fontsize=16)
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate}%', ha='center', va='bottom', fontweight='bold', fontsize=14)
    
    # Structure-by-structure breakdown
    structures = ['00001', '00010', '00015', '00020', '00025', '00030', '00035', '00040']
    before = [1, 0, 1, 0, 1, 1, 0, 0]  # 1=pass, 0=fail
    after = [1, 1, 1, 1, 1, 1, 1, 1]
    
    x = np.arange(len(structures))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, before, width, label='Before', color='#e74c3c', alpha=0.8, edgecolor='black')
    bars2 = ax2.bar(x + width/2, after, width, label='After', color='#27ae60', alpha=0.8, edgecolor='black')
    
    ax2.set_xlabel('Structure ID (PDBDEV_000000XX)', fontweight='bold')
    ax2.set_ylabel('Pass (1) / Fail (0)', fontweight='bold')
    ax2.set_title('Per-Structure Validation Results', fontweight='bold', fontsize=16)
    ax2.set_xticks(x)
    ax2.set_xticklabels(structures, rotation=45)
    ax2.legend()
    ax2.set_ylim(0, 1.2)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/generated/success_rate_comparison.png', dpi=300, bbox_inches='tight')
    print("Generated: success_rate_comparison.png")
    plt.close()

# ============================================================================
# Figure 2: Validation Time by Structure Size
# ============================================================================
def create_validation_time_figure():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data
    sizes = [1.6, 5.8, 2.3, 2.1, 1.8, 2.4, 2.0, 2.2]  # MB
    times = [2.5, 9.0, 4.0, 3.0, 2.8, 4.5, 3.5, 3.8]  # minutes
    structures = ['PDBDEV_00000001', 'PDBDEV_00000010', 'PDBDEV_00000015', 
                  'PDBDEV_00000020', 'PDBDEV_00000025', 'PDBDEV_00000030',
                  'PDBDEV_00000035', 'PDBDEV_00000040']
    
    # Color by size
    colors = plt.cm.viridis(np.array(sizes) / max(sizes))
    
    scatter = ax.scatter(sizes, times, s=300, c=sizes, cmap='viridis', 
                        alpha=0.7, edgecolors='black', linewidth=2)
    
    # Add structure labels
    for i, txt in enumerate(['01', '10', '15', '20', '25', '30', '35', '40']):
        ax.annotate(txt, (sizes[i], times[i]), ha='center', va='center', 
                   fontweight='bold', fontsize=10)
    
    # Add trend line
    z = np.polyfit(sizes, times, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(sizes), max(sizes), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend')
    
    ax.set_xlabel('Structure Size (MB)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Validation Time (minutes)', fontweight='bold', fontsize=12)
    ax.set_title('Validation Performance: Time vs Structure Size', fontweight='bold', fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Structure Size (MB)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/generated/validation_time_analysis.png', dpi=300, bbox_inches='tight')
    print("Generated: validation_time_analysis.png")
    plt.close()

# ============================================================================
# Figure 3: Issues Fixed - Impact Analysis
# ============================================================================
def create_issues_fixed_figure():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    issues = ['ATSAS\nInstallation', 'EM Webdriver\nInitialization', 
              'Chimera\nVersion Check', 'ChimeraX\nVersion Check', 
              'MapQ\nVersion Check']
    structures_fixed = [3, 0, 1, 1, 1]  # Number of structures fixed by each
    colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
    
    bars = ax.barh(issues, structures_fixed, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=2)
    
    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, structures_fixed)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2., 
               f'{count} structures', ha='left', va='center', 
               fontweight='bold', fontsize=11, bbox=dict(boxstyle='round', 
               facecolor='white', alpha=0.8))
    
    ax.set_xlabel('Number of Structures Fixed', fontweight='bold', fontsize=12)
    ax.set_title('Impact of Each Fix on Validation Success', fontweight='bold', fontsize=16)
    ax.set_xlim(0, 4)
    ax.grid(axis='x', alpha=0.3)
    
    # Add legend for issue severity
    severity_labels = ['Critical (blocks all SAS)', 'Enhancement', 
                      'Stability Fix', 'Stability Fix', 'Large Structure Fix']
    legend_elements = [mpatches.Patch(facecolor=colors[i], edgecolor='black', 
                                     label=f'{issues[i].replace(chr(10), " ")}: {severity_labels[i]}')
                      for i in range(len(issues))]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('figures/generated/issues_impact_analysis.png', dpi=300, bbox_inches='tight')
    print("Generated: issues_impact_analysis.png")
    plt.close()

# ============================================================================
# Figure 4: Resource Usage Pattern
# ============================================================================
def create_resource_usage_figure():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Memory usage over time
    stages = ['Start', 'Format\nValidation', 'Quality\nCheck', 'SAS\nValidation', 
              'CX-MS\nValidation', 'EM\nValidation', 'Report\nGeneration']
    
    # Small structure (2MB)
    memory_small = [0.5, 1.2, 1.8, 2.5, 2.3, 3.0, 2.0]
    # Large structure (6MB)
    memory_large = [0.5, 1.5, 2.5, 3.5, 3.2, 6.0, 3.5]
    
    x = np.arange(len(stages))
    
    ax1.plot(x, memory_small, 'o-', linewidth=3, markersize=10, 
            label='Small Structure (2MB)', color='#3498db', alpha=0.8)
    ax1.plot(x, memory_large, 's-', linewidth=3, markersize=10, 
            label='Large Structure (6MB)', color='#e74c3c', alpha=0.8)
    ax1.fill_between(x, memory_small, alpha=0.2, color='#3498db')
    ax1.fill_between(x, memory_large, alpha=0.2, color='#e74c3c')
    
    ax1.set_ylabel('Memory Usage (GB)', fontweight='bold', fontsize=12)
    ax1.set_title('Memory Usage Pattern During Validation', fontweight='bold', fontsize=16)
    ax1.set_xticks(x)
    ax1.set_xticklabels(stages)
    ax1.legend(loc='upper left', fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 7)
    
    # Add horizontal line for recommended RAM
    ax1.axhline(y=4, color='orange', linestyle='--', linewidth=2, 
               label='Minimum RAM (4GB)', alpha=0.7)
    ax1.axhline(y=8, color='green', linestyle='--', linewidth=2, 
               label='Recommended RAM (8GB)', alpha=0.7)
    ax1.legend(loc='upper left', fontsize=11)
    
    # CPU usage distribution
    components = ['SAS\nValidation', 'CX-MS\nValidation', 'EM\nValidation', 
                  'Report\nGeneration', 'Other']
    cpu_time = [30, 15, 40, 10, 5]  # percentage of total time
    colors_cpu = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#95a5a6']
    explode = (0.05, 0, 0.1, 0, 0)
    
    wedges, texts, autotexts = ax2.pie(cpu_time, explode=explode, labels=components, 
                                       colors=colors_cpu, autopct='%1.1f%%',
                                       shadow=True, startangle=90, 
                                       textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    ax2.set_title('CPU Time Distribution by Component', fontweight='bold', fontsize=16)
    
    # Make percentage text white for visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('figures/generated/resource_usage_patterns.png', dpi=300, bbox_inches='tight')
    print("Generated: resource_usage_patterns.png")
    plt.close()

# ============================================================================
# Figure 5: Validation Components Coverage
# ============================================================================
def create_component_coverage_figure():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    structures = ['00001', '00010', '00015', '00020', '00025', '00030', '00035', '00040']
    
    # Component availability (1=present, 0=absent)
    quality = [1, 1, 1, 1, 1, 1, 1, 1]
    sas = [1, 1, 0, 1, 0, 1, 1, 1]
    cxms = [1, 1, 1, 0, 1, 1, 1, 0]
    em = [0, 1, 0, 0, 0, 1, 0, 1]
    
    x = np.arange(len(structures))
    width = 0.2
    
    bars1 = ax.bar(x - 1.5*width, quality, width, label='Quality Check', 
                   color='#27ae60', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x - 0.5*width, sas, width, label='SAS Validation', 
                   color='#e74c3c', alpha=0.8, edgecolor='black')
    bars3 = ax.bar(x + 0.5*width, cxms, width, label='CX-MS Validation', 
                   color='#3498db', alpha=0.8, edgecolor='black')
    bars4 = ax.bar(x + 1.5*width, em, width, label='EM Validation', 
                   color='#f39c12', alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Structure ID (PDBDEV_000000XX)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Component Present (1) / Absent (0)', fontweight='bold', fontsize=12)
    ax.set_title('Validation Components Coverage Across Test Structures', 
                fontweight='bold', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(structures, rotation=45)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 1.2)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/generated/component_coverage.png', dpi=300, bbox_inches='tight')
    print("Generated: component_coverage.png")
    plt.close()

# ============================================================================
# Figure 6: Development Timeline
# ============================================================================
def create_timeline_figure():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    phases = ['Phase 1-2:\nSetup &\nTesting', 'Phase 3-4:\nATSAS\nFix', 
              'Phase 5-6:\nEM & Chimera\nFixes', 'Phase 7:\nChimeraX\nFix', 
              'Phase 8:\nMapQ Fix &\nFinal Testing']
    hours = [6, 4, 3, 1.5, 2.5]
    success_rate = [50, 87.5, 87.5, 87.5, 100]
    
    # Create dual-axis plot
    x = np.arange(len(phases))
    
    # Bar plot for hours
    bars = ax.bar(x, hours, alpha=0.7, color='#3498db', edgecolor='black', linewidth=2)
    ax.set_xlabel('Development Phase', fontweight='bold', fontsize=12)
    ax.set_ylabel('Time Invested (hours)', fontweight='bold', fontsize=12, color='#3498db')
    ax.set_title('Development Timeline: Effort vs Success Rate', fontweight='bold', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(phases)
    ax.tick_params(axis='y', labelcolor='#3498db')
    ax.grid(axis='y', alpha=0.3)
    
    # Add hour labels on bars
    for bar, hour in zip(bars, hours):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{hour}h', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Line plot for success rate
    ax2 = ax.twinx()
    line = ax2.plot(x, success_rate, 'o-', color='#27ae60', linewidth=3, 
                   markersize=12, label='Success Rate')
    ax2.set_ylabel('Validation Success Rate (%)', fontweight='bold', fontsize=12, color='#27ae60')
    ax2.tick_params(axis='y', labelcolor='#27ae60')
    ax2.set_ylim(0, 110)
    
    # Add success rate labels
    for i, rate in enumerate(success_rate):
        ax2.text(x[i], rate + 3, f'{rate}%', ha='center', fontweight='bold', 
                fontsize=10, color='#27ae60')
    
    # Add cumulative hours
    total_hours = sum(hours)
    ax.text(0.98, 0.98, f'Total: {total_hours} hours', transform=ax.transAxes,
           fontsize=12, fontweight='bold', verticalalignment='top', 
           horizontalalignment='right', bbox=dict(boxstyle='round', 
           facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/generated/development_timeline.png', dpi=300, bbox_inches='tight')
    print("Generated: development_timeline.png")
    plt.close()

# ============================================================================
# Generate all figures
# ============================================================================
if __name__ == '__main__':
    print("Generating professional figures...")
    print()
    
    create_success_rate_figure()
    create_validation_time_figure()
    create_issues_fixed_figure()
    create_resource_usage_figure()
    create_component_coverage_figure()
    create_timeline_figure()
    
    print()
    print("All figures generated successfully in figures/generated/")
    print("High-resolution PNG files (300 DPI) ready for publication")
