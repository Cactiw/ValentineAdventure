from sqlalchemy import Table, Column, ForeignKey, INT, VARCHAR, DATE, ARRAY, TEXT, BOOLEAN, BIGINT, FLOAT, func, and_, \
    or_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from work_materials.globals import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(INT, primary_key=True)
    username = Column(VARCHAR)
    game_class = Column(VARCHAR)

    pair_id = Column(INT, ForeignKey('players.id'))
    pair = relationship("Player", uselist=False, backref=backref('parent', remote_side=[id]))

    progress = Column(JSONB)
    status = Column(VARCHAR)
    battle_status = Column(VARCHAR)

    hp = Column(INT)
    max_hp = Column(INT)


