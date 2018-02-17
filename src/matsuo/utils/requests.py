

from matsuo.utils import config_helper
import urllib
import urllib.request
import json

SERVICE_ENDPOINT_PARAM_NAME = "service endpoints"


def get(service_name, api_endpoint, args):
    configs = config_helper.get_configs()
    validate_config(configs)
    endpoints = configs[SERVICE_ENDPOINT_PARAM_NAME]
    if service_name not in endpoints:
        raise ValueError('{} is not a configured service'.format(service_name))
    service_config = endpoints[service_name]
    return _get(service_config['hostname'], service_config['port'], api_endpoint, args)


def _get(hostname, port, api_endpoint, args):
    with urllib.request.urlopen('http://{}:{}/{}'.format(
            hostname, port, api_endpoint, urllib.urlencode(args))) as url:
        return json.loads(url.read().decode())


def validate_config(configs):
    if SERVICE_ENDPOINT_PARAM_NAME not in configs:
        raise ValueError('Configs should have {}'.format(SERVICE_ENDPOINT_PARAM_NAME))
    return True
