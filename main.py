from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config
import time



bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")


while True:
    


r = cam.getImage()
if r == False:
    print("Camera offline")
else:
    bot.sendPhoto(r)
    cam.callbackVideoList(bot.sendVideo)