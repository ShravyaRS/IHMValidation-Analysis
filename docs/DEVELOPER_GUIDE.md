# IHMValidation: Developer's Guide

## Getting Started with Development

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/salilab/IHMValidation.git
cd IHMValidation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
pip install pytest pytest-cov black flake8 mypy
```

### Code Style & Standards
```bash
# Format code with Black
black ihm_validation/

# Check style with Flake8
flake8 ihm_validation/

# Type checking
mypy ihm_validation/

# Run tests
pytest tests/ -v --cov=ihm_validation
```

---

## Architecture for Developers

### Adding a New Data Modality (e.g., FRET)

1. **Create module**: `ihm_validation/fret.py`
2. **Implement validation logic**:
```python
   class FRETValidation:
       def __init__(self, mmcif_file, cache):
           # Initialize with structure
           pass
       
       def get_fret_ids(self) -> list:
           # Extract FRET measurements
           pass
       
       def validate_distances(self) -> dict:
           # Validate against predicted distances
           pass
```

3. **Add tests**: `tests/test_fret.py`
4. **Update ihm_validator.py**: Register new validator
5. **Update documentation**: Add to docs

### Code Organization Principles
Cohesion: High (each module does one thing well)
Coupling: Low (modules independent)
Modularity: High (easy to extend)
Testability: High (functions are isolated)

---

## Testing Guidelines

### Test Structure
```python
# tests/test_module.py
import pytest
from ihm_validation.module import ModuleClass

class TestModuleClass:
    @pytest.fixture
    def sample_data(self):
        # Provide test data
        return test_data
    
    def test_initialization(self, sample_data):
        # Test that module initializes correctly
        obj = ModuleClass(sample_data)
        assert obj is not None
    
    def test_core_function(self, sample_data):
        # Test main functionality
        result = obj.validate()
        assert result is not None
```

### Coverage Goals
- Target: 80%+ code coverage
- Critical paths: 100% coverage
- Edge cases: Must be tested

---

## Performance Optimization Tips

### Profiling Code
```bash
# Use cProfile to identify bottlenecks
python -m cProfile -s cumulative ihm_validator.py -f structure.cif
```

### Optimization Points

1. **mmcif_io.py** - File parsing can be slow
   - Consider memory-mapped files
   - Lazy loading of data

2. **Validation loops** - Use NumPy vectorization
   - Avoid Python loops
   - Leverage NumPy's performance

3. **Plotting** - Image generation is slow
   - Cache intermediate results
   - Generate in parallel

---

## Contributing Code

### Pull Request Process

1. Fork repository
2. Create feature branch: `git checkout -b feature/fret-validation`
3. Make changes
4. Add tests
5. Format code: `black`
6. Run tests: `pytest tests/`
7. Push to GitHub
8. Open pull request

### Code Review Checklist

- ✅ Code passes tests
- ✅ Code is formatted with Black
- ✅ Type hints present
- ✅ Docstrings complete
- ✅ No breaking changes
- ✅ Documentation updated

