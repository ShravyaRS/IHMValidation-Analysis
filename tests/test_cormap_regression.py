
#!/usr/bin/env python3
"""
Regression tests for CorMap implementation
Ensures reproducibility and catches breaking changes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import numpy as np
from cormap_implementation import cormap_pairwise

# Reference test cases with expected results
REFERENCE_CASES = [
    {
        'name': 'perfect_match',
        'exp_q': np.linspace(0.01, 0.3, 100),
        'exp_I': 100 * np.exp(-np.linspace(0.01, 0.3, 100)**2 / 0.01),
        'exp_err': np.ones(100) * 1.0,
        'fit_q': np.linspace(0.01, 0.3, 100),
        'fit_I': 100 * np.exp(-np.linspace(0.01, 0.3, 100)**2 / 0.01),
        'expected_p_range': (0.9, 1.0),  # Should be very high
        'expected_status': 'success'
    },
    {
        'name': 'poor_match',
        'exp_q': np.linspace(0.01, 0.3, 100),
        'exp_I': 100 * np.exp(-np.linspace(0.01, 0.3, 100)**2 / 0.01),
        'exp_err': np.ones(100) * 1.0,
        'fit_q': np.linspace(0.01, 0.3, 100),
        'fit_I': 50 * np.exp(-np.linspace(0.01, 0.3, 100)**2 / 0.01),  # Wrong amplitude
        'expected_p_range': (0.0, 0.001),  # Should be very low
        'expected_status': 'success'
    },
    {
        'name': 'no_overlap',
        'exp_q': np.linspace(0.01, 0.1, 50),
        'exp_I': np.ones(50) * 100,
        'exp_err': np.ones(50) * 1.0,
        'fit_q': np.linspace(0.2, 0.3, 50),
        'fit_I': np.ones(50) * 100,
        'expected_p': None,
        'expected_status': 'insufficient_data'
    },
    {
        'name': 'zero_errors',
        'exp_q': np.linspace(0.01, 0.3, 100),
        'exp_I': np.ones(100) * 100,
        'exp_err': np.zeros(100),  # All zeros
        'fit_q': np.linspace(0.01, 0.3, 100),
        'fit_I': np.ones(100) * 100,
        'expected_p': None,
        'expected_status': 'undefined'
    },
    {
        'name': 'small_dataset',
        'exp_q': np.array([0.01, 0.02]),
        'exp_I': np.array([100, 90]),
        'exp_err': np.array([5, 5]),
        'fit_q': np.array([0.01, 0.02]),
        'fit_I': np.array([100, 90]),
        'expected_p': None,
        'expected_status': 'insufficient_data'
    }
]

def test_reference_cases():
    """
    Test all reference cases
    """
    print("="*80)
    print("CORMAP REGRESSION TESTS")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for case in REFERENCE_CASES:
        print(f"\nTest: {case['name']}")
        
        result = cormap_pairwise(
            case['exp_q'], case['exp_I'], case['exp_err'],
            case['fit_q'], case['fit_I']
        )
        
        # Check status
        if result['status'] != case['expected_status']:
            print(f"  ✗ FAILED: Status mismatch")
            print(f"    Expected: {case['expected_status']}")
            print(f"    Got: {result['status']}")
            failed += 1
            continue
        
        # Check p-value if applicable
        if 'expected_p_range' in case:
            p = result['p_value']
            if p is None or not (case['expected_p_range'][0] <= p <= case['expected_p_range'][1]):
                print(f"  ✗ FAILED: P-value out of expected range")
                print(f"    Expected: {case['expected_p_range']}")
                print(f"    Got: {p}")
                failed += 1
                continue
        elif 'expected_p' in case:
            if result['p_value'] != case['expected_p']:
                print(f"  ✗ FAILED: P-value mismatch")
                print(f"    Expected: {case['expected_p']}")
                print(f"    Got: {result['p_value']}")
                failed += 1
                continue
        
        print(f"  ✓ PASSED")
        print(f"    p-value: {result['p_value']}")
        print(f"    C-value: {result['c_value']}")
        print(f"    Status: {result['status']}")
        passed += 1
    
    print(f"\n{'='*80}")
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0

if __name__ == "__main__":
    success = test_reference_cases()
    sys.exit(0 if success else 1)
