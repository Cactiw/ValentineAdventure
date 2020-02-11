
from resources.items import items

import logging


class Item:
    items = {}

    def __init__(self, item_id: str, name: str):
        self.id = item_id
        self.name = name

    @staticmethod
    def get_item(item_id: str):
        return Item.items.get(item_id)

    @staticmethod
    def load_items():
        """
        Метод загрузки всех квестов из ресурсов, вызывается один раз при старте бота
        :return: None
        """
        logging.info("Loading items...")

        for item_id, data in list(items.items()):
            data.update({"item_id": item_id})
            Item.items.update({item_id: Item(**data)})

        logging.info("Items loaded.")

