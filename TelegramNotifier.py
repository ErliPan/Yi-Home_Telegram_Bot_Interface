from telegram import *
from telegram.ext import *
import telegram

class Telegram:

    def __init__(self, config):
        self.config = config
        self.bot = telegram.Bot(config.TOKEN)
    
    
    def sendPhoto(self, media, caption=""):

        self.bot.sendVideo(self.config.CHATID, media, caption=caption, parse_mode="HTML")

    
    def sendPhoto(self, media, caption=""):

        self.bot.sendVideo(self.config.CHATID, media, caption=caption, parse_mode="HTML")


    def sendMessage(self, title, message=""):
        text = f"<strong>{title}</strong>\n{message}"

        self.bot.sendMessage(self.config.CHATID, text, parse_mode="HTML")
