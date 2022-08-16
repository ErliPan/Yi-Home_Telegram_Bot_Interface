import config.config as CONFIG


class DummyCam:

    videoPath = "/tmp/sd/record"
    tmpFile = "tmp.mp4.tmp"

    def __init__(self, IPCam):
        self.IPCam = IPCam
        self.connected = False
        self.connectFTP()
        if self.connected:
            self.updateCamera()

    def connectFTP(self):
        self.connected = True
        self.updateCamera()

        return self.connected

    def isConnected(self):
        return self.connected

    def disconnect(self):
        self.ftp = False
        self.connected = False

    def textToSpeech(self, text):
        print(
            f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/speak.sh?lang={CONFIG.SPEAK_LANG}")

    def sendSound(self, filename):
        print(f"play {filename} ", end="")
        print(f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/speaker.sh")

    def updateCamera(self):
        status = "yes" if self.IPCam.getConfig('enabled') else "no"
        humanDetectionStr = "yes" if self.IPCam.getConfig(
            'humanDetection') else "no"
        url = f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/camera_settings.sh?save_video_on_motion=yes&sensitivity={self.IPCam.getConfig('sensitivity')}&ai_human_detection={humanDetectionStr}&sound_detection=no&sound_sensitivity=80&led={status}&ir=yes&rotate=no&switch_on={status}"
        print(url)

        return True

    def getImage(self, highQuality=False, timeStamp=False):
        print("Get Image")
        return False

    def isRecording(self):
        return False

    def getTmpVideoSize(self):
        print("return tmpVideoSize")
        return -1

    def removeTmpVideo(self):
        print("remove old video")

    def callbackVideoList(self, name=None, videoFunc=None, notification=True):
        print(".", end="")
