"""Search text files for the chat agent."""

import glob
import re

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "grep",
        "description": "Search safe relative files with a regular expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "regex": {
                    "type": "string",
                    "description": "Regular expression to search for.",
                },
                "path": {
                    "type": "string",
                    "description": "Relative file path or glob to search.",
                },
            },
            "required": ["regex", "path"],
        },
    },
}


def grep(regex, path):
    """Return matching lines from files selected by a safe relative glob.

    >>> from pathlib import Path
    >>> _ = Path('grep_a.txt').write_text('alpha\\nbeta\\n')
    >>> _ = Path('grep_b.txt').write_text('alphabet\\ngamma\\n')
    >>> grep('alpha', 'grep_*.txt')
    'alpha\\nalphabet'
    >>> grep('delta', 'grep_*.txt')
    ''
    >>> grep('alpha', '../*.txt')
    'error: unsafe path'
    >>> grep('[', 'grep_*.txt')
    'error: invalid regex'
    >>> _ = Path('grep_binary.txt').write_bytes(b'\\xff')
    >>> grep('alpha', 'grep_binary.txt')
    ''
    >>> Path('grep_a.txt').unlink()
    >>> Path('grep_b.txt').unlink()
    >>> Path('grep_binary.txt').unlink()
    """
    if not is_path_safe(path):
        return "error: unsafe path"

    try:
        pattern = re.compile(regex)
    except re.error:
        return "error: invalid regex"

    matches = []
    for filename in sorted(glob.glob(path)):
        try:
            with open(filename, encoding="utf-8") as file:
                for line in file:
                    if pattern.search(line):
                        matches.append(line.rstrip("\n"))
        except (FileNotFoundError, UnicodeDecodeError):
            pass
    return "\n".join(matches)
