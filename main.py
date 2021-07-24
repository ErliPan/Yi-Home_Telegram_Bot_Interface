from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config




bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")


r = cam.getImage()
if r == False:
    print("Camera offline")
else:
    #bot.sendPhoto(r)
    cam.getVideoList(bot.sendVideo)