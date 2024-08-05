import os

from voltron.pages.shared import get_driver
from voltron.utils.exceptions.general_exception import GeneralException
from selenium.webdriver.remote.webelement import WebElement


def get_js_function(function_name):
    try:
        with open(os.path.join(os.path.join(os.path.split(__file__)[0]), 'js_tools', f'{function_name}.js')) as js_file:
            return js_file.read()
    except Exception as e:
        raise GeneralException(f'Error calling "{function_name}" function. {e}')


def set_date_picker(*args, **kwargs):
    driver = get_driver()
    set_date = get_js_function('set_date_for_date_picker')
    return driver.execute_script(set_date, *args)


def remove_readonly(*args, **kwargs):
    driver = get_driver()
    remove_readonly_attr = get_js_function('remove_readonly_attr')
    return driver.execute_script(remove_readonly_attr, *args)


def set_quick_bet_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_quick_bet_value')
    return driver.execute_script(set_value, *args)


def set_betslip_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_betslip_value')
    return driver.execute_script(set_value, *args)


def set_betslip_complex_stake_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_betslip_complex_stake_value')
    return driver.execute_script(set_value, *args)


def get_value(*args, **kwargs):
    driver = get_driver()
    get_value = get_js_function('get_value')
    return driver.execute_script(get_value, *args)


def set_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_value')
    return driver.execute_script(set_value, *args)


def get_css_property_text(*args):
    driver = get_driver()
    css_prop_text = get_js_function('get_css_property_text')
    return driver.execute_script(css_prop_text, *args)


def click(*args, **kwargs):
    driver = get_driver()
    js_click = get_js_function('click')
    return driver.execute_script(js_click, *args)


def mouse_event_click(*args, **kwargs):
    driver = get_driver()
    mouse_click = get_js_function('mouse_event_click')
    return driver.execute_script(mouse_click, *args)


def get_text_excluding_child_nodes_text(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('get_text_excluding_child_nodes_text')
    return driver.execute_script(get_text, *args, **kwargs)


def set_viewport_size(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('set_viewport_size')
    return driver.execute_script(get_text, *args, **kwargs)


def get_data_layer(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('get_data_layer')
    return driver.execute_script(get_text, *args, **kwargs)


def scroll_into_view_above(*args):
    """ use when scroll_to_we() does not help and element is obstructed by elements like sticky desktop header """
    driver = get_driver()
    scroll_up = get_js_function('scroll_into_view_above')
    return driver.execute_script(scroll_up, *args)


def get_location(*args):
    driver = get_driver()
    get_location_ = get_js_function('get_location')
    return driver.execute_script(get_location_, *args)


def natural_mouse_click(*args, **kwargs):
    """
    Simulating natural mouse click
    source of inspiration: https://stackoverflow.com/q/24025165/3574726
    """
    driver = get_driver()
    natural_mouse_click_ = get_js_function('natural_mouse_click')
    return driver.execute_script(natural_mouse_click_, *args, **kwargs)


def scroll_to_center_of_element(*args, **kwargs):
    """ Scrolls to the center of the element"""
    driver = get_driver()
    scroll_up = get_js_function('scroll_to_center_of_element')
    return driver.execute_script(scroll_up, *args, **kwargs)


def get_document_ready_state(*args, **kwargs):
    """ Return of document.readyState """
    driver = get_driver()
    doc_ready = get_js_function('document_ready_state')
    return driver.execute_script(doc_ready, *args, **kwargs)


def get_shadow_root(*args, **kwargs):
    """ Return of shadowRoot """
    driver = get_driver()
    shadow_root = get_js_function('get_shadow_root')
    context_dict = driver.execute_script(shadow_root, *args, **kwargs)
    key, val = context_dict.popitem()
    context = WebElement(driver, val, w3c=True)
    return context


def format_ss_date_to_ui_date(*args, **kwargs):
    driver = get_driver()
    format_date_to_local_date = get_js_function('format_date_to_localdate')
    return driver.execute_script(format_date_to_local_date, *args, **kwargs)


def determine_day(*args, **kwargs):
    driver = get_driver()
    getday = get_js_function('getday')
    return driver.execute_script(getday, *args, **kwargs)

def get_perf_logs():
    driver = get_driver()
    perf_logs = get_js_function('get_perf_logs')
    driver.execute_script(perf_logs)
    start_perf_interception()

def start_perf_interception():
    driver = get_driver()
    driver.execute_script("window.exposeInterceptionMethods().startInterception()")

def stop_perf_interception():
    driver = get_driver()
    driver.execute_script("window.exposeInterceptionMethods().stopInterception()")

def get_perf_websocket():
    start_perf_interception()
    driver = get_driver()
    return driver.execute_script('return window.exposeWebsocketMethods().getInterceptedRequests("WebSocket")')

def get_perf_xhrequests():
    start_perf_interception()
    driver = get_driver()
    return driver.execute_script('return window.exposeWebsocketMethods().getInterceptedRequests("XHR")')

def get_perf_socketIO():
    start_perf_interception()
    driver = get_driver()
    return driver.execute_script('return window.exposeWebsocketMethods().getInterceptedRequests("SocketIO")')

def get_perf_fetch():
    start_perf_interception()
    driver = get_driver()
    return driver.execute_script('return window.exposeWebsocketMethods().getInterceptedRequests("Fetch")')


def delete_popups():
    try:
        selectors = ["#kampyleFormContainer",
                     "#kampyleFormModal",
                     "#kampyleForm2989",
                     "#MDigitalLightboxWrapper",
                     "#onetrust-consent-sdk",
                     "#MDigitalInvitationWrapper",
                     "#MDigitalLightboxWrapper",
                     "script[src='https://cdn.cookielaw.org/scripttemplates/otSDKStub.js']"
                     ]
        driver = get_driver()
        delete_popup = get_js_function('close_popup')
        for selector in selectors:
            driver.execute_script(delete_popup, selector)
    except Exception as e:
        pass