import io
import os
from datetime import datetime


class SaveVideo:

    def __init__(self, Notifyer, folderPath, sendNotification):
        self.Notifyer = Notifyer
        self.folderPath = folderPath


    def sendPhoto(self, media, caption="", reply_markup = None, notification = True):
        with open(f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.jpg", "wb") as out:
            out.write(media.read())

        if notification:
            media.seek(0) #Rewind
            self.Notifyer.sendPhoto(media, caption, reply_markup)


    def sendVideo(self, media, caption="", reply_markup = None, notification = True):
        with open(f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.mp4", "wb") as out:
            out.write(media.read())

        if notification:
            media.seek(0) #Rewind
            self.Notifyer.sendVideo(media, caption, reply_markup)


    def sendMessage(self, title, message="", reply_markup = None, notification = True):
        if notification:
            self.Notifyer.sendMessage(title, message, reply_markup)