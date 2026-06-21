from typing import TypedDict, Literal


class ChatMessage(TypedDict):
    role: Literal[
        "system",
        "user",
        "assistant",
    ]
    content: str


class OpenRouterMessage(TypedDict):
    role: str
    content: str


class OpenRouterChoice(TypedDict):
    message: OpenRouterMessage


class OpenRouterResponse(TypedDict):
    choices: list[OpenRouterChoice]
