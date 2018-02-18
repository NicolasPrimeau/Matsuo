
from matsuo.service_base.service import HostedService
from matsuo.describe_service.describe_service import DescribeService
from matsuo.haiku_service.haiku_service import HaikuService
from matsuo.utils import requests


def get_haiku(args):
    describe_service_result = requests.get(DescribeService.SERVICE_NAME, 'get_keywords', args)
    return requests.get(HaikuService.SERVICE_NAME, 'generate_haiku', describe_service_result)


class CoordinatorService(HostedService):

    SERVICE_NAME = 'Coordinator'

    def __init__(self, **kwargs):
        super().__init__(CoordinatorService.SERVICE_NAME, kwargs=kwargs)

    def start(self):
        self.host.add_endpoint('get_haiku', 'get_haiku', get_haiku, methods=['GET'])
        self.host.start()
