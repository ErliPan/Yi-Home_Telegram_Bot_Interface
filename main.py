from TelegramNotifier import Telegram
from YiHomeCamera import YiCam
from IPCam import IPCam
from telegram import *
from telegram.ext import *
import config
import time



telegram = Telegram(config)
yiCam = YiCam(config, "10.10.10.57")



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



cam = IPCam(telegram, yiCam, "Camera 1")

print("start loop")
while True:

    time.sleep(2)
