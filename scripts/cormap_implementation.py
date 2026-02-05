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
    
    Returns:
    --------
    p_value : float or None
    c_value : int or None
    n_points : int
    """
    
    # Ensure arrays
    exp_q = np.asarray(exp_q)
    exp_I = np.asarray(exp_I)
    exp_err = np.asarray(exp_err)
    fit_q = np.asarray(fit_q)
    fit_I = np.asarray(fit_I)
    
    # Check for valid data
    if len(exp_q) == 0 or len(fit_q) == 0:
        return None, None, 0
    
    # Interpolate fitted data to experimental q points
    fit_I_interp = np.interp(exp_q, fit_q, fit_I)
    
    # Filter out zero or invalid errors
    valid_mask = (exp_err > 0) & np.isfinite(exp_err)
    if not np.any(valid_mask):
        return None, None, len(exp_q)
    
    exp_q = exp_q[valid_mask]
    exp_I = exp_I[valid_mask]
    exp_err = exp_err[valid_mask]
    fit_I_interp = fit_I_interp[valid_mask]
    
    # Calculate normalized residuals
    residuals = (exp_I - fit_I_interp) / exp_err
    
    # Special case: perfect match (all residuals ~0)
    if np.all(np.abs(residuals) < 1e-10):
        # Perfect agreement - return p=1.0
        return 1.0, 1, len(residuals)
    
    # Convert to binary sequence
    signs = np.sign(residuals)
    
    # Remove zeros
    signs = signs[signs != 0]
    
    n = len(signs)
    
    # Need at least 3 points for meaningful CorMap test
    if n < 3:
        return None, None, n
    
    # Count runs
    sign_changes = np.diff(signs) != 0
    n_runs = np.sum(sign_changes) + 1
    
    # Calculate longest run (C statistic)
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
    
    # Calculate p-value: P(C >= c) = 2(n - c + 1) * (1/2)^c
    p_value = 2.0 * (n - c_value + 1) * (0.5 ** c_value)
    
    # Ensure p-value is in [0, 1]
    p_value = min(max(p_value, 0.0), 1.0)
    
    return p_value, c_value, n


def cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I):
    """
    Wrapper for CorMap test with proper status handling
    
    Returns:
    --------
    dict with keys: p_value, c_value, n_points, status
    """
    try:
        # Ensure arrays
        exp_q = np.asarray(exp_q, dtype=float)
        exp_I = np.asarray(exp_I, dtype=float)
        exp_err = np.asarray(exp_err, dtype=float)
        fit_q = np.asarray(fit_q, dtype=float)
        fit_I = np.asarray(fit_I, dtype=float)
        
        # Check for empty arrays
        if len(exp_q) == 0 or len(fit_q) == 0:
            return {
                'p_value': None,
                'c_value': None,
                'n_points': 0,
                'status': 'insufficient_data'
            }
        
        # Find common q-range
        q_min = max(exp_q.min(), fit_q.min())
        q_max = min(exp_q.max(), fit_q.max())
        
        # Check for overlap
        if q_min >= q_max:
            return {
                'p_value': None,
                'c_value': None,
                'n_points': 0,
                'status': 'insufficient_data'
            }
        
        # Filter to common range
        exp_mask = (exp_q >= q_min) & (exp_q <= q_max)
        fit_mask = (fit_q >= q_min) & (fit_q <= q_max)
        
        exp_q_common = exp_q[exp_mask]
        exp_I_common = exp_I[exp_mask]
        exp_err_common = exp_err[exp_mask]
        
        fit_q_common = fit_q[fit_mask]
        fit_I_common = fit_I[fit_mask]
        
        # Check if we have enough overlap
        if len(exp_q_common) < 3:
            return {
                'p_value': None,
                'c_value': None,
                'n_points': len(exp_q_common),
                'status': 'insufficient_data'
            }
        
        # Run CorMap test
        p_value, c_value, n_points = cormap_test(
            exp_q_common, exp_I_common, exp_err_common,
            fit_q_common, fit_I_common
        )
        
        # Determine status
        if p_value is None:
            if n_points == 0:
                status = 'insufficient_data'
            elif n_points < 3:
                status = 'insufficient_data'
            else:
                status = 'undefined'
        else:
            status = 'success'
        
        return {
            'p_value': p_value,
            'c_value': c_value,
            'n_points': n_points,
            'status': status
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
