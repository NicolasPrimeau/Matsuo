from abc import ABC, abstractmethod


class Service(ABC):

    def __init__(self, service_name):
        self.service_name = service_name

    @abstractmethod
    def start(self):
        raise NotImplementedError('Implement me')
