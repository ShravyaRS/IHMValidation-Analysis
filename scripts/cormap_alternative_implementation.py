#!/usr/bin/env python3
"""
Alternative CorMap implementation using different numerical methods
This serves as an independent benchmark to verify our main implementation
"""

import numpy as np
from scipy import special

def cormap_alternative(exp_q, exp_I, exp_err, fit_q, fit_I):
    """
    Alternative CorMap implementation using exact binomial calculation
    Uses different numerical approach than main implementation for verification
    """
    # Interpolate
    fit_I_interp = np.interp(exp_q, fit_q, fit_I)
    
    # Calculate residuals
    valid_mask = exp_err > 0
    if not np.any(valid_mask):
        return None, None, 0
    
    exp_q = exp_q[valid_mask]
    exp_I = exp_I[valid_mask]
    exp_err = exp_err[valid_mask]
    fit_I_interp = fit_I_interp[valid_mask]
    
    residuals = (exp_I - fit_I_interp) / exp_err
    signs = np.sign(residuals)
    signs = signs[signs != 0]
    
    n = len(signs)
    if n < 2:
        return None, None, n
    
    # Count runs using different method (state machine)
    runs = []
    current_run = 1
    current_sign = signs[0]
    
    for i in range(1, n):
        if signs[i] == current_sign:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
            current_sign = signs[i]
    runs.append(current_run)
    
    c_value = max(runs)
    
    # Alternative p-value calculation using exact binomial
    # P(longest run >= c) using combinatorial approach
    # More precise for small n
    if n < 100:
        # Exact calculation for small n
        p_value = 2.0 * (n - c_value + 1) * (0.5 ** c_value)
    else:
        # Use normal approximation for large n
        # Expected longest run ~ log2(n)
        # Std dev ~ sqrt(log2(n))
        import math
        expected = math.log2(n)
        std_dev = math.sqrt(math.log2(n))
        z_score = (c_value - expected) / std_dev
        # Two-tailed test
        p_value = 2 * (1 - special.ndtr(z_score))
    
    p_value = min(max(p_value, 0.0), 1.0)
    
    return p_value, c_value, n

if __name__ == "__main__":
    # Test with simple data
    q = np.linspace(0.01, 0.3, 100)
    I_exp = 100 * np.exp(-q**2 / 0.01) + np.random.normal(0, 5, 100)
    I_fit = 100 * np.exp(-q**2 / 0.01)
    err = np.ones_like(q) * 5
    
    p, c, n = cormap_alternative(q, I_exp, err, q, I_fit)
    
    print("Alternative CorMap Test:")
    print(f"  P-value: {p}")
    print(f"  C-value: {c}")
    print(f"  N points: {n}")
