#!/usr/bin/env python3
"""
Extract SASDBD9 data correctly from .sascif file
Uses FIT block q-grid to avoid interpolation artifacts
"""

import numpy as np
import subprocess
from freesas.cormap import gof

cache_file = "/root/projects/IHMValidation-Analysis/Validation/cache/SASDBD9.sascif"

with open(cache_file, 'r') as f:
    lines = f.readlines()

print("="*80)
print("EXTRACTING SASDBD9 DATA FROM SASCIF")
print("="*80)

# The FIT_728 block contains:
# Format: fit_id  point_id  q  I_exp  I_fit
fit_block = []
for line in lines:
    parts = line.split()
    if len(parts) >= 4 and parts[0] == '728':
        fit_block.append(parts)

print(f"FIT_728 block points: {len(fit_block)}")

# Filter out padding points where I_exp = 0
valid_rows = []
for row in fit_block:
    if len(row) >= 5:
        q     = float(row[2])
        I_exp = float(row[3])
        I_fit = float(row[4])
        if I_exp != 0.0:
            valid_rows.append([q, I_exp, I_fit])

valid_data = np.array(valid_rows)
print(f"Valid points (non-zero experimental): {len(valid_data)}")
print(f"q range: [{valid_data[0,0]:.6e}, {valid_data[-1,0]:.6e}]")

# Get experimental errors from scan block (scan_id=492)
exp_block = []
for line in lines:
    parts = line.split()
    if len(parts) == 5 and parts[-1] == '492':
        try:
            q     = float(parts[1])
            I     = float(parts[2])
            sigma = float(parts[3])
            exp_block.append([q, I, sigma])
        except:
            pass

exp_array = np.array(exp_block)
print(f"Experimental block points: {len(exp_array)}")

# Match q-values to get sigma for each point
matched_exp = []
matched_fit = []

for row in valid_rows:
    q_target = row[0]
    I_exp    = row[1]
    I_fit    = row[2]
    
    idx   = np.argmin(np.abs(exp_array[:, 0] - q_target))
    sigma = exp_array[idx, 2]
    
    matched_exp.append([q_target, I_exp, sigma])
    matched_fit.append([q_target, I_fit, sigma])

matched_exp = np.array(matched_exp)
matched_fit = np.array(matched_fit)

print(f"Matched points: {len(matched_exp)}")

# Run freesas cormap
print("\n" + "="*80)
print("FREESAS CORMAP TEST")
print("="*80)

result = gof(matched_exp, matched_fit)
print(f"FreeSAS result: C={result.c}, p={result.P:.6f}")

# Also test via command line
np.savetxt('/tmp/sasdbd9_exp.dat', matched_exp, fmt='%.6e')
np.savetxt('/tmp/sasdbd9_fit.dat', matched_fit, fmt='%.6e')

cmd_result = subprocess.run(
    ['cormapy', '/tmp/sasdbd9_exp.dat', '/tmp/sasdbd9_fit.dat'],
    capture_output=True, text=True
)
print(f"\ncormapy output:\n{cmd_result.stdout}")

print("="*80)
print("COMPARISON")
print("="*80)
print(f"Professor's DATCMP:   p = 0.230925, C = 11")
print(f"FreeSAS result:       p = {result.P:.6f}, C = {result.c}")
diff = abs(result.P - 0.230925)
print(f"Difference:           {diff:.6f}")

if diff < 0.01:
    print("Status: WITHIN 0.01 TOLERANCE")
elif diff < 0.05:
    print("Status: WITHIN 0.05 TOLERANCE")
else:
    print("Status: OUTSIDE TOLERANCE - Still investigating")

print("="*80)

# Save corrected files
np.savetxt('validation_comparison/extracted_data/SASDBD9_exp.dat',
           matched_exp, fmt='%.6e', header='q I sigma')
np.savetxt('validation_comparison/extracted_data/SASDBD9_fit.dat',
           matched_fit, fmt='%.6e', header='q I_fit sigma')

print("\nFiles saved to validation_comparison/extracted_data/")
