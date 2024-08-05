import os
import yaml
import logging.config

from crlat_cms_client.utils.exceptions import CMSException
from crlat_cms_client.utils.helpers import DictKeysToProperties

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CMSSettings(object):
    """cms_config.yaml"""

    config = None

    def __init__(self, backend, brand):
        config_file = f'resources/cms_config_{brand}.yaml'
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               config_file)) as yamlfile:
            config = yaml.full_load(yamlfile)
            self.config = DictKeysToProperties(**config[backend])
            self.config.backend = backend

    def __getattr__(self, item):
        try:
            return self.config[item]
        except (AttributeError, KeyError):
            raise CMSException(f'Error getting "{item}"')


_cms_settings = None


def define_cms_settings(env, brand):
    global _cms_settings
    _cms_settings = CMSSettings(backend=env, brand=brand)


def get_cms_settings():
    return _cms_settings


def setup_logging(env_key: str = 'LOCATION_NAME') -> None:
    """Setup logging configuration

    :param env_key: Name of the environment key
    """
    location = os.getenv(env_key, 'IDE')
    if location:
        config_file_name = 'dev' if location not in ['AWS', 'AWS_GRID', 'Mac_Mini_GRID'] else 'default'
        path = os.path.join(BASE_DIR, f"resources/logging/{config_file_name}.yaml")

    try:
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    except Exception:
        default_path = os.path.join(BASE_DIR, "resources/logging/default.yaml")
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
