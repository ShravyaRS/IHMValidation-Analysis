# Build Instructions

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 22.04 LTS or compatible Linux distribution
- **Disk Space**: Minimum 15GB free space
  - 5.5GB for built container
  - 5GB for build cache
  - 5GB for temporary files
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **CPU**: Multi-core recommended for faster build

### Software Requirements

1. **Singularity/Apptainer** (version 3.8 or higher)

Install on Ubuntu 22.04:
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:apptainer/ppa
sudo apt update
sudo apt install -y apptainer
```

Verify installation:
```bash
singularity --version
# or
apptainer --version
```

2. **Root/Sudo Access**: Required for container building

3. **Internet Connection**: Required for downloading packages and dependencies

## Build Process

### Step 1: Clone Repository
```bash
git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
cd IHMValidation-Analysis/IHMValidation
```

### Step 2: Verify Files

Ensure the following files are present:
```bash
ls -l singularity/Singularity.def
ls -l patch_em_properly.py
```

Expected output:
```
-rw-r--r-- 1 user user  XXXX singularity/Singularity.def
-rwxr-xr-x 1 user user  XXXX patch_em_properly.py
```

### Step 3: Build Container
```bash
sudo singularity build ihmvalidation_complete.sif singularity/Singularity.def
```

Build process will:
1. Download Ubuntu 22.04 base image
2. Install system packages
3. Set up Conda environment
4. Install ATSAS with dependencies
5. Install Chimera and ChimeraX
6. Clone and patch IHMValidation
7. Clean up build artifacts

**Expected Duration**: 30-45 minutes (depending on internet speed)

### Step 4: Verify Build

Check container size:
```bash
ls -lh ihmvalidation_complete.sif
# Should show approximately 5.5GB
```

Test container execution:
```bash
singularity exec ihmvalidation_complete.sif python3 --version
# Should output: Python 3.10.x
```

Test validation script:
```bash
singularity exec ihmvalidation_complete.sif \
  /opt/IHMValidation/ihm_validation/ihm_validator.py --help
# Should display usage information
```

## Troubleshooting

### Build Failures

#### Issue: Package download failures
```
E: Failed to fetch http://archive.ubuntu.com/...
```

**Solution**: Retry build - temporary network issue
```bash
sudo singularity build --force ihmvalidation_complete.sif singularity/Singularity.def
```

#### Issue: Hash sum mismatch
```
E: Failed to fetch ... Hash Sum mismatch
```

**Solution**: Repository mirror sync issue, retry after few minutes

#### Issue: Disk space errors
```
FATAL: ... no space left on device
```

**Solution**: Free up disk space or use different build location:
```bash
export SINGULARITY_TMPDIR=/path/to/larger/tmp
sudo -E singularity build ihmvalidation_complete.sif singularity/Singularity.def
```

### Runtime Issues

#### Issue: Permission denied
```
FATAL: container creation failed: ... permission denied
```

**Solution**: Ensure sudo is used for build, or check SELinux/AppArmor settings

#### Issue: Missing bind mounts
```
WARNING: Skipping user bind control directory: ...
```

**Solution**: Normal warning, container will work. To fix:
```bash
mkdir -p ~/ihmv/{input,output,cache,databases}
```

## Testing the Built Container

### Quick Test
```bash
# Create test directory
mkdir -p test-validation

# Run simple validation test (if you have test data)
singularity exec ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f test-data/PDBDEV_00000001.cif \
  --output-root test-validation \
  --output-prefix test
```

### Full Test Suite

To run all 8 test structures:
```bash
for pdb in 00000001 00000010 00000015 00000020 00000025 00000030 00000035 00000040; do
  echo "Testing PDBDEV_${pdb}..."
  singularity exec ihmvalidation_complete.sif python3 \
    /opt/IHMValidation/ihm_validation/ihm_validator.py \
    -f test-data-extended/PDBDEV_${pdb}.cif \
    --output-root test-outputs \
    --output-prefix PDBDEV_${pdb}
done
```

Expected: All 8 validations should complete successfully with PDF outputs.

## Advanced Build Options

### Customize Build Cache
```bash
export SINGULARITY_CACHEDIR=/path/to/cache
sudo -E singularity build ihmvalidation_complete.sif singularity/Singularity.def
```

### Build with Different Base Image

Edit `singularity/Singularity.def`:
```
Bootstrap: docker
From: ubuntu:24.04  # Change version
```

### Add Custom Packages

Edit `%post` section in `Singularity.def`:
```bash
%post
    # Existing packages...
    apt install -y your-custom-package
    pip install your-python-package
```

## Post-Build Steps

### Container Distribution

Compress for transfer:
```bash
gzip -c ihmvalidation_complete.sif > ihmvalidation_complete.sif.gz
```

Calculate checksum:
```bash
sha256sum ihmvalidation_complete.sif > ihmvalidation_complete.sif.sha256
```

### Container Registry Upload

Upload to Singularity Container Library:
```bash
singularity sign ihmvalidation_complete.sif
singularity push ihmvalidation_complete.sif library://username/collection/image:tag
```

## Cleanup

Remove build cache:
```bash
singularity cache clean --all
```

Remove temporary files:
```bash
rm -rf /tmp/sbuild-*
```

## Support

For build issues:
1. Check Singularity version compatibility
2. Review build logs for specific errors
3. Ensure all prerequisites are met
4. Consult Singularity documentation
5. Open issue in repository
