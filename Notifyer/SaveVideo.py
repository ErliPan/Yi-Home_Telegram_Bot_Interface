import io
import os
from datetime import datetime


class SaveVideo:

    def __init__(self, Notifyer, folderPath, compressVideo = False):
        self.Notifyer = Notifyer
        self.folderPath = folderPath
        self.compressVideo = compressVideo

    def sendPhoto(self, media, caption="", reply_markup=None, notification=True, disable_notification=False):
        fileName = f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.jpg"
        with open(fileName, "wb") as out:
            out.write(media.read())

        if notification:
            fileSize = (int(os.path.getsize(fileName) / 1000))
            media.seek(0) #Rewind
            self.Notifyer.sendPhoto(media, f"{caption} {fileSize} KB", reply_markup, disable_notification=disable_notification)

    def sendVideo(self, media, caption="", reply_markup=None, notification=True, disable_notification=False):
        fileName = f"{self.folderPath}{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.mp4"
        with open(fileName, "wb") as out:
            out.write(media.read())

        if notification:
            
            if self.compressVideo:
                fileName, media = self.__videoCompress(fileName)
            else:
                media.seek(0)  # Rewind
            
            fileSize = (int(os.path.getsize(fileName) / 1000))

            self.Notifyer.sendVideo(media, f"{caption} {fileSize} KB", reply_markup, disable_notification=disable_notification)

    def sendMessage(self, title, message="", reply_markup=None, disable_notification=False):
        self.Notifyer.sendMessage(title, message, reply_markup, disable_notification=disable_notification)
    

    def __videoCompress(self, videoFile):
        tmpFile =  videoFile.replace(".mp4", "_compressed.mp4")
        os.system(f"ffmpeg -i file:\"{videoFile}\" -vcodec libx264 -preset veryfast -crf 30 -vf scale=960:-1 -r 5 file:\"{tmpFile}\"")
        return tmpFile, io.open(tmpFile, "rb")
