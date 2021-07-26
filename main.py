from TelegramNotifier import Telegram
from YiHomeCamera import YiCam
from IPCam import IPCam
from telegram import *
from telegram.ext import *
import config
import time


camerasInfo = [
    ["10.10.10.52", "1-yi-b312"],
    ["10.10.10.54", "2-yi-23ba"],
    ["10.10.10.56", "3-yi-d685"],
    ["10.10.10.57", "4-yi-d2ea"],
    ["10.10.10.60", "5-yi-e08f"],
    ["10.10.10.61", "6-yi-499d"],
]


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

def __main__():
    telegram = Telegram(config)
    cams = []

    for cameraInfo in camerasInfo:
        cams.append(IPCam(telegram, YiCam(config, cameraInfo[0]), cameraInfo[1]))

    telegram.sendMessage("Camera Status", getOnlineStatus(cams))


def getOnlineStatus(cams):
    msg = ""
    for cam in cams:
        status = "ONLINE" if cam.isOnline() else "OFFLINE"
        msg += f"Camera <code>{cam.name}</code> is <code>{status}</code>\n"
    
    return msg


__main__()