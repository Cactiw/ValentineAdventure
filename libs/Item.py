from work_materials.globals import Base, Session
from sqlalchemy import Column, INT, VARCHAR
from sqlalchemy.orm import relationship


class Item(Base):

    __tablename__ = "items"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(VARCHAR, nullable=False, unique=True)

    item_rel = relationship('ItemRel', backref='item', lazy='subquery')

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
        res =  session.query(Item).get(id)
        session.close()
        return res


    @staticmethod
    def get_by_name(name: str):
        """
        Получить предмет по имени
        :param name: Имя предмета
        :return: экземпляр класса Item
        """
        session = Session()
        res = session.query(Item).filter_by(name=name).first()
        session.close()
        return res

