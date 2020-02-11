from sqlalchemy import Table, Column, ForeignKey, INT, VARCHAR, DATE, ARRAY, TEXT, BOOLEAN, BIGINT, FLOAT, func, and_, \
    or_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref, Session

from libs.Quest import Quest
from libs.Item import Item

from work_materials.globals import Base, dispatcher, Session as NewSession


inventory = Table('inventory', Base.metadata,
    Column('player_id', INT, ForeignKey('players.id')),
    Column('item_id', INT)
)




class Player(Base):
    __tablename__ = "players"
    id = Column(INT, primary_key=True)
    username = Column(VARCHAR)
    game_class = Column(VARCHAR)

    pair_id = Column(INT, ForeignKey('players.id'))
    pair = relationship("Player", uselist=False, backref=backref('parent', remote_side=[id]))

    quest_id = Column(INT)
    selected = Column(BOOLEAN, default=False)
    selected_variant = Column(VARCHAR)
    progress = Column(JSONB, default={})
    status = Column(VARCHAR)
    battle_status = Column(VARCHAR)

    hp = Column(INT)
    max_hp = Column(INT)

    # item_ids = relationship(INT, secondary=inventory)
    item_ids = []  # TODO fix inventory

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

    def get_active_quest(self) -> Quest:
        return Quest.get_quest(self.quest_id)

    def verify_quest_answer(self, answer):
        return self.get_active_quest().verify_quest_answer(answer)

    def set_quest(self, quest_id, session: Session):
        self.quest_id = quest_id
        self.selected = False
        self.status = "quest"
        self.progress.clear()

        quest = self.get_active_quest()
        quest.start(self)
        dispatcher.bot.send_message(chat_id=self.id, text=quest.get_enter_text(), parse_mode='HTML',
                                    reply_markup=quest.get_buttons())
        self.update(session)

    def chose_variant(self, answer: str, session: Session):
        self.selected = True
        self.update(session)
        quest = self.get_active_quest()
        current: {str: {}} = quest.answers.get(answer)
        if self.check_has_pair_selected() or not current.get("wait_companion"):
            # Оба выбрали, или не нужно ждать второго - прогресс
            path = current.get("path")
            if path is not None:
                # Действия на этой локации
                progress = self.progress.get(path, 0)
                self.progress.update({path: progress + current.get("add_progress", 1)})
                dispatcher.bot.send_message(chat_id=self.id, text=current.get("first_text"), parse_mode='HTML',
                                            reply_markup=quest.get_buttons(progress=self.progress))
                dispatcher.bot.send_message(chat_id=self.pair_id, text=current.get("second_text"), parse_mode='HTML',
                                            reply_markup=quest.get_buttons(progress=self.pair.progress))
                print(self.pair.progress)
                self.update(session)
            else:
                self.progress_both_to_quest(current.get("new_id"), session)
            pass
        else:
            # Пара не выбрала
            dispatcher.bot.send_message(chat_id=self.id, text="Принято. Ожидай решение партнёра")


    def progress_both_to_quest(self, quest_id, session: Session):
        self.set_quest(quest_id, session)
        self.pair.set_quest(quest_id, session)

    def set_variant(self, variant, session: Session):
        self.selected = True
        self.selected_variant = variant
        self.update(session)

    def finish_quest(self, selected):
        pass

    #

    def add_item(self, item_id, session):
        self.item_ids.append(item_id)
        self.update(session)



