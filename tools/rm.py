"""Delete files and commit the removal for the chat agent."""

import glob
import os
import subprocess

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": (
            "Delete safe relative files (supports globs) and commit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path or glob to delete.",
                },
            },
            "required": ["path"],
        },
    },
}


def rm(path):
    """Delete files matching a safe relative glob and commit the removal.

    >>> rm('/etc/passwd')
    'error: unsafe path'
    >>> rm('../secret')
    'error: unsafe path'
    >>> rm('docs/../leak')
    'error: unsafe path'
    >>> rm('nonexistent_rm_doctest_*.txt')
    'error: no files matched nonexistent_rm_doctest_*.txt'
    """
    if not is_path_safe(path):
        return "error: unsafe path"
    matched = sorted(glob.glob(path))
    if not matched:
        return f"error: no files matched {path}"
    for f in matched:
        os.remove(f)
    try:
        subprocess.run(
            ["git", "add"] + matched, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", f"[docchat] rm {path}"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        raw = error.stderr
        stderr = raw.decode() if isinstance(raw, bytes) else (raw or "")
        return f"Removed files but git commit failed: {stderr.strip()}"
    return f"Removed: {', '.join(matched)}"
