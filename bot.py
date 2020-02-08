from telegram.ext import MessageHandler, CommandHandler

from work_materials.globals import Base, engine, dispatcher, updater

from bin.game import start

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


dispatcher.add_handler(CommandHandler('start', start))

#

Base.metadata.create_all(engine)

updater.start_polling(clean=False)
updater.idle()

