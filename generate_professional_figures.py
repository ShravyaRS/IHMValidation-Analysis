
#!/usr/bin/env python3
"""
Professional publication-quality figures for IHMValidation
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Professional publication settings
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'axes.linewidth': 1.5,
    'grid.linewidth': 0.8,
    'lines.linewidth': 2.5,
})

import os
os.makedirs('figures/generated', exist_ok=True)

# CORRECT DATA
ACTUAL_DATA = {
    'PDBDEV_00000001': {'before': True, 'after': True, 'size_mb': 1.6, 'time_min': 2.5},
    'PDBDEV_00000010': {'before': False, 'after': True, 'size_mb': 5.8, 'time_min': 9.0},  # Fixed by MapQ
    'PDBDEV_00000015': {'before': True, 'after': True, 'size_mb': 2.3, 'time_min': 4.0},
    'PDBDEV_00000020': {'before': False, 'after': True, 'size_mb': 2.1, 'time_min': 3.0},  # Fixed by ATSAS
    'PDBDEV_00000025': {'before': True, 'after': True, 'size_mb': 1.8, 'time_min': 2.8},
    'PDBDEV_00000030': {'before': True, 'after': True, 'size_mb': 2.4, 'time_min': 4.5},
    'PDBDEV_00000035': {'before': False, 'after': True, 'size_mb': 2.0, 'time_min': 3.5},  # Fixed by ATSAS
    'PDBDEV_00000040': {'before': False, 'after': True, 'size_mb': 2.2, 'time_min': 3.8},  # Fixed by ATSAS
}

# Figure 1: Success Rate
def create_success_rate():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    before = sum(1 for d in ACTUAL_DATA.values() if d['before'])
    after = sum(1 for d in ACTUAL_DATA.values() if d['after'])
    total = len(ACTUAL_DATA)
    
    bars = ax.bar(['Before', 'After'], [before, after], 
                  color=['#d62728', '#2ca02c'], width=0.6,
                  edgecolor='black', linewidth=2)
    
    ax.text(0, before + 0.2, f'{before}/{total}\n50%', ha='center', fontsize=13, fontweight='bold')
    ax.text(1, after + 0.2, f'{after}/{total}\n100%', ha='center', fontsize=13, fontweight='bold')
    
    ax.set_ylabel('Structures Validated', fontweight='bold')
    ax.set_title('Validation Success Rate', fontweight='bold', pad=15)
    ax.set_ylim(0, 9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figures/generated/success_rate.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ success_rate.png")

# Figure 2: Performance Analysis (3D surface)
def create_performance_3d():
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    sizes = np.array([d['size_mb'] for d in ACTUAL_DATA.values()])
    times = np.array([d['time_min'] for d in ACTUAL_DATA.values()])
    complexity = sizes * 100  # complexity metric
    
    scatter = ax.scatter(sizes, times, complexity, c=times, cmap='viridis', 
                        s=200, alpha=0.8, edgecolors='black', linewidth=1.5)
    
    ax.set_xlabel('Size (MB)', fontweight='bold', labelpad=10)
    ax.set_ylabel('Time (min)', fontweight='bold', labelpad=10)
    ax.set_zlabel('Complexity', fontweight='bold', labelpad=10)
    ax.set_title('Validation Performance Analysis', fontweight='bold', pad=20)
    
    plt.colorbar(scatter, ax=ax, label='Time (min)', pad=0.1)
    plt.tight_layout()
    plt.savefig('figures/generated/performance_3d.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ performance_3d.png")

# Figure 3: Component Impact
def create_component_impact():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # CORRECT: Only ATSAS and MapQ fixed structures
    components = ['ATSAS\nInstallation', 'MapQ\nError Handling', 
                  'EM Webdriver\n(Enhancement)', 'Version Checks\n(Stability)']
    impact = [3, 1, 0, 0]  # Number of structures fixed
    colors = ['#d62728', '#2ca02c', '#1f77b4', '#ff7f0e']
    
    bars = ax.barh(components, impact, color=colors, edgecolor='black', linewidth=2)
    
    for bar, val in zip(bars, impact):
        if val > 0:
            ax.text(val + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{val} structure{"s" if val > 1 else ""}', 
                   va='center', fontweight='bold')
        else:
            ax.text(0.05, bar.get_y() + bar.get_height()/2, 
                   'Stability enhancement', va='center', fontsize=9, style='italic')
    
    ax.set_xlabel('Structures Fixed', fontweight='bold')
    ax.set_title('Component Impact Analysis', fontweight='bold', pad=15)
    ax.set_xlim(0, 3.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figures/generated/component_impact.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ component_impact.png")

if __name__ == '__main__':
    print("\nGenerating professional figures...")
    create_success_rate()
    create_performance_3d()
    create_component_impact()
    print("\nComplete. 3 publication-quality figures generated.\n")
