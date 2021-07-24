from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config
import time



bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")




print("start loop")
rec = False
counter = 0
while True:

    if (counter % 7 == 0):
        print("Check old video")
        cam.callbackVideoList(bot.sendVideo)

    counter = (counter + 1) % 1000

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
            print(f"{counter} wait")
    else:
        if rec:
            cam.callbackVideoList(bot.sendVideo)
        else:
            time.sleep(2)
            print(f"{counter} sleep")
        rec = False
        





    