class Dummy:

    def __init__(self, config):
        self.config = config


    def sendPhoto(self, media, caption=""):
        print(f"SendPhoto {caption}")


    def sendVideo(self, media, caption=""):
        print(f"SendVideo {caption}")


    def sendMessage(self, title, message=""):
        text = f"<strong>{title}</strong>\n{message}"
        print(f"SendText {text}")
