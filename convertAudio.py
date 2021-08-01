from sys import argv
import os
import os.path
from config import *


if __name__ == "__main__":
    try:
        script, inFile, outFile, time = argv
    except:
        try:
            script, inFile, outFile = argv
            time = None
        except:
            print("arg error: inFile outFile cutoff(optional)")
            quit()


    if os.path.isfile(inFile):
        outFile = outFile.replace(".wav", "")
        if time == None:
            os.system(f"ffmpeg -i {inFile} -acodec pcm_s16le -ac 1 -ar 16000 {SOUND_SAVE_PATH}{outFile}.wav -y")
        else:
            os.system(f"ffmpeg -i {inFile} -t {time} -acodec pcm_s16le -ac 1 -ar 16000 {SOUND_SAVE_PATH}{outFile}.wav -y")
        print("done")
        os.unlink(inFile)
    else:
        print("inFile does not exist")