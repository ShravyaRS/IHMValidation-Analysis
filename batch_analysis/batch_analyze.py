
#!/usr/bin/env python3
"""
Batch Processing & Meta-Analysis Module
Analyzes multiple structures and generates summary statistics
"""

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import time

class BatchAnalyzer:
    """Process multiple structures and generate meta-analysis"""
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
    
    def validate_structure(self, cif_file):
        """Run validation on single structure"""
        name = cif_file.stem
        print(f"Processing {name}...")
        
        start_time = time.time()
        cmd = [
            'singularity', 'exec',
            'IHMValidation/ihmvalidation_complete.sif',
            'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
            '-f', str(cif_file),
            '--output-root', str(self.output_dir / name),
            '--output-prefix', name
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=600)
            elapsed = time.time() - start_time
            
            return {
                'structure': name,
                'success': result.returncode == 0,
                'time_seconds': elapsed,
                'size_mb': cif_file.stat().st_size / 1024 / 1024
            }
        except Exception as e:
            return {
                'structure': name,
                'success': False,
                'time_seconds': -1,
                'size_mb': cif_file.stat().st_size / 1024 / 1024,
                'error': str(e)
            }
    
    def process_batch(self):
        """Process all CIF files in input directory"""
        cif_files = list(self.input_dir.glob("*.cif"))
        print(f"\nFound {len(cif_files)} structures to process")
        print("="*60)
        
        for cif_file in cif_files:
            result = self.validate_structure(cif_file)
            self.results.append(result)
        
        # Save results
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_dir / 'summary_statistics.csv', index=False)
        print(f"\n✓ Saved summary to {self.output_dir / 'summary_statistics.csv'}")
        
        return df
    
    def generate_meta_analysis(self, df):
        """Generate meta-analysis plots"""
        print("\nGenerating meta-analysis visualizations...")
        
        # Success rate
        success_rate = (df['success'].sum() / len(df)) * 100
        
        # Time distribution
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Success rate
        axes[0, 0].bar(['Failed', 'Passed'], 
                      [(~df['success']).sum(), df['success'].sum()],
                      color=['#d62728', '#2ca02c'])
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].set_title(f'Success Rate: {success_rate:.1f}%')
        
        # Time distribution
        axes[0, 1].hist(df[df['success']]['time_seconds'], bins=10, 
                       color='#1f77b4', edgecolor='black')
        axes[0, 1].set_xlabel('Time (seconds)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Validation Time Distribution')
        
        # Size vs Time
        successful = df[df['success']]
        axes[1, 0].scatter(successful['size_mb'], successful['time_seconds'],
                          alpha=0.6, s=100)
        axes[1, 0].set_xlabel('Structure Size (MB)')
        axes[1, 0].set_ylabel('Validation Time (s)')
        axes[1, 0].set_title('Performance Scaling')
        
        # Summary statistics
        stats_text = f"""
        Total Structures: {len(df)}
        Successful: {df['success'].sum()}
        Failed: {(~df['success']).sum()}
        
        Avg Time: {df[df['success']]['time_seconds'].mean():.1f}s
        Avg Size: {df['size_mb'].mean():.2f} MB
        """
        axes[1, 1].text(0.1, 0.5, stats_text, fontsize=12, family='monospace')
        axes[1, 1].axis('off')
        axes[1, 1].set_title('Summary Statistics')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'meta_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved meta-analysis to {self.output_dir / 'meta_analysis.png'}")
        plt.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python batch_analyze.py <input_dir> <output_dir>")
        sys.exit(1)
    
    analyzer = BatchAnalyzer(sys.argv[1], sys.argv[2])
    df = analyzer.process_batch()
    analyzer.generate_meta_analysis(df)
    print("\n✓ Batch analysis complete")
