import json
import logging
import os

import native_ios
from native_ios.pages.shared import get_device_properties
from native_ios.utils import mixins
from native_ios.utils.exceptions.general_exception import GeneralException
from native_ios.utils.helpers import do_request


class IOSNativeSettings(mixins.LoggingMixin):
    _logger = logging.getLogger('native_ios_logger')

    def __init__(self, environment: str = 'qa2.sports.coral.co.uk', location: str = 'IDE'):
        self.environment = environment
        self.location = location
        with open(os.path.join(os.path.split(native_ios.__file__)[0], 'resources/environments.json'),
                  encoding='utf-8') as config_file:
            config_data = json.load(config_file)
            self.params = {}
            for name, value in config_data['default'].items():
                self.params[name] = value
            if environment.endswith('ladbrokes.com'):
                for name, value in config_data['default_ladbrokes'].items():
                    self.params[name] = value
            if environment in config_data.keys():
                for name, value in config_data[environment].items():
                    self.params[name] = value
            else:
                self._logger.warning(f'No specific configuration found for host "{environment}", defaults are used')
            if location in config_data.keys():
                for name, value in config_data[location].items():
                    self.params[name] = value

        with open(os.path.join(os.path.split(native_ios.__file__)[0],
                               f'resources/uat_users/{self.params["brand"]}_uat_users.json'),
                  encoding='utf-8') as users_file:
            self.users_data = json.load(users_file)

    @property
    def device_type(self):
        return get_device_properties()['type']

    def __getattr__(self, item):
        try:
            # This 'if' block to avoid collision of brand variables for Fastlane and our framework
            if item.upper() != 'BRAND':
                return os.environ[item.upper()]
            else:
                pass
        except KeyError:
            pass
        if 'user' in item:
            if self.location == "IDE":
                try:
                    users = self.users_data[self.backend_env][item]
                    from random import choice
                    return choice(users)
                except Exception as e:
                    raise GeneralException(f'Error occurred during account request "{e}"')
            else:
                import psutil
                cmdline = psutil.Process(os.getpid()).cmdline()
                if '--collect-only' in cmdline or 'gocd_test_runner.py' in cmdline:
                    return
                try:
                    self._logger.debug(f'*** Requesting user "{item}" for brand "{self.brand}" on "{self.backend_env}" backend')
                    return do_request(method='GET',
                                      url=f'{self.accounts_sharing_url}/get_ios_user/{self.brand}/{self.backend_env}/{item}',
                                      load_response=False)
                except Exception as err:
                    raise GeneralException(f'Error occurred during account request "{err}"')
        elif item in self.params.keys():
            return self.params[item]
        else:
            raise GeneralException(f'Unknown setting "{item}"')
