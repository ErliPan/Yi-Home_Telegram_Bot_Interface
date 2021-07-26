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
        self.recordingSize = -1
        self.counter = 0

        self.__printLog("Create Timer")
        self.updateTimer = threading.Timer(2.0, self.update).start()


    def update(self):
        
        if self.counter % 1 == 0:
            self.movementCheck()
        if self.counter % 2 == 0:
            self.sendVideo()
        if self.counter % 10 == 0:
            self.unstuckTmpVideo()
        
        self.counter = (self.counter + 1) % 100

        self.updateTimer = threading.Timer(2.0, self.update).start()


    def movementCheck(self):
        self.__printLog("Update")
        if self.Camera.isRecording():
            self.__printLog(f"Camera is recording size {int(self.Camera.getTmpVideoSize()) / 1000} kB")
            if self.recording == False:
                self.__printLog("Trigger video recording")
                self.__movementTriggered()
                self.recording = True
        else:
            if self.recording:
                self.__printLog("recording ended")
            self.recording = False
    
    
    def unstuckTmpVideo(self):
        if self.Camera.isRecording():
            size = self.Camera.getTmpVideoSize()
            if self.recordingSize != -1:
                if self.recordingSize == size:
                    self.__printLog(f" #### UNSTUCK STUCK VIDEO size = {int(size) / 1000} kB")
            self.size = size


    def sendVideo(self):
        self.__printLog("Check old video")
        self.Camera.callbackVideoList(self.Notifier.sendVideo, self.name)


    def sendImage(self, msg):
        res = self.Camera.getImage()
        if res:
            self.__printLog("Send photo")
            self.Notifier.sendPhoto(res, self.name)
        else:
            self.__printLog("Send photo failed camera offine")
            self.__sendMessage("Camera offline")
        return res


    def __movementTriggered(self):
        self.__printLog("Movement triggered")
        self.__sendMessage("Movimento")
        self.sendImage("Camera offine")


    def __printLog(self, msg):
        if self.debug:
            timePassed = int(time.time() - self.startTime)
            print(f"{self.name} {timePassed} {msg}")


    def __sendMessage(self, msg):
        self.Notifier.sendMessage(f"{self.name}", f"{msg}")
