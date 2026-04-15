# DocChat

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

DocChat is a terminal assistant for asking questions about files in the current folder. It can use `calculate`, `ls`, `cat`, and `grep` automatically, or you can run them directly with slash commands.

![demo](demo.gif)

PyPI: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

```text
$ chat
chat> /ls .github
workflows
chat> /calculate 6 * 7
42
```

## Test Projects

```text
$ cd test_projects/webpage
$ chat
chat> /cat README.md
```

This is useful for quickly reading a webpage project's documentation.

```text
$ cd test_projects/markdown_compiler
$ chat
chat> /grep 'import re' '*.py'
```

This is useful for checking how a markdown compiler searches or parses text.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> /ls
chat> /cat README.md
```

This is useful for checking the files and documentation in an eBay scraper.
