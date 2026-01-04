#!/usr/bin/env python3
"""
Automated batch validation pipeline for IHM structures
Analyzes multiple structures and compares validation results
"""
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
import sys
class ValidationPipeline:
def init(self, structures_dir, output_dir):
self.structures_dir = Path(structures_dir)
self.output_dir = Path(output_dir)
self.results = []
def validate_structure(self, structure_file):
"""Run validation on a single structure"""
print(f"\nValidating {structure_file.name}...")
result = {
'structure': structure_file.name,
'timestamp': datetime.now().isoformat(),
'success': False,
'errors': [],
'metrics': {}
}
try:
Run validation
cmd = [
'singularity', 'exec',
'IHMValidation/ihmvalidation.sif',
'ihm_validate',
str(structure_file),
'-o', str(self.output_dir / structure_file.stem)
]
proc = subprocess.run(
cmd,
capture_output=True,
text=True,
timeout=300 # 5 min timeout
)
result['return_code'] = proc.returncode
result['success'] = proc.returncode == 0
if proc.stderr:
result['errors'] = proc.stderr.split('\n')
Parse output for metrics
result['metrics'] = self.extract_metrics(structure_file.stem)
except subprocess.TimeoutExpired:
result['errors'].append('Validation timeout (5 min)')
except Exception as e:
result['errors'].append(str(e))
self.results.append(result)
return result
def extract_metrics(self, structure_name):
"""Extract validation metrics from output"""
metrics = {}
Look for validation output files
json_file = self.output_dir / f"{structure_name}_validation.json"
if json_file.exists():
try:
with open(json_file) as f:
data = json.load(f)
Extract relevant metrics
metrics['has_data'] = True
Add specific metric extraction here
except:
pass
return metrics
def run_batch(self):
"""Run validation on all structures"""
structures = list(self.structures_dir.glob('*.cif'))
print(f"Found {len(structures)} structures to validate")
for structure in structures:
self.validate_structure(structure)
Save results
self.save_results()
self.generate_summary()
def save_results(self):
"""Save detailed results"""
output_file = self.output_dir / 'validation_results.json'
with open(output_file, 'w') as f:
json.dump(self.results, f, indent=2)
print(f"\nResults saved to {output_file}")
def generate_summary(self):
"""Generate summary statistics"""
total = len(self.results)
successful = sum(1 for r in self.results if r['success'])
summary = {
'total_structures': total,
'successful_validations': successful,
'failed_validations': total - successful,
'success_rate': f"{successful/total*100:.1f}%" if total > 0 else "0%",
'timestamp': datetime.now().isoformat()
}
Save summary
summary_file = self.output_dir / 'summary.json'
with open(summary_file, 'w') as f:
json.dump(summary, f, indent=2)
Print summary
print("\n" + "="*60)
print("VALIDATION SUMMARY")
print("="*60)
print(f"Total Structures: {summary['total_structures']}")
print(f"Successful: {summary['successful_validations']}")
print(f"Failed: {summary['failed_validations']}")
print(f"Success Rate: {summary['success_rate']}")
print("="*60)
if name == 'main':
pipeline = ValidationPipeline('test-data', 'analysis/results')
pipeline.run_batch()
