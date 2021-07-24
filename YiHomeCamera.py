import requests
import urllib.request
import io
import os
from ftplib import FTP
import time

class IPCam:

    videoPath = "/tmp/sd/record"

    def __init__(self, config, ip):
        self.ip = ip
        self.config = config
        self.ftp = FTP(ip)
        self.ftp.login(user="root", passwd = "")
    

    def getImage(self, highQuality = False, timeStamp = False):
        highQuality = "high" if highQuality else "low"
        timeStamp = "yes" if timeStamp else "no"

        url = f"http://{self.ip}:8080/cgi-bin/snapshot.sh?res={highQuality}&watermark={timeStamp}"

        response = requests.get(url, timeout=self.config.SNAPSHOT_TIMEOUT)

        return io.BytesIO(response.content) if (response.headers.get("content-type") == "image/jpeg") else False


    def isRecording(self):
        self.ftp.cwd(self.videoPath)
        return "tmp.mp4.tmp" in ftp.nlst()


    def getVideoList(self, videoFunc):
        i = 0
        self.ftp.cwd(self.videoPath)
        for folder in self.ftp.nlst():
            self.ftp.cwd(f"{self.videoPath}/{folder}")
            for videoFile in self.ftp.nlst():
                if i == 0:
                    filepath = f"ftp://root:@{self.ip}//{self.videoPath}/{folder}/{videoFile}"
                    print(filepath)
                    videoObj = io.BytesIO(urllib.request.urlopen(filepath).read())
                    videoFunc(videoObj)
                    i = 2

    #def getAllVideo(self):




