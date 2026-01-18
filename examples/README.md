
# Example Gallery

This directory contains example structures for testing and demonstration.

## Valid Examples

### `valid/good_structure.cif`
A minimal but well-formed integrative model that passes validation.

**Expected validation results:**
- Format check: PASS
- Structure completeness: PASS
- Coordinate validity: PASS

**Use this to verify installation:**
```bash
bash run_example.sh valid/good_structure.cif
```

## Invalid Examples

### `invalid/broken_structure.cif`
A deliberately malformed structure for testing error detection.

**Expected validation results:**
- Format check: FAIL (missing required fields)
- Structure completeness: FAIL (no coordinates)

**Use this to test error handling:**
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f examples/invalid/broken_structure.cif \
  --output-root test_output \
  --output-prefix broken_test
```

## Screenshots

Visual examples of validation outputs:

- `validation_report_screenshot.png` - Example PDF report
- `interactive_dashboard.png` - Bokeh interactive visualization
- `summary_metrics.png` - Key validation metrics

## Running Examples

### Quick Test
```bash
bash run_example.sh
```

### Custom Structure
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f examples/valid/good_structure.cif \
  --output-root example_output \
  --output-prefix my_test
```

## Expected Runtime

- Valid structure: 1-3 minutes
- Invalid structure: <30 seconds (fails early)

## Troubleshooting

If validation fails unexpectedly:
1. Check container is built: `ls IHMValidation/ihmvalidation_complete.sif`
2. Verify input file format: `head -20 your_structure.cif`
3. Check logs in output directory
4. See main README troubleshooting section
