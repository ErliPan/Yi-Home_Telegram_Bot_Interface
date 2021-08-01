import requests
import urllib.request
import io
import os
from ftplib import FTP, error_perm
import time
from config.config import *

class YiCam:

    videoPath = "/tmp/sd/record"
    tmpFile = "tmp.mp4.tmp"

    def __init__(self, ip, switchOn = True, sensitivity = "low"):
        self.ip = ip
        self.sensitivity = sensitivity
        self.connectFTP()
        #self.switchCamera(switchOn)


    def connectFTP(self):
        try:
            self.ftp = FTP(self.ip, timeout=15)
            self.ftp.login(user="root", passwd = "")
            self.connected = True
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
        requests.post(f"http://{self.ip}:8080/cgi-bin/speak.sh?lang={SPEAK_LANG}", text.encode('utf-8'))
    

    def sendSound(self, filename):
        requests.post(f"http://{self.ip}:8080/cgi-bin/speaker.sh", io.open(filename, "rb"))


    def switchCamera(self, switchOn):
        status = "yes" if switchOn else "no"
        url = f"http://{self.ip}:8080/cgi-bin/camera_settings.sh?save_video_on_motion=yes&sensitivity={self.sensitivity}&ai_human_detection=no&sound_detection=no&sound_sensitivity=80&led={status}&ir=yes&rotate=no&switch_on={status}"
        print(url)

        try:
            #Camera firmware bug, sometimes the settings are applied only on the second request
            x = requests.get(url, timeout=SETTINGS_TIMEOUT)
            if switchOn:
                y = requests.get(url, timeout=SETTINGS_TIMEOUT)
                return x.status_code == 200 and y.status_code == 200
            else:
                return x.status_code == 200
        except:
            return False


    def getImage(self, highQuality = False, timeStamp = False):
        highQuality = "high" if highQuality else "low"
        timeStamp = "yes" if timeStamp else "no"

        url = f"http://{self.ip}:8080/cgi-bin/snapshot.sh?res={highQuality}&watermark={timeStamp}"
        response = requests.get(url, timeout=SNAPSHOT_TIMEOUT)
        return io.BytesIO(response.content) if (response.headers.get("content-type") == "image/jpeg") else False


    def isRecording(self):
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
        videoCount = 0
        self.ftp.cwd(self.videoPath)
        for folder in self.ftp.nlst():
            if folder != self.tmpFile:
                dirPath = f"{self.videoPath}/{folder}"
                self.ftp.cwd(dirPath)
                for videoFile in self.ftp.nlst():
                    filePath = f"/{self.videoPath}/{folder}/{videoFile}"
                    urlPath = f"ftp://root:@{self.ip}{filePath}"
                    print(urlPath)
                    videoObj = io.BytesIO(urllib.request.urlopen(urlPath).read())
                    if videoFunc:
                        videoFunc(videoObj, name, notification=notification)
                    self.ftp.delete(filePath)
                try:
                    self.ftp.rmd(dirPath)
                except error_perm as e:
                    print(e) #New video have been saved in the meanwhile