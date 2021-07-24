import requests
import io

class IPCam:

    def __init__(self, config, ip):
        self.ip = ip
        self.config = config
    

    def getImage(self, highQuality = False, timeStamp = False):
        highQuality = "high" if highQuality else "low"
        timeStamp = "yes" if timeStamp else "no"

        url = f"http://{self.ip}:8080/cgi-bin/snapshot.sh?res={highQuality}&watermark={timeStamp}"

        response = requests.get(url, timeout=self.config.SNAPSHOT_TIMEOUT)

        return io.BytesIO(response.content) if (response.headers.get("content-type") == "image/jpeg") else False






