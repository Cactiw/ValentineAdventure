from sqlalchemy import Table, Column, ForeignKey, INT, VARCHAR, DATE, ARRAY, TEXT, BOOLEAN, BIGINT, FLOAT, func, and_, \
    or_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref, Session

from libs.Quest import Quest

from work_materials.globals import Base, dispatcher, Session as NewSession


class Player(Base):
    __tablename__ = "players"
    id = Column(INT, primary_key=True)
    username = Column(VARCHAR)
    game_class = Column(VARCHAR)

    pair_id = Column(INT, ForeignKey('players.id'))
    pair = relationship("Player", uselist=False, backref=backref('parent', remote_side=[id]))

    quest_id = Column(INT)
    selected = Column(BOOLEAN, default=False)
    progress = Column(JSONB)
    status = Column(VARCHAR)
    battle_status = Column(VARCHAR)

    hp = Column(INT)
    max_hp = Column(INT)

    #

    def set_game_class(self, new_class):
        self.game_class = new_class

    def update(self, session: Session):
        session.add(self)
        session.commit()


    def check_has_pair_selected(self):
        if self.pair is None:
            raise RuntimeError
        return self.pair.selected

    def set_quest(self, quest_id, session: Session):
        self.quest_id = quest_id
        self.selected = False
        self.status = "quest"

        quest = Quest.get_quest(quest_id)
        quest.start(self)
        dispatcher.bot.send_message(chat_id=self.id, text=quest.get_enter_text(), parse_mode='HTML')
        self.update(session)


    def progress_both_to_quest(self, quest_id, session: Session):
        self.set_quest(quest_id, session)
        self.pair.set_quest(quest_id, session)










