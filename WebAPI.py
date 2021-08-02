import flask
from flask import request, jsonify
import threading

class WebAPI:

    def __init__(self, cams):

        app = flask.Flask(__name__)

        @app.route('/', methods=['GET'])
        def home():
            return jsonify({"online":True})


        @app.route('/cameras', methods=['GET'])
        def cameras():
            camList = []

            for cam in cams:
                status = {}
                status["online"] = cam.isOnline()
                status["notify"] = cam.sendNotification()
                status["enabled"] = cam.isEnabled()
                camList.append(status)

            return jsonify(camList)


        threading.Thread(target=app.run, args=('10.0.0.119',)).start()