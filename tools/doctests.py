"""Run doctests for the chat agent."""

import ast
import contextlib
import doctest as stdlib_doctest
import io
import pathlib

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "doctests",
        "description": (
            "Run doctests (with --verbose) on a safe relative Python file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to a Python file.",
                },
            },
            "required": ["path"],
        },
    },
}


def doctests(path):
    """Run doctests with --verbose on a safe relative Python file.

    >>> doctests('/etc/passwd')
    'error: unsafe path'
    >>> doctests('../secret.py')
    'error: unsafe path'
    >>> doctests('docs/../secret.py')
    'error: unsafe path'
    """
    if not is_path_safe(path):
        return "error: unsafe path"

    file_path = pathlib.Path(path)
    module_name = file_path.stem
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    globals_dict = {"__file__": str(file_path), "__name__": module_name}
    exec(compile(source, str(file_path), "exec"), globals_dict)

    parser = stdlib_doctest.DocTestParser()
    items = []
    for name, docstring in iter_docstrings(tree, module_name):
        examples = parser.get_examples(docstring or "")
        if examples:
            items.append((name, examples))

    output = []
    failures = 0
    total_tests = 0
    failed_items = []

    for name, examples in items:
        item_failures = 0
        item_globals = globals_dict.copy()
        for example in examples:
            total_tests += 1
            output.append("Trying:\n")
            output.append(indent_block(example.source.rstrip("\n")))
            if example.want:
                output.append("Expecting:\n")
                output.append(indent_block(example.want.rstrip("\n")))
            else:
                output.append("Expecting nothing\n")
            ok, failure_output = run_example(
                example.source,
                example.want,
                item_globals,
                str(file_path),
            )
            if ok:
                output.append("ok\n")
            else:
                failures += 1
                item_failures += 1
                output.append(failure_output)
        if item_failures:
            failed_items.append((name, item_failures, len(examples)))

    if failures:
        if len(failed_items) == 1:
            label = "item had failures"
        else:
            label = "items had failures"
        output.append(f"{len(failed_items)} {label}:\n")
        for name, item_failures, example_count in failed_items:
            output.append(
                f"   {item_failures} of   {example_count} in {name}\n"
            )
        output.append(f"{total_tests} tests in {len(items)} items.\n")
        output.append(
            f"{total_tests - failures} passed and {failures} failed.\n"
        )
        output.append(f"***Test Failed*** {failures} failures.\n")
    else:
        output.append(f"{len(items)} items passed all tests:\n")
        for name, examples in items:
            output.append(f"   {len(examples)} tests in {name}\n")
        output.append(f"{total_tests} tests in {len(items)} items.\n")
        output.append(f"{total_tests} passed.\n")
        output.append("Test passed.\n")

    return "".join(output)


def iter_docstrings(tree, module_name):
    """Yield `(name, docstring)` pairs from a parsed Python module.

    >>> module = ast.parse("'module'\\n\\ndef f():\\n    'doc'\\n")
    >>> list(iter_docstrings(module, 'sample'))
    [('sample', 'module'), ('sample.f', 'doc')]
    """
    module_doc = ast.get_docstring(tree, clean=False)
    if module_doc is not None:
        yield module_name, module_doc
    yield from iter_node_docstrings(tree.body, prefix=module_name)


def iter_node_docstrings(nodes, prefix):
    """Yield docstrings from classes and functions inside one AST body.

    >>> tree = ast.parse(
    ...     "class C:\\n    'doc'\\n    def m(self):\\n        'method'\\n"
    ... )
    >>> list(iter_node_docstrings(tree.body, '__main__'))
    [('__main__.C', 'doc'), ('__main__.C.m', 'method')]
    """
    for node in nodes:
        if isinstance(
            node,
            (ast.AsyncFunctionDef, ast.ClassDef, ast.FunctionDef),
        ):
            name = f"{prefix}.{node.name}"
            docstring = ast.get_docstring(node, clean=False)
            if docstring is not None:
                yield name, docstring
            if isinstance(node, ast.ClassDef):
                yield from iter_node_docstrings(node.body, prefix=name)


def run_example(source, expected, globals_dict, filename):
    """Execute one doctest example and compare it with expected output.

    >>> run_example('1 + 1\\n', '2\\n', {}, '<doctest>')[0]
    True
    >>> expected = (
    ...     'Traceback (most recent call last):\\n'
    ...     '...\\n'
    ...     'ValueError: x\\n'
    ... )
    >>> run_example(
    ...     'raise ValueError("x")\\n',
    ...     expected,
    ...     {},
    ...     '<doctest>',
    ... )[0]
    True
    """
    try:
        actual = execute_example(source, globals_dict, filename)
    except Exception as error:  # pragma: no cover - exercised by doctest above
        if wants_exception(expected):
            expected_line = final_expected_line(expected)
            actual_line = f"{type(error).__name__}: {error}"
            if actual_line == expected_line:
                return True, ""
            actual = (
                "Traceback (most recent call last):\n"
                f"...\n{actual_line}\n"
            )
            return False, format_failure(source, expected, actual)
        actual = (
            "Traceback (most recent call last):\n"
            f"...\n{type(error).__name__}: {error}\n"
        )
        return False, format_failure(source, expected, actual)

    if normalize_output(actual) == normalize_output(expected):
        return True, ""
    return False, format_failure(source, expected, actual)


def execute_example(source, globals_dict, filename):
    """Execute one example and return the text a REPL would display.

    >>> execute_example('1 + 1\\n', {}, '<doctest>')
    '2\\n'
    >>> execute_example('print("hi")\\n', {}, '<doctest>')
    'hi\\n'
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            compiled = compile(source, filename, "eval")
        except SyntaxError:
            exec(compile(source, filename, "exec"), globals_dict)
        else:
            result = eval(compiled, globals_dict)
            if result is not None:
                buffer.write(f"{result!r}\n")
    return buffer.getvalue()


def wants_exception(expected):
    """Return True when expected doctest output describes an exception.

    >>> wants_exception(
    ...     'Traceback (most recent call last):\\n...\\nValueError: x\\n'
    ... )
    True
    >>> wants_exception('2\\n')
    False
    """
    return expected.startswith("Traceback (most recent call last):")


def final_expected_line(expected):
    """Return the final non-ellipsis line from expected traceback text.

    >>> final_expected_line(
    ...     'Traceback (most recent call last):\\n...\\nValueError: x\\n'
    ... )
    'ValueError: x'
    """
    lines = [line for line in expected.strip().splitlines() if line != "..."]
    return lines[-1] if lines else ""


def normalize_output(text):
    """Normalize trailing newlines before comparing doctest output.

    >>> normalize_output('x\\n')
    'x'
    >>> normalize_output('')
    ''
    """
    return text.rstrip("\n")


def format_failure(source, expected, actual):
    """Format one doctest failure block in a verbose, readable form.

    >>> failure = format_failure('1 + 1\\n', '3\\n', '2\\n')
    >>> failure.splitlines()[:5]
    ['Failed example:', '    1 + 1', 'Expected:', '    3', 'Got:']
    """
    return (
        "Failed example:\n"
        f"{indent_block(source.rstrip(chr(10)))}"
        "Expected:\n"
        f"{indent_block(expected.rstrip(chr(10)))}"
        "Got:\n"
        f"{indent_block(actual.rstrip(chr(10)))}"
    )


def indent_block(text):
    """Indent a block the same way verbose doctest output does.

    >>> indent_block('a\\nb\\n')
    '    a\\n    b\\n'
    """
    if not text:
        return "    \n"
    return "".join(f"    {line}\n" for line in text.splitlines())
