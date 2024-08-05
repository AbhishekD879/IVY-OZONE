import json
import logging
import typing

import requests
from requests import HTTPError
from requests import models

from .exceptions import InvalidResponseException
from .parsers import ResponseParserBase

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

Verify = typing.TypeVar('Verify', str, bool)


class Request(object):
    """ Request class is a thin wrapper on requests library.
    """
    logger = logging.getLogger('crlat_cms_client')

    def __init__(
            self,
            use_session: bool = False,
            hostname: typing.Optional[str] = None,
            headers: typing.Optional[dict] = None,
            proxies: typing.Optional[dict] = None,
            timeout: int = 5,
            verify: Verify = False,
            validators: list = [],
            parser: ResponseParserBase = None,
    ):

        self._hostname = hostname
        self._timeout = timeout
        self._headers = headers or {}
        self._proxies = proxies or {}
        self._verify = verify

        self._validators = validators
        self._parser = parser

        self._session = None
        if use_session:
            self._session = requests.Session()

    def set_timeout(self, seconds: int = 5) -> 'Request':
        """ Set timeout for every request

        :param seconds: number of seconds
        :returns: self
        """

        self._timeout = seconds

        return self

    @property
    def session(self) -> requests.sessions.Session:
        """ Return session it use_session is set or new session otherwise """

        if self._session:
            return self._session

        with requests.Session() as session:
            return session

    @property
    def headers(self) -> dict:
        """ Return dict containing headers used in every request """

        return self._headers

    def add_headers(self, headers: typing.Dict[str, str]) -> 'Request':
        """ Updates request headers with given dictionary """

        self._headers.update(headers)

        return self

    def remove_headers(self, *names: typing.Iterable[str]) -> 'Request':
        """ Remove a header by name

        :param names: list of header names
        :return: self
        """

        for header_name in names:
            self._headers.pop(header_name, None)

        return self

    @property
    def proxies(self) -> typing.Dict[str, str]:
        """ Returns dict containing used proxies """

        return self._proxies

    def add_proxies(self, proxies: typing.Dict[str, str]) -> 'Request':
        """ Updates request proxies with given dictionary """

        self._proxies.update(proxies)

        return self

    def remove_proxies(self, *names: typing.Iterable[str]) -> 'Request':
        """ Remove a proxy by name

        :param names: list of proxies names
        :return: self
        """

        for proxy_name in names:
            self._proxies.pop(proxy_name, None)

        return self

    def verify_certificate(self, verify: Verify = True) -> 'Request':
        """ Enable or disable certificate verification

            :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.

        """

        self._verify = verify

        return self

    @staticmethod
    def check_status_code(response: requests.models.Response) -> None:
        """ Raise InvalidResponseException if a bad request was made (4XX or 5XX error response)

        :param response: :class:`requests.models.Response` object
        """
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise InvalidResponseException(f'Something went wrong with request. {e}')

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

    def get(self, url, params=None, **kwargs):
        """Sends a GET request.
        :param url: URL for the new request
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string.
        :param **kwargs: Optional arguments that ``Request.send`` takes.
        """

        return self.send('get', url, params=params, **kwargs)

    def delete(self, url, **kwargs):
        """Sends a DELETE request.
        :param url: URL for the new request.
        :param **kwargs: Optional arguments that ``Request.send`` takes.
        """

        return self.send('delete', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        """Sends a POST request.`
        :param url: URL for the new request
        :param data: (optional) Dictionary, list of tuples or bytes to send
            in the request content.
        :param **kwargs: Optional arguments that ``Request.send`` takes.
        """

        return self.send('post', url, data=data, **kwargs)

    def put(self, url, data, **kwargs):
        """Sends a PUT request.`
        :param url: URL for the new request
        :param data: (optional) Dictionary, list of tuples or bytes to send
            in the request content.
        :param **kwargs: Optional arguments that ``Request.send`` takes.
        """

        return self.send('put', url, data=data, **kwargs)
