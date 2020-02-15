

from libs.Buff import Buff


class Skill:
    def __init__(self, name, max_cooldown, game_class):
        self.name = name
        self.cooldown = 0
        self.max_cooldown = max_cooldown
        self.game_class = game_class

        self.player = None

    def set_player(self, player):
        self.player = player
        return self

    def check_ready(self):
        return self.cooldown <= 0

    def set_cooldown(self):
        self.cooldown = self.max_cooldown
        return self

    def reduce_cooldown(self):
        self.cooldown -= 1 if self.cooldown > 0 else 0
        return self

    def use(self, *args, **kwargs):
        raise NotImplemented


class CriticalHit(Skill):
    DAMAGE_MULTIPLIER = 2

    def use(self, target):
        dealt_damage = target.reduce_hp(self.player.get_attack_damage() * CriticalHit.DAMAGE_MULTIPLIER)
        return "{} {} {} (-{}🌡️)\n".format(self.player.username, self.name, target.username, dealt_damage)


class BattleCry(Skill):
    DAMAGE_MULTIPLIER = 1.5

    def use(self, target):
        target.add_buff(Buff("Battle Cry", "attack", 60, percents=True, duration=3))
        return "{} {} {} \n".format(self.player.username, self.name, target.username)


skills = [CriticalHit("CriticalHit", 2, "⚔Рыцарь"), BattleCry("BattleCry", 2, "⚔Рыцарь")]

