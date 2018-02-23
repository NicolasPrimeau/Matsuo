import uuid
import io
from PIL import Image
from flask import render_template, request, url_for, send_file
import urllib.parse
from werkzeug.utils import redirect

from matsuo.io_service.cache import Cache
from matsuo.service_base.service import HostedService


def main(*wargs, **kwargs):
    return render_template('template1.html', **locals())


class IoService(HostedService):

    SERVICE_NAME = 'IO'

    def __init__(self, upload_folder='data/uploads', accepted_extensions={'png', 'jpg', 'jpeg', 'gif'}, **kwargs):
        super().__init__(IoService.SERVICE_NAME, kwargs=kwargs)
        self.host.app.static_folder = upload_folder
        self.upload_folder = upload_folder
        self.accepted_extensions = accepted_extensions
        self.cache = Cache()

    def start(self):
        self.host.add_endpoint('/upload', 'upload', self.upload, methods=['POST'])
        self.host.add_endpoint('/show', 'uploaded_file', self.uploaded_file, methods=['GET'])
        self.host.add_endpoint('/get/image', 'get_image', self.get_image, methods=['GET'])
        self.host.add_endpoint('/', 'main', main, methods=['GET'])
        self.host.start()

    def upload(self, *wargs, **kwargs):
        if request.method == 'POST':
            pic = request.files['file']
            if pic and self.allowed_file(pic.filename):
                img = Image.open(pic)
                img.thumbnail((600, 600), resample=0)
                output = io.BytesIO()
                img.save(output, format='png')
                output.seek(0)
                unique_id = uuid.uuid4().hex
                self.cache.add_item(unique_id, output)
                return redirect(url_for('uploaded_file', uid=unique_id))
        return redirect(url_for('main'))

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.accepted_extensions

    def uploaded_file(self, *wargs, **kwargs):
        uid = request.args['uid']
        return render_template('template1.html', haiku=self.get_haiku(self.cache.get_item(uid)), uid=uid)

    def get_image(self, *wargs, **kwargs):
        return send_file(
            self.cache.get_item(request.args['uid']),
            attachment_filename='file.png',
            mimetype='image/png'
        )

    def get_haiku(self, image_data):
        haiku = "Five syllables here\nSeven more syllables there\nAre you happy now?"
        if request.method == 'GET':
            #-----------
            #GENERATE THE HAIKU HERE
            #-----------
            pass

        return haiku.split('\n')
