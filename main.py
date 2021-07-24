from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config




bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")


r = cam.getImage()
bot.sendPhoto(r)