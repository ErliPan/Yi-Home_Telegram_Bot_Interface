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

        self.__printLog("Create updateTimer")
        self.updateTimer = threading.Timer(3.0, self.update).start()
        self.__printLog("Create sendVideoTimer")
        self.sendVideoTimer  = threading.Timer(5.0, self.sendVideo).start()
        self.__printLog("Create unstuckTimer")
        self.unstuckTimer  = threading.Timer(10.0, self.unstuckTmpVideo).start()


    def sendImage(self, msg):
        res = self.Camera.getImage()
        if res:
            self.__printLog("Send photo")
            self.Notifier.sendPhoto(res)
        else:
            self.__printLog("Send photo failed camera offine")
            self.__sendMessage("Camera offline")
        return res


    def unstuckTmpVideo(self):
        self.unstuckTimer  = threading.Timer(10.0, self.unstuckTmpVideo).start()
        if self.Camera.isRecording():
            size = self.Camera.getTmpVideoSize()
            if self.recordingSize != -1:
                if self.recordingSize == size:
                    self.__printLog(f" #### UNSTUCK STUCK VIDEO size = {int(size) / 1000} kB")
            self.size = size


    def update(self):
        self.updateTimer = threading.Timer(3.0, self.update).start()
        self.__printLog("Update")
        if self.Camera.isRecording():
            self.__printLog(f"Camera is self.recording size {int(self.Camera.getTmpVideoSize()) / 1000} kB")
            if self.recording == False:
                self.__printLog("Trigger video self.recording")
                self.__movementTriggered()
                self.recording = True
        else:
            if self.recording:
                self.__printLog("self.recording ended")
            self.recording = False
    
    
    def sendVideo(self):
        self.sendVideoTimer = threading.Timer(5.0, self.sendVideo).start()
        self.__printLog("Check old video")
        self.Camera.callbackVideoList(self.Notifier.sendVideo)


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
