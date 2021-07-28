class Dummy:

    def __init__(self, config):
        self.config = config


    def sendPhoto(self, media, caption="", reply_markup = None):
        print(f"SendPhoto {caption}")


    def sendVideo(self, media, caption="", reply_markup = None):
        print(f"SendVideo {caption}")


    def sendMessage(self, title, message="", reply_markup = None):
        text = f"<strong>{title}</strong>\n{message}"
        print(f"SendText {text}")
