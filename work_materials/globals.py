from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession
from sqlalchemy.ext.declarative import declarative_base

from libs.bot_async_messaging import AsyncBot
from libs.updater_async import AsyncUpdater

import re
from config import psql_credentials, TOKEN, request_kwargs

engine = create_engine(f'postgresql+psycopg2://{psql_credentials["user"]}:{psql_credentials["pass"]}@'
                       f'{psql_credentials["host"]}:{psql_credentials["port"]}/{psql_credentials["dbname"]}',
                       echo=False)

Session = sessionmaker(bind=engine, autoflush=False)
session: SQLSession = Session()
Base = declarative_base()

bot = AsyncBot(token=TOKEN, workers=16, request_kwargs=request_kwargs)
updater = AsyncUpdater(bot=bot)

dispatcher = updater.dispatcher
job = updater.job_queue

bot.dispatcher = dispatcher


game_classes = ["⚗️Алхимик", "⚒Кузнец", "📦Добытчик", "🏹Лучник", "⚔Рыцарь", "🛡Защитник"]


sex_selected = ['👨 Парень', '👩 Девушка']


def multiple_replace(dic, text) -> str:
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], text)


def set_sexs(base_text: str, my_sex: int, parner_sex: int) -> str:
    my = {'[q]': ['к', 'ца'], '[w]': ['ку', 'це'], '[e]': ['ком', 'цей'], '[r]': ['', 'а'], '[t]': ['ся', 'ась'],
          '[y]': ['й', 'я'], '[u]': ['го', 'ё'], '[i]': ['му', 'й'], '[o]': ['ёл', 'ла'], '[p]': ['ый', 'ая'],
          '[a]': ['его', 'ю'], '[b]': ['ка', 'цу'], '[s]': ['им', 'ей'], '[d]': ['го', 'ей'], '[f]': ['ка', 'цы']}
    parner = {'[qq]': ['к', 'ца'], '[ww]': ['ку', 'це'], '[ee]': ['ком', 'цей'], '[rr]': ['', 'а'],
              '[tt]': ['ся', 'ась'], '[yy]': ['й', 'я'], '[uu]': ['го', 'ё'], '[ii]': ['му', 'й'], '[oo]': ['ёл', 'ла'],
              '[pp]': ['ый', 'ая'], '[aa]': ['его', 'ю'], '[bb]': ['ка', 'цу'], '[ss]': ['им', 'ей'], '[dd]': ['го', 'ей'],
              '[ff]': ['ка', 'цы']}

    for i in my:
        my[i] = my[i][my_sex]
    for i in parner:
        parner[i] = parner[i][parner_sex]
    my.update(parner)
    return multiple_replace(my, base_text)