
from matsuo.service_base.service import Service
from matsuo.utils.host import FlaskHost
from matsuo.utils import config_helper
from matsuo.utils import requests


class HaikuService(Service):

    _service_name = "Haiku Generator"

    def __init__(self, host=FlaskHost):
        super().__init__(self._service_name)
        host_config = config_helper.get_config(requests.SERVICE_ENDPOINT_PARAM_NAME, self._service_name)
        self.host = host(service_name=self._service_name, hostname=host_config['hostname'],
                         port=host_config['port'], is_publicly_accessible=True)

    def generate_haiku(self, args):
        pass

    def start(self):
        self.host.add_endpoint('get/generate_haiku', self.generate_haiku, methods=['GET'])
        self.host.start()
