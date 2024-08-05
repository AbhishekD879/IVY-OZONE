import json

import requests

import tests
from voltron.utils import mixins
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.helpers import check_response
from voltron.utils.helpers import check_status_code
from voltron.utils.helpers import do_request

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass


class BPPConfig(mixins.LoggingMixin,):

    def get_currency_exchange_rates(self, currency_code=None):
        """
        :param currency_code: string - USD, GBP, SEK, HKD, EUR, AUD
        :return: float - exchange rate if currency_code is specified, if not - dictionary with all exchange rates
        """
        url = '{0}currencies'.format(tests.settings.bpp)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https:{tests.HOSTNAME}'
        }
        self._logger.debug('*** Request url %s' % url)
        r = requests.get(url=url, headers=headers)
        check_status_code(r)
        check_response(r)
        try:
            currencies = json.loads(r.text)['response']['respGetCurrencies']['currencyDetail']
        except KeyError as e:
            raise GeneralException(e)
        exchange_rates = {currency['currency']: float(currency['exchangeRate']) for currency in currencies}
        if not currency_code:
            return exchange_rates
        return exchange_rates[currency_code]

    def get_account_freebets(self, bpp_user_token: str) -> dict:
        """
        Retrieve data with available free bet tokens for specified user
        :param bpp_user_token: Unique user BPP token
        :return: dict with user free bet tokens
        """
        url = f'{tests.settings.bpp}accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https:{tests.HOSTNAME}',
            'token': bpp_user_token
        }
        self._logger.debug(f'*** Request url {url}')
        r = do_request(method='GET', url=url, headers=headers)
        try:
            freebets = r['response']['model']['freebetToken']
        except KeyError as e:
            raise GeneralException(e)

        return freebets

    def delete_bpp_token(self, bpp_user_token: str, username: str):
        """
        :param bpp_user_token: Unique user BPP token
        :param username: logged user
        :return: int request status code
        """
        url = f'{tests.settings.bpp}auth/invalidateSession'
        headers = {
            'token': bpp_user_token,
            'username': username
        }
        self._logger.debug(f'*** Request url {url}')
        r = requests.delete(url=url, headers=headers, verify=False)
        check_status_code(r)
        return r
