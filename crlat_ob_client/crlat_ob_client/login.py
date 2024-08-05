import json
import ssl
from urllib.request import urlopen

import requests
import tenacity
from lxml import html

from crlat_ob_client import BackEndSettings
from crlat_ob_client import get_ob_cookies
from crlat_ob_client import OBException
from crlat_ob_client import set_ob_cookies
from crlat_ob_client.utils.helpers import _logger
from crlat_ob_client.utils.helpers import check_status_code

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass


class OBLogin(object):
    def __init__(self, env, brand, *args, **kwargs):
        self._logger = _logger
        self.env = env
        self.brand = brand if brand else 'bma'
        self.backend = BackEndSettings(backend=env, brand=self.brand)
        self.site = self.backend.ti.general_info.hostname
        self.admin = self.backend.admin.hostname
        account_sharing_hostname = 'https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com'
        response = None
        self.user = None
        self.password = None
        if self.env != 'prod':
            try:
                url = f'{account_sharing_hostname}/get_ob_user/{self.brand}/{self.env}'
                response = requests.get(url, verify=False)
            except Exception as err:
                OBException(f'Error occurred during getting ob account info "{err}"')
            if response is not None and response.status_code in [200, 204]:
                credentials = json.loads(response.content)
                self.user = credentials['username']
                self.password = credentials['password']

    @property
    def site_cookies(self):
        cookies = get_ob_cookies()
        if not cookies:
            self.login_to_backoffice()
        return get_ob_cookies()

    @tenacity.retry(wait=tenacity.wait_fixed(wait=5),
                    stop=tenacity.stop_after_attempt(max_attempt_number=2),
                    retry=tenacity.retry_if_exception(predicate=OBException),
                    reraise=True)
    def login_to_backoffice(self):
        session = requests.Session()
        context = ssl.create_default_context()
        page = html.parse(urlopen(self.site, context=context))
        uid = page.xpath('//input[@name="uid"]')[0].attrib['value']
        params = (
            ('action', 'login::H_redirect_login'),
            ('language', 'en'),
            ('password', self.password),
            ('username', self.user),
            ('uid', uid)
        )
        try:
            r = session.post(self.site, params=params, verify=False)
        except Exception as err:
            raise OBException(f'OB request failed "{err}"')
        print(r.content)
        print(r.status_code)
        check_status_code(r)
        cookies = session.cookies.get_dict()
        print(cookies)
        if not cookies.get('OFFICELOGIN'):
            raise OBException('Error logging in to BackOffice, getting "OFFICELOGIN" cookie failed')
        set_ob_cookies(cookies)
