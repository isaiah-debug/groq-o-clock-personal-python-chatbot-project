"""Run doctests without pytest's doctest plugin."""

import doctest
import importlib
import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


MODULES = [
    "chat",
    "tools.calculate",
    "tools.cat",
    "tools.grep",
    "tools.ls",
    "tools.path_safety",
]


def main():
    """Run doctests across the project modules."""
    failures = 0
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        result = doctest.testmod(module, verbose=True)
        failures += result.failed

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
