CAMERA_OFFLINE = "Camera offline"
CAMERA_DISABLED = "Camera disabilitato"
MOTION_DETECTED = "Movimento"
STATUS_ON = "Acceso"
STATUS_OFF = "Spento"
TURNING_ON = "Accendi"
TURNING_OFF = "Spegni"
IMAGE = "Foto"
CAMERA_STATUS = "Stato telecamere"
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline"
INTENT_YES = "Si"
INTENT_NO = "No"
ONLINE_LIST = "Stato"


def ONLINE_STATUS_MSG(CAMNAME, STATUS, ENABLED):
    return f"Camera <code>{CAMNAME}</code> is <code>{STATUS}</code> notification <code>{ENABLED}</code>\n"


#Say tts function
EMPTY_ARGS = "Errore manca parametri"

SAY_COMMAND = "/say"

def TTS_SAYING(TEXT):
    return f"Dico {TEXT}"


def SET_STATUS(NAME, STATUS):
    return f"Trying to set {NAME} {STATUS}..."


def CAMERA_STATE(NAME, STATUS):
    return f"{NAME} è {STATUS}"


def CAMERA_SET_FAILED(NAME):
    return f"Trying to set {NAME} failed"