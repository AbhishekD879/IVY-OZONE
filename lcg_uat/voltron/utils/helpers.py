import json
import logging
import random
import re
import string
from json import JSONDecodeError

import requests
from faker import Faker
from gevent.subprocess import PIPE
from gevent.subprocess import Popen
from requests import HTTPError
from requests import request
from requests import RequestException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from voltron.pages.shared import get_device, get_cms_config
from voltron.pages.shared import get_driver
from voltron.pages.shared import get_is_driver_in_iframe
from voltron.pages.shared import set_driver_in_iframe
from voltron.pages.shared import set_driver_in_main_page
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.device_exception import DeviceException
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

_logger = logging.getLogger(name='voltron_logger')


def parse_pattern(pattern_data='', pattern_values={}):
    names = re.findall(r'{([a-zA-Z0-9]+)}', pattern_data)
    for name in names:
        try:
            pattern_data = pattern_data.replace('{%s}' % name, pattern_values[name])
        except NameError:
            raise VoltronException(f'Error building sector from pattern, Value argument must be missed for "{name}"')
        except Exception as err:
            raise VoltronException(f'Unknown exception parsing selector pattern: "{err}"')
    _logger.debug(f'Parsed selector pattern "{pattern_data}"')
    return pattern_data


def parse_selector(selector=''):
    by = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'id': By.ID,
        'name': By.NAME,
        'tag': By.TAG_NAME,
    }
    if not isinstance(selector, str):
        raise GeneralException(f'Selector should be a string value got "{selector}" with type "{type(selector)}"')
    matcher = re.match(r'^([a-z]+)=(.+)', selector)
    # TODO: allow whitespace characters in xpath, e.g.: xpath = .//*
    if matcher is not None and matcher.lastindex == 2:
        sector_type = matcher.group(1)
        selector_string = matcher.group(2)
        if sector_type in by.keys():
            return (by[sector_type], selector_string)
        else:
            raise GeneralException(f'Unknown selector type "{sector_type}"')
    else:
        raise GeneralException(f"Selector doesn't match pattern 'xpath=//*', given '{selector}'")


def find_element(selector, context=None, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=15):
    context = context if context else get_driver()
    (by, val) = parse_selector(selector)
    try:
        element = context.find_element(by=by, value=val)
    except InvalidSelectorException as e:
        raise GeneralException(message=e.msg)
    except (NoSuchElementException, WebDriverException):
        return wait_for_result(lambda: context.find_element(by=by, value=val),
                               name=f'Waiting for web element to exist by selector {selector}',
                               bypass_exceptions=bypass_exceptions,
                               timeout=timeout
                               )
    return element


def find_elements(selector, context=None, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=15):
    context = context if context else get_driver()
    (by, val) = parse_selector(selector)
    try:
        elements = context.find_elements(by=by, value=val)
    except InvalidSelectorException as e:
        raise VoltronException(message=e.msg)
    except WebDriverException:
        elements = wait_for_result(lambda: context.find_elements(by=by, value=val),
                                   name=f'Waiting for web elements to exist by selector {selector}',
                                   bypass_exceptions=bypass_exceptions,
                                   timeout=timeout
                                   )
    if not elements:
        elements = wait_for_result(lambda: context.find_elements(by=by, value=val),
                                   name=f'Waiting for web elements to exist by selector {selector}',
                                   bypass_exceptions=bypass_exceptions,
                                   timeout=timeout
                                   )
    return [] if elements is None else elements


def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_name():
    fake = Faker()
    name = fake.city()
    return name


def cleanhtml(raw_html, clean_buttons=False):
    if '<!--' in raw_html:
        raw_html = re.sub(r"\n<!--(.|\s|\n)*?-->", '', raw_html)  # to remove commented text
    if clean_buttons:
        cleanbtns = re.compile('<a class="btn.*">.*</a>')
    cleantags = re.compile('<.*?>')
    if clean_buttons:
        cleantext = re.sub(cleanbtns, '', raw_html)
        cleantext = re.sub(cleantags, '', cleantext)
    else:
        cleantext = re.sub(cleantags, '', raw_html)
    text = cleantext.replace('&nbsp;', ' ')
    text = text.replace('Â', '')
    text = text.replace('&ndash;', '–')
    text = text.replace('&amp;', '&')
    text = text.replace('&pound;', '£')
    return text


