"""Run doctests without pytest's doctest plugin."""

import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


FILES = [
    "chat.py",
    "tools/calculate.py",
    "tools/cat.py",
    "tools/compact.py",
    "tools/diff_utils.py",
    "tools/doctests.py",
    "tools/grep.py",
    "tools/ls.py",
    "tools/load_image.py",
    "tools/path_safety.py",
    "tools/pip_install.py",
    "tools/rm.py",
    "tools/write_file.py",
    "tools/write_files.py",
]


def main():
    """Run doctests across the project modules."""
    from chat import _doctest_result_has_failures
    from tools.doctests import doctests

    failed = False
    for path in FILES:
        output = doctests(path)
        sys.stdout.write(output)
        if _doctest_result_has_failures(output):
            failed = True

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
