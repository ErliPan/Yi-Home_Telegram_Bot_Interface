import telegram
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

        dispatcher.add_handler(MessageHandler(Filters.regex(NOTIFY_ON(self.camera.name)), self.enableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(NOTIFY_OFF(self.camera.name)), self.disableNotification))
        dispatcher.add_handler(MessageHandler(Filters.regex(TURNING_ON(self.camera.name)), self.enableCam))
        dispatcher.add_handler(MessageHandler(Filters.regex(TURNING_OFF(self.camera.name)), self.disableCam))

        dispatcher.add_handler(MessageHandler(Filters.regex(IMAGE(self.camera.name)), self.getImmagine))
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


    def __setCamera(self, enabled, update: Update, context: CallbackContext):
        reply_markup = telegram.ReplyKeyboardMarkup([[WAIT]])
        if enabled:
            update.message.reply_text(SET_STATUS_ON(self.camera.name), parse_mode="HTML", reply_markup = reply_markup)
        else:
            update.message.reply_text(SET_STATUS_OFF(self.camera.name), parse_mode="HTML", reply_markup = reply_markup)

        if self.camera.enableCam(enabled) == False:
            update.message.reply_text(SET_STATUS_FAILED(), parse_mode="HTML")

        self.updateStatus()


    def textToSpeech(self, update: Update, context: CallbackContext):
        text = update.message.text.replace(self.sayCommand, "")
        if len(text) == 0:
            update.message.reply_text(EMPTY_ARGS, parse_mode="HTML")
        else:
            update.message.reply_text(TTS_SAYING(text), parse_mode="HTML")
            self.camera.textToSpeech(text)


    def playSound(self, update: Update, context: CallbackContext):
        text = update.message.text.replace(self.playSoundCommand, "")
        if len(text) == 0:
            update.message.reply_text(EMPTY_ARGS, parse_mode="HTML")
        else:
            filename = SOUND_SAVE_PATH + text + ".wav"
            if os.path.isfile(filename):
                update.message.reply_text(PLAYING_FILE(filename), parse_mode="HTML")
                self.camera.sendSound(filename)
            else:
                update.message.reply_text(FILE_NOT_FOUND(filename), parse_mode="HTML")


    def getImmagine(self, update: Update, context: CallbackContext):
        self.camera.sendImage(force = True)