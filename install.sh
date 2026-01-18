
#!/bin/bash
#
# One-line install script for IHMValidation
#
# Usage: bash install.sh
#

set -e

echo "============================================================"
echo "IHMValidation Installation"
echo "============================================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Singularity
if ! command -v singularity &> /dev/null && ! command -v apptainer &> /dev/null; then
    echo "ERROR: Singularity/Apptainer not found"
    echo ""
    echo "Install with:"
    echo "  sudo apt update"
    echo "  sudo apt install -y apptainer"
    exit 1
fi

echo "✓ Singularity/Apptainer found"

# Check disk space
AVAILABLE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE" -lt 15 ]; then
    echo "WARNING: Less than 15GB free space"
    echo "Available: ${AVAILABLE}GB"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✓ Sufficient disk space"

# Check sudo
if [ "$EUID" -ne 0 ]; then
    echo ""
    echo "This script needs sudo privileges to build the container."
    echo "You will be prompted for your password."
    echo ""
fi

echo ""
echo "Installation will:"
echo "  1. Build Singularity container (30-45 min)"
echo "  2. Install all dependencies (ATSAS, Chimera, etc.)"
echo "  3. Apply validation fixes"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

echo ""
echo "Starting build..."
sudo bash install_complete.sh

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Test the installation:"
echo "  bash run_example.sh"
echo ""
echo "Validate your structure:"
echo "  singularity exec IHMValidation/ihmvalidation_complete.sif python3 \\"
echo "    /opt/IHMValidation/ihm_validation/ihm_validator.py \\"
echo "    -f your_structure.cif \\"
echo "    --output-root output \\"
echo "    --output-prefix name"
echo ""
