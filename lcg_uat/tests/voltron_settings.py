import json
import logging

import os
import voltron

from voltron.pages.shared import get_device_properties
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.helpers import do_request
from voltron.utils import mixins


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class VoltronSettings(mixins.LoggingMixin, metaclass=Singleton):
    _logger = logging.getLogger('voltron_logger')

    def __init__(self, environment: str = 'qa2.sports.coral.co.uk', location: str = 'IDE', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment = environment
        with open(os.path.join(os.path.split(voltron.__file__)[0], 'resources/environments.json'),
                  encoding='utf-8') as config_file:
            config_data = json.load(config_file)
            self.params = {}
            self.build_info_json = self.get_build_info_json_data()
            self.cms_envs = {
                'https://cms-dev0.coral.co.uk': 'dev0',
                'https://cms-dev1.coral.co.uk': 'dev1',
                'https://cms-dev2.coral.co.uk': 'dev2',
                'https://cms-tst0.coral.co.uk': 'tst0',
                'https://cms-tst1.coral.co.uk': 'tst1',
                'https://cms-stg.coral.co.uk': 'stg0',
                'https://cms-hl.coral.co.uk': 'hlv0',
                'https://cms-hlv1.coral.co.uk': 'hlv1',
                'https://cms-hl2.coral.co.uk': 'hlv2',
                'https://cms.coral.co.uk': 'prd0',
                'https://cms-dev0.ladbrokes.com': 'dev0',
                'https://cms-dev1.ladbrokes.com': 'dev1',
                'https://cms-dev2.ladbrokes.com': 'dev2',
                'https://cms-tst0.ladbrokes.com': 'tst0',
                'https://cms-tst1.ladbrokes.com': 'tst1',
                'https://cms-stg.ladbrokes.com': 'stg0',
                'https://cms-hl.ladbrokes.com': 'hlv0',
                'https://cms-hlv1.ladbrokes.com': 'hlv1',
                'https://cms-hl2.ladbrokes.com': 'hlv2',
                'https://cms-prod.ladbrokes.com': 'prd0'

            }
            self.required_params = {
                'cms_env': 'CMS_ENDPOINT',
                'bpp': 'BPP_ENDPOINT',
                'timeform': 'TIMEFORM_ENDPOINT',
                'optin_hostname': 'OPT_IN_ENDPOINT',
                'banach_api_hostname': 'BYB_CONFIG',
                'hr_bet_filter_url': 'BET_FINDER_ENDPOINT',
                'datafabric_url': 'RACING_POST_API_ENDPOINT',
                'datafabric_api_key': 'RACING_POST_API_KEY',
                'environment': 'ENVIRONMENT',
                "BETTINGMS": "BETTINGMS"
            }
            for name, value in config_data['default'].items():
                self.params[name] = value
                self.replace_params_with_build_info(name=name)
            if environment.endswith('ladbrokes.com'):
                for name, value in config_data['default_ladbrokes'].items():
                    self.params[name] = value
                    self.replace_params_with_build_info(name=name)
            if environment in config_data.keys():
                for name, value in config_data[environment].items():
                    self.params[name] = value
                    self.replace_params_with_build_info(name=name)
            else:
                proxy_environment = self.params.get("environment", None)
                proxy_brand = self.params.get("brand", None)
                proxy_env_map = {
                    "bma": {
                        "hiddenprod": "beta-sports.coral.co.uk",
                        "stg": "test.sports.coral.co.uk",
                        "tst2": "qa2.sports.coral.co.uk",
                        "prod": "sports.coral.co.uk"
                    },
                    "ladbrokes": {
                        "hiddenprod": "beta-sports.ladbrokes.com",
                        "stg": "test.sports.ladbrokes.com",
                        "tst2": "qa2.sports.ladbrokes.com",
                        "prod": "sports.ladbrokes.com"
                    }
                }
                try:
                    mapped_env = proxy_env_map.get(proxy_brand, None).get(proxy_environment, None)
                    result = {"value": mapped_env, "error": None}
                except (KeyError, AttributeError) as e:
                    result = {"value": None, "error": str(e)}

                if result["error"] is not None:
                    # Handle the error
                    self._logger.error(f"An error occurred: {result['error']}")
                    raise GeneralException(
                        message=f"An error occurred while Determining the Proxy Env For {environment}")
                else:
                    mapped_env = result["value"]
                    for name, value in config_data[mapped_env].items():
                        self.params[name] = value
                        self.replace_params_with_build_info(name=name)
                    self._logger.info(
                        f'No matching Envs found for {environment} in environment.json Considering this as ProxyEnvironment')
                    self._logger.info(
                        f'ProxyEnvironment Details:\n environment-name: {environment} \n environment-brand:{proxy_brand} \n environment-mapped to {proxy_env_map[proxy_brand][proxy_environment]}')
                self._logger.warning(f'No specific configuration found for host "{environment}", defaults are used')
            if location in config_data.keys():
                for name, value in config_data[location].items():
                    self.params[name] = value
        with open(os.path.join(os.path.split(voltron.__file__)[0],
                               f'resources/uat_users/{self.params["brand"]}_uat_users.json'),
                  encoding='utf-8') as users_file:
            self.users_data = json.load(users_file)
            self._logger.info(self.users_data)
        self.cards = {
            'master_card': self.master_card,
            'visa_card': self.visa_card,
            'maestro': self.maestro_card,
        }

    def get_build_info_json_data(self):
        url = f'https://{self.environment}/buildInfo.json'
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        request = do_request(method='GET', url=url, headers=headers)
        return request['environment']

    def replace_params_with_build_info(self, name):
        if name in self.required_params.keys():
            if name == 'banach_api_hostname':
                param = self.required_params[name]
                self.params[name] = self.build_info_json[param]['uri'].replace('api', '')
            elif name == 'cms_env':
                param = self.build_info_json[self.required_params[name]].replace('/cms/api', '')
                self.params[name] = self.cms_envs[param]
            elif name == 'bpp':
                param = self.required_params[name]
                self.params[name] = self.build_info_json[param].replace('Proxy', 'Proxy/')
            elif name == 'environment':
                param = self.required_params[name]
                self.params[name] = self.build_info_json[param]
            elif name == "BETTINGMS":
                param = self.required_params[name]
                self.params[name] = self.build_info_json[param]+'/'
            else:
                self.params[name] = self.build_info_json[self.required_params[name]]

    @property
    def device_type(self):
        return get_device_properties()['type']

    @property
    def market_link_pattern(self):
        return '^\\+[\\d]+(\nMARKETS)*$' if self.device_type == 'desktop' and self.brand == 'bma' else '^\\d+ MORE*$'

    @property
    def football_autotest_league(self):
        return f'{self.football_autotest_competition} - {self.football_autotest_competition_league}'

    @property
    def football_autotest_special_league(self):
        return '%s - %s' % (self.football_autotest_competition, self.football_autotest_competition_special_league)

    @property
    def football_autotest_league2(self):
        return '%s - %s' % (self.football_autotest_competition, self.football_autotest_competition_league_2)

    def __getattr__(self, item):
        try:
            return os.environ[item.upper()]
        except KeyError:
            pass
        if 'user' in item:
            try:
                users = self.users_data[self.backend_env][item]
                from random import choice
                return choice(users)
            except Exception as e:
                raise GeneralException(f'Error occurred during account request "{e}"')
        elif item in self.params.keys():
            return self.params[item]
        else:
            raise Exception('Unknown setting "%s"' % item)
