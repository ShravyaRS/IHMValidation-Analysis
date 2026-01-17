# IHMValidation Container: From 50% to 100% Success

[![Lint and Validate](https://github.com/ShravyaRS/IHMValidation-Analysis/actions/workflows/lint-and-validate.yml/badge.svg)](https://github.com/ShravyaRS/IHMValidation-Analysis/actions/workflows/lint-and-validate.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Singularity](https://img.shields.io/badge/Singularity-3.8+-green.svg)](https://sylabs.io/singularity/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)](https://ubuntu.com/)
[![Success Rate](https://img.shields.io/badge/Validation_Success-100%25-brightgreen.svg)]()


## Project Summary

**In this project, we identified 5 critical bugs in the IHMValidation system, resolved all dependency and runtime issues, and produced a reproducible Singularity container that achieves 100% validation success across all test structures.**

**Key Metrics:**
- Fixed 5 blocking issues (ATSAS installation, EM webdriver, Chimera/ChimeraX/MapQ version checks)
- Improved validation success rate from 50% to 100%
- Validated 8 diverse integrative model structures
- Created production-ready containerized solution with complete documentation

---

## Executive Summary

**Problem**: The IHMValidation system failed to validate 50% of test structures due to missing ATSAS dependencies and runtime errors in validation components.

**Solution**: Systematically resolved dependency issues and implemented robust error handling across all validation pipelines.

**Outcome**: Achieved 100% validation success rate (8/8 structures), with all components functioning reliably in a reproducible Singularity container.

---
## Quick Start

### Prerequisites
- Ubuntu 22.04 or compatible Linux
- Singularity/Apptainer 3.8+
- 10GB free disk space
- sudo access

### Installation
```bash
# Clone repository
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis/IHMValidation

# Build container (30-45 minutes)
sudo singularity build ihmvalidation_complete.sif singularity/Singularity.def
```

### Usage
```bash
# Validate a structure
singularity exec ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f your_structure.cif \
  --output-root validation_output \
  --output-prefix structure_name
```

**Output**: Full validation PDF report with quality metrics, restraint satisfaction, and precision analysis.

---
