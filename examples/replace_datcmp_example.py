#!/usr/bin/env python3
"""
Example: Replace DATCMP with FreeSAS cormapy + exact Decimal p-value

This shows how to compute CorMap p-values without ATSAS/DATCMP,
using FreeSAS for N and C, and exact Decimal arithmetic for the p-value.
"""

import numpy as np
from decimal import Decimal, getcontext
from freesas.cormap import gof

getcontext().prec = 100


def cormap_pvalue_exact(n, c_longest):
    """Exact CorMap p-value using Schilling (1990) recursion with Decimal."""
    k = c_longest - 1
    if k > n:
        return 0.0
    if k <= 0:
        return 1.0
    f = [Decimal(0)] * (n + 1)
    for i in range(min(k, n + 1)):
        f[i] = Decimal(2) ** i
    for i in range(k, n + 1):
        f[i] = sum(f[i - j] for j in range(1, k + 1))
    return float(Decimal(1) - f[n] / Decimal(2) ** n)


def cormap_test(exp_file, fit_file):
    """Run CorMap test on two data files (q, I, sigma) format."""
    exp = np.loadtxt(exp_file)
    fit = np.loadtxt(fit_file)

    # Get N and C from FreeSAS
    result = gof(exp, fit)

    # Recompute p-value with exact arithmetic
    p_exact = cormap_pvalue_exact(result.n, result.c)

    return result.n, result.c, p_exact


if __name__ == "__main__":
    # Example: generate synthetic data
    np.random.seed(42)
    n_points = 100
    q = np.linspace(0.01, 0.5, n_points)
    I_exp = 1000 * np.exp(-q * 10) + np.random.normal(0, 5, n_points)
    I_fit = 1000 * np.exp(-q * 10)

    # Save to temp files
    exp_data = np.column_stack([q, I_exp, np.ones(n_points)])
    fit_data = np.column_stack([q, I_fit, np.ones(n_points)])
    np.savetxt("/tmp/exp.dat", exp_data)
    np.savetxt("/tmp/fit.dat", fit_data)

    # Run CorMap
    n, c, p = cormap_test("/tmp/exp.dat", "/tmp/fit.dat")
    print(f"N = {n}, C = {c}, p = {p:.6f}")
    print(f"Conclusion: {'PASS' if p > 0.05 else 'FAIL'} (threshold = 0.05)")
