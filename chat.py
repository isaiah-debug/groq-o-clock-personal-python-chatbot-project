"""Command line chat program with local document tools.

The module defines a small Groq-powered chat agent that can answer questions
directly or call safe local tools for reading files in the current project.
"""

import argparse
import json
import os
import shlex

from dotenv import load_dotenv
from groq import AuthenticationError
from groq import Groq

from tools.calculate import TOOL_SPEC as CALCULATE_SPEC
from tools.calculate import calculate
from tools.cat import TOOL_SPEC as CAT_SPEC
from tools.cat import cat
from tools.doctests import TOOL_SPEC as DOCTESTS_SPEC
from tools.doctests import doctests
from tools.grep import TOOL_SPEC as GREP_SPEC
from tools.grep import grep
from tools.ls import TOOL_SPEC as LS_SPEC
from tools.ls import ls
from tools.pip_install import TOOL_SPEC as PIP_INSTALL_SPEC
from tools.pip_install import pip_install
from tools.rm import TOOL_SPEC as RM_SPEC
from tools.rm import rm
from tools.write_file import TOOL_SPEC as WRITE_FILE_SPEC
from tools.write_file import write_file
from tools.write_files import TOOL_SPEC as WRITE_FILES_SPEC
from tools.write_files import write_files

load_dotenv()


TOOL_SPECS = [
    CALCULATE_SPEC,
    LS_SPEC,
    CAT_SPEC,
    GREP_SPEC,
    DOCTESTS_SPEC,
    WRITE_FILE_SPEC,
    WRITE_FILES_SPEC,
    RM_SPEC,
    PIP_INSTALL_SPEC,
]
TOOL_FUNCTIONS = {
    "calculate": calculate,
    "ls": ls,
    "cat": cat,
    "grep": grep,
    "doctests": doctests,
    "write_file": write_file,
    "write_files": write_files,
    "rm": rm,
    "pip_install": pip_install,
}
EXIT_COMMANDS = {"/exit", "/quit"}


def live_doctests_enabled():
    """Return True when live Groq doctests should run.

    >>> isinstance(live_doctests_enabled(), bool)
    True
    """
    return bool(os.getenv("GROQ_API_KEY"))


def _doctest_result_has_failures(content):
    """Return True if a doctest tool result string reports failures.

    >>> _doctest_result_has_failures('1 item had failures.')
    True
    >>> _doctest_result_has_failures('Failed example')
    True
    >>> _doctest_result_has_failures('5 items passed all tests')
    False
    >>> _doctest_result_has_failures('error: unsafe path')
    False
    >>> _doctest_result_has_failures('')
    False
    """
    return (
        "items had failures" in content
        or "item had failures" in content
        or "Failed example" in content
    )


