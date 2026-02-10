#!/usr/bin/env python3
"""
Test freesas cormap on SASDBD9 to verify it matches DATCMP
"""

import numpy as np
from freesas.cormap import gof

# Load the data we extracted earlier
cache_file = "/root/projects/IHMValidation-Analysis/Validation/cache/SASDBD9.sascif"

with open(cache_file, 'r') as f:
    lines = f.readlines()

# Extract experimental data
exp_data = []
for i in range(125, 685):
    parts = lines[i].split()
    if len(parts) >= 4:
        q = float(parts[1])
        I = float(parts[2])
        sigma = float(parts[3])
        exp_data.append([q, I, sigma])

exp_data = np.array(exp_data)

# Extract fitted data (FIT_728)
fit_data = []
for i in range(1312, 1856):
    parts = lines[i].split()
    if len(parts) >= 4:
        q = float(parts[2])
        I_fit = float(parts[3])
        fit_data.append([q, I_fit])

fit_data = np.array(fit_data)

print("="*80)
print("FREESAS CORMAP TEST ON SASDBD9")
print("="*80)
print(f"Experimental points: {len(exp_data)}")
print(f"Fitted points: {len(fit_data)}")

# Check what gof expects
import inspect
print(f"\ngof signature: {inspect.signature(gof)}")

# freesas gof expects two arrays of same length
# We need to align the q values first
# Find common q range
q_exp = exp_data[:, 0]
I_exp = exp_data[:, 1]
sigma_exp = exp_data[:, 2]

q_fit = fit_data[:, 0]
I_fit = fit_data[:, 1]

# Interpolate fit to experimental q points
I_fit_interp = np.interp(q_exp, q_fit, I_fit)

# Create aligned arrays for freesas
# gof expects arrays of [q, I, sigma] format
data1 = np.column_stack([q_exp, I_exp, sigma_exp])
data2 = np.column_stack([q_exp, I_fit_interp, sigma_exp])

print(f"\nAligned data shape: {data1.shape}")

# Run freesas cormap
try:
    result = gof(data1, data2)
    print(f"\nFreeSAS CorMap Result:")
    print(f"  Result object: {result}")
    print(f"  Type: {type(result)}")
    
    # Check attributes
    if hasattr(result, '__dict__'):
        print(f"  Attributes: {result.__dict__}")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("ALSO TESTING VIA COMMAND LINE")
print("="*80)

# Save files and test via command line
np.savetxt('/tmp/sasdbd9_exp.dat', 
           np.column_stack([q_exp, I_exp, sigma_exp]),
           fmt='%.6e')

np.savetxt('/tmp/sasdbd9_fit.dat',
           np.column_stack([q_exp, I_fit_interp, sigma_exp]),
           fmt='%.6e')

import subprocess
result_cmd = subprocess.run(
    ['cormapy', '/tmp/sasdbd9_exp.dat', '/tmp/sasdbd9_fit.dat'],
    capture_output=True, text=True
)
print(f"cormapy output:\n{result_cmd.stdout}")
if result_cmd.stderr:
    print(f"stderr: {result_cmd.stderr}")

print("="*80)
print("EXPECTED (from professor):")
print("  DATCMP: p = 0.230925, C = 11")
print("="*80)
