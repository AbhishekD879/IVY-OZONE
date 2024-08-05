import logging
import re
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

import requests
from lxml import html

from crlat_ob_client import OBException
from crlat_ob_client.login import OBLogin
from crlat_ob_client.utils.helpers import check_status_code, do_request
from datetime import datetime, timedelta

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

from crlat_ob_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


class Freebet(OBLogin):
    customer = None

    def __init__(self, env, brand, redemption_value, freebet_name, *args, **kwargs):
        super(Freebet, self).__init__(env, brand, *args, **kwargs)
        self.redemption_value = redemption_value
        self.freebet_name = freebet_name

    def get_future_date_as_encoded_url(self, expiration_date=None, **kwargs):
        days = kwargs.get('days', 30)
        now = datetime.utcnow()
        self._logger.debug('Current date is: %s' % now.strftime("%Y-%m-%d %H:%M:%S"))
        future = expiration_date if expiration_date else now + timedelta(
            days=days)  # added n days to current date
        self._logger.debug('Future date is: %s' % future.strftime("%Y-%m-%d %H:%M:%S"))
        future_url_date = quote(future.strftime("%Y-%m-%d %H:%M:%S"))
        self._logger.debug('Future URL date is: %s' % future_url_date)
        return future_url_date

    def get_custid(self, username, raise_exceptions=True):
        """
        :param username - username on coral/OB site
        :param raise_exceptions - raise OBException if True
        """
        custid_parameters = 'camp_mgr' \
                            '?action=FREEBETS%3A%3ADoAdhocTokensCustSearch' \
                            '&Username={username}' \
                            '&ExactName=Y' \
                            '&UpperName=Y' \
                            '&SiteOperatorId=-1'.format(username=username)
        url = self.site[:-2] + custid_parameters  # removing last 2 symbols from site as /office is not needed
        self._logger.debug('*** requesting by url : "%s"' % url)
        r = requests.get(url=url, cookies=self.site_cookies, verify=False)
        check_status_code(r)
        page = html.fromstring(r.content)
        try:
            self.__class__.customer = page.xpath('//input[@name="CustId"]')[0].attrib['value']
        except IndexError:
            self._logger.debug("Current user doesn't have Free Bets available")
        self._logger.debug('*** customer_id: "%s"' % self.customer)
        if not self.customer and raise_exceptions:
            raise OBException('Customer id was not found')
        return self.customer

    def give_offer(self, freebet_value=1, expiration_date=None):
        """
        :param expiration_date: expiration date in format %Y-%m-%d %H:%M:%S.
        """
        expiration_date = self.get_future_date_as_encoded_url(expiration_date=expiration_date, days=10)
        offer_parameters = 'camp_mgr' \
                           '?Value={freebet_value}' \
                           '&CcyCode=GBP' \
                           '&RValID={redemption_value}' \
                           '&AbsoluteEx={expiration_date}' \
                           '&RelativeEx=' \
                           '&OfferID={offer_id}' \
                           '&action=FREEBETS%3A%3ADoRewardAdhocTokens' \
                           '&CustId={customer}'.format(expiration_date=expiration_date, customer=self.customer,
                                                       redemption_value=self.redemption_value,
                                                       freebet_value=freebet_value,
                                                       offer_id=self.backend.ob.freebets.general_offer.offer_id)
        url = self.site[:-2] + offer_parameters
        self._logger.debug('*** requesting by url : "%s"' % url)
        do_request(url=url, load_response=False, cookies=self.site_cookies)

    def add_freebet_to_level(self, level, id):
        """
        linking freebet offer for specific level
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
                            '&opAdd=0'.format(name=quote(self.freebet_name), level=level.upper(), key=id,
                                              redemption_value=self.redemption_value)
        url = self.site[:-2] + custid_parameters
        self._logger.debug('*** requesting by url : "%s"' % url)

        do_request(method='GET', url=url, cookies=self.site_cookies, load_response=False)


# def get_redemption_value(self): # TODO seems not needed for current implementation, but might be considered for redemption values with non-default bet type
    #     """ getting redemption id value for specific freebet title """
        # custid_parameters = 'camp_mgr?action=FREEBETS::GoRValList'
        # url = self.site[:-2] + custid_parameters
        # self._logger.debug('*** requesting by url : "%s"' % url)
        #
        # r = requests.post(url=url, cookies=self.site_cookies)
        # check_status_code(r)
        # self.__class__.redemption_value = re.search('RValID=(\d+).+%s' % self.freebet_name, str(r.content)).groups()[0]
        # self._logger.info('*** freebet_redemption_id %s' % self.redemption_value)
