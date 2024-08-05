

import requests
from health_check.checks.utils.exceptions import *
from health_check.checks.utils.globals import hosts_description


def check_akamai(host):
    url = 'https://{0}/'.format(host)
    response = requests.get(url)
    if response.status_code == 200:
        if host not in response.url:
            raise UnexpectedRedirection(
                hosts_description[host]['environment'],
                hosts_description[host]['backend'],
                response.status_code,
                'Request to "%s" redirected to "%s"' % (url, response.url)
            )
        else:
            print 'OK'
        exit(0)
    else:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content,
        )
