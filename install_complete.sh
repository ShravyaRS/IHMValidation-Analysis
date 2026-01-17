
#!/bin/bash
# Complete IHMValidation Container Installation Script
# This consolidates all Phase 8 fixes into a single script

set -e  # Exit on error

echo "============================================================"
echo "IHMValidation Complete Container Build"
echo "============================================================"
echo ""
echo "This script will:"
echo "  1. Verify prerequisites"
echo "  2. Build Singularity container with all fixes"
echo "  3. Run validation tests"
echo "  4. Generate success report"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v singularity &> /dev/null && ! command -v apptainer &> /dev/null; then
    echo "ERROR: Singularity/Apptainer not found"
    echo "Install with: sudo apt install -y apptainer"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then 
    echo "ERROR: This script must be run with sudo"
    echo "Usage: sudo ./install_complete.sh"
    exit 1
fi

# Check disk space (need at least 15GB)
available=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$available" -lt 15 ]; then
    echo "WARNING: Less than 15GB free space. Build may fail."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Prerequisites OK"
echo ""

# Navigate to correct directory
cd "$(dirname "$0")"

if [ ! -f "singularity/Singularity.def" ]; then
    echo "ERROR: Singularity.def not found"
    echo "Are you in the IHMValidation directory?"
    exit 1
fi

# Build container
echo "============================================================"
echo "Building container (this will take 30-45 minutes)..."
echo "============================================================"
echo ""

singularity build --force ihmvalidation_complete.sif singularity/Singularity.def

if [ ! -f "ihmvalidation_complete.sif" ]; then
    echo "ERROR: Container build failed"
    exit 1
fi

echo ""
echo "============================================================"
echo "Build complete!"
echo "============================================================"
echo ""

# Show container info
ls -lh ihmvalidation_complete.sif

# Quick verification
echo ""
echo "Verifying container..."
singularity exec ihmvalidation_complete.sif python3 --version
singularity exec ihmvalidation_complete.sif which datcmp

echo ""
echo "============================================================"
echo "Installation successful!"
echo "============================================================"
echo ""
echo "Container: ihmvalidation_complete.sif ($(du -h ihmvalidation_complete.sif | cut -f1))"
echo ""
echo "Quick test:"
echo "  singularity exec ihmvalidation_complete.sif python3 \\"
echo "    /opt/IHMValidation/ihm_validation/ihm_validator.py \\"
echo "    -f your_structure.cif \\"
echo "    --output-root output \\"
echo "    --output-prefix test"
echo ""
echo "Full documentation: README.md"
echo "============================================================"
