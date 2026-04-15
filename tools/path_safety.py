"""Helpers for keeping document tools inside the current folder."""

from pathlib import PurePath


def is_path_safe(path):
    """Return True only for relative paths that do not contain '..'.

    >>> is_path_safe('README.md')
    True
    >>> is_path_safe('.github/workflows')
    True
    >>> is_path_safe('/etc/passwd')
    False
    >>> is_path_safe('../secret')
    False
    >>> is_path_safe('docs/../secret')
    False
    """
    path = str(path)
    parts = PurePath(path).parts
    return not PurePath(path).is_absolute() and ".." not in parts