def normalize_name(name: str) -> str:
    """
    :param name: str event/market name
    :return: string with removed all unnecessary spaces/pipes/(BG)/(FT)/(HT) etc.
    """
    text = name.replace('(BG)', '')
    text = text.replace('(FT)', '')
    text = text.replace('(HT)', '')
    text = text.replace(' FT', '')
    text = text.replace(' HT', '')
    text = text.replace('|', '')
    text = text.replace('   ', ' ')
    text = text.replace('  ', ' ')
    text = re.sub(r' [\d]-[\d] ', ' v ', text)
    text = text.replace(' vs ', ' v ').strip()
    text = text.replace('(Bo1)', '')
    text = text.replace('(BO1)', '')
    text = text.strip()
    _logger.info(f'*** Initial text "{name}" normalized to "{text}"')
    return text


def convert_weight_pounds_to_stones(pounds):
    pounds = int(pounds)
    st = int(pounds / 14)
    lb = pounds - (st * 14)
    return st, lb


def do_request(url, method='POST', proxies=None, load_response=True, **kwargs):
    keywords = kwargs
    keyword_params = kwargs.get('params', '')
    _logger.debug('*** Performing %s request %s%s'
                  % (method,
                     url,
                     ('?' + '&'.join(['%s=%s' % (k, v) for k, v in keyword_params])) if len(keyword_params) else '')
                  )
    r = request(url=url, method=method, proxies=proxies, verify=False, timeout=5, **keywords)
    check_status_code(r)
    if load_response:
        if r.text == '':
            raise RequestException('Empty response')
        resp_dict = json.loads(r.text)
        return resp_dict
    return r.text


def check_status_code(request):
    r = request
    try:
        r.raise_for_status()
    except HTTPError as e:
        raise HTTPError('Something goes wrong with request. %s' % e)


def check_response(request):
    r = request
    resp_dict = None
    if r.text == '':
        raise RequestException('Empty response')
    else:
        try:
            resp_dict = json.loads(r.text)
            if resp_dict['status'] == 'error':
                raise RequestException(resp_dict['notifications'][0]['msg'])
        except (KeyError, ValueError, TypeError) as e:
            _logger.warning(e)
    return resp_dict


