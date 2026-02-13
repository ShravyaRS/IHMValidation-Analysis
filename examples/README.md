# Example: Replacing DATCMP with FreeSAS + Exact Decimal

## Quick Start
```bash
python replace_datcmp_example.py
```

## What This Shows

How to replace DATCMP (ATSAS) with FreeSAS cormapy for CorMap goodness-of-fit testing, using exact Decimal arithmetic for the p-value to avoid float64 precision issues.

## Key Function
```python
from freesas.cormap import gof
from decimal import Decimal, getcontext

getcontext().prec = 100

def cormap_pvalue_exact(n, c_longest):
    k = c_longest - 1
    if k > n: return 0.0
    if k <= 0: return 1.0
    f = [Decimal(0)] * (n + 1)
    for i in range(min(k, n + 1)):
        f[i] = Decimal(2) ** i
    for i in range(k, n + 1):
        f[i] = sum(f[i - j] for j in range(1, k + 1))
    return float(Decimal(1) - f[n] / Decimal(2) ** n)

# Usage
result = gof(exp_data, fit_data)
p = cormap_pvalue_exact(result.n, result.c)
```
