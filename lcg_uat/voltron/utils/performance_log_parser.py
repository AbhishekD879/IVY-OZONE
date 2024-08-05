import json
from json import JSONDecodeError
import logging

_logger = logging.getLogger(name='voltron_logger')


def parse_web_socket_response_by_id(logs: str, response_id: (int, str), delimiter: str = ':::') -> dict:
    """
    DESCRIPTION: This method allows to get Web Socket response info based on required response ID
    :param logs: All gathered Network responses
    :param response_id: expected response ID
    :param delimiter: two delimiters are present in WS with different types default get 'dict' with delimiter ':::'
    :return: Dictionary which contains all WS response info with expected ID
    """
    data_dict = None
    for log in list(reversed(logs)):
        try:
            data_dict = json.loads(log[1]['message']['message']['params']['response']['payloadData'].split(delimiter, maxsplit=1)[-1])
            if isinstance(data_dict, dict) and str(data_dict['ID']) == str(response_id):
                return data_dict
            elif isinstance(data_dict, list) and data_dict[0] == str(response_id):
                return data_dict[1]
        except (KeyError, JSONDecodeError, TypeError, IndexError):
            continue
    _logger.info(f'Last received data is: "{data_dict}"')
    return {}


def parse_web_socket_response_by_url(logs: str, url: str) -> dict:
    """
    DESCRIPTION: This method allows to get Web Socket response info based on required request
    :param logs: All gathered Network responses
    :param url: expected request URL
    :return: Dictionary which contains all URL request info for expected URL
    """
    for log in list(reversed(logs)):
        try:
            data_dict = log[1]['message']['message']['params']['request']
            request_url = data_dict['url']
            if url == request_url:
                post_data = data_dict.get('postData')
                data_dict['postData'] = json.loads(post_data)
                return data_dict
        except (KeyError, JSONDecodeError, TypeError, IndexError):
            continue
    return {}
