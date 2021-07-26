import threading

class IPCam:

    debug = True

    def __init__(self, Notifier, Camera, name):
        self.recording = False
        self.counter = 0
        self.name = name
        self.Notifier = Notifier
        self.Camera = Camera

        self.updateTimer = threading.Timer(3.0, self.update)
        self.sendVideoTimer  = threading.Timer(5.0, self.update)


    
    def sendImage(self, msg):

        res = self.Camera.getImage()

        if res:
            self.Notifier.sendPhoto(r)
        else:
            self.Notifier.sendMessage("Camera offline")
        
        return res


    def __movementTriggered(self):
        __printLog("Movement triggered")
        self.Notifier.sendMessage("Movimento")
        self.sendImage("Camera offine")


    def update(self):
        __printLog("Update")
        if self.Camera.isRecording():
            __printLog("Camera is recording size {self.Camera.getTmpVideoSize()}")
            if recording == False:
                __printLog("Trigger video recording")
                __movementTriggered()
                recording = True
        else:
            __printLog("Recording ended")
            recording = False
    
    
    def sendVideo(self):
        __printLog("Check old video")
        self.Camera.callbackVideoList(self.Notifier.sendVideo)


    def __printLog(self, msg):
        if debug:
            print(f"{self.name} {self.counter} msg")


