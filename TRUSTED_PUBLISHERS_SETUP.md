# PyPI Publishing via Trusted Publishers

PyPI now requires API tokens instead of passwords. Here's how to publish using GitHub Actions and PyPI Trusted Publishers:

## Step 1: Configure Trusted Publisher on PyPI

1. Log in to https://pypi.org with your account (username: `123zay123`)
2. Go to your account settings
3. Find "Publishing" or "Trusted Publishers" section
4. Click "Add a Trusted Publisher"
5. Select "GitHub Actions"
6. Fill in:
   - **Owner:** `isaiah-debug`
   - **Repository name:** `groq-o-clock-personal-python-chatbot-project`
   - **Workflow name:** `publish-pypi`
   - **Environment name:** `pypi` (or leave blank)
7. Click "Save"

## Step 2: Run the Publish Workflow

1. Go to: https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions
2. Click on "publish-pypi" workflow in the left sidebar
3. Click "Run workflow" button
4. Select branch: `main`
5. Click "Run workflow"
6. Wait for the workflow to complete

## Step 3: Verify the Package

Once the workflow succeeds:
- Visit: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/
- The README badge will display the package version

## What This Enables

With Trusted Publishers configured:
- The GitHub Action can publish to PyPI without storing passwords or API tokens
- Publishing is fully automated via the workflow
- Your credentials are never exposed in the repository
- Future version releases can be automated on tags/releases

## Alternative: Direct API Token Upload

If you prefer to use an API token for local uploads:

1. Go to: https://pypi.org/account/api-tokens/
2. Create a new "Project-specific" API token for `cmc-csci040-isaiah-bingham-docsum`
3. Use it like this:
   ```bash
   python -m twine upload dist/* --username __token__ --password pypi-YOUR-TOKEN-HERE
   ```

## Current Status

✅ Package built and validated  
✅ README badge updated to show PyPI version  
✅ GitHub Actions workflow ready  
⏳ Waiting for Trusted Publisher setup on PyPI  
⏳ Ready to run publish workflow  

Once you complete Step 1 above, the package will be published to PyPI!
