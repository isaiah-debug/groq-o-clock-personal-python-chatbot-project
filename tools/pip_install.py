"""Install Python packages for the chat agent (extra credit)."""

import subprocess
import sys


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "pip_install",
        "description": "Install a Python package using pip.",
        "parameters": {
            "type": "object",
            "properties": {
                "library_name": {
                    "type": "string",
                    "description": "Name of the Python package to install via pip.",
                },
            },
            "required": ["library_name"],
        },
    },
}


def pip_install(library_name):
    """Install a Python package using pip.

    >>> pip_install('')
    'error: library name cannot be empty'
    >>> pip_install('   ')
    'error: library name cannot be empty'
    """
    if not library_name or not library_name.strip():
        return "error: library name cannot be empty"
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", library_name.strip()],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return f"Successfully installed {library_name}"
    return f"error: {result.stderr.strip()}"
