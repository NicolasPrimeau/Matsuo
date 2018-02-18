from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from random import randint
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder='images')
APP_ROT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        pic = request.files['file']
        pic.save("./images/test.jpg")
        return redirect(url_for('main'))

@app.route("/main",methods=['GET', 'POST'])
def main():
    pic_filename = "test.jpg"
    text = "Please submit a picture!"
    return render_template('template1.html',**locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
