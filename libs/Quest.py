
from resources.quests import quests

import logging


class Quest:

    quests = {}  # { id: Quest }

    def __init__(self, quest_id: int, quest_type: str, enter_text: str, answer_variants: {str: [ int ] }):
        self.id = quest_id
        self.type = quest_type
        self.enter_text = enter_text
        self.answers = answer_variants

    def start(self, player):
        pass

    def get_enter_text(self):
        return self.enter_text

    @staticmethod
    def get_quest(quest_id: int) -> "Quest":
        return Quest.quests.get(quest_id)

    @staticmethod
    def load_quests():
        """
        Метод загрузки всех квестов из ресурсов, вызывается один раз при старте бота
        :return: None
        """
        logging.info("Loading quests...")

        for quest_id, data in list(quests.items()):
            data.update({"quest_id": quest_id})
            Quest.quests.update({quest_id: Quest(**data)})

        logging.info("Quests loaded.")



