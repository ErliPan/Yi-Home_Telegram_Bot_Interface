class TelegramChat:

    def __init__(self, telegram, camera):
        self.telegram = telegram
        self.camera = camera
    
    def echo(update: Update, context: CallbackContext):
        text = update.message.text

        if 