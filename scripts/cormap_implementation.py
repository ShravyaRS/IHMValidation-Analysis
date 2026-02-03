#!/usr/bin/env python3
"""
CorMap (Correlation Map) Implementation
Based on: Franke et al. (2015) Nature Methods
https://doi.org/10.1038/nmeth.3358
"""

import numpy as np
from scipy import stats

def cormap_test(exp_q, exp_I, exp_err, fit_q, fit_I):
    """
    Perform CorMap test between experimental and fitted SAS data
    
    Parameters:
    -----------
    exp_q : array-like
        Experimental momentum transfer values
    exp_I : array-like
        Experimental intensities
    exp_err : array-like
        Experimental errors
    fit_q : array-like
        Fitted momentum transfer values
    fit_I : array-like
        Fitted intensities
    
    Returns:
    --------
    p_value : float
        CorMap p-value
    c_value : float
        Number of runs (longest contiguous stretch)
    n_points : int
        Number of points used in comparison
    """
    
    # Ensure arrays
    exp_q = np.asarray(exp_q)
    exp_I = np.asarray(exp_I)
    exp_err = np.asarray(exp_err)
    fit_q = np.asarray(fit_q)
    fit_I = np.asarray(fit_I)
    
    # Interpolate fitted data to experimental q points
    fit_I_interp = np.interp(exp_q, fit_q, fit_I)
    
    # Calculate normalized residuals
    # Avoid division by zero
    valid_mask = exp_err > 0
    if not np.any(valid_mask):
        return None, None, 0
    
    exp_q = exp_q[valid_mask]
    exp_I = exp_I[valid_mask]
    exp_err = exp_err[valid_mask]
    fit_I_interp = fit_I_interp[valid_mask]
    
    residuals = (exp_I - fit_I_interp) / exp_err
    
    # Convert to binary sequence (+1 if residual > 0, -1 if residual < 0)
    signs = np.sign(residuals)
    
    # Remove any zero residuals
    signs = signs[signs != 0]
    
    n = len(signs)
    
    if n < 2:
        return None, None, n
    
    # Count runs (changes in sign)
    sign_changes = np.diff(signs) != 0
    n_runs = np.sum(sign_changes) + 1
    
    # Calculate the longest run (C statistic)
    runs = []
    current_run = 1
    for i in range(1, n):
        if signs[i] == signs[i-1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    runs.append(current_run)
    
    c_value = max(runs) if runs else 1
    
    # Calculate p-value using the CorMap formula
    # P(C >= c) = probability of longest run being >= c by chance
    # Using the formula: P ≈ 2(n - c + 1) * (1/2)^c
    
    p_value = 2.0 * (n - c_value + 1) * (0.5 ** c_value)
    
    # Ensure p-value is in [0, 1]
    p_value = min(p_value, 1.0)
    p_value = max(p_value, 0.0)
    
    return p_value, c_value, n

def cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I):
    """
    Wrapper for CorMap test matching DATCMP output format
    
    Returns:
    --------
    dict with keys: p_value, c_value, n_points, status
    """
    try:
        # Find common q-range
        q_min = max(exp_q.min(), fit_q.min())
        q_max = min(exp_q.max(), fit_q.max())
        
        # Filter to common range
        exp_mask = (exp_q >= q_min) & (exp_q <= q_max)
        fit_mask = (fit_q >= q_min) & (fit_q <= q_max)
        
        exp_q_common = exp_q[exp_mask]
        exp_I_common = exp_I[exp_mask]
        exp_err_common = exp_err[exp_mask]
        
        fit_q_common = fit_q[fit_mask]
        fit_I_common = fit_I[fit_mask]
        
        if len(exp_q_common) < 3:
            return {
                'p_value': None,
                'c_value': None,
                'n_points': 0,
                'status': 'undefined'
            }

        
        p_value, c_value, n_points = cormap_test(
            exp_q_common, exp_I_common, exp_err_common,
            fit_q_common, fit_I_common
        )
        
        return {
            'p_value': p_value,
            'c_value': c_value,
            'n_points': n_points,
            'status': 'success' if p_value is not None else 'undefined'
        }
        
    except Exception as e:
        return {
            'p_value': None,
            'c_value': None,
            'n_points': 0,
            'status': f'error: {str(e)}'
        }


if __name__ == "__main__":
    # Test with simple data
    import matplotlib.pyplot as plt
    
    # Generate test data
    q = np.linspace(0.01, 0.3, 100)
    I_exp = 100 * np.exp(-q**2 / 0.01) + np.random.normal(0, 5, 100)
    I_fit = 100 * np.exp(-q**2 / 0.01)
    err = np.ones_like(q) * 5
    
    result = cormap_pairwise(q, I_exp, err, q, I_fit)
    
    print("CorMap Test Results:")
    print(f"  P-value: {result['p_value']}")
    print(f"  C-value (longest run): {result['c_value']}")
    print(f"  N points: {result['n_points']}")
    print(f"  Status: {result['status']}")
