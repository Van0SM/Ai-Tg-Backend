import httpx
from typing import Any

from app.core.config import settings

from app.ai.schemas import ChatMessage, OpenRouterResponse
from app.ai.constants import OPENROUTER_URL
from app.ai.prompts import SYSTEM_PROMPT, GEN_TITLE_PROPMPT


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
            "temperature": 0.4,
        }

    async def _request_openrouter(
        self,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> OpenRouterResponse:
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

    def extract_content(
        self,
        response: OpenRouterResponse,
    ) -> str:
        return response["choices"][0]["message"]["content"]

    def validate_response(
        self,
        response: OpenRouterResponse,
    ) -> None:
        error = response.get("error")

        if error is not None:
            raise ValueError(error["message"])

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

    # Зарефакторить и разобраться, когда будет настроение
    def split_long_message(
        self,
        content: str,
        max_length: int = 4000,
    ) -> list[str]:
        paragraphs = content.split("\n")

        chunks: list[str] = []
        current_chunk = ""

        for paragraph in paragraphs:
            paragraph_with_newline = paragraph + "\n"

            if len(paragraph_with_newline) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                    current_chunk = ""

                for i in range(0, len(paragraph_with_newline), max_length):
                    part = paragraph_with_newline[i : i + max_length]
                    chunks.append(part.rstrip())

                continue

            if len(current_chunk) + len(paragraph_with_newline) <= max_length:
                current_chunk += paragraph_with_newline
            else:
                chunks.append(current_chunk.rstrip())
                current_chunk = paragraph_with_newline

        if current_chunk:
            chunks.append(current_chunk.rstrip())

        return chunks

    async def generate_title(
        self,
        last_message: str,
    ) -> str:
        system_message: ChatMessage = {
            "role": "system",
            "content": GEN_TITLE_PROPMPT,
        }

        user_message: ChatMessage = {
            "role": "user",
            "content": last_message,
        }

        payload = self.build_payload(messages=[system_message, user_message])

        response = await self._request_openrouter(
            payload=payload,
            headers=self.build_headers(),
        )

        self.validate_response(response=response)

        return self.extract_content(response=response)
