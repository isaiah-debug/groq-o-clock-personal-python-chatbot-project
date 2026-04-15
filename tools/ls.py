"""List files for the chat agent."""

import glob
import os

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "ls",
        "description": (
            "List files in the current folder or one safe subfolder."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative folder path to list.",
                },
            },
            "required": [],
        },
    },
}


def ls(path="."):
    """List files in a safe relative folder, one filename per line.

    >>> from pathlib import Path
    >>> Path('ls_doctest').mkdir(exist_ok=True)
    >>> _ = Path('ls_doctest/b.txt').write_text('b')
    >>> _ = Path('ls_doctest/a.txt').write_text('a')
    >>> ls('ls_doctest')
    'a.txt\\nb.txt'
    >>> ls('/tmp')
    'error: unsafe path'
    >>> ls('../')
    'error: unsafe path'
    >>> Path('ls_doctest/a.txt').unlink()
    >>> Path('ls_doctest/b.txt').unlink()
    >>> Path('ls_doctest').rmdir()
    """
    if not is_path_safe(path):
        return "error: unsafe path"

    filenames = sorted(
        os.path.basename(filename) for filename in glob.glob(f"{path}/*")
    )
    return "\n".join(filenames)
