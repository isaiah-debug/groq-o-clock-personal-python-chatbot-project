# Groq O'Clock

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project/branch/main/graph/badge.svg)](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

download the project and run it

![demo](demo.gif)

PyPI: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

packages u need

To use the published package from PyPI, install:

```bash
python -m pip install cmc-csci040-isaiah-bingham-docsum
```

To work from this repo locally, install:

```bash
python -m pip install -e .
```

To run tests and packaging checks from this repo, install:

```bash
python -m pip install -e ".[dev]"
```

The chat client needs:

- `groq`
- `python-dotenv`
- a `GROQ_API_KEY` in your shell or in a local `.env` file

You can start from:

```bash
cp .env.example .env
```

installation

The package is meant to be installed and then used from the terminal with the
`chat` command.

```bash
python -m pip install -e .
export GROQ_API_KEY=your_api_key_here
chat "What files are in this directory? Reply with just the filenames."
```

using it

The main workflow is asking a normal question and letting Groq decide when to
inspect files with tools.

```text
$ chat
chat> what files are in this directory?
README.md, chat.py, pyproject.toml, requirements.txt, tests, tools, and demo.gif.
```

If you want to drive the tools yourself, the slash commands are still available
inside the REPL. These are the same kinds of commands exercised in the
integration tests.

```text
$ chat
chat> /ls itest
sample.txt
chat> /calculate 6 * 7
42
chat> /cat itest/sample.txt
DocChat docs
needle line
chat> /grep needle itest/*.txt
itest/sample.txt:needle line
```



That command prepares the same sample file used by the tests and records the
session defined in [demo.tape](/Users/isaiahbingham/project/groq-o-clock-personal-python-chatbot-project/demo.tape).
The output overwrites `demo.gif`, which is already embedded at the top of this
README.

test projects



```text
$ cd test_projects/webpage
$ chat
chat> what does this project do?
This is a personal portfolio website built with HTML and CSS.
```

-tool reads project files and summarizes them directly.



```text
$ cd test_projects/markdown_compiler
$ chat
chat> does this project use regular expressions?
No, I grepped all .py files and found no imports of the `re` module.
```

-tool can automatically grep project files before it
answers.

- chatbot reading project files
to give a higher-level summary.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> tell me about this project
This project scrapes eBay listings and extracts product titles and prices using BeautifulSoup.
```

- tool can inspect the README and source files before
responding.
