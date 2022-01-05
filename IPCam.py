import threading
import time
import config.config as CONFIG

class IPCam:

    def __init__(self, Notifyer, Camera, CameraSettings, name):

        self.CameraSettings = CameraSettings
        self.log = True
        self.recording = False
        self.startTime = time.time()
        self.name = name
        self.Notifyer = Notifyer
        self.Camera = Camera(self)
        self.recordingSize = -1
        self.counter = 1
        
        self.__printLog("Created")


    def start(self):
        self.startTime = time.time()
        self.__printLog("Starting...")
        self.update()


    def enableCam(self, enabled):
        self.__printLog(f"Set camera to {enabled}")
        self.CameraSettings.setConfig(self.name, "enabled", enabled)
        if self.Camera.updateCamera():
            return True
        else:
            self.CameraSettings.setConfig(self.name, "enabled", not enabled)
            return False
    
    def setConfig(self, param, value):
        self.CameraSettings.setConfig(self.name, param, value)
    
    def getConfig(self, param):
        return self.CameraSettings.getConfig(self.name, param)


    def sendNotification(self):
        return self.getConfig("notification")
    

    def setNotification(self, sendNotificaton):
        self.setConfig("notification", sendNotificaton)


    def isEnabled(self):
        return self.getConfig("enabled")


    def isOnline(self):
        return self.Camera.isConnected()


    def getName(self):
        return self.name


    def textToSpeech(self, text):
        if self.Camera.isConnected():
            self.Camera.textToSpeech(text)


    def sendSound(self, filename):
        if self.Camera.isConnected():
            self.Camera.sendSound(filename)


    def update(self):
        try:
            self.updateCycle()
        except Exception as e:
            print(f"Update error exception: {e}")
        
        #Call itself after x sec
        thread = threading.Timer(0.5, self.update)
        thread.daemon = True
        thread.start()


    def updateCycle(self):
        if self.Camera.isConnected():
            try:
                if self.counter % 1 == 0:
                    self.movementCheck()
                if self.counter % 3 == 0:
                    self.sendVideo()
                if self.counter % 7 == 0:
                    self.unstuckTmpVideo()
                if self.counter % 21 == 0:
                    self.__printLog("RUNNING")
            except Exception as e:
                print(f"Camera disconnected exception: {e}")
                self.Camera.disconnect()
        
        elif self.counter % 4 == 0:
            status = "SUCCESS" if self.Camera.connectFTP() else "FAIL"


        self.counter = (self.counter + 1) % 100


    def movementCheck(self):
        if self.Camera.isRecording():
            self.__printLog(f"Camera is recording size {int(self.Camera.getTmpVideoSize() / 10000) / 100} MB")
            if self.recording == False:
                self.__printLog("Trigger video recording")
                self.__movementTriggered()
                self.recording = True
        else:
            if self.recording:
                self.__printLog("Recording ended")
            self.recording = False
    
    
    def unstuckTmpVideo(self):
        if self.Camera.isRecording():
            size = self.Camera.getTmpVideoSize()
            if self.recordingSize != -1:
                if self.recordingSize == size:
                    self.__printLog(f" #### UNSTUCK STUCK VIDEO size = {int(size / 10000) / 100} MB")
                    self.Camera.removeTmpVideo()
            self.recordingSize = size
            self.__printLog(f"Check size is {self.recordingSize}")


    def sendVideo(self):
        if self.isOnline():
            if self.isEnabled():
                self.Camera.callbackVideoList(self.name, self.Notifyer.sendVideo, notification = self.getConfig("notification"))
            else:
                self.Camera.callbackVideoList()
        else:
            print("Calling sendVideo when offline")


    def sendImage(self, caption="", force = False):
        if self.isEnabled():
            try:
                res = self.Camera.getImage(highQuality = not CONFIG.VIDEO_COMPRESSION)
            except Exception as e:
                self.__printLog(f"SEND IMAGE ISSUE EX: {e}")
                res = False
            if res:
                notification = True if force else self.getConfig("notification")
                self.__printLog("Send photo")
                self.Notifyer.sendPhoto(res, f"{self.name} {caption}", notification = notification)
                return True

            self.__sendMessage(CONFIG.CAMERA_OFFLINE)
        else:
            self.__sendMessage(CONFIG.CAMERA_DISABLED)
        return False


    def __movementTriggered(self):
        self.sendImage(CONFIG.MOTION_DETECTED)


    def __printLog(self, msg):
        if self.log:
            timePassed = int(time.time() - self.startTime)
            print(f"{self.name} {timePassed} {msg}")


    def __sendMessage(self, msg):
        if self.log:
            self.__printLog(f"Telegram-> {msg}")
        try:
            self.Notifyer.sendMessage(f"{self.name}", f"{msg}")
        except Exception as e:
            print(f"FAILED TO SEND: {msg} exception: {e}")
            time.sleep(5)
        time.sleep(0.7)
