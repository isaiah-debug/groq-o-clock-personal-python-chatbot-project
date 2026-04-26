"""Helpers for compacting chat history into a single summary message."""


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "compact",
        "description": (
            "Summarize the current conversation and replace chat history "
            "with a compact summary."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}


def format_transcript(messages):
    """Convert chat messages into text suitable for summarization.

    >>> format_transcript([{'role': 'user', 'content': 'hello'}])
    'user: hello'
    >>> format_transcript([
    ...     {
    ...         'role': 'user',
    ...         'content': [
    ...             {'type': 'text', 'text': 'look'},
    ...             {
    ...                 'type': 'image_url',
    ...                 'image_url': {'url': 'data:image/png;base64,AA=='},
    ...             },
    ...         ],
    ...     },
    ... ])
    'user: look [image]'
    """
    rendered = []
    for message in messages:
        content = message.get("content", "")
        if isinstance(content, list):
            parts = []
            for block in content:
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "image_url":
                    parts.append("[image]")
            content = " ".join(part for part in parts if part)
        rendered.append(
            f"{message.get('role', 'unknown')}: {content}".rstrip()
        )
    return "\n".join(rendered)


def build_compact_messages(system_prompt, summary):
    """Build the replacement message list used after compaction.

    >>> build_compact_messages('Follow instructions.', 'Work on README.')
    [{'role': 'system', 'content': 'Follow instructions.\\n\\n'
    ...  'Conversation summary:\\nWork on README.'}]
    """
    return [{
        "role": "system",
        "content": f"{system_prompt}\n\nConversation summary:\n{summary}",
    }]
