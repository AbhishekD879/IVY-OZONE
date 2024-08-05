import json

from crlat_core.request import models
from crlat_core.request import Request
from crlat_core.request import typing
from crlat_core.request import Verify

from .validators import ProductionRequestValidator
from crlat_cms_client.request.parsers import CMSJSONResponseParser
from crlat_cms_client.utils.settings import get_cms_settings
from tenacity import retry, wait_fixed
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from crlat_core.request import InvalidResponseException
from urllib3.exceptions import ReadTimeoutError

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class CMSAPIRequest(Request):
    def __init__(self, **kwargs):
        parser = kwargs.pop('parser', CMSJSONResponseParser())

        cms_settings = get_cms_settings()
        hostname = kwargs.pop('hostname', cms_settings.config.api_url)
        self.env = cms_settings.config.backend

        use_session = kwargs.pop('use_session', True)
        origin = 'https://sports.coral.co.uk' if 'coral' in cms_settings.config.public_api_url else 'https://sports.ladbrokes.com'
        headers = {'origin': origin,
                   'user-agent': 'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36',
                   'accept': 'application/json',
                   'Content-Type': 'application/json',
                   'sec-fetch-site': 'same-site',
                   'sec-fetch-mode': 'cors',
                   'sec-fetch-dest': 'empty',
                   'authority': origin.replace('https://', ''),
                   'accept-language': 'en-US,en;q=0.9'
                   }

        headers.update(kwargs.pop('headers', {}))
        timeout = kwargs.pop('timeout', 10)

        super(CMSAPIRequest, self).__init__(
            use_session=use_session,
            headers=headers,
            parser=parser,
            validators=[ProductionRequestValidator()],
            hostname=hostname,
            timeout=timeout,
            **kwargs
        )

    def get_credentials(self):
        accounts_sharing_url = 'https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com/'
        url = f'{accounts_sharing_url}get_cms_user/{self.env}'
        account = json.loads(self.get(url=url, parse_response=False).content)
        return account['username'], account['password']

    def login(self) -> 'Request':
        """ Log user in with given username and password

        :param username: username
        :param password: password
        """
        username, password = self.get_credentials()
        data = json.dumps({'username': username, 'password': password})
        login_token = self.post(url='login', data=data)
        if 'token' not in login_token:
            raise Exception('User is not logged in')
        self.add_headers({'Authorization': login_token['token']})

        return self

    def is_logged_in(self):
        """ Checks if Authorization token is included in the headers. This however doesn't
            guarantee that token is still valid
        """
        return 'Authorization' in self.headers

    @retry(stop=stop_after_attempt(2),
           retry=retry_if_exception_type((InvalidResponseException, ReadTimeoutError)),
           wait=wait_fixed(wait=1), reraise=True)
    def send(self,
             method: str,
             url: str,
             params: typing.Any = None,
             data: typing.Any = None,
             extra_headers: typing.Dict[str, str] = {},
             extra_proxies: typing.Dict[str, str] = {},
             cookies: typing.Dict[str, str] = {},
             timeout: int = False,
             verify: Verify = False,
             parse_response: bool = True
             ):
        """Constructs and sends a :class:`Request <Request>`.
        :param parse_response: (optional) If needed to parse response
        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param extra_headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param extra_proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param cookies: (optional) Dictionary contains explicitly passed cookies to request.
        :param timeout: (optional) How many seconds to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
        :type timeout: int
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
        """
        if self._hostname:
            url = urljoin(self._hostname, url)

        self.logger.debug(f'*** Prepare {method.upper()} request ***')
        self.logger.debug(f'Request url: {url}')

        headers = self._headers.copy()
        headers.update(extra_headers)

        if get_cms_settings().config.public_api_url in url:
            if headers.get('Authorization'):
                del headers['Authorization']
        elif 'login' in url or 'accounts-sharing' in url:
            pass
        else:
            if not self.is_logged_in():
                self.login()
                headers = self._headers.copy()
                headers.update(extra_headers)

        self.logger.debug(f'Request headers: {json.dumps(headers, indent=2)}')

        proxies = self._proxies.copy()
        proxies.update(extra_proxies)
        self.logger.debug(f'Request proxies: {json.dumps(proxies, indent=2)}')

        timeout = timeout or self._timeout
        self.logger.debug(f'Request timeout: {timeout}')

        verify = self._verify or verify
        self.logger.debug(f'Request verify: {verify}')

        session = self.session

        req = models.Request(
            method=method.upper(),
            url=url,
            headers=headers,
            data=data or {},
            params=params or {},
            cookies=cookies or {}
        )

        prep = session.prepare_request(req)

        proxies = proxies or {}

        settings = session.merge_environment_settings(
            prep.url, proxies, None, verify, None
        )

        # Send the request.
        send_kwargs = {
            'timeout': timeout,
            'allow_redirects': True,
        }

        send_kwargs.update(settings)

        self.logger.debug('*** Validate prepared request ***')
        for validator in self._validators:
            validator.validate(prep, session)

        self.logger.debug('*** Send request ***')
        resp = session.send(
            prep,
            **send_kwargs
        )

        self.logger.debug('*** Check response code ***')
        self.check_status_code(resp)

        self.logger.debug(f'*** {resp.status_code} response received ***')
        return self._parser.parse(resp) if self._parser and parse_response else resp
