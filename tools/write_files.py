"""Write files and commit them to git for the chat agent."""

import subprocess

from tools.doctests import doctests
from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": (
            "Write multiple files (utf-8) and commit them all to git in one commit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "description": (
                        "List of files to write. Each item needs 'path' and 'contents'."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "contents": {"type": "string"},
                        },
                        "required": ["path", "contents"],
                    },
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message (prefixed with [docchat] automatically).",
                },
            },
            "required": ["files", "commit_message"],
        },
    },
}


def write_files(files, commit_message):
    """Write files to disk (utf-8) and commit them all to git.

    >>> write_files([{'path': '/etc/passwd', 'contents': 'x'}], 'test')
    'error: unsafe path /etc/passwd'
    >>> write_files([{'path': '../secret', 'contents': 'x'}], 'test')
    'error: unsafe path ../secret'
    >>> write_files([{'path': 'docs/../leak', 'contents': 'x'}], 'test')
    'error: unsafe path docs/../leak'
    """
    paths = []
    doctest_output = []

    for f in files:
        path = f["path"]
        contents = f["contents"]
        if not is_path_safe(path):
            return f"error: unsafe path {path}"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(contents)
        paths.append(path)
        if path.endswith(".py"):
            doctest_output.append(doctests(path))

    try:
        subprocess.run(["git", "add"] + paths, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"[docchat] {commit_message}"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return f"error: git operation failed: {stderr.strip()}"

    return "\n".join(doctest_output) if doctest_output else "Files written and committed."
