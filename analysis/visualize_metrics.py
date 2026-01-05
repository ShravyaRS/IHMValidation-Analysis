#!/usr/bin/env python3
"""
Create high-quality visualizations of validation metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class MetricVisualizer:
    def __init__(self, metrics_file):
        self.df = pd.read_csv(metrics_file)
        self.output_dir = Path('analysis/figures')
        self.output_dir.mkdir(exist_ok=True)
        
    def create_all_visualizations(self):
        """Generate all visualization figures"""
        print("Generating visualizations...")
        
        self.plot_success_rate()
        self.plot_metric_distributions()
        self.plot_correlation_matrix()
        self.create_summary_dashboard()
        
        print(f"\n✓ All figures saved to {self.output_dir}/")
    
    def plot_success_rate(self):
        """Validation success rate"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        success_counts = self.df['validation_success'].value_counts()
        colors = ['#2ecc71', '#e74c3c']
        
        ax.bar(['Success', 'Failed'], 
               [success_counts.get(True, 0), success_counts.get(False, 0)],
               color=colors)
        
        ax.set_ylabel('Number of Structures', fontsize=12)
        ax.set_title('IHM Validation Success Rate', fontsize=14, fontweight='bold')
        
        # Add percentage labels
        total = len(self.df)
        for i, (label, count) in enumerate(zip(['Success', 'Failed'], 
                                                [success_counts.get(True, 0), 
                                                 success_counts.get(False, 0)])):
            pct = count/total*100
            ax.text(i, count, f'{count}\n({pct:.1f}%)', 
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'success_rate.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Success rate plot created")
    
    def plot_metric_distributions(self):
        """Distribution of numeric metrics"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != 'validation_success']
        
        if len(numeric_cols) == 0:
            print("  ⚠ No numeric metrics to plot")
            return
        
        n_metrics = min(len(numeric_cols), 9)  # Plot up to 9 metrics
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.flatten()
        
        for idx, col in enumerate(numeric_cols[:n_metrics]):
            data = self.df[col].dropna()
            if len(data) > 0:
                axes[idx].hist(data, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
                axes[idx].set_title(col, fontsize=10, fontweight='bold')
                axes[idx].set_xlabel('Value', fontsize=9)
                axes[idx].set_ylabel('Frequency', fontsize=9)
        
        # Hide unused subplots
        for idx in range(n_metrics, 9):
            axes[idx].axis('off')
        
        plt.suptitle('Distribution of Validation Metrics', 
                    fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'metric_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Metric distributions plot created")
    
    def plot_correlation_matrix(self):
        """Correlation heatmap of metrics"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            print("  ⚠ Not enough metrics for correlation matrix")
            return
        
        corr = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Metric Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Correlation matrix created")
    
    def create_summary_dashboard(self):
        """Create summary dashboard figure"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Overall statistics
        ax1 = fig.add_subplot(gs[0, :])
        stats_text = self.get_summary_stats()
        ax1.text(0.5, 0.5, stats_text, fontsize=12, ha='center', va='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.axis('off')
        ax1.set_title('Validation Analysis Summary', fontsize=16, fontweight='bold', pad=20)
        
        # Success pie chart
        ax2 = fig.add_subplot(gs[1, 0])
        success_counts = self.df['validation_success'].value_counts()
        ax2.pie([success_counts.get(True, 0), success_counts.get(False, 0)],
               labels=['Success', 'Failed'],
               autopct='%1.1f%%',
               colors=['#2ecc71', '#e74c3c'],
               startangle=90)
        ax2.set_title('Validation Outcomes', fontweight='bold')
        
        # Structure names
        ax3 = fig.add_subplot(gs[1:, 1:])
        structures = self.df['structure'].tolist()
        success = self.df['validation_success'].tolist()
        
        y_pos = np.arange(len(structures))
        colors = ['green' if s else 'red' for s in success]
        
        ax3.barh(y_pos, [1]*len(structures), color=colors, alpha=0.6)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(structures, fontsize=9)
        ax3.set_xlabel('Status', fontsize=10)
        ax3.set_title('Structure-by-Structure Results', fontweight='bold')
        ax3.set_xlim(0, 1.2)
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='green', alpha=0.6, label='Success'),
                          Patch(facecolor='red', alpha=0.6, label='Failed')]
        ax3.legend(handles=legend_elements, loc='upper right')
        
        plt.savefig(self.output_dir / 'summary_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Summary dashboard created")
    
    def get_summary_stats(self):
        """Get formatted summary statistics"""
        total = len(self.df)
        success = self.df['validation_success'].sum()
        success_rate = success/total*100 if total > 0 else 0
        
        numeric_cols = len(self.df.select_dtypes(include=[np.number]).columns)
        
        text = f"""
        Total Structures Analyzed: {total}
        Successful Validations: {success}
        Failed Validations: {total - success}
        Success Rate: {success_rate:.1f}%
        
        Numeric Metrics Extracted: {numeric_cols}
        """
        
        return text

if __name__ == '__main__':
    if Path('analysis/data/extracted_metrics.csv').exists():
        visualizer = MetricVisualizer('analysis/data/extracted_metrics.csv')
        visualizer.create_all_visualizations()
    else:
        print("Error: Run extract_metrics.py first!")
