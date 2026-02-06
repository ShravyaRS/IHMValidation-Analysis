# Status Code Reference

## Overview

Python CorMap returns detailed status codes to help users diagnose issues.

## Status Codes

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `success` | Valid CorMap test performed | Use p-value for interpretation |
| `insufficient_data` | N < 3 points available | Get more data or check q-range |
| `no_overlap` | Empty intersection of q-ranges | Check experimental vs fitted ranges |
| `no_variance` | All errors σ = 0 | Check experimental error column |
| `undefined` | Mathematically undefined | Review data quality |
| `error: <msg>` | Computational error | Report as bug with data |

## Status Code Details

### `success`
**Returned when**: Valid CorMap test successfully completed

**Output**:
```python
{
    'status': 'success',
    'p_value': 0.042,  # float
    'c_value': 14,     # int
    'n_points': 150    # int
}
```

**Interpretation**: Use p-value for statistical decision.

---

### `insufficient_data`
**Returned when**: Fewer than 3 overlapping data points

**Output**:
```python
{
    'status': 'insufficient_data',
    'p_value': None,
    'c_value': None,
    'n_points': 2  # or 0
}
```

**Common causes**:
- No q-range overlap between exp and fit
- Heavy filtering of invalid points
- Very sparse experimental data

**Action**: Increase data density or expand q-range.

---

### `no_variance` (future)
**Returned when**: All experimental errors are zero

**Output**:
```python
{
    'status': 'no_variance',
    'p_value': None,
    'c_value': None,
    'n_points': 150
}
```

**Common causes**:
- Missing error column (defaulted to 0)
- Unrealistic data (σ should never be exactly 0)

**Action**: Check experimental data format.

---

### `undefined`
**Returned when**: Mathematical edge case encountered

**Output**:
```python
{
    'status': 'undefined',
    'p_value': None,
    'c_value': None,
    'n_points': varies
}
```

**Common causes**:
- All residuals exactly zero (perfect match handled separately)
- Numerical instability
- Data corruption

**Action**: Inspect data manually.

---

## Usage Examples

### Check Status Before Using p-value
```python
result = cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)

if result['status'] == 'success':
    if result['p_value'] < 0.05:
        print("Reject fit")
    else:
        print("Accept fit")
elif result['status'] == 'insufficient_data':
    print("Need more overlapping data")
elif result['status'] == 'no_variance':
    print("Check experimental errors")
else:
    print(f"Issue: {result['status']}")
```

### Log All Status Codes
```python
results = []
for exp_file, fit_file in dataset:
    result = cormap_pairwise(...)
    results.append({
        'file': exp_file,
        'status': result['status'],
        'p_value': result['p_value']
    })

# Summary
df = pd.DataFrame(results)
print(df['status'].value_counts())
```

---

## Comparison with DATCMP

| Scenario | DATCMP | Python CorMap |
|----------|--------|---------------|
| Valid test | Returns p-value | `status='success'` |
| No overlap | Crash or NaN | `status='insufficient_data'` |
| Zero errors | Crash | `status='no_variance'` (future) |
| Edge case | Silent NaN | `status='undefined'` |

**Advantage**: Python CorMap provides **actionable diagnostic information**.

---

**Last Updated**: 2026-02-06
