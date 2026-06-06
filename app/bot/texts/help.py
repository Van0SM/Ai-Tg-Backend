from typing import Final

HELP_TEXT_BLOCKS: Final[dict[str, str]] = {
    "about": """
<code>🤖 Что это?</code>

AI-бот, который помогает превратить
сырой запрос в понятную и точную
инструкцию для нейросети.

Вы описываете задачу своими словами —
бот помогает получить сильный результат
без сложного prompt engineering.""",
    "features": """
<code>⚡ Что умеет?</code>

• улучшает и структурирует ваши запросы

• помогает точнее объяснить задачу AI

• отправляет готовый ответ нейросети

• в разы упрощает работу с AI""",
    "start": """
<code>🚀 Как начать?</code>

Нажмите 
<code>💬 Новый диалог</code>
и просто опишите задачу своими словами.""",
}


def get_help_text(
    text_block: str,
) -> str:
    return HELP_TEXT_BLOCKS.get(text_block, "Help block not found")
