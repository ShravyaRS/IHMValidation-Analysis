#!/usr/bin/env python3
"""
Test the p-value calculation formula
"""

import numpy as np
from scipy import stats

# Test case: C=11, N=497 (from SASDBD9)
C = 11
N = 497

print("="*80)
print("CORMAP P-VALUE FORMULA TEST")
print("="*80)
print(f"\nInput: C={C}, N={N}")

# Our current formula: P(C >= c) = 2(N - C + 1) * (1/2)^C
our_p = 2.0 * (N - C + 1) * (0.5 ** C)
print(f"\nOur formula: P = 2(N - C + 1) * (1/2)^C")
print(f"  Result: {our_p:.6f}")

# DATCMP result
datcmp_p = 0.230925
print(f"\nDATCMP result: {datcmp_p:.6f}")

# Difference
print(f"\nDifference: {abs(our_p - datcmp_p):.6f}")

# Let me check the correct CorMap formula from the paper
# Franke et al. (2015) Nature Methods
# The formula is: P(C >= c | n) = 2 * sum_{i=c}^{n} (n-1 choose i-1) * (1/2)^(n-1)

print("\n" + "="*80)
print("TESTING ALTERNATIVE FORMULAS")
print("="*80)

# Method 1: Exact combinatorial (from paper)
# P(C >= c) = 2 * sum from i=c to n of: C(n-1, i-1) * 0.5^(n-1)
from math import comb

def cormap_exact(C, N):
    """Exact CorMap p-value from the paper"""
    p_value = 0.0
    for i in range(C, N+1):
        p_value += comb(N-1, i-1)
    p_value *= 2.0 * (0.5 ** (N-1))
    return p_value

exact_p = cormap_exact(C, N)
print(f"\nMethod 1 - Exact combinatorial:")
print(f"  P = 2 * sum(C(N-1, i-1)) * 0.5^(N-1) for i=C to N")
print(f"  Result: {exact_p:.6f}")
print(f"  Diff from DATCMP: {abs(exact_p - datcmp_p):.6f}")

# Method 2: Using scipy.stats (binomial test)
# The runs test is related to binomial distribution
# P(longest run >= C) 
print(f"\nMethod 2 - Approximation used in some implementations:")

# For large N, approximate with normal distribution
# Mean of longest run ≈ log2(N)
# Variance ≈ complicated formula

# Method 3: Check if DATCMP uses a different N
# Maybe DATCMP uses different point count?
print(f"\nMethod 3 - Testing with different N values:")
for test_N in [497, 496, 498, 500, 490]:
    test_p = cormap_exact(C, test_N)
    diff = abs(test_p - datcmp_p)
    print(f"  N={test_N}: p={test_p:.6f}, diff={diff:.6f}")

print("\n" + "="*80)
print("INVESTIGATING THE DISCREPANCY")
print("="*80)

# Check the original paper formula more carefully
# Perhaps there's a two-tailed vs one-tailed issue?

# One-tailed (as we calculate)
one_tail = cormap_exact(C, N)
print(f"\nOne-tailed test (C >= 11): {one_tail:.6f}")

# Maybe DATCMP uses a different correction?
# Let me check if there's a continuity correction

# Or check if it's about runs vs longest run
# In the runs test, we count number of runs, not longest run
# Let me recalculate assuming we need to count total runs

print("\n" + "="*80)

# Actually, let me verify what our implementation is actually calculating
print("Checking what C-value actually represents...")
print(f"C = {C} means: the longest consecutive sequence of same-sign residuals")
print(f"N = {N} means: total number of data points after filtering")

# The exact formula should be what I implemented above
# Let me test if the issue is overflow/underflow

print(f"\nTesting numerical stability:")
print(f"  0.5^{N-1} = {0.5**(N-1)}")
print(f"  This is effectively 0 (underflow)")

# For large N, we need to use log probabilities
import math

def cormap_log_exact(C, N):
    """CorMap p-value using log probabilities to avoid underflow"""
    log_prob = math.log(2.0) - (N-1) * math.log(2.0)  # log(2 * 0.5^(N-1))
    
    # Sum the binomial coefficients
    total_comb = 0.0
    for i in range(C, N+1):
        total_comb += comb(N-1, i-1)
    
    p_value = total_comb * math.exp(log_prob)
    return p_value

log_p = cormap_log_exact(C, N)
print(f"\nMethod with log probabilities: {log_p:.6f}")
print(f"Diff from DATCMP: {abs(log_p - datcmp_p):.6f}")
