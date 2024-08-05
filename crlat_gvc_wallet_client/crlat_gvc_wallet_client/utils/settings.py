import os

import yaml
from crlat_core.datatypes.dict_keys_to_properties import DictKeysToProperties


class GVCSettings(object):
    """This class contains functionality to represent config data as property variables"""

    config = None

    def __init__(self, backend, brand, env_host=None):
        config_file = f'resources/environments_config_{brand}.yaml'
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               config_file)) as yamlfile:
            config = yaml.full_load(yamlfile)
            if env_host:
                self.config = DictKeysToProperties(**config[backend][env_host])
            else:
                self.config = DictKeysToProperties(**config[backend])
            self.config.backend = backend

    def __getattr__(self, item):
        try:
            return self.config[item]
        except (AttributeError, KeyError):
            raise Exception(f'Error getting "{item}"')


_gvc_settings = None


def define_gvc_settings(backend, brand, env_host=None):
    global _gvc_settings
    _gvc_settings = GVCSettings(backend=backend, brand=brand, env_host=env_host)


def get_gvc_settings():
    return _gvc_settings
