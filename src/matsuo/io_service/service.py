from PIL import Image
from flask import render_template, request, url_for, send_from_directory
import os

from werkzeug.utils import redirect

from matsuo.service_base.service import HostedService


UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload(*wargs, **kwargs):
    if request.method == 'POST':
        pic = request.files['file']
        if pic and allowed_file(pic.filename):
            pic.save(os.path.join(UPLOAD_FOLDER, pic.filename))
            img = Image.open(os.path.join(UPLOAD_FOLDER, pic.filename))
            img.thumbnail((300,300), resample=0)
            img.save(os.path.join(UPLOAD_FOLDER, pic.filename))
            with open(UPLOAD_FOLDER + '/current_filename.txt', 'w') as c:
                c.write(pic.filename)
            return redirect(url_for('uploaded_file', filename=pic.filename))
    return redirect(url_for('main'))


def uploaded_file(*wargs, **kwargs):
    return render_template('template1.html', filename=wargs[1]['filename'])


def send_file(*wargs, **kwargs):
    return send_from_directory(UPLOAD_FOLDER, wargs[1]['filename'])


def generate(*wargs, **kwargs):
    haiku = "Five syllables here\nSeven more syllables there\nAre you happy now?"
    if request.method == 'POST':
        #-----------
        #GENERATE THE HAIKU HERE
        #-----------
        pass
    with open(UPLOAD_FOLDER + '/current_filename.txt') as c:
        filename = c.readline()
    shaiku=haiku.split('\n')
    return render_template('template1.html',
                            haiku=True,
                            haiku1 = shaiku[0],
                            haiku2 = shaiku[1],
                            haiku3 = shaiku[2],
                            filename=filename)


def main(*wargs, **kwargs):
    return render_template('template1.html', **locals())


class IoService(HostedService):

    SERVICE_NAME = 'IO'

    def __init__(self, **kwargs):
        super().__init__(IoService.SERVICE_NAME, kwargs=kwargs)
        self.host.app.static_folder = UPLOAD_FOLDER
        global BASE_PATH

    def start(self):
        self.host.add_endpoint('/upload', 'upload', upload, methods=['POST'])
        self.host.add_endpoint('/show/<filename>', 'uploaded_file', uploaded_file, methods=['GET'])
        self.host.add_endpoint('/uploads/<filename>', 'send_file', send_file, methods=['GET'])
        self.host.add_endpoint('/generate', 'generate', generate, methods=['POST'])
        self.host.add_endpoint('/main', 'main', main, methods=['GET'])
        self.host.start()
