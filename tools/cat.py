"""Read text files for the chat agent."""

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "cat",
        "description": "Read a safe relative text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path to read.",
                },
            },
            "required": ["path"],
        },
    },
}


def cat(path):
    """Return the contents of a safe relative text file.

    >>> from pathlib import Path
    >>> _ = Path('cat_doctest.txt').write_text('hello\\nworld\\n')
    >>> cat('cat_doctest.txt')
    'hello\\nworld\\n'
    >>> cat('missing.txt')
    'error: file not found'
    >>> cat('/etc/passwd')
    'error: unsafe path'
    >>> _ = Path('cat_binary.txt').write_bytes(b'\\xff')
    >>> cat('cat_binary.txt')
    'error: file is not valid utf-8 text'
    >>> Path('cat_doctest.txt').unlink()
    >>> Path('cat_binary.txt').unlink()
    """
    if not is_path_safe(path):
        return "error: unsafe path"

    try:
        with open(path, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "error: file not found"
    except UnicodeDecodeError:
        return "error: file is not valid utf-8 text"
