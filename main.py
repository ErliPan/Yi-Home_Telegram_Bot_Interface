from TelegramNotifyer import Telegram
from DummyNotifyer import Dummy
from YiHomeCamera import YiCam
from IPCam import IPCam
from telegram import *
from telegram.ext import *
import config as CONFIG
import time


def getImmagine(update: Update, context: CallbackContext):
    r = cam.getImage()

    if r == True:
        bot.sendMessage("Camera offline")
    else:
        bot.sendPhoto(r)

botUpdater = Updater(CONFIG.TOKEN)
dispatcher = botUpdater.dispatcher

#MessageHandler(Filters.regex('pattern'), callback)

dispatcher.add_handler(CommandHandler("immagine", getImmagine))
botUpdater.start_polling()


def __main__():
    #polymorphism (?)
    notifyer = Telegram(CONFIG)
    camera = YiCam

    cams = []

    for CAMERA in CONFIG.CAMERAS:
        cams.append(IPCam(notifyer, camera(CONFIG, CAMERA[0]), CAMERA[1]))
    
    #Make them start at the same time (more or less)
    for cam in cams:
        cam.start()

    cameraStatus = ""

    while True:
        stat = getOnlineStatus(cams)
        if stat != cameraStatus:
            cameraStatus = stat

            keyboard = []
            for cam in cams:
                if cam.isOnline():
                    keyboard.append([f"Foto cam.getName()"])

            try:
                notifyer.sendMessage("Camera Status", cameraStatus, reply_markup = keyboard)
            except Exception as e:
                print(e) # If too many messages have been sent, an exception can occur #TODO
        
        time.sleep(10)


def getOnlineStatus(cams):
    msg = ""
    for cam in cams:
        status = "ONLINE" if cam.isOnline() else "OFFLINE"
        msg += f"Camera <code>{cam.name}</code> is <code>{status}</code>\n"

    return msg


__main__()