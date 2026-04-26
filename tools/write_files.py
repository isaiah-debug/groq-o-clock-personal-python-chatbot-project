"""Write files and commit them to git for the chat agent."""

import os

from git import Repo

from tools.diff_utils import apply_text_update
from tools.doctests import doctests
from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": (
            "Write multiple files (utf-8) and commit them to git."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "description": "List of {path, contents|diff} dicts.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "contents": {"type": "string"},
                            "diff": {"type": "string"},
                        },
                        "required": ["path"],
                    },
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message (prefixed with [docchat]).",
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
    >>> write_files([{'path': 'README.md'}], 'test')
    'error: each file needs exactly one of contents or diff'
    """
    paths = []
    doctest_output = []

    for f in files:
        path = f["path"]
        if not is_path_safe(path):
            return f"error: unsafe path {path}"
        contents = f.get("contents")
        diff = f.get("diff")
        try:
            original_text = ""
            if diff is not None and os.path.exists(path):
                with open(path, encoding="utf-8") as file:
                    original_text = file.read()
            updated_text = apply_text_update(
                original_text,
                contents=contents,
                diff=diff,
            )
        except UnicodeDecodeError:
            return f"error: {path} is not valid utf-8 text"
        except ValueError as error:
            if str(error) == "provide exactly one of contents or diff":
                return "error: each file needs exactly one of contents or diff"
            return f"error: {error}"

        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(updated_text)
        paths.append(path)
        if path.endswith(".py"):
            doctest_output.append(doctests(path))

    try:
        repo = Repo(".")
        repo.index.add(paths)
        repo.index.commit(f"[docchat] {commit_message}")
    except Exception as error:  # pragma: no cover - GitPython error types vary
        return f"error: git operation failed: {error}"

    if doctest_output:
        return "\n".join(doctest_output)
    return "Files written and committed."
