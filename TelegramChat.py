from telegram import *
from telegram.ext import *

class TelegramChat:

    def __init__(self, token, camera):
        self.camera = camera

        botUpdater = Updater(token)
        dispatcher = botUpdater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.regex(camera.name), self.getImmagine))
        botUpdater.start_polling()


    def getImmagine(self, update: Update, context: CallbackContext):
        self.camera.sendImage()