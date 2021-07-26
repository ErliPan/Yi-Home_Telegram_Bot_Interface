from TelegramNotifier import Telegram
from YiHomeCamera import YiCam
from IPCam import IPCam
from telegram import *
from telegram.ext import *
import config
import time



telegram = Telegram(config)


"""
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
"""


cam = IPCam(telegram, YiCam(config, "10.10.10.52"), "yi-b312")
cam = IPCam(telegram, YiCam(config, "10.10.10.54"), "yi-23ba")
cam = IPCam(telegram, YiCam(config, "10.10.10.56"), "yi-d685")
cam = IPCam(telegram, YiCam(config, "10.10.10.57"), "yi-d2ea")
cam = IPCam(telegram, YiCam(config, "10.10.10.60"), "yi-e08f")


while True:
    time.sleep(2)
