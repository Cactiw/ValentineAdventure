

class Buff:
    def __init__(self, name, stat, value, percents, duration):
        self.name: str = name
        self.stat: str = stat
        self.value: int = value
        self.percents: bool = percents
        self.duration: int = duration

    def check_active(self):
        return self.duration > 0

    def reduce_duration(self):
        self.duration -= 1 if self.duration > 0 else 0
        return self
