
#!/usr/bin/env python3
"""
Performance Profiling and Complexity Analysis
Measures time complexity and generates scaling reports
"""

import cProfile
import pstats
import time
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class PerformanceProfiler:
    """Profile validation performance and analyze complexity"""
    
    def __init__(self):
        self.results = []
    
    def profile_structure(self, structure_file, label):
        """Profile validation of single structure"""
        import subprocess
        
        print(f"Profiling {label}...")
        start = time.time()
        
        cmd = [
            'singularity', 'exec',
            'IHMValidation/ihmvalidation_complete.sif',
            'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
            '-f', structure_file,
            '--output-root', f'profiling/output_{label}',
            '--output-prefix', label
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=600)
            elapsed = time.time() - start
            
            size_mb = Path(structure_file).stat().st_size / 1024 / 1024
            
            self.results.append({
                'label': label,
                'size_mb': size_mb,
                'time_seconds': elapsed,
                'atoms': int(size_mb * 1000)  # Rough estimate
            })
            
            return elapsed
        except Exception as e:
            print(f"Error profiling {label}: {e}")
            return -1
    
    def analyze_complexity(self):
        """Analyze time complexity"""
        if len(self.results) < 2:
            print("Need at least 2 data points for complexity analysis")
            return
        
        sizes = np.array([r['size_mb'] for r in self.results])
        times = np.array([r['time_seconds'] for r in self.results])
        
        # Fit to different complexity models
        # Linear: O(n)
        linear_coef = np.polyfit(sizes, times, 1)
        # Quadratic: O(n²)
        quad_coef = np.polyfit(sizes, times, 2)
        
        # Calculate R² for each fit
        linear_fit = np.poly1d(linear_coef)(sizes)
        quad_fit = np.poly1d(quad_coef)(sizes)
        
        ss_res_linear = np.sum((times - linear_fit)**2)
        ss_tot = np.sum((times - np.mean(times))**2)
        r2_linear = 1 - (ss_res_linear / ss_tot)
        
        ss_res_quad = np.sum((times - quad_fit)**2)
        r2_quad = 1 - (ss_res_quad / ss_tot)
        
        # Plot results
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Complexity plot
        ax1.scatter(sizes, times, s=100, alpha=0.7, label='Actual', color='blue')
        x_smooth = np.linspace(sizes.min(), sizes.max(), 100)
        ax1.plot(x_smooth, np.poly1d(linear_coef)(x_smooth), 
                'r--', label=f'Linear (R²={r2_linear:.3f})')
        ax1.plot(x_smooth, np.poly1d(quad_coef)(x_smooth), 
                'g--', label=f'Quadratic (R²={r2_quad:.3f})')
        ax1.set_xlabel('Structure Size (MB)', fontweight='bold')
        ax1.set_ylabel('Validation Time (seconds)', fontweight='bold')
        ax1.set_title('Time Complexity Analysis', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Scaling report
        report_text = f"""
        PERFORMANCE PROFILE
        
        Best Fit: {'Linear' if r2_linear > r2_quad else 'Quadratic'}
        
        Linear Model (O(n)):
          R² = {r2_linear:.4f}
          Slope = {linear_coef[0]:.2f} s/MB
          
        Quadratic Model (O(n²)):
          R² = {r2_quad:.4f}
          
        Scalability:
        • 2x size → {2 * linear_coef[0]:.1f}x time (linear)
        • 2x size → {4 * quad_coef[0]:.1f}x time (quad)
        
        Structures Profiled: {len(self.results)}
        Size Range: {sizes.min():.1f} - {sizes.max():.1f} MB
        Time Range: {times.min():.1f} - {times.max():.1f} s
        """
        
        ax2.text(0.1, 0.5, report_text, fontsize=10, family='monospace',
                verticalalignment='center')
        ax2.axis('off')
        ax2.set_title('Complexity Report', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('profiling/complexity_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Saved complexity analysis to profiling/complexity_analysis.png")
        plt.close()
        
        # Print summary
        print("\n" + "="*60)
        print("TIME COMPLEXITY ANALYSIS")
        print("="*60)
        print(f"Best fit model: {'Linear O(n)' if r2_linear > r2_quad else 'Quadratic O(n²)'}")
        print(f"R² score: {max(r2_linear, r2_quad):.4f}")
        print(f"\nScalability: As structure size doubles,")
        print(f"validation time increases by ~{2 * linear_coef[0] / linear_coef[0]:.1f}x")

if __name__ == '__main__':
    profiler = PerformanceProfiler()
    
    # Profile test structures
    test_structures = [
        ('test-data-extended/PDBDEV_00000001.cif', 'small'),
        ('test-data-extended/PDBDEV_00000020.cif', 'medium'),
        ('test-data-extended/PDBDEV_00000010.cif', 'large'),
    ]
    
    for struct_file, label in test_structures:
        profiler.profile_structure(struct_file, label)
    
    profiler.analyze_complexity()
