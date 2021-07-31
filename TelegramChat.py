from telegram import *
from telegram.ext import *

class TelegramChat:

    def __init__(self, camera, dispatcher):
        self.camera = camera

        dispatcher.add_handler(MessageHandler(Filters.regex(f"{camera.name} On"), self.enableCam))
        dispatcher.add_handler(MessageHandler(Filters.regex(f"{camera.name} Off"), self.disableCam))
        dispatcher.add_handler(MessageHandler(Filters.regex(camera.name), self.getImmagine))


    def enableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(True, update)
    
    
    def disableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(False, update)

    
    def __setCamera(self, enabled, update: Update):
        status = "On" if enabled else "Off"
        update.message.reply_text(f"Trying to set {self.camera.name} {status}...")
        if self.camera.enableCam(enabled):
            update.message.reply_text(f"{self.camera.name} is {status}")
        else:
            update.message.reply_text(f"Trying to set {self.camera.name} failed")


    def getImmagine(self, update: Update, context: CallbackContext):
        self.camera.sendImage()