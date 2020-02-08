from telegram import KeyboardButton, ReplyKeyboardMarkup


class_select_buttons = [
    [
        KeyboardButton("⚗️Алхимик"),
        KeyboardButton("⚒Кузнец"),
        KeyboardButton("📦Добытчик"),
    ],
    [
        KeyboardButton("🏹Лучник"),
        KeyboardButton("⚔Рыцарь"),
        KeyboardButton("🛡Защитник"),
    ],
    # [
    #     KeyboardButton("↩️ Назад"),
    # ]
]


def get_class_select_buttons():
    return ReplyKeyboardMarkup(class_select_buttons)

