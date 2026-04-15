# Groq O' Clock

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project/branch/main/graph/badge.svg)](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project)
[![PyPI](https://img.shields.io/badge/pypi-not%20published-lightgrey)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project)

Lets get to grokkin'

![demo](demo.gif)

```text
$ chat
chat> /ls .github
workflows
chat> /calculate 6 * 7
42
```

## Test Projects

### Webpage Project

```text
$ cd test_projects/webpage
$ chat
chat> what does this project do?
This project creates a personal website. It contains HTML, CSS, and JavaScript files that build a responsive portfolio site.
```

This example demonstrates the chat tool reading and comprehending project documentation automatically through the `cat` tool.

### Markdown Compiler Project

```text
$ cd test_projects/markdown_compiler
$ chat
chat> does this project use regular expressions?
No, I searched all .py files and found no imports of the `re` module.
```

This example shows the LLM using the `grep` tool automatically to search for regex imports across the project, proving it can reason about code patterns.

### eBay Scraper Project

```text
$ cd test_projects/ebay_scraper
$ chat
chat> tell me about this project
This is a web scraper designed to extract product information from eBay listings, including titles, prices, and seller information.
```

This example demonstrates the LLM reading and summarizing the project's README to give an accurate overview of the project's purpose.
