import logging
import requests
import urllib3
from urllib.parse import quote
from requests import HTTPError
from requests import request
from crlat_siteserve_client import LOGGER_NAME
from crlat_siteserve_client.utils.exceptions import SiteServeException

urllib3.disable_warnings()
urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

_logger = logging.getLogger(LOGGER_NAME)


def do_request(url, cookies=None, method='POST', **kwargs):
    cookies = cookies if cookies else {}
    timeout = kwargs.get('timeout', 30)
    kwargs.pop('timeout', None)  # because timeout is in args already
    _logger.debug('List of keyword parameters: %s', kwargs.get('params'))
    r = request(url=url, cookies=cookies, method=method, timeout=timeout, verify=False, **kwargs)
    keyword_params = kwargs['params'] if 'params' in kwargs else ''
    _logger.debug('*** Performing %s request %s%s' % (
        method,
        url,
        ('?' + '&'.join(['%s=%s' % (k, quote(v)) for k, v in keyword_params])) if len(keyword_params) else ''
    ))
    check_status_code(r)
    # _logger.debug('\n\n\n"%s"', r.text)
    resp_dict = r.json()
    return resp_dict


def check_status_code(request):
    r = request
    try:
        r.raise_for_status()
    except HTTPError as e:
        raise SiteServeException(f'Something goes wrong with request. Status code: {r.status_code}: {r.reason}')


def extract_response(response: dict, raise_exceptions: bool=True) -> list:
    """
    Extracts responseFooter from SiteServe response, leaving list of objects only
    :param response: response from SiteServe as is
    :param raise_exceptions: whether to raise exceptions on empty response or not
    :return: list of dictionaries
    """
    try:
        children = response['SSResponse']['children']
        # _logger.debug(f'Received response:\n{response["SSResponse"]}')
        children = [child for child in children if 'responseFooter' not in child]
        if raise_exceptions and not children:
            raise SiteServeException('Error getting data from response')
        return children
    except Exception as err:
        raise SiteServeException('Error getting data from response "%s"' % err)
