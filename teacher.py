from openai import OpenAI
from prompts import SYSTEM_PROMPT


def build_context(user_memory: dict) -> str:
    return f"""
Поточна пам'ять учениці:
- Рівень чеської: {user_memory.get('czech_level')}
- Рівень англійської: {user_memory.get('english_level')}
- Поточна мова: {user_memory.get('current_language')}
- Відомі теми: {user_memory.get('known_topics')}
- Типові помилки: {user_memory.get('mistakes')}
- Словник: {user_memory.get('vocabulary')}
- Кількість уроків: {user_memory.get('lesson_count')}
"""


def ask_teacher(client: OpenAI, user_text: str, user_memory: dict) -> str:
    context = build_context(user_memory)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT + "\n\n" + context,
        input=user_text,
    )

    return response.output_text
