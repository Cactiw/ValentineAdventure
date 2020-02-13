from work_materials.globals import Base, Session
from sqlalchemy import Column, INT, ForeignKey, UniqueConstraint, VARCHAR
from sqlalchemy.orm import relationship, backref

from libs.Player import Player


class ItemRel(Base):

    __tablename__ = "itemrel"

    item_id = Column(INT, ForeignKey('items.id'), nullable=False)
    player_id = Column(INT, ForeignKey('players.id'), nullable=False)
    quantity = Column(INT, default=1)

    __table_args__ = (
        UniqueConstraint('item_id', 'player_id', name='unique_record')
    )

    def reduce_quantity(self, n=1):
        if self.quantity == n:
            # TODO Удалить из таблицы
            pass
        elif self.quantity < n:
            raise ValueError('Not enough items!')
        else:
            self.quantity -= n

    def increase_quantity(self, n=1):
        self.quantity += n

    def get_inventory(self, player):
        if isinstance(player, int):
            id = player
        elif isinstance(player, Player):
            id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        return Session().query(ItemRel.item_id, ItemRel.quantity).filter_by(player_id=id)




class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False)

    item = relationship('ItemRel', backref=backref('item'))


