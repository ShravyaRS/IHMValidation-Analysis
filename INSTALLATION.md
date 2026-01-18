# Installation Guide

## Quick Install (Recommended)
```bash
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis
bash install.sh
```

## Installation Methods

### Method 1: Singularity Container (Recommended)

**Advantages**: All dependencies pre-installed, reproducible environment
```bash
# Install Singularity/Apptainer if needed
sudo apt update
sudo apt install -y apptainer

# Build container
sudo bash install_complete.sh
```

**System Requirements:**
- Ubuntu 22.04 or compatible Linux
- 10GB free disk space
- 4GB RAM minimum (8GB recommended)
- sudo privileges

### Method 2: Conda Environment

**Advantages**: Lightweight, familiar to Python users
```bash
# Create environment
conda env create -f environment.yml
conda activate ihmvalidation

# Note: System packages (ATSAS, Chimera) must be installed separately
```

### Method 3: pip + System Packages

**Advantages**: Minimal Python setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system packages (Ubuntu 22.04)
# ATSAS
wget https://www.embl-hamburg.de/biosaxs/download/ATSAS-3.0.3-1_amd64.deb
sudo dpkg -i ATSAS-3.0.3-1_amd64.deb
sudo apt install -y -f

# Additional packages
sudo apt install -y chimera chimerax firefox-esr
```

## Dependency Management

### Python Dependencies

**Primary method**: `requirements.txt`
```bash
pip install -r requirements.txt
```

**Alternative**: `environment.yml` (conda)
```bash
conda env create -f environment.yml
```

### Version Compatibility

| Package | Version | Notes |
|---------|---------|-------|
| Python | 3.10 | Required |
| Bokeh | 2.4.2 - 3.x | Use compatibility layer for 3.x |
| NumPy | 1.26.2 | Recommended |
| IHM | 2.7 | Required |
| ATSAS | 3.0.3-1 | System package |

### Bokeh 3.x Support

This project now supports Bokeh 3.x:
```bash
# Install Bokeh 3.x
pip install 'bokeh>=3.0'

# Compatibility layer handles API differences automatically
```

## Verification

Test installation:
```bash
# Quick test
bash run_example.sh

# Full test suite
bash run_tests.sh
```

Expected output:
- Example validation completes in <5 minutes
- All tests pass (8/8)
- PDF reports generated

## Troubleshooting

### Common Issues

**Issue**: Container build fails with disk space error
```bash
# Solution: Clean up space or use external tmp
export SINGULARITY_TMPDIR=/path/to/larger/disk
sudo -E singularity build container.sif definition.def
```

**Issue**: Bokeh import errors
```bash
# Solution: Use compatibility layer
from src.bokeh_compat import Button, Slider  # Instead of direct bokeh imports
```

**Issue**: ATSAS not found
```bash
# Solution: Verify installation
which datcmp
# Should output: /usr/bin/datcmp
```

## Updating

Pull latest changes:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

Rebuild container:
```bash
sudo singularity build --force ihmvalidation_complete.sif singularity/Singularity.def
```

## Uninstallation
```bash
# Remove container
rm IHMValidation/ihmvalidation_complete.sif

# Remove conda environment
conda env remove -n ihmvalidation

# Remove pip packages
pip uninstall -r requirements.txt -y
```
