#!/bin/bash
# PyPI Upload Script for cmc-csci040-isaiah-bingham-docsum
# Run this script after setting your PyPI credentials

cd "$(dirname "$0")" || exit 1

echo "=== PyPI Upload Script ==="
echo "This script will upload the built package to PyPI"
echo ""

# Check if dist files exist
if [ ! -f "dist/cmc_csci040_isaiah_bingham_docsum-0.1.0.tar.gz" ]; then
    echo "Error: Build artifacts not found. Run 'python -m build' first."
    exit 1
fi

echo "Build artifacts found:"
ls -lh dist/

echo ""
echo "=== Uploading to PyPI ==="
echo "You will be prompted for your PyPI username and password (or API token)"
echo ""

python -m twine upload dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Package successfully uploaded to PyPI!"
    echo "View it at: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/"
else
    echo ""
    echo "✗ Upload failed. Check your credentials and try again."
    exit 1
fi
