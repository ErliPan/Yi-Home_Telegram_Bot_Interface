import threading
import time
import config.config as CONFIG

class IPCam:

    def __init__(self, Notifyer, Camera, name, enabled = True, notification = True):

        self.log = True
        self.recording = False
        self.startTime = time.time()
        self.name = name
        self.Notifyer = Notifyer
        self.Camera = Camera
        self.recordingSize = -1
        self.counter = 1
        self.enabled = enabled
        self.notification = notification
        
        self.__printLog("Created")


    def start(self):
        self.startTime = time.time()
        self.__printLog("Starting...")
        self.update()


    def enableCam(self, enabled):
        self.__printLog(f"Set camera to {enabled}")
        if self.Camera.switchCamera(enabled):
            self.enabled = enabled
            return True
        return False


    def sendNotification(self):
        return self.notification
    

    def setNotification(self, sendNotificaton):
        self.notification = sendNotificaton


    def isEnabled(self):
        return self.enabled


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
                self.__printLog(f"Camera disconnected exception: {e}")
                self.Camera.disconnect()
        
        elif self.counter % 5 == 0:
            status = "SUCCESS" if self.Camera.connectFTP() else "FAIL"
            self.__printLog(f"Reconnecting result: {status}")


        self.counter = (self.counter + 1) % 100
        #Call itself after 1 sec
        threading.Timer(1.0, self.update).start()


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
                self.Camera.callbackVideoList(self.name, self.Notifyer.sendVideo, notification = self.notification)
            else:
                self.Camera.callbackVideoList()
        else:
            self.__printLog("Calling sendVideo when offline")


    def sendImage(self, caption="", force = False):
        if self.isEnabled():
            try:
                res = self.Camera.getImage(highQuality = not CONFIG.VIDEO_COMPRESSION)
            except Exception as e:
                self.__printLog(f"SEND IMAGE ISSUE EX: {e}")
                res = False
            if res:
                notification = True if force else self.notification
                self.__printLog("Send photo")
                self.Notifyer.sendPhoto(res, f"{self.name} {caption}", notification = notification)
                return True

            self.__sendMessage(CONFIG.CAMERA_OFFLINE)
        else:
            self.__sendMessage(CONFIG.CAMERA_DISABLED)
        return False


    def __movementTriggered(self):
        #self.__sendMessage(CONFIG.MOTION_DETECTED)
        #self.sendImage()

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
            self.__printLog(f"FAILED TO SEND: {msg} exception: {e}")
            time.sleep(5)
        time.sleep(0.7)
