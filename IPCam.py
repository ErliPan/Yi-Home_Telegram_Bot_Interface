import threading

class IPCam:

    debug = True

    def __init__(self, Notifier, Camera, name):

        self.recording = False
        self.counter = 0
        self.name = name
        self.Notifier = Notifier
        self.Camera = Camera

        self.__printLog("Create updateTimer")
        self.updateTimer = threading.Timer(3.0, self.update)
        self.__printLog("Create sendVideoTimer")
        self.sendVideoTimer  = threading.Timer(5.0, self.update)


    
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
        self.__printLog("Update")
        if self.Camera.isRecording():
            self.__printLog("Camera is recording size {self.Camera.getTmpVideoSize()}")
            if recording == False:
                self.__printLog("Trigger video recording")
                __movementTriggered()
                recording = True
        else:
            self.__printLog("Recording ended")
            recording = False
    
    
    def sendVideo(self):
        self.__printLog("Check old video")
        self.Camera.callbackVideoList(self.Notifier.sendVideo)


    def __printLog(self, msg):
        if self.debug:
            print(f"{self.name} {self.counter} {msg}")


