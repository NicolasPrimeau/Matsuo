
from flask import Flask
from flask import request


class Host:

    def __init__(self, app_name, hostname='localhost', port=80):
        self.app_name = app_name
        self.hostname = hostname
        self.port = port


class SimpleHost(Host):
    pass


class FlaskHost(SimpleHost):

    def __init__(self, service_name, hostname, port, is_publicly_accessible=False):
        super().__init__(app_name=service_name, hostname=hostname, port=port)
        self.app = Flask(service_name)
        self.is_publicly_accessible = is_publicly_accessible
        self.add_endpoint('/', 'index', lambda args: '<h1>{}</h1>'.format(service_name))

    def start(self):
        if self.is_publicly_accessible:
            self.app.run(host='0.0.0.0', port=self.port)
        else:
            self.app.run(port=self.port)

    def add_endpoint(self, name, func_name, func, methods=('GET', 'POST')):
        if name[0] != '/':
            name = '/' + name
        self.app.add_url_rule(name, endpoint=func_name, view_func=lambda: func(request.args), methods=methods)
