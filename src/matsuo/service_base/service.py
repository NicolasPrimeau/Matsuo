from abc import ABC, abstractmethod
from matsuo.utils.host import FlaskHost
from matsuo.utils import config_helper
from matsuo.utils import requests


class Service(ABC):

    def __init__(self, service_name):
        self.service_name = service_name

    @abstractmethod
    def start(self):
        raise NotImplementedError('Implement me')


class HostedService(Service):

    def __init__(self, service_name, host_type=FlaskHost):
        super().__init__(service_name=service_name)
        host_config = config_helper.get_config(requests.SERVICE_ENDPOINT_PARAM_NAME, self.service_name)
        self.host = host_type(service_name=self.service_name, hostname=host_config['hostname'],
                              port=host_config['port'], is_publicly_accessible=True)

    @abstractmethod
    def start(self):
        super().start()