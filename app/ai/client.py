from app.core.config import settings

from app.ai.schemas import ChatMessage


class AIClient:
    def __init__(self) -> None:
        self.model = settings.openrouter_model
        self.api_key = settings.openrouter_api_key

    def create_response(
        self,
        context: list[ChatMessage],
    ) -> str:
        last_message = context[-1]["content"]

        return f"AI's response to: {last_message}"

    def build_messages(
        self,
        context: list[ChatMessage],
    ) -> list[ChatMessage]:
        system_message: ChatMessage = {
            "role": "system",
            "content": "",
        }

        return [system_message] + context
