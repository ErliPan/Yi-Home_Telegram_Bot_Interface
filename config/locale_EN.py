CAMERA_OFFLINE = "❌Camera offline"
CAMERA_DISABLED = "⛔️Camera disabled"
MOTION_DETECTED = "🏃Movement detected"
CAMERA_STATUS = "Cameras status📹"

#Say tts function
SPEAK_LANG = "en-US"
EMPTY_ARGS = "❌Error incorrect args"

#Play sound function
PLAY_VOICE = "📢Playing this"

NOTIFICATION_YES = "🔔"
NOTIFICATION_NO = "🔕"

WAIT = "⏳Elaborating...⌛️"


def NOTIFY_ON(CAMNAME):
    return f"🔔Activate alert {CAMNAME}"


def NOTIFY_OFF(CAMNAME):
    return f"🔕Disable alert {CAMNAME}"


def TURNING_ON(CAMNAME):
    return f"🎬Activate on {CAMNAME}"


def TURNING_OFF(CAMNAME):
    return f"💤Disable {CAMNAME}"


def IMAGE(CAMNAME):
    return f"📷{CAMNAME} Picture"


def STATUS_OFFLINE(CAMNAME):
    return f"⛔️<code>{CAMNAME}</code> is <code>offline</code>\n"


def STATUS_DISABLED(CAMNAME):
    return f"⚠️<code>{CAMNAME}</code> is <code>disabled</code>\n"


def STATUS_ONLINE(CAMNAME, NOTIFY):
    return f"✅<code>{CAMNAME}</code> is <code>online</code>, alerts {NOTIFY}\n"


#Play sound function
def PLAYING_FILE(FILENAME):
    return f"🎶Playing file: <code>{FILENAME}</code>"


def FILE_NOT_FOUND(FILENAME):
    return f"❌File not found: <code>{FILENAME}</code>"


def TTS_SAYING(TEXT):
    return f"🔊Saying <b><i>{TEXT}</i></b>"


def SET_STATUS_ON(CAMNAME):
    return f"⚙️Activating <code>{CAMNAME}</code>..."


def SET_STATUS_OFF(CAMNAME):
    return f"⚙️Deactivating <code>{CAMNAME}</code>..."


def SET_STATUS_FAILED():
    return f"❌Failed operation"