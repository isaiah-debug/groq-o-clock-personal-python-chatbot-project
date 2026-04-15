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

```text
$ cd test_projects/webpage
$ chat
chat> what does this project do?
This is a personal portfolio website built with HTML and CSS.
```

This is useful because the tool reads project files and summarizes them without any manual commands.

```text
$ cd test_projects/markdown_compiler
$ chat
chat> does this project use regular expressions?
No, I grepped all .py files and found no imports of the `re` module.
```

This is useful because the tool automatically searches source files with grep to answer code questions.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> tell me about this project
This project scrapes eBay listings and extracts product titles and prices using BeautifulSoup.
```

This is useful because the tool reads the README and summarizes the project purpose automatically.
