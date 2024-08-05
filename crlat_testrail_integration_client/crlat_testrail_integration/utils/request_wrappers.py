import json
from time import sleep

import requests
from requests import HTTPError
from requests import request

from crlat_testrail_integration.utils.exceptions import TestRailAPIError
from crlat_testrail_integration.utils.log_mngr import setup_custom_logger

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
_logger = setup_custom_logger()


def do_request(url, method='POST', headers=None, data=None, proxies=None, load_response=True, **kwargs):
    keywords = kwargs
    _logger.info('*** Performing %s request %s' % (method, url))
    if data:
        data = json.dumps(data)
    try:
        r = request(url=url, method=method, headers=headers, data=data, proxies=proxies, verify=False, timeout=40, **keywords)
        if not f"{r.status_code}".startswith("2"):
            sleep(10)
            r = request(url=url, method=method, headers=headers, data=data, proxies=proxies, verify=False, timeout=60, **keywords)
    except Exception as e:
        _logger.warning(e)
        sleep(1)
        r = request(url=url, method=method, headers=headers, data=data, proxies=proxies, verify=False, timeout=60, **keywords)
        if not f"{r.status_code}".startswith("2"):
            sleep(10)
            r = request(url=url, method=method, headers=headers, data=data, proxies=proxies, verify=False, timeout=60, **keywords)
    e = check_status_code(r)
    if load_response:
        if r.text == '':
            raise TestRailAPIError('Empty response')
        resp_dict = json.loads(r.text)

        result = resp_dict
    else:
        result = r.text

    if e is not None:
        if result and 'error' in result:
            error = '"' + result['error'] + '"'
        else:
            error = 'No additional error message received'
        raise TestRailAPIError('TestRail API returned HTTP %s (%s)' % (e, error))

    return result


def check_status_code(request):
    r = request
    try:
        r.raise_for_status()
    except HTTPError as e:
        return e
