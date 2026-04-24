"""Deterministic tests for local helper behavior."""

from types import SimpleNamespace

from chat import (
    Chat,
    assistant_tool_message,
    format_debug_tool_call,
    live_doctests_enabled,
    manual_args,
    run_tool,
)


def test_manual_slash_command_adds_tool_output_to_context():
    """Manual slash commands run tools without contacting the model."""
    chat = Chat(client=False)

    result = chat.run_manual_command("/calculate 6 * 7")

    assert result == "42"
    assert chat.messages[-1] == {
        "role": "user",
        "content": "Manual tool /calculate returned:\n42",
    }


def test_assistant_tool_message_converts_tool_calls_to_plain_dict():
    """Assistant messages with tool calls are converted to plain dicts."""
    call = SimpleNamespace(
        id="call_1",
        type="function",
        function=SimpleNamespace(name="ls", arguments='{"path": "."}'),
    )
    message = SimpleNamespace(content=None, tool_calls=[call])

    result = assistant_tool_message(message)

    assert result["role"] == "assistant"
    assert result["tool_calls"][0]["function"]["name"] == "ls"
    assert result["tool_calls"][0]["function"]["arguments"] == '{"path": "."}'


def test_manual_args_joins_calculate_expressions():
    """Slash-command parsing preserves calculator expressions."""
    assert manual_args("calculate", ["2", "+", "3"]) == ["2 + 3"]
    assert manual_args("grep", ["needle", "*.txt"]) == ["needle", "*.txt"]


def test_run_tool_reports_missing_arguments_and_unknown_commands():
    """Tool dispatch surfaces simple command errors as strings."""
    assert run_tool("calculate", ["2 + 2"]) == "4"
    assert run_tool("unknown") == "error: unknown command unknown"
    assert run_tool("cat") == (
        "error: cat() missing 1 required positional argument: 'path'"
    )


def test_format_debug_tool_call_and_live_flag_are_simple_strings_and_bools():
    """Debug formatting and live-doctest gating stay lightweight."""
    assert format_debug_tool_call(
        "ls",
        {"path": ".github"},
    ) == "[tool] /ls .github"
    assert format_debug_tool_call("ls", {}) == "[tool] /ls"
    assert isinstance(live_doctests_enabled(), bool)
