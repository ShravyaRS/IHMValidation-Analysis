# IHMValidation Code Exploration Notes

## Exploration Date: December 28, 2024

## Initial Discovery

### Repository Structure
```
IHMValidation/
├── .git/
├── .github/
├── .gitignore
├── .readthedocs.yaml
├── LICENSE
├── README.md
├── docs/
├── ihm_validation/        # Main package (18 Python files)
├── singularity/           # Container definition
├── static/                # Web interface assets
├── templates/             # HTML templates
└── tests/                 # Test files
```

**Key Observation**: No `master/` directory as expected from some IHM tools. Package is `ihm_validation/` directly.

## Python Module Discovery

### Found 23 Python Files

**Main modules** (`ihm_validation/`):
```
__init__.py (empty - no exports defined)
cx.py
em.py
excludedvolume.py
format_checker.py
futures.py
generate_static_html_pages.py
get_plots.py
ihm_validator.py (main entry point)
images.py
mmcif_io.py
molprobity.py
molprobity_convert.py
precision.py
report.py
sas.py
sas_plots.py
utility.py
```

**Test modules** (`tests/`):
```
test_get_excluded_volume.py
test_get_input_information.py
test_sas_validation.py
test_write_report.py
README.md
```

## Entry Point Analysis

### Main Entry Point: `ihm_validator.py`

**Key findings**:
- **446 lines** of code
- **No `main()` function** - executes at module level
- Uses **argparse** for CLI arguments
- Imports from relative modules (problematic)

**Import structure**:
```python
from collections import defaultdict
import os, shutil, datetime, json
import argparse
from multiprocessing import Manager
import pdfkit                    # External - undocumented
import jinja2                    # External - undocumented
import pytz                      # External - undocumented
import sys, logging
from pathlib import Path
import utility                   # Local - relative import issue
from report import WriteReport   # Local - relative import issue
```

**Functions defined**:
- `load_json_plot()` - Load plot data
- `createdirs()` - Create output directories
- `write_html()` - Generate HTML report
- `write_pdf()` - Generate PDF report (requires pdfkit)
- `write_supplementary_table()` - Create supplementary data
- `write_json()` - Output JSON results

**Validation types mentioned**:
- SAS: 19 occurrences
- CX (crosslinking): 21 occurrences  
- EM: 133 occurrences (most prominent)
- Molprobity: 3 occurrences
- Excluded volume: 2 occurrences
- Precision: 6 occurrences

## Module Deep Dive

### mmcif_io.py - Input Handling
**Purpose**: Parse mmCIF files and extract IHM data

**Key class**: `GetInputInformation`

**Dependencies**:
```python
import utility  # Relative import - causes ModuleNotFoundError
import ihm      # External - undocumented
```

**Critical issue**: Cannot import standalone due to relative imports

### sas.py - SAS Validation
**Purpose**: Small Angle Scattering validation

**Dependencies**:
```python
from mmcif_io import GetInputInformation  # Relative
import numpy, scipy  # External
```

**Validation outputs**:
- Chi-squared values
- Guinier analysis
- Fit quality metrics

### cx.py - Crosslinking Validation
**Purpose**: Chemical crosslinking mass spec validation

**Key metrics**:
- Satisfaction rate
- Distance violations
- Crosslink density

### em.py - EM Validation
**Purpose**: Electron microscopy map validation

**Issues found**:
```python
# Line 161:
code_ = re.search('\d+', code).group()
# SyntaxWarning: invalid escape sequence '\d'
# Should be: r'\d+'

# Lines 700, 707: Same issue
```

**Dependencies**:
```python
import bokeh  # External - version-critical
```

### utility.py - Helper Functions
**Exports**: 64 utility functions!

**Key functions discovered**:
- `Counter()` - Counting operations
- `Path()` - Path handling
- `all_same()` - Comparison
- `calc_optimal_range()` - Range calculation
- Many more...

**Interesting**: This is the ONLY module that imports successfully standalone

### report.py - Report Generation
**Purpose**: Generate validation reports

**Dependencies chain**:
```python
import mmcif_io          # Needs utility
import excludedvolume    # Needs mendeleev
import get_plots         # Needs bokeh
import sas               # Needs scipy
import sas_plots         # Needs matplotlib
```

**Critical**: This is where the dependency cascade happens

## Import Chain Analysis
```
ihm_validator.py
    ↓
report.py (WriteReport)
    ↓
├─ mmcif_io.py
│   └─ utility.py ✓
│   └─ ihm [external]
│
├─ excludedvolume.py
│   └─ mendeleev [external] ✗
│
├─ get_plots.py
│   └─ bokeh [external] ✗
│   └─ bokeh.models.widgets (Bokeh 3.0 breaks)
│
├─ sas.py
│   └─ scipy [external]
│   └─ numpy [external]
│
└─ sas_plots.py
    └─ matplotlib [external]
    └─ plotly [external]
```

**Legend**:
- ✓ = Successfully imports
- ✗ = Import fails without external package
- [external] = Not in stdlib, not documented

## Web Interface Discovery

**Templates found**:
```
templates/
├── HTML templates for web interface
└── Suggests Flask/Django web server capability
```

**Static assets**:
```
static/
├── CSS
├── JavaScript
└── Images
```

**Conclusion**: Tool has TWO modes:
1. Command-line validator (what we tested)
2. Web server (not explored)

## Configuration Discovery

