CAMERA_OFFLINE = "Camera offline"
CAMERA_DISABLED = "Camera disabilitato"
MOTION_DETECTED = "Movimento"
STATUS_ON = "Acceso"
STATUS_OFF = "Spento"
NOTIFY_ON = "Accendi notifiche"
NOTIFY_OFF = "Spegni notifiche"
TURNING_ON = "Accendi"
TURNING_OFF = "Spegni"
IMAGE = "Foto"
CAMERA_STATUS = "Stato telecamere"
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline"
INTENT_YES = "Si"
INTENT_NO = "No"
ONLINE_LIST = "Stato telecamere"


def ONLINE_STATUS_MSG(CAMNAME, STATUS, ENABLED):
    return f"<code>{CAMNAME}</code> è <code>{STATUS}</code>, notifiche <code>{ENABLED}</code>\n"


#Play sound function
PLAY_VOICE = "Riproduco questo"
PLAY_COMMAND = "suono" # /suono

#Play sound function
def PLAYING_FILE(filename):
    return f"Riproduco file: {filename}"


def FILE_NOT_FOUND(filename):
    return f"File non trovato: {filename}"

#Say tts function
SPEAK_LANG = "it-IT"
EMPTY_ARGS = "Errore manca parametri"
SAY_COMMAND = "dici"


def TTS_SAYING(TEXT):
    return f"Dico {TEXT}"


def SET_STATUS(NAME, STATUS):
    return f"Impostando {NAME} {STATUS}..."


def CAMERA_STATE(NAME, STATUS):
    return f"{NAME} è {STATUS}"


def CAMERA_SET_FAILED(NAME):
    return f"Impostando {NAME} non riuscito"