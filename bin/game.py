from telegram import ReplyKeyboardRemove

from work_materials.globals import Session, game_classes

from libs.Player import Player
from libs.ItemRel import ItemRel

from bin.buttons import get_class_select_buttons


def get_session_and_player(update):
    session = Session()
    player = session.query(Player).get(update.message.from_user.id)
    return [session, player]


def start(bot, update):
    mes = update.message
    session = Session()
    cur_player = session.query(Player).get(mes.from_user.id)
    if cur_player is None:
        cur_player = Player(id=mes.from_user.id, username=mes.from_user.username, status="selecting_game_class")

    else:
        cur_player.status = "selecting_game_class"  # TODO поставить заглушку
    session.add(cur_player)
    session.commit()
    bot.send_message(cur_player.id, text="Привет! Выбери класс, за который будешь играть!",
                     reply_markup=get_class_select_buttons())
    session.close()



def class_selected(bot, update):
    mes = update.message
    if mes.text not in game_classes:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис. Выберите один из перечисленных классов.")
        return
    session = Session()
    player: Player = session.query(Player).get(mes.from_user.id)
    player.set_game_class(mes.text)
    player.status = "awaiting_pair_id"
    player.update(session)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Хорошо, <b>{}</b>! Пришли мне id своей половинки!\n"
                          "Твой id: <code>{}</code>".format(player.game_class, update.message.from_user.id),
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode='HTML')


def id_entered(bot, update):
    mes = update.message
    try:
        player_id = int(mes.text)
    except ValueError:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис. Введите число.")
        return
    session = Session()
    cur_player: Player = session.query(Player).get(mes.from_user.id)
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
    cur_player.pair_id = player.id
    if player.pair_id is not None and player.pair_id == cur_player.id:
        bot.send_message(chat_id=mes.chat_id, text="Поздравляем! Ваш выбор совпал!")
        bot.send_message(chat_id=player.id, text="Поздравляем! Ваш выбор совпал!")
        player.progress_both_to_quest(0, session)
        # Начало игры
    else:
        bot.send_message(chat_id=mes.chat_id, text="Хорошо. Теперь Ваша половинка должна также выбрать вас.")
        bot.send_message(chat_id=player.id, text="@{} хочет сыграть с вами! Для согласия выберите его:\n"
                                                   "id: <code>{}</code>".format(cur_player.username,
                                                                               cur_player.id), parse_mode='HTML')
    player.update(session)
    cur_player.update(session)
    session.close()


def quest_variant_chosen(bot, update):
    mes = update.message
    session, player = get_session_and_player(update)
    if not player.verify_quest_answer(mes.text):
        # bot.send_message(chat_id=player.id, text="Ответ не распознан. Пожалуйста, используйте кнопки")
        player.send_current_quest_message()
        return
    player.chose_variant(mes.text, session)



def text_entered(bot, update):
    """
    Функция, которая определяет, какой callback запустить на основе статуса игрока
    :param bot:
    :param update:
    :return:
    """
    mes = update.message
    session, player = get_session_and_player(update)
    if player is None:
        bot.send_message(chat_id=mes.chat_id, text="Вы не зарегистрированы. Нажмите /start")
        return
    if player.status == "selecting_game_class":
        return class_selected(bot, update)
    elif player.status == "awaiting_pair_id":
        return id_entered(bot, update)
    elif player.status == "quest":
        quest_variant_chosen(bot, update)


    else:
        pass
        # unknown_response(bot, update)


def inv(bot, update):
    player_id = update.message.from_user.id
    inv = ItemRel.get_inventory(player_id)
    res = f"Твой инвентарь:\n" if len(inv) > 0 else "Твой инвентарь пуст!"
    for item, quantity in inv:
        res += str(item) + f" ({quantity})\n"
    bot.send_message(chat_id=update.message.chat_id, text=res)
