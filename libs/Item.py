from work_materials.globals import Base
from sqlalchemy import Table, Column, ForeignKey, INT, VARCHAR, BOOLEAN
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref, Session

import logging


class ItemRel(Base):
    item_id = Column(INT, nullable=False)
    player_id = Column(INT, nullable=False)
    quantity = Column(INT, default=1)




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

