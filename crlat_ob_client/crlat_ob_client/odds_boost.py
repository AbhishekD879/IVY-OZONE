try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

import logging
import requests

from crlat_ob_client.freebet import Freebet
from crlat_ob_client.utils.helpers import check_status_code, do_request

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

from crlat_ob_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


class OddsBoost(Freebet):
    customer = None

    def __init__(self, env, brand, redemption_value, odds_boost_token_name, *args, **kwargs):
        super(OddsBoost, self).__init__(env, brand, redemption_value, '', *args, **kwargs)
        self.odds_boost_token_name = odds_boost_token_name
        self.redemption_value = redemption_value

    def give_offer(self, offer_id, token_value=1, expiration_date=None, days=2):
        """
        :param expiration_date: expiration date in format %Y-%m-%d %H:%M:%S.
        """
        expiration_date = self.get_future_date_as_encoded_url(expiration_date=expiration_date, days=days)
        offer_parameters = 'camp_mgr' \
                           '?Value={odds_boost_value}' \
                           '&CcyCode=GBP' \
                           '&RValID={redemption_value}' \
                           '&AbsoluteEx={expiration_date}' \
                           '&RelativeEx=' \
                           '&OfferID={offer_id}' \
                           '&action=FREEBETS%3A%3ADoRewardAdhocTokens' \
                           '&CustId={customer}'.format(expiration_date=expiration_date, customer=self.customer,
                                                       redemption_value=self.redemption_value,
                                                       odds_boost_value=token_value,
                                                       offer_id=offer_id)
        url = self.site[:-2] + offer_parameters
        self._logger.debug('*** requesting by url : "%s"' % url)
        do_request(url=url, cookies=self.site_cookies, load_response=False)

    def add_odds_boost_token_to_level(self, level, id):
        """
        linking odds boost token for specific level
        :param level: name of level, one of: MARKET, TYPE, CLASS, EVENT, SELECTION
        :param id: id of event/type/class/selection/market
        """
        custid_parameters = 'camp_mgr?' \
                            'action=CM::drilldown::go_drilldown' \
                            '&level={level}' \
                            '&id={id}' \
                            '&sports_only=' \
                            '&type='.format(level=level.upper(), id=id)
        url = self.site[:-2] + custid_parameters
        self._logger.debug('*** requesting by url : "%s"' % url)

        do_request(method='GET', url=url, cookies=self.site_cookies, load_response=False)

        custid_parameters = 'camp_mgr?' \
                            'rname={name}' \
                            '&level={level}&' \
                            'key={key}' \
                            '&type=' \
                            '&RValID={redemption_value}' \
                            '&SubmitName=RValMod' \
                            '&action=FREEBETS%3A%3ADoRVal' \
                            '&opAdd=0'.format(name=quote(self.odds_boost_token_name), level=level.upper(), key=id,
                                              redemption_value=self.redemption_value)
        url = self.site[:-2] + custid_parameters
        self._logger.debug('*** requesting by url : "%s"' % url)

        do_request(method='GET', url=url, cookies=self.site_cookies, load_response=False)
