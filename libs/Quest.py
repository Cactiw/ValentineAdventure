
from resources.quests import quests

from bin.buttons import build_buttons_menu

from telegram import ReplyKeyboardMarkup

import logging


class Quest:

    quests = {}  # { id: Quest }

    def __init__(self, quest_id: int, quest_type: str, enter_text: str, answers: {str: [ int ] }):
        self.id = quest_id
        self.type = quest_type
        self.enter_text = enter_text
        self.answers = answers

    def start(self, player):
        pass

    def get_enter_text(self):
        return self.enter_text

    def get_buttons(self, progress={}):
        answers = []
        for text, d in tuple(self.answers.items()):
            path, curr_progress = d.get("path"), d.get("progress", 0)
            if d.get("path") is None:
                answers.append(text)
            elif curr_progress == progress.get(path, 0):
                answers.append(text)
        return ReplyKeyboardMarkup(build_buttons_menu(tuple(self.answers.keys()), 2), resize_keyboard=True)

    def verify_quest_answer(self, answer):
        return answer in tuple(self.answers.keys())

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