### Environment Variables
Found references to:
```python
# In ihm_validator.py:
operational_mode = os.environ.get('MODE', 'PRODUCTION')
# Logs: "INFO:root:Current operational mode is: PRODUCTION"
```

### No config files found
- No `.env` file in repo
- No `config.py`
- No `settings.py`
- Configuration appears to be environment-variable based

## Test Suite Analysis

**Test coverage**: Limited

**Test files**:
1. `test_get_excluded_volume.py`
2. `test_get_input_information.py`
3. `test_sas_validation.py`
4. `test_write_report.py`

**Observation**: Tests exist but no CI/CD setup to run them

## Documentation Structure

### README.md
- Focus: Web server deployment
- Missing: CLI usage, installation, dependencies
- Links to: validate.pdb-ihm.org (web service)

### docs/ Directory
Contains Sphinx documentation source:
```
docs/
├── source/
│   └── conf.py (Sphinx config)
└── .readthedocs.yaml (ReadTheDocs config)
```

### Documentation URLs Mentioned
- https://ihmvalidation.readthedocs.io/
- https://validate.pdb-ihm.org
- https://pdb-ihm.org

## Singularity Container

**Found**: `singularity/README.md`

**Observation**: Singularity definition exists but:
- Not used in our analysis
- Could be alternative to Docker
- Not documented in main README

## Key Architectural Insights

### 1. Two-Mode Design
- Web server (documented in README)
- CLI validator (undocumented, what we need)

### 2. Relative Import Pattern
**Every module** uses:
```python
import module_name
```
Instead of:
```python
from . import module_name
```

**Impact**: Must run from specific directory

### 3. Dependency Cascade
One import triggers 12+ external dependencies with no documentation

### 4. Validation Pipeline
```
Input (mmCIF)
    ↓
Parse (mmcif_io)
    ↓
Extract datasets
    ↓
Run validations (parallel):
    - SAS
    - Crosslinking
    - EM
    - Molprobity
    ↓
Generate report (HTML/JSON/PDF)
    ↓
Output
```

### 5. Missing Pieces
- No requirements.txt
- No setup.py
- No __version__ attribute
- No main() function
- Minimal __init__.py

## Comparison with Expected Structure

**Expected** (from analysis plan):
```
master/
└── pyext/
    └── src/
        └── validation/
```

**Actual**:
```
ihm_validation/
├── (all modules directly here)
```

**Impact**: Our initial analysis scripts targeted wrong path

## Command-Line Interface Discovery

**Arguments found** (from argparse in ihm_validator.py):
```bash
python3 ihm_validator.py <input.cif> --output <dir>

Options (discovered):
-v, --verbose      : Verbose output
-o, --output       : Output directory
--mmcif_dictionary : Path to mmCIF dictionary
```

**Observation**: `--help` didn't work initially due to import errors

## Error Patterns Observed

### Pattern 1: Cascading Import Failures
```
Try to import → Fail on pdfkit
Install pdfkit → Fail on bokeh  
Install bokeh → Fail on mendeleev
...
```

### Pattern 2: Version Conflicts
```
Install bokeh 3.0 → API incompatibility
Install bokeh 2.4 → NumPy conflict
```

### Pattern 3: Silent Requirements
```
Tool runs → Crashes on PDF generation
Reason: wkhtmltopdf not installed (system package)
```

## Performance Characteristics

**Repository size**: 224 MB (large!)
- Likely contains test data
- May contain pre-generated reports
- Git history is substantial (20,435 objects)

**Code complexity**:
- Medium complexity
- Clear module separation
- Each validation type isolated

## Undocumented Features Discovered

1. **Multiple output formats**:
   - HTML (always generated)
   - JSON (machine-readable)
   - PDF (requires wkhtmltopdf)

2. **Parallel processing**:
```python
   from multiprocessing import Manager
```
   Suggests parallel validation execution

3. **Static HTML page generation**:
```python
   # generate_static_html_pages.py
```
   Can pre-generate static validation pages

4. **Image generation**:
```python
   # images.py
```
   Creates validation plot images

5. **Format checking**:
```python
   # format_checker.py
```
   Validates mmCIF format before processing

## Critical Files Not Found

Expected but missing:
- ❌ requirements.txt
- ❌ setup.py / pyproject.toml
- ❌ CONTRIBUTING.md
- ❌ CHANGELOG.md
- ❌ .gitattributes (for large files)
- ❌ tox.ini (for testing)
- ❌ .flake8 / .pylintrc (linting config)

## Positive Findings

Despite issues, tool has:
- ✅ Clear module organization
- ✅ Separation of concerns
- ✅ Comprehensive validation coverage
- ✅ Multiple output formats
- ✅ Web and CLI interfaces
- ✅ Some test coverage
- ✅ Documentation infrastructure (ReadTheDocs)
- ✅ Container support (Singularity)

## Exploration Conclusions

This exploration revealed:

1. **Architecture is sound** - good modular design
2. **Packaging is broken** - missing standard Python packaging
3. **Dependencies are hidden** - complete lack of documentation
4. **Two interfaces exist** - web (documented) and CLI (not documented)
5. **Tests exist** - but no CI/CD
6. **Documentation exists** - but focuses on wrong use case

The tool is **scientifically capable** but **operationally inaccessible**.

---

**Exploration methodology**: Systematic file discovery, import testing, code reading  
**Tools used**: grep, find, Python introspection, static analysis  
**Time invested**: 8 phases over multiple hours  
**Files examined**: 23 Python files, all documentation  
**Key discovery**: Dependency documentation gap is the primary barrier  
