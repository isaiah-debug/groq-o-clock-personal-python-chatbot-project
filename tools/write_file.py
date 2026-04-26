"""Write a single file and commit it to git for the chat agent."""

from tools.write_files import write_files as _write_files


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a file (utf-8) and commit it to git.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path to write.",
                },
                "contents": {
                    "type": "string",
                    "description": "UTF-8 text content to write.",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message (prefixed with [docchat]).",
                },
            },
            "required": ["path", "contents", "commit_message"],
        },
    },
}


def write_file(path, contents, commit_message):
    """Write a file and commit it to git.

    >>> write_file('/etc/passwd', 'x', 'test')
    'error: unsafe path /etc/passwd'
    >>> write_file('../secret', 'x', 'test')
    'error: unsafe path ../secret'
    >>> write_file('docs/../leak', 'x', 'test')
    'error: unsafe path docs/../leak'
    """
    return _write_files([{"path": path, "contents": contents}], commit_message)
