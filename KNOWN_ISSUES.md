# Known Issues and Workarounds

## Issue 1: High p-values show larger variance

**Symptom**: Disagreements between DATCMP and Python CorMap occur mostly at p > 0.2

**Cause**: Noise-dominated regime has low statistical power

**Workaround**: Both methods agree fit is acceptable. Use either value.

**Status**: Expected behavior, not a bug

---

## Issue 2: DATCMP fails on 54% of cases

**Symptom**: DATCMP returns NaN or crashes on 30/56 test cases

**Cause**: DATCMP limitations (closed-source, poor error handling)

**Workaround**: Python CorMap handles these cases correctly

**Status**: Python CorMap is MORE robust than DATCMP

---

## Issue 3: Perfect match edge case

**Symptom**: When exp == fit exactly, early versions returned insufficient_data

**Fix**: Version 1.1+ returns p=1.0 (perfect agreement)

**Status**: FIXED in current version

---

## Support

For issues not listed here:
1. Check regression tests: `python tests/test_cormap_regression.py`
2. Review documentation: `docs/`
3. Open GitHub issue: https://github.com/ShravyaRS/IHMValidation-Analysis/issues
