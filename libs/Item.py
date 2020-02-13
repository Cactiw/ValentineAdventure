from work_materials.globals import Base, Session
from sqlalchemy import Column, INT, ForeignKey, PrimaryKeyConstraint, VARCHAR
from sqlalchemy.orm import relationship

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
        """
        Возвращает отношение по id игрока и предмета либо по объектам классов (определяет как работать сам
        :param player: id игрока, либо экземпляр класса Player
        :param item:  id предмета, либо экземпляр класса Item
        :return: Класс ItemRel с полями item, player и quantity (item и player - экземпляры классов)
        """
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
        if isinstance(player, int):
            id = player
        elif isinstance(player, Player):
            id = player.id
        else:
            raise TypeError('player is not int nor class Player')

        session = Session()
        query = session.query(ItemRel).filter_by(player_id=id).all()
        inv = [(i.item, i.quantity) for i in query]
        return inv





class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False, unique=True)

    item_rel = relationship('ItemRel', backref='item')

    def __repr__(self):
        return f"- {self.name}"

    def use(self, times=1):
        pass

    @staticmethod
    def get(id: int):
        """
        Получить предмет по id
        :param id: id предмета
        :return: экземпляр класса Item
        """
        session = Session()
        return session.query(Item).get(id)


    @staticmethod
    def get_by_name(name: str):
        """
        Получить предмет по имени
        :param name: Имя предмета
        :return: экземпляр класса Item
        """
        session = Session()
        return session.query(Item).filter_by(name=name).first()

