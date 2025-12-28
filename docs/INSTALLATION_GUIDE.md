# IHMValidation: Installation & Deployment Guide

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- git (for cloning)
- ATSAS tools (optional, for SAS validation)

## Installation Methods

### Method 1: Clone from GitHub (Development)
```bash
# Clone repository
git clone https://github.com/salilab/IHMValidation.git
cd IHMValidation

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov
```

### Method 2: Docker/Singularity (Recommended for Production)
```bash
# Singularity container
singularity pull library://salilab/ihm-validation:latest
singularity run ihm-validation_latest.sif -f structure.cif

# Docker container (if available)
docker pull salilab/ihm-validation:latest
docker run -v $(pwd):/data salilab/ihm-validation -f /data/structure.cif
```

## Quick Start

### Basic Usage
```bash
# Run validation on a structure
python -m ihm_validation.ihm_validator -f PDBDEV_00000001.cif

# With output directory
python -m ihm_validation.ihm_validator \
  -f PDBDEV_00000001.cif \
  --output-root ./validation_results

# Verbose mode
python -m ihm_validation.ihm_validator \
  -f PDBDEV_00000001.cif \
  -v
```

### Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-f` | Input mmCIF file | `-f structure.cif` |
| `-v` | Verbose output | `-v` |
| `--output-root` | Output directory | `--output-root ./results` |
| `-models` | Number of models | `-models 10` |
| `-mp` | Model precision (Å) | `-mp 10` |
| `-p` | Physical principles used | `-p yes` |
| `--force` | Overwrite existing | `--force` |

## Output

The validation produces:

1. **HTML Report** - Interactive validation report
2. **PDF Report** - Printable version
3. **JSON Data** - Raw validation metrics
4. **PNG Plots** - Validation plots and graphs

## Performance

Expected runtime on typical structure:
- **Data parsing**: 5-10 seconds
- **SAS validation**: 2-5 minutes (if SAS data present)
- **Crosslinking validation**: 1-3 minutes (if crosslinks present)
- **3DEM validation**: 3-10 minutes (if EM data present)
- **Report generation**: 1-2 minutes

**Total**: 10-30 minutes depending on data modalities

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pdfkit'"
```bash
pip install pdfkit
```

Also requires wkhtmltopdf:
- Ubuntu: `sudo apt-get install wkhtmltopdf`
- macOS: `brew install wkhtmltopdf`
- Windows: Download from https://wkhtmltopdf.org/

### Issue: "ATSAS not found"

Install ATSAS tools:
- Download from: http://www.atsas.de/
- Add to PATH

### Issue: "EMDB connection failed"

- Check internet connection
- EMDB server might be down
- Try with `--nocache` flag

## Database Caching

The software caches SASBDB and EMDB data:
```bash
# Use local cache
python ihm_validator.py -f structure.cif --databases-root /path/to/local/db

# Bypass cache
python ihm_validator.py -f structure.cif --nocache

# Specify cache location
python ihm_validator.py -f structure.cif --cache-root /custom/cache/path
```

## Containerized Deployment

### Building Docker Image Locally
```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["python", "-m", "ihm_validation.ihm_validator"]
```
```bash
docker build -t ihm-validation:latest .
docker run -v $(pwd):/data ihm-validation:latest -f /data/structure.cif
```

## System Requirements

### Minimum

- 2GB RAM
- 5GB disk space
- 1 CPU core

### Recommended

- 8GB RAM
- 50GB disk space
- 4 CPU cores

### For Large Structures

- 16GB+ RAM
- 100GB+ disk space
- 8+ CPU cores

## Advanced Usage

### Batch Processing
```bash
# Validate multiple structures
for file in structures/*.cif; do
    python ihm_validator.py -f "$file" --output-root ./results/
done
```

### Parallel Processing
```bash
# Using GNU Parallel
ls structures/*.cif | parallel python ihm_validator.py -f {} --output-root ./results/
```

### Custom Parameters
```bash
python ihm_validator.py \
  -f structure.cif \
  -models 100 \
  -mp "15 Å" \
  -p yes \
  -m "Integrative modeling using cryo-EM, SAS, and crosslinking data" \
  -v1 "Model fits SAS, EM, and crosslinking data" \
  -v2 "Model validated against independent EM data"
```

## Documentation

- Main docs: https://ihmvalidation.readthedocs.io/
- GitHub issues: https://github.com/salilab/IHMValidation/issues
- Contact: ihmv@pdb-ihm.org

