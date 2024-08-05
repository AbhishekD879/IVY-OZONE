import json
import logging
import random
import re
import string
from time import sleep

import requests
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from faker import Faker
from gevent.subprocess import PIPE
from gevent.subprocess import Popen
from requests import HTTPError
from requests import request
from requests import RequestException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from native_ios.pages.shared import get_cms_config
from native_ios.pages.shared import get_driver
from native_ios.pages.shared import get_is_driver_in_iframe
from native_ios.pages.shared import set_driver_in_iframe
from native_ios.pages.shared import set_driver_in_main_page
from native_ios.utils.exceptions.cms_client_exception import CmsClientException
from native_ios.utils.exceptions.device_exception import DeviceException
from native_ios.utils.exceptions.voltron_exception import VoltronException
from native_ios.utils.waiters import wait_for_result

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

_logger = logging.getLogger(name='native_ios_logger')


def parse_selector(selector=''):
    by = {
        'id': MobileBy.ACCESSIBILITY_ID,
        'xpath': MobileBy.XPATH
    }
    matcher = re.match(r'^([a-z]+)=(.+)', selector)
    if matcher is not None and matcher.lastindex == 2:
        sector_type = matcher.group(1)
        selector_string = matcher.group(2)
        if sector_type in by.keys():
            return by[sector_type], selector_string
        else:
            raise VoltronException(f'Unknown selector type [{sector_type}]')
    else:
        raise VoltronException(f"Selector doesn't match pattern 'xpath=//*', given '{selector}'")


def find_element_by_selector(selector='', context=None, bypass_exceptions=(
        NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=10):
    context = context if context else get_driver()
    # ToDo: currently can't find from context because of appium issue
    (by, val) = parse_selector(selector)
    try:
        element = context.find_element(by=by, value=val)
    except NoSuchElementException:
        return wait_for_result(lambda: context.find_element(by=by, value=val),
                               name=f'Waiting for web element to exist by selector "{selector}"',
                               bypass_exceptions=bypass_exceptions,
                               timeout=timeout
                               )
    return element


def find_elements_by_selector(selector, context=None, bypass_exceptions=(
        NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=10):
    context = context if context else get_driver()
    (by, val) = parse_selector(selector)
    try:
        elements = context.find_elements(by=by, value=val)
    except NoSuchElementException:
        elements = wait_for_result(lambda: context.find_elements(by=by, value=val),
                                   name=f'Waiting for web elements to exist by selector "{selector}"',
                                   bypass_exceptions=bypass_exceptions,
                                   timeout=timeout
                                   )
    if elements is None:
        return []
    return elements


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
        raise DeviceException('Error while executing command "%s". Errorcode: "%s", message: "%s"' % (
            terminal_command, cmd.returncode, error))
    pattern = r'^%s \(([A-Z0-9-]+)\) \(\w+\)' % device_name
    # e.g 'iPhone 7 (C78D845C-69F7-4A39-A8DE-A042A0F45113) (Shutdown)'
    device_uuid = next(
        (re.match(pattern, line.strip()).group(1) for line in output.split('\n') if re.match(pattern, line.strip())),
        None)
    if not device_uuid:
        raise DeviceException('Cannot find UUID for %s' % device_name)
    _logger.info('*** Found UUID "%s" for "%s"' % (device_uuid, device_name))
    return device_uuid


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
            if find_elements_by_selector(selector=selector, context=context, timeout=0):
                _logger.debug(f'*** Found active selector "{selector}"')
                return selector

    return wait_for_result(lambda: checker(),
                           name=f'Find any available selector from "{selectors}"',
                           timeout=timeout)


def switch_to_iframe(iframe_selector: str, timeout: int = 5):
    drv = get_driver()

    if not get_is_driver_in_iframe():
        iframe_we = find_element_by_selector(selector=iframe_selector, timeout=timeout)
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
    return number[0:4] + ' ' + 'x' * 4 + ' ' + 'x' * 4 + ' ' + number[12:]


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


def run_terminal_command(command):
    """
    Run a terminal command and capture its output and return code.

    Args:
        command (str): The terminal command to run.

    Returns:
        dict: A dictionary containing the result of the command execution.
            - "success" (bool): True if the command executed successfully, False otherwise.
            - "output" (str): The standard output of the command (empty string if no output).
            - "error_message" (str): The error message if the command failed (empty string if no error).

    Raises:
        Exception: If there is an unexpected error during command execution.

    Example usage:
    >>> result = run_terminal_command("ls -l")
    >>> if result["success"]:
    ...     print("Command executed successfully.")
    ...     print("Standard Output:")
    ...     print(result["output"])
    ... else:
    ...     print("Command failed with an error:")
    ...     print(result["error_message"])
    """
    try:
        # Run the command in the terminal
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        stdout, stderr = process.communicate()

        # Check the return code
        if process.returncode == 0:
            return {
                "success": True,
                "output": stdout.strip()  # Remove leading/trailing whitespace
            }
        else:
            return {
                "success": False,
                "error_message": stderr.strip()  # Remove leading/trailing whitespace
            }
    except Exception as e:
        return {
            "success": False,
            "error_message": str(e)
        }


def tap_at_coordinates(x=None, y=None):
    sleep(5)
    action = TouchAction(
        get_driver())
    action.tap(None, x=x, y=y).perform()
    sleep(5)
