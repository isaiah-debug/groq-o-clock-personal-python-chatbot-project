"""Helpers for loading local images into chat messages."""

import base64
import os

from tools.path_safety import is_path_safe


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "load_image",
        "description": (
            "Load a safe local image into the current chat session."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to a local image file.",
                },
            },
            "required": ["path"],
        },
    },
}


MIME_TYPES = {
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def build_image_message(path):
    """Return a chat message containing a safe local image as a data URL.

    >>> from pathlib import Path
    >>> _ = Path('tiny.png').write_bytes(b'not-really-a-png')
    >>> message = build_image_message('tiny.png')
    >>> message['role']
    'user'
    >>> message['content'][0]['type']
    'text'
    >>> message['content'][1]['type']
    'image_url'
    >>> Path('tiny.png').unlink()
    >>> build_image_message('/etc/passwd')
    Traceback (most recent call last):
    ...
    ValueError: unsafe path
    """
    if not is_path_safe(path):
        raise ValueError("unsafe path")

    suffix = os.path.splitext(path)[1].lower()
    mime_type = MIME_TYPES.get(suffix)
    if mime_type is None:
        raise ValueError("unsupported image type")

    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"Please use this image from {path} when answering.",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{encoded}",
                },
            },
        ],
    }
