import json

from health_check.globals import hosts_description

import requests
from health_check.checks.sio_client import SioClient
from health_check.checks.utils.exceptions import *


def open_api_login(env):
    open_api_prod_session = SioClient(environment=env.lower())
    open_api_prod_session.connect()
    session_token_response = open_api_prod_session.process_request(
        'sessionToken',
        userName='ims_tester',
        password='qwerty'
    )
    if session_token_response['ID'] == 31010:
        # there is session token in "terms and conditions" response so we can reassign the response data
        session_token_response = open_api_prod_session.process_request(
            'termsAndConditions',
            termVersionReference=session_token_response['data']['termVersionReference']
        )

    temp_auth_token_response = open_api_prod_session.process_request(
        'token',
        userName=session_token_response['data']['username'],
        sessionToken=session_token_response['data']['sessionToken']
    )

    if temp_auth_token_response['ID'] == 30002:
        return temp_auth_token_response['data']['token']

def check_proxy(host):
    url = 'https://{0}/Proxy/auth/user'.format(host)
    data = json.dumps({'username': 'ims_tester', 'token': open_api_login(hosts_description[host]['environment'])})
    response = requests.post(url, data)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    expected = 'firstName'
    if expected not in response.content :
        raise UnexpectedContent(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            'Expected "{0}" string not found in response:\n{1}'.format(expected, response.content)
        )
    else:
        print 'OK'
