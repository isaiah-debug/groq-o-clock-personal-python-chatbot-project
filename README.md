# DocChat

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

Chat with local documents from the terminal.

- Tools: `calculate`, `ls`, `cat`, `grep`
- Commands: `/calculate`, `/ls`, `/cat`, `/grep`
- Safety: rejects absolute paths and `..`
- Tests: doctest, integration-test, flake8, >90% coverage
- Package: `pyproject.toml`, `requirements.txt`, `chat` command
- TODO: add `demo.gif` and real `test_projects` submodules

PyPI: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

```text
$ chat
chat> /ls .github
workflows
chat> /calculate 6 * 7
42
```

```text
$ cd test_projects/webpage
$ chat
chat> /cat README.md
```

```text
$ cd test_projects/markdown_compiler
$ chat
chat> /grep 'import re' '*.py'
```

```text
$ cd test_projects/ebay_scraper
$ chat
chat> /ls
chat> /cat README.md
```
