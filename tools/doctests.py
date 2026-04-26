"""Run doctests for the chat agent."""

import pathlib
import shutil
import subprocess
import sys

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "doctests",
        "description": (
            "Run doctests (with --verbose) on a safe relative Python file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to a Python file.",
                },
            },
            "required": ["path"],
        },
    },
}


def doctests(path):
    """Run doctests with --verbose on a safe relative Python file.

    >>> doctests('/etc/passwd')
    'error: unsafe path'
    >>> doctests('../secret.py')
    'error: unsafe path'
    >>> doctests('docs/../secret.py')
    'error: unsafe path'
    """
    if not is_path_safe(path):
        return "error: unsafe path"
    file_path = pathlib.Path(path)
    interpreter = shutil.which("python3") or sys.executable
    result = subprocess.run(
        [interpreter, "-m", "doctest", "-v", str(file_path)],
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr
