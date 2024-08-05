import json
import logging

import os
import voltron

from voltron.pages.shared import get_device_properties
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.helpers import do_request
from voltron.utils import mixins


class IOSNativeSettings(mixins.LoggingMixin):
    _logger = logging.getLogger('voltron_logger')

    def __init__(self, environment: str = 'qa2.sports.coral.co.uk', location: str = 'IDE'):
        self.environment = environment
        with open(os.path.join(os.path.split(voltron.__file__)[0], 'resources/ios_native_environments.json'),
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

    @property
    def device_type(self):
        return get_device_properties()['type']

    def __getattr__(self, item):
        try:
            return os.environ[item.upper()]
        except KeyError:
            pass
        if 'user' in item:
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
