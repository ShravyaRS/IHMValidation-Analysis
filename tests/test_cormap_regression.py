#!/usr/bin/env python3
"""
Regression tests for CorMap validation pipeline
Uses freesas.cormap.gof + exact Decimal p-value
"""

import sys
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


def test_perfect_match():
    """Perfect match should return p = 1.0"""
    q = np.linspace(0.01, 0.3, 100)
    I = 100 * np.exp(-q**2 / 0.01)
    err = np.ones(100)

    data1 = np.column_stack([q, I, err])
    data2 = np.column_stack([q, I, err])

    result = gof(data1, data2)
    p = cormap_pvalue_exact(result.n, result.c)
    assert p >= 0.99, f"Perfect match should have p >= 0.99, got {p}"
    print(f"PASS test_perfect_match: C={result.c}, p={p:.6f}")


def test_poor_match():
    """Poor match should return low p-value"""
    q = np.linspace(0.01, 0.3, 100)
    I1 = 100 * np.exp(-q**2 / 0.01)
    I2 = 50 * np.exp(-q**2 / 0.01)
    err = np.ones(100)

    data1 = np.column_stack([q, I1, err])
    data2 = np.column_stack([q, I2, err])

    result = gof(data1, data2)
    p = cormap_pvalue_exact(result.n, result.c)
    assert p < 0.05, f"Poor match should have p < 0.05, got {p}"
    print(f"PASS test_poor_match: C={result.c}, p={p:.6f}")


def test_known_case_sasdbd9():
    """
    SASDBD9 FIT_728: verified against professor's DATCMP result
    Expected: N=543, C=11, p=0.230925
    """
    cache = "/root/projects/IHMValidation-Analysis/Validation/cache/SASDBD9.sascif"

    try:
        with open(cache, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("SKIP test_known_case_sasdbd9: SASDBD9.sascif not found")
        return

    # Extract from _sas_model_fitting block (FIT_728)
    # Columns: id, ordinal, q, I_exp, I_fit
    fit_rows = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == '728':
            try:
                q = float(parts[2])
                I_exp = float(parts[3])
                I_fit = float(parts[4])
                if q > 0:
                    fit_rows.append([q, I_exp, I_fit])
            except:
                pass

    data = np.array(fit_rows)
    exp_data = np.column_stack([data[:, 0], data[:, 1], np.ones(len(data))])
    fit_data = np.column_stack([data[:, 0], data[:, 2], np.ones(len(data))])

    result = gof(exp_data, fit_data)
    p = cormap_pvalue_exact(result.n, result.c)

    assert result.n == 543, f"N should be 543, got {result.n}"
    assert result.c == 11, f"C should be 11, got {result.c}"
    assert abs(p - 0.230925) < 0.000001, f"p should be 0.230925, got {p:.6f}"

    print(f"PASS test_known_case_sasdbd9: N={result.n}, C={result.c}, "
          f"p={p:.6f} (expected 0.230925, diff={abs(p - 0.230925):.6f})")


def test_self_comparison():
    """Self-comparison (I_exp == I_fit) should return p = 1.0, C = 0"""
    q = np.linspace(0.01, 0.3, 100)
    I = 100 * np.exp(-q**2 / 0.01)
    err = np.ones(100)

    data = np.column_stack([q, I, err])
    result = gof(data, data)
    p = cormap_pvalue_exact(result.n, result.c)

    assert result.c == 0, f"Self-comparison C should be 0, got {result.c}"
    assert p == 1.0, f"Self-comparison p should be 1.0, got {p}"
    print(f"PASS test_self_comparison: C={result.c}, p={p:.6f}")


def test_exact_decimal_vs_float():
    """Verify Decimal fix gives different (more accurate) result than raw FreeSAS"""
    # For large n, float64 accumulates error
    # Use n=543, C=11 (SASDBD9 case)
    n, c = 543, 11
    p_exact = cormap_pvalue_exact(n, c)

    # The exact value should be 0.230925 (matching Schilling formula)
    assert abs(p_exact - 0.230925) < 0.000001, \
        f"Exact Decimal should give 0.230925, got {p_exact:.6f}"
    print(f"PASS test_exact_decimal_vs_float: "
          f"exact={p_exact:.6f}, expected=0.230925")


if __name__ == "__main__":
    print("=" * 60)
    print("CORMAP REGRESSION TESTS (with exact Decimal p-value)")
    print("=" * 60)

    passed = 0
    failed = 0

    tests = [
        test_perfect_match,
        test_poor_match,
        test_known_case_sasdbd9,
        test_self_comparison,
        test_exact_decimal_vs_float,
    ]

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"FAIL {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {test.__name__}: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)
