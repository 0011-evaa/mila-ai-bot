"""
Brain of Mila AI.

Цей модуль вирішує,
що потрібно зробити з повідомленням користувача.
"""

from memory import get_user_memory


def decide_next_action(user_id: int) -> str:
    user = get_user_memory(user_id)

    # Новий користувач
    if user["current_language"] is None:
        return "assessment"

    # Якщо ще триває діагностика
    if user["assessment_mode"]:
        return "assessment"

    # В майбутньому тут буде:
    #
    # if homework:
    #     return "homework"
    #
    # if conversation:
    #     return "conversation"
    #
    # if pronunciation:
    #     return "pronunciation"

    return "lesson"