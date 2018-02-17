from matsuo.service_base.service import Service


class DescribeService(Service):

    SERVICE_NAME = 'DescribeService'

    def __init__(self, **kwargs):
        super().__init__(DescribeService.SERVICE_NAME, kwargs)

    def start(self):
        pass