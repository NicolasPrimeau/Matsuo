
from matsuo.service_base.service import Service


class HaikuService(Service):

    _servie_name = "Haiku Generator"

    def __init__(self):
        super().__init__(self._service_name)