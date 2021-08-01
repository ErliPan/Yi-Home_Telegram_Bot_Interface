CAMERA_OFFLINE = "Camera offline"
CAMERA_DISABLED = "Camera disabled"
MOTION_DETECTED = "Movement detected"
STATUS_ON = "Turned on"
STATUS_OFF = "Turned off"
TURNING_ON = "Turning on"
TURNING_OFF = "Turning off"
IMAGE = "Picture"
CAMERA_STATUS = "Cameras status"
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline"
INTENT_YES = "Yes"
INTENT_NO = "No"
ONLINE_LIST = "Camera state"


def ONLINE_STATUS_MSG(CAMNAME, STATUS, ENABLED):
    return f"<code>{CAMNAME}</code> is <code>{STATUS}</code> with notification <code>{ENABLED}</code>\n"


#Play sound function
PLAY_VOICE = "Playing this"
PLAY_COMMAND = "/sound"

#Play sound function
def PLAYING_FILE(filename):
    return f"Playing file: {filename}"


def FILE_NOT_FOUND(filename):
    return f"File not found: {filename}"

#Say tts function
SPEAK_LANG = "en-US"
EMPTY_ARGS = "Error incorrect args"
SAY_COMMAND = "/say"

def TTS_SAYING(TEXT):
    return f"Saying {TEXT}"


def SET_STATUS(NAME, STATUS):
    return f"Setting {NAME} {STATUS}..."


def CAMERA_STATE(NAME, STATUS):
    return f"{NAME} is {STATUS}"


def CAMERA_SET_FAILED(NAME):
    return f"Setting {NAME} failed"