def get_device_uuid_from_xcode(device_name):
    terminal_command = 'xcrun simctl list | grep "%s ("' % device_name
    # e.g. xcrun simctl list | grep 'iPhone 7 ('  extra bracket is needed to cut off devices with 'Plus' in name
    cmd = Popen(terminal_command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    output, error = cmd.communicate()
    if cmd.returncode != 0:
        error = error if error else 'Empty command output'
        raise DeviceException('Error while executing command "%s". Errorcode: "%s", message: "%s"' % (terminal_command, cmd.returncode, error))
    pattern = r'^%s \(([A-Z0-9-]+)\) \(\w+\)' % device_name
    # e.g 'iPhone 7 (C78D845C-69F7-4A39-A8DE-A042A0F45113) (Shutdown)'
    device_uuid = next((re.match(pattern, line.strip()).group(1) for line in output.split('\n') if re.match(pattern, line.strip())), None)
    if not device_uuid:
        raise DeviceException('Cannot find UUID for %s' % device_name)
    _logger.info('*** Found UUID "%s" for "%s"' % (device_uuid, device_name))
    return device_uuid


def get_featured_structure_changed(delimiter='42'):
    """
    wss://featured-sports
    :param delimiter:
    :return:
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            if 'FEATURED_STRUCTURE_CHANGED' in entry[1]['message']['message']['params']['response']['payloadData']:
                return json.loads('[' + entry[1]['message']['message']['params']['response']['payloadData'].split(delimiter + '[')[1])[1]
        except (KeyError, IndexError, AttributeError):
            continue
    return {}


def get_featured_event_hub_by_event_id(event_id: str, index_number: str, delimiter='42'):
    """
    wss://featured-sports
    :param delimiter: WS messages delimited, string
    :param index_number: index number of event hub created in cms
    :param event_id: id of the event
    :return: list that has events with properties
    """
    logs = get_device().get_performance_log()
    delimit = delimiter + '/' + 'h' + str(index_number) + ','
    for entry in logs[::-1]:
        try:
            if event_id in entry[1]['message']['message']['params']['response']['payloadData']:
                return json.loads(entry[1]['message']['message']['params']['response']['payloadData'].split(delimit)[1])[1]
        except (KeyError, IndexError, AttributeError):
            continue
    return {}



def get_inplay_event_initial_data(delimiter: str = '42', category_id: str = 16, **kwargs) -> list:
    """
    Gets STREAM_EVENT (for Watch Live tab) / LIVE EVENT(Live Now section) / UPCOMING EVENT (Upcoming section) response on inplay page
    :param delimiter: WS messages delimited, string
    :param category_id: id of category, string
    :return: list that has events with properties
    """
    messages = []
    logs = get_device().get_performance_log()
    search_event_id = int(kwargs.get('event_id', 0))
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if 'IN_PLAY_SPORT_TYPE' in payload_data and payload_data.startswith(delimiter):
                sport_info = json.loads(payload_data[len(delimiter):])[0]
                sport_info_split = sport_info.split('::')  # "IN_PLAY_SPORT_TYPE::6::STREAM_EVENT::136"
                category_id_resp = sport_info_split[1]
                if category_id_resp == category_id:
                    messages.extend(json.loads(payload_data[len(delimiter):])[1])
                    if search_event_id:
                        for message in messages:
                            if message['id'] == search_event_id:
                                messages = [message, ]
                                break
        except (KeyError, IndexError, AttributeError, TypeError):
            continue
    return messages


def get_inplay_sports_by_section(delimiter: (str, int) = '42', type='UPCOMING_STREAM_EVENT') -> dict:
    """
    Gets STREAM_EVENT (for Watch Live tab) / LIVE EVENT(Live Now section) / UPCOMING EVENT (Upcoming section) response on inplay page
    :param delimiter: WS messages delimited, string
    :param category_id: id of category, string
    :return: list that has events with properties
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if 'IN_PLAY_SPORTS' in payload_data and type in payload_data and payload_data.startswith(delimiter):
                message = json.loads(payload_data[len(str(delimiter)):])[1]
                return message
        except (KeyError, IndexError, AttributeError, TypeError, JSONDecodeError):
            continue
    return {}


def get_inplay_sports_ribbon(delimiter: (str, int) = '42') -> dict:
    """
    Gets INPLAY_SPORTS_RIBBON response on inplay page
    :return: dict with sport tabs and their properties
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if '"INPLAY_SPORTS_RIBBON"' in payload_data or 'IN_PLAY_SPORTS_RIBBON_CHANGED' in payload_data and 'subscribe' not in payload_data and \
                    payload_data.startswith(str(delimiter)):
                message = json.loads(payload_data[len(str(delimiter)):])[1]
                return message['items']
        except (KeyError, IndexError, AttributeError, TypeError, JSONDecodeError):
            continue
    return {}


def wait_for_category_in_inplay_sports_ribbon(category_id: (str, int),
                                              delimiter: (str, int) = '42',
                                              timeout: (int, float) = 60,
                                              poll_interval: (int, float) = 2,
                                              raise_exceptions: bool = True) -> bool:
    """
    Waiter for get_inplay_sports_ribbon

    :param category_id:
    :param delimiter:
    :param timeout:
    :param poll_interval:
    :param raise_exceptions:
    :return:
    """
    result = wait_for_result(lambda: category_id in [category.get('categoryId') for category
                                                     in get_inplay_sports_ribbon(delimiter=delimiter)],
                             name=f'Category "{category_id}" to appear in WS',
                             timeout=timeout,
                             poll_interval=poll_interval)
    if not result and raise_exceptions:
        raise ThirdPartyDataException(f'Category "{category_id}"  is not present in WS')
    return result


def get_score_update_from_inplay_ms(delimiter: str, resp_type: str, event_id: str, score_type: str, **kwargs) -> dict:
    search_score = kwargs.get('score', '')
    search_team = kwargs.get('team', '').upper()
    logs = get_device().get_performance_log()

    data_list = []
    for log in logs[::-1]:
        try:
            data_dict = json.loads(log[1]['message']['message']['params']['response']['payloadData'].split(delimiter, maxsplit=1)[-1])
            if isinstance(data_dict, dict) and str(data_dict['ID']) == str(event_id):
                data_list.append(data_dict)
            elif isinstance(data_dict, list) and data_dict[0] == str(event_id):
                data_list.append(data_dict[1])
        except (KeyError, JSONDecodeError, TypeError, IndexError):
            continue

    for result in data_list:
        if result['type'] == resp_type and search_team:
            for entry in result['event']['scoreboard'][score_type]:
                if (entry['role_code'] == search_team) and not search_score:
                    _logger.debug(f'*** SCRBD update: Team is {entry["role_code"]}')
                    return result
                if (entry['role_code'] == search_team) and (entry['value'] == search_score):
                    _logger.debug(f'*** *** SCRBD update: Score is {entry["value"]}')
                    return result
    return {}


def get_inplay_sports_ribbon_home_page(delimiter: (str, int) = '42') -> dict:
    """
    Method to get data from INPLAY_LS_SPORTS_RIBBON & IN_PLAY_LS_SPORTS_RIBBON_CHANGED messages

    WS connection endpoint: wss://inplay-publisher
    Present on pages:
        - In-Play and Live Stream module on Homepage (desktop)
        -
    :return: dict with sport tabs and and their properties
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if '"INPLAY_LS_SPORTS_RIBBON"' in payload_data or 'IN_PLAY_LS_SPORTS_RIBBON_CHANGED' \
                    in payload_data and 'subscribe' not in payload_data and payload_data.startswith(str(delimiter)):
                message = json.loads(payload_data[len(str(delimiter)):])[1]
                return message['items']
        except (KeyError, IndexError, AttributeError):
            continue
    return {}


def wait_for_category_in_inplay_sports_ribbon_home_page(category_id: (str, int),
                                                        delimiter: (str, int) = '42',
                                                        timeout: (int, float) = 60,
                                                        poll_interval: (int, float) = 2,
                                                        raise_exceptions: bool = True) -> bool:
    """
    Waiter for get_inplay_sports_ribbon_home_page

    :param category_id:
    :param delimiter:
    :param timeout:
    :param poll_interval:
    :param raise_exceptions:
    :return:
    """
    result = wait_for_result(lambda: int(category_id) in [category.get('categoryId') for category
                                                          in get_inplay_sports_ribbon_home_page(delimiter=delimiter)],
                             name=f'Category "{category_id}" to appear in WS',
                             timeout=timeout,
                             poll_interval=poll_interval)
    if not result and raise_exceptions:
        raise ThirdPartyDataException(f'Category "{category_id}"  is not present in WS')
    return result


def get_live_updates_for_event_on_featured_ms(event_id, delimiter='42/0,', **kwargs):
    price = kwargs.get('price')
    if price:
        price_num, price_den = price.split('/')
    selection_id = kwargs.get('selection_id', '')

    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if 'FEATURED_STRUCTURE_CHANGED' not in payload_data and event_id in payload_data:
                message_split = re.split(r'\d+/\d,(\d+)?', payload_data)
                message_split_filtered = list(filter(None, message_split))
                message = json.loads(message_split_filtered[0])[1]
                if price:
                    if event_id == str(message['event']['eventId']) and message['type'] == 'PRICE' \
                            and str(message['event']['market']['outcome']['outcomeId']) == selection_id \
                            and str(message['event']['market']['outcome']['price']['lp_num']) == price_num \
                            and str(message['event']['market']['outcome']['price']['lp_den']) == price_den:

                        _logger.info(f'*** {payload_data}')
                        return message
                else:
                    if event_id == str(message['event']['eventId']) and message['type'] == 'PRICE' \
                            and str(message['event']['market']['outcome']['outcomeId']) == selection_id:
                        return message

        except (KeyError, IndexError, AttributeError, TypeError):
            continue


def get_live_serve_updates(delimiter='42', **kwargs):
    event_id = kwargs.get('event_id')
    selection_id = kwargs.get('selection_id')
    market_id = kwargs.get('market_id')
    price = kwargs.get('price')
    preserve_option = kwargs.get('preserve')
    sub_channel_types = ['sPRICE']
    if price:
        price_num, price_den = price.split('/')
    multi_update = kwargs.get('multi_update')
    if multi_update:
        sub_channel_types.append('sSELCN')
    search_param = None
    if event_id:
        event_id_len = len(event_id)
        difference = 10 - event_id_len  # if count is less than 10, it should be filled by '0' at the beginning of ID
        search_param = f'sEVENT{"0"*difference}{event_id}'
    elif selection_id:
        search_param = f'sSELCN0{selection_id}'
        sub_channel_types.append('sSELCN')
    elif market_id:
        search_param = f'sEVMKT0{market_id}'
    if preserve_option or preserve_option is None:
        logs = get_device().get_performance_log()
    else:
        logs = get_device().get_performance_log(preserve=False)
    _logger.debug(f'*** Found {len(logs)} logs')
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if search_param in payload_data:
                message = json.loads(payload_data.split(delimiter, maxsplit=1)[1])[1]
                if message['type'] == 'MESSAGE':
                    if price:
                        if selection_id and selection_id.lstrip('0') == str(message['channel']['id']) \
                                and message['subChannel']['type'] in sub_channel_types \
                                and str(message['message']['lp_num']) == price_num \
                                and str(message['message']['lp_den']) == price_den:
                            _logger.info(f'*** {message}')
                            return message
                    else:
                        if selection_id and selection_id.lstrip('0') == str(message['channel']['id']) and message['subChannel']['type'] in sub_channel_types:
                            _logger.info(f'*** {message}')
                            return message
                        if event_id or market_id:
                            message = json.loads(payload_data.split(delimiter)[1])
                            if message[0] == search_param:
                                return message
        except (KeyError, IndexError, AttributeError, JSONDecodeError):
            continue


def get_updated_total_inplay_events_number(delimiter='42'):
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if 'InplayModule' in payload_data and 'FEATURED_STRUCTURE_CHANGED' not in payload_data:
                return json.loads('[' + payload_data.split(delimiter + '[')[1])[1]['totalEvents']
        except KeyError:
            continue


def get_inplay_ls_structure(delimiter: (int, str) = '42') -> dict:
    """
    Method to get data from INPLAY_LS_STRUCTURE & IN_PLAY_LS_STRUCTURE_CHANGED messages

    WS connection endpoint: wss://inplay-publisher
    Present on pages:
        - /in-play/watchlive
        - /home/live-stream
        - /live-stream
        -
    :param delimiter:
    :return:
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if '"INPLAY_LS_STRUCTURE"' in payload_data or 'IN_PLAY_LS_STRUCTURE_CHANGED' in payload_data \
                    and 'subscribe' not in payload_data:
                message = payload_data.split(str(delimiter), maxsplit=1)[1]
                return json.loads(message)[1]
        except KeyError:
            continue
    return {}


def wait_for_category_in_inplay_ls_structure(category_id: (str, int),
                                             delimiter: (str, int) = '42',
                                             timeout: (int, float) = 60,
                                             poll_interval: (int, float) = 2,
                                             raise_exceptions: bool = True) -> bool:
    """
    Waiter for get_inplay_ls_structure

    :param category_id:
    :param delimiter:
    :param timeout:
    :param poll_interval:
    :param raise_exceptions:
    :return:
    """
    result = wait_for_result(lambda: int(category_id) in [category.get('categoryId') for category
                                                          in get_inplay_ls_structure(delimiter=delimiter).get('liveStream', {}).get('eventsBySports', [])],
                             name=f'Category "{category_id}" to appear in WS',
                             timeout=timeout,
                             poll_interval=poll_interval)
    if not result and raise_exceptions:
        raise ThirdPartyDataException(f'Category "{category_id}"  is not present in WS')
    return result


def get_inplay_structure(delimiter: (int, str) = '42'):
    """
    Method to get data from INPLAY_STRUCTURE & IN_PLAY_STRUCTURE_CHANGED messages

    WS connection endpoint: wss://inplay-publisher
    Present on pages:
        - /home/in-play
        -
    :param delimiter:
    :return:
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if '"INPLAY_STRUCTURE"' in payload_data or 'IN_PLAY_STRUCTURE_CHANGED' in payload_data \
                    and 'subscribe' not in payload_data:
                message = payload_data.split(str(delimiter), maxsplit=1)[1]
                return json.loads(message)[1]
        except KeyError:
            continue
    return {}

def get_inplay_sport_by_category(delimiter: (int, str) = '42',category_id = 16):
    """
    Method to get data from
    "IN_PLAY_SPORTS::{category_id}::LIVE_EVENT" messages

    WS connection endpoint: wss://inplay-publisher
    Present on pages:
        - /home/in-play
        -
    :param delimiter:
    :return:
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if f'"IN_PLAY_SPORTS::{category_id}::LIVE_EVENT"' in payload_data \
                    and 'subscribe' not in payload_data:
                message = payload_data.split(str(delimiter), maxsplit=1)[1]
                return json.loads(message)[1]
        except KeyError:
            continue
    return {}

def get_live_stream_sport_by_category(delimiter: (int, str) = '42',category_id = 16):
    """
    Method to get data from
    "IN_PLAY_SPORTS::{category_id}::STREAM_EVENT" messages
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if f'"IN_PLAY_SPORTS::{category_id}::STREAM_EVENT"' in payload_data \
                    and 'subscribe' not in payload_data:
                message = payload_data.split(str(delimiter), maxsplit=1)[1]
                return json.loads(message)[1]
        except KeyError:
            continue
    return {}

def wait_for_category_in_inplay_structure(category_id: (str, int),
                                          delimiter: (str, int) = '42',
                                          section: str = 'livenow',
                                          timeout: (int, float) = 60,
                                          poll_interval: (int, float) = 2,
                                          raise_exceptions: bool = True) -> bool:
    """
    Waiter for get_inplay_structure

    :param category_id:
    :param delimiter:
    :param section:
    :param timeout:
    :param poll_interval:
    :param raise_exceptions:
    :return:
    """
    result = wait_for_result(lambda: int(category_id) in [category.get('categoryId')
                                                          for category
                                                          in get_inplay_structure(delimiter=delimiter).get(section, {}).get('eventsBySports', [])],
                             name=f'Category "{category_id}" to appear in WS',
                             timeout=timeout,
                             poll_interval=poll_interval)
    if not result and raise_exceptions:
        raise ThirdPartyDataException(f'Category "{category_id}"  is not present in WS')
    return result


def get_in_play_module_from_ws(delimiter='42', timeout=3) -> dict:
    """
    WS connection endpoint: wss://featured-sports

    Present on pages:
        - Every page with In-Play module from Featured MS
        -
    Gets part of FEATURED_STRUCTURE_CHANGED response with all data related to inplay module.
    :return:
    """
    resp = wait_for_result(lambda: get_featured_structure_changed(delimiter=delimiter),
                           timeout=timeout,
                           name='Wait to response to be not empty')
    modules = resp.get('modules', [])
    for module in modules:
        if module['@type'] == 'InplayModule':
            return module
    return {}


def get_modules_from_ws(category_id: (str, int), delimiter: str = '42', timeout: int = 3) -> dict:
    """
    WS connection endpoint: wss://featured-sports

    Present on Landing pages
    Gets all FEATURED_STRUCTURE_CHANGED response
    :param delimiter: WS delimiter
    :return: list with modules
    """
    # delimiter_ = f'{delimiter}/{category_id},'
    resp = wait_for_result(lambda: get_featured_structure_changed(delimiter=delimiter),
                           timeout=timeout,
                           name='Wait to response to be not empty')
    return resp.get('modules', [])


def get_racing_module_from_ws(delimiter: str = '42', category_id: (str, int) = 21, type: str = 'RacingModule', name: str = 'UIR', timeout: int = 3) -> dict:
    """
    WS connection endpoint: wss://featured-sports

    Present on Horse Racing and Greyhound Landing pages
    Gets part of FEATURED_STRUCTURE_CHANGED response with all data related to RacingModule.
    :param delimiter: WS delimiter
    :param type: type of message, RacingModuleConfig in this case
    :param name: internal name of module, UIR - UR&IRE Races, LVR - Ladbrokes Legends, IR - International Races, ITC - Int Tote, VRC - Virtual Races
    :return: dict with requested module
    """
    modules = get_modules_from_ws(delimiter=delimiter, category_id=category_id)
    for module in modules:
        if module.get('@type', '') == type and module.get('data', {})[0].get('name', '') == name:
            return module
    return {}


def wait_for_category_in_inplay_module_from_ws(category_id, delimiter='42', timeout=60, poll_interval=2, raise_exceptions=True) -> bool:
    """
    Waiter for get_in_play_module_from_ws above

    :param category_id:
    :param delimiter:
    :param timeout:
    :param poll_interval:
    :param raise_exceptions:
    :return:
    """
    result = wait_for_result(lambda: int(category_id) in [category.get('categoryId')
                                                          for category in get_in_play_module_from_ws(timeout=0,
                                                                                                     delimiter=delimiter).get('data', {})],
                             name=f'Category "{category_id}" to appear in In-Play module',
                             timeout=timeout,
                             poll_interval=poll_interval)

    if not result and raise_exceptions:
        raise ThirdPartyDataException(f'Category "{category_id}" is not present in WS for In-Play module')
    return result


def get_expected_inplay_events_order(delimiter='42'):
    """
    Looks through WS response and figures out what event order is expected. Applicable for InplayModule only.
    :return: list of event names
    """
    inplay_module = get_in_play_module_from_ws(delimiter)

    inplay_data = inplay_module['data']
    inplay_sports = []  # Like Football, Baseball, Tennis etc
    inplay_sports_classes = []  # Like English Premier League, English Football Cup, Greece Football Cup etc
    inplay_sports_events = []  # Like England Premier League events

    # Sorting sports
    for sport_segment in inplay_data:
        if sport_segment.get('displayOrder'):
            inplay_sports.append((sport_segment, sport_segment['displayOrder']))
    inplay_sports = sorted(inplay_sports, key=lambda x: x[1])

    # Sorting classes within each sport
    for inplay_sport in inplay_sports:
        sports_classes = inplay_sport[0]['eventsByTypeName']
        ip_sports_classes = []
        for sport_class in sports_classes:
            ip_sports_classes.append((sport_class, sport_class['classDisplayOrder'], sport_class['typeDisplayOrder']))
        ip_sports_classes = sorted(ip_sports_classes, key=lambda x: (x[1], x[2]))
        inplay_sports_classes += ip_sports_classes

    # Sorting events within each type
    for sport_type in inplay_sports_classes:
        ip_sports_events = []
        for event in sport_type[0]['events']:
            if re.search(r'\d+-\d+', event['name']):
                score = re.search(r'\d+-\d+', event['name']).group()
                ip_sports_events.append((event['startTime'], event['displayOrder'], normalize_name(event['name'].replace(score, 'v'))))
            else:
                ip_sports_events.append((event['startTime'], event['displayOrder'], normalize_name(event['name'])))
        inplay_sports_events += [event[2] for event in sorted(ip_sports_events, key=lambda x: (x[0], x[1], x[2]))]

    return inplay_sports_events


def get_web_socket_response_by_id_from_live_serve(web_socket_id: str, delimiter: str = '42'):
    """
    DESCRIPTION: This method allows to get Web Socket response info based on required web_socket_id from live serve
    :param web_socket_id: desired web_socket_id
    :param delimiter: default delimiter 42 for live serve
    :return: Dictionary which contains all WS response info for expected ID
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if payload_data.startswith(delimiter):
                message = json.loads(payload_data.split(delimiter)[1])
                if message[0] == web_socket_id:
                    return message[1]['data']
        except (KeyError, IndexError, AttributeError, JSONDecodeError):
            continue


def get_response_url(self, url):
    """
    Get the complete URL from the performance logs matching the provided URL.
    :param url: The URL to search for in the performance logs.
    :return: The complete URL if found, else None.
    """
    perflog = self.device.get_performance_log()
    for log in reversed(perflog):
        try:
            data_dict = log[1]['message']['message']['params']['request']
            request_url = data_dict['url']
            if url in request_url:
                return request_url
        except (KeyError, JSONDecodeError, TypeError, IndexError):
            continue
    return None


def get_status_code_of_url(url=None, endpoint_url=None):
    """
    Retrieve the status code of a URL or an endpoint URL from the performance log.

    Args:
        url (str, optional): The exact URL to match.
        endpoint_url (str, optional): Part of the URL to match.

    Returns:
        int or None: The status code of the matched URL, or None if not found.
    """
    status_code = None
    perflog = get_device().get_performance_log()
    for log in reversed(perflog):
        try:
            data_dict = log[1]['message']['message']['params']['response']
            if (url and url == data_dict['url']) or (endpoint_url and endpoint_url in data_dict['url']):
                status_code = data_dict['status']
                break
        except (IndexError, KeyError):
            continue
    return status_code


def get_matching_response_url(self, urls):
    """
    Retrieve the URL from the performance logs that matches all provided URLs.
    Args: urls (list): A list of URLs to match against in the performance logs..
    Returns: str or None: The URL from the performance logs that matches all provided URLs, or None if no match is found.
    """
    perflog = self.device.get_performance_log()
    for log in reversed(perflog):
        try:
            data_dict = log[1]['message']['message']['params']['request']
            request_url = data_dict['url']
            if all(url in request_url for url in urls):
                return request_url
        except (KeyError, JSONDecodeError, TypeError, IndexError):
            continue
    return None

def perform_offset_mouse_click(x=200, y=200):
    """
    Moving the mouse to an offset from current mouse position and click
    :param x: offset to move to, as a positive or negative integer.
    :param y: offset to move to, as a positive or negative integer.
    """
    ActionChains(get_driver()).move_by_offset(x, y).click().perform()


def get_active_selector(selectors: list, context=None, timeout: int = 5):
    def checker():
        for selector in selectors:
            if find_elements(selector=selector, context=context, timeout=0):
                _logger.debug(f'*** Found active selector "{selector}"')
                return selector

    return wait_for_result(lambda: checker(),
                           name=f'Find any available selector from "{selectors}"',
                           timeout=timeout)


def switch_to_iframe(iframe_selector: str, timeout: int = 5):
    drv = get_driver()

    if not get_is_driver_in_iframe():
        iframe_we = find_element(selector=iframe_selector, timeout=timeout)
        if not iframe_we:
            raise VoltronException(f'Iframe navigation failure! Can not find iframe "{iframe_selector}"')
        _logger.debug(f'*** Switching to "{iframe_selector}" iframe')
        drv.switch_to.frame(iframe_we)
        set_driver_in_iframe()
    else:
        _logger.debug(f'*** Skipping switch to "{iframe_selector}" iframe')

    return drv


def switch_to_main_page():
    if get_is_driver_in_iframe():
        _logger.debug(f'*** Switching to default content')
        drv = get_driver()
        drv.switch_to.default_content()
        set_driver_in_main_page()
    else:
        _logger.debug(f'*** Skipping switch to default content')


def execute_in_iframe(_iframe, timeout):
    def iframe_handler(func):
        def executor(self, *args, **kwargs):
            switch_to_iframe(_iframe, timeout)

            result = func(self, *args, **kwargs)

            switch_to_main_page()

            return result
        return executor
    return iframe_handler


def hide_number(number: str):
    return 'x' * 4 + ' ' + 'x' * 4 + ' ' + 'x' * 4 + ' ' + number[12:]


_has_betslip_animation = None


def get_betslip_animation_status():
    global _has_betslip_animation
    if _has_betslip_animation is None:
        cms = get_cms_config()
        sys_config = cms.get_initial_data(cached=True).get('systemConfiguration', {})
        if not sys_config:
            raise CmsClientException('CMS System configuration is empty')
        generals_sys_config = sys_config.get('Generals', {})
        if not generals_sys_config:
            generals_sys_config = cms.get_system_configuration_item('Generals')
        if not generals_sys_config or not generals_sys_config.get('betSlipAnimation'):
            _has_betslip_animation = False
        elif generals_sys_config.get('betSlipAnimation') == 'On':
            _has_betslip_animation = True
        elif generals_sys_config.get('betSlipAnimation') == 'Off':
            _has_betslip_animation = False
        else:
            _has_betslip_animation = False
        return _has_betslip_animation
    return _has_betslip_animation


def has_betslip_animation():
    status = get_betslip_animation_status()
    return status


def get_cashout_value():
    """
    return: Cashout value
    """
    logs = get_device().get_performance_log()
    for entry in logs[::-1]:
        try:
            payload_data = entry[1]['message']['message']['params']['response']['payloadData']
            if 'initial' in payload_data:
                payload = payload_data.replace('42[', '[')
                break
        except (KeyError, IndexError, AttributeError):
            continue
    data = json.loads(payload)
    cashout_value = data[1]['bets'][0]['cashoutValue']
    return cashout_value
