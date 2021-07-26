from TelegramNotifier import Telegram
from telegram import *
from telegram.ext import *
from YiHomeCamera import YiCam
import config
import time



bot = Telegram(config)
cam = YiCam(config, "10.10.10.54")




def getImmagine(update: Update, context: CallbackContext):
    r = cam.getImage()

    if r == True:
        bot.sendMessage("Camera offline")
    else:
        bot.sendPhoto(r)

botUpdater = Updater(config.TOKEN)
dispatcher = botUpdater.dispatcher
dispatcher.add_handler(CommandHandler("immagine", getImmagine))
botUpdater.start_polling()

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
            print(f"{counter} wait tmpsize: {cam.getTmpVideoSize()}")
    else:
        if rec:
            cam.callbackVideoList(bot.sendVideo)
        else:
            time.sleep(2)
            print(f"{counter} sleep")
        rec = False
