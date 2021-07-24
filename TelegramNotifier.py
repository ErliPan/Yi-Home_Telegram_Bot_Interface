import telepot

class Telegram:

    def __init__(self, config):
        self.config = config
        self.bot = telepot.Bot(config.TOKEN)
    
    def sendMessage(self, title, message=""):
        text = f"<strong>{title}</strong>\n{message}"

        self.bot.sendMessage(self.config.CHATID, text, parse_mode="HTML")
