from app.ai.schemas import ChatMessage


class AIClient:
    def __init__(self) -> None:
        pass

    async def create_response(self, context: list[ChatMessage]) -> str:
        last_message = context[-1]["content"]

        return f"AI's response to: {last_message}"
