#!/bin/bash
# This script publishes the package to PyPI using an API token
# Usage: PYPI_TOKEN=pypi-YOUR-TOKEN-HERE ./publish_to_pypi.sh

if [ -z "$PYPI_TOKEN" ]; then
    echo "ERROR: PYPI_TOKEN environment variable not set"
    echo ""
    echo "To get an API token:"
    echo "1. Go to https://pypi.org/account/api-tokens/"
    echo "2. Click 'Add API token'"
    echo "3. Create a project-specific token for cmc-csci040-isaiah-bingham-docsum"
    echo "4. Copy the token (starts with 'pypi-')"
    echo ""
    echo "Then run:"
    echo "  export PYPI_TOKEN=pypi-YOUR-TOKEN-HERE"
    echo "  ./publish_to_pypi.sh"
    exit 1
fi

cd "$(dirname "$0")" || exit 1

echo "Publishing to PyPI..."
python -m twine upload dist/* --username __token__ --password "$PYPI_TOKEN" --non-interactive

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Package successfully published to PyPI!"
    echo "  https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/"
else
    echo ""
    echo "✗ Upload failed"
    exit 1
fi
