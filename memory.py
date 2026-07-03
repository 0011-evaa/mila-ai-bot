import json
from pathlib import Path
from typing import Any, Dict

MEMORY_FILE = Path("memory.json")

DEFAULT_USER_MEMORY = {
    "czech_level": "unknown",
    "english_level": "unknown",
    "current_language": None,
    "assessment_mode": None,
    "assessment_step": 0,
    "assessment_answers": [],
    "known_topics": [],
    "mistakes": [],
    "vocabulary": [],
    "lesson_count": 0,
}


def load_memory() -> Dict[str, Any]:
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_memory(memory: Dict[str, Any]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=2)


def get_user_memory(user_id: int) -> Dict[str, Any]:
    memory = load_memory()
    user_data = memory.get(str(user_id), {})
    merged = DEFAULT_USER_MEMORY.copy()
    merged.update(user_data)
    return merged


def update_user_memory(user_id: int, user_memory: Dict[str, Any]) -> None:
    memory = load_memory()
    memory[str(user_id)] = user_memory
    save_memory(memory)


def remember_interaction(user_id: int, user_text: str, bot_text: str) -> None:
    user_memory = get_user_memory(user_id)
    user_memory.setdefault("last_interactions", [])
    user_memory["last_interactions"].append({"user": user_text, "bot": bot_text})
    user_memory["last_interactions"] = user_memory["last_interactions"][-10:]
    update_user_memory(user_id, user_memory)
