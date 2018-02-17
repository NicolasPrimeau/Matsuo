from matsuo.haiku_service.solver import create_haiku
from matsuo.service_base.service import HostedService


def generate_haiku(args):
    keywords = args['keywords']
    haiku = create_haiku(keywords)
    return {
        'text': str(haiku)
    }


class HaikuService(HostedService):

    SERVICE_NAME = 'Haiku Generator'

    def __init__(self, **kwargs):
        super().__init__(HaikuService.SERVICE_NAME, kwargs)

    def start(self):
        self.host.add_endpoint('generate_haiku', generate_haiku, methods=['GET'])
        self.host.start()
