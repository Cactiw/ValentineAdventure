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

    def reduce_quantity(self, n=1, use=False):
        if self.quantity == n:
            if use:
                self.item.use(times=n)
            session = Session()
            session.delete(self)
            session.commit()
        elif self.quantity < n:
            raise ValueError('Not enough items!')
        else:
            if use:
                self.item.use(times=n)
            self.quantity -= n


    def increase_quantity(self, n=1):
        self.quantity += n

    @staticmethod
    def get_inventory(player, as_string=False):
        if isinstance(player, int):
            id = player
        elif isinstance(player, Player):
            id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        session = Session()
        inv = session.query(ItemRel.item, ItemRel.quantity).filter_by(player_id=id)
        if not as_string:
            return inv
        else:
            res = f"Твой инвентарь:\n"
            for item, quantity in inv:
                res += str(item) + f" ({quantity})\n"
            return res


class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False, unique=True)

    item = relationship('ItemRel', backref=backref('item'))

    def __repr__(self):
        return f"- {self.name}"

    def use(self, times=1):
        pass

    @staticmethod
    def get(id: int):
        session = Session()
        return session.query(Item).get(id)


