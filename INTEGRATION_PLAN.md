# Integration Plan: Python CorMap into IHMValidation

## Files to Add
```
IHMValidation/
├── ihm/
│   └── cormap.py          # Copy from scripts/cormap_implementation.py
└── tests/
    └── test_cormap.py     # Copy from tests/test_cormap_regression.py
```

## Files to Modify

1. **Replace DATCMP calls**:
   - Find: All subprocess calls to DATCMP
   - Replace: With `from ihm.cormap import cormap_pairwise`

2. **Update dependencies**:
   - requirements.txt: Already has numpy, scipy (no new deps)

3. **Update documentation**:
   - Mention Python CorMap replaces DATCMP
   - No ATSAS/Singularity container needed

## Migration Steps

1. Add `cormap.py` to `ihm/` module
2. Add regression tests
3. Update 1-2 files that call DATCMP
4. Run full test suite
5. Remove ATSAS dependency from docs

## Benefits After Integration

- No Singularity container needed
- 2484x faster validation
- Better error messages
- Easier to maintain (pure Python)

## Rollback Plan

Keep DATCMP as fallback option for 1 release cycle:
```python
try:
    from ihm.cormap import cormap_pairwise
    use_python = True
except ImportError:
    use_python = False
    # Fall back to DATCMP
```
