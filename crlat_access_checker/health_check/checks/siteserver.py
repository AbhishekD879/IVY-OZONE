import json

from health_check.globals import hosts_description

import requests
from health_check.checks.utils.exceptions import *


def check_site_server(host):
    url = 'https://{0}/openbet-ssviewer/Common/2.14/HealthCheck'.format(host)
    response = requests.get(url,
                            headers={'Accept': 'application/json'})
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    else:
        try:
            content = json.loads(response.content)
            status = content['SSResponse']['children'][0]['healthCheck']['status']
            if status.upper() != 'OK':
                raise UnexpectedContent(
                    hosts_description[host]['environment'],
                    hosts_description[host]['backend'],
                    'Status "{0}"!="OK", Content:\n{1}'.format(status, response.content)
                )
            else:
                print 'OK'
                exit(0)
        except Exception as err:
            raise UnexpectedContent(
                hosts_description[host]['environment'],
                hosts_description[host]['backend'],
                'Element "status": "OK" not found. Content:\n{1}'.format(response.content)
            )

