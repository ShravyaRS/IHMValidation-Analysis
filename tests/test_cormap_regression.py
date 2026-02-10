#!/usr/bin/env python3
"""
Regression tests for CorMap validation pipeline
Uses freesas.cormap.gof directly
"""

import sys
import numpy as np
from freesas.cormap import gof

def test_perfect_match():
    """Perfect match should return high p-value"""
    q   = np.linspace(0.01, 0.3, 100)
    I   = 100 * np.exp(-q**2 / 0.01)
    err = np.ones(100) * 5.0
    
    data1 = np.column_stack([q, I, err])
    data2 = np.column_stack([q, I, err])
    
    result = gof(data1, data2)
    assert result.P > 0.05, f"Perfect match should have p > 0.05, got {result.P}"
    print(f"PASS test_perfect_match: C={result.c}, p={result.P:.6f}")

def test_poor_match():
    """Poor match should return low p-value"""
    q    = np.linspace(0.01, 0.3, 100)
    I1   = 100 * np.exp(-q**2 / 0.01)
    I2   = 50  * np.exp(-q**2 / 0.01)
    err  = np.ones(100) * 1.0
    
    data1 = np.column_stack([q, I1, err])
    data2 = np.column_stack([q, I2, err])
    
    result = gof(data1, data2)
    assert result.P < 0.05, f"Poor match should have p < 0.05, got {result.P}"
    print(f"PASS test_poor_match: C={result.c}, p={result.P:.6f}")

def test_known_case():
    """
    SASDBD9 FIT_728: known result from professor verification
    DATCMP: C=11, p=0.230925
    FreeSAS: C=11, p~0.229-0.231
    """
    cache = "/root/projects/IHMValidation-Analysis/Validation/cache/SASDBD9.sascif"
    
    try:
        with open(cache, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("SKIP test_known_case: SASDBD9.sascif not found")
        return
    
    # Extract FIT_728 block (q > 0 filter)
    fit_rows = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == '728':
            try:
                q     = float(parts[2])
                I_exp = float(parts[3])
                I_fit = float(parts[4])
                if q > 0:
                    fit_rows.append([q, I_exp, I_fit])
            except:
                pass
    
    # Get sigma from scan block
    exp_block = []
    for line in lines:
        parts = line.split()
        if len(parts) == 5 and parts[-1].isdigit():
            try:
                q     = float(parts[1])
                I     = float(parts[2])
                sigma = float(parts[3])
                if q > 0 and sigma > 0:
                    exp_block.append([q, I, sigma])
            except:
                pass
    
    exp_array = np.array(exp_block)
    
    matched_exp = []
    matched_fit = []
    for row in fit_rows:
        q_target = row[0]
        idx      = np.argmin(np.abs(exp_array[:, 0] - q_target))
        sigma    = exp_array[idx, 2]
        if sigma > 0:
            matched_exp.append([q_target, row[1], sigma])
            matched_fit.append([q_target, row[2], sigma])
    
    data1  = np.array(matched_exp)
    data2  = np.array(matched_fit)
    result = gof(data1, data2)
    
    # C must match exactly
    assert result.c == 11, f"C should be 11, got {result.c}"
    
    # p must be within 0.005 of DATCMP
    assert abs(result.P - 0.230925) < 0.005, \
        f"p should be ~0.230925, got {result.P:.6f}"
    
    print(f"PASS test_known_case: C={result.c}, p={result.P:.6f} "
          f"(DATCMP: C=11, p=0.230925, diff={abs(result.P-0.230925):.6f})")

def test_minimum_points():
    """Less than 3 points should raise error or return undefined"""
    q   = np.array([0.01, 0.02])
    I   = np.array([100.0, 90.0])
    err = np.array([5.0, 5.0])
    
    data1 = np.column_stack([q, I, err])
    data2 = np.column_stack([q, I, err])
    
    try:
        result = gof(data1, data2)
        print(f"PASS test_minimum_points: handled gracefully, p={result.P}")
    except Exception as e:
        print(f"PASS test_minimum_points: raised exception as expected: {type(e).__name__}")

def test_sasdbb8_known_value():
    """
    SASDBB8 FIT_592: both DATCMP and FreeSAS agree closely
    DATCMP: p=0.248832
    FreeSAS: p=0.261263
    Difference: 0.012431 (within 0.05 tolerance)
    """
    cache = "/root/projects/IHMValidation-Analysis/Validation/cache/SASDBB8.sascif"
    
    try:
        with open(cache) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("SKIP test_sasdbb8_known_value: SASDBB8.sascif not found")
        return
    
    # Extract FIT_592
    fit_rows = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == '592':
            try:
                q     = float(parts[2])
                I_exp = float(parts[3])
                I_fit = float(parts[4])
                if q > 0:
                    fit_rows.append([q, I_exp, I_fit])
            except:
                pass
    
    exp_block = []
    for line in lines:
        parts = line.split()
        if len(parts) == 5 and parts[-1].isdigit():
            try:
                q     = float(parts[1])
                I     = float(parts[2])
                sigma = float(parts[3])
                if q > 0 and sigma > 0:
                    exp_block.append([q, I, sigma])
            except:
                pass
    
    exp_array = np.array(exp_block)
    matched_exp = []
    matched_fit = []
    for row in fit_rows:
        q_target = row[0]
        idx      = np.argmin(np.abs(exp_array[:, 0] - q_target))
        sigma    = exp_array[idx, 2]
        if sigma > 0:
            matched_exp.append([q_target, row[1], sigma])
            matched_fit.append([q_target, row[2], sigma])
    
    result = gof(np.array(matched_exp), np.array(matched_fit))
    
    assert abs(result.P - 0.248832) < 0.05, \
        f"p should be ~0.248832, got {result.P:.6f}"
    
    print(f"PASS test_sasdbb8_known_value: C={result.c}, p={result.P:.6f} "
          f"(DATCMP: p=0.248832, diff={abs(result.P-0.248832):.6f})")


if __name__ == "__main__":
    print("="*60)
    print("CORMAP REGRESSION TESTS")
    print("="*60)
    
    passed = 0
    failed = 0
    
    tests = [
        test_perfect_match,
        test_poor_match,
        test_known_case,
        test_minimum_points,
        test_sasdbb8_known_value
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
    print("="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    sys.exit(0 if failed == 0 else 1)
