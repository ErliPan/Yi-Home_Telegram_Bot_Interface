from telegram import *
from telegram.ext import *
import telegram
import random


class Telegram:

    def __init__(self, config):
        self.config = config
        self.bots = []

        for alt in config.TOKEN_ALL:
            self.bots.append(telegram.Bot(alt))


    def sendPhoto(self, media, caption="", reply_markup = None):
        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendPhoto(self.config.CHATID, media, caption=caption, parse_mode="HTML", reply_markup = reply_markup)
                error = False
                break
            except telegram.error.TimedOut as e:
                print(f"Timed out Send failed pass to alt {e}")
                error = False
                #Typically timed out is sent
                break
            except Exception as e:
                print(f"Send failed pass to alt {e}")


    def sendVideo(self, media, caption="", reply_markup = None):
        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendVideo(self.config.CHATID, media, caption=caption, parse_mode="HTML", reply_markup = reply_markup)
                error = False
                break
            except telegram.error.TimedOut as e:
                print(f"Timed out Send failed pass to alt {e}")
                error = False
                #Typically timed out is sent
                break
            except Exception as e:
                print(f"Send failed pass to alt {e}")
        


    def sendMessage(self, title, message="", reply_markup = None):
        text = f"<strong>{title}</strong>\n{message}"

        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendMessage(self.config.CHATID, text, parse_mode="HTML", reply_markup = reply_markup)
                error = False
                break
            except telegram.error.TimedOut as e:
                print(f"Timed out Send failed pass to alt {e} {title}")
                error = False
                #Typically timed out is sent
                break
            except Exception as e:
                print(f"Send failed pass to alt {e} {title}")
        
        if error:
            raise Exception("Runned out of alt bot")
