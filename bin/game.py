

from work_materials.globals import Session

from libs.Player import Player

from bin.buttons import get_class_select_buttons


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет! Пришли мне id своей половинки!\n"
                          "Твой id: <code>{}</code>".format(update.message.from_user.id), parse_mode='HTML')


def id_entered(bot, update):
    mes = update.message
    try:
        player_id = int(mes.text)
    except ValueError:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис. Введите число.")
        return
    session = Session()
    cur_player = session.query(Player).get(mes.from_user.id)
    player: Player = session.query(Player).get(player_id)
    if player is None:
        bot.send_message(chat_id=mes.chat_id, text="Этот человек ещё не зарегистрирован.")
        return
    if cur_player.pair_id is not None and cur_player.progress:
        bot.send_message(chat_id=mes.chat_id, text="У вас уже выбрана пара.")
        return
    if player.pair_id is not None and player.pair_id != cur_player.id:
        bot.send_message(chat_id=mes.chat_id, text="У другого игрока уже выбрана пара, и это не вы!")
        return
    cur_player.pair_id = player.pair_id
    if player.pair_id is not None and player.pair_id == cur_player.pair_id:
        buttons = get_class_select_buttons()
        bot.send_message(chat_id=mes.chat_id, text="Поздравляем! Ваш выбор совпал!\nВыберите класс",
                         reply_markup=buttons)
        bot.send_message(chat_id=player.id, text="Поздравляем! Ваш выбор совпал!\nВыберите класс",
                         reply_markup=buttons)
        # Начало игры
    else:
        bot.send_message(chat_id=mes.chat_id, text="Хорошо. Теперь Ваша половинка должна также выбрать вас.")
        bot.send_message(chat_id=mes.chat_id, text="@{} хочет сыграть с вами! Для согласия выберите его:\n"
                                                   "id: <code>{}<code>".format(cur_player.username,
                                                                               cur_player.id), parse_mode='HTML')


def class_selected(bot, update):
    pass
