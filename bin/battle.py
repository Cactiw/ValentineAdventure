
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
    parse = re.search("\\[(\\d+)\\]", mes.text)
    if mes.text.startswith("⚔️"):
        if parse is None:
            bot.send_message(chat_id=mes.from_user.id, text="Цель не распознана")
            return
        target_id = int(parse.group(1))
        player.select_battle_action(battle, "attack", target_id, session)
        bot.send_message(chat_id=mes.from_user.id, text="Ты приготовился ⚔атаковать")
    else:
        dispatcher.bot.send_message(chat_id=player.id, text=battle.get_battle_text(),
                                    parse_mode='HTML', reply_markup=battle.get_battle_buttons(player))


