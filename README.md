# Groq O'Clock

[![doctest](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/doctest.yml)
[![integration-test](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/integration-test.yml)
[![flake8](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml/badge.svg)](https://github.com/isaiah-debug/groq-o-clock-personal-python-chatbot-project/actions/workflows/flake8.yml)
[![coverage](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project/branch/main/graph/badge.svg)](https://codecov.io/gh/isaiah-debug/groq-o-clock-personal-python-chatbot-project)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-isaiah-bingham-docsum)](https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/)

Groq O'Clock is a terminal chat tool for reading and editing local projects with automatic git commits. It supports local tools for listing files, reading files, running doctests, writing files, patching files, deleting files, compacting chat history, and loading images into the conversation.

![demo](demo.gif)

PyPI: https://pypi.org/project/cmc-csci040-isaiah-bingham-docsum/

## Packages

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
- `openai`
- `python-dotenv`
- `gitpython`
- a `GROQ_API_KEY` for the default Groq provider
- an `OPENROUTER_API_KEY` if you use `--provider openai`, `anthropic`, or `google`

You can start from:

```bash
cp .env.example .env
```

## Install

The package is meant to be installed and then used from the terminal with the `chat` command.

```bash
python -m pip install -e .
export GROQ_API_KEY=your_api_key_here
chat "What files are in this directory? Reply with just the filenames."
```

## Usage

The main workflow is asking a normal question and letting Groq decide when to inspect files with tools.

```text
$ chat
chat> what files are in this directory?
README.md, chat.py, pyproject.toml, requirements.txt, tests, tools, and demo.gif.
```

If you want to drive the tools yourself, the slash commands are still available inside the REPL. These are the same kinds of commands exercised in the integration tests.

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

You can also choose a provider explicitly. `groq` remains the default, while the OpenRouter-backed providers let the same agent run against OpenAI, Anthropic, or Google models:

```text
$ chat --provider openai "Summarize the README in one sentence."
Groq O'Clock is a terminal agent that can inspect and modify local repositories while committing its changes with git.
```

## Agent Writes

This example is interesting because it demonstrates the project-4 requirement that the agent can create, update, and delete files while making git commits for each filesystem change.

```text
$ ls -1
AGENTS.md
README.md
chat.py
$ git log --oneline -2
d711556 hi
fa197cc hi
$ chat
chat> Create hello.py with a doctested greet() function that returns "hello".
The agent created `hello.py`, ran its doctests, and committed the change.
chat> Update hello.py so greet() returns "hello, Isaiah" instead.
The agent patched `hello.py`, reran its doctests, and committed the update.
chat> Delete hello.py.
The agent removed `hello.py` and committed the deletion.
chat> ^C
$ git log --oneline -3
7c3f412 [docchat] rm hello.py
6a8a1dd [docchat] personalize hello module
13c2baf [docchat] create hello module
```

This works because `write_file`, `write_files`, and `rm` all validate safe relative paths, update the working tree, and commit through GitPython.

## More Tools

This example is interesting because it shows the extra-credit quality-of-life features that make the agent usable over longer sessions.

```text
$ chat
chat> /load_image screenshot.png
Loaded image screenshot.png
chat> what error is shown in that screenshot?
The screenshot shows a traceback ending in `ValueError: unsupported image type`.
chat> /compact
Summarized the conversation into one compact system message.
chat> /doctests chat.py
Trying:
    parse_args([])
Expecting:
    Namespace(debug=False, provider='groq', message=[])
...
Test passed.
```

This works because `/load_image` injects a local image into the message list, `/compact` summarizes the current chat into one message, and `doctests` runs a verbose doctest pass without leaving the REPL.

## Record A Demo GIF

The cleanest way to make a real terminal GIF is to use `vhs`, which records the actual terminal session you type through.

On macOS:

```bash
brew install vhs
```

Then make sure your Groq key is available and run:

```bash
export GROQ_API_KEY=your_api_key_here
./scripts/record_demo.sh
```

That command prepares the same sample file used by the tests and records the session defined in [demo.tape](demo.tape). The output overwrites `demo.gif`, which is already embedded at the top of this README.

## Test Projects

This example is interesting because it shows the chatbot summarizing a project without any manual slash commands.

```text
$ cd test_projects/webpage
$ chat
chat> what does this project do?
This is a personal portfolio website built with HTML and CSS.
```

This works because the tool reads project files and summarizes them directly.

This example is interesting because it shows the chatbot using search across the codebase to answer a code question.

```text
$ cd test_projects/markdown_compiler
$ chat
chat> does this project use regular expressions?
No, I grepped all .py files and found no imports of the `re` module.
```

This works because the tool can automatically grep project files before it answers.

This example is interesting because it shows the chatbot reading project files to give a higher-level summary.

```text
$ cd test_projects/ebay_scraper
$ chat
chat> tell me about this project
This project scrapes eBay listings and extracts product titles and prices using BeautifulSoup.
```

This works because the tool can inspect the README and source files before responding.
