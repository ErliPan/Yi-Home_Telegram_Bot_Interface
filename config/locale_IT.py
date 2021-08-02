CAMERA_OFFLINE = "Camera offline"
CAMERA_DISABLED = "Camera disabilitato"
MOTION_DETECTED = "Movimento"
CAMERA_STATUS = "Stato telecamere"

#Say tts function
SPEAK_LANG = "it-IT"
EMPTY_ARGS = "Errore manca parametri"

#Play sound function
PLAY_VOICE = "Riproduco questo"

NOTIFICATION_YES = "Si"
NOTIFICATION_NO = "No"

WAIT = "Operazione in corso..."


def NOTIFY_ON(CAMNAME):
    return f"Abilita avvisi {CAMNAME}"


def NOTIFY_OFF(CAMNAME):
    return f"Disabilita avvisi {CAMNAME}"


def TURNING_ON(CAMNAME):
    return f"Abilita {CAMNAME}"


def TURNING_OFF(CAMNAME):
    return f"Disabilita {CAMNAME}"


def IMAGE(CAMNAME):
    return f"{CAMNAME} Foto"


def STATUS_OFFLINE(CAMNAME):
    return f"<code>{CAMNAME}</code> è <code>offline</code>\n"


def STATUS_DISABLED(CAMNAME):
    return f"<code>{CAMNAME}</code> è <code>disabilitato</code>\n"


def STATUS_ONLINE(CAMNAME, NOTIFY):
    return f"<code>{CAMNAME}</code> è <code>online</code>, notifiche <code>{NOTIFY}</code>\n"


#Play sound function
def PLAYING_FILE(FILENAME):
    return f"Riproduco file: <code>{FILENAME}</code>"


def FILE_NOT_FOUND(FILENAME):
    return f"File non trovato: <code>{FILENAME}</code>"


def TTS_SAYING(TEXT):
    return f"Dico <b><i>{TEXT}</i></b>"


def SET_STATUS_ON(CAMNAME):
    return f"Abilitando <code>{CAMNAME}</code>..."


def SET_STATUS_OFF(CAMNAME):
    return f"Disabilitando <code>{CAMNAME}</code>..."


def SET_STATUS_FAILED():
    return f"Operazione fallita"