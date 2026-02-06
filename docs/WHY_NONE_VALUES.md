# Why Some Tests Return p_value = None and c_value = None

## This is CORRECT Behavior!

### Understanding CorMap Test Requirements

The CorMap test **requires** certain conditions to produce a valid p-value:

1. **Sufficient data points** (N ≥ 3)
2. **Valid experimental errors** (σ > 0)
3. **Overlapping q-ranges** between experimental and fitted data
4. **Non-zero residuals** that can be signed

## Test Case Breakdown

### Test 1: `perfect_match`
```
Status: success
p-value: 1.0
C-value: 1
```
**Why it works**: Has valid data, can compute residuals (even though all ~0), returns p=1.0 (perfect agreement)

### Test 2: `poor_match`
```
Status: success
p-value: 1.58e-30
C-value: 100
```
**Why it works**: Has valid data, systematic deviation detected, very low p-value indicates poor fit

### Test 3: `no_overlap` → Returns None ✓
```
Status: insufficient_data
p-value: None
C-value: None
```
**Why None is CORRECT**:
- Experimental q-range: [0.01, 0.1]
- Fitted q-range: [0.2, 0.3]
- **No overlap!** Cannot compare non-overlapping curves
- Mathematically undefined → None is the right answer

### Test 4: `zero_errors` → Returns None ✓
```
Status: undefined
p-value: None
C-value: None
```
**Why None is CORRECT**:
- Experimental errors: All zeros (σ = 0)
- Cannot calculate normalized residuals: (I_exp - I_fit) / 0 = undefined
- Division by zero → Cannot compute CorMap
- None is the mathematically correct answer

### Test 5: `small_dataset` → Returns None ✓
```
Status: insufficient_data
p-value: None
C-value: None
```
**Why None is CORRECT**:
- Only 2 data points
- CorMap needs N ≥ 3 for statistical validity
- Cannot detect runs with only 2 points
- None indicates "not enough data"

## Status vs p-value Matrix

| Status | p-value | c-value | Meaning |
|--------|---------|---------|---------|
| `success` | float | int | Valid CorMap test performed |
| `insufficient_data` | None | None | Not enough data to compute |
| `undefined` | None | None | Mathematically undefined (e.g., σ=0) |
| `error` | None | None | Computational error occurred |

## Why This Design is Good

### 1. **Explicit Failure Modes**
Instead of:
```python
p_value = 0.0  # Ambiguous: good fit or error?
```

We return:
```python
p_value = None  # Clear: test could not be performed
status = 'insufficient_data'  # Explains why
```

### 2. **Prevents Misinterpretation**
If we returned `p=0.0` for `no_overlap`, users might think:
- "The fit is terrible!" 

With `p=None`, users correctly understand:
- "Cannot evaluate - no overlapping data" ✓

### 3. **Defensive Programming**
Returning `None` for invalid cases prevents:
- Division by zero errors
- Meaningless statistics
- Silent failures

### 4. **Matches Scientific Practice**
In real experiments:
- Not all measurements are valid
- Some datasets are unusable
- Scientists need to know WHY something failed

## Real-World Example

Imagine comparing two SAS curves:

**Scenario A**: Good data, poor fit
```
p_value: 0.001
c_value: 45
status: success
→ "Fit is statistically poor"
```

**Scenario B**: Zero experimental errors
```
p_value: None
c_value: None
status: undefined
→ "Cannot evaluate - experimental errors are zero"
```

**Scenario C**: Non-overlapping q-ranges
```
p_value: None
c_value: None
status: insufficient_data
→ "Cannot compare - no common q-range"
```

## How to Use in Production
```python
result = cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)

if result['status'] == 'success':
    if result['p_value'] < 0.05:
        print("Reject fit - poor agreement")
    else:
        print("Accept fit - good agreement")
        
elif result['status'] == 'insufficient_data':
    print("Cannot evaluate - need more overlapping data")
    
elif result['status'] == 'undefined':
    print("Cannot evaluate - check experimental errors")
    
else:
    print(f"Error: {result['status']}")
```

## Comparison with DATCMP

**DATCMP behavior**:
- Often crashes with cryptic errors
- Returns NaN without explanation
- Users don't know what went wrong

**Our Python CorMap**:
- Returns None explicitly
- Provides clear status message
- Users understand exactly what happened

## Summary

**None values are CORRECT and NECESSARY** because:

1. Some data cannot be analyzed (no overlap, zero errors)
2. Returning None is more honest than returning 0 or NaN
3. Status field explains exactly why None was returned
4. Prevents misinterpretation and silent errors
5. Matches scientific best practices

**All 5 regression tests passing** means:
- Valid cases return numbers
- Invalid cases return None
- Status correctly describes what happened

This is **error handling**! 
