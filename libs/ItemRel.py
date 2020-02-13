from work_materials.globals import Base, Session
from sqlalchemy import Column, INT, ForeignKey, PrimaryKeyConstraint

# Необщодимый импорт, без него не работает
from libs.Item import Item


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
        """
        Возвращает отношение по id игрока и предмета либо по объектам классов (определяет как работать сам
        :param player: id игрока, либо экземпляр класса Player
        :param item:  id предмета, либо экземпляр класса Item
        :return: Класс ItemRel с полями item, player и quantity (item и player - экземпляры классов)
        """
        from libs.Player import Player
        if isinstance(player, int):
            player_id = player
        elif isinstance(player, Player):
            player_id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        from libs.Item import Item
        if isinstance(player, int):
            item_id = player
        elif isinstance(item, Item):
            item_id = player.id
        else:
            raise TypeError('item is not int nor class Item')

        session = Session()
        res = session.query(ItemRel).filter_by(item_id=item_id, player_id=player_id).first()
        session.close()
        return res


    def reduce_quantity(self, n=1, use=False):
        """
        Уменьшает количество предметов в записи на n и, если нужно вызывает функцию use() для каждого предмета
        :param n: Количество предметов, которое нужно изъять
        :param use: Нужно ли использовать предмет
        :return: None
        """
        if self.quantity == n:
            if use:
                self.item.use(times=n)
            session = Session()
            session.delete(self)
            session.commit()
            session.close()
        elif self.quantity < n:
            raise ValueError('Not enough items!')
        else:
            if use:
                self.item.use(times=n)
            self.quantity -= n


    def increase_quantity(self, n=1):
        """
        Добавляет n предметов
        :param n: Количество предметов
        :return: None
        """
        self.quantity += n


    @staticmethod
    def get_inventory(player):
        """
        Возвращает инвентарь игрока
        :param player: id игрока либо экземпляр класса Player чей инвентарь нужно получить
        :return: список из tuple (item, quantity)
        """
        from libs.Player import Player
        if isinstance(player, int):
            id = player
        elif isinstance(player, Player):
            id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        session = Session()
        query = session.query(ItemRel).filter_by(player_id=id).all()
        inv = [(i.item, i.quantity) for i in query]
        session.close()
        return inv