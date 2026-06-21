import httpx
import json
from typing import Any

from app.core.config import settings

from app.ai.schemas import ChatMessage
from app.ai.constants import SYSTEM_PROMPT, OPENROUTER_URL


class AIClient:
    def __init__(self) -> None:
        self.model = settings.openrouter_model
        self.api_key = settings.openrouter_api_key

    def build_messages(
        self,
        context: list[ChatMessage],
    ) -> list[ChatMessage]:
        system_message: ChatMessage = {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }

        return [system_message] + context

    def build_payload(
        self,
        messages: list[ChatMessage],
    ) -> dict[str, object]:
        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1000,
        }

    async def _request_openrouter(
        self,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=OPENROUTER_URL,
                headers=headers,
                json=payload,
            )

            return response.json()

    def build_headers(self) -> dict[
        str,
        str,
    ]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def create_response(
        self,
        context: list[ChatMessage],
    ) -> str:
        messages = self.build_messages(
            context=context,
        )

        payload = self.build_payload(
            messages=messages,
        )

        headers = self.build_headers()

        response = await self._request_openrouter(
            payload=payload,
            headers=headers,
        )

        print(response)

        self.validate_response(
            response=response,
        )

        return self.extract_content(
            response=response,
        )

    def extract_content(
        self,
        response: dict[str, Any],
    ) -> str:
        return response["choices"][0]["message"]["content"]

    def validate_response(
        self,
        response: dict[str, Any],
    ) -> None:
        error = response.get("error")

        if error is not None:
            raise ValueError(error["message"])
