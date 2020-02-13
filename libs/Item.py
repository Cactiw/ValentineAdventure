from work_materials.globals import Base, Session
from sqlalchemy import Column, INT, ForeignKey, PrimaryKeyConstraint, VARCHAR
from sqlalchemy.orm import relationship, backref

from libs.Player import Player


class ItemRel(Base):

    __tablename__ = "itemrel"

    item_id = Column(INT, ForeignKey('items.id'), nullable=False)
    player_id = Column(INT, ForeignKey('players.id'), nullable=False)
    quantity = Column(INT, default=1)

    __table_args__ = (
        PrimaryKeyConstraint('item_id', 'player_id', name='unique_record'),
    )

    @staticmethod
    def get_rel(player, item):
        if isinstance(player, int):
            player_id = player
        elif isinstance(player, Player):
            player_id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        if isinstance(player, int):
            item_id = player
        elif isinstance(item, Item):
            item_id = player.id
        else:
            raise TypeError('item is not int nor class Item')

        session = Session()
        return session.query(ItemRel).filter_by(item_id=item_id, player_id=player_id).first()

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

    @staticmethod
    def get_inventory(player):
        if isinstance(player, int):
            id = player
        elif isinstance(player, Player):
            id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        session = Session()
        return session.query(ItemRel.item_id, ItemRel.quantity).filter_by(player_id=id)



class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False, unique=True)

    item = relationship('ItemRel', backref=backref('item'))


