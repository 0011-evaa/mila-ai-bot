from openai import OpenAI
from prompts import SYSTEM_PROMPT


def build_context(user_memory: dict) -> str:
    interactions = user_memory.get("last_interactions", [])

    history_text = ""
    for item in interactions[-8:]:
        history_text += f"Учениця: {item.get('user')}\nМіла: {item.get('bot')}\n\n"

    return f"""
Поточна пам'ять учениці:
- Рівень чеської: {user_memory.get('czech_level')}
- Рівень англійської: {user_memory.get('english_level')}
- Поточна мова: {user_memory.get('current_language')}
- Відомі теми: {user_memory.get('known_topics')}
- Типові помилки: {user_memory.get('mistakes')}
- Словник: {user_memory.get('vocabulary')}
- Кількість уроків: {user_memory.get('lesson_count')}

Останній контекст розмови:
{history_text}

ВАЖЛИВО:
- Не починай діагностику заново, якщо вона вже триває.
- Продовжуй попередній урок або попереднє питання.
- Якщо учениця уточнює або заперечує, відповідай на це уточнення, а не став нове питання.
- Не повторюй одне й те саме.
"""


def ask_teacher(client: OpenAI, user_text: str, user_memory: dict) -> str:
    context = build_context(user_memory)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT + "\n\n" + context,
        input=user_text,
    )

    return response.output_text