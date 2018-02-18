from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
from random import randint
from werkzeug.utils import secure_filename
import os
from PIL import Image

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),"uploads")
app = Flask(__name__)
app.static_folder = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def index():
    return render_template("upload.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        pic = request.files['file']
        if pic and allowed_file(pic.filename):
            pic.save(os.path.join(UPLOAD_FOLDER, pic.filename))
            img = Image.open(os.path.join(UPLOAD_FOLDER, pic.filename))
            img.thumbnail((300,300), resample=0)
            img.save(os.path.join(UPLOAD_FOLDER, pic.filename))
            with open('./uploads/current_filename.txt', 'w') as c:
                c.write(pic.filename)
            return redirect(url_for('uploaded_file', filename=pic.filename))
        return redirect(url_for('main'))

@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('template1.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
     return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/generate', methods=['POST'] )
def generate():
    if request.method == 'POST':
        haiku = "Five syllables here\nSeven more syllables there\nAre you happy now?"
        #-----------
        #GENERATE THE HAIKU HERE
        #-----------
        pass
    with open('./uploads/current_filename.txt', 'r') as c:
        filename = c.readline()
    shaiku=haiku.split('\n')
    return render_template('template1.html',
                            haiku=True,
                            haiku1 = shaiku[0],
                            haiku2 = shaiku[1],
                            haiku3 = shaiku[2],
                            filename=filename)

@app.route("/main",methods=['GET', 'POST'])
def main():
    return render_template('template1.html',**locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
