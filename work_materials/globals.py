from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession
from sqlalchemy.ext.declarative import declarative_base

from libs.bot_async_messaging import AsyncBot
from libs.updater_async import AsyncUpdater

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
