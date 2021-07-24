from TelegramNotifier import Telegram
from YiHomeCamera import IPCam
import config




bot = Telegram(config)
cam = IPCam(config, "10.10.10.54")

#bot.sendMessage("Titolo", "messaggio")
r = cam.getImage()
print(r)