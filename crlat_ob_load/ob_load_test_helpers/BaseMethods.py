import os
from crlat_ob_client.openbet_config import OBConfig
from crlat_ob_client.utils.helpers import generate_name

EVENT_PREFIX = os.getenv('EVENT_PREFIX', 'MQA')


class BaseMethods(object):
    def __init__(self, env, brand):
        self.__class__.backend_env = env
        self.__class__.brand = brand

    backend_env = None
    __ob_config = None

    @classmethod
    def get_ob_config(cls):
        if not cls.__ob_config:
            cls.__ob_config = OBConfig(env=cls.backend_env, brand=cls.brand)
        return cls.__ob_config

    @property
    def team1(self):
        return f'{EVENT_PREFIX} test {generate_name()}'

    @property
    def team2(self):
        return f'{EVENT_PREFIX} test {generate_name()}'

    @property
    def ob_config(self):
        self.get_ob_config()
        return self.__ob_config
