# PyPI Publishing Guide

The package `cmc-csci040-isaiah-bingham-docsum` is ready to be published. Here are your options:

## Option 1: Automated via GitHub Actions (Recommended)

1. Go to https://pypi.org/account/api-tokens/
2. Create a new API token (or use an existing one)
3. Copy the token (it starts with `pypi-`)
4. Go to your GitHub repo → Settings → Secrets and variables → Actions
5. Create a new secret named `PYPI_API_TOKEN` and paste your token
6. Go to Actions → publish-pypi → Run workflow → Run workflow
7. The workflow will build and upload your package to PyPI

## Option 2: Manual Upload from Local Machine

```bash
# Install twine if not already installed
pip install twine

# Upload the built package
python -m twine upload dist/*

# When prompted:
# Username: __token__
# Password: (Your PyPI API token starting with pypi-)
```

## Option 3: Using the Helper Script

```bash
bash PYPI_UPLOAD.sh

# When prompted:
# Username: __token__
# Password: (Your PyPI API token starting with pypi-)
```

## After Publishing

Once the package is uploaded, you can verify it at:
https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

The badge in README.md will automatically show the package version on PyPI.

## Getting Your PyPI API Token

1. Go to https://pypi.org/account/login/
2. Log in with your account
3. Go to https://pypi.org/account/api-tokens/
4. Click "Add API token"
5. Give it any name (e.g., "groq-o-clock")
6. Select "Entire account" scope
7. Click "Create token"
8. Copy the token immediately (you won't be able to see it again)
