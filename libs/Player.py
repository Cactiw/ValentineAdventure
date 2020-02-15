from sqlalchemy import Column, ForeignKey, INT, VARCHAR, BOOLEAN
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.orm.attributes import flag_modified

from telegram import ReplyKeyboardMarkup

from libs.Quest import Quest
from libs.ItemRel import ItemRel
from libs.Item import Item
from libs.Enemy import Enemy

from work_materials.globals import Base, dispatcher

import logging
import traceback
from uuid import uuid4

class Player(Base):
    __tablename__ = "players"
    id = Column(INT, primary_key=True)
    username = Column(VARCHAR)
    game_class = Column(VARCHAR)
    link = Column(VARCHAR)

    pair_id = Column(INT, ForeignKey('players.id'))
    pair = relationship("Player", uselist=False, backref=backref('parent', remote_side=[id]))

    quest_id = Column(INT)
    selected = Column(BOOLEAN, default=False)
    selected_variant = Column(VARCHAR)
    progress = Column(JSONB, default={})
    status = Column(VARCHAR)

    battle_id = Column(INT)
    battle_status = Column(VARCHAR)
    battle_action = Column(VARCHAR)
    battle_target = Column(INT)

    attack = Column(INT, default=1)
    hp = Column(INT, default=15)
    max_hp = Column(INT, default=15)
    alive = Column(BOOLEAN, default=True)

    player = relationship('ItemRel', backref='player', lazy='subquery')

    def set_game_class(self, new_class):
        self.game_class = new_class

    def update(self, session: Session):
        cur_session = session.object_session(self) or session
        try:
            cur_session.add(self)
        except Exception:
            logging.warning(traceback.format_exc())
            cur_session.merge(self, load=True)
        cur_session.commit()

    def check_has_pair_selected(self, answer=None):
        if self.pair is None:
            raise RuntimeError
        return self.pair.selected and (answer is None or answer == self.pair.selected_variant)

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
        self.selected_variant = answer
        self.update(session)
        quest = self.get_active_quest()
        current: {str: {}} = quest.answers.get(answer)
        if self.check_has_pair_selected() or not current.get("wait_companion"):
            # Оба выбрали, или не нужно ждать второго - прогресс
            battle: dict = current.get("battle")
            path: dict = current.get("path")
            if battle is not None:
                # Начинается бой
                from bin.battle import start_battle
                d_enemies: dict = battle.get("enemies")
                enemies = []
                for name, enemy in list(d_enemies.items()):
                    enemies.append(Enemy.load_enemy(name, enemy))
                start_battle(self, enemies, session)

            elif path is not None:
                # Действия на этой локации
                progress = self.progress.get(path, 0)
                self.update_progress(path, progress + current.get("add_progress", 1))
                dispatcher.bot.send_message(chat_id=self.id, text=current.get("first_text"), parse_mode='HTML',
                                            reply_markup=quest.get_buttons(progress=self.progress))
                dispatcher.bot.send_message(chat_id=self.pair_id, text=current.get("second_text"), parse_mode='HTML',
                                            reply_markup=quest.get_buttons(progress=self.pair.progress))
                # print(self.pair.progress)
                self.update(session)
            else:
                self.progress_both_to_quest(current.get("new_id"), session)
            pass
        else:
            # Пара не выбрала
            dispatcher.bot.send_message(chat_id=self.id, text="Принято. Ожидай решение партнёра")

    def send_current_quest_message(self):
        dispatcher.bot.send_message(self.id, text=self.get_active_quest().get_enter_text(), parse_mode='HTML',
                                    reply_markup=self.get_active_quest().get_buttons(self.progress))


    def progress_both_to_quest(self, quest_id, session: Session):
        self.set_quest(quest_id, session)
        self.pair.set_quest(quest_id, session)

    def set_variant(self, variant, session: Session):
        self.selected = True
        self.selected_variant = variant
        self.update(session)

    def finish_quest(self, selected):
        pass

    def update_progress(self, key, value):
        self.progress.update({key: value})
        flag_modified(self, "progress")

    def set_battle(self, battle, session):
        self.status = "battle"
        self.selected = False
        self.battle_id = battle.id
        self.battle_status = None

        self.update(session)

        dispatcher.bot.send_message(chat_id=self.id, text="Битва начинается!\n{}".format(battle.get_battle_text()),
                                    parse_mode='HTML', reply_markup=battle.get_battle_buttons(self))

    def start_battle(self, battle, session):
        self.set_battle(battle, session)
        self.pair.set_battle(battle, session)

    def select_battle_action(self, battle, action_type, target_id, session):
        self.selected = True
        self.battle_action = action_type
        self.battle_target = target_id


        if self.check_has_pair_selected(None):
            battle.tick(session)

            self.selected = False
            self.pair.selected = False
        self.update(session)
        self.pair.update(session)

    def get_attack_damage(self):
        return self.attack

    def reduce_hp(self, damage, session):
        self.hp -= damage
        if self.hp <= 0:
            self.death(session)
        return damage

    def death(self, session):
        self.status = "death"
        self.quest_id = 0
        buttons = ReplyKeyboardMarkup([['/start']])
        dispatcher.bot.send_message(chat_id=self.id, text="Смерть, окончательная и бесповоротная разлучила ваши сердца!"
                                                          "\nНачать заного можно по команде /start",
                                    reply_markup=buttons)
        self.update(session)
        self.pair.quest_id = 0
        self.pair.status = 0
        dispatcher.bot.send_message(chat_id=self.pair.id,
                                    text="Смерть, окончательная и бесповоротная разлучила ваши сердца!\n"
                                         "Начать заного можно по команде /start",
                                    reply_markup=buttons)
        self.pair.update(session)

    def get_current_battle(self, session):
        from libs.Battle import Battle
        battle = Battle.get_battle(self.battle_id)
        if battle is None:
            dispatcher.bot.send_message(chat_id=self.id, text="Ошибка при поиске битвы. "
                                                              "Возвращаюсь в последнюю локацию.")
            self.progress_both_to_quest(self.quest_id, session)
            raise RuntimeError
        else:
            return battle

    #

    def add_item(self, item, quantity=1):
        """
        Добавляет запись в таблицу itemrel
        :param item: id предмена или экземпляр класса Item
        :param quantity: количество предметов
        :return: None
        """
        if isinstance(item, int):
            id = item
        elif isinstance(item, Item):
            id = item.id
        else:
            raise TypeError('item is not int nor class Item')
        session = Session()
        rel = ItemRel(item_id=id, player_id=self.id, quantity=quantity)
        session.add(rel)
        session.commit()


    def get_inventory(self):
        """
        Получает инвентарь игрока
        :return: Список из tuple (item: Item, quantity: int)
        """
        return ItemRel.get_inventory(self)


