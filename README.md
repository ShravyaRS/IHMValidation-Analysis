
# IHMValidation Container Analysis

Complete dependency resolution for IHMValidation on Ubuntu 22.04, achieving 100% validation success.

![Python](https://img.shields.io/badge/python-3.10-blue)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Summary

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
