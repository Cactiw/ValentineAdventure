
from libs.Skill import Skill, skills

import random
import copy


class Enemy:
    def __init__(self, name, lvl, hp, max_hp, attack):
        self.username = name
        self.lvl = lvl
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack

        self.game_class = "🖥"

        self.battle_id = -1
        self.alive = True

        self.buffs = []

        self.skills = {}
        self.fill_skills()

    def get_attack_damage(self):
        return self.attack

    def reduce_hp(self, value, *args):
        self.hp -= value
        self.check_death()
        return value

    def check_death(self) -> bool:
        if self.hp < 0:
            self.alive = False
        return self.alive

    def fill_skills(self):
        for skill in skills:
            if skill.game_class == "All" or skill.game_class == self.username:
                cur_skill = copy.deepcopy(skill)
                self.skills.update({cur_skill.name: cur_skill})
                cur_skill.set_player(self)

    def get_random_ready_skill(self):
        return random.choice(list(filter(lambda x: x.check_ready(), list(self.skills.values()))))

    #

    @staticmethod
    def load_enemy(name: str, d: dict) -> "Enemy":
        d.update({"name": name})
        return Enemy(**d)



