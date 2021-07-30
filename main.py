from TelegramNotifyer import Telegram
from DummyNotifyer import Dummy

from YiHomeCamera import YiCam
from IPCam import IPCam

from TelegramChat import TelegramChat

import config as CONFIG

import telegram
import time

def main():
    #polymorphism (?)
    notifyer = Telegram(CONFIG)
    camera = YiCam

    cams = []

    for CAMERA in CONFIG.CAMERAS:
        cams.append(IPCam(notifyer, camera(CONFIG, CAMERA[0]), CAMERA[1]))
    
    #Make them start at the same time (more or less)
    for cam in cams:
        cam.start()
        TelegramChat(CONFIG.TOKEN, cam)

    cameraStatus = ""

    while True:
        stat = getOnlineStatus(cams)
        if stat != cameraStatus:
            cameraStatus = stat

            keyboard = []
            for cam in cams:
                if cam.isOnline():
                    keyboard.append([f"{cam.getName()} Foto"])
            keyboard = telegram.ReplyKeyboardMarkup(keyboard)

            try:
                notifyer.sendMessage("Camera Status", cameraStatus, reply_markup = keyboard)
            except Exception as e:
                print(e) # If too many messages have been sent, an exception can occur #FIXME
        
        time.sleep(10)


def getOnlineStatus(cams):
    msg = ""
    for cam in cams:
        status = "ONLINE" if cam.isOnline() else "OFFLINE"
        msg += f"Camera <code>{cam.name}</code> is <code>{status}</code>\n"

    return msg



if __name__ == "__main__":
    main()