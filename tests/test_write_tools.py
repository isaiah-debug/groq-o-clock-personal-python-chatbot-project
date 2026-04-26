"""Tests for git-backed write and delete tools."""

from pathlib import Path

from git import Repo

from tools.rm import rm
from tools.write_file import write_file
from tools.write_files import write_files


def test_write_file_commits_python_and_returns_doctest_output(
    tmp_path,
    monkeypatch,
):
    """Writing a Python file runs doctests and creates a git commit."""
    monkeypatch.chdir(tmp_path)
    repo = Repo.init(tmp_path)
    source = '''"""Example module.

>>> greet()
'hi'
"""

def greet():
    """Return a short greeting."""
    return "hi"
'''

    output = write_file("hello.py", source, "add hello module")

    assert "passed all tests" in output
    assert Path("hello.py").read_text(encoding="utf-8") == source
    assert repo.head.commit.message == "[docchat] add hello module"


def test_write_files_supports_diff_updates(tmp_path, monkeypatch):
    """Unified diffs can update existing tracked files before committing."""
    monkeypatch.chdir(tmp_path)
    repo = Repo.init(tmp_path)

    result = write_files(
        [{"path": "notes.txt", "contents": "alpha\nbeta\ngamma\n"}],
        "add notes",
    )

    assert result == "Files written and committed."

    diff = "@@ -1,3 +1,3 @@\n alpha\n-beta\n+delta\n gamma\n"
    result = write_files(
        [{"path": "notes.txt", "diff": diff}],
        "patch notes",
    )

    assert result == "Files written and committed."
    assert (
        Path("notes.txt").read_text(encoding="utf-8")
        == "alpha\ndelta\ngamma\n"
    )
    assert repo.head.commit.message == "[docchat] patch notes"


def test_rm_deletes_globbed_files_and_commits(tmp_path, monkeypatch):
    """The rm tool deletes tracked files selected by a glob and commits it."""
    monkeypatch.chdir(tmp_path)
    repo = Repo.init(tmp_path)
    Path("a.txt").write_text("a", encoding="utf-8")
    Path("b.txt").write_text("b", encoding="utf-8")
    repo.index.add(["a.txt", "b.txt"])
    repo.index.commit("base")

    result = rm("*.txt")

    assert result == "Removed: a.txt, b.txt"
    assert not Path("a.txt").exists()
    assert not Path("b.txt").exists()
    assert repo.head.commit.message == "[docchat] rm *.txt"
