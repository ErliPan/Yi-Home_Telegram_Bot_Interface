import threading
import time

class IPCam:

    debug = True

    def __init__(self, Notifier, Camera, name):

        self.recording = False
        self.startTime = time.time()
        self.name = name
        self.Notifier = Notifier
        self.Camera = Camera

        self.__printLog("Create updateTimer")
        self.updateTimer = threading.Timer(3.0, self.update).start()
        self.__printLog("Create sendVideoTimer")
        self.sendVideoTimer  = threading.Timer(5.0, self.update).start()


    def sendImage(self, msg):

        res = self.Camera.getImage()
        if res:
            self.__printLog("Send photo")
            self.Notifier.sendPhoto(r)
        else:
            self.__printLog("Send photo failed camera offine")
            self.Notifier.sendMessage("Camera offline")
        return res


    def __movementTriggered(self):
        self.__printLog("Movement triggered")
        self.Notifier.sendMessage("Movimento")
        self.sendImage("Camera offine")


    def update(self):
        self.updateTimer = threading.Timer(3.0, self.update).start()
        self.__printLog("Update")
        if self.Camera.isRecording():
            self.__printLog("Camera is self.recording size {self.Camera.getTmpVideoSize()}")
            if self.recording == False:
                self.__printLog("Trigger video self.recording")
                __movementTriggered()
                self.recording = True
        else:
            if self.recording:
                self.__printLog("self.recording ended")
            self.recording = False
    
    
    def sendVideo(self):
        self.sendVideoTimer  = threading.Timer(5.0, self.update).start()
        self.__printLog("Check old video")
        self.Camera.callbackVideoList(self.Notifier.sendVideo)


    def __printLog(self, msg):
        if self.debug:
            timePassed = int(time.time() - self.startTime)
            print(f"{self.name} {timePassed} {msg}")


