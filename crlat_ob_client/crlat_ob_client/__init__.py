import os
import yaml
from crlat_core.datatypes.dict_keys_to_properties import DictKeysToProperties

from crlat_ob_client.utils.exceptions import OBException
from crlat_ob_client.utils.settings import setup_logging

LOGGER_NAME = __name__
setup_logging()

_ob_cookies = None


def get_ob_cookies():
    return _ob_cookies


def set_ob_cookies(cookies):
    global _ob_cookies
    _ob_cookies = cookies


class BackEndSettings(object):
    """
    'crlat_backend_config_bma.yaml' – for Coral
    'crlat_backend_config_ladbrokes.yaml' – for Ladbrokes
    """

    config = None

    def __init__(self, backend, brand):
        self.brand = 'bma' if brand != 'ladbrokes' else brand

        with open(os.path.join(os.path.split(__file__)[0],
                               f'./resources/{self.brand}/crlat_backend_config_{backend}.yaml')) as yamlfile:
            config = yaml.full_load(yamlfile)
            self.config = DictKeysToProperties(**config[backend])

    def __getattr__(self, item):
        try:
            return self.config[item]
        except (AttributeError, KeyError):
            raise OBException(f'Error getting "{item}" for "{self.brand}" brand')
