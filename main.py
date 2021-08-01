from TelegramNotifyer import Telegram
from DummyNotifyer import Dummy

from YiHomeCamera import YiCam
from IPCam import IPCam
from SaveVideo import SaveVideo

from TelegramChat import TelegramChat

from config import *

import time
import os
import os.path
from multiprocessing import Process

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler


class main:

    def __init__(self):
        #polymorphism (?)
        self.notifyer = SaveVideo(Telegram(), MEDIA_SAVE_PATH)
        camera = YiCam
        self.cameraStatus = ""
        self.cams = []

        for CAMERA in CAMERAS:
            self.cams.append(IPCam(self.notifyer, camera(CAMERA[0], sensitivity = CAMERA[2]), CAMERA[1]))


        botUpdater = Updater(TOKEN)
        dispatcher = botUpdater.dispatcher

        #Make them start at the same time (more or less)
        for cam in self.cams:
            cam.start()
            TelegramChat(cam, dispatcher, self.updateStatus)


        dispatcher.add_handler(MessageHandler(Filters.regex(ONLINE_LIST), self.updateStatus))
        dispatcher.add_handler(CommandHandler(PLAY_COMMAND, self.playSound))
        dispatcher.add_handler(CommandHandler(SAY_COMMAND, self.textToSpeech))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.voiceMethod))


        botUpdater.start_polling()

        while True:
            self.deleteOldMedia(MEDIA_SAVE_PATH, 7)
            self.updateStatus(force = False)
            time.sleep(10)

    
    def textToSpeech(self, update: Update, context: CallbackContext):
        text = SOUND_SAVE_PATH + " ".join(context.args)
        update.message.reply_text(TTS_SAYING(text))
        self.__playTTS(text)


    def playSound(self, update: Update, context: CallbackContext):
        filename = SOUND_SAVE_PATH + " ".join(context.args) + ".wav"
        if os.path.isfile(filename):
            update.message.reply_text(PLAYING_FILE(filename))
            self.__playAudio(filename, self.cams)
        else:
            update.message.reply_text(FILE_NOT_FOUND(filename))


    def voiceMethod(self, update: Update, context: CallbackContext):
        update.message.reply_text(PLAY_VOICE)
        newFile = update.message.effective_attachment.get_file()
        newFile.download(AUDIO_TEMP_FILE)
        os.system(f"ffmpeg -i {AUDIO_TEMP_FILE} -acodec pcm_s16le -ac 1 -ar 16000 {AUDIO_TEMP_FILE}.wav -y")
        self.__playAudio(AUDIO_TEMP_FILE + ".wav", self.cams)
        os.unlink(AUDIO_TEMP_FILE)
        os.unlink(AUDIO_TEMP_FILE + ".wav")


    def __playTTS(self, text, cams):
        proc = []
        for cam in cams:
            proc.append(Process(target=cam.textToSpeech, args=(text, )))
        for p in proc:
            p.start()
        for p in proc:
            p.join()


    def __playAudio(self, filename, cams):
        proc = []
        for cam in cams:
            proc.append(Process(target=cam.sendSound, args=(filename, )))
        for p in proc:
            p.start()
        for p in proc:
            p.join()


    def deleteOldMedia(self, path, olderThanDays):
        current_time = time.time()
        for f in os.listdir(path):
            f = path + f
            creation_time = os.path.getctime(f)
            if (current_time - creation_time) // (24 * 3600) >= olderThanDays:
                os.unlink(f)
                print('{} removed'.format(f))


    def updateStatus(self, update: Update = None, context: CallbackContext = None, force = True):
        stat = self.getOnlineStatus()
        if stat != self.cameraStatus or force:
            self.cameraStatus = stat
            try:
                self.notifyer.sendMessage(CAMERA_STATUS, self.cameraStatus, reply_markup = self.generateKeyboard())
            except Exception as e:
                print(e) #If too many messages have been sent, an exception can occur #FIXME


    def generateKeyboard(self):
        keyboard = []
        for cam in self.cams:
            if cam.isOnline():
                status = TURNING_ON if not cam.sendNotification() else TURNING_OFF
                keyboard.append([f"{cam.getName()} {IMAGE}", f"{status} {cam.getName()}"])

        keyboard.append([ONLINE_LIST])
        return keyboard


    def getOnlineStatus(self):
        msg = ""
        for cam in self.cams:
            status = STATUS_ONLINE if cam.isOnline() else STATUS_OFFLINE
            notification = INTENT_YES if cam.sendNotification() else INTENT_NO
            msg += ONLINE_STATUS_MSG(cam.name, status, notification)

        return msg



if __name__ == "__main__":
    main()