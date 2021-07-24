import config
import telepot

class TelegramNotifier:

    def __init__(self, config):
        self.config = config
        self.bot = telepot.Bot(config.TOKEN)
    
    def sendMessage(self, title, message=""):
        text = "<b>{title}</b><br />{message}"

        self.bot.sendMessage(config.CHATID, text, parse_mode="HTML")