class Chat:
    """Chat with a language model that can use local document tools.

    The class keeps conversation history in `messages`, sends user messages to
    Groq, and handles any tool calls requested by the model.

    >>> result = True
    >>> if live_doctests_enabled():
    ...     chat = Chat()
    ...     reply = chat.send_message(
    ...         'Use the ls tool on the tools directory and reply with the '
    ...         'exact filename calculate.py.',
    ...         temperature=0.0,
    ...     )
    ...     result = 'calculate.py' in reply and any(
    ...         message.get('role') == 'tool'
    ...         and message.get('name') == 'ls'
    ...         for message in chat.messages
    ...     )
    >>> result
    True
    >>> result = True
    >>> if live_doctests_enabled():
    ...     chat = Chat()
    ...     _ = chat.send_message(
    ...         'Remember that my name is Isaiah. Reply with OK.',
    ...         temperature=0.0,
    ...     )
    ...     result = 'isaiah' in chat.send_message(
    ...         'What name did I ask you to remember? Reply with just the '
    ...         'name.',
    ...         temperature=0.0,
    ...     ).lower()
    >>> result
    True
    """

    def __init__(self, client=None, debug=False):
        """Create a chat session.

        Class behavior is demonstrated in the class docstring.
        """
        self.client = client
        self.debug = debug
        self.timeout = 30
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Write the output in 1-2 sentences. "
                    "Use tools when you need to inspect files or do math."
                ),
            },
        ]

    def send_message(self, message, temperature=0.0):
        """Send a user message and return the assistant response.

        >>> chat = Chat(client=Groq(api_key='invalid-key'))
        >>> chat.send_message('hi').startswith('error:')
        True
        """
        self.messages.append({"role": "user", "content": message})
        return self._complete_with_tools(temperature)

    def run_manual_command(self, line):
        """Run a slash command and add the result to the conversation context.

        >>> chat = Chat(client=False)
        >>> chat.run_manual_command('/calculate 6 * 7')
        '42'
        >>> chat.messages[-1]['content']
        'Manual tool /calculate returned:\\n42'
        >>> chat.run_manual_command('/nope')
        'error: unknown command nope'
        >>> chat.run_manual_command('/')
        'error: missing command'
        >>> chat.run_manual_command('/cat "unfinished')
        'error: No closing quotation'
        """
        try:
            parts = shlex.split(line[1:])
        except ValueError as error:
            return f"error: {error}"

        if not parts:
            return "error: missing command"

        command = parts[0]
        args = manual_args(command, parts[1:])
        result = run_tool(command, args)
        self.messages.append(
            {
                "role": "user",
                "content": f"Manual tool /{command} returned:\n{result}",
            }
        )
        return result

    def _complete_with_tools(self, temperature):
        """Call Groq until the assistant returns a final text response.

        Implements the Ralph Wiggum loop: if doctests fail after the model
        tries to give a final answer, force another round of tool usage.

        Class behavior is demonstrated in the class docstring.
        """
        if self.client is None:
            self.client = Groq(timeout=self.timeout)

        for _ in range(10):
            try:
                response = self.client.chat.completions.create(
                    messages=self.messages,
                    model="llama-3.1-8b-instant",
                    temperature=temperature,
                    tools=TOOL_SPECS,
                    tool_choice="auto",
                )
            except AuthenticationError:
                return (
                    "error: invalid GROQ_API_KEY. "
                    "Set a valid key in your shell or .env file."
                )
            message = response.choices[0].message
            tool_calls = getattr(message, "tool_calls", None)

            if not tool_calls:
                content = message.content or ""
                # Ralph Wiggum loop: force another round if doctests failed
                if self._last_doctests_failed():
                    self.messages.append(
                        {"role": "assistant", "content": content}
                    )
                    self.messages.append({
                        "role": "user",
                        "content": (
                            "Some doctests are still failing. "
                            "Please fix and run doctests again."
                        ),
                    })
                    continue
                self.messages.append({"role": "assistant", "content": content})
                return content

            self.messages.append(assistant_tool_message(message))
            for tool_call in tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments or "{}")
                content = run_tool(name, kwargs=arguments)
                if self.debug:
                    print(format_debug_tool_call(name, arguments))
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": content,
                    }
                )

        return "error: too many tool calls"

    def _last_doctests_failed(self):
        """Return True if the most recent doctests tool result shows failures.

        >>> chat = Chat(client=False)
        >>> chat._last_doctests_failed()
        False
        >>> chat.messages.append({'role': 'tool', 'name': 'doctests', 'content': '5 items passed all tests'})
        >>> chat._last_doctests_failed()
        False
        >>> chat.messages.append({'role': 'tool', 'name': 'doctests', 'content': '1 item had failures.'})
        >>> chat._last_doctests_failed()
        True
        """
        for msg in reversed(self.messages):
            if msg.get("role") == "tool" and msg.get("name") == "doctests":
                return _doctest_result_has_failures(msg.get("content", ""))
        return False


def assistant_tool_message(message):
    """Convert a Groq assistant message with tool calls into a plain dict.

    >>> from types import SimpleNamespace
    >>> call = SimpleNamespace(
    ...     id='abc',
    ...     type='function',
    ...     function=SimpleNamespace(name='ls', arguments='{"path": "."}'),
    ... )
    >>> message = SimpleNamespace(content=None, tool_calls=[call])
    >>> result = assistant_tool_message(message)
    >>> result['role']
    'assistant'
    >>> result['tool_calls'][0]['function']['arguments']
    '{"path": "."}'
    """
    return {
        "role": "assistant",
        "content": message.content,
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": getattr(tool_call, "type", "function"),
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
            for tool_call in message.tool_calls
        ],
    }


def manual_args(command, args):
    """Convert slash-command arguments into the shape expected by a tool.

    >>> manual_args('calculate', ['2', '+', '3'])
    ['2 + 3']
    >>> manual_args('grep', ['alpha', '*.txt'])
    ['alpha', '*.txt']
    >>> manual_args('ls', [])
    []
    """
    if command == "calculate" and args:
        return [" ".join(args)]
    return args


def run_tool(name, args=None, kwargs=None):
    """Run one named tool with positional or keyword arguments.

    >>> run_tool('calculate', ['2 + 2'])
    '4'
    >>> run_tool('ls', kwargs={'path': 'missing-folder'})
    ''
    >>> run_tool('unknown')
    'error: unknown command unknown'
    >>> run_tool('cat')
    "error: cat() missing 1 required positional argument: 'path'"
    """
    args = args or []
    kwargs = kwargs or {}
    function = TOOL_FUNCTIONS.get(name)
    if function is None:
        return f"error: unknown command {name}"

    try:
        if kwargs:
            return function(**kwargs)
        return function(*args)
    except TypeError as error:
        return f"error: {error}"


def format_debug_tool_call(name, arguments):
    """Format a tool call for debug output.

    >>> format_debug_tool_call('ls', {'path': '.github'})
    '[tool] /ls .github'
    >>> format_debug_tool_call('calculate', {'expression': '2 + 2'})
    '[tool] /calculate 2 + 2'
    >>> format_debug_tool_call('ls', {})
    '[tool] /ls'
    """
    if not arguments:
        return f"[tool] /{name}"
    argument_text = " ".join(str(value) for value in arguments.values())
    return f"[tool] /{name} {argument_text}"


def repl(chat=None, temperature=0.0):
    """Run the interactive command line loop.

    >>> import contextlib, io, sys
    >>> old_stdin = sys.stdin
    >>> sys.stdin = io.StringIO('/calculate 2 + 2\\n/exit\\n')
    >>> buf = io.StringIO()
    >>> with contextlib.redirect_stdout(buf):
    ...     repl()
    >>> sys.stdin = old_stdin
    >>> '4' in buf.getvalue()
    True
    """
    try:
        import readline  # noqa: F401
    except ImportError:
        pass
    chat = chat or Chat()
    try:
        while True:
            user_input = input("chat> ")
            if user_input.strip() in EXIT_COMMANDS:
                break
            if user_input.startswith("/"):
                print(chat.run_manual_command(user_input))
            else:
                print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()


def parse_args(argv=None):
    """Parse command line arguments.

    >>> parse_args([]).debug
    False
    >>> parse_args(['--debug']).debug
    True
    >>> parse_args(['hello', 'world']).message
    ['hello', 'world']
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("message", nargs="*")
    return parser.parse_args(argv)


def main(argv=None):
    """Run one command line message or start the interactive REPL.

    Exits with an error if the current directory is not a git repository.
    Loads AGENTS.md into the conversation context if present.

    >>> result = True
    >>> if live_doctests_enabled():
    ...     import contextlib, io
    ...     buf = io.StringIO()
    ...     with contextlib.redirect_stdout(buf):
    ...         main(['Reply', 'with', 'only', 'the', 'word', 'pong.'])
    ...     result = 'pong' in buf.getvalue().lower()
    >>> result
    True
    """
    if not os.path.isdir(".git"):
        print("error: no .git folder found in the current directory.")
        return

    args = parse_args(argv)
    chat = Chat(debug=args.debug)

    if os.path.isfile("AGENTS.md"):
        agents_content = cat("AGENTS.md")
        chat.messages[0]["content"] += f"\n\nAGENTS.md:\n{agents_content}"

    if args.message:
        print(chat.send_message(" ".join(args.message)))
    else:
        repl(chat=chat)


if __name__ == "__main__":
    main()
