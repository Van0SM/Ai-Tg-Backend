from typing import TypedDict, Literal


class ChatMessage(TypedDict):
    role: Literal[
        "system",
        "user",
        "assistant",
    ]
    content: str
