
from matsuo.service_base.service import HostedService


class HaikuService(HostedService):

    def generate_haiku(self, args):
        pass

    def start(self):
        self.host.add_endpoint('get/generate_haiku', self.generate_haiku, methods=['GET'])
        self.host.start()
