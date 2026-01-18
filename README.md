
# IHMValidation Container Analysis

Complete dependency resolution for IHMValidation on Ubuntu 22.04, achieving 100% validation success.

![Python](https://img.shields.io/badge/python-3.10-blue)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Summary

## Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis

# One-line install
bash install.sh
```

### Run Example (5 minutes)
```bash
bash run_example.sh
```

This validates an example structure and generates:
- Full validation PDF report
- Summary PDF report  
- Interactive HTML dashboard

Output location: `example_output/demo/`

### Validate Your Structure
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f your_structure.cif \
  --output-root validation_results \
  --output-prefix structure_name
```

**Input**: mmCIF format structure file  
**Output**: PDF reports + HTML visualization in `validation_results/structure_name/`

### Command Line Options
```bash
# Basic usage
python3 /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f structure.cif \
  --output-root output_dir \
  --output-prefix name

# Verbose mode (see detailed progress)
python3 /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -v \
  -f structure.cif \
  --output-root output_dir \
  --output-prefix name

# Use cached databases (faster for multiple runs)
python3 /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f structure.cif \
  --output-root output_dir \
  --output-prefix name \
  --cache cache_directory
```

### Expected Output
```
validation_results/
└── structure_name/
    ├── structure_name_full_validation.pdf      # Complete report
    ├── structure_name_summary_validation.pdf   # Key findings
    ├── structure_name_htmls.zip                # Interactive dashboard
    └── structure_name/
        ├── images/                             # Generated plots
        ├── htmls/                              # Interactive HTML
        └── supplementary_tables/               # Data tables
```


## Quick Start

### One-Line Install
```bash
bash install.sh
```

### Run Example
```bash
bash run_example.sh
```

This validates an example structure and generates reports in `example_output/`.

### Validate Your Structure
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f your_structure.cif \
  --output-root output \
  --output-prefix structure_name
```


Fixed ATSAS dependency installation issues preventing validation of structures with Small Angle Scattering data. Implemented error handling for EM validation components.

**Result**: Validation success improved from 50% to 100% (4/8 to 8/8 structures).

## Installation
```bash
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis
sudo bash install_complete.sh
```

Build time: 30-45 minutes

## Usage
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f structure.cif \
  --output-root output_dir \
  --output-prefix name
```

## Results

### Success Rate
![Success Rate](figures/generated/success_rate.png)

### Performance Analysis
![Performance](figures/generated/performance_3d.png)

### Component Impact
![Component Impact](figures/generated/component_impact.png)

## Technical Implementation

### Primary Fix: ATSAS Installation
- **Issue**: Missing libicu66 dependency on Ubuntu 22.04
- **Solution**: Manual dependency installation via dpkg
- **Impact**: Fixed 3 structures (PDBDEV_00000020, 35, 40)

### Secondary Fix: EM Validation
- **Issue**: MapQ version check failures on large structures
- **Solution**: Error handling with default versions
- **Impact**: Fixed 1 structure (PDBDEV_00000010)

### Enhancements
- EM webdriver initialization (Selenium/Firefox)
- Chimera/ChimeraX version error handling
- Improved stability across all validation components

## Validation Results

| Structure | Size | Before | After | Issue Resolved |
|-----------|------|--------|-------|----------------|
| PDBDEV_00000001 | 1.6MB | Pass | Pass | - |
| PDBDEV_00000010 | 5.8MB | Fail | Pass | MapQ error handling |
| PDBDEV_00000015 | 2.3MB | Pass | Pass | - |
| PDBDEV_00000020 | 2.1MB | Fail | Pass | ATSAS installation |
| PDBDEV_00000025 | 1.8MB | Pass | Pass | - |
| PDBDEV_00000030 | 2.4MB | Pass | Pass | - |
| PDBDEV_00000035 | 2.0MB | Fail | Pass | ATSAS installation |
| PDBDEV_00000040 | 2.2MB | Fail | Pass | ATSAS installation |

## Repository Structure
```
├── src/container/          # Container definition and patches
├── figures/generated/      # Publication-quality figures
├── docs/                   # Technical documentation
├── tests/                  # Test suite
├── install_complete.sh     # Automated build script
└── requirements.txt        # Python dependencies
```

## Documentation

- [Technical Details](docs/TECHNICAL_DETAILS.md)
- [Build Instructions](docs/BUILD_INSTRUCTIONS.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## Requirements

- Ubuntu 22.04 or compatible Linux
- Singularity/Apptainer 3.8+
- 10GB disk space
- 4GB RAM minimum (8GB recommended)

## License

MIT License - see LICENSE file

## Contact

- Issues: https://github.com/ShravyaRS/IHMValidation-Analysis/issues
- Upstream: https://github.com/salilab/IHMValidation

## Testing

Verify installation and functionality:
```bash
# Run complete test suite
bash run_tests.sh

# Run specific tests
python3 -m pytest tests/unit_tests/ -v
python3 -m pytest tests/integration_tests/ -v
python3 tests/scientific_controls/test_scientific_validation.py
```

**Test Coverage:**
- Container integrity and dependencies
- Validation logic (correct error detection)
- Complete workflow (end-to-end)
- Scientific correctness (biophysical validation)

See [tests/README.md](tests/README.md) for details.

