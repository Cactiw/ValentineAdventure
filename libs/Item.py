from work_materials.globals import Base
from sqlalchemy import Column, INT, ForeignKey, UniqueConstraint, VARCHAR
from sqlalchemy.orm import relationship, backref

import logging


class ItemRel(Base):

    __tablename__ = "itemrel"

    item_id = Column(INT, ForeignKey('items.id'), nullable=False)
    player_id = Column(INT, ForeignKey('players.id'), nullable=False)
    quantity = Column(INT, default=1)

    __table_args__ = (
        UniqueConstraint('item_id', 'player_id', name='unique_record')
    )


class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False)

    item = relationship('ItemRel', backref=backref('item'))


