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
    return ReplyKeyboardMarkup(class_select_buttons, resize_keyboard=True)


def build_buttons_menu(buttons,
                       n_cols,
                       header_buttons=None,
                       footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
