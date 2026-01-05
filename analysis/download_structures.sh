#!/bin/bash
# Download diverse IHM structures from PDB-Dev

mkdir -p test-data-extended

# Get various structure types
structures=(
    "PDBDEV_00000001"
    "PDBDEV_00000010"
    "PDBDEV_00000015"
    "PDBDEV_00000020"
    "PDBDEV_00000025"
    "PDBDEV_00000030"
    "PDBDEV_00000035"
    "PDBDEV_00000040"
)

echo "Downloading structures from PDB-Dev..."
for struct in "${structures[@]}"; do
    url="https://pdb-dev.wwpdb.org/static/cif/${struct}.cif"
    echo "Fetching $struct..."
    wget -q -O "test-data-extended/${struct}.cif" "$url" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✓ $struct downloaded"
    else
        echo "  ✗ $struct failed"
    fi
done

echo ""
echo "Downloaded structures to test-data-extended/"
ls -lh test-data-extended/
