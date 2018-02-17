import os
from flask import Flask, render_template, request

from matsuo.haiku_service.haiku_service import HaikuService
from matsuo.utils import requests

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    img = request.files.getlist("file")
    requests.get(HaikuService.SERVICE_NAME, 'get_haiku', {img})
    return render_template("complete.html")


if __name__== "__main__":
    app.run(port=3333, debug=True)
