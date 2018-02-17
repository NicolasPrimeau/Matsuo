
from matsuo.service_base.service import HostedService


class HaikuService(HostedService):

    SERVICE_NAME = 'Haiku Generator'

    def __init__(self, **kwargs):
        super().__init__(HaikuService.SERVICE_NAME, kwargs)

    def generate_haiku(self, args):
        pass

    def start(self):
        self.host.add_endpoint('generate_haiku', self.generate_haiku, methods=['GET'])
        self.host.start()
