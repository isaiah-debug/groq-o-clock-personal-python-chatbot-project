"""Delete files and commit the removal for the chat agent."""

import glob
import os

from git import Repo

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
        repo = Repo(".")
        repo.index.remove(matched, working_tree=False)
        repo.index.commit(f"[docchat] rm {path}")
    except Exception as error:  # pragma: no cover - GitPython error types vary
        return f"Removed files but git commit failed: {error}"
    return f"Removed: {', '.join(matched)}"
