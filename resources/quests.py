

quests = {
    0: {
        "quest_type": "quest",
        "enter_text": """Добро пожаловать в игру!""",
        "answers": {
            "Пойти вперёд": [1],
            "Прочитать табличку": [2, 3],
        }
    },
    1: {
        "quest_type": "quest",
        "enter_text": """Вы двинулись вперёд и встретили гоблина""",
        "answers": {
            "Спросить, откуда он": [3, 4],
            "Напасть": [5],
        }
    }
}
