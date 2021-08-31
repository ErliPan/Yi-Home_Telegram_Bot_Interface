from Notifyer.Telegram import Telegram
from Notifyer.SaveVideo import SaveVideo
from YiHomeCamera import YiCam
from IPCam import IPCam
from TelegramChat import TelegramChat
import config.config as CONFIG
from multiprocessing import Process
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler
import time, os, os.path

class main:

    def __init__(self):
        #polymorphism (?)
        self.notifyer = SaveVideo(Telegram(), CONFIG.MEDIA_SAVE_PATH, compressVideo = CONFIG.VIDEO_COMPRESSION)
        camera = YiCam
        self.cameraStatus = ""
        self.cams = []

        for cam in CONFIG.CAMERAS:
            self.cams.append(IPCam(self.notifyer, camera(cam[0], sensitivity = cam[2]), cam[1]))

        botUpdater = Updater(CONFIG.TOKEN)
        dispatcher = botUpdater.dispatcher

        #Make them start at the same time (more or less)
        for cam in self.cams:
            cam.start()
            TelegramChat(cam, dispatcher, self.updateStatus)

        dispatcher.add_handler(MessageHandler(Filters.regex(CONFIG.CAMERA_STATUS), self.updateStatus))  # Get camera status
        dispatcher.add_handler(MessageHandler(Filters.voice, self.playVoice)) #Audio message
        dispatcher.add_handler(CommandHandler(CONFIG.PLAY_COMMAND, self.playSound))  # Play .wav audio
        dispatcher.add_handler(CommandHandler(CONFIG.SAY_COMMAND, self.textToSpeech))  # TTS command

        botUpdater.start_polling()

        while True:
            self.deleteOldMedia(CONFIG.MEDIA_SAVE_PATH, CONFIG.MEDIA_RETENTION)
            self.updateStatus(force = False)
            time.sleep(10)

    
    def textToSpeech(self, update: Update, context: CallbackContext):
        if update.message.chat.id != CONFIG.CHATID:
            return #Ignore messages not from the chatid
        text = " ".join(context.args)
        if len(text) == 0:
            update.message.reply_text(CONFIG.EMPTY_ARGS, parse_mode="HTML")
        else:
            update.message.reply_text(CONFIG.TTS_SAYING(text), parse_mode="HTML")
            self.__playTTS(text, self.cams)


    def playSound(self, update: Update, context: CallbackContext):
        if update.message.chat.id != CONFIG.CHATID:
            return #Ignore messages not from the chatid
        text = " ".join(context.args)
        if len(text) == 0:
            update.message.reply_text(CONFIG.EMPTY_ARGS, parse_mode="HTML")
        else:
            filename = CONFIG.SOUND_SAVE_PATH + text + ".wav"
            if os.path.isfile(filename):
                update.message.reply_text(CONFIG.PLAYING_FILE(filename), parse_mode="HTML")
                self.__playAudio(filename, self.cams)
            else:
                update.message.reply_text(CONFIG.FILE_NOT_FOUND(filename), parse_mode="HTML")


    def playVoice(self, update: Update, context: CallbackContext):
        if update.message.chat.id != CONFIG.CHATID:
            return #Ignore messages not from the chatid
        update.message.reply_text(CONFIG.PLAY_VOICE, parse_mode="HTML")
        update.message.effective_attachment.get_file().download(CONFIG.AUDIO_TEMP_FILE)
        #Convert to 16 bit mono
        os.system(f"ffmpeg -i {CONFIG.AUDIO_TEMP_FILE} -acodec pcm_s16le -ac 1 -ar 16000 {CONFIG.AUDIO_TEMP_FILE}.wav -y")
        self.__playAudio(CONFIG.AUDIO_TEMP_FILE + ".wav", self.cams)
        os.unlink(CONFIG.AUDIO_TEMP_FILE)
        os.unlink(CONFIG.AUDIO_TEMP_FILE + ".wav")


    def __playTTS(self, text, cams):
        #Use multiprocessing to send the command all at the same time
        proc = []
        for cam in cams:
            if cam.isOnline():
                proc.append(Process(target=cam.textToSpeech, args=(text, )))
        for p in proc:
            p.start()
        for p in proc:
            p.join()


    def __playAudio(self, filename, cams):
        #Use multiprocessing to send the command all at the same time
        proc = []
        for cam in cams:
            if cam.isOnline():
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


    def updateStatus(self, update: Update = None, context: CallbackContext = None, force = True, count = 0):
        if update != None and update.message.chat.id != CONFIG.CHATID:
            return #Ignore messages not from the chatid
        stat = self.__getOnlineStatus()

        if force:
            self.cameraStatus = stat
            try:
                self.notifyer.sendMessage(CONFIG.CAMERA_STATUS, self.cameraStatus, reply_markup=self.__generateKeyboard())
            except Exception as e:
                print(e)

        if stat != self.cameraStatus:
            if count >= CONFIG.STATE_CHANGE_DELAY:
                self.updateStatus(update, context, force=True)
            else:
                self.updateStatus(update, context, count=count + 1)


    def __generateKeyboard(self):
        keyboard = []
        for cam in self.cams:
            notifyAction = CONFIG.NOTIFY_OFF(cam.getName()) if cam.sendNotification() else CONFIG.NOTIFY_ON(cam.getName())
            onOffAction = CONFIG.TURNING_OFF(cam.getName()) if cam.isEnabled() else CONFIG.TURNING_ON(cam.getName())
            
            if cam.isOnline():
                if cam.isEnabled():
                    keyboard.append([CONFIG.IMAGE(cam.getName())])
                    keyboard.append([notifyAction, onOffAction])
                else:
                    keyboard.append([onOffAction])

        keyboard.append([CONFIG.CAMERA_STATUS])
        return keyboard


    def __getOnlineStatus(self):
        msg = ""
        for cam in self.cams:
            if cam.isOnline():
                if cam.isEnabled():
                    notification = CONFIG.NOTIFICATION_YES if cam.sendNotification() else CONFIG.NOTIFICATION_NO
                    msg += CONFIG.STATUS_ONLINE(cam.name, notification)
                else:
                    msg += CONFIG.STATUS_DISABLED(cam.name)
            else:
                msg += CONFIG.STATUS_OFFLINE(cam.name)

        return msg


if __name__ == "__main__":
    main()
