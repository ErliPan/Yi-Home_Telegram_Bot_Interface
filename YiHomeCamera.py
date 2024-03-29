import requests
import urllib.request
import io
import os
from ftplib import FTP, error_perm
import time
import config.config as CONFIG

class YiCam:

    videoPath = "/tmp/sd/record"
    tmpFile = "tmp.mp4.tmp"

    def __init__(self, IPCam):
        self.IPCam = IPCam
        self.connected = False
        self.connectFTP()
        if self.connected:
            self.updateCamera()


    def connectFTP(self):
        try:
            self.ftp = FTP(self.IPCam.getConfig('ip'), timeout=15)
            self.ftp.login(user="root", passwd = "")

            if self.connected == False:
                self.connected = True
                self.updateCamera()
            
        except Exception as e:
            print(e)
            self.connected = False

        return self.connected


    def isConnected(self):
        return self.connected


    def disconnect(self):
        self.ftp = False
        self.connected = False


    def textToSpeech(self, text):
        requests.post(f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/speak.sh?lang={CONFIG.SPEAK_LANG}", text.encode('utf-8'))
    

    def sendSound(self, filename):
        print(f"play {filename}")
        requests.post(f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/speaker.sh", io.open(filename, "rb"))

    def updateCamera(self):
        status = "yes" if self.IPCam.getConfig('enabled') else "no"
        humanDetectionStr = "yes" if self.IPCam.getConfig('humanDetection') else "no"
        url = f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/camera_settings.sh?save_video_on_motion=yes&sensitivity={self.IPCam.getConfig('sensitivity')}&ai_human_detection={humanDetectionStr}&sound_detection=no&sound_sensitivity=80&led={status}&ir=yes&rotate=no&switch_on={status}"
        print(url)

        try:
            #Camera firmware bug, sometimes the settings are applied only on the second request
            x = requests.get(url, timeout=CONFIG.SETTINGS_TIMEOUT)
            if self.IPCam.getConfig("enabled"):
                y = requests.get(url, timeout=CONFIG.SETTINGS_TIMEOUT)
                return x.status_code == 200 and y.status_code == 200
            else:
                return x.status_code == 200
        except:
            return False


    def getImage(self, highQuality = False, timeStamp = False):
        highQuality = "high" if highQuality else "low"
        timeStamp = "yes" if timeStamp else "no"

        url = f"http://{self.IPCam.getConfig('ip')}:8080/cgi-bin/snapshot.sh?res={highQuality}&watermark={timeStamp}"
        response = requests.get(url, timeout=CONFIG.SNAPSHOT_TIMEOUT)
        return io.BytesIO(response.content) if (response.headers.get("content-type") == "image/jpeg") else False


    def isRecording(self):
        if self.isConnected() == False:
            return False

        try:
            self.ftp.cwd(self.videoPath)
        except Exception as e:
            print(e)
            return False
        return self.tmpFile in self.ftp.nlst()

    
    def getTmpVideoSize(self):
        if self.isRecording():
            return self.ftp.size(f"{self.videoPath}/{self.tmpFile}")
        else:
            return -1


    def removeTmpVideo(self):
        if self.isRecording():
            self.ftp.delete(f"{self.videoPath}/{self.tmpFile}")


    def callbackVideoList(self, name = None, videoFunc = None, notification = True):
        i = 0
        self.ftp.cwd(self.videoPath)
        for folder in self.ftp.nlst():
            if folder != self.tmpFile:
                dirPath = f"{self.videoPath}/{folder}"
                self.ftp.cwd(dirPath)
                for videoFile in self.ftp.nlst():
                    filePath = f"/{self.videoPath}/{folder}/{videoFile}"
                    urlPath = f"ftp://root:@{self.IPCam.getConfig('ip')}{filePath}"
                    print(urlPath)
                    videoObj = io.BytesIO(urllib.request.urlopen(urlPath).read())
                    if videoFunc:
                        videoFunc(videoObj, name, notification=notification, disable_notification=True)
                    
                    self.ftp.delete(filePath)

                    if i > 2 and videoFunc:
                        return
                    else:
                        i += 1
                try:
                    self.ftp.rmd(dirPath)
                except error_perm as e:
                    print(e) #New video have been saved in the meanwhile
