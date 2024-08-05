import abc
import logging
from typing import Any

import requests


class ResponseParserBase(metaclass=abc.ABCMeta):
    """ Base class for response parser. Just after request is made if parser is set
        a response object will be passed to parser parse method. Otherwise response
        object will be returned.
    """
    logger = logging.getLogger('crlat_cms_client')

    @abc.abstractmethod
    def parse(self, response: requests.models.Response) -> None:
        pass


class PlainResponseParser(ResponseParserBase):

    def parse(self, response: requests.models.Response) -> str:
        """ Returns response content as string

        :param response: requests response object
        :return: string
        """
        self.logger.debug(f'Parse response: {response.content}')
        return response.content.decode('utf-8')


class JSONResponseParser(ResponseParserBase):

    _allowed_content_types = ('application/json',)

    def is_allowed(self, response):
        """ Checks if returned content type is allowed to be parsed

        :param response: requests response object
        :return: string
        """
        content_type = response.headers.get('content-type').split(';')[0]
        return content_type in self._allowed_content_types

    def parse(self, response: requests.models.Response) -> Any:
        """ Parse response as json and returns it as a dict.
            Raises ValueError if content is not a valid json

        :param response: requests response object
        :return: dict, list, string or None
        """
        self.logger.debug(f'Parse response: {response.content}')
        if self.is_allowed(response):
            return response.json()
        return response
