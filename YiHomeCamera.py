import requests
import urllib.request
import io
import os
from ftplib import FTP, error_perm
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
        self.ftp.cwd(self.videoPath) #ConnectionResetError: [Errno 104] Connection reset by peer
        return "tmp.mp4.tmp" in self.ftp.nlst()


    def callbackVideoList(self, videoFunc):
        videoCount = 0
        self.ftp.cwd(self.videoPath)
        for folder in self.ftp.nlst():
            if folder != "tmp.mp4.tmp":
                dirPath = f"{self.videoPath}/{folder}"
                self.ftp.cwd(dirPath)
                for videoFile in self.ftp.nlst():
                    filePath = f"/{self.videoPath}/{folder}/{videoFile}"
                    urlPath = f"ftp://root:@{self.ip}/{filePath}"
                    print(urlPath)
                    videoObj = io.BytesIO(urllib.request.urlopen(urlPath).read())
                    videoFunc(videoObj)
                    self.ftp.delete(filePath)
            
                try:
                    self.ftp.rmd(dirPath) #ftplib.error_perm: 550 Can't remove directory: Directory not empty
                except error_perm:
                    pass





