#!/usr/bin/env python3
"""
Comparative analysis of IHM validation results
Generates insights and visualizations
"""
import json
import pandas as pd
from pathlib import Path
class ValidationAnalyzer:
def init(self, results_file):
self.results_file = Path(results_file)
self.load_results()
def load_results(self):
"""Load validation results"""
with open(self.results_file) as f:
self.results = json.load(f)
self.df = pd.DataFrame(self.results)
def analyze_patterns(self):
"""Identify patterns in validation results"""
print("\nPATTERN ANALYSIS")
print("="*60)
Success patterns
if 'success' in self.df.columns:
print(f"\nSuccess Rate: {self.df['success'].mean()*100:.1f}%")
Common errors
all_errors = []
for result in self.results:
all_errors.extend(result.get('errors', []))
if all_errors:
print(f"\nTotal Errors: {len(all_errors)}")
Could add error frequency analysis here
print("="*60)
def generate_report(self):
"""Generate HTML report"""
html = f"""
        
        
            <title>IHM Validation Analysis</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                .metric {{ background: #ecf0f1; padding: 15px; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
            </style>
        
        
            IHM Validation Analysis Report
            
                Summary Statistics
                Total Structures: {len(self.results)}
                Successful: {sum(1 for r in self.results if r.get('success'))}
            
            Detailed Results
            
        """
for result in self.results:
status = "Success" if result.get('success') else "Failed"
errors = len(result.get('errors', []))
html += f"""
                
            """
html += """
            StructureStatusErrors{result['structure']}{status}{errors}
        
        
        """
report_file = self.results_file.parent / 'analysis_report.html'
with open(report_file, 'w') as f:
f.write(html)
print(f"\nReport generated: {report_file}")
if name == 'main':
analyzer = ValidationAnalyzer('analysis/results/validation_results.json')
analyzer.analyze_patterns()
analyzer.generate_report()
