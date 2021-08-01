from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from config.config import *
import os.path


class TelegramChat:

    def __init__(self, camera, dispatcher, callbackUpdate):
        self.camera = camera
        self.updateStatus = callbackUpdate
        
        self.sayCommand = f"/{SAY_COMMAND} {self.camera.name} "
        self.playSoundCommand = f"/{PLAY_COMMAND} {self.camera.name} "

        dispatcher.add_handler(MessageHandler(Filters.regex(f"{NOTIFY_ON} {self.camera.name}"), self.enableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(f"{NOTIFY_OFF} {self.camera.name}"), self.disableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(f"{self.camera.name} {IMAGE}"), self.getImmagine))

        dispatcher.add_handler(MessageHandler(Filters.regex(self.sayCommand), self.textToSpeech))
        dispatcher.add_handler(MessageHandler(Filters.regex(self.playSoundCommand), self.playSound))


    def enableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(True, update, CallbackContext)


    def disableCam(self, update: Update, context: CallbackContext):
        self.__setCamera(False, update, CallbackContext)


    def enableNotification(self, update: Update, context: CallbackContext):
        self.__setNotification(True, update, CallbackContext)
    

    def disableNotification(self, update: Update, context: CallbackContext):
        self.__setNotification(False, update, CallbackContext)


    def __setNotification(self, enabled, update: Update, context: CallbackContext):
        self.camera.setNotification(enabled)
        self.updateStatus()
    

    def textToSpeech(self, update: Update, context: CallbackContext):
        text = update.message.text.replace(self.sayCommand, "")
        if len(text) == 0:
            update.message.reply_text(EMPTY_ARGS)
        else:
            update.message.reply_text(TTS_SAYING(text))
            self.camera.textToSpeech(text)
    

    def playSound(self, update: Update, context: CallbackContext):
        print("self.playSoundCommand")
        filename = SOUND_SAVE_PATH + update.message.text.replace(self.playSoundCommand, "") + ".wav"
        if os.path.isfile(filename):
            update.message.reply_text(PLAYING_FILE(filename))
            self.camera.sendSound(filename)
        else:
            update.message.reply_text(FILE_NOT_FOUND(filename))


    def __setCamera(self, enabled, update: Update, context: CallbackContext):
        status = STATUS_ONLINE if enabled else STATUS_OFFLINE
        update.message.reply_text(SET_STATUS(self.camera.name, status))
        if self.camera.enableCam(enabled):
            update.message.reply_text(CAMERA_STATE(self.camera.name, status))
        else:
            update.message.reply_text(CAMERA_SET_FAILED(self.camera.name))


    def getImmagine(self, update: Update, context: CallbackContext):
        self.camera.sendImage(force = True)