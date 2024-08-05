import json
import urllib
import logging

from faker import Faker
from requests import HTTPError
from requests import request
import requests

from crlat_ob_client import LOGGER_NAME
from crlat_ob_client.utils.exceptions import OBException


requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

_logger = logging.getLogger(LOGGER_NAME)


def generate_name():
    fake = Faker()
    name = fake.city()
    return name


def do_request(url, cookies, method='POST', load_response=True, **kwargs):
    keywords = kwargs
    timeout = kwargs.get('timeout', 30)
    kwargs.pop('timeout', None)  # because timeout is in args already
    r = request(url=url, method=method, cookies=cookies, timeout=timeout, verify=False, **keywords)
    _logger.debug('*** Performing %s request %s?%s' % (method, url, urllib.parse.urlencode(keywords['params']) if 'params' in kwargs else ''))
    check_status_code(r)
    check_response(r)
    if load_response:
        if r.text == '':
            raise OBException('Empty response')
        resp_dict = json.loads(r.text)
        return resp_dict
    return r.text


def check_status_code(request):
    r = request
    try:
        r.raise_for_status()
    except HTTPError:
        raise OBException(f'Something goes wrong with request. Status code: {r.status_code}: {r.reason}')


def check_response(request):
    r = request
    if r.text == '':
        raise OBException('Empty response')
    else:
        try:
            resp_dict = json.loads(r.text)
            if resp_dict['status'] in ('error', 'failed'):
                raise OBException(resp_dict['notifications'][0]['msg'])
            else:
                pass
        except (KeyError, ValueError) as e:
            _logger.warning(e)
