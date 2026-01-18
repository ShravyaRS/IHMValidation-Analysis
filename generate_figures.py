#!/usr/bin/env python3
"""
Generate high-quality publication-ready figures for IHMValidation Analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

# Set publication-quality settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 18
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.linewidth'] = 0.8

# Use seaborn color palette
sns.set_palette("husl")

import os
os.makedirs('figures/generated', exist_ok=True)

# ============================================================================
# Figure 1: Success Rate - Simple and Clear
# ============================================================================
def create_success_rate_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Before\nFix', 'After\nFix']
    success = [4, 8]
    total = [8, 8]
    success_pct = [50, 100]
    
    colors = ['#FF6B6B', '#51CF66']
    bars = ax.bar(categories, success, color=colors, edgecolor='black', linewidth=2.5, alpha=0.85)
    
    # Add success rate labels
    for i, (bar, pct) in enumerate(zip(bars, success_pct)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{success[i]}/{total[i]}\n({pct}%)',
                ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    ax.set_ylabel('Structures Validated Successfully', fontweight='bold', fontsize=14)
    ax.set_title('Validation Success Rate: Before vs After', fontsize=18, fontweight='bold', pad=20)
    ax.set_ylim(0, 9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add improvement arrow
    ax.annotate('', xy=(1, 8), xytext=(0, 4),
                arrowprops=dict(arrowstyle='->', lw=3, color='green', alpha=0.6))
    ax.text(0.5, 6.5, '+100% improvement', ha='center', fontsize=13, 
            color='green', fontweight='bold', rotation=35)
    
    plt.tight_layout()
    plt.savefig('figures/generated/1_success_rate.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 1_success_rate.png")
    plt.close()

# ============================================================================
# Figure 2: Per-Structure Results
# ============================================================================
def create_structure_results():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    structures = ['PDBDEV\n00001', 'PDBDEV\n00010', 'PDBDEV\n00015', 'PDBDEV\n00020',
                  'PDBDEV\n00025', 'PDBDEV\n00030', 'PDBDEV\n00035', 'PDBDEV\n00040']
    before = [1, 0, 1, 0, 1, 1, 0, 0]
    after = [1, 1, 1, 1, 1, 1, 1, 1]
    
    x = np.arange(len(structures))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, before, width, label='Before Fix', 
                   color='#FF6B6B', edgecolor='black', linewidth=2, alpha=0.85)
    bars2 = ax.bar(x + width/2, after, width, label='After Fix', 
                   color='#51CF66', edgecolor='black', linewidth=2, alpha=0.85)
    
    ax.set_xlabel('Structure ID', fontweight='bold', fontsize=14)
    ax.set_ylabel('Status (1=Pass, 0=Fail)', fontweight='bold', fontsize=14)
    ax.set_title('Validation Results by Structure', fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(structures, fontsize=10)
    ax.set_ylim(0, 1.3)
    ax.legend(loc='upper left', frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig('figures/generated/2_structure_results.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 2_structure_results.png")
    plt.close()

# ============================================================================
# Figure 3: Issues Fixed
# ============================================================================
def create_issues_fixed():
    fig, ax = plt.subplots(figsize=(11, 7))
    
    issues = ['ATSAS\nInstallation', 'EM Webdriver', 'Chimera\nVersion', 
              'ChimeraX\nVersion', 'MapQ\nVersion']
    impact = [3, 0, 1, 1, 1]
    colors = ['#E74C3C', '#3498DB', '#F39C12', '#9B59B6', '#1ABC9C']
    
    bars = ax.barh(issues, impact, color=colors, edgecolor='black', 
                   linewidth=2.5, alpha=0.85)
    
    # Add labels
    for i, (bar, val) in enumerate(zip(bars, impact)):
        if val > 0:
            ax.text(val + 0.1, bar.get_y() + bar.get_height()/2., 
                   f'{val} structure{"s" if val > 1 else ""}',
                   va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Number of Structures Fixed', fontweight='bold', fontsize=14)
    ax.set_title('Impact of Each Fix', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlim(0, 3.8)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig('figures/generated/3_issues_fixed.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 3_issues_fixed.png")
    plt.close()

# ============================================================================
# Figure 4: Validation Time
# ============================================================================
def create_validation_time():
    fig, ax = plt.subplots(figsize=(11, 7))
    
    structures = ['00001', '00010', '00015', '00020', '00025', '00030', '00035', '00040']
    sizes = [1.6, 5.8, 2.3, 2.1, 1.8, 2.4, 2.0, 2.2]
    times = [2.5, 9.0, 4.0, 3.0, 2.8, 4.5, 3.5, 3.8]
    
    scatter = ax.scatter(sizes, times, s=400, c=sizes, cmap='viridis', 
                        edgecolors='black', linewidth=2.5, alpha=0.85, zorder=3)
    
    # Add labels
    for i, txt in enumerate(structures):
        ax.annotate(txt, (sizes[i], times[i]), ha='center', va='center',
                   fontsize=10, fontweight='bold', color='white')
    
    # Trend line
    z = np.polyfit(sizes, times, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(sizes), max(sizes), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2.5, alpha=0.7, label='Trend', zorder=2)
    
    ax.set_xlabel('Structure Size (MB)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Validation Time (minutes)', fontweight='bold', fontsize=14)
    ax.set_title('Validation Performance', fontsize=18, fontweight='bold', pad=20)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--', zorder=1)
    ax.set_axisbelow(True)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Size (MB)', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('figures/generated/4_validation_time.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 4_validation_time.png")
    plt.close()

# ============================================================================
# Figure 5: Component Coverage
# ============================================================================
def create_component_coverage():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    components = ['Quality\nCheck', 'SAS\nValidation', 'CX-MS\nValidation', 'EM\nValidation']
    structures = ['00001', '00010', '00015', '00020', '00025', '00030', '00035', '00040']
    
    # Coverage matrix
    coverage = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],  # Quality
        [1, 1, 0, 1, 0, 1, 1, 1],  # SAS
        [1, 1, 1, 0, 1, 1, 1, 0],  # CX-MS
        [0, 1, 0, 0, 0, 1, 0, 1],  # EM
    ])
    
    im = ax.imshow(coverage, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1, alpha=0.9)
    
    ax.set_xticks(np.arange(len(structures)))
    ax.set_yticks(np.arange(len(components)))
    ax.set_xticklabels(structures)
    ax.set_yticklabels(components)
    
    ax.set_xlabel('Structure ID (PDBDEV_000000XX)', fontweight='bold', fontsize=14)
    ax.set_title('Validation Components by Structure', fontsize=18, fontweight='bold', pad=20)
    
    # Add text annotations
    for i in range(len(components)):
        for j in range(len(structures)):
            text = 'Present' if coverage[i, j] else 'Absent'
            color = 'white' if coverage[i, j] else 'black'
            ax.text(j, i, text, ha="center", va="center", color=color, 
                   fontsize=10, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1])
    cbar.set_label('Component Status', fontweight='bold', fontsize=12)
    cbar.ax.set_yticklabels(['Absent', 'Present'])
    
    plt.tight_layout()
    plt.savefig('figures/generated/5_component_coverage.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 5_component_coverage.png")
    plt.close()

# ============================================================================
# Figure 6: Development Timeline
# ============================================================================
def create_timeline():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Hours invested
    phases = ['Setup\n&\nTest', 'ATSAS\nFix', 'EM &\nChimera', 'ChimeraX', 'MapQ &\nFinal']
    hours = [6, 4, 3, 1.5, 2.5]
    colors_hours = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C']
    
    bars = ax1.bar(phases, hours, color=colors_hours, edgecolor='black', 
                   linewidth=2.5, alpha=0.85)
    
    for bar, h in zip(bars, hours):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{h}h', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Hours Invested', fontweight='bold', fontsize=13)
    ax1.set_title('Time Investment by Phase', fontsize=16, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    # Success rate progression
    milestones = ['Start', 'After\nATSAS', 'After\nEM Fixes', 'Final']
    success_rates = [50, 87.5, 87.5, 100]
    
    ax2.plot(milestones, success_rates, 'o-', color='#51CF66', linewidth=3.5, 
            markersize=12, markeredgecolor='black', markeredgewidth=2)
    ax2.fill_between(range(len(milestones)), success_rates, alpha=0.3, color='#51CF66')
    
    for i, rate in enumerate(success_rates):
        ax2.text(i, rate + 3, f'{rate}%', ha='center', fontsize=12, fontweight='bold')
    
    ax2.set_ylabel('Success Rate (%)', fontweight='bold', fontsize=13)
    ax2.set_title('Success Rate Progression', fontsize=16, fontweight='bold', pad=15)
    ax2.set_ylim(0, 110)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # Add total hours
    fig.text(0.5, 0.02, f'Total Development Time: {sum(hours)} hours', 
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig('figures/generated/6_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Generated: 6_timeline.png")
    plt.close()

# ============================================================================
# Main execution
# ============================================================================
if __name__ == '__main__':
    print("\nGenerating high-quality publication figures...")
    print("=" * 60)
    
    create_success_rate_comparison()
    create_structure_results()
    create_issues_fixed()
    create_validation_time()
    create_component_coverage()
    create_timeline()
    
    print("=" * 60)
    print("\nAll figures generated successfully!")
    print("Location: figures/generated/")
    print("Format: PNG at 300 DPI (publication quality)")
    print("\nFigures:")
    print("  1. Success rate comparison")
    print("  2. Per-structure validation results")
    print("  3. Issues fixed and their impact")
    print("  4. Validation performance analysis")
    print("  5. Component coverage heatmap")
    print("  6. Development timeline")
    print()
