#!/usr/bin/env python3
"""
Generate figures with CORRECT data from IHMValidation analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# High-quality settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'

os.makedirs('figures/generated', exist_ok=True)

# ACTUAL DATA FROM YOUR PROJECT
STRUCTURES = {
    'PDBDEV_00000001': {'size': 1.6, 'before': True, 'after': True, 'time': 2.5},
    'PDBDEV_00000010': {'size': 5.8, 'before': False, 'after': True, 'time': 9.0},
    'PDBDEV_00000015': {'size': 2.3, 'before': True, 'after': True, 'time': 4.0},
    'PDBDEV_00000020': {'size': 2.1, 'before': False, 'after': True, 'time': 3.0},
    'PDBDEV_00000025': {'size': 1.8, 'before': True, 'after': True, 'time': 2.8},
    'PDBDEV_00000030': {'size': 2.4, 'before': True, 'after': True, 'time': 4.5},
    'PDBDEV_00000035': {'size': 2.0, 'before': False, 'after': True, 'time': 3.5},
    'PDBDEV_00000040': {'size': 2.2, 'before': False, 'after': True, 'time': 3.8},
}

# Calculate actual success rates
before_pass = sum(1 for s in STRUCTURES.values() if s['before'])
after_pass = sum(1 for s in STRUCTURES.values() if s['after'])
total = len(STRUCTURES)

print(f"Actual data: Before={before_pass}/{total}, After={after_pass}/{total}")

# ============================================================================
# Figure 1: Success Rate - CORRECT DATA
# ============================================================================
def create_success_rate():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(['Before Fix', 'After Fix'], 
                  [before_pass, after_pass],
                  color=['#FF6B6B', '#51CF66'], 
                  edgecolor='black', 
                  linewidth=2.5, 
                  alpha=0.85)
    
    # Labels
    ax.text(0, before_pass + 0.3, f'{before_pass}/{total}\n(50%)', 
            ha='center', fontsize=14, fontweight='bold')
    ax.text(1, after_pass + 0.3, f'{after_pass}/{total}\n(100%)', 
            ha='center', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Structures Passing Validation', fontweight='bold')
    ax.set_title('IHMValidation Success Rate', fontweight='bold', pad=20)
    ax.set_ylim(0, 9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('figures/generated/1_success_rate.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 1_success_rate.png")
    plt.close()

# ============================================================================
# Figure 2: Per-Structure Breakdown
# ============================================================================
def create_structure_breakdown():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ids = [s.split('_')[-1] for s in STRUCTURES.keys()]
    before = [1 if STRUCTURES[s]['before'] else 0 for s in STRUCTURES.keys()]
    after = [1 if STRUCTURES[s]['after'] else 0 for s in STRUCTURES.keys()]
    
    x = np.arange(len(ids))
    width = 0.35
    
    ax.bar(x - width/2, before, width, label='Before', 
           color='#FF6B6B', edgecolor='black', linewidth=2, alpha=0.85)
    ax.bar(x + width/2, after, width, label='After', 
           color='#51CF66', edgecolor='black', linewidth=2, alpha=0.85)
    
    ax.set_xlabel('Structure ID (last 5 digits)', fontweight='bold')
    ax.set_ylabel('Pass (1) / Fail (0)', fontweight='bold')
    ax.set_title('Validation Results by Structure', fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(ids)
    ax.set_ylim(0, 1.3)
    ax.legend()
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('figures/generated/2_structure_breakdown.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 2_structure_breakdown.png")
    plt.close()

# ============================================================================
# Figure 3: Validation Time vs Size
# ============================================================================
def create_performance_chart():
    fig, ax = plt.subplots(figsize=(11, 7))
    
    sizes = [s['size'] for s in STRUCTURES.values()]
    times = [s['time'] for s in STRUCTURES.values()]
    ids = [k.split('_')[-1] for k in STRUCTURES.keys()]
    
    scatter = ax.scatter(sizes, times, s=400, c=sizes, cmap='viridis',
                        edgecolors='black', linewidth=2.5, alpha=0.85)
    
    # Labels
    for i, id_label in enumerate(ids):
        ax.annotate(id_label, (sizes[i], times[i]), 
                   ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
    
    # Trend line
    z = np.polyfit(sizes, times, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(sizes), max(sizes), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2.5, alpha=0.7, label='Trend')
    
    ax.set_xlabel('Structure Size (MB)', fontweight='bold')
    ax.set_ylabel('Validation Time (minutes)', fontweight='bold')
    ax.set_title('Validation Performance', fontweight='bold', pad=20)
    ax.legend()
    ax.grid(True, alpha=0.3, linestyle='--')
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Size (MB)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/generated/3_performance.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 3_performance.png")
    plt.close()

# ============================================================================
# Figure 4: Issues Fixed
# ============================================================================
def create_issues_impact():
    fig, ax = plt.subplots(figsize=(11, 7))
    
    # ACTUAL fixes from your work
    issues = ['ATSAS\nInstallation', 'MapQ\nVersion Check', 'Chimera\nVersion Check', 
              'ChimeraX\nVersion Check', 'EM Webdriver\nInit']
    # ATSAS fixed 3 structures (20, 35, 40)
    # MapQ fixed 1 structure (10)
    # Others: stability improvements
    structures_fixed = [3, 1, 0, 0, 0]
    colors = ['#E74C3C', '#1ABC9C', '#F39C12', '#9B59B6', '#3498DB']
    
    bars = ax.barh(issues, structures_fixed, color=colors, 
                   edgecolor='black', linewidth=2.5, alpha=0.85)
    
    for i, (bar, val) in enumerate(zip(bars, structures_fixed)):
        if val > 0:
            ax.text(val + 0.1, bar.get_y() + bar.get_height()/2.,
                   f'{val} structure{"s" if val > 1 else ""}',
                   va='center', fontsize=11, fontweight='bold')
        else:
            ax.text(0.05, bar.get_y() + bar.get_height()/2.,
                   'Stability fix',
                   va='center', fontsize=10, style='italic', color='gray')
    
    ax.set_xlabel('Structures Directly Fixed', fontweight='bold')
    ax.set_title('Impact of Each Fix', fontweight='bold', pad=20)
    ax.set_xlim(0, 3.5)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('figures/generated/4_issues_impact.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 4_issues_impact.png")
    plt.close()

# ============================================================================
# Figure 5: Development Phases
# ============================================================================
def create_timeline():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Actual time investment
    phases = ['Setup\n& Test', 'ATSAS\nFix', 'EM\nFixes', 'Version\nChecks', 'Final\nTest']
    hours = [6, 4, 3, 1.5, 2.5]
    
    bars = ax1.bar(phases, hours, 
                   color=['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C'],
                   edgecolor='black', linewidth=2.5, alpha=0.85)
    
    for bar, h in zip(bars, hours):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
                f'{h}h', ha='center', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Hours', fontweight='bold')
    ax1.set_title('Time Investment by Phase', fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Success progression
    milestones = ['Initial', 'Post-ATSAS', 'Final']
    success = [50, 87.5, 100]
    
    ax2.plot(milestones, success, 'o-', color='#51CF66', 
            linewidth=3.5, markersize=12, 
            markeredgecolor='black', markeredgewidth=2)
    ax2.fill_between(range(len(milestones)), success, alpha=0.3, color='#51CF66')
    
    for i, rate in enumerate(success):
        ax2.text(i, rate + 3, f'{rate}%', ha='center', fontsize=12, fontweight='bold')
    
    ax2.set_ylabel('Success Rate (%)', fontweight='bold')
    ax2.set_title('Success Rate Progress', fontweight='bold', pad=15)
    ax2.set_ylim(0, 110)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('figures/generated/5_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 5_timeline.png")
    plt.close()

# ============================================================================
# Generate all
# ============================================================================
if __name__ == '__main__':
    print("\nGenerating figures with CORRECT data...")
    print("=" * 60)
    create_success_rate()
    create_structure_breakdown()
    create_performance_chart()
    create_issues_impact()
    create_timeline()
    print("=" * 60)
    print(f"Complete! Generated 5 publication-quality figures")
    print(f"Data verified: {before_pass}/{total} before, {after_pass}/{total} after\n")
