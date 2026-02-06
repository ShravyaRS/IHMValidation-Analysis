#!/usr/bin/env python3
"""
Formal performance benchmark: DATCMP vs Python CorMap
"""

import time
import numpy as np
from pathlib import Path
import json
import psutil
import os
from cormap_implementation import cormap_pairwise

def benchmark_cormap():
    """Benchmark Python CorMap performance"""
    
    print("="*80)
    print("PERFORMANCE BENCHMARK")
    print("="*80)
    
    # Load test cases
    with open('validation_comparison/extracted_data/exp_fit_pairs.json', 'r') as f:
        pairs = json.load(f)
    
    # Select 10 representative pairs
    test_pairs = pairs[:min(10, len(pairs))]
    
    times = []
    memory_usage = []
    
    process = psutil.Process(os.getpid())
    
    for pair in test_pairs:
        exp_file = Path(pair['exp_file'])
        fit_file = Path(pair['fit_file'])
        
        # Load data
        exp_data = np.loadtxt(exp_file, comments='#')
        fit_data = np.loadtxt(fit_file, comments='#')
        
        exp_q, exp_I, exp_err = exp_data[:, 0], exp_data[:, 1], exp_data[:, 2]
        fit_q, fit_I = fit_data[:, 0], fit_data[:, 1]
        
        # Measure time
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        start = time.perf_counter()
        
        result = cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)
        
        end = time.perf_counter()
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        
        elapsed = (end - start) * 1000  # Convert to ms
        mem_delta = max(0, mem_after - mem_before)
        
        times.append(elapsed)
        memory_usage.append(mem_delta)
    
    # Statistics
    mean_time = np.mean(times)
    std_time = np.std(times)
    mean_memory = np.mean(memory_usage)
    
    print(f"\nPython CorMap Performance (n={len(test_pairs)}):")
    print(f"  Mean time: {mean_time:.4f} ms ({mean_time/1000:.6f} s)")
    print(f"  Std dev: {std_time:.4f} ms")
    print(f"  Min time: {min(times):.4f} ms")
    print(f"  Max time: {max(times):.4f} ms")
    print(f"  Memory: ~{mean_memory:.2f} MB delta")
    
    # Compare with DATCMP (estimated from previous runs)
    datcmp_time_estimate = 500  # ms (0.5 seconds)
    speedup = datcmp_time_estimate / mean_time
    
    print(f"\nComparison with DATCMP:")
    print(f"  DATCMP (estimated): ~500 ms")
    print(f"  Python CorMap: {mean_time:.4f} ms")
    print(f"  Speedup: ~{speedup:.0f}x faster")
    
    # System info
    import platform
    print(f"\nSystem Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Python: {platform.python_version()}")
    print(f"  CPU cores: {psutil.cpu_count()}")
    print(f"  RAM: {psutil.virtual_memory().total / 1024**3:.1f} GB")
    
    # Save benchmark results
    benchmark = {
        'python_cormap': {
            'mean_time_ms': mean_time,
            'std_time_ms': std_time,
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'mean_memory_mb': mean_memory
        },
        'datcmp': {
            'estimated_time_ms': datcmp_time_estimate,
            'note': 'Estimated from validation runs with Singularity container'
        },
        'speedup': speedup,
        'system': {
            'os': f"{platform.system()} {platform.release()}",
            'python': platform.python_version(),
            'cpu_cores': psutil.cpu_count(),
            'ram_gb': psutil.virtual_memory().total / 1024**3
        }
    }
    
    output_dir = Path('validation_comparison/benchmarks')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'performance.json', 'w') as f:
        json.dump(benchmark, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Benchmark saved to: {output_dir}/performance.json")
    print("="*80)

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    benchmark_cormap()
