from telegram import *
from telegram.ext import *
import telegram

class Telegram:

    def __init__(self, config):
        self.config = config
        self.bot = telegram.Bot(config.TOKEN)


    def sendPhoto(self, media, caption="", reply_markup = None):
        self.bot.sendPhoto(self.config.CHATID, media, caption=caption, parse_mode="HTML", reply_markup = reply_markup)


    def sendVideo(self, media, caption="", reply_markup = None):
        self.bot.sendVideo(self.config.CHATID, media, caption=caption, parse_mode="HTML", reply_markup = reply_markup)


    def sendMessage(self, title, message="", reply_markup = None):
        text = f"<strong>{title}</strong>\n{message}"

        self.bot.sendMessage(self.config.CHATID, text, parse_mode="HTML", reply_markup = reply_markup)
