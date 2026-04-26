"""Deterministic tests for compacting chat history and image loading."""

from pathlib import Path

from chat import Chat
from chat import SlashCompleter


class FakeClient:
    """Small fake completion client that always returns one fixed string."""

    def __init__(self, content):
        self.content = content
        self.chat = self
        self.completions = self

    def create(self, **_kwargs):
        """Return one synthetic completion response."""
        message = type(
            "Message",
            (),
            {"content": self.content, "tool_calls": None},
        )()
        choice = type("Choice", (), {"message": message})()
        return type("Response", (), {"choices": [choice]})()


def test_compact_history_replaces_messages_with_one_summary_entry():
    """Compaction preserves system instructions and drops old turns."""
    chat = Chat(client=FakeClient("short summary"))
    chat.messages.append({"role": "user", "content": "Fix README.md"})

    summary = chat.compact_history()

    assert summary == "short summary"
    assert len(chat.messages) == 1
    assert chat.messages[0]["role"] == "system"
    assert (
        "Conversation summary:\nshort summary"
        in chat.messages[0]["content"]
    )


def test_load_image_manual_command_adds_image_message(tmp_path, monkeypatch):
    """The image loader appends a multimodal user message to chat history."""
    monkeypatch.chdir(tmp_path)
    Path("sample.png").write_bytes(b"png-bytes")
    chat = Chat(client=False)

    result = chat.run_manual_command("/load_image sample.png")

    assert result == "Loaded image sample.png"
    assert chat.messages[-2]["content"][1]["type"] == "image_url"
    assert chat.messages[-1]["content"] == (
        "Manual tool /load_image returned:\nLoaded image sample.png"
    )


def test_slash_completer_lists_commands_and_paths(tmp_path, monkeypatch):
    """Tab-completion suggestions cover commands and file paths."""
    monkeypatch.chdir(tmp_path)
    Path("alpha.txt").write_text("a", encoding="utf-8")
    completer = SlashCompleter(["ls", "load_image"])

    assert completer.command_matches("/l") == ["/load_image", "/ls"]
    assert completer.path_matches("alp") == ["alpha.txt"]
