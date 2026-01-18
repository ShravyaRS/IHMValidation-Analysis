
# Test Suite

Comprehensive testing for IHMValidation container and validation logic.

## Test Structure
```
tests/
├── unit_tests/              # Component-level tests
│   └── test_validation_components.py
├── integration_tests/       # End-to-end workflow tests
│   └── test_complete_workflow.py
└── scientific_controls/     # Biophysical correctness tests
    └── test_scientific_validation.py
```

## Running Tests

### All Tests
```bash
bash run_tests.sh
```

### Individual Test Suites
```bash
# Unit tests only
python3 -m pytest tests/unit_tests/ -v

# Integration tests only
python3 -m pytest tests/integration_tests/ -v

# Scientific validation only
python3 tests/scientific_controls/test_scientific_validation.py
```

## Test Coverage

### Unit Tests
- Container integrity check
- ATSAS accessibility verification
- Python version confirmation
- Module import validation

### Integration Tests
- Complete validation pipeline
- PDF report generation
- Batch processing capability
- Performance benchmarking

### Scientific Tests
- Valid structure detection
- Invalid structure rejection
- Biophysical correctness validation

## Expected Results

All tests should pass:
- Unit tests: 4/4 pass
- Integration tests: 2/2 pass
- Scientific tests: Correct discrimination

## Troubleshooting

### Test Failures

**Container not found:**
```bash
bash install.sh
```

**Module import errors:**
```bash
pip install -r requirements.txt
```

**Timeout errors:**
- Increase timeout in test files
- Check system resources (memory, CPU)

## Adding New Tests

1. Create test file in appropriate directory
2. Follow pytest conventions (`test_*.py`)
3. Use clear test names (`test_feature_behavior`)
4. Add to `run_tests.sh` if needed
5. Document expected behavior

## Continuous Integration

Tests are designed to run in CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run tests
  run: bash run_tests.sh
```
