from telegram.ext import MessageHandler, CommandHandler, Filters

from work_materials.globals import Base, engine, dispatcher, updater, session

from bin.game import start, text_entered, inv

from libs.Quest import Quest

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('inv', inv))
dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, text_entered))

#

Base.metadata.create_all(engine)
Quest.load_quests()

logging.info("Starting pooling")
updater.start_polling(clean=False)
updater.idle()

session.close_all()
