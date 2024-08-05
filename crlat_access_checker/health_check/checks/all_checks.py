import json

import requests
from checks.sio_client import SioClient
from checks.utils.exceptions import UnexpectedRedirection, UnexpectedStatusCode, UnexpectedContent
from checks.utils.globals import hosts_description


def check_akamai(host):
    url = 'https://{0}/'.format(host)
    response = requests.get(url, timeout=15)
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
        # exit(0)
    else:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content,
        )


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
    response = requests.post(url, data, timeout=15)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    expected = 'firstName'
    if expected not in response.content:
        raise UnexpectedContent(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            'Expected "{0}" string not found in response:\n{1}'.format(expected, response.content)
        )
    else:
        print 'OK'


def check_cms(host):
    url = 'https://{0}/api/footer-menu'.format(host)
    response = requests.get(url, verify=False, timeout=15)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    else:
        print 'OK'


def check_liveserver(host):
    url = 'https://{0}/push_api.html'.format(host)
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    else:
        print 'OK'


def check_openapi(host):
    sio = SioClient(environment=hosts_description[host]['environment'].lower())
    sio.connect()
    response = sio.process_request('ping')
    sio.disconnect()
    if response['ID'] != 18:
        raise UnexpectedContent(
            host,
            sio.endpointOpenAPI,
            'Unexpected response received'.format(json.dumps(response, indent=2))
        )
    else:
        print 'OK'


def check_siteserver(host):
    url = 'https://{0}/openbet-ssviewer/Common/2.14/HealthCheck'.format(host)
    response = requests.get(url,
                            headers={'Accept': 'application/json'},
                            timeout=15
                            )
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
                # exit(0)
        except Exception:
            raise UnexpectedContent(
                hosts_description[host]['environment'],
                hosts_description[host]['backend'],
                'Element "status": "OK" not found. Content:\n{1}'.format(response.content)
            )


def check_spark(host):
    url = 'https://{0}/api/areas/1'.format(host)
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise UnexpectedStatusCode(
            hosts_description[host]['environment'],
            hosts_description[host]['backend'],
            response.status_code,
            response.content
        )
    else:
        print 'OK'
