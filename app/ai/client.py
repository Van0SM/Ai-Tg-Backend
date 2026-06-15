from app.core.config import settings

from app.ai.schemas import ChatMessage


class AIClient:
    def __init__(self) -> None:
        self.model = settings.openrouter_model
        self.api_key = settings.openrouter_api_key

    async def create_response(self, context: list[ChatMessage]) -> str:
        last_message = context[-1]["content"]

        return f"AI's response to: {last_message}"
