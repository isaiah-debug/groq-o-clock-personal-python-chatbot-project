"""Integration tests for manual commands and automatic tool calls."""

from types import SimpleNamespace
from unittest.mock import Mock

from chat import Chat


def completion(text):
    """Return a fake Groq completion with plain assistant text."""
    message = SimpleNamespace(content=text, tool_calls=None)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def tool_completion(name, arguments):
    """Return a fake Groq completion that requests one tool call."""
    tool_call = SimpleNamespace(
        id="call_1",
        type="function",
        function=SimpleNamespace(name=name, arguments=arguments),
    )
    message = SimpleNamespace(content=None, tool_calls=[tool_call])
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_manual_slash_command_adds_tool_output_to_context():
    """Manual slash commands run tools without calling the LLM."""
    client = Mock()
    chat = Chat(client=client)

    result = chat.run_manual_command("/calculate 6 * 7")

    assert result == "42"
    assert chat.messages[-1] == {
        "role": "user",
        "content": "Manual tool /calculate returned:\n42",
    }
    client.chat.completions.create.assert_not_called()


def test_automatic_tool_call_runs_local_tool_and_returns_final_answer():
    """Automatic tool calls run through the fake client and tool dispatcher."""
    client = Mock()
    client.chat.completions.create.side_effect = [
        tool_completion("calculate", '{"expression": "6 * 7"}'),
        completion("6 * 7 is 42."),
    ]
    chat = Chat(client=client)

    result = chat.send_message("what is six times seven?")

    assert result == "6 * 7 is 42."
    assert chat.messages[-2]["role"] == "tool"
    assert chat.messages[-2]["name"] == "calculate"
    assert chat.messages[-2]["content"] == "42"


def test_debug_mode_prints_tool_calls(capsys):
    """Debug mode prints the tool call before returning the final answer."""
    client = Mock()
    client.chat.completions.create.side_effect = [
        tool_completion("ls", '{"path": "."}'),
        completion("I checked the folder."),
    ]
    chat = Chat(client=client, debug=True)

    result = chat.send_message("what files are here?")

    assert result == "I checked the folder."
    assert "[tool] /ls ." in capsys.readouterr().out
