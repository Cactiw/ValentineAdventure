
from libs.Player import Player
from libs.Enemy import Enemy

from telegram import keyboardbutton, ReplyKeyboardMarkup

from bin.buttons import build_buttons_menu
from work_materials.globals import dispatcher

import random


class Battle:
    battles = {}

    def __init__(self, players: [Player], enemies: [Enemy]):
        self.id: int = players[0].id
        self.players: [Player] = players
        self.enemies: [Enemy] = enemies

        for i, enemy in enumerate(self.enemies):
            enemy.battle_id = i

        Battle.battles.update({self.id: self})

    def get_battle_text(self):
        s = ""
        for player in self.players:
            s += Battle.format_participant_text(player)
        s += "\nВраги:\n"
        for enemy in self.enemies:
            s += Battle.format_participant_text(enemy)
        return s

    def get_battle_buttons(self, player):
        buttons = build_buttons_menu(["⚔️[{}]Атаковать {} {}🌡️"
                                      "".format(i.battle_id, i.username, i.hp) for i in filter(lambda x: x.alive,
                                                                                               self.enemies)], 2)
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    def tick(self, session):
        response = ""
        for player in self.players:
            if player.battle_action == "attack":
                response += self.attack(bot=False, target_id=player.battle_target, attacker=player, session=session)
        response += "\n"
        for enemy in self.enemies:
            # ИИ
            if not enemy.alive:
                pass
            else:
                # Атака
                response += self.attack(bot=True, target_id=random.randint(0, len(self.players) - 1), attacker=enemy,
                                        session=session)
        self.check_win(session)
        for player in self.players:
            dispatcher.bot.send_message(chat_id=player.id, text="{}\n{}".format(response, self.get_battle_text()),
                                        reply_markup=self.get_battle_buttons(player), parse_mode='HTML')



    def attack(self, bot: bool, target_id, attacker, session) -> str:
        target = self.players[target_id] if bot else self.enemies[target_id]
        dealt_damage = target.reduce_hp(attacker.get_attack_damage(), session)
        return "{} ⚔️атаковал {} (-{}🌡️)\n".format(attacker.username, target.username, dealt_damage)

    def check_win(self, session):
        for enemy in self.enemies:
            if not enemy.alive:
                self.end(win=True, session=session)
        return False

    def end(self, win: bool, session):
        if win:
            player = self.players[0]
            quest = player.get_active_quest()
            player.update(session)
            player.pair.update(session)
            player.progress_both_to_quest(quest.answers.get(player.selected_variant).get("new_id"), session)
        Battle.battles.pop(self.id)


    @staticmethod
    def format_participant_text(player):
        return "{}{}<b>{}</b>  {}🌡️\n" \
                "".format("" if player.alive else "✖", player.game_class[0], player.username, player.hp)

    @staticmethod
    def get_battle(battle_id: int) -> "Battle":
        return Battle.battles.get(battle_id)

