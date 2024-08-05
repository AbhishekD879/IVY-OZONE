from crlat_core.request.parsers import JSONResponseParser
import requests
from typing import Any


class CMSJSONResponseParser(JSONResponseParser):

    _allowed_content_types = ('application/json',
                              'text/plain',
                              'binary/octet-stream')

    def parse(self, response: requests.models.Response) -> Any:
        """ Parse response as json and returns it as a dict.

        :param response: requests response object
        :return: dict, list, string or None
        """
        # self.logger.debug(f'Parse response: {response.content}')
        if self.is_allowed(response):
            try:
                parsed_response = response.json()
            except Exception as e:
                self.logger.warning(f'Failed to parse response into JSON: {e}')
                parsed_response = response
        else:
            parsed_response = response
        return parsed_response

