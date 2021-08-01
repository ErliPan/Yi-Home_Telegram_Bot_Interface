import io
import os
from datetime import datetime


class SaveVideo:

    def __init__(self, Notifyer, folderPath, sendNotification):
        self.Notifyer = Notifyer
        self.folderPath = folderPath
        self.notification = True
    

    def setNotification(sendNotification):
        self.notification = sendNotification
    

    def isNotificationEnabled():
        return self.notification


    def sendPhoto(self, media, caption="", reply_markup = None):
        with open(f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.jpg", "wb") as out:
            out.write(media.read())

        if self.notification:
            media.seek(0) #Rewind
            self.Notifyer.sendPhoto(media, caption, reply_markup)


    def sendVideo(self, media, caption="", reply_markup = None):
        with open(f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.mp4", "wb") as out:
            out.write(media.read())

        if self.notification:
            media.seek(0) #Rewind
            self.Notifyer.sendVideo(media, caption, reply_markup)


    def sendMessage(self, title, message="", reply_markup = None):
        if self.notification:
            self.Notifyer.sendMessage(title, message, reply_markup)