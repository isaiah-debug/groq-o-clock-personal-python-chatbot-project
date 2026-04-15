# DocChat

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

DocChat is a command line assistant that can answer questions about files in the current folder. It can calculate, list files, read text files, and grep with regular expressions using either automatic tool calls or manual slash commands.

PyPI project page: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

## Demo

Add a terminal-only animated gif here after recording the final project demo.

## Usage

```text
$ chat
chat> /ls .github
workflows
chat> /calculate 6 * 7
42
chat> what files are in the .github folder?
The `.github` folder contains the `workflows` folder.
```

This example is good because it demonstrates both manual slash commands and a follow-up question that can use previous tool output already in the conversation.

## Test Project Examples

```text
$ cd test_projects/webpage
$ chat
chat> /cat README.md
...
chat> tell me what this website is about
The README describes the purpose and structure of the website.
```

This example is good because it shows how DocChat can read project documentation before answering.

```text
$ cd test_projects/markdown_compiler
$ chat
chat> /grep 're\\.' '*.py'
...
chat> does this project use regular expressions?
Yes. The grep output shows Python files using the `re` module.
```

This example is good because it demonstrates source-code search with `grep`.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> /ls
README.md
...
chat> /cat README.md
...
chat> tell me about this project
The README says this project scrapes product information from eBay.
```

This example is good because it combines directory listing and file reading.
