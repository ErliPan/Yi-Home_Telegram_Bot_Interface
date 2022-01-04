import telegram
import random
import config.config as CONFIG


class Telegram:

    def __init__(self):
        self.bots = []

        for alt in CONFIG.TOKEN_ALL:
            self.bots.append(telegram.Bot(alt))

    def sendPhoto(self, media, caption="", reply_markup=None, disable_notification=False):
        if reply_markup != None:
            reply_markup = telegram.ReplyKeyboardMarkup(reply_markup, disable_notification=disable_notification)

        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendPhoto(CONFIG.CHATID, media, caption=caption,parse_mode="HTML", reply_markup=reply_markup)
                error = False
                break
            except telegram.error.TimedOut as e:
                print(f"Timed out Send failed pass to alt {e}")
                error = False
                #Typically timed out is sent
                break
            except Exception as e:
                print(f"Send failed pass to alt {e}")
        return error


    def sendVideo(self, media, caption="", reply_markup=None, disable_notification=False):
        if reply_markup != None:
            reply_markup = telegram.ReplyKeyboardMarkup(reply_markup, disable_notification=disable_notification)

        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendVideo(CONFIG.CHATID, media, caption=caption, parse_mode="HTML", reply_markup=reply_markup)
                error = False
                break
            except telegram.error.TimedOut as e:
                print(f"Timed out Send failed pass to alt {e}")
                error = False
                #Typically timed out is sent
                break
            except Exception as e:
                print(f"Send failed pass to alt {e}")
        return error


    def sendMessage(self, title, message="", reply_markup=None, disable_notification=False):
        if reply_markup != None:
            reply_markup = telegram.ReplyKeyboardMarkup(reply_markup)

        text = f"<strong>{title}</strong>\n{message}"

        random.shuffle(self.bots)
        error = True
        for bot in self.bots:
            try:
                bot.sendMessage(CONFIG.CHATID, text, parse_mode="HTML", reply_markup=reply_markup, disable_notification=disable_notification)
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
