class IPCam:

    recording = False

    def __init__(self, Notifier, Camera, name):
        self.name = name
        self.Notifier = Notifier
        self.Camera = Camera

    
    def sendImage(self, msg):

        res = self.Camera.getImage()

        if res:
            self.Notifier.sendPhoto(r)
        else:
            self.Notifier.sendMessage("Camera offline")
        
        return res


    def __movementTriggered(self):
        self.bot.sendMessage("Movimento")
        self.sendImage("Camera offine")


    def update(self):
        if self.Camera.isRecording():
            if recording == False:
                __movementTriggered()
                recording = True
        else:
            recording = False


