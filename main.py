from TelegramNotifyer import Telegram
from DummyNotifyer import Dummy

from YiHomeCamera import YiCam
from IPCam import IPCam
from SaveVideo import SaveVideo

from TelegramChat import TelegramChat

import config as CONFIG

import telegram
import time

from telegram import *
from telegram.ext import *


class main:

    def __init__(self):
        #polymorphism (?)
        self.notifyer = SaveVideo(Telegram(CONFIG), CONFIG.MEDIA_SAVE_PATH)
        self.camera = YiCam

        self.cams = []

        for CAMERA in CONFIG.CAMERAS:
            self.cams.append(IPCam(self.notifyer, self.camera(CONFIG, CAMERA[0]), CAMERA[1]))


        botUpdater = Updater(CONFIG.TOKEN)
        dispatcher = botUpdater.dispatcher


        #Make them start at the same time (more or less)
        for cam in self.cams:
            cam.start()
            TelegramChat(cam, dispatcher, self.updateStatus)


        botUpdater.start_polling()

        self.cameraStatus = ""

        while True:
            self.updateStatus()
            time.sleep(10)


    def updateStatus(self, force = False):
        stat = self.getOnlineStatus()
        if stat != self.cameraStatus or force:
            self.cameraStatus = stat
            try:
                self.notifyer.sendMessage("Camera Status", self.cameraStatus, reply_markup = self.generateKeyboard())
            except Exception as e:
                print(e) #If too many messages have been sent, an exception can occur #FIXME


    def generateKeyboard(self):
        keyboard = []
        for cam in self.cams:
            if cam.isOnline():
                status = "On" if not cam.sendNotification() else "Off"
                keyboard.append([f"{cam.getName()} Foto", f"{cam.getName()} {status}"])

        return keyboard


    def getOnlineStatus(self):
        msg = ""
        for cam in self.cams:
            status = "ONLINE" if cam.isOnline() else "OFFLINE"
            notification = "YES" if cam.sendNotification() else "NO"
            msg += f"Camera <code>{cam.name}</code> is <code>{status}</code> notification <code>{notification}</code>\n"

        return msg



if __name__ == "__main__":
    main()