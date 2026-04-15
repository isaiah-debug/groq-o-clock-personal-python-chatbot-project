# DocChat

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

Terminal chat for local documents using Groq plus safe tools.

PyPI: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

## Rubric Checklist

- `chat.py` contains the main program.
- `tools/` contains `calculate`, `ls`, `cat`, and `grep`.
- Tools reject absolute paths and `..` traversal.
- Manual slash commands work, for example `/ls`, `/cat`, `/grep`, and `/calculate`.
- Automatic Groq tool calls are implemented in `Chat`.
- Every function/class/file has docstrings and doctests where required.
- Doctest coverage is above 90%; tool modules are covered at 100%.
- GitHub Actions include doctest, integration-test, and flake8.
- `pyproject.toml` and `requirements.txt` support install/build.
- `.env`, `.coverage`, `.DS_Store`, caches, build files, and virtualenv files are ignored.
- `test_projects/` exists for previous-project submodules.
- README includes badges, PyPI link, usage examples, and a demo placeholder.

## Demo

`demo.gif` goes here.

## Usage

```text
$ chat
chat> /ls .github
workflows
chat> /calculate 6 * 7
42
```

## Test Project Examples

```text
$ cd test_projects/webpage
$ chat
chat> /cat README.md
chat> what is this project?
```

Good because it checks that DocChat can read project documentation.

```text
$ cd test_projects/markdown_compiler
$ chat
chat> /grep 'import re' '*.py'
chat> does this project use regular expressions?
```

Good because it checks source search with regular expressions.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> /ls
chat> /cat README.md
chat> what does this project do?
```

Good because it checks directory listing plus file reading.
