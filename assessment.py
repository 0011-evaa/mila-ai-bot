ASSESSMENT_STEPS = {
    "czech": [
        "Напиши чеською: Мене звати ... Я з України.",
        "Переклади чеською: Я живу в Чехії вже два роки.",
        "Напиши 3 речення чеською про свій звичайний день.",
        "Уяви, що ти в магазині. Скажи чеською, що хочеш купити хліб і молоко.",
        "Напиши чеською: Вчора я була на роботі, а завтра піду до лікаря."
    ],
    "english": [
        "Write in English: My name is ... I am from Ukraine.",
        "Translate into English: Я живу в Чехії вже два роки.",
        "Write 3 sentences in English about your usual day.",
        "Imagine you are in a café. Order coffee and ask how much it costs.",
        "Write in English: Yesterday I was at work, and tomorrow I will go to the doctor."
    ]
}


def get_assessment_question(language: str, step: int) -> str:
    questions = ASSESSMENT_STEPS.get(language, [])
    if step < len(questions):
        return questions[step]
    return ""


def assessment_is_finished(language: str, step: int) -> bool:
    questions = ASSESSMENT_STEPS.get(language, [])
    return step >= len(questions)


def language_name(language: str) -> str:
    if language == "czech":
        return "чеської"
    if language == "english":
        return "англійської"
    return "мови"