#!/usr/bin/env python3
"""
Extract and analyze validation metrics from IHM structures
FIXED VERSION with correct validation command
"""

import json
import re
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import subprocess
import time

class MetricExtractor:
    def __init__(self):
        self.metrics = []
        self.structures = []
        
    def validate_and_extract(self, structure_file):
        """Run validation and extract all metrics"""
        print(f"\n{'='*60}")
        print(f"Analyzing: {structure_file.name}")
        print(f"{'='*60}")
        
        struct_name = structure_file.stem
        output_dir = Path(f"analysis/results/{struct_name}")
        
        # Run validation with CORRECT command
        try:
            start_time = time.time()
            
            cmd = [
                'singularity', 'exec',
                'IHMValidation/ihmvalidation.sif',
                'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
                '-f', str(structure_file.absolute()),
                '--output-root', 'analysis/results',
                '--output-prefix', struct_name
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 min timeout
            )
            
            elapsed = time.time() - start_time
            
            print(f"Return code: {result.returncode}")
            print(f"Time elapsed: {elapsed:.1f} seconds")
            
            if result.stdout:
                print(f"Output (first 500 chars): {result.stdout[:500]}")
            if result.stderr and result.returncode != 0:
                print(f"Errors: {result.stderr[:500]}")
            
            # Check if PDFs were generated
            pdf_full = Path(f"analysis/results/{struct_name}_full_validation.pdf")
            pdf_summary = Path(f"analysis/results/{struct_name}_summary_validation.pdf")
            
            metrics = {
                'structure': struct_name,
                'validation_success': result.returncode == 0,
                'pdf_full_generated': pdf_full.exists(),
                'pdf_summary_generated': pdf_summary.exists(),
                'processing_time_seconds': elapsed,
                'return_code': result.returncode
            }
            
            # Try to extract metrics from output
            if pdf_full.exists():
                metrics['pdf_full_size_kb'] = pdf_full.stat().st_size / 1024
            if pdf_summary.exists():
                metrics['pdf_summary_size_kb'] = pdf_summary.stat().st_size / 1024
            
            self.metrics.append(metrics)
            
        except subprocess.TimeoutExpired:
            print(f"⚠ Validation timeout (10 min)")
            self.metrics.append({
                'structure': struct_name,
                'validation_success': False,
                'error': 'Timeout after 10 minutes'
            })
        except Exception as e:
            print(f"✗ Error: {e}")
            self.metrics.append({
                'structure': struct_name,
                'validation_success': False,
                'error': str(e)
            })
    
    def analyze_all(self, structure_dir):
        """Analyze all structures in directory"""
        structures = sorted(list(Path(structure_dir).glob('*.cif')))
        print(f"\n{'='*60}")
        print(f"BATCH VALIDATION ANALYSIS")
        print(f"{'='*60}")
        print(f"Found {len(structures)} structures to analyze")
        print(f"Output directory: analysis/results/")
        print(f"{'='*60}\n")
        
        for idx, struct in enumerate(structures, 1):
            print(f"\n[{idx}/{len(structures)}] Processing {struct.name}...")
            self.validate_and_extract(struct)
        
        # Save results
        self.save_results()
        self.generate_analysis()
    
    def save_results(self):
        """Save extracted metrics"""
        df = pd.DataFrame(self.metrics)
        
        output_file = 'analysis/data/validation_results.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✓ Results saved to {output_file}")
        
        # Also save as JSON
        json_file = 'analysis/data/validation_results.json'
        with open(json_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"✓ Detailed data saved to {json_file}")
        
        return df
    
    def generate_analysis(self):
        """Generate statistical analysis"""
        df = pd.DataFrame(self.metrics)
        
        print(f"\n{'='*60}")
        print("VALIDATION ANALYSIS SUMMARY")
        print(f"{'='*60}")
        
        total = len(df)
        successful = df['validation_success'].sum() if 'validation_success' in df.columns else 0
        
        print(f"\nTotal structures: {total}")
        print(f"Successful validations: {successful}")
        print(f"Failed validations: {total - successful}")
        
        if total > 0:
            print(f"Success rate: {successful/total*100:.1f}%")
        
        if 'pdf_full_generated' in df.columns:
            pdf_count = df['pdf_full_generated'].sum()
            print(f"Full PDF reports: {pdf_count}")
        
        if 'pdf_summary_generated' in df.columns:
            summary_count = df['pdf_summary_generated'].sum()
            print(f"Summary PDF reports: {summary_count}")
        
        if 'processing_time_seconds' in df.columns:
            times = df['processing_time_seconds'].dropna()
            if len(times) > 0:
                print(f"\nProcessing times:")
                print(f"  Average: {times.mean():.1f} seconds")
                print(f"  Median: {times.median():.1f} seconds")
                print(f"  Range: {times.min():.1f} - {times.max():.1f} seconds")
        
        # Save summary
        summary = {
            'total_structures': total,
            'successful_validations': int(successful),
            'failed_validations': total - int(successful),
            'success_rate': float(successful/total) if total > 0 else 0,
            'structures_analyzed': df['structure'].tolist()
        }
        
        with open('analysis/data/summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Summary saved to analysis/data/summary.json")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    Path('analysis/results').mkdir(parents=True, exist_ok=True)
    Path('analysis/data').mkdir(parents=True, exist_ok=True)
    
    extractor = MetricExtractor()
    
    # Analyze extended test data
    if Path('test-data-extended').exists():
        extractor.analyze_all('test-data-extended')
    else:
        extractor.analyze_all('test-data')
