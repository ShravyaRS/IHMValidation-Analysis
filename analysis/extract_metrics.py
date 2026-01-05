#!/usr/bin/env python3
"""
Extract and analyze validation metrics from IHM structures
High-quality research analysis
"""

import json
import re
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import subprocess

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
        output_dir = Path(f"analysis/data/{struct_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run validation
        try:
            cmd = [
                'singularity', 'exec',
                'IHMValidation/ihmvalidation.sif',
                'ihm_validate',
                str(structure_file),
                '-o', str(output_dir / 'validation')
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(f"Return code: {result.returncode}")
            
            # Extract metrics from output
            metrics = self.parse_validation_output(output_dir, struct_name)
            metrics['structure'] = struct_name
            metrics['validation_success'] = result.returncode == 0
            
            self.metrics.append(metrics)
            
        except Exception as e:
            print(f"Error: {e}")
            self.metrics.append({
                'structure': struct_name,
                'validation_success': False,
                'error': str(e)
            })
    
    def parse_validation_output(self, output_dir, struct_name):
        """Parse validation output files for metrics"""
        metrics = {}
        
        # Look for JSON output
        json_files = list(output_dir.glob('*.json'))
        for jf in json_files:
            try:
                with open(jf) as f:
                    data = json.load(f)
                    # Extract relevant metrics
                    if isinstance(data, dict):
                        self.extract_from_dict(data, metrics)
            except:
                pass
        
        # Parse text output
        text_files = list(output_dir.glob('*.txt'))
        for tf in text_files:
            try:
                with open(tf) as f:
                    content = f.read()
                    self.extract_from_text(content, metrics)
            except:
                pass
        
        # Check for PDF (indicates successful report generation)
        pdf_files = list(output_dir.glob('*.pdf'))
        metrics['pdf_generated'] = len(pdf_files) > 0
        
        return metrics
    
    def extract_from_dict(self, data, metrics, prefix=''):
        """Recursively extract numeric metrics from dict"""
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, (int, float)):
                metrics[full_key] = value
            elif isinstance(value, dict):
                self.extract_from_dict(value, metrics, full_key)
            elif isinstance(value, list) and value and isinstance(value[0], (int, float)):
                metrics[f"{full_key}.mean"] = np.mean(value)
                metrics[f"{full_key}.std"] = np.std(value)
    
    def extract_from_text(self, text, metrics):
        """Extract metrics from text output using patterns"""
        # Look for common patterns like "Score: 0.85" or "RMSD = 2.3"
        patterns = [
            r'(\w+)\s*:\s*([\d.]+)',
            r'(\w+)\s*=\s*([\d.]+)',
            r'(\w+)\s*score\s*:\s*([\d.]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                key = match.group(1).lower()
                value = float(match.group(2))
                if key not in metrics:
                    metrics[key] = value
    
    def analyze_all(self, structure_dir):
        """Analyze all structures in directory"""
        structures = list(Path(structure_dir).glob('*.cif'))
        print(f"\nFound {len(structures)} structures to analyze")
        
        for struct in structures:
            self.validate_and_extract(struct)
        
        # Save results
        self.save_results()
        self.generate_analysis()
    
    def save_results(self):
        """Save extracted metrics"""
        df = pd.DataFrame(self.metrics)
        
        output_file = 'analysis/data/extracted_metrics.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✓ Metrics saved to {output_file}")
        
        # Also save as JSON for detailed view
        json_file = 'analysis/data/extracted_metrics.json'
        with open(json_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"✓ Detailed data saved to {json_file}")
        
        return df
    
    def generate_analysis(self):
        """Generate statistical analysis"""
        df = pd.DataFrame(self.metrics)
        
        print(f"\n{'='*60}")
        print("STATISTICAL SUMMARY")
        print(f"{'='*60}")
        
        print(f"\nTotal structures analyzed: {len(df)}")
        print(f"Successful validations: {df['validation_success'].sum()}")
        print(f"Success rate: {df['validation_success'].mean()*100:.1f}%")
        
        if 'pdf_generated' in df.columns:
            print(f"PDF reports generated: {df['pdf_generated'].sum()}")
        
        # Analyze numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\nNumeric metrics found: {len(numeric_cols)}")
            print("\nMetric Statistics:")
            print(df[numeric_cols].describe())
        
        # Save summary
        summary = {
            'total_structures': len(df),
            'successful_validations': int(df['validation_success'].sum()),
            'success_rate': float(df['validation_success'].mean()),
            'metrics_extracted': len(numeric_cols),
            'structures_analyzed': df['structure'].tolist()
        }
        
        with open('analysis/data/summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Summary saved to analysis/data/summary.json")

if __name__ == '__main__':
    extractor = MetricExtractor()
    
    # Analyze extended test data if available, otherwise use original
    if Path('test-data-extended').exists():
        extractor.analyze_all('test-data-extended')
    else:
        extractor.analyze_all('test-data')
