from health_check.globals import hosts_description

import requests
from health_check.checks.utils.exceptions import UnexpectedStatusCode


def check(host):
    url = 'https://{0}/push_api.html'.format(host)
    response = requests.get(url)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    else:
        print 'OK'