

from matsuo.utils import config_helper
import urllib.parse
import urllib.request
import json

SERVICE_ENDPOINT_PARAM_NAME = "service endpoints"


def get(service_name, api_endpoint, args):
    service_config = config_helper.get_config(SERVICE_ENDPOINT_PARAM_NAME, service_name)
    return _get(service_config['hostname'], service_config['port'], api_endpoint, args)


def _get(hostname, port, api_endpoint, args):
    with urllib.request.urlopen('http://{}:{}/{}'.format(
            hostname, port, api_endpoint, urllib.parse.urlencode(args))) as url:
        return json.loads(url.read().decode())
