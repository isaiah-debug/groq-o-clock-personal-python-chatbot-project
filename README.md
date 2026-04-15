# Groq O'Clock

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project/branch/main/graph/badge.svg)](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

Groq O'Clock is a terminal chat tool for asking questions about local projects. It supports Groq tool calls plus direct slash commands for `calculate`, `ls`, `cat`, and `grep`.

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

### Webpage

```text
$ cd test_projects/webpage
$ chat
chat> what does this project do?
```

This is useful because the tool can read project files before answering.

### Markdown Compiler

```text
$ cd test_projects/markdown_compiler
$ chat
chat> does this project use regular expressions?
```

This is useful because the tool can search source files with `grep`.

### eBay Scraper

```text
$ cd test_projects/ebay_scraper
$ chat
chat> tell me about this project
```

This is useful because the tool can summarize project documentation.
