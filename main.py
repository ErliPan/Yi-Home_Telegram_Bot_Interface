from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config
import time



bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")

print("Check old video")
cam.callbackVideoList(bot.sendVideo)


print("start loop")
rec = False

while True:

    if cam.isRecording():
        if rec == False:
            print("Movimento")
            bot.sendMessage("Movimento")
            r = cam.getImage()

            if r == False:
                bot.sendMessage("Camera offline")
            else:
                bot.sendPhoto(r)

            rec = True
        else:
            time.sleep(2)
            print("sleep wait")
    else:
        if rec:
            cam.callbackVideoList(bot.sendVideo)
        else:
            time.sleep(2)
            print("sleep")
        rec = False
        





    