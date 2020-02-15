

class Enemy:
    def __init__(self, name, lvl, hp, max_hp, attack, skills):
        self.username = name
        self.lvl = lvl
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.skills = skills

        self.game_class = "🖥"

        self.battle_id = -1
        self.alive = True

        self.buffs = []

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

    #

    @staticmethod
    def load_enemy(name: str, d: dict) -> "Enemy":
        d.update({"name": name})
        return Enemy(**d)



