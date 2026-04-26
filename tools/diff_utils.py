"""Helpers for applying file updates from diff text.

The patcher intentionally ignores unified-diff line numbers and instead
matches hunks by their surrounding text. This is more tolerant of the slightly
broken diffs that LLMs often generate.
"""

import re


HUNK_HEADER_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,\d+)? \+\d+(?:,\d+)? @@"
)


def apply_text_update(original_text, contents=None, diff=None):
    """Return updated text from either full contents or a unified diff.

    Exactly one of `contents` or `diff` must be provided.

    >>> apply_text_update('old\\n', contents='new\\n')
    'new\\n'
    >>> patch = '@@ -1 +1 @@\\n-old\\n+new\\n'
    >>> apply_text_update('old\\n', diff=patch)
    'new\\n'
    >>> apply_text_update('old\\n', contents='new\\n', diff=patch)
    Traceback (most recent call last):
    ...
    ValueError: provide exactly one of contents or diff
    """
    if (contents is None) == (diff is None):
        raise ValueError("provide exactly one of contents or diff")
    if contents is not None:
        return contents
    return apply_unified_diff(original_text, diff)


def apply_unified_diff(original_text, diff_text):
    """Apply a unified diff to text while matching hunks by content.

    >>> original = 'alpha\\nbeta\\ngamma\\n'
    >>> diff = '@@ -1,3 +1,3 @@\\n alpha\\n-beta\\n+delta\\n gamma\\n'
    >>> apply_unified_diff(original, diff)
    'alpha\\ndelta\\ngamma\\n'
    >>> original = 'alpha\\ngamma\\n'
    >>> diff = '@@ -1,2 +1,3 @@\\n alpha\\n+beta\\n gamma\\n'
    >>> apply_unified_diff(original, diff)
    'alpha\\nbeta\\ngamma\\n'
    >>> apply_unified_diff('alpha\\n', '')
    Traceback (most recent call last):
    ...
    ValueError: diff did not contain any hunks
    """
    lines = original_text.splitlines(keepends=True)
    hunks = parse_unified_diff(diff_text)
    if not hunks:
        raise ValueError("diff did not contain any hunks")

    for hunk in hunks:
        old_block = []
        new_block = []
        for line in hunk["lines"]:
            if line.startswith("\\"):
                continue
            prefix = line[:1]
            body = line[1:]
            if prefix in {" ", "-"}:
                old_block.append(body)
            if prefix in {" ", "+"}:
                new_block.append(body)

        index = find_subsequence(lines, old_block)
        if index is None:
            index = max(hunk["old_start"] - 1, 0)
            candidate = lines[index:index + len(old_block)]
            if old_block and candidate != old_block:
                raise ValueError("diff hunk could not be applied")

        lines = lines[:index] + new_block + lines[index + len(old_block):]
    return "".join(lines)


def find_subsequence(lines, block):
    """Return the index of a contiguous block inside a list of lines.

    >>> find_subsequence(['a\\n', 'b\\n', 'c\\n'], ['b\\n'])
    1
    >>> find_subsequence(['a\\n', 'b\\n'], ['c\\n']) is None
    True
    >>> find_subsequence(['a\\n'], [])
    0
    """
    if not block:
        return 0
    limit = len(lines) - len(block) + 1
    for index in range(max(limit, 0)):
        if lines[index:index + len(block)] == block:
            return index
    return None


def parse_unified_diff(diff_text):
    """Parse a unified diff into hunks with metadata.

    >>> parse_unified_diff('@@ -2 +2 @@\\n-old\\n+new\\n')[0]['old_start']
    2
    >>> parse_unified_diff('not a diff')
    []
    """
    hunks = []
    current = None
    for line in diff_text.splitlines(keepends=True):
        match = HUNK_HEADER_RE.match(line)
        if match:
            current = {
                "old_start": int(match.group("old_start")),
                "lines": [],
            }
            hunks.append(current)
            continue
        if current is not None:
            current["lines"].append(line)
    return hunks
