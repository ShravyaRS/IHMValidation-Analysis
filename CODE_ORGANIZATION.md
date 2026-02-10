# Code Organization Guide

## Core Implementation (USE THIS)

**File**: `scripts/cormap_implementation.py`
**Purpose**: Production-ready CorMap implementation
**Function**: `cormap_pairwise(exp_q, exp_I, exp_err, fit_q, fit_I)`
**Status**: STABLE - This is the validated code

## Validation Pipeline (How validation was done)

### Step 1: Data Extraction
**File**: `scripts/extract_exp_and_fit_data.py`
**Purpose**: Extract experimental and fitted data from .sascif files

### Step 2: Run DATCMP
**File**: `scripts/run_datcmp_on_exp_fit.py`
**Purpose**: Run DATCMP on extracted data for comparison

### Step 3: Run Python CorMap
**File**: `scripts/run_cormap_on_exp_fit.py`
**Purpose**: Run Python CorMap on same data

### Step 4: Compare Results
**File**: `scripts/compare_datcmp_cormap_final.py`
**Purpose**: Statistical comparison of DATCMP vs Python CorMap

### Step 5: Generate Report
**File**: `scripts/generate_final_report.py`
**Purpose**: Create comprehensive validation report

## Testing (Verify correctness)

**File**: `tests/test_cormap_regression.py`
**Purpose**: 5 regression tests to ensure code correctness
**Status**: ALL 5 TESTS PASSING

## Supplementary Analysis Scripts (Optional)

These were created during analysis but are NOT core:
- `calculate_confidence_intervals.py` - Bootstrap CI calculation
- `characterize_disagreements.py` - Categorize disagreement cases
- `benchmark_performance.py` - Performance measurements
- `analyze_boundary_cases.py` - Boundary case analysis
- `explain_spearman.py` - Spearman correlation explanation

## Ignore These (Experimental/Deprecated)

- `cormap_alternative_implementation.py` - Experimental alternative
- `download_*.py` - Data download utilities
- `three_way_comparison.py` - Three-way validation check

## For Integration: YOU ONLY NEED

1. `scripts/cormap_implementation.py` - The implementation
2. `tests/test_cormap_regression.py` - The tests

Everything else is validation documentation.
