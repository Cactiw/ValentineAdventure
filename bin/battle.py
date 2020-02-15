
from libs.Player import Player
from libs.Enemy import Enemy
from libs.Battle import Battle


from work_materials.globals import dispatcher

import re


def start_battle(player: Player, enemies: [Enemy], session):
    battle = Battle([player, player.pair], enemies)
    player.start_battle(battle, session)


def process_battle_message(bot, update, player, session):
    mes = update.message
    battle = player.get_current_battle(session)
    print(player.battle_status)
    if player.battle_status == "choose_skill":
        player.select_battle_action(battle, mes.text, session)
        bot.send_message(chat_id=player.id, text="Выберите цель!", parse_mode='HTML',
                         reply_markup=battle.get_target_choose_buttons())
    elif player.battle_status == "choose_target":
        parse = re.search("\\[(\\d+)\\]", mes.text)
        if parse is None:
            bot.send_message(chat_id=mes.from_user.id, text="Цель не распознана")
            return
        target_id = int(parse.group(1))
        player.select_battle_target(battle, target_id, session)
        bot.send_message(chat_id=mes.from_user.id, text="Ты приготовился ⚔атаковать",
                         reply_markup=battle.get_battle_buttons(player))
    else:
        dispatcher.bot.send_message(chat_id=player.id, text=battle.get_battle_text(),
                                    parse_mode='HTML', reply_markup=battle.get_battle_buttons(player))


