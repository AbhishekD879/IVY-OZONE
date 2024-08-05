import requests


def check_if_siteserve_config_not_present(context):
    siteserve_url = context.config.userdata.get('siteserve_url')
    wiremock_url = context.config.userdata.get('wiremock_url')
    resp = requests.get(wiremock_url)
    if len(resp.json().get('mappings')) == 0:
        return True
    for stub in resp.json().get('mappings'):
        if stub.get('response').get('proxyBaseUrl', None) == siteserve_url:
            return False
    return True


def check_if_cms_config_not_present(context):
    cms_url = context.config.userdata.get('cms_url')
    wiremock_url = context.config.userdata.get('wiremock_url')
    resp = requests.get(wiremock_url)
    if len(resp.json().get('mappings')) == 0:
        return True
    for stub in resp.json().get('mappings'):
        if stub.get('response').get('proxyBaseUrl', None) == cms_url:
            return False
    return True


def setup_siteserve_forwarding(context):
    siteserve_url = context.config.userdata.get('siteserve_url')
    wiremock_url = context.config.userdata.get('wiremock_url')
    data = {
        'request': {
            'method': "GET",
            'urlPattern': '/openbet-ssviewer/.*'
        },
        'response': {
            'proxyBaseUrl': siteserve_url
        }
    }
    requests.post(wiremock_url, json=data)


def setup_cms_forwarding(context):
    cms_url = context.config.userdata.get('cms_url')
    wiremock_url = context.config.userdata.get('wiremock_url')
    data = {
        'request': {
            'method': "GET",
            'urlPattern': '/cms/api/.*'
        },
        'response': {
            'proxyBaseUrl': cms_url
        }
    }
    requests.post(wiremock_url, json=data)


def delete_stubs(context):
    wiremock_url = context.config.userdata.get('wiremock_url')
    for stub_id in context.stubs:
        requests.delete(f'{wiremock_url}/{stub_id}')
