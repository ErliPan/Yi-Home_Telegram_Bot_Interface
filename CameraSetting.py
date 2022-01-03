import json

class CameraSetting:

    def __init__(self, configPath):
        self.configPath = configPath
        self.config = json.load(open(self.configPath))

    def addPaddingToNames(self):
        maxlen = 0
        for cam in self.config:
            if len(cam["name"]) > maxlen:
                maxlen = len(cam["name"])

        for cam in CAMERAS:
            if len(cam["name"]) < maxlen:
                padding = (maxlen - len(cam["name"]))
                #Half padding at the beginning and half at the end. In case of odd padding the end have the extra
                cam["name"] = cam["name"] + ((padding - (padding // 2)) * "_")
                cam["name"] = ((padding // 2) * "_") + cam["name"]

    def getAllConfigs(self):
        return self.config
    
    def getConfig(self, name, param):
        return self.config[name][param]

    def setConfig(self, name, param, value):
        self.config[name][param] = value
        json.dump(self.config, open(self.configPath, "w"))